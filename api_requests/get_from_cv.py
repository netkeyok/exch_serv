import asyncio

from api_models.Cleverence.PodborDokumentov import ODataResponse
from api_models.Cleverence.Postuplenie import Postuplenie
from config_urls import (
    postuplenie_url,
    podbor_docs_all,
    podbor_doc_tables,
    postuplenie_url_get_header,
    gruppovayapriemka_url_get_header,
)
from utils.requests import get_request, delete_request


async def get_doc_postuplenie(doc_id):
    doc_url = f"{postuplenie_url}('{doc_id}')"
    data_request = await get_request(doc_url)
    if "data_json" in data_request:
        print(data_request[1])
        # for data in data_request[1]["value"]:
        #     data_doc = Postuplenie(**data)
        #     print(data_doc)


async def get_docs_podbor_docs():
    docs_list = []
    data_request = await get_request(podbor_docs_all)
    if "data_json" in data_request:
        data_docs = ODataResponse(**data_request[1])
        for doc_data in data_docs.value:
            docs_list.append(doc_data.id)
    return docs_list


async def get_tables_podbor_docs(doc_id):
    doc_list = []
    url = podbor_doc_tables.format(doc_id=doc_id)
    data_request = await get_request(url)
    if "data_json" in data_request:
        result_request = data_request[1]["value"]
        for data_request in result_request:
            doc_list.append(data_request["docId"])
        return doc_list
    else:
        return None


async def get_header_postuplenie(doc_id):
    url = postuplenie_url_get_header.format(doc_id=doc_id)
    doc_header_request = await get_request(url)
    if "data_json" in doc_header_request:
        doc_header = Postuplenie(**doc_header_request[1])
        return doc_header.warehouseId, doc_header.summaDokumenta
        # warehouse_list.append(result.warehouseId)
        # summa_doc += result.summaDokumenta


async def get_gruppovayapriemka_finished_id():
    data_request = await get_request(gruppovayapriemka_url_get_header)
    finished_id = []
    if "data_json" in data_request:
        for doc_data in data_request[1]["value"]:
            if doc_data["finished"]:
                finished_id.append(doc_data["id"])
    return finished_id


if __name__ == "__main__":
    # result = asyncio.run(get_gruppovayapriemka_finished_id())
    # print(result)
    pass
    # result = asyncio.run(get_header_postuplenie("25ORA-E736628"))
    # print(result)
    # asyncio.run(get_doc_postuplenie("18ORA-E733908"))
    # data = asyncio.run(get_docs_podbor_docs())
    # print(data)
    # asyncio.run(get_doc_postuplenie(data[0]))
    # doclist = asyncio.run(get_tables_podbor_docs(data[0]))
    # print(doclist)

    # asyncio.run(
    #     delete_request(podbor_docs_all, "new_6cc93c28-8d96-4434-9f61-ee70ae28650a")
    # )