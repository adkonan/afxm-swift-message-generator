import random
import uuid
import json
import os
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Load datasets
with open("data/banks.json", "r") as f:
    BANKS = json.load(f)
with open("data/sanctioned_countries.json", "r") as f:
    SANCTIONED_COUNTRIES = json.load(f)
with open("data/restricted_currencies.json", "r") as f:
    RESTRICTED_CURRENCIES = json.load(f)

CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "SGD"]
TRANSACTION_HISTORY = {}


def get_random_bic():
    return random.choice(BANKS)["bic"]


def get_random_currency():
    if random.random() < 0.1:
        return random.choice(RESTRICTED_CURRENCIES)
    return random.choice(CURRENCIES)


def get_random_amount():
    amount = random.randint(1000, 500000)
    if random.random() < 0.2:
        amount *= random.choice([0.01, 10, 100])
    return f"{amount:.2f}"


def get_random_date():
    date = datetime.today() - timedelta(days=random.randint(1, 365))
    if random.random() < 0.05:
        date = date.replace(hour=random.choice([0, 1, 2, 3, 23]))
    return date.strftime("%y%m%d")


def get_uuid():
    return str(uuid.uuid4())


def get_random_company():
    return fake.company()


def get_random_address():
    return fake.address().replace("\n", " ")


def get_random_reference():
    return f"REF-{random.randint(10000, 99999)}"


def save_message(message, folder, index, extension="txt"):
    os.makedirs(f"messages/{folder}", exist_ok=True)
    file_path = f"messages/{folder}/{folder}_{index:05d}.{extension}"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(message)
