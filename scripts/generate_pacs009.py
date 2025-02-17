from utils.random_data import *


def generate_pacs009():
    sender_bic = get_random_bic()
    receiver_bic = get_random_bic()
    amount = get_random_amount()
    currency = get_random_currency()
    reference = get_random_reference()

    return f"""<?xml version="1.0" encoding="UTF-8"?>
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
         </CdtTrfTxInf>
      </FICdtTrf>
   </Document>
</RequestPayload>"""


def save_pacs009_messages(num_messages=10000):
    for i in range(1, num_messages + 1):
        save_message(generate_pacs009(), "pacs009", i, "xml")


save_pacs009_messages()
