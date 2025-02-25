import random
import logging
import os
import json
from utils.random_data import *
from datetime import datetime
from scripts.anomaly_rules import inject_anomalies

# Configure logging
logging.basicConfig(filename="logs/mt103_generation.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Load data from JSON files
DATA_PATH = "data"
BANKS_FILE = os.path.join(DATA_PATH, "banks.json")
ADDRESSES_FILE = os.path.join(DATA_PATH, "addresses.json")
RESTRICTED_CURRENCIES_FILE = os.path.join(DATA_PATH, "restricted_currencies.json")
VALID_CURRENCIES_FILE = os.path.join(DATA_PATH, "valid_currencies.json")
SANCTIONED_COUNTRIES_FILE = os.path.join(DATA_PATH, "sanctioned_countries.json")


def load_json(file_path):
    """Loads a JSON file safely and returns its content."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load {file_path}: {e}")
        return []  # Return empty list to prevent crashes


# Load datasets
banks_data = load_json(BANKS_FILE)
addresses_data = load_json(ADDRESSES_FILE)
restricted_currencies = set(load_json(RESTRICTED_CURRENCIES_FILE))
valid_currencies_data = set(load_json(VALID_CURRENCIES_FILE))
sanctioned_countries = set(load_json(SANCTIONED_COUNTRIES_FILE))


def get_valid_bank(is_unusual=False, exclude_country=None):
    """Returns a random bank ensuring valid BIC and real country-based filtering."""
    filtered_banks = [b for b in banks_data if b["country"] != exclude_country]
    return random.choice(filtered_banks) if filtered_banks else {"bic": "UNKNOWNBIC", "country": "Unknown"}


def get_real_address(country):
    """Returns a realistic geographic address for a given country."""
    country_addresses = [addr for addr in addresses_data if "address" in addr and addr["country"] == country]
    return random.choice(country_addresses)["address"] if country_addresses else "Unknown Address"


def get_valid_currency(is_unusual=False):
    """Returns a valid currency ensuring restricted currencies are avoided."""
    valid_currencies = [cur for cur in valid_currencies_data if cur not in restricted_currencies]
    return random.choice(valid_currencies) if valid_currencies else "USD"  # Default to USD if no valid options


def generate_mt103(is_unusual=False):
    """
    Generates a highly realistic MT103 message with:
    - Real BIC codes
    - Real addresses
    - Avoids restricted currencies
    - Flags sanctioned countries if needed
    """
    sender_bank = get_valid_bank(is_unusual)
    receiver_bank = get_valid_bank(is_unusual, exclude_country=sender_bank["country"])

    sender_bic = sender_bank["bic"]
    receiver_bic = receiver_bank["bic"]

    transaction_date = get_random_date()
    amount = get_random_amount(is_unusual)
    currency = get_valid_currency(is_unusual)
    reference = get_random_reference()
    sender_company = get_random_company()

    sender_address = get_real_address(sender_bank["country"])
    receiver_address = get_real_address(receiver_bank["country"])

    # Sanctioned country check
    is_sanctioned = sender_bank["country"] in sanctioned_countries or receiver_bank["country"] in sanctioned_countries

    # Inject anomalies if needed
    reason = None  # Initialize as None

    if is_unusual or is_sanctioned:
        reason = inject_anomalies(sender_bic, receiver_bic, currency, amount, transaction_date, reference, sender_company)

        if reason and reason != "USUAL":  # Only log and append if there's a real anomaly
            logging.warning(f"Unusual MT103 Transaction Detected - Reason: {reason}")

    message = f"""{{1:F01{sender_bic}1234567890}}{{2:O103{transaction_date}{receiver_bic}XXXXN}}{{3:{{121:{get_uuid()}}}}}{{4:
:20:{reference}
:23B:CRED
:32A:{transaction_date}{currency}{amount}
:50K:/OC{random.randint(1000000, 9999999)}
{sender_company}
{sender_address}
:57A:{receiver_bic}
:59:/BEN{random.randint(10000000000000, 99999999999999)}
{get_random_company()}
{receiver_address}
:70:INV {get_uuid().replace('-', '')[:12].upper()} {fake.sentence()}
:71A:OUR
-}}{{5:{{CHK:{get_uuid().replace('-', '')[:10]}}}}}"""

    if is_unusual or is_sanctioned:
        message += f" UNUSUAL REASON: {reason}"

    return message


def save_mt103_messages(num_messages=100):
    """
    Generates and saves highly realistic MT103 messages with:
    - Real banks
    - Real addresses
    - Cross-border logic
    - Sanctioned country flags
    """
    unusual_count = num_messages // 2
    usual_count = num_messages - unusual_count

    for i in range(1, usual_count + 1):
        message = generate_mt103(False)
        save_message(message, "mt103", i, False)

    for i in range(usual_count + 1, num_messages + 1):
        message = generate_mt103(True)
        save_message(message, "mt103", i, True)

    print(f"Generated {num_messages} MT103 messages.")


def save_message(message, folder, index, is_unusual, extension="txt"):
    """
    Saves an MT103 message to a file with 'usual' or 'unusual' in the name.
    """
    try:
        os.makedirs(f"messages/{folder}", exist_ok=True)
        label = "unusual" if is_unusual else "usual"
        file_path = f"messages/{folder}/{folder}_{label}_{index:05d}.{extension}"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(message)
        logging.info(f"Message saved: {file_path}")
    except Exception as e:
        logging.error(f"Failed to save message {index} in {folder}: {e}")


# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

save_mt103_messages()
