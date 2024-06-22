


async def send_spisok_doc(doc_dict):
    data = OR.Data(**doc_dict)
    # получаем список постобъектов
    # print(data)
    postobjects = data.PACKAGE.POSTOBJECT
    doc_list = []
    for postobject in postobjects:
        docdata = postobject.OR.SMDOCUMENTS[0]
        original_datetime = postobject.OR.SMDOCUMENTS[0].CREATEDAT
        docprops = (postobject.OR.SMDOCPROPS[0].PARAMVALUE or []) if postobject.OR.SMDOCPROPS else None
        formatted_datetime = original_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")
        timezone_info = datetime.now(timezone.utc).astimezone().strftime("%z")
        formatted_datetime_with_timezone = f"{formatted_datetime}{timezone_info}"
        # Получаем строки документа
        doc_list.append(docdata.ID)
        # Получаем шапку документа
        spisokdok = SpisokDokumentov(
            uid=docdata.ID,
            docdate=formatted_datetime_with_timezone,
            docType="Postuplenie",
            docBarcode=docprops,
            idKontragenta=str(docdata.CLIENTINDEX),
            summaDokumenta=docdata.TOTALSUM,
            warehouseId=str(docdata.LOCATION),
        )
        spisokdokumentov_json = spisokdok.model_dump_json(exclude_none=True)
        await post_request(begin_tables_spisokdokumentov)
        await post_request(tables_spisokdokumentov, spisokdokumentov_json)
        await post_request(end_tables_spisokdokumentov)
    if doc_list:
        return doc_list
    else:
        return 'nothing'

if __name__ == '__main__':
    data = asyncio.run(send_spisok_doc())
    for d in data:
        print(d)
    # data = asyncio.run(send_wi())
    # print(data)
    pass
