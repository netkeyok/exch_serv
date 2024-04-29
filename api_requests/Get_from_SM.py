from select import select
from sqlalchemy import select, and_, desc

from db_connections.db_conf import session
from db_connections.oramodels import SMCard, SMStoreUnits, SACardClass


def get_data():
    SMrequest = (
        select(SMCard.article, SMCard.shortname, SMStoreUnits.barcode)
        .join(SMStoreUnits, SMCard.article == SMStoreUnits.article)
        .where(
            and_(
                SMCard.idclass.in_(
                    select(SACardClass.id).where(SACardClass.tree.like('36.%'))
                ),
                SMStoreUnits.barcodetype == 7
            )
        )
    )

    # Получение данных из Oracle
    SMresults = session.execute(SMrequest).all()
    return SMresults


def get_card(code):
    request = (
        select(SMCard.article, SMCard.shortname)
        .join(SMStoreUnits, SMCard.article == SMStoreUnits.article)
        .where(SMStoreUnits.barcode == code)
    )
    results = session.execute(request).all()
    if results:
        data = [{"article": item[0], "name": item[1]} for item in results]
        return data
    else:
        return {"article": '000000', "name": 'Не найден в СМ'}


if __name__ == '__main__':
    print(get_card('4680089950555'))
