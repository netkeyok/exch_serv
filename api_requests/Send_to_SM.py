import asyncio
import aiohttp
import json
from sm_models.WI import Data, Package, Item, WI, SMDocuments
from sm_models.WI import SMCommonbases, SMWaybillIn, SMSpec
from load_to_cv import send_request
from cv_models.Postuplenie import Postuplenie, DocumentItem


header = {'Content-Type': 'application/json'}


async def load_wi():

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
                # print(doclist)
                if doclist.finished:
                    print(doclist.warehouseId, doclist.id, doclist.finished)
                else:
                    print(f'del {doclist.id}, {doclist.finished}')
            # print(status)
            # Проверяем статус ответа и выводим результат
            if status not in (200,):
                print('Произошла ошибка при запросе на сервер')
                print(status)
                print(response)

async def get_wi_items(docid):
    get_doc_items_url = f"http://192.168.0.166:9000/MobileSMARTS/api/v1/Docs/Postuplenie('{docid}')/declaredItems"
    async with aiohttp.ClientSession() as sessionapi:
        # Отправляем POST-запрос с JSON-данными на сервер api с помощью асинхронного менеджера контекста
        async with sessionapi.get(get_doc_items_url, headers=header) as response:
            # Получаем кодировку, статус и текст ответа асинхронно с помощью await
            status = response.status
            data_js = await response.json()
            # print(data_js)
            data_list = data_js['value']
            for data in data_list:
                docitems = DocumentItem(**data)
                # print(docitems)
                # print(docitems.uid,
                #       docitems.productId,
                #       docitems.productId,
                #       docitems.declaredQuantity,
                #       docitems.currentQuantity,
                #       docitems.price,
                #       docitems.cenaPostavki)
                smspec = SMSpec(
                    DOCID="WI02PV257626",
                    DOCTYPE="WI",
                    SPECITEM=1,
                    ARTICLE="012248",
                    DISPLAYITEM=1,
                    ITEMPRICE=132.91,
                    QUANTITY=4,
                    TOTALPRICE=531.64,
                    TOTALPRICECUR=531.64,
                )
            # print(status)
            # Проверяем статус ответа и выводим результат
            if status not in (200,):
                print('Произошла ошибка при запросе на сервер')
                print(status)
                print(response)



spec_list = []
# Список позиций накладных
smspec = {
    "DOCID": "WI02PV257626",
    "DOCTYPE": "WI",
    "SPECITEM": 1,
    "ARTICLE": "012248",
    "DISPLAYITEM": 1,
    "ITEMPRICE": 132.91,
    "QUANTITY": 4,
    "TOTALPRICE": 531.64,
    "TOTALPRICECUR": 531.64,
}
spec_list.append(smspec)
# Создаем экземпляр модели
WI_data = Data(
    PACKAGE=Package(
        name="example_package",
        POSTOBJECT=[
            Item(
                description="Приходная накладная",
                action="normal",
                Id="WIWI02PV257626",
                WI=WI(
                    SMDOCUMENTS=[
                        SMDocuments(
                            ID="WI02PV257626",
                            DOCTYPE="WI",
                            BORNIN="zW3taivnRyidInB3UjAdZQ==",
                            CLIENTINDEX=100995,
                            COMMENTARY='Прием товара ТСД по заказу: ',
                            CREATEDAT="2024-02-28T00:00:00",
                            CURRENCYMULTORDER=0,
                            CURRENCYRATE=1.0,
                            CURRENCYTYPE=1,
                            DOCSTATE=1,
                            ISROUBLES="1",
                            LOCATIONTO="23",
                            OPCODE="0",
                            PRICEROUNDMODE=3,
                            TOTALSUM=531.64,
                            TOTALSUMCUR=531.64,
                        )],
                    SMCOMMONBASES=[
                        SMCommonbases(
                            ID="WI02PV257626",
                            DOCTYPE="WI",
                            BASEDOCTYPE="OR",
                            BASEID="18ORA-E630868",
                        )],
                    SMSPEC=spec_list,
                    SMWAYBILLSIN=[
                        SMWaybillIn(
                            ID="WI02PV257626",
                            DOCTYPE="WI",
                            GOODSOWNER=0,
                            # OURSELFCLIENT=101085,
                            PAYCASH="0",
                            SUPPLDOCSUM=0.0,  # Сумма по документу поставщика
                            SUPPLIERDOC='aslakfnas',  # Номер документа поставщика
                            SUPPLIERDOCCREATE="2024-02-28T00:00:00",  # Дата документа поставщика

                        )
                    ]
                )
            )
        ]
    )
)

# Получаем словарь из экземпляра модели
data_dict = WI_data.dict()

# Получаем JSON строку из словаря
data_json = json.dumps(data_dict, indent=4)
url = 'http://192.168.0.238:8080/in/json'


# print(data_json)

if __name__ == '__main__':
    # asyncio.run(send_request(url, data_json))
    asyncio.run(get_wi_items())
    # asyncio.run(load_wi())
