import asyncio
from datetime import datetime

import aiohttp
import json
import xml.etree.ElementTree as ET
from api_models.Supermag.WI import Data, Package, Item, WI, SMDocuments
from api_models.Supermag.WI import SMCommonbases, SMWaybillIn, SMSpec, SLSpecqmismatch
from api_models.Cleverence.Postuplenie import Postuplenie, DocumentItem
from config_urls import postuplenie_url, header, supermag_in_url, PostuplenieRuchnoe
from utils.db_functions import generate_number, send_post
from utils.requests import post_request, read_request_sm, delete_request, get_request


# async def send_wi():
#     print("Start sending WI")
#     result = 'Nothing to send'
#     async with aiohttp.ClientSession() as sessionapi:
#         # Отправляем POST-запрос с JSON-данными на сервер api с помощью асинхронного менеджера контекста
#         async with sessionapi.get(postuplenie_url, headers=header) as response:
#             # async with sessionapi.get(PostuplenieRuchnoe, headers=header) as response:
#             data_js = await response.json()
#             data_list = data_js['value']
#             for data in data_list:
#                 doclist = Postuplenie(**data)
#                 if doclist.finished:
#                     cv_date = doclist.createDate.strftime("%Y-%m-%dT%H:%M:%S")
#                     date_doc = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
#                     wi_id = generate_number(doclist.warehouseId)
#                     items = await get_wi_items(doclist.id, wi_id)
#                     # Создаем экземпляр модели
#                     wi_data = Data(
#                         PACKAGE=Package(
#                             name="package",
#                             POSTOBJECT=[
#                                 Item(
#                                     description="Приходная накладная",
#                                     action="normal",
#                                     Id=f'WI{wi_id}',
#                                     WI=WI(
#                                         SMDOCUMENTS=[
#                                             SMDocuments(
#                                                 ID=wi_id,
#                                                 DOCTYPE="WI",
#                                                 BORNIN="zW3taivnRyidInB3UjAdZQ00",
#                                                 CLIENTINDEX=doclist.idKontragenta,
#                                                 COMMENTARY=doclist.name,
#                                                 CREATEDAT=date_doc,
#                                                 CURRENCYMULTORDER=0,
#                                                 CURRENCYRATE=1.0,
#                                                 CURRENCYTYPE=1,
#                                                 DOCSTATE=1,
#                                                 ISROUBLES="1",
#                                                 LOCATIONTO=doclist.warehouseId,
#                                                 OPCODE="0",
#                                                 PRICEROUNDMODE=3,
#                                                 TOTALSUM=sum(items[2]),
#                                                 TOTALSUMCUR=sum(items[2]),
#                                             )],
#                                         SMCOMMONBASES=[
#                                             SMCommonbases(
#                                                 ID=wi_id,
#                                                 DOCTYPE="WI",
#                                                 BASEDOCTYPE="OR",
#                                                 BASEID=doclist.id,
#                                             )],
#                                         SMSPEC=items[0],
#                                         SLSPECQMISMATCH=items[1],
#                                         SMWAYBILLSIN=[
#                                             SMWaybillIn(
#                                                 ID=wi_id,
#                                                 DOCTYPE="WI",
#                                                 GOODSOWNER=0,
#                                                 OURSELFCLIENT=doclist.selfclient,
#                                                 PAYCASH="0",
#                                                 # SUPPLDOCSUM=doclist.summaDokumenta,  # Сумма по документу поставщика
#                                                 SUPPLDOCSUM=doclist.summaDokumenta if doclist.summaDokumenta is not None else 0,
#                                                 SUPPLIERDOC=doclist.id,  # Номер документа поставщика
#                                                 SUPPLIERDOCCREATE=cv_date,  # Дата документа поставщика
#
#                                             )
#                                         ]
#                                     )
#                                 )
#                             ]
#                         )
#                     )
#
#                     # Получаем словарь из экземпляра модели
#                     data_dict = wi_data.dict()
#
#                     # Получаем JSON строку из словаря
#                     data_json = json.dumps(data_dict, indent=4)
#
#                     # print(data_json)
#                     text = await post_request(supermag_in_url, data_json)
#                     print(data_json, text)
#                     if text:
#                         ticket = ET.fromstring(text)
#                         ticket_id = ticket.find('ticketId').text
#                         while True:
#                             request_text = await read_request_sm(ticket_id)
#                             await asyncio.sleep(0.5)
#                             states = ET.fromstring(request_text)
#                             # print(request_text)
#                             state = states.find('state').text
#                             # print(state)
#                             if state == 'Success':
#                                 print(wi_id, doclist.warehouseId)
#                                 send_post(doclist.warehouseId, wi_id)
#                                 result = f'send doc {wi_id}'
#                                 await delete_request(url=postuplenie_url, doc_id=doclist.id)
#                                 break
#                             elif state not in ('Success', 'Handling', 'Queued'):
#                                 result = f"Документ не обработан статус: {state}"
#                                 raise ValueError(f"Документ не обработан статус: {state}")
#     return result

async def send_wi():
    print("Start sending WI")
    result = 'Nothing to send'
    data_request = await get_request(postuplenie_url)
    if 'data_json' in data_request:
        for data_js in data_request[1]["value"]:
            doclist = Postuplenie(**data_js)
            if doclist.finished:
                cv_date = doclist.createDate.strftime("%Y-%m-%dT%H:%M:%S")
                date_doc = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                # print(doclist.warehouseId)
                wi_id = generate_number(doclist.warehouseId)
                items = await get_wi_items(doclist.id, wi_id)
                # Создаем экземпляр модели
                wi_data = Data(
                    PACKAGE=Package(
                        name="package",
                        POSTOBJECT=[
                            Item(
                                description="Приходная накладная",
                                action="normal",
                                Id=f'WI{wi_id}',
                                WI=WI(
                                    SMDOCUMENTS=[
                                        SMDocuments(
                                            ID=wi_id,
                                            DOCTYPE="WI",
                                            BORNIN="zW3taivnRyidInB3UjAdZQ00",
                                            CLIENTINDEX=doclist.idKontragenta,
                                            COMMENTARY=doclist.name,
                                            CREATEDAT=date_doc,
                                            CURRENCYMULTORDER=0,
                                            CURRENCYRATE=1.0,
                                            CURRENCYTYPE=1,
                                            DOCSTATE=1,
                                            ISROUBLES="1",
                                            LOCATIONTO=doclist.warehouseId,
                                            OPCODE="0",
                                            PRICEROUNDMODE=3,
                                            TOTALSUM=sum(items[2]),
                                            TOTALSUMCUR=sum(items[2]),
                                        )],
                                    SMCOMMONBASES=[
                                        SMCommonbases(
                                            ID=wi_id,
                                            DOCTYPE="WI",
                                            BASEDOCTYPE="OR",
                                            BASEID=doclist.id,
                                        )],
                                    SMSPEC=items[0],
                                    SLSPECQMISMATCH=items[1],
                                    SMWAYBILLSIN=[
                                        SMWaybillIn(
                                            ID=wi_id,
                                            DOCTYPE="WI",
                                            GOODSOWNER=0,
                                            OURSELFCLIENT=doclist.selfclient,
                                            PAYCASH="0",
                                            # SUPPLDOCSUM=doclist.summaDokumenta,  # Сумма по документу поставщика
                                            SUPPLDOCSUM=doclist.summaDokumenta if doclist.summaDokumenta is not None else 0,
                                            SUPPLIERDOC=doclist.id,  # Номер документа поставщика
                                            SUPPLIERDOCCREATE=cv_date,  # Дата документа поставщика

                                        )
                                    ]
                                )
                            )
                        ]
                    )
                )

                # Получаем словарь из экземпляра модели
                data_dict = wi_data.dict()

                # Получаем JSON строку из словаря
                data_json = json.dumps(data_dict, indent=4)

                # print(data_json)
                text = await post_request(supermag_in_url, data_json)
                if text:
                    ticket = ET.fromstring(text)
                    ticket_id = ticket.find('ticketId').text
                    while True:
                        request_text = await read_request_sm(ticket_id)
                        await asyncio.sleep(0.5)
                        states = ET.fromstring(request_text)
                        # print(request_text)
                        state = states.find('state').text
                        # print(state)
                        if state == 'Success':
                            print(wi_id, doclist.warehouseId)
                            send_post(doclist.warehouseId, wi_id)
                            result = f'send doc {wi_id}'
                            await delete_request(url=postuplenie_url, doc_id=doclist.id)
                            break
                        elif state not in ('Success', 'Handling', 'Queued'):
                            result = f"Документ не обработан статус: {state}"
                            raise ValueError(f"Документ не обработан статус: {state}")
    return result


# async def get_wi_items(or_id, wi_id):
#     get_doc_items_url = f"{postuplenie_url}('{or_id}')/declaredItems"
#     async with aiohttp.ClientSession() as sessionapi:
#         # Отправляем POST-запрос с JSON-данными на сервер api с помощью асинхронного менеджера контекста
#         async with sessionapi.get(get_doc_items_url, headers=header) as response:
#             # Получаем кодировку, статус и текст ответа асинхронно с помощью await
#             status = response.status
#             data_js = await response.json()
#             data_list = data_js['value']
#             smspeclist = []
#             mismathlist = []
#             summa_doc = []
#             spec_id = 0
#             for data in data_list:
#                 spec_id += 1
#                 docitems = DocumentItem(**data)
#                 result_id = spec_id if not docitems.nomerStrokiDokumenta else docitems.nomerStrokiDokumenta
#                 string_summa = docitems.currentQuantity * docitems.cena
#                 summa_doc.append(string_summa)
#                 smspec = SMSpec(
#                     DOCID=wi_id,
#                     DOCTYPE="WI",
#                     SPECITEM=result_id,
#                     ARTICLE=docitems.productId,
#                     DISPLAYITEM=result_id,
#                     ITEMPRICE=docitems.cena,
#                     QUANTITY=docitems.currentQuantity,
#                     TOTALPRICE=string_summa,
#                     TOTALPRICECUR=string_summa
#                 )
#                 specmismath = SLSpecqmismatch(
#                     DOCID=wi_id,
#                     DOCTYPE="WI",
#                     SPECITEM=result_id,
#                     QUANTBYDOC=docitems.declaredQuantity,
#                 )
#                 smspeclist.append(smspec)
#                 mismathlist.append(specmismath)
#             # Проверяем статус ответа и выводим результат
#             if status not in (200, 204):
#                 print('Произошла ошибка при запросе на сервер')
#                 print(status)
#                 print(response)
#     return smspeclist, mismathlist, summa_doc


async def get_wi_items(or_id, wi_id):
    get_doc_items_url = f"{postuplenie_url}('{or_id}')/declaredItems"
    data_request = await get_request(get_doc_items_url)
    smspeclist = []
    mismathlist = []
    summa_doc = []
    spec_id = 0
    if 'data_json' in data_request:
        data_list = data_request[1]["value"]
        for data in data_list:
            spec_id += 1
            docitems = DocumentItem(**data)
            result_id = spec_id if not docitems.nomerStrokiDokumenta else docitems.nomerStrokiDokumenta
            string_summa = docitems.currentQuantity * docitems.cena
            summa_doc.append(string_summa)
            smspec = SMSpec(
                DOCID=wi_id,
                DOCTYPE="WI",
                SPECITEM=result_id,
                ARTICLE=docitems.productId,
                DISPLAYITEM=result_id,
                ITEMPRICE=docitems.cena,
                QUANTITY=docitems.currentQuantity,
                TOTALPRICE=string_summa,
                TOTALPRICECUR=string_summa
            )
            specmismath = SLSpecqmismatch(
                DOCID=wi_id,
                DOCTYPE="WI",
                SPECITEM=result_id,
                QUANTBYDOC=docitems.declaredQuantity,
            )
            smspeclist.append(smspec)
            mismathlist.append(specmismath)
    return smspeclist, mismathlist, summa_doc

if __name__ == '__main__':
    # asyncio.run(send_request(url, data_json))
    # asyncio.run(get_wi_items('23ORA-NV96456'))
    asyncio.run(send_wi())
