import random
import uuid
import json
import os
import logging
from datetime import datetime, timedelta
from faker import Faker

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(filename="logs/random_data.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Faker
fake = Faker()

# Load datasets with error handling
try:
    with open("data/banks.json", "r", encoding="utf-8") as f:
        BANKS = json.load(f)
    with open("data/addresses.json", "r", encoding="utf-8") as f:
        ADDRESSES = json.load(f)
    with open("data/valid_currencies.json", "r", encoding="utf-8") as f:
        VALID_CURRENCIES = json.load(f)
    with open("data/restricted_currencies.json", "r", encoding="utf-8") as f:
        RESTRICTED_CURRENCIES = json.load(f)
    with open("data/sanctioned_countries.json", "r", encoding="utf-8") as f:
        SANCTIONED_COUNTRIES = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    logging.error(f"❌ Data file issue: {e}")
    BANKS, ADDRESSES, VALID_CURRENCIES, RESTRICTED_CURRENCIES, SANCTIONED_COUNTRIES = [], [], [], [], []

# Extract valid BICs and their corresponding countries from banks.json
VALID_BICS = {bank["bic"]: bank["country"] for bank in BANKS if "bic" in bank and len(bank["bic"]) == 11}

# Extract valid currencies
CURRENCIES = VALID_CURRENCIES if VALID_CURRENCIES else ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "SGD"]

# Dictionary to track repeated transactions
TRANSACTION_HISTORY = {}


def get_random_bic(is_unusual=False):
    """Returns a valid BIC from the bank list. Ensures all BICs are valid."""
    if VALID_BICS and not is_unusual:
        return random.choice(list(VALID_BICS.keys()))
    elif is_unusual:
        anomaly_bic = random.choice(list(VALID_BICS.keys()))  # Keep BIC valid, but modify usage
        logging.warning(f"⚠️ Unusual transaction detected with BIC: {anomaly_bic}")
        return anomaly_bic
    else:
        logging.warning("⚠️ No valid BICs available. Returning UNKNOWN BIC.")
        return "UNKNOWNBIC"


def get_random_currency(is_unusual=False):
    """Returns a valid currency or a restricted one if an anomaly is required."""
    if is_unusual and RESTRICTED_CURRENCIES:
        restricted_currency = random.choice(RESTRICTED_CURRENCIES)
        logging.warning(f"⚠️ Anomalous restricted currency selected: {restricted_currency}")
        return restricted_currency
    return random.choice(CURRENCIES)


def get_random_amount(is_unusual=False):
    """Generates a realistic transaction amount with anomalies where necessary."""
    amount = round(random.uniform(1000, 500000), 2)  # Normal transactions
    if is_unusual:
        amount = random.choice([0.01, round(random.uniform(1000000, 5000000), 2)])  # Suspicious values
        logging.warning(f"⚠️ Anomalous amount generated: {amount}")
    return f"{amount:.2f}"


def get_random_date():
    """Generates a realistic transaction date with occasional unusual timestamps."""
    date = datetime.today() - timedelta(days=random.randint(1, 365))
    if random.random() < 0.05:  # 5% chance of unusual transaction time
        date = date.replace(hour=random.choice([0, 1, 2, 3, 23]))
        logging.warning(f"⚠️ Unusual transaction time detected: {date.strftime('%Y-%m-%d %H:%M')}")
    return date.strftime("%y%m%d")


def get_uuid():
    """Generates a universally unique identifier."""
    return str(uuid.uuid4())


def get_random_company():
    """Generates a realistic company name."""
    return fake.company()


def get_random_address(is_unusual=False):
    """Returns a real geographic address, ensuring country consistency."""
    if ADDRESSES:
        selected_address = random.choice(ADDRESSES)
        if is_unusual and SANCTIONED_COUNTRIES:
            selected_address["country"] = random.choice(SANCTIONED_COUNTRIES)  # Inject a sanctioned country
            logging.warning(f"⚠️ Injected address from sanctioned country: {selected_address}")
        return f"{selected_address['street']}, {selected_address['city']}, {selected_address['country']}"
    else:
        logging.warning("⚠️ No addresses found. Generating fake address.")
        return fake.address().replace("\n", ", ")


def get_random_reference():
    """Creates a structured transaction reference ID."""
    return f"REF-{random.randint(10000, 99999)}"


def save_message(message, folder, index, is_unusual, extension="txt"):
    """Saves a message to a file with 'usual' or 'unusual' in the name."""
    try:
        os.makedirs(f"messages/{folder}", exist_ok=True)
        label = "unusual" if is_unusual else "usual"
        file_path = f"messages/{folder}/{folder}_{label}_{index:05d}.{extension}"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(message)
        logging.info(f"✅ Message saved: {file_path}")
    except Exception as e:
        logging.error(f"❌ Failed to save message {index} in {folder}: {e}")
