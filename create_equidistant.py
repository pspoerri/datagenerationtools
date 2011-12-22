#!/usr/bin/env python

import subprocess

for i in range(2,110):
  subprocess.call(["Create_equidistant", "-f equidistant_{i}.in".format(i=i), str(i)])
