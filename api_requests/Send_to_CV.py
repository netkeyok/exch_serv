import asyncio
import json

import aiohttp
from collections import defaultdict
import time
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, exists

from api_models.Cleverence.Products import Product
from api_models.Cleverence.Contragents import Contragent
from api_models.Cleverence.Warehouse import Warehouse
from api_models.Supermag import IOSMIOSTORELOCATIONS, IOUSIOSMCONTRAGENT, OR
from api_requests.get_from_sm import get_request, get_mesabbrev
from db_connections.oramodels import SMStoreUnits, SMCard, SMClientInfo, SMDocuments, SMStoreLocations, SMSpecor
from db_connections.db_conf import session
from config_urls import products_url, begin_product, end_product, contragents_url, begin_contragent, end_contragent, \
    header, storelocs_sm_url, contragents_sm_url
from config_urls import postuplenie_url, warehouse_url, ticket_url

from api_models.Cleverence.Postuplenie import Postuplenie, DocumentItem

gmt5 = timezone(timedelta(hours=5))


async def send_request(url, js_data):
    # асинхронная функция для отправки запроса на сервер api

    # Создаем сессию клиента с помощью асинхронного менеджера контекста
    async with aiohttp.ClientSession() as sessionapi:
        # Отправляем POST-запрос с JSON-данными на сервер api с помощью асинхронного менеджера контекста
        async with sessionapi.post(url, data=js_data, headers=header) as response:
            # Получаем статус и текст ответа
            status = response.status
            text = await response.text()
            # Проверяем статус ответа и выводим результат
            if status not in (200, 201, 204):
                print(js_data)
                print('Произошла ошибка при добавлении продукта на сервер')
                print(status)
                print(response)
    return text


async def read_request_sm(ticket):
    """
    Read the status of a ticket in the SM system.

    Args:
        ticket (str): The ticket number.

    Returns:
        str: The response text.

    Raises:
        ValueError: If the ticket is invalid.
    """
    # Validate the ticket parameter
    if not ticket:
        raise ValueError("Invalid ticket")

    url = f"{ticket_url}{ticket}"
    text = ''
    try:
        async with aiohttp.ClientSession() as sessionapi:
            async with sessionapi.get(url, headers=header) as response:
                status = response.status
                if status == 200:
                    text = await response.text()
                else:
                    text = f"Request failed with status code {status}"
    except Exception as e:
        print(f"An error occurred during the HTTP request: {e}")
    return text


async def load_card(article):
    # Загрузка карточки на сервер Клеверенс

    # Получаем данные из базы
    full_request = select(
        SMCard.article,
        SMCard.shortname,
        SMCard.mesabbrev,
        SMStoreUnits.unitname,
        SMStoreUnits.barcode,
        SMStoreUnits.quantity,
    ).join(SMStoreUnits, SMCard.article == SMStoreUnits.article).where(
        SMStoreUnits.article == article).order_by(SMStoreUnits.unitname)
    result = session.execute(full_request)
    dict_iterator = result.mappings()

    # Получаем список словарей
    results = list(dict_iterator)

    # создание defaultdict с функцией list
    dict_packeges = defaultdict(list)

    # Создаем пустые переменные
    packing_list = []
    default_barcode = ''

    # Проверяем наличие кол-ва для упаковок в карточке (у весовых может отсутсвовать, поэтому отсекаем.)
    if not any(data['quantity'] is None for data in results):
        # цикл по списку словарей
        for card in results:
            # добавление barcode в список по ключу unitname
            if card['mesabbrev'] == card['unitname']:
                pack_name = card['mesabbrev']
            else:
                pack_name = card['unitname'] + '_' + str(card['quantity'])
            dict_packeges[pack_name].append(card['barcode'])

        # Получаем кол-во в упаковке которое зашифровали на предыдущем шаге (пока ничего лучше не придумал.)
        for pack, barcode in dict_packeges.items():
            pack_qnty = pack.split('_')
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
        pack = results[0]['mesabbrev']
        packing = {
            "name": pack,
            "unitsQuantity": 1,
            "id": pack,
        }
        packing_list.append(packing)

    #    Формирование json
    product = Product(
        id=article,
        name=results[0]['shortname'],
        packings=packing_list,
        barcode=default_barcode,
        basePackingId=results[0]['mesabbrev'],
        marking=article
    )

    session.close()

    # Конвертируем объект в JSON-формат
    product_json = product.model_dump_json(exclude_none=True)
    # Отправляем данные на сервер.
    await send_request(products_url, product_json)


# async def load_contragents():
#     # Загрузка справочника контрагентов в Клеверенс
#
#     await send_request(begin_contragent, None)
#     query = select(SMClientInfo.id,
#                    SMClientInfo.name,
#                    SMClientInfo.inn).where(SMClientInfo.accepted == '1')
#     result = session.execute(query)
#
#     dict_iterator = result.mappings()
#
#     # Получаем список словарей
#     results = list(dict_iterator)
#     for data in results:
#         # print(data)
#
#         contragents = Contragent(
#             uid=str(data['id']),
#             naimenovanie=data['name'],
#             etoPapka=False,
#             iNN=data['inn'],
#             naimenovanieDlyaPoiska=data['name'],
#             id=str(data['id'])
#         )
#
#         contragents_json = contragents.model_dump_json(exclude_none=True)
#         print(contragents_json)
#         # Отправляем данные на сервер.
#         await send_request(contragents_url, contragents_json)
#     session.close()
#     await send_request(end_contragent, None)
async def send_contragents():
    await send_request(begin_contragent, None)
    data_request = await get_request(contragents_sm_url)
    dictionary = json.loads(data_request)
    data_model = IOUSIOSMCONTRAGENT.DataModel(**dictionary)
    for d in data_model:
        data = d[1].POSTOBJECT[0].IOUSIOSMCONTRAGENT.USIOSMCONTRAGENT
        for row in data:
            contragents = Contragent(
                uid=str(row.ID),
                naimenovanie=row.NAME,
                etoPapka=False,
                iNN=row.INN,
                naimenovanieDlyaPoiska=row.NAME,
                id=str(row.ID)
            )

            contragents_json = contragents.model_dump_json(exclude_none=True)
            print(contragents_json)
            # Отправляем данные на сервер.
            await send_request(contragents_url, contragents_json)
    await send_request(end_contragent, None)


async def send_articles():
    # Загрузка справочника товаров в Клеверенс
    start_time = time.time()

    print('Начало загрузки данных')

    # Передаем на сервер запрос на обновление справочника
    await send_request(begin_product, None)

    # получаем список всех article, удовлетворяющих условиям
    query = select(SMCard.article).where(SMCard.receiptok == 1,
                                         SMCard.accepted == 1,
                                         exists().where(SMCard.article == SMStoreUnits.article))
    cards = session.execute(query).fetchall()
    counter = 0
    # отправляем данные на сервер
    for article in cards:
        counter += 1
        await load_card(article[0])
    await send_request(end_product, None)

    # Замеряем время загрузки
    end_time = time.time()
    execution_time = (end_time - start_time) / 60

    print('Загрузка данных закончена')
    print(f'Время выполнения: {execution_time}')
    return f'Загружено {counter} SKU'


# Отправка документов на сервер.
# async def send_postuplenie(docid=None):
#     # Загрузка документов поступление в Клеверенс, если не установлен номер документа, грузятся все документы,
#     # которые соотвествуют условию отбора
#
#     # Фильтр по дате, при загрузке всех документов.
#     days_ago = datetime.now() - timedelta(days=2)
#     # Если указан номер документа, то грузим строго по номеру. Номер получаем по API от СМ.
#     if docid:
#         query = (
#             select(SMDocuments.ID,
#                    SMDocuments.LOCATION,
#                    SMDocuments.CREATEDAT,
#                    SMDocuments.CLIENTINDEX,
#                    SMDocuments.TOTALSUM)
#             .where(SMDocuments.ID == docid)
#         )
#     else:
#         query = (
#             select(SMDocuments.ID,
#                    SMDocuments.LOCATION,
#                    SMDocuments.CREATEDAT,
#                    SMDocuments.CLIENTINDEX,
#                    SMDocuments.TOTALSUM)
#             .where(SMDocuments.DOCTYPE.in_(['OR']),
#                    SMDocuments.DOCSTATE.in_(['2']),
#                    SMDocuments.CREATEDAT.between(days_ago, datetime.now())
#                    )
#         )
#     result = session.execute(query)
#     dict_iterator = result.mappings()
#
#     # Получаем список словарей
#     results = list(dict_iterator)
#
#     # проходим по списку и отправляем на сервер.
#     for result in results:
#         original_datetime = result['CREATEDAT']
#         # Преобразование в нужный формат
#         formatted_datetime = original_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")
#         timezone_info = datetime.now(timezone.utc).astimezone().strftime("%z")
#         formatted_datetime_with_timezone = f"{formatted_datetime}{timezone_info}"
#         items = await send_postuplenie_items(result['ID'])
#         doc = Postuplenie(
#             id=result['ID'],
#             name=f"Прием ТСД по заказу: {result['ID']}",
#             createDate=formatted_datetime_with_timezone,
#             warehouseId=str(result['LOCATION']),
#             idKontragenta=str(result['CLIENTINDEX']),
#             summaDokumenta=result['TOTALSUM'],
#             declaredItems=items
#         )
#         postuplenie_json = doc.model_dump_json(exclude_none=True)
#         # print(postuplenie_json)
#         await send_request(postuplenie_url, postuplenie_json)


# async def send_storeloc():
#     # Загрузка справочников мест хранения в Клеверенс
#     query = (
#         select(SMStoreLocations.ID,
#                SMStoreLocations.NAME,
#                )
#         .where(SMStoreLocations.ACCEPTED == 1)
#     )
#     result = session.execute(query)
#     dict_iterator = result.mappings()
#
#     # Получаем список словарей
#     results = list(dict_iterator)
#
#     for result in results:
#         print(result)
#         warehouse = Warehouse(
#             storageId=str(result['ID']),
#             id=str(result['ID']),
#             name=result['NAME']
#         )
#         warehouse_json = warehouse.model_dump_json(exclude_none=True)
#         await send_request(warehouse_url, warehouse_json)

async def send_storeloc():
    data_request = await get_request(storelocs_sm_url)
    dictionary = json.loads(data_request)
    data_mod = IOSMIOSTORELOCATIONS.DataModel(**dictionary)
    for d in data_mod:
        locs = d[1].POSTOBJECT[0].IOSMIOSTORELOCATIONS.SMIOSTORELOCATIONS
        for loc in locs:
            if loc.sClassTree[0] == '1':
                warehouse = Warehouse(
                    storageId=str(loc.iLocID),
                    id=str(loc.iLocID),
                    name=loc.sLocName
                )
                warehouse_json = warehouse.model_dump_json(exclude_none=True)
                print(warehouse_json)
                await send_request(warehouse_url, warehouse_json)


async def clear_postuplenie(doc_id):
    async with aiohttp.ClientSession() as sessionapi:
        try:
            del_url_with_id = f'{postuplenie_url}({doc_id})'
            async with sessionapi.delete(del_url_with_id) as del_response:
                print(del_response.status)
        except Exception as e:
            print(f'An error occurred: {e}')
    await sessionapi.close()


# async def send_postuplenie_items(docid):
#     # Формирование списка позиций накладной
#     query = (
#         select(SMSpecor.ARTICLE,
#                SMSpecor.SPECITEM,
#                SMSpecor.DISPLAYITEM,
#                SMSpecor.QUANTITY,
#                SMSpecor.ITEMPRICE,
#                SMSpecor.TOTALPRICE
#                )
#         .where(SMSpecor.DOCID == docid)
#     )
#     result = session.execute(query)
#     dict_iterator = result.mappings()
#
#     # Получаем список словарей
#     results = list(dict_iterator)
#     spec_list = []
#     for result in results:
#         spec_items = DocumentItem(
#             uid=str(result['SPECITEM']),
#             productId=result['ARTICLE'],
#             declaredQuantity=result['QUANTITY'],
#             price=result['ITEMPRICE'],
#             priceTotal=result['TOTALPRICE']
#         )
#         spec_list.append(spec_items)
#     return spec_list


# async def get_finalized_doc():
#     # Получить список документов завершенных на ТСД
#     async with aiohttp.ClientSession() as sessionapi:
#         # Отправляем POST-запрос с JSON-данными на сервер api с помощью асинхронного менеджера контекста
#         async with sessionapi.get(postuplenie_url, headers=header) as response:
#             # Получаем кодировку, статус и текст ответа асинхронно с помощью await
#             status = response.status
#             data_js = await response.json()
#             data_list = data_js['value']
#             for data in data_list:
#                 doclist = Postuplenie(**data)
# #                 if doclist.finished:
#                 print(doclist.id, doclist.createDate)
#                 # print(f"{postuplenie_url}('{doclist.id}')/declaredItems")
#             print(status)
#             # Проверяем статус ответа и выводим результат
#             if status not in (200,):
#                 print('Произошла ошибка при запросе на сервер')
#                 print(status)
#                 print(response)


# Используется в асинхронной функции для получения недавних документов
async def get_finalized_doc(days: int):
    docs_list = []
    async with aiohttp.ClientSession() as sessionapi:
        async with sessionapi.get(postuplenie_url, headers=header) as response:
            status = response.status
            if status == 200:
                data_js = await response.json()
                data_list = data_js['value']
                # Создание осведомлённого объекта datetime по GMT+5
                gmt_plus_five = timezone(timedelta(hours=5))
                cutoff_date = datetime.now(gmt_plus_five) - timedelta(days=days)
                for data in data_list:
                    doclist = Postuplenie(**data)
                    # Проверка, что createDate в формате datetime с tzinfo
                    # Если createDate меньше или равно дате отсечки, добавляем в список
                    if doclist.createDate <= cutoff_date:
                        docs_list.append((doclist.id, doclist.createDate))
            else:
                print('Произошла ошибка при запросе на сервер')
                print(status)
    return docs_list


async def send_or_to_cv(doc_dict):
    data = OR.Data(**doc_dict)
    # получаем список постобъектов
    # print(data)
    postobjects = data.PACKAGE.POSTOBJECT
    for postobject in postobjects:
        docdata = postobject.OR.SMDOCUMENTS[0]
        docitems = postobject.OR.SMSPECOR
        ourselfclient = postobject.OR.SMDOCOR[0].OURSELFCLIENT
        original_datetime = postobject.OR.SMDOCUMENTS[0].CREATEDAT

        formatted_datetime = original_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")
        timezone_info = datetime.now(timezone.utc).astimezone().strftime("%z")
        formatted_datetime_with_timezone = f"{formatted_datetime}{timezone_info}"
        # Получаем строки документа
        spec_list = []
        for items in docitems:
            mesabbr = await get_mesabbrev(items.ARTICLE)
            spec_items = DocumentItem(
                uid=str(items.SPECITEM),
                productId=items.ARTICLE,
                declaredQuantity=items.QUANTITY,
                idEdinicyIzmereniya=mesabbr,
                packingId=mesabbr,
                cena=items.ITEMPRICE,
                priceTotal=items.TOTALPRICE
            )
            spec_list.append(spec_items)

        # Получаем шапку документа
        doc = Postuplenie(
            id=docdata.ID,
            name=f"Прием ТСД по заказу: {docdata.ID}",
            createDate=formatted_datetime_with_timezone,
            warehouseId=str(docdata.LOCATION),
            idKontragenta=str(docdata.CLIENTINDEX),
            summaDokumenta=docdata.TOTALSUM,
            declaredItems=spec_list,
            selfclient=ourselfclient
        )
        postuplenie_json = doc.model_dump_json(exclude_none=True)
        await send_request(postuplenie_url, postuplenie_json)


if __name__ == '__main__':
    # asyncio.run(load_card('014073'))
    asyncio.run(send_articles())
    # asyncio.run(send_contragents())
    # asyncio.run(send_postuplenie('7ORA-E643252'))
    # asyncio.run(send_storeloc())
    # asyncio.run(clear_postuplenie('28ORA-E660518'))
    # data = asyncio.run(get_finalized_doc(2))
    # print(data)
    # for d in data:
    #     print(d[0])
        # asyncio.run(clear_postuplenie(d[0]))
    # asyncio.run(permitdel())
    # asyncio.run(read_request_sm('23fa886b-4aea-4b12-a697-9e6cb8d0f7df'))
    pass
