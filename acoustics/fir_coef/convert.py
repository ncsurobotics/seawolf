#!/usr/bin/env python

import sys

lines = sys.stdin.read().split("\n")

for line in lines:
    line = line.strip()
    if line == "" or line.startswith("%") or line.startswith("Numerator"):
        continue
    sys.stdout.write("%d\n" % (int(float(line) * 32767),))
