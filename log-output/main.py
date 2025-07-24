import time
import random
import string
import signal
from datetime import datetime

def generate_random_string(length=12):
  return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

running = True

def main():
  random_str = generate_random_string()
  while running:
    timestamp = datetime.isoformat(datetime.now())
    print(f"{timestamp}: {random_str}")
    time.sleep(5)

def handle_sigterm():
    global running
    running = False

signal.signal(signal.SIGTERM, handle_sigterm)

if __name__ == "__main__":
  main()