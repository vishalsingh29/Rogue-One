from flask import Flask, request
import db_client
import onesignal_client

app = Flask(__name__)

app.config.from_object('settings')

@app.route('/hello')
def hello_world():
    # print app.config['DEFAULT_ENV']
    return 'Hello World'


@app.route('/doctors', methods=['GET', 'POST'])
def send_doctor_push():
    if request.method == 'POST':
        account_ids = db_client.get_doctor_account_ids_from_fabric()
        if not account_ids:
            return {
                'success': False,
                'message': 'No account ids found!!'
            }
        player_ids = db_client.get_doctor_player_ids_from_account_ids(
            account_ids)
        if not player_ids:
            return {
                'success': False,
                'message': 'No player ids found!!'
            }
        message = requests.form.get('message')
        response_status_code = onesignal_client.send_notification(
            player_ids, message)
        return {
            'success': True,
            'status_code': response_status_code
        }
    else:
        # render form here
        return "Hello doctor"


@app.route('/patients')
def send_patient_push():
    pass


if __name__ == '__main__':
    app.run()