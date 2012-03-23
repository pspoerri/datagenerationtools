#!/bin/bash

import os
import re
import argparse
import fileinput
import sys
## Dataformat:

"""
4.98914e-05 1.74668 -19.0253 6.79166 -0.420658 0.597319 -0.37661 
4.98914e-05 1.70056 -19.0035 6.83187 -0.305732 0.958783 -0.149375 
4.98914e-05 1.77301 -19.013 6.80016 -0.226915 0.402915 -0.187241 
4.98914e-05 1.81599 -19.0531 6.82844 -0.456958 0.639559 -0.435593
"""

def filter_line(line, multiplicator=1.0):
    m = re.split("(\S+)", line)
    
    w = float(m[1])*multiplicator
    x = m[3]
    y = m[5]
    z = m[7]
    vx = m[9]
    vy = m[11]
    vz = m[13]

    return "{w} {x} {y} {z} {vx} {vy} {vz}\n".format(x=x, y=y, z=z, w=w, vx=vx, vy=vy, vz=vz)

def filter_file(f, output, modfactor=2):
    counter = 0
    for line in f.readlines():
        if counter%modfactor == 0:
            output.write(filter_line(line, float(modfactor)))
        counter += 1  


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('infile', nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin)
parser.add_argument('outfile', nargs='?', 
        type=argparse.FileType('w'),
        default=sys.stdout)

parser.add_argument('mod',metavar='m', 
      type=int, nargs='?',
      default=2,
      help='The modulo')
args = parser.parse_args()

filter_file(args.infile, args.outfile, args.mod)
