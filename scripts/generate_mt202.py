import random
import logging
import os
import json
from utils.random_data import *
from datetime import datetime
from scripts.anomaly_rules import inject_anomalies

# Configure logging
logging.basicConfig(filename="logs/mt202_generation.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Load data from JSON files
DATA_PATH = "data"
BANKS_FILE = os.path.join(DATA_PATH, "banks.json")
ADDRESSES_FILE = os.path.join(DATA_PATH, "addresses.json")
RESTRICTED_CURRENCIES_FILE = os.path.join(DATA_PATH, "restricted_currencies.json")
SANCTIONED_COUNTRIES_FILE = os.path.join(DATA_PATH, "sanctioned_countries.json")


def load_json(file_path):
    """Loads a JSON file safely and returns its content."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load {file_path}: {e}")
        return {}


# Load datasets
banks_data = load_json(BANKS_FILE)
addresses_data = load_json(ADDRESSES_FILE)
restricted_currencies = set(load_json(RESTRICTED_CURRENCIES_FILE))
sanctioned_countries = set(load_json(SANCTIONED_COUNTRIES_FILE))

# Store transaction history for fraud detection
TRANSACTION_HISTORY = {}


def get_valid_bank(is_unusual=False, exclude_country=None):
    """Returns a random bank ensuring valid BIC and real country-based filtering."""
    filtered_banks = [b for b in banks_data if b["country"] != exclude_country]
    return random.choice(filtered_banks) if filtered_banks else random.choice(banks_data)


def get_real_address(country):
    """Returns a realistic geographic address for a given country."""
    country_addresses = [addr for addr in addresses_data if addr["country"] == country]
    return random.choice(country_addresses)["address"] if country_addresses else "Unknown Address"


def get_currency_list():
    """Returns a list of common valid currencies excluding restricted ones."""
    return [
        "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "HKD", "SGD", "ZAR",
        "NOK", "SEK", "DKK", "INR", "BRL", "RUB", "MXN", "KRW", "NZD", "TRY", "THB",
        "MYR", "IDR", "PHP", "PLN", "HUF", "CZK", "ILS", "AED", "SAR", "QAR", "KWD"
    ]


def get_valid_currency(is_unusual=False):
    """Returns a valid currency ensuring restricted currencies are avoided."""
    valid_currencies = [cur for cur in get_currency_list() if cur not in restricted_currencies]
    return random.choice(valid_currencies)


def generate_mt202(is_unusual=False):
    """
    Generates a highly realistic MT202 message with:
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

    sender_address = get_real_address(sender_bank["country"])
    receiver_address = get_real_address(receiver_bank["country"])

    # Sanctioned country check
    is_sanctioned = sender_bank["country"] in sanctioned_countries or receiver_bank["country"] in sanctioned_countries

    # Inject anomalies if needed
    reason = inject_anomalies(sender_bic, receiver_bic, currency, amount, transaction_date, reference, sender_bank["bank_name"])

    # Only log and append UNUSUAL REASON if there's an actual anomaly
    if reason and reason != "USUAL":
        logging.warning(f"Unusual MT202 Transaction Detected - Reason: {reason}")
        unusual_reason = f" UNUSUAL REASON: {reason}"
    else:
        unusual_reason = ""

    # Fraud Scenario 1: Repeated transactions between the same parties
    transaction_key = (sender_bic, receiver_bic)
    TRANSACTION_HISTORY[transaction_key] = TRANSACTION_HISTORY.get(transaction_key, 0) + 1
    if not is_unusual and TRANSACTION_HISTORY[transaction_key] > 3:
        logging.warning(
            f"⚠️ Suspicious: {sender_bic} sent {TRANSACTION_HISTORY[transaction_key]} transactions to {receiver_bic} in one day.")

    # Fraud Scenario 2: Unusual currency usage
    if not is_unusual and random.random() < 0.02:  # 2% chance of unusual currency
        currency = random.choice(list(restricted_currencies))
        logging.warning(f"⚠️ Suspicious: Unusual currency {currency} detected in MT202 transaction.")

    message = f"""{{1:F01{sender_bic}1234567890}}{{2:I202{receiver_bic}XXXXN}}{{3:{{121:{get_uuid()}}}}}{{4:
:20:{reference}
:21:NONREF
:32A:{transaction_date}{currency}{amount}
:53B:/{random.randint(100000000, 999999999)}
{sender_address}
:57A:{receiver_bic}
:58A:/{random.randint(100000000, 999999999)}
{receiver_address}
-}}{{5:{{CHK:{get_uuid().replace('-', '')[:10]}}}}}{unusual_reason}"""

    return message


def save_mt202_messages(num_messages=100):
    """
    Generates and saves highly realistic MT202 messages with:
    - Real banks
    - Real addresses
    - Cross-border logic
    - Sanctioned country flags
    """
    unusual_count = num_messages // 2
    usual_count = num_messages - unusual_count

    for i in range(1, usual_count + 1):
        message = generate_mt202(False)
        save_message(message, "mt202", i, False)

    for i in range(usual_count + 1, num_messages + 1):
        message = generate_mt202(True)
        save_message(message, "mt202", i, True)

    print(f"Generated {num_messages} MT202 messages.")


def save_message(message, folder, index, is_unusual, extension="txt"):
    """
    Saves an MT202 message to a file with 'usual' or 'unusual' in the name.
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

save_mt202_messages()
