import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from cv_models.Postuplenie import Postuplenie
from db_connections.oramodels import SMDocuments
from db_connections.oracle_conf import session


async def send_postuplenie(docid=None):
    print(f"send postuplenie {docid}")

    query = (
        select(SMDocuments.ID,
               SMDocuments.LOCATION,
               SMDocuments.CREATEDAT,
               SMDocuments.CLIENTINDEX,
               SMDocuments.TOTALSUM)
        .where(SMDocuments.ID == docid)
    )

    data = session.execute(query).fetchall()
    print(f'!!!!!!!{data}')
    result = session.execute(query)
    print(result)
    dict_iterator = result.mappings()

    # Получаем список словарей
    results = list(dict_iterator)
    print(results)



if __name__ == '__main__':
    # asyncio.run(load_card(article))
    # asyncio.run(get_articlelist())
    # asyncio.run(load_contragents())
    asyncio.run(send_postuplenie('2ORA-E643481'))
    # asyncio.run(send_storeloc())
    # asyncio.run(clear_postuplenie())
    # asyncio.run(get_finalized_doc())
    # asyncio.run(permitdel())
