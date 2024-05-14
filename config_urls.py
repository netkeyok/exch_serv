
api_server_ip = '192.168.0.166'
api_server_port = '9000'

header = {'Content-Type': 'application/json'}

# Clevrense urls
cleverence_url = f'http://{api_server_ip}:{api_server_port}/MobileSMARTS/api/v1/'


# Раздел карточек
products_url = f'{cleverence_url}Products'
begin_product = f'{cleverence_url}Products/BeginUpdate'
end_product = f'{cleverence_url}Products/EndUpdate'

# Раздел контрагентов
contragents_url = f'{cleverence_url}Tables/Kontragenty'
begin_contragent = f'{cleverence_url}Tables/Kontragenty/BeginUpdate'
end_contragent = f'{cleverence_url}Tables/Kontragenty/EndUpdate'


# Раздел загрузки поставок
postuplenie_url = f'{cleverence_url}Docs/Postuplenie'
postupleniebaza_url = f'{cleverence_url}Docs/PostuplenieBaza'


# Раздел загрузки складов.(МХ в Супермаге)
warehouse_url = f'{cleverence_url}Warehouses'

# Супермаг urls
supermag_out_url = 'http://192.168.0.238:8080/out/json/'
supermag_in_url = 'http://192.168.0.238:8080/in/json/'

ticket_url = f"http://192.168.0.238:8080/out/ticket/"

storelocs_sm_url = f'{supermag_out_url}IOSMIOSTORELOCATIONS/*'

contragents_sm_url = f'{supermag_out_url}IOUSIOSMCONTRAGENT/*'

smcard_sm_url = f'{supermag_out_url}IOUSIOMESABBREVINFO/*/pArticle='
