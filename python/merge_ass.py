#!/usr/bin/env python3
import os
import re

total = 1
first_folder = ''
first_file = r'.*\[{:0>2d}\].*\.ass'
first_encode = 'utf-16-le'
second_folder = ''
second_file = r'.*\[{:0>2d}\].*\.ass'
second_encode = 'utf-16-le'

output_folder = ''
output_file = r'(.*[{:0>2d}].*)\.mkv'

skip_part = ['[Script Info]']
merge_part = ['[V4+ Styles]', '[Events]']


def merge_ass(f1: str, f2: str, out: str, index: int):
    with open(f1, encoding = first_encode) as fin:
        fp = list(map(lambda x: x.strip(), fin.readlines()))
    with open(f2, encoding = second_encode) as fin:
        sp = list(map(lambda x: x.strip(), fin.readlines()))

    merge = ''

    for line in sp:
        if not line:
            continue

        if line in skip_part:
            merge = ''
        elif line in merge_part:
            merge = line
        elif line in fp:
            continue
        elif merge:
            index = fp.index(merge)
            for i in range(index, len(fp)):
                if not fp[i]:
                    fp = fp[:i] + [line] + fp[i:]
                    break
            else:
                fp.append(line)
        else:
            print('[Skip] {0} in {1}'.format(line, index))

    with open(out, 'w', encoding = 'utf-8') as fout:
        fout.write('\n'.join(fp))


if __name__ == "__main__":
    first_files = sorted(os.listdir(first_folder))
    second_files = sorted(os.listdir(second_folder))
    output_files = sorted(os.listdir(output_folder))
    for i in range(total):
        index = i + 1
        for (i1, f1) in enumerate(first_files):
            m1 = re.match(first_file.format(index), f1)
            if m1:
                for (i2, f2) in enumerate(second_files):
                    if re.match(second_file.format(index), f2):
                        for (i3, out) in enumerate(output_files):
                            m = re.match(output_file.format(index), out)
                            if m:
                                output_name = '{0}.sc.ass'.format(m.group(1))
                                output_files.pop(i3)
                                break
                        else:
                            output_name = m1.group()

                        assert output_name, "No Output Name"
                        first_files.pop(i1)
                        second_files.pop(i2)

                        merge_ass(
                            os.path.join(first_folder, f1),
                            os.path.join(second_folder, f2),
                            os.path.join(output_folder, output_name), index)
