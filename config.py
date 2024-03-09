
api_server_ip = '192.168.0.166'
api_server_port = '9000'

# Clevrense urls
baseURL = f'http://{api_server_ip}:{api_server_port}/MobileSMARTS/api/v1/'

# Раздел карточек
products_url = f'{baseURL}Products'
begin_product = f'{baseURL}Products/BeginUpdate'
end_product = f'{baseURL}Products/EndUpdate'

# Раздел контрагентов
contragents_url = f'{baseURL}Tables/Kontragenty'
begin_contragent = f'{baseURL}Tables/Kontragenty/BeginUpdate'
end_contragent = f'{baseURL}Tables/Kontragenty/EndUpdate'


# Раздел загрузки поставок
postuplenie_url = f'{baseURL}Docs/Postuplenie'


# Раздел загрузки складов.(МХ в Супермаге)
warehouse_url = f'{baseURL}Warehouses'

test_endpoint = f'http://{api_server_ip}:8000/v1/json_in/test'
