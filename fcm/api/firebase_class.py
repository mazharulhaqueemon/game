import requests
import json

SERVER_TOKEN = 'AAAAOlTs0_A:APA91bFv1-zL3w0tWe8hufZpJZjMXxZJ5J9bnZmKqQb7z6ljB_wNSQs9Oc39WHdoXO0RnaY1Yy9qhsTa1jToijb6YIckh_NKTl9dhCrk6PXTMEAOouGKX-Sz78ncCqvP06Ubt-SWktBw'
class Firebase:
    def __init__(self):
        pass

    def send(self,registrations_ids, message):
        fields = {
            # 'registration_ids' : registrations_ids,
            'to' : registrations_ids,
            'data' : message,
        }
        return self.send_push_notification(fields)

    def send_push_notification(self,fields):
        # firebase server url to send the curl request
        url = 'https://fcm.googleapis.com/fcm/send'

        # building headers for the request
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + SERVER_TOKEN,
        }

        # body = {
        #         'notification': {'title': 'Sending push form python script',
        #                             'body': 'New Message'
        #                             },
        #         'to':
        #             deviceToken,
        #         'priority': 'high',
        #         #   'data': dataPayLoad,
        #         }
        # data = {
        #     "registration_ids": "dQDHpqOsS-SSl7Ry8x4C5d:APA91bEVk38hVSWpl3k9iIQCMb732lW_VRo0ji9NU_0cIdW5MbzUZUP-bXsmpCe21LPW2eUeZAUk18bF-twmUJx0RJ3tCvgqg0La7ArCXDP8iWV7AXhzELsEdWFwz19C7KrquLbPrCc9", 
        #     "data": 'nothing'}

        data = json.dumps(fields)
        response = requests.post(url,headers=headers, data=data,)

        # print(response)
        # print(response.status_code)

        return True