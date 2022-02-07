import time


def time_printer(passed_time=None, programm_step=None):

    if passed_time is None:
        timer = time.time()
        print(f'--INFO:-- Start: {programm_step} ----')
    else:
        timer = time.time() - passed_time
        print(f"--INFO:-- Finished: {programm_step} ----")
        print(f"--INFO:-- Time: {round(timer,2)} sec ----")
    return timer
