# 🚀 SWIFT Message Generator (MT103, MT202, pacs.008, pacs.009)

## 📌 Overview
The **SWIFT Message Generator** is a **production-grade Python project** that creates **MT103, MT202, pacs.008, and pacs.009** messages with **maximum possible fields** and **fraudulent patterns** for anomaly detection.

This project is designed to **simulate real-world financial transactions** while embedding suspicious transaction behaviors, such as:
- **High-frequency transactions between the same sender and beneficiary**
- **Large or extremely small transaction amounts**
- **Use of unusual trade currencies**
- **Transactions to first-time beneficiaries**
- **Transactions at abnormal times (midnight, weekends, holidays)**
- **Circular transactions between multiple entities**
- **Involvement of sanctioned countries or institutions**

Each generated message is **saved as an individual file** in the `messages/` directory, organized by message type.

---

## 📂 Project Structure

```
swift_message_generator/
│── messages/
│   ├── mt103/      # Folder for generated MT103 messages
│   ├── mt202/      # Folder for generated MT202 messages
│   ├── pacs008/    # Folder for generated pacs.008 messages
│   ├── pacs009/    # Folder for generated pacs.009 messages
│── data/
│   ├── banks.json                # List of real-world banks with BIC codes
│   ├── sanctioned_countries.json  # List of countries under international sanctions
│   ├── restricted_currencies.json # List of rarely used trade currencies
│── scripts/
│   ├── generate_mt103.py          # Script to generate MT103 messages
│   ├── generate_mt202.py          # Script to generate MT202 messages
│   ├── generate_pacs008.py        # Script to generate pacs.008 messages
│   ├── generate_pacs009.py        # Script to generate pacs.009 messages
│── utils/
│   ├── random_data.py             # Utility functions for random data generation
│── main.py                        # Master script to generate all message types
│── requirements.txt                # Dependencies file
│── README.md                      # Documentation file
```

---

## 🛠 Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/swift-message-generator.git
cd swift-message-generator
```

### **2️⃣ Create a Virtual Environment (Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the SWIFT Message Generator**
To generate **all message types**:
```bash
python main.py
```

---

## 📜 SWIFT Message Formats

### **MT103 - Single Customer Credit Transfer**
- Used for **international wire transfers** between financial institutions.
- Includes **sender, receiver, transaction details, and purpose**.

### **MT202 - Financial Institution Transfer**
- Used for **bank-to-bank transfers**.
- Contains **interbank settlement instructions**.

### **pacs.008 - Customer Credit Transfer**
- Used in **ISO 20022 payment messaging**.
- Contains **detailed information about transaction parties**.

---

## 📊 **Fraudulent Transaction Patterns**
The generator **embeds fraud detection elements** in transactions:
- **🚨 Same sender → same beneficiary multiple times a day**
- **🚨 Unusual currency usage**
- **🚨 Transactions at suspicious times (midnight, weekends)**
- **🚨 Large transactions after a long period of inactivity**
- **🚨 Circular transactions among multiple accounts**
- **🚨 Beneficiaries receiving a payment for the first time**
- **🚨 Sanctioned country involvement**
- **🚨 High-velocity transactions in a short timeframe**

Fraud indicators are **printed in the console** during execution.

---

## 📩 **Saving and Viewing Messages**
All generated messages are **saved in separate files** under:
```
messages/mt103/
messages/mt202/
messages/pacs008/
messages/pacs009/
```
To inspect messages:
```bash
cat messages/mt103/mt103_00001.txt
cat messages/pacs008/pacs008_00001.xml
```

---

## ⚡ **Contributions**
If you'd like to **improve fraud detection** or **extend message types**, feel free to **submit a pull request**!

---

## 🏆 **License**
This project is **MIT licensed**. Feel free to use, modify, and distribute.

---

🚀 **Now you're ready to generate high-quality SWIFT messages with built-in fraud patterns!** 🚀
