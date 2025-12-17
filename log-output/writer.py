import time
import random
import string
import signal
from datetime import datetime

def generate_random_string(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

IS_RUNNING = True

def main():
    random_str = generate_random_string()
    while IS_RUNNING:
        timestamp = datetime.isoformat(datetime.now())
        content = f"{timestamp}: {random_str}"
        print(f"Writing: {content}")

        with open("files/output.txt", "w") as file:
            file.write(content)

        time.sleep(5)

def handle_sigterm():
    global IS_RUNNING
    IS_RUNNING = False

signal.signal(signal.SIGTERM, handle_sigterm)

if __name__ == "__main__":
    main()