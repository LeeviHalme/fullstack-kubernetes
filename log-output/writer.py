import os
import time
import random
import string
import signal
from datetime import datetime

def generate_random_string(length=12):
    """Generate a random alphanumeric string of given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

IS_RUNNING = True

def main():
    """Main loop to write timestamped random strings to output file every 5 seconds."""

    random_str = generate_random_string()
    output_file_path = os.getenv("OUTPUT_FILE_PATH")

    while IS_RUNNING:
        timestamp = datetime.isoformat(datetime.now())
        content = f"{timestamp}: {random_str}"
        print(f"Writing: {content}")

        with open(output_file_path, "w") as file:
            file.write(content)

        time.sleep(5)

def handle_sigterm():
    """Handle SIGTERM signal to gracefully stop the main loop."""
    # pylint: disable=global-statement
    global IS_RUNNING
    IS_RUNNING = False

signal.signal(signal.SIGTERM, handle_sigterm)

if __name__ == "__main__":
    main()
