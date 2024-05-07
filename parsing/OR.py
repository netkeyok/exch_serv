from datetime import datetime, timezone

from api_models.Supermag import OR
from api_models.Cleverence.Postuplenie import Postuplenie, DocumentItem
from api_requests.Send_to_CV import send_request
from config_urls import postupleniebaza_url, postuplenie_url


async def parse_or(doc_dict):
    data = OR.Data(**doc_dict)
    # получаем список постобъектов
    postobjects = data.PACKAGE.POSTOBJECT
    for postobject in postobjects:
        docdata = postobject.OR.SMDOCUMENTS[0]
        docitems = postobject.OR.SMSPECOR
        ourselfclient = postobject.OR.SMDOCOR[0].OURSELFCLIENT
        original_datetime = postobject.OR.SMDOCUMENTS[0].CREATEDAT

        formatted_datetime = original_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")
        timezone_info = datetime.now(timezone.utc).astimezone().strftime("%z")
        formatted_datetime_with_timezone = f"{formatted_datetime}{timezone_info}"
        # Получаем строки документа
        spec_list = []
        for items in docitems:
            spec_items = DocumentItem(
                uid=str(items.SPECITEM),
                productId=items.ARTICLE,
                declaredQuantity=items.QUANTITY,
                idEdinicyIzmereniya='шт',
                packingId='шт',
                cena=items.ITEMPRICE,
                priceTotal=items.TOTALPRICE
            )
            spec_list.append(spec_items)

        # Получаем шапку документа
        doc = Postuplenie(
            id=docdata.ID,
            name=f"Прием ТСД по заказу: {docdata.ID}",
            createDate=formatted_datetime_with_timezone,
            warehouseId=str(docdata.LOCATION),
            idKontragenta=str(docdata.CLIENTINDEX),
            summaDokumenta=docdata.TOTALSUM,
            declaredItems=spec_list,
            selfclient=ourselfclient
        )
        postuplenie_json = doc.model_dump_json(exclude_none=True)
        await send_request(postuplenie_url, postuplenie_json)
