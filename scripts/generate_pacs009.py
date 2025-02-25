import random
import logging
import os
import json
from utils.random_data import *
from datetime import datetime
from scripts.anomaly_rules import inject_anomalies

# Configure logging
logging.basicConfig(filename="logs/pacs009_generation.log", level=logging.INFO,
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
    ]  # These are standard global trade currencies


def get_valid_currency(is_unusual=False):
    """Returns a valid currency ensuring restricted currencies are avoided."""
    valid_currencies = [cur for cur in get_currency_list() if cur not in restricted_currencies]
    return random.choice(valid_currencies)


def generate_pacs009(is_unusual=False):
    """
    Generates a highly realistic pacs.009 XML message with:
    - Real BIC codes
    - Real addresses
    - Avoids restricted currencies
    - Flags sanctioned countries if needed
    """
    sender_bank = get_valid_bank(is_unusual)
    receiver_bank = get_valid_bank(is_unusual, exclude_country=sender_bank["country"])

    sender_bic = sender_bank["bic"]
    receiver_bic = receiver_bank["bic"]

    amount = get_random_amount(is_unusual)
    currency = get_valid_currency(is_unusual)
    reference = get_random_reference()
    transaction_date = get_random_date()

    sender_address = get_real_address(sender_bank["country"])
    receiver_address = get_real_address(receiver_bank["country"])

    # Sanctioned country check
    is_sanctioned = sender_bank["country"] in sanctioned_countries or receiver_bank["country"] in sanctioned_countries

    # Inject anomalies if needed
    reason = None  # Initialize with None to avoid incorrect "USUAL"
    if is_unusual or is_sanctioned:
        reason = inject_anomalies(sender_bic, receiver_bic, currency, amount, transaction_date, reference, sender_bank["bank_name"])

        if reason and reason != "USUAL":  # Only log actual anomalies
            logging.warning(f"Unusual pacs.009 Transaction Detected - Reason: {reason}")

    # Fraud Scenario: Transaction involving sanctioned country
    if not is_unusual and random.random() < 0.03:  # 3% chance of involving sanctioned country
        sanctioned_country = random.choice(list(sanctioned_countries))
        reason = f"Transaction involving sanctioned country: {sanctioned_country}"
        logging.warning(f"⚠️ Suspicious: {reason}")

    message = f"""<?xml version="1.0" encoding="UTF-8"?>
<RequestPayload>
   <AppHdr>
      <Fr><FIId><FinInstnId><BICFI>{sender_bic}</BICFI></FinInstnId></FIId></Fr>
      <To><FIId><FinInstnId><BICFI>{receiver_bic}</BICFI></FinInstnId></FIId></To>
      <BizMsgIdr>{reference}</BizMsgIdr>
      <MsgDefIdr>pacs.009.001.08</MsgDefIdr>
      <CreDt>{datetime.now().isoformat()}</CreDt>
   </AppHdr>
   <Document>
      <FICdtTrf>
         <GrpHdr>
            <MsgId>{reference}</MsgId>
            <CreDtTm>{datetime.now().isoformat()}</CreDtTm>
            <NbOfTxs>1</NbOfTxs>
         </GrpHdr>
         <CdtTrfTxInf>
            <IntrBkSttlmAmt Ccy="{currency}">{amount}</IntrBkSttlmAmt>
            <Dbtr>
               <Nm>{get_random_company()}</Nm>
               <PstlAdr>
                   <StrtNm>{sender_address}</StrtNm>
                   <Ctry>{sender_bank["country"]}</Ctry>
               </PstlAdr>
            </Dbtr>
            <Cdtr>
               <Nm>{get_random_company()}</Nm>
               <PstlAdr>
                   <StrtNm>{receiver_address}</StrtNm>
                   <Ctry>{receiver_bank["country"]}</Ctry>
               </PstlAdr>
            </Cdtr>
         </CdtTrfTxInf>
      </FICdtTrf>
   </Document>
</RequestPayload>"""

    if is_unusual or is_sanctioned:
        message += f"<!-- UNUSUAL REASON: {reason} -->"

    return message


def save_pacs009_messages(num_messages=100):
    """
    Generates and saves highly realistic pacs.009 messages with:
    - Real banks
    - Real addresses
    - Cross-border logic
    - Sanctioned country flags
    """
    unusual_count = num_messages // 2
    usual_count = num_messages - unusual_count

    for i in range(1, usual_count + 1):
        message = generate_pacs009(False)
        save_message(message, "pacs009", i, False, "xml")

    for i in range(usual_count + 1, num_messages + 1):
        message = generate_pacs009(True)
        save_message(message, "pacs009", i, True, "xml")

    print(f"Generated {num_messages} pacs.009 messages.")


def save_message(message, folder, index, is_unusual, extension="xml"):
    """
    Saves a pacs.009 message to a file with 'usual' or 'unusual' in the name.
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

save_pacs009_messages()
