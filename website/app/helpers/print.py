import time
import inspect


def retrieve_name(var):
    """
    Gets the name of var. Does it from the out most frame inner-wards.
    :param var: variable to get name from.
    :return: string
    """
    for fi in reversed(inspect.stack()):
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]

def sleep_sequence_print(count=5, sleep_time=1):
    # simply counts to i and logs to console
    for i in range(count + 1):
        print(i, flush=True)
        time.sleep(sleep_time)

def prnt(val, label=''):
    '''
    Print wrapper for clear logging
    '''
    if not label:
        label = retrieve_name(val)
    print(f"\n{label}: {val}\n", flush=True)