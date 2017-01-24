from flask import request, render_template
from app.client import onesignal_client, db_client
from app import app

@app.route('/hello')
def hello_world():
    return render_template('hello.html', name="Vishal")


@app.route('/doctors', methods=['GET', 'POST'])
def send_doctor_push():
    if request.method == 'POST':
        target = request.form.get('target', None)
        database = request.form.get('database', None)
        query = request.form.get('query', '')
        message = request.form.get('message', '')
        if all([target, database, query, message]):
            account_ids = db_client.get_account_ids_from_query(
                query, database=database)
            player_ids = []
            if target == 'Doctor':
                player_ids = get_doctor_player_ids_from_account_ids(account_ids)
            elif target = 'Patient':
                player_ids = get_patient_player_ids_from_account_ids(
                    account_ids)
            if player_ids:
                response_status_code = onesignal_client.send_notification(
                    player_ids, message)
                return render_template(
                    'success.html', status_code=response_status_code)
        return render_template(
            'error.html', message='Something went wrong!')
    else:
        return render_template(
            'index.html',
            dbs_available=['fabric', 'ray', 'accounts', 'oneness'],
            customer_types=['Doctor', 'Patient']
        )


@app.route('/patients')
def send_patient_push():
    pass
