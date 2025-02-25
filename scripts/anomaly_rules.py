import random
import logging
import json
from datetime import datetime
from utils.random_data import TRANSACTION_HISTORY

# Ensure logs directory exists
import os
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(filename="logs/anomaly_detection.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Load data files with error handling
try:
    with open("data/restricted_currencies.json", "r") as f:
        RESTRICTED_CURRENCIES = json.load(f)
    with open("data/valid_currencies.json", "r") as f:
        VALID_CURRENCIES = json.load(f)
    with open("data/sanctioned_countries.json", "r") as f:
        SANCTIONED_COUNTRIES = json.load(f)
except FileNotFoundError as e:
    logging.error(f"Missing data file: {e}")
    RESTRICTED_CURRENCIES, VALID_CURRENCIES, SANCTIONED_COUNTRIES = [], [], []

REFERENCE_TRACKER = {}  # Track duplicate references
FRAUDULENT_COMPANIES = set()  # Track flagged fraudulent companies


def inject_anomalies(sender_bic, receiver_bic, currency, amount, transaction_date, reference, sender_company):
    """Injects anomalies into transactions based on predefined fraud scenarios."""
    anomalies = []

    # 1. High-Frequency Transactions (Same Sender → Same Beneficiary)
    transaction_key = (sender_bic, receiver_bic)
    TRANSACTION_HISTORY[transaction_key] = TRANSACTION_HISTORY.get(transaction_key, 0) + 1
    if TRANSACTION_HISTORY[transaction_key] > 3:
        anomalies.append(random.choice([
            f"Frequent transactions detected: {TRANSACTION_HISTORY[transaction_key]} times within a short period.",
            f"Possible structuring: {TRANSACTION_HISTORY[transaction_key]} transactions observed between the same entities.",
            f"Unusual transaction pattern: Repeated payments ({TRANSACTION_HISTORY[transaction_key]} times) within a short timeframe."
        ]))

    # 2. Abnormal Transaction Amounts
    try:
        amount_float = float(amount)
        if amount_float > 10000000:
            anomalies.append(random.choice([
                f"Large transaction alert: {amount} appears significantly above normal limits.",
                f"Suspiciously high transfer: Amount of {amount} exceeds threshold.",
                f"Potential fraud risk: Extremely high amount ({amount}) not typical for this sender."
            ]))
    except ValueError:
        anomalies.append("Transaction amount format error detected.")

    # 3. Transactions with a Sanctioned Country
    if SANCTIONED_COUNTRIES and (random.random() < 0.03 or sender_bic[:2] in SANCTIONED_COUNTRIES or receiver_bic[:2] in SANCTIONED_COUNTRIES):
        sanctioned_country = random.choice(SANCTIONED_COUNTRIES)
        anomalies.append(random.choice([
            f"Transaction flagged: Involves {sanctioned_country}, which is under international sanctions.",
            f"High-risk transfer: {sanctioned_country} is flagged for financial concerns.",
            f"Compliance alert: Payment routed through {sanctioned_country}, requiring review."
        ]))

    # 4. Invalid BIC Codes
    if sender_bic == "INVALIDBIC" or receiver_bic == "INVALIDBIC":
        anomalies.append(random.choice([
            "Financial institution verification failed: BIC code invalid.",
            "Suspicious institution: BIC code used in the transaction is incorrect.",
            "Transaction error: Unrecognized BIC code detected."
        ]))

    # 5. Unusual Currency Usage
    if currency in RESTRICTED_CURRENCIES:
        anomalies.append(random.choice([
            f"Rare currency detected: {currency} is not typically used for such transactions.",
            f"Transaction flagged: {currency} is restricted or under monitoring.",
            f"Uncommon currency warning: {currency} appears outside usual trading patterns."
        ]))

    # 6. Duplicate Transaction Reference
    if reference in REFERENCE_TRACKER:
        anomalies.append(random.choice([
            f"Possible duplicate reference: Transaction ID {reference} has been used before.",
            f"Duplicate transaction detected: Reference {reference} matches a previous transaction.",
            f"Compliance alert: Repeated reference {reference} might indicate suspicious activity."
        ]))
    else:
        REFERENCE_TRACKER[reference] = 1  # Store unique reference

    # 7. Fraudulent Company Behavior
    if sender_company in FRAUDULENT_COMPANIES:
        anomalies.append(random.choice([
            f"High-risk entity detected: {sender_company} has been flagged for suspicious transactions.",
            f"Potential shell company: {sender_company} has been associated with anomalies before.",
            f"Financial fraud warning: {sender_company} is under review for money laundering risks."
        ]))
    elif random.random() < 0.02:  # 2% chance to randomly flag a new company
        FRAUDULENT_COMPANIES.add(sender_company)
        anomalies.append(f"New high-risk entity: {sender_company} added to fraud watchlist.")

    # 8. Round-Number Transactions
    if amount_float % 10000 == 0:
        anomalies.append(random.choice([
            "Possible structuring attempt: Transaction amount is a round figure.",
            "Red flag: Large round-number transactions are often linked to laundering.",
            "Suspicious structuring: Use of round amounts may indicate financial manipulation."
        ]))

    # 9. Transactions with Recently Opened Accounts
    if random.random() < 0.02:
        anomalies.append(random.choice([
            "High-risk account: Transaction from a newly created financial account.",
            "Unverified source: Account has limited transaction history.",
            "Fraud alert: Transaction involves a recently opened or inactive account."
        ]))

    # 10. Rapid Movement of Funds
    if random.random() < 0.04:
        anomalies.append(random.choice([
            "Fast fund transfers detected: Money moving between multiple accounts.",
            "Suspicious activity: Money passes through accounts too quickly.",
            "Red flag: Funds moving rapidly through unrelated entities."
        ]))

    # 11. Payments to Offshore Financial Centers
    if random.random() < 0.03:
        anomalies.append(random.choice([
            "Offshore transaction warning: Payment linked to tax haven jurisdiction.",
            "Financial secrecy risk: Destination country known for weak regulatory oversight.",
            "Potential laundering risk: Transfer involves an offshore financial hub."
        ]))

    # 12. Dormant Account Activity
    if random.random() < 0.02:
        anomalies.append(random.choice([
            "Reactivated account: Transaction detected from previously inactive entity.",
            "Fraud warning: Dormant account suddenly engaged in financial activity.",
            "High-risk activity: Suspicious transaction from an unused account."
        ]))

    # 13. Unusual Payment Instructions
    if random.random() < 0.03:
        anomalies.append(random.choice([
            "Non-standard payment description detected.",
            "Suspicious transaction details: Lack of clear payment purpose.",
            "Compliance review needed: Payment instructions contain vague or misleading terms."
        ]))

    # Log anomalies
    if anomalies:
        logging.warning(f"Anomaly Detected: {', '.join(anomalies)}")

    return " | ".join(anomalies) if anomalies else "USUAL"
