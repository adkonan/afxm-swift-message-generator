from scripts.generate_mt103 import save_mt103_messages
from scripts.generate_mt202 import save_mt202_messages
from scripts.generate_pacs008 import save_pacs008_messages
from scripts.generate_pacs009 import save_pacs009_messages

if __name__ == "__main__":
    print("Generating SWIFT Messages...")

    save_mt103_messages()
    save_mt202_messages()
    save_pacs008_messages()
    save_pacs009_messages()

    print("All messages generated and saved in separate files.")
