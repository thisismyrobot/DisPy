#!/usr/bin/env python3.2

import doctest


files = ("README.txt",)
opts = doctest.REPORT_ONLY_FIRST_FAILURE|doctest.ELLIPSIS

for f in files:
    doctest.testfile(f, optionflags=opts)
