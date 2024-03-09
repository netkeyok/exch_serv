from sm_models import WI, RL, UI


def parse_ui(doc_dict):
    data = UI.UtmsPackageResponse(**doc_dict)
    # Отсылаем на сервер уведомление о начале загрузке справочника
    # await send_request(begin_product, None)
    # получаем список постобъектов
    postobjects = data.PACKAGE.POSTOBJECT
    article_list = []
    doctest = ''
    # для каждого постобъекта получаем его описание, действие, идентификатор и документы
    for postobject in postobjects:
        description = postobject.description
        action = postobject.action
        id = postobject.Id
        documents = postobject.UI.SMDOCUMENTS
        specs = postobject.UI.SMSPECWE
        smcommonbases = postobject.UI.SMCOMMONBASES
        print('test-------------------------')
        print(documents)

        # print(description)
        # print(id)
        # print(action)
    # для каждого документа получаем его идентификатор, тип, комментарий и дату создания
    print('test++++++++++++++++++++++++++++++')
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

    for commonbases in smcommonbases:
        dic_id = commonbases.ID
        doc_type = commonbases.DOCTYPE
        base_doctype = commonbases.BASEDOCTYPE
        base_id = commonbases.BASEID

    for spec in specs:
        specitem = spec.SPECITEM
        article = spec.ARTICLE
        print(article)
        # await load_card(article)
        displayitem = spec.DISPLAYITEM
        itemprice = spec.ITEMPRICE
        quantity = spec.QUANTITY


def parse_rl(doc_dict):
    data = RL.Data(**doc_dict)
    # Отсылаем на сервер уведомление о начале загрузке справочника
    # await send_request(begin_product, None)
    # получаем список постобъектов
    postobjects = data.PACKAGE.POSTOBJECT
    article_list = []
    # для каждого постобъекта получаем его описание, действие, идентификатор и документы
    for postobject in postobjects:
        description = postobject.description
        action = postobject.action
        id = postobject.Id
        documents = postobject.RL.SMDOCUMENTS
        spec = postobject.RL.SMSPEC
        specrl = postobject.RL.SMSPECRL

        # print(description)
        # print(id)
        # print(action)
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
    # print(f"Document ID: {doc_id}")
    # print(f"Document type: {doc_type}")
    # print(f"Commentary: {commentary}")
    # print(f"Created at: {created_at}")
    # print(f"Docstate: {docstate}")
    # print(f"location: {location}")
    # print(f"locationto: {locationto}")
    # print(f"locationfrom: {locationfrom}")
    # print(f"totalsum: {totalsum}")
    # print(f"clientindex: {clientindex}")

    for spec in spec:
        specitem = spec.SPECITEM
        article = spec.ARTICLE
        # await load_card(article)
        displayitem = spec.DISPLAYITEM
        itemprice = spec.ITEMPRICE
        quantity = spec.QUANTITY

    # print(specitem)
    # print(f'№ {displayitem}')
    # print(f'specitem: {specitem}')
    # print(f'article: {article}')
    # print(f'price: {itemprice}')
    # print(f'quantity: {quantity}')

    print(specrl)
    for sprl in specrl:
        specitem = sprl.SPECITEM
        awaitq = sprl.AWAITQUANTITY


def parse_wi(doc_dict):
    data = WI.Data(**doc_dict)
    # получаем список постобъектов
    postobjects = data.PACKAGE.POSTOBJECT
    # для каждого постобъекта получаем его описание, действие, идентификатор и документы
    for postobject in postobjects:
        # description = postobject.description
        # action = postobject.action
        id = postobject.Id
        documents = postobject.WI.SMDOCUMENTS
        specs = postobject.WI.SMSPEC

        # print(description)
        # print(id)
        # print(action)
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
    # print(f"Document ID: {doc_id}")
    # print(f"Document type: {doc_type}")
    # print(f"Commentary: {commentary}")
    # print(f"Created at: {created_at}")
    # print(f"Docstate: {docstate}")
    # print(f"location: {location}")
    # print(f"locationto: {locationto}")
    # print(f"locationfrom: {locationfrom}")
    # print(f"totalsum: {totalsum}")
    # print(f"clientindex: {clientindex}")

    for spec in specs:
        specitem = spec.SPECITEM
        article = spec.ARTICLE
        # await load_card(article)
        displayitem = spec.DISPLAYITEM
        itemprice = spec.ITEMPRICE
        quantity = spec.QUANTITY

        print(article)

# print(specitem)
# print(f'№ {displayitem}')
# print(f'specitem: {specitem}')
# print(f'article: {article}')
# print(f'price: {itemprice}')
# print(f'quantity: {quantity}')