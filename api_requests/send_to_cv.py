import asyncio
import json

from collections import defaultdict
import time
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, exists

from api_models.Cleverence.Products import Product
from api_models.Cleverence.Contragents import Contragent
from api_models.Cleverence.Tables_SpisokDokumentov import SpisokDokumentov
from api_models.Cleverence.Warehouse import Warehouse
from api_models.Supermag import IOSMIOSTORELOCATIONS, IOUSIOSMCONTRAGENT, OR
from api_requests.get_from_cv import (
    get_docs_podbor_docs,
    get_tables_podbor_docs,
    get_header_postuplenie,
)
from api_requests.get_from_sm import get_request, get_mesabbrev
from db_connections.oramodels import SMStoreUnits, SMCard
from db_connections.db_conf import session
from config_urls import (
    products_url,
    begin_product,
    end_product,
    contragents_url,
    begin_contragent,
    end_contragent,
    storelocs_sm_url,
    contragents_sm_url,
    begin_tables_spisokdokumentov,
    tables_spisokdokumentov,
    end_tables_spisokdokumentov,
    gruppovayapriemka_url,
    postuplenie_docline_list,
)
from config_urls import postuplenie_url, warehouse_url
from api_models.Cleverence.Postuplenie import Postuplenie, DocumentItem
from utils.local_db_utils import generate_document_number
from utils.requests import post_request, delete_request

gmt5 = timezone(timedelta(hours=5))


async def load_card(article):
    # Загрузка карточки на сервер Клеверенс
    # Получаем данные из базы
    full_request = (
        select(
            SMCard.article,
            SMCard.shortname,
            SMCard.mesabbrev,
            SMStoreUnits.unitname,
            SMStoreUnits.barcode,
            SMStoreUnits.quantity,
        )
        .join(SMStoreUnits, SMCard.article == SMStoreUnits.article)
        .where(SMStoreUnits.article == article)
        .order_by(SMStoreUnits.unitname)
    )
    result = session.execute(full_request)
    dict_iterator = result.mappings()

    # Получаем список словарей
    results = list(dict_iterator)

    # создание defaultdict с функцией list
    dict_packeges = defaultdict(list)

    # Создаем пустые переменные
    packing_list = []
    default_barcode = ""

    # Проверяем наличие кол-ва для упаковок в карточке (у весовых может отсутсвовать, поэтому отсекаем.)
    if not any(data["quantity"] is None for data in results):
        # цикл по списку словарей
        for card in results:
            # добавление barcode в список по ключу unitname
            if card["mesabbrev"] == card["unitname"]:
                pack_name = card["mesabbrev"]
            else:
                pack_name = card["unitname"] + "_" + str(card["quantity"])
            dict_packeges[pack_name].append(card["barcode"])

        # Получаем кол-во в упаковке которое зашифровали на предыдущем шаге (пока ничего лучше не придумал.)
        for pack, barcode in dict_packeges.items():
            pack_qnty = pack.split("_")
            if len(pack_qnty) != 1:
                pack_qnty = pack_qnty[-1]
            else:
                pack_qnty = 1
                default_barcode = barcode[0]

            # Формируем словарь с упаковками с полученными ранее данными
            packing = {
                "name": pack,
                "unitsQuantity": pack_qnty,
                "barcodes": barcode,
                "id": pack,
            }
            packing_list.append(packing)

    else:
        pack = results[0]["mesabbrev"]
        packing = {
            "name": pack,
            "unitsQuantity": 1,
            "id": pack,
        }
        packing_list.append(packing)

    #    Формирование json
    product = Product(
        id=article,
        name=results[0]["shortname"],
        packings=packing_list,
        barcode=default_barcode,
        basePackingId=results[0]["mesabbrev"],
        marking=article,
    )

    session.close()

    # Конвертируем объект в JSON-формат
    product_json = product.model_dump_json(exclude_none=True)
    # Отправляем данные на сервер.
    await post_request(products_url, product_json)


async def send_contragents():
    await post_request(begin_contragent)
    url = contragents_sm_url
    data_request = await get_request(url)
    if "data_text" in data_request:
        dictionary = json.loads(data_request[1])
        data_model = IOUSIOSMCONTRAGENT.DataModel(**dictionary)
        count = 0
        for d in data_model:

            data = d[1].POSTOBJECT[0].IOUSIOSMCONTRAGENT.USIOSMCONTRAGENT
            for row in data:
                count += 1
                contragents = Contragent(
                    uid=str(row.ID),
                    naimenovanie=row.NAME,
                    etoPapka=False,
                    iNN=row.INN,
                    naimenovanieDlyaPoiska=row.NAME,
                    id=str(row.ID),
                )

                contragents_json = contragents.model_dump_json(exclude_none=True)
                # Отправляем данные на сервер.
                await post_request(contragents_url, contragents_json)
        await post_request(end_contragent)
        return f"Загружено {count} контрагентов"


async def send_articles():
    # Загрузка справочника товаров в Клеверенс
    start_time = time.time()

    print("Начало загрузки данных")

    # Передаем на сервер запрос на обновление справочника
    await post_request(begin_product)

    # получаем список всех article, удовлетворяющих условиям
    query = select(SMCard.article).where(
        SMCard.receiptok == 1,
        SMCard.accepted == 1,
        exists().where(SMCard.article == SMStoreUnits.article),
    )
    cards = session.execute(query).fetchall()
    counter = 0
    # отправляем данные на сервер
    for article in cards:
        counter += 1
        await load_card(article[0])
    await post_request(end_product)

    # Замеряем время загрузки
    end_time = time.time()
    execution_time = (end_time - start_time) / 60

    print("Загрузка данных закончена")
    print(f"Время выполнения: {execution_time}")
    return f"Загружено {counter} SKU"


async def send_storeloc():
    url = storelocs_sm_url
    data_request = await get_request(url)
    if "data_text" in data_request:
        dictionary = json.loads(data_request[1])
        data_mod = IOSMIOSTORELOCATIONS.DataModel(**dictionary)
        count = 0
        for d in data_mod:
            locs = d[1].POSTOBJECT[0].IOSMIOSTORELOCATIONS.SMIOSTORELOCATIONS
            for loc in locs:
                if loc.sClassTree[0] == "1":
                    count += 1
                    warehouse = Warehouse(
                        storageId=str(loc.iLocID), id=str(loc.iLocID), name=loc.sLocName
                    )
                    warehouse_json = warehouse.model_dump_json(exclude_none=True)
                    print(warehouse_json)
                    await post_request(warehouse_url, warehouse_json)
    return f"Выгружено {count} магазинов"


async def get_docs_of_dates(days: int):
    docs_list = []
    data_request = await get_request(postuplenie_url)
    if "data_json" in data_request:
        # Создание осведомлённого объекта datetime по GMT+5
        gmt_plus_five = timezone(timedelta(hours=5))
        cutoff_date = datetime.now(gmt_plus_five) - timedelta(days=days)
        for data in data_request[1]["value"]:
            doclist = Postuplenie(**data)
            # Проверка, что createDate в формате datetime с tzinfo
            # Если createDate меньше или равно дате отсечки, добавляем в список
            if doclist.createDate <= cutoff_date:
                docs_list.append((doclist.id, doclist.createDate))
            else:
                print("Произошла ошибка при запросе на сервер")
    return docs_list


async def clear_old_docs(days):
    docs_id = await get_docs_of_dates(days)
    count = 0
    for doc in docs_id:
        await delete_request(url=postuplenie_url, doc_id=doc[0])
        count += 1
    return f"Очищено {count} документов"


async def send_or_to_cv(doc_dict):
    data = OR.Data(**doc_dict)
    # получаем список постобъектов
    postobjects = data.PACKAGE.POSTOBJECT
    doc_list = []
    for postobject in postobjects:
        docdata = postobject.OR.SMDOCUMENTS[0]
        docitems = postobject.OR.SMSPECOR
        ourselfclient = postobject.OR.SMDOCOR[0].OURSELFCLIENT
        original_datetime = postobject.OR.SMDOCUMENTS[0].CREATEDAT
        docprops = (
            (postobject.OR.SMDOCPROPS[0].PARAMVALUE or [])
            if postobject.OR.SMDOCPROPS
            else None
        )
        formatted_datetime = original_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")
        timezone_info = datetime.now(timezone.utc).astimezone().strftime("%z")
        formatted_datetime_with_timezone = f"{formatted_datetime}{timezone_info}"
        # Получаем строки документа
        spec_list = []
        spec_id = 0
        for items in docitems:
            spec_id += 1
            result_id = str(spec_id if not items.SPECITEM else items.SPECITEM)
            mesabbr = await get_mesabbrev(items.ARTICLE)
            spec_items = DocumentItem(
                nomerStrokiDokumenta=result_id,
                # uid=str(items.SPECITEM),
                productId=items.ARTICLE,
                declaredQuantity=items.QUANTITY,
                idEdinicyIzmereniya=mesabbr,
                packingId=mesabbr,
                cena=items.ITEMPRICE,
                CenaPriemki=items.ITEMPRICE,
                # priceTotal=items.TOTALPRICE
            )
            spec_list.append(spec_items)
        doc_list.append(docdata.ID)
        # Получаем шапку документа
        doc = Postuplenie(
            id=docdata.ID,
            name=f"Прием ТСД по заказу: {docdata.ID}",
            createDate=formatted_datetime_with_timezone,
            warehouseId=str(docdata.LOCATION),
            idKontragenta=str(docdata.CLIENTINDEX),
            summaDokumenta=docdata.TOTALSUM,
            declaredItems=spec_list,
            selfclient=ourselfclient,
            barcode=docprops,
        )
        postuplenie_json = doc.model_dump_json(exclude_none=True)
        await post_request(postuplenie_url, postuplenie_json)
        spisokdok = SpisokDokumentov(
            docid=docdata.ID,
            uid=docdata.ID,
            docdate=formatted_datetime_with_timezone,
            docType="Postuplenie",
            docBarcode=docprops,
            idKontragenta=str(docdata.CLIENTINDEX),
            summaDokumenta=docdata.TOTALSUM,
            warehouseId=str(docdata.LOCATION),
        )
        spisokdokumentov_json = spisokdok.model_dump_json(exclude_none=True)
        await post_request(begin_tables_spisokdokumentov)
        await post_request(tables_spisokdokumentov, spisokdokumentov_json)
        await post_request(end_tables_spisokdokumentov)
    if doc_list:
        return doc_list
    else:
        return "nothing"


async def clean_tables_list(days=7):
    data_request = await get_request(tables_spisokdokumentov)
    gmt_plus_five = timezone(timedelta(hours=5))
    cutoff_date = str(datetime.now(gmt_plus_five) - timedelta(days=days))
    if "data_json" in data_request:
        count = 0
        for data in data_request[1]["value"]:
            doc_list = SpisokDokumentov(**data)
            if doc_list.docdate <= cutoff_date:
                await delete_request(url=tables_spisokdokumentov, doc_id=doc_list.uid)
                count += 1
            return f"Очищено {count} строк"
    else:
        return "Нет строк для очистки"


async def create_doc_gruppovayapriemka(doc_list_id):
    # print(doc_list_id)
    spec_list = []
    warehouse_id = 0
    summa_doc = 0
    ourselfclient = 0
    formatted_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    timezone_info = datetime.now(timezone.utc).astimezone().strftime("%z")
    formatted_datetime_with_timezone = f"{formatted_datetime}{timezone_info}"
    for doc_id in doc_list_id:
        podbor_doc_url = postuplenie_docline_list.format(doc_id=doc_id)
        data_lines_request = await get_request(podbor_doc_url)
        if "data_json" in data_lines_request:
            for data_lines in data_lines_request[1]["value"]:
                data_docs = DocumentItem(**data_lines)
                spec_items = DocumentItem(
                    nomerStrokiDokumenta=data_docs.nomerStrokiDokumenta,
                    productId=data_docs.productId,
                    declaredQuantity=data_docs.declaredQuantity,
                    idEdinicyIzmereniya=data_docs.packingId,
                    packingId=data_docs.packingId,
                    cena=data_docs.cena,
                    CenaPriemki=data_docs.cena,
                    idDokumenta=doc_id,
                )
                spec_list.append(spec_items)
        # Получаем шапку документа
        request_data = await get_header_postuplenie(doc_id)
        if request_data:
            summa_doc += request_data[1]
            warehouse_id = request_data[0]
    id_doc = generate_document_number("GTMP", warehouse_id)
    doc = Postuplenie(
        id=id_doc,
        name=f"Групповая приемка от: {formatted_datetime}",
        createDate=formatted_datetime_with_timezone,
        warehouseId=str(warehouse_id),
        summaDokumenta=summa_doc,
        declaredItems=spec_list,
        selfclient=ourselfclient,
        documentTypeName="Групповая приемка",
    )
    postuplenie_json = doc.model_dump_json(indent=4, exclude_none=True)
    if await post_request(gruppovayapriemka_url, postuplenie_json):
        return True
    else:
        return False


async def exchange_podbor_doc():
    docs_count = 0
    podbor_list = await get_docs_podbor_docs()
    if podbor_list:
        for doc_id in podbor_list:
            doclist = await get_tables_podbor_docs(doc_id)
            if doclist:
                docs_count += 1
                if await create_doc_gruppovayapriemka(doclist):
                    pass
                    await delete_request(gruppovayapriemka_url, doc_id)
                else:
                    return "Произошла ошибка!"
        return f"Сформировано документов: {docs_count}"
    else:
        return "Нет документов"


if __name__ == "__main__":
    asyncio.run(exchange_podbor_doc())
    pass
    # asyncio.run(send_articles())
