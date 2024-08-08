import asyncio

from api_models.Cleverence.PodborDokumentov import ODataResponse
from api_models.Cleverence.Postuplenie import Postuplenie
from config_urls import postuplenie_url, podbor_docs_all, podbor_doc_tables
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
        for data in data_docs.value:
            docs_list.append(data.id)
    return docs_list


async def get_tables_podbor_docs(doc_id):
    doc_list = []
    url = podbor_doc_tables.format(doc_id=doc_id)
    # print(url)
    datarequest = await get_request(url)
    resultrequest = datarequest[1]["value"]
    for data_request in resultrequest:
        doc_list.append(data_request["docId"])
    return {
        "podbor_for": doc_id,
        "document_list": doc_list,
    }


if __name__ == "__main__":
    # asyncio.run(get_doc_postuplenie("18ORA-E733908"))
    data = asyncio.run(get_docs_podbor_docs())
    print(data)
    # asyncio.run(get_doc_postuplenie(data[0]))
    doclist = asyncio.run(get_tables_podbor_docs(data[0]))
    print(doclist)

    # asyncio.run(
    #     delete_request(podbor_docs_all, "new_6cc93c28-8d96-4434-9f61-ee70ae28650a")
    # )
