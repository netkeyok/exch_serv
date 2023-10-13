from fastapi import FastAPI, File, Request
from sm_models import WI, RL
import json


app = FastAPI()

@app.post("/json_in/wi")
async def upload_data_WI(file: bytes = File()):
# преобразуем байты в строку
    string = file.decode("utf-8-sig")
    # преобразуем строку в словарь
    dictionary = json.loads(string)
    # print(dictionary["PACKAGE"]["POSTOBJECT"][0])
# передаем словарь в модель Pydantic
    data = WI.Data(**dictionary)    
# получаем имя пакета
    # package_name = data.PACKAGE.name
    print(data.PACKAGE.POSTOBJECT)
# получаем список постобъектов
    postobjects = data.PACKAGE.POSTOBJECT
# для каждого постобъекта получаем его описание, действие, идентификатор и документы
    for postobject in postobjects:
        description = postobject.description
        action = postobject.action
        id = postobject.Id
        documents = postobject.WI.SMDOCUMENTS
        spec = postobject.WI.SMSPEC

        print(description)
        print(id)
        print(action)
# для каждого документа получаем его идентификатор, тип, комментарий и дату создания

    for document in documents:
        doc_id = document.ID
        doc_type = document.DOCTYPE
        commentary = document.COMMENTARY
        clientindex = document.CLIENTINDEX
        created_at = document.CREATEDAT
        docstate = document.DOCSTATE
        location = document.LOCATION
        locationto = document.LOCATIONTO
        locationfrom = document.LOCATIONFROM
        totalsum = document.TOTALSUM

# выводим информацию о документе в консоль или в файл
        print(f"Document ID: {doc_id}")
        print(f"Document type: {doc_type}")
        print(f"Commentary: {commentary}")
        print(f"Created at: {created_at}")
        print(f"Docstate: {docstate}")
        print(f"location: {location}")
        print(f"locationto: {locationto}")
        print(f"locationfrom: {locationfrom}")
        print(f"totalsum: {totalsum}")
        print(f"clientindex: {clientindex}")

    for spec in spec:
        specitem = spec.SPECITEM
        article = spec.ARTICLE
        displayitem = spec.DISPLAYITEM
        itemprice = spec.ITEMPRICE
        quantity = spec.QUANTITY

# print(specitem)
        print(f'№ {displayitem}')
        print(f'specitem: {specitem}')
        print(f'article: {article}')
        print(f'price: {itemprice}')
        print(f'quantity: {quantity}')


@app.post("/json_in/rl")
async def upload_data_WI(file: bytes = File()):
# преобразуем байты в строку
    string = file.decode("utf-8-sig")
    # преобразуем строку в словарь
    dictionary = json.loads(string)
    # print(dictionary["PACKAGE"]["POSTOBJECT"][0])
# передаем словарь в модель Pydantic
    data = RL.Data(**dictionary)    
# получаем имя пакета
    # package_name = data.PACKAGE.name
    print(data.PACKAGE.POSTOBJECT)
# получаем список постобъектов
    postobjects = data.PACKAGE.POSTOBJECT
# для каждого постобъекта получаем его описание, действие, идентификатор и документы
    for postobject in postobjects:
        description = postobject.description
        action = postobject.action
        id = postobject.Id
        documents = postobject.RL.SMDOCUMENTS
        spec = postobject.RL.SMSPEC
        specrl = postobject.RL.SMSPECRL

        print(description)
        print(id)
        print(action)
# для каждого документа получаем его идентификатор, тип, комментарий и дату создания

    for document in documents:
        doc_id = document.ID
        doc_type = document.DOCTYPE
        commentary = document.COMMENTARY
        clientindex = document.CLIENTINDEX
        created_at = document.CREATEDAT
        docstate = document.DOCSTATE
        location = document.LOCATION
        locationto = document.LOCATIONTO
        locationfrom = document.LOCATIONFROM
        totalsum = document.TOTALSUM

# выводим информацию о документе в консоль или в файл
        print(f"Document ID: {doc_id}")
        print(f"Document type: {doc_type}")
        print(f"Commentary: {commentary}")
        print(f"Created at: {created_at}")
        print(f"Docstate: {docstate}")
        print(f"location: {location}")
        print(f"locationto: {locationto}")
        print(f"locationfrom: {locationfrom}")
        print(f"totalsum: {totalsum}")
        print(f"clientindex: {clientindex}")

    for spec in spec:
        specitem = spec.SPECITEM
        article = spec.ARTICLE
        displayitem = spec.DISPLAYITEM
        itemprice = spec.ITEMPRICE
        quantity = spec.QUANTITY

# print(specitem)
        print(f'№ {displayitem}')
        print(f'specitem: {specitem}')
        print(f'article: {article}')
        print(f'price: {itemprice}')
        print(f'quantity: {quantity}')

# print(specrl)
    for sprl in specrl:
        specitem = sprl.SPECITEM
        awaitq = sprl.AWAITQUANTITY

        print(f'specitem: {specitem}')
        print(f'awaitquantity: {awaitq}')