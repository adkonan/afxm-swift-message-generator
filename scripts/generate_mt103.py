from utils.random_data import *


def generate_mt103():
    sender_bic = get_random_bic()
    receiver_bic = get_random_bic()
    transaction_date = get_random_date()
    amount = get_random_amount()
    currency = get_random_currency()
    reference = get_random_reference()

    return f"""{{1:F01{sender_bic}1234567890}}{{2:O103{transaction_date}{receiver_bic}XXXXN}}{{3:{{121:{get_uuid()}}}}}{{4:
:20:{reference}
:23B:CRED
:32A:{transaction_date}{currency}{amount}
:50K:/OC{random.randint(1000000, 9999999)}
{get_random_company()}
{get_random_address()}
:57A:{receiver_bic}
:59:/BEN{random.randint(10000000000000, 99999999999999)}
{get_random_company()}
{get_random_address()}
:70:INV {get_uuid().replace('-', '')[:12].upper()} {fake.sentence()}
:71A:OUR
-}}{{5:{{CHK:{get_uuid().replace('-', '')[:10]}}}}}"""


def save_mt103_messages(num_messages=10000):
    for i in range(1, num_messages + 1):
        save_message(generate_mt103(), "mt103", i)


save_mt103_messages()
