import MySQLdb
from app import app
from app.constants import FABRIC_DOCTOR_QUERY

def get_account_ids_from_query(query, **kwargs):
    if not all([query, kwargs.get('database')]):
        return []
    db_config = app.config['DB_CONFIG'].get(kwargs['database'])
    if not db_config:
        return []
    db = MySQLdb.connect(
        host=db_config.get('host'),
        user=db_config.get('user'),
        passwd=db_config.get('password'),
        db=db_config.get('db')
    )
    cur = db.cursor()
    cur.execute(query)
    account_ids = [i[0] for i in cur.fetchall() if i]
    account_ids = [int(i) for i in account_ids]
    return account_ids


def get_doctor_account_ids_from_fabric():
    db = MySQLdb.connect(
        host=app.config.get('FABRIC_RO_DB_HOST'),
        user=app.config.get('FABRIC_RO_DB_USERNAME'),
        passwd=app.config.get('FABRIC_RO_DB_PASSWORD'),
        db=app.config.get('FABRIC_RO_DB')
    )
    cur = db.cursor()
    query = FABRIC_DOCTOR_QUERY
    cur.execute(query)
    account_ids = []
    for row in cur.fetchall():
        account_id = row[0]
        if account_id:
            account_ids.append(int(row[0]))
    return account_ids


def get_doctor_player_ids_from_account_ids(query_account_ids):
    db = MySQLdb.connect(
        host=app.config.get('ONENESS_RO_DB_HOST'),
        user=app.config.get('ONENESS_RO_DB_USERNAME'),
        passwd=app.config.get('ONENESS_RO_DB_PASSWORD'),
        db=app.config.get('ONENESS_RO_DB')
    )
    cur = db.cursor()
    query_batch_size = 5000
    player_ids = []
    for i in range(0, len(account_ids) / query_batch_size + 1):
        query = """
            SELECT distinct player_id from user_settings
            WHERE account_id in (%s)
        """
        account_ids = query_account_ids[
            i * query_batch_size:(i+1) * query_batch_size]
        if not account_ids:
            break
        query = query % ', '.join(['%s'] * len(account_ids))
        cur.execute(query, account_ids)
        for row in cur.fetchall():
            player_ids.append(row[0])
    return player_ids


def get_patient_player_ids_from_account_ids(account_ids):
    db = MySQLdb.connect(
        host=app.config.get('ONENESS_RO_DB_HOST'),
        user=app.config.get('ONENESS_RO_DB_USERNAME'),
        passwd=app.config.get('ONENESS_RO_DB_PASSWORD'),
        db=app.config.get('ONENESS_RO_DB')
    )
    cur = db.cursor()
    query = """
        SELECT distinct one_signal_id from device_information
        WHERE account_id in (%s)
    """
    query = query % ', '.join(['%s'] * len(account_ids))
    cur.execute(query, account_ids)
    player_ids = []
    for row in cur.fetchall():
        player_ids.append(row[0])
    # convert player_id to int
    return player_ids
