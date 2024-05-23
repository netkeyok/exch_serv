# Clevrence api connections
cv_api_server = '192.168.0.166'
cv_api_server_port = '9000'

# Supermag api connections
sm_api_server = '192.168.0.238'
sm_api_server_port = '8080'

# Header
header = {'Content-Type': 'application/json'}

# Clevrense urls
cleverence_url = f'http://{cv_api_server}:{cv_api_server_port}/MobileSMARTS/api/v1/'


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
supermag_out_url = f'http://{sm_api_server}:{sm_api_server_port}/out/json/'
supermag_in_url = f'http://{sm_api_server}:{sm_api_server_port}/in/json/'

ticket_url = f"http://{sm_api_server}:{sm_api_server_port}/out/ticket/"

storelocs_sm_url = f'{supermag_out_url}IOSMIOSTORELOCATIONS/*'

contragents_sm_url = f'{supermag_out_url}IOUSIOSMCONTRAGENT/*'

cards_sm_url = f'{supermag_out_url}IOUSIOCARDINFO/*'

barcodes_sm_url = f'{supermag_out_url}IOUSIOBARINFO/*/pArticle='

smcard_sm_url = f'{supermag_out_url}IOUSIOMESABBREVINFO/*/pArticle='
