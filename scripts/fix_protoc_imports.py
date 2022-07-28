#!/usr/bin/env python
import fileinput
import re

regex = re.compile(r"^import (.*_pb2) as")

with fileinput.input(inplace=True) as f:
    for line in f:
        if regex.match(line):
            print(regex.sub(r"from . import \g<1> as", line), end="")
        else:
            print(line, end="")
