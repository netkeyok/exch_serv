from sqlalchemy import func
from db_connections.oracle_conf import session
from db_connections.oramodels import SMDocuments, SADocDefaults


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
