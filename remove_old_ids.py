import asyncio
import os
from dotenv import load_dotenv
from nio import AsyncClient, LoginResponse

load_dotenv()

HOMESERVER = os.getenv("MATRIX_HOMESERVER")
USERNAME = os.getenv("MATRIX_USER")
PASSWORD = os.getenv("MATRIX_PASSWORD")

# The device_id your bot currently uses (keep this one!) — read from device_id.json
import json
with open("device_id.json") as f:
    CURRENT_DEVICE_ID = json.load(f)["device_id"]


async def main():
    client = AsyncClient(HOMESERVER, USERNAME)
    resp = await client.login(PASSWORD)
    if not isinstance(resp, LoginResponse):
        print(f"Login failed: {resp}")
        return

    devices_resp = await client.devices()
    all_ids = [d.id for d in devices_resp.devices]
    stale_ids = [d for d in all_ids if d != CURRENT_DEVICE_ID and d != client.device_id]

    print(f"Found devices: {all_ids}")
    print(f"Deleting stale: {stale_ids}")

    if stale_ids:
        # delete_devices requires UIA (password re-auth)
        resp = await client.delete_devices(
            stale_ids,
            auth={
                "type": "m.login.password",
                "user": USERNAME,
                "password": PASSWORD,
            },
        )
        print(resp)

    await client.close()


asyncio.run(main())
