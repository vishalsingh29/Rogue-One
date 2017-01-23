from app import app
import requests
import json

def send_notification(player_ids, message):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
    }
    headers['Authorization'] = 'Basic ' + app.config['ONESIGNAL_API_KEY']
    payload = {
        "app_id": app.config['ONESIGNAL_APP_ID'],
        "include_player_ids": player_ids,
        "contents": {
            "en": message
        }
    }
    req = requests.post(
        "https://onesignal.com/api/v1/notifications",
        headers=headers,
        data=json.dumps(payload)
    )
    return req.status_code


def send_notification1(player_ids, message):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
    }
    headers['Authorization'] = 'Basic ' + 'NDBhMGEyMGEtYTBiZS00YjQyLTgxMzAtMTViZTI2NDQyYmZh'
    payload = {
        "app_id": 'eb9b7d42-7c4e-451d-b87c-f79b20d13c88',
        "android_background_data":"true",
        "include_player_ids": player_ids,
        "data": {
           "type": "custom_message",
            "message_id": "1",
            "created_at": "Fri, 28 Dec 2016 13:37:00",
             "message" : {
               "title": "Get ready for Consult Direct!",
              "message": "Add your bank details securely to get paid for online consultations.",
              "summary_text": "",
               "icon_type": "views",
               "image_url": "",
               "target_url": "",
               "service": "consult"
           }
       },
        "contents": {
        }
    }
    req = requests.post(
        "https://onesignal.com/api/v1/notifications",
        headers=headers,
        data=json.dumps(payload)
    )
    return req.status_code
