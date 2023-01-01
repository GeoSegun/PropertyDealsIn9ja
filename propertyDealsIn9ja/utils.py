import json
import random
import smtplib
import string
from json import JSONDecodeError

import phonenumbers
from django.db.models import F
from phonenumbers import geocoder, region_code_for_country_code
from requests.exceptions import ConnectionError
import requests
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    slug = new_slug if new_slug is not None else slugify(instance.name)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def send_email(user, password, recipient, subject, body):

    gmail_user = user
    gmail_pwd = password
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = f"""From: {FROM}\nTo: {", ".join(TO)}\nSubject: {SUBJECT}\n\n{TEXT}
    """
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    print("email sent!")
    server.close()


def exchange_rate(instance, price, rate, currency):
    upload_price = price
    x_rate = rate
    if instance.currency == currency:
        upload_price *= x_rate
        return upload_price
    return upload_price


def debit_wallet(instance, price):
    if instance.balance >= price:
        instance.balance = F('balance') - price
        instance.save()
        return True
    return False


def list_bank_names(country, public_key):
    try:
        url = f"https://api.flutterwave.com/v3/banks/{country}?public_key={public_key}"
        payload = {}
        headers = {'Authorization': 'Bearer FLWSECK_TEST-SANDBOXDEMOKEY-X'}
        response = requests.request("GET", url, headers=headers, data=payload)
        banks = json.loads(response.text)
        return [b["name"] for b in banks["data"]]
    except Exception as e:
        print(e)
        return None


def get_bank_detail(bank_country, account_bank, skey):
    try:
        url = f"https://api.flutterwave.com/v3/banks/{bank_country}?public_key={skey}"
        payload = {}
        headers = {'Authorization': 'Bearer FLWSECK_TEST-SANDBOXDEMOKEY-X'}
        response = requests.request("GET", url, headers=headers, data=payload)
        banks = json.loads(response.text)
        print(next(bank for bank in banks["data"] if bank["name"] == account_bank))
        return next(bank for bank in banks["data"] if bank["name"] == account_bank)
    except Exception as e:
        print(e)
        return None


def create_sub_account(bank, num, biz_name, biz_email, biz_contact, biz_mob, biz_mob2, country, split_value, routing_num, swift_code, branch_code, secret_key):
    try:
        url = "https://api.flutterwave.com/v3/subaccounts"
        payload = json.dumps({
            "account_bank": f"{bank}",
            "account_number": f"{num}",
            "business_name": f"{biz_name}",
            "business_email": f"{biz_email}",
            "business_contact": f"{biz_contact}",
            "business_contact_mobile": f"{biz_mob}",
            "business_mobile": f"{biz_mob2}",
            "country": f"{country}",
            "split_type": "percentage",
            "split_value": split_value,
            "meta": [
                {
                    "routingNumber": routing_num,
                    "swiftCode": swift_code,
                },
                {
                    "branchCode": branch_code,
                },
            ],
        })
        headers = {
          'Content-Type': 'application/json',
          'Authorization': f'Bearer {secret_key}'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print("executing ==> create_sub_account()")
        print(json.loads(response.text))
        return json.loads(response.text)
    except Exception as e:
        print(e)
        return None


def get_phone_country(phone_number):
    i = phonenumbers.parse(phone_number)
    return region_code_for_country_code(i.country_code)
    # return geocoder.description_for_number(i, "en")


def get_states(json_file_dir):
    file_path = json_file_dir
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return [b for b in data]


# Get nested states by names
def get_states_only(json_file_dir):
    file_path = json_file_dir
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return [b["name"] for b in data]


def get_cities_only(json_file_dir, state):
    file_path = json_file_dir
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return next(b['cities'] for b in data if b["name"] == state)




