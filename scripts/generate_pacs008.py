from utils.random_data import *


def generate_pacs008():
    sender_bic = get_random_bic()
    receiver_bic = get_random_bic()
    amount = get_random_amount()
    currency = get_random_currency()
    reference = get_random_reference()

    # Fraud scenarios
    if random.random() < 0.03:  # 3% chance: transaction with sanctioned country
        sender_country = random.choice(SANCTIONED_COUNTRIES)
        print(f"Suspicious: Transaction involving {sender_country}")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<RequestPayload>
   <AppHdr>
      <Fr><FIId><FinInstnId><BICFI>{sender_bic}</BICFI></FinInstnId></FIId></Fr>
      <To><FIId><FinInstnId><BICFI>{receiver_bic}</BICFI></FinInstnId></FIId></To>
      <BizMsgIdr>{reference}</BizMsgIdr>
      <MsgDefIdr>pacs.008.001.08</MsgDefIdr>
      <CreDt>{datetime.now().isoformat()}</CreDt>
   </AppHdr>
   <Document>
      <FIToFICstmrCdtTrf>
         <GrpHdr>
            <MsgId>{reference}</MsgId>
            <CreDtTm>{datetime.now().isoformat()}</CreDtTm>
            <NbOfTxs>1</NbOfTxs>
         </GrpHdr>
         <CdtTrfTxInf>
            <IntrBkSttlmAmt Ccy="{currency}">{amount}</IntrBkSttlmAmt>
            <Dbtr><Nm>{get_random_company()}</Nm></Dbtr>
            <Cdtr><Nm>{get_random_company()}</Nm></Cdtr>
         </CdtTrfTxInf>
      </FIToFICstmrCdtTrf>
   </Document>
</RequestPayload>"""


def save_pacs008_messages(num_messages=10000):
    for i in range(1, num_messages + 1):
        save_message(generate_pacs008(), "pacs008", i, "xml")

    print(f"Generated {num_messages} pacs.008 messages.")


save_pacs008_messages()
