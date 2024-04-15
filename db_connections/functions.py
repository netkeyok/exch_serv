import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, func, text

from cv_models.Postuplenie import Postuplenie
from db_connections.oramodels import SMDocuments, SADocDefaults, SMPostLocMap, SMPostQueue
from db_connections.db_conf import session


def generate_number(mx_id):
    with session.begin():
        # получаем префикс документа для заданного места хранения
        location_prefix = (
            session.query(SADocDefaults.nameoutprefix)
            .filter(SADocDefaults.doctype == 'WI', SADocDefaults.location == mx_id)
            .scalar()
        )
        # Получаем последний номер существующего документа
        max_id = (
            session.query(func.max(SMDocuments.ID))
            .filter(SMDocuments.ID.like(f'{location_prefix}%'))
            .scalar()
        )

    # Получаем номер без префикса
    str_number = (max_id[len(location_prefix):])
    # преобразуем к числу и увеличиваем номер на 1
    int_id = int(str_number) + 1
    # собираем новый номер вместе с префиксом
    new_number = f'{location_prefix}{str(int_id).zfill(6)}'
    return new_number


def mxid_to_postid(mx_id):
    with session.begin():
        post_id = (
            session.query(SMPostLocMap.DBASEID).where(SMPostLocMap.STORELOC == mx_id).scalar())
        resilt = post_id
        print(resilt)


def send_post(mx_id, doc_id):
    with session.begin():
        raw_sql = text("select supermag.SMPostQueueSeq.NEXTVAL from dual")
        # current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        # получаем префикс документа для заданного места хранения
        post_id = (
            session.query(SMPostLocMap.DBASEID).where(SMPostLocMap.STORELOC == mx_id).scalar())
        # post_id = int(select(SMPostLocMap.DBASEID).where(SMPostLocMap.STORELOC == mx_id).as_scalar())
        # Получаем последний номер существующего документа
        new_post = SMPostQueue(
            ENQTIME=datetime.now(),
            ENQSEQ=int(session.execute(raw_sql).scalar()),
            TARGET=post_id,
            OBJTYPE='WI',
            OBJID=doc_id)
        session.add(new_post)
        session.commit()

        # Закрытие сессии
        session.close()
