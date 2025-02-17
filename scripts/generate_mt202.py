from utils.random_data import *


def generate_mt202():
    sender_bic = get_random_bic()
    receiver_bic = get_random_bic()
    transaction_date = get_random_date()
    amount = get_random_amount()
    currency = get_random_currency()
    reference = get_random_reference()

    # Fraud scenarios
    if random.random() < 0.05:  # 5% chance: Same sender → same receiver multiple times
        transaction_count = TRANSACTION_HISTORY.get((sender_bic, receiver_bic), 0) + 1
        TRANSACTION_HISTORY[(sender_bic, receiver_bic)] = transaction_count
        if transaction_count > 3:
            print(f"Suspicious: {sender_bic} sent {transaction_count} transactions to {receiver_bic} in one day")

    if random.random() < 0.02:  # 2% chance: unusual currency usage
        currency = random.choice(RESTRICTED_CURRENCIES)
        print(f"Suspicious: Unusual currency {currency} detected")

    return f"""{{1:F01{sender_bic}1234567890}}{{2:I202{receiver_bic}XXXXN}}{{3:{{121:{get_uuid()}}}}}{{4:
:20:{reference}
:21:NONREF
:32A:{transaction_date}{currency}{amount}
:53B:/{random.randint(100000000, 999999999)}
:57A:{receiver_bic}
:58A:/{random.randint(100000000, 999999999)}
{get_random_company()}
-}}{{5:{{CHK:{get_uuid().replace('-', '')[:10]}}}}}"""


def save_mt202_messages(num_messages=10000):
    for i in range(1, num_messages + 1):
        save_message(generate_mt202(), "mt202", i)

    print(f"Generated {num_messages} MT202 messages.")


save_mt202_messages()
