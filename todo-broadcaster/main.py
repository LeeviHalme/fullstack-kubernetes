import asyncio
import os
import json
import requests
from nats.aio.client import Client as NATS

NATS_URI = os.getenv("NATS_URI")
EXTERNAL_URL = os.getenv("EXTERNAL_URL")

async def run():
    """Main entry point for the broadcaster service."""
    nc = NATS()
    await nc.connect(NATS_URI)

    async def message_handler(msg):
        data = json.loads(msg.data.decode())
        print(f"Received message: {data}")

        try:
            # Send to your Generic URL
            response = requests.post(EXTERNAL_URL, json=data, timeout=5)
            if response.status_code == 200:
                print("Successfully forwarded to external service")
        except Exception as e: # pylint: disable=broad-except
            print(f"Failed to forward: {e}")

    # 'queue="workers"' ensures only ONE replica gets the message
    await nc.subscribe("todo_updates", queue="workers", cb=message_handler)

    print("Successfully connected to NATS at", NATS_URI)
    print("Broadcaster is listening for NATS messages...")

    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(run())
