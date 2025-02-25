import threading
import logging
import os
from scripts.generate_mt103 import save_mt103_messages
from scripts.generate_mt202 import save_mt202_messages
from scripts.generate_pacs008 import save_pacs008_messages
from scripts.generate_pacs009 import save_pacs009_messages

# Ensure logs directory exists before logging setup
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/main.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def generate_mt103():
    """Generate MT103 messages."""
    try:
        logging.info("Starting MT103 message generation...")
        save_mt103_messages()
        logging.info("✅ MT103 message generation completed successfully.")
    except Exception as e:
        logging.error(f"❌ Error in MT103 generation: {e}", exc_info=True)


def generate_mt202():
    """Generate MT202 messages."""
    try:
        logging.info("Starting MT202 message generation...")
        save_mt202_messages()
        logging.info("✅ MT202 message generation completed successfully.")
    except Exception as e:
        logging.error(f"❌ Error in MT202 generation: {e}", exc_info=True)


def generate_pacs008():
    """Generate pacs.008 messages."""
    try:
        logging.info("Starting pacs.008 message generation...")
        save_pacs008_messages()
        logging.info("✅ pacs.008 message generation completed successfully.")
    except Exception as e:
        logging.error(f"❌ Error in pacs.008 generation: {e}", exc_info=True)


def generate_pacs009():
    """Generate pacs.009 messages."""
    try:
        logging.info("Starting pacs.009 message generation...")
        save_pacs009_messages()
        logging.info("✅ pacs.009 message generation completed successfully.")
    except Exception as e:
        logging.error(f"❌ Error in pacs.009 generation: {e}", exc_info=True)


if __name__ == "__main__":
    print("\n🚀 Starting SWIFT message generation...")

    # Define all message types to generate
    tasks = {
        "MT103": generate_mt103,
        "MT202": generate_mt202,
        "pacs.008": generate_pacs008,
        "pacs.009": generate_pacs009
    }

    # Initialize and start threads
    threads = []
    for name, func in tasks.items():
        thread = threading.Thread(target=func, name=name, daemon=True)  # Use daemon to allow clean exits
        threads.append(thread)
        thread.start()
        print(f"📌 Started {name} generation...")

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("\n✅ All SWIFT messages generated successfully!")
    logging.info("✅ All SWIFT messages generated successfully.")
