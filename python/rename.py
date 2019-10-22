#!/usr/bin/env python3
import os
import re
import glob

cwd = os.path.join(
    os.environ['HOME'],
    'Movies/[异域-11番小队][来自风平浪静的明日 Nagi no Asukara][1-26][BDRIP][X264_AAC]'
)
apattern = r'\[Nagi.*\[(\d{2})(?:v\d)?\](?:.*?)\.(.*\.ass)'
mpattern = r'(.*\[{}\].*)\.mp4'

if __name__ == '__main__':
    os.chdir(cwd)
    ass = glob.glob('*.ass')
    mp4 = glob.glob('*.mp4')
    for af in sorted(ass):
        m = re.match(apattern, af)
        if m:
            for mf in mp4:
                x = re.match(mpattern.format(m.group(1)), mf)
                if x:
                    # print(af, '{}.{}'.format(x.group(1), m.group(2)))
                    os.rename(af, '{}.{}'.format(x.group(1), m.group(2)))
