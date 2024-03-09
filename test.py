import asyncio
from datetime import datetime
import json

import aiohttp
from sqlalchemy import select, exists
from cv_models.Products import Product
from db_connections.oramodels import SMStoreUnits, SMCard
from db_connections.oracle_conf import session

from config import products_url, begin_product, end_product

# импорт модуля collections
from collections import defaultdict

import time

# article = '065579'


# article = '001076'
# article = '055219'
# article = '060260'
# article = '097047'
# article = '022611'
# article = '022890'
# article = '019519'
article = '002242'


# Создаем асинхронную функцию для отправки запроса на сервер api
async def send_request(url, js_data):
    header = {'Content-Type': 'application/json'}
    # Создаем сессию клиента с помощью асинхронного менеджера контекста
    async with aiohttp.ClientSession() as sessionapi:
        # Отправляем POST-запрос с JSON-данными на сервер api с помощью асинхронного менеджера контекста
        async with sessionapi.post(url, data=js_data, headers=header) as response:
            # Получаем кодировку, статус и текст ответа асинхронно с помощью await
            status = response.status
            text = await response.text()
            # Проверяем статус ответа и выводим результат
            if status not in (201, 204):
                print('Произошла ошибка при добавлении продукта на сервер')
                print(status)
                print(response)
                print(js_data)


async def load_card(article):
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
    defailt_barcode = ''

    # Проверяем наличие кол-ва для упаковок в карточке (у весовых может отсутсвовать, поэтому отсекаем.)
    if all(data['quantity'] for data in results):
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
                defailt_barcode = barcode[0]

            # Формируем словарь с упаковками с полученными ранее данными
            Packing = {
                        "name": pack,
                        "unitsQuantity": pack_qnty,
                        # "barcode": barcode[0],
                        "barcodes": barcode,
                        "id": pack,
                    }
            packing_list.append(Packing)

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
        barcode=defailt_barcode,
        basePackingId=results[0]['mesabbrev'],
        marking=article
        )

    session.close()

    # Конвертируем объект в JSON-формат
    product_json = product.model_dump_json(exclude_none=True)
    with open('product_json.json', 'w') as file:
        json.dump(product_json, file)
    # Отправляем данные на сервер.
    await send_request(products_url, product_json)


async def get_articlelist():
    start_time = time.time()

    print('Начало загрузки данных')

    # Передаем на сервер запрос на обновление справочника
    await send_request(begin_product, None)
    # получаем список всех article, удовлетворяющих условиям
    query = select(SMCard.article).where(SMCard.receiptok == '1',
                                         SMCard.accepted == '1',
                                         exists().where(SMCard.article == SMStoreUnits.article))
    articles = session.execute(query).fetchall()

    # отправляем данные на сервер
    for i in articles:
        await load_card(i[0])
    await send_request(end_product, None)

    # Замеряем время загрузки
    end_time = time.time()
    elapsed_time = start_time - end_time
    time_dt = datetime.fromtimestamp(elapsed_time)
    time_format = "%Y-%m-%d %H:%M:%S"
    time_str = time_dt.strftime(time_format)

    print('Загрузка данных закончена')
    print(f'Время выполнения: {time_str}')



# load_card(article)
if __name__ == '__main__':
    # asyncio.run(load_card(article))
    asyncio.run(get_articlelist())
