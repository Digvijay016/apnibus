import json
import requests
import urllib.parse
from django.conf import settings

SMS_CONFIG = ''
API_KEY = "NDU0MTM2MzQzNjZjMzc2MTY4Nzk2ODY1NDY0ZjRkNDk="
MSG91_API_KEY = "372570A1WKiiTht61f8c2f5P1"
SENDER_NAME = "APNBUS"
environment_list = ["production", "local", "staging"]
# environment = settings.ENVIRONMENT
environment = 'local'

MSG91_TEMPLATE_IDS = {
    'SEND_OTP': '63dcc3fdd6fc0570073f1e82'
}


class SMSService:

    def __init__(self, mobile, message):
        self.mobile = mobile
        self.message = message

    def get_url(self):
        return SMS_CONFIG['MSG91']['send_national_sms'] % ('91' + self.mobile, self.message)

    def send_sms(self, unicode=1):
        if environment not in environment_list:
            return None

        numbers = self.mobile
        message = self.message
        data = urllib.parse.urlencode({'apikey': API_KEY,
                                       'numbers': numbers,
                                       'message': message,
                                       'sender': SENDER_NAME,
                                       'unicode': unicode
                                       })
        data = data.encode('utf-8')
        request = urllib.request.Request("https://api.textlocal.in/send/?")

        f = urllib.request.urlopen(request, data)
        fr = f.read()
        return fr


class MSG91Service:

    def __init__(self, mobile, template_id, variable_list):
        self.mobile = mobile
        self.template_id = template_id
        self.variable_list = variable_list

    def validate_mobile_number(self):
        mobile_number = self.mobile

        if len(mobile_number) == 11:
            mobile_number = mobile_number[1:]

        elif len(mobile_number) == 12:
            mobile_number = mobile_number[2:]

        mobile_number = f"91{mobile_number}"

        return mobile_number

    def update_variables_in_payload(self, payload):
        variable_list = self.variable_list

        i = 1
        for variable in variable_list:
            payload[f"var{i}"] = variable
            i += 1

        return payload

    @staticmethod
    def get_headers():
        headers = {
            'authkey': MSG91_API_KEY,
            'content-type': "application/json"
        }

        return headers

    def prepare_payload(self):
        mobile = self.validate_mobile_number()
        payload = {
            "flow_id": self.template_id,
            "sender": SENDER_NAME,
            "short_url": "0",
            "mobiles": mobile
        }

        payload = self.update_variables_in_payload(payload)

        return payload

    def send_sms(self):
        msg_sent = False
        try:
            url = "https://api.msg91.com/api/v5/flow/"
            headers = self.get_headers()
            payload = self.prepare_payload()
            print(payload)
            request = requests.request("POST", url=url, headers=headers, data=json.dumps(payload))
            response = request.json()
            print(response)

            if response['type'] == 'success':
                msg_sent = True

        except Exception as ex:
            print(ex)

        return msg_sent

