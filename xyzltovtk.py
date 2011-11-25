#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyleft 2011 Pascal Spörri <pascal.spoerri@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" This file will create a VTK file out of a simple xyz-like file format """

import sys
import argparse
import re
import vtktools
REGEX_NORMAL = "\s*1\s+([+-]?\d+\.?\d*)\s+([+-]?\d+\.?\d*)\s+([+-]?\d+\.?\d*)"
REGEX_WEIGHT = "\s*([+-]?\d+\.?\d*)\s+([+-]?\d+\.?\d*)\s+([+-]?\d+\.?\d*)\s+([+-]?\d+\.?\d*)"

def readBlock(inFile,v,hasweight=False):
    N = int(infile.readline())
    A = infile.readline()
    if A != "Atoms":
        raise RuntimeError("Input file has wrong format")
    if hasweight:
        m = re.match("t(\d+\.?\d+)",inputfile)
        time = m.group(1)

    x = []*N
    y = []*N
    z = []*N
    if hasweight:
        w = []*N
    for i in range(0,N):
        line = infile.readline()
        if hasweight:
            m = re.match(line,REGEX_WEIGHT)
            w[i] = m.group(4)
        else:
            m = re.match(line,REGEX_NORMAL)
        x[i] = m.group(1)
        y[i] = m.group(2)
        z[i] = m.group(3)
   if hasweight:
       return (t,x,y,z,w)
   return (t,x,y,z)
def createOutput(inFile, outFile, hasweight=False):
    v = VTK_XML_Serial_Unstructured()
    counter = 0
    while True:
        try:
            if hasweight:
                t,x,y,z,w = readBlock(infile,hasweight)
                v.snapshot("outfile_{n}.vtu".format(
                            n=counter,x,y,z,radii=w))
            else:
                x,y,z,w = readBlock(infile,hasweight)
                v.snapshot("outfile_{n}.vtu".format(
                            n=counter,x,y,z))
            counter += 1
        except:
            if counter==0:
                raise RuntimeError("File has wrong format")
def main():
    parser = argparse.ArgumentParser(description="""Create a VTK dataset out of the given XYZ-like dataset.""")
    parser.add_argument("--hasweight","-w",
            action='store_const',const=True,default=False,
            help="Special version of the file: x y z w (per row)")

   parser.add_argument('infile','i',nargs=1,
            type=argparse.FileType('r'), default=sys.stdout,
            help='The inputfile')
   parser.add_argument('outfile','o',nargs=1,
            type=str,
            help='The outputfile')

   createOutput(args.infile,args.outfile,args.hasweight)
if __name__ == "__main__":
    main()
  
