


async def send_wi():
    print("Start sending WI")
    # result = 'Nothing to send'
    data_request = await get_request(postuplenie_url)
    if 'data_json' in data_request:
        for data_js in data_request[1]["value"]:
            doclist = Postuplenie(**data_js)
            print(doclist)

        # data_list = data_js['value']
        # for data in data_list:
        #     doclist = Postuplenie(**data)
        #     print(doclist)
    # return result


async def get_docs_of_dates(days: int):
    docs_list = []
    data_request = await get_request(postuplenie_url)
    if 'data_json' in data_request:
        # Создание осведомлённого объекта datetime по GMT+5
        gmt_plus_five = timezone(timedelta(hours=5))
        cutoff_date = datetime.now(gmt_plus_five) - timedelta(days=days)
        for data in data_request[1]['value']:
            doclist = Postuplenie(**data)
            # Проверка, что createDate в формате datetime с tzinfo
            # Если createDate меньше или равно дате отсечки, добавляем в список
            if doclist.createDate <= cutoff_date:
                docs_list.append((doclist.id, doclist.createDate))
            else:
                print('Произошла ошибка при запросе на сервер')
    return docs_list


if __name__ == '__main__':
    data = asyncio.run(get_docs_of_dates(1))
    for d in data:
        print(d)
    # data = asyncio.run(send_wi())
    # print(data)
    pass
