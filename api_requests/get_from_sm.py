import asyncio
import json

import aiohttp

from api_models.Supermag import CD, USIOMESABBREVINFO
from config_urls import header, smcard_sm_url


async def get_request(url, js_data=None):
    # асинхронная функция для отправки запроса на сервер api

    # Создаем сессию клиента с помощью асинхронного менеджера контекста
    async with aiohttp.ClientSession() as sessionapi:
        # Отправляем POST-запрос с JSON-данными на сервер api с помощью асинхронного менеджера контекста
        async with sessionapi.get(url, data=js_data, headers=header) as response:
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


async def get_mesabbrev(article):
    # print(article)
    url = f'{smcard_sm_url}{article}'
    data = await get_request(url)
    dictionary = json.loads(data)
    data_model = USIOMESABBREVINFO.DataModel(**dictionary)
    for data in data_model:
        mesabbrev = data[1].POSTOBJECT[0].IOUSIOMESABBREVINFO.USIOMESABBREVINFO[0].MESABBREV
        return mesabbrev


if __name__ == '__main__':
    asyncio.run(get_mesabbrev('113057'))
    pass