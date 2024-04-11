import asyncio
import time

import aiohttp
import json
import xml.etree.ElementTree as ET
from sm_api_models.WI import Data, Package, Item, WI, SMDocuments
from sm_api_models.WI import SMCommonbases, SMWaybillIn, SMSpec, SLSpecqmismatch
from api_requests.Send_to_CV import send_request, permitdel, read_request_sm
from cv_models.Postuplenie import Postuplenie, DocumentItem
from db_connections.functions import generate_number, send_post

header = {'Content-Type': 'application/json'}


async def send_wi():
    print("Start sending WI")
    # Создаем сессию клиента с помощью асинхронного менеджера контекста
    url = 'http://192.168.0.166:9000/MobileSMARTS/api/v1/Docs/Postuplenie'

    async with aiohttp.ClientSession() as sessionapi:
        # Отправляем POST-запрос с JSON-данными на сервер api с помощью асинхронного менеджера контекста
        async with sessionapi.get(url, headers=header) as response:
            # Получаем кодировку, статус и текст ответа асинхронно с помощью await
            status = response.status
            data_js = await response.json()
            data_list = data_js['value']
            for data in data_list:
                doclist = Postuplenie(**data)
                if doclist.finished:
                    print(doclist)
                    cv_date = doclist.createDate
                    formatted_date = cv_date.strftime("%Y-%m-%dT%H:%M:%S")
                    wi_id = generate_number(doclist.warehouseId)
                    items = await get_wi_items(doclist.id, wi_id)
                    print(wi_id, doclist.id)
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
                                                CREATEDAT=formatted_date,
                                                CURRENCYMULTORDER=0,
                                                CURRENCYRATE=1.0,
                                                CURRENCYTYPE=1,
                                                DOCSTATE=1,
                                                ISROUBLES="1",
                                                LOCATIONTO=doclist.warehouseId,
                                                OPCODE="0",
                                                PRICEROUNDMODE=3,
                                                TOTALSUM=doclist.summaDokumenta,
                                                TOTALSUMCUR=doclist.summaDokumenta,
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
                                                # OURSELFCLIENT=101085,
                                                PAYCASH="0",
                                                SUPPLDOCSUM=doclist.summaDokumenta,  # Сумма по документу поставщика
                                                SUPPLIERDOC=doclist.id,  # Номер документа поставщика
                                                SUPPLIERDOCCREATE=formatted_date,  # Дата документа поставщика

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
                    cm_url = 'http://192.168.0.238:8080/in/json'

                    # print(data_json)
                    text = await send_request(cm_url, data_json)
                    if text:
                        ticket = ET.fromstring(text)
                        ticket_id = ticket.find('ticketId').text
                        while True:
                            state = 'Handling'
                            request_text = await read_request_sm(ticket_id)
                            time.sleep(0.5)
                            states = ET.fromstring(request_text)
                            state = states.find('state').text
                            if state == 'Success':
                                send_post(doclist.warehouseId, wi_id)
                                await permitdel(doclist.id)
                                break
                            elif state not in ('Success', 'Handling', 'Queued'):
                                raise ValueError(f"Документ не обработан статус: {state}")


async def get_wi_items(or_id, wi_id):
    get_doc_items_url = f"http://192.168.0.166:9000/MobileSMARTS/api/v1/Docs/Postuplenie('{or_id}')/declaredItems"
    async with aiohttp.ClientSession() as sessionapi:
        # Отправляем POST-запрос с JSON-данными на сервер api с помощью асинхронного менеджера контекста
        async with sessionapi.get(get_doc_items_url, headers=header) as response:
            # Получаем кодировку, статус и текст ответа асинхронно с помощью await
            status = response.status
            data_js = await response.json()
            data_list = data_js['value']
            specitem = 0
            smspeclist = []
            mismathlist = []
            for data in data_list:
                docitems = DocumentItem(**data)
                specitem += 1
                # print(docitems.Price, docitems.PriceTotal)
                smspec = SMSpec(
                    DOCID=wi_id,
                    DOCTYPE="WI",
                    SPECITEM=docitems.uid,
                    ARTICLE=docitems.productId,
                    DISPLAYITEM=specitem,
                    ITEMPRICE=docitems.price,
                    QUANTITY=docitems.currentQuantity,
                    TOTALPRICE=docitems.priceTotal,
                    TOTALPRICECUR=docitems.priceTotal
                )
                specmismath = SLSpecqmismatch(
                    DOCID=wi_id,
                    DOCTYPE="WI",
                    SPECITEM=specitem,
                    QUANTBYDOC=docitems.declaredQuantity,
                )
                smspeclist.append(smspec)
                mismathlist.append(specmismath)
            # Проверяем статус ответа и выводим результат
            if status not in (200,):
                print('Произошла ошибка при запросе на сервер')
                print(status)
                print(response)
    return smspeclist, mismathlist




if __name__ == '__main__':
    # asyncio.run(send_request(url, data_json))
    # asyncio.run(get_wi_items('23ORA-NV96456'))
    asyncio.run(send_wi())

