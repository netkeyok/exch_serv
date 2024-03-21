import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import update, select, func, text

from cv_models.Postuplenie import Postuplenie
from db_connections.oramodels import SMDocuments, SADocDefaults, SMPostLocMap, SMPostQueue
from db_connections.oracle_conf import session, engine

# post_id = select(SMPostLocMap.DBASEID).where(SMPostLocMap.STORELOC == 17)
# post_id = session.query(func.select SMPostQueueSeq.NEXTVAL from dual)


# Выполняем запрос
# text = session.execute(post_id).scalar()
# print(text)

raw_sql = text("select supermag.SMPostQueueSeq.NEXTVAL from dual")

# Выполнение запроса
result = session.execute(raw_sql).scalar()

print(result)
# Обработка результатов
# for row in result:
#     print(row)
# result = session.execute(raw_sql)

# Завершаем транзакцию
# session.commit()
