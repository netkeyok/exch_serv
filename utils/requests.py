import aiohttp

from config_urls import header, ticket_url


async def post_request(url, js_data=None):
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
                print("Произошла ошибка при добавлении продукта на сервер")
                print(status)
                print(response)
                return False
    return text


async def get_request(url, js_data=None, headers=None):
    # асинхронная функция для отправки запроса на сервер API
    async with aiohttp.ClientSession() as session:
        # Отправляем GET-запрос с данными на сервер API
        async with session.get(url, params=js_data, headers=headers) as response:
            status = response.status
            try:
                # Пытаемся возвратить JSON
                response_json = await response.json()
                return "data_json", response_json
            except Exception:
                # Если JSON невозможно получить, возвратим обычный текст ответа
                response_text = await response.text()
                # if status not in (200, 201, 204):
                # print(js_data)
                # print("Произошла ошибка при запросе сервер")
                # print(status)
                # print(response)

                # return "data_text", response_text
                return None


async def delete_request(url: str, doc_id: str):
    async with aiohttp.ClientSession() as sessionapi:
        try:
            del_url = f"{url}('{doc_id}')"
            # print(del_url)
            async with sessionapi.delete(url=del_url) as del_response:
                print(del_response.status)
        except Exception as e:
            print(f"An error occurred: {e}")
    await sessionapi.close()


async def read_request_sm(ticket):
    # Validate the ticket parameter
    if not ticket:
        raise ValueError("Invalid ticket")

    url = f"{ticket_url}{ticket}"
    text = ""
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
