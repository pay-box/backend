import random
from django.conf import settings

from user.models import Device
import requests
import json


def validate_phone_number(phone_number):
    try:
        int(phone_number)
        if len(str(phone_number)) > 8:
            return True
        return False
    except Exception:
        return False


def normalize_phone_number(phone_number):
    phone_number = phone_number.replace('+', '')
    if (phone_number.find('00') == 0):
        phone_number = phone_number[2:]
    if phone_number.find('0') == 0:
        phone_number = phone_number[1:]
    return phone_number


def generate_random_code(length):
    pl = random.sample(['1', '2', '3', '4', '5', '6',
                        '7', '8', '9', '0'], length)
    code = ''.join(pl)
    return code


def generate_random_string(length):
    pl = random.sample(['1', '2', '3', '4', '5', '6', 'o', 'w',
                        '7', '8', '9', '0', 'a', 'b', 'c',
                        'd', 'e', 'f', 'g', 'h', 'i', 'j',
                        'k', 'l', 'm', 'n', 'p', 'q', 'r',
                        's', 't', 'u', 'v', 'x', 'y', 'z'], length)
    code = ''.join(pl)
    return code


def send_notification(users, data, notification):
    devices = Device.objects.filter(user__in=users).all()
    registration_ids = []
    for dev in devices:
        registration_ids.append(dev.token)
    for i in range(0, len(registration_ids), 500):
        temp = registration_ids[i:i + 500]
        data['click_action'] = "FLUTTER_NOTIFICATION_CLICK"
        body = {
            "priority": "high",
            "click_action": "FLUTTER_NOTIFICATION_CLICK",
            "data": data,
            "notification": notification,
            "registration_ids": temp}
        headers = {
            "Content-Type": "application/json",
            "Authorization": "key=%s" % settings.FIREBASE_TOKEN
        }
        requests.post(
            settings.FIREBASE_URL,
            data=json.dumps(body),
            headers=headers
        )
