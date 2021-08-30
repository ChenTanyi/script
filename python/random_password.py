#!/usr/bin/env python3
import sys
import random
import string

all_characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

if __name__ == '__main__':
    length = int(sys.argv[1])
    count = 1 if len(sys.argv) < 3 else int(sys.argv[2])
    for i in range(count):
        print(''.join(random.sample(all_characters, length)))
