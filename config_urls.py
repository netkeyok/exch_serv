# Clevrence api connections
cv_api_server = "192.168.0.166"
cv_api_server_port = "9000"

# Supermag api connections
sm_api_server = "192.168.0.238"
sm_api_server_port = "8080"

# Header
header = {"Content-Type": "application/json"}

# Clevrense urls
cleverence_url = f"http://{cv_api_server}:{cv_api_server_port}/MobileSMARTS/api/v1/"

# Раздел карточек
products_url = f"{cleverence_url}Products"
begin_product = f"{cleverence_url}Products/BeginUpdate"
end_product = f"{cleverence_url}Products/EndUpdate"

# Раздел контрагентов
contragents_url = f"{cleverence_url}Tables/Kontragenty"
begin_contragent = f"{cleverence_url}Tables/Kontragenty/BeginUpdate"
end_contragent = f"{cleverence_url}Tables/Kontragenty/EndUpdate"

# Раздел таблицы
begin_tables_spisokdokumentov = f"{cleverence_url}Tables/SpisokDokumentov/BeginUpdate"
end_tables_spisokdokumentov = f"{cleverence_url}Tables/SpisokDokumentov/EndUpdate"
tables_spisokdokumentov = f"{cleverence_url}Tables/SpisokDokumentov"


# Раздел загрузки поставок
postuplenie_url = f"{cleverence_url}Docs/Postuplenie"
postuplenie_url_get_header = (
    f"{cleverence_url}Docs/Postuplenie('{{doc_id}}')?$select=warehouseId,summaDokumenta,"
    f"idKontragenta"
)
postuplenieruchnoe = f"{cleverence_url}Docs/PostuplenieRuchnoe"
postuplenie_docline_list = (
    f"{cleverence_url}Docs/Postuplenie('{{doc_id}}')/declaredItems"
)

postuplenie_warehause_id_url = (
    f"{cleverence_url}Docs/postuplenie('{{doc_id}}')?$select=warehouseId"
)

gruppovayapriemka_url = f"{cleverence_url}Docs/GruppovayaPriemka"
gruppovayapriemka_url_get_header = (
    f"{cleverence_url}Docs/GruppovayaPriemka?$select=id,finished"
)
gruppovayapriemka_items_url = (
    f"{cleverence_url}Docs/GruppovayaPriemka('{{doc_id}}')/declaredItems"
)
gruppovayapriemka_warehause_id_url = (
    f"{cleverence_url}Docs/GruppovayaPriemka('{{doc_id}}')?$select=warehouseId"
)

# Работа с выбором документов для загрузки

# Раздел таблиц документов
podbor_doc_tables = f"{cleverence_url}Docs/PodborDokumentov('{{doc_id}}')/Dokumenty"
podbor_docs_all = f"{cleverence_url}Docs/PodborDokumentov"

# Раздел загрузки складов.(МХ в Супермаге)
warehouse_url = f"{cleverence_url}Warehouses"

# Супермаг urls
supermag_out_url = f"http://{sm_api_server}:{sm_api_server_port}/out/json/"
supermag_in_url = f"http://{sm_api_server}:{sm_api_server_port}/in/json/"

ticket_url = f"http://{sm_api_server}:{sm_api_server_port}/out/ticket/"

storelocs_sm_url = f"{supermag_out_url}IOSMIOSTORELOCATIONS/*"

contragents_sm_url = f"{supermag_out_url}IOUSIOSMCONTRAGENT/*"

cards_sm_url = f"{supermag_out_url}IOUSIOCARDINFO/*"

barcodes_sm_url = f"{supermag_out_url}IOUSIOBARINFO/*/pArticle="

smcard_sm_url = f"{supermag_out_url}IOUSIOMESABBREVINFO/*/pArticle="

sm_doc_or_url = f"http://{sm_api_server}:{sm_api_server_port}/out/json/or/"
