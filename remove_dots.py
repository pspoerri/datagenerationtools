#!/usr/bin/env python

import os
import re
import subprocess

for f in os.listdir("."):
    b = f.split(".")
    if len(b) > 2:
        c = "".join(b[:-1])+"."+b[-1]
        print "Moving", f, c
        subprocess.call(["mv",f , c])
