#!/usr/bin/env python3
import os
import re
import sys
import subprocess
from datetime import timedelta

d = sys.argv[1]
for ds in os.listdir(d):
    ds = os.path.join(d, ds)
    if os.path.isdir(ds):
        duration = timedelta(0)
        for f in os.listdir(ds):
            f = os.path.join(ds, f)
            stdout = subprocess.run(
                f'ffprobe {f}',
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                shell = True).stderr
            x = re.search(b'Duration: (\d+):(\d+):(\d+\.\d+)', stdout)
            duration += timedelta(
                hours = int(x.group(1)),
                minutes = int(x.group(2)),
                seconds = float(x.group(3)))

        print(ds, duration)
