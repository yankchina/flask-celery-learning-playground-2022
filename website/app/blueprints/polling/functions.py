import asyncio
from app.blueprints.polling import bp
import random


async def async_get_data():
    while True:
        await asyncio.sleep(1)
        if random.randint(0, 1000) > 200:
            test_success()
        else:
            test_failure()

    # await asyncio.sleep(1)
    # return 'Done!'


def test_success(i):
    print(f"Value: {i} was a success!", flush=True)

def test_failure():
    print("failed", flush=True)