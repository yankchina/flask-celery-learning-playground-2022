import time


def throttle_print(count=5):
    # simply counts to i and logs to console
    for i in range(count + 1):
        print(i, flush=True)
        time.sleep(1)