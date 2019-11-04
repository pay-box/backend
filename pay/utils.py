import uuid
import random
from khayyam import JalaliDatetime
from dateutil import tz
import datetime
from django.utils import translation
from django.utils.timezone import localtime


from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Asia/Tehran')

englishDigits = ['0', '1', '2', '3', '4',
                 '5', '6', '7', '8', '9']

persianDigits = ['۰', '۱', '۲', '۳', '۴',
                 '۵', '۶', '۷', '۸', '۹']

persianiserDict = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
                   '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}

digitConvertorDict = {'۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
                      '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'}

arabicDigitConvertorDict = {'٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
                            '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'}


def generate_unique_id():
    return uuid.uuid4().hex.replace('-', '')


def generate_random_code(length):
    pl = random.sample(['1', '2', '3', '4', '5', '6',
                        '7', '8', '9', '0'], length)
    code = ''.join(pl)
    return code


def generate_random():
    return generate_random_code(6)


def humanizeNumber(num):
    return '0'+num[2:]


def humanizeAmount(amount):
    res = amount
    res = f"{amount:,d}"
    res = persianiser(res)
    res = res.replace(',', '،')
    return res


def persianiser(inputStr):
    if translation.get_language() not in ['fa', 'ar', 'ps']:
        return inputStr
    inputStr = str(inputStr)
    res = ''
    for lttr in inputStr:
        if lttr in persianiserDict:
            res += persianiserDict[lttr]
        else:
            res += lttr
    return res


def convertToDigit(inputStr):
    res = ''
    for lttr in inputStr:
        if lttr in digitConvertorDict:
            res += digitConvertorDict[lttr]
        elif lttr in arabicDigitConvertorDict:
            res += arabicDigitConvertorDict[lttr]
        elif lttr in englishDigits:
            res += lttr
    return res


def getJalaliDateFromISO(isoDate):
    dt = datetime.datetime.strptime(isoDate, '%Y-%m-%dT%H:%M:%S.%fZ')
    if translation.get_language() not in ['fa', 'ps']:
        return localtime(dt).strftime('%Y-%m-%d %H:%M:%S')
    dt = dt.replace(tzinfo=from_zone)
    dt = dt.astimezone(to_zone)
    jl = JalaliDatetime(dt)
    jlStr = jl.strftime('%N/%R/%D %k:%r:%s')
    return jlStr


def getJalaliDate(dt):
    if not dt:
        return ''
    if translation.get_language() not in ['fa', 'ps']:
        return localtime(dt).strftime('%Y-%m-%d %H:%M:%S')
    dt = dt.replace(tzinfo=from_zone)
    dt = dt.astimezone(to_zone)
    jl = JalaliDatetime(dt)
    jlStr = jl.strftime('%N/%R/%D %k:%r:%s')
    return jlStr
