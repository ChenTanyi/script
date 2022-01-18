#!/usr/bin/env python3
import time
import ctypes

ES_AWAYMODE_REQUIRED = 0x00000040
ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002
ES_SYSTEM_REQUIRED = 0x00000001


def awake_windows(timestamp: float):
    while True:
        if 0 < timestamp < time.time():
            break
        ctypes.windll.kernel32.SetThreadExecutionState(ES_DISPLAY_REQUIRED)
        time.sleep(30)


if __name__ == "__main__":
    awake_windows(0)