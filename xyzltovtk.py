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
             #          1                               2                           3                         4
REGEX_WEIGHT = "\s*([-]?\d+[\.]?\d*[e\-\d]*)\s+" \
                  "([-]?\d+[\.]?\d*[e\-\d]*)\s+" \
                  "([-]?\d+[\.]?\d*[e\-\d]*)\s+" \
                  "([-]?\d+[\.]?\d*[e\-\d]*)\s*"

def readBlock(inFile,v,hasweight=False):
    print "ReadingBlock, hasweight=",hasweight
    N = int(inFile.readline().strip())
    A = inFile.readline().strip()
    if A != "Atoms":
        raise RuntimeError("Input file has wrong format")
    if hasweight:
        tmp = inFile.readline()
        m = re.match("t(\d+\.?\d*)",tmp)
        time = m.group(1)

    x = [None]*N
    y = [None]*N
    z = [None]*N
    w = None
    if hasweight:
        w = [None]*N
#    print w
    for i in range(0,N):
        line = inFile.readline().strip()
#        print line
        if hasweight:
            m = re.split(REGEX_WEIGHT,line)
#            print i," ",N
            w[i] = float(m[4])
            x[i] = float(m[1])
            y[i] = float(m[2])
            z[i] = float(m[3])
        else:
            m = re.search(REGEX_NORMAL,line)
            x[i] = m.group(1)
            y[i] = m.group(2)
            z[i] = m.group(3)
    if hasweight:
       return (time,x,y,z,w)
    return (t,x,y,z)
def createOutput(inFile, outFile, hasweight=False):
    v = vtktools.VTK_XML_Serial_Unstructured()
    counter = 0
    while True:
        try:
            if hasweight:
                t,x,y,z,w = readBlock(inFile,v,hasweight)
                v.snapshot("{ofile}_{n}.vtu".format(
                            n=counter,ofile=outFile)
                        ,x,y,z,radii=w)
            else:
                t,x,y,z = readBlock(inFile,v,hasweight)
                v.snapshot("{ofile}_{n}.vtu".format(
                            n=counter,ofile=outFile)
                        ,x,y,z)
            counter += 1
            if counter == 1:
                print x
                print y
                print z
                print w
        except:
            if counter==0:
                raise RuntimeError("File has wrong format")
            break
    v.writePVD("{fname}.pvd".format(fname=outFile))

def main():
    parser = argparse.ArgumentParser(description="""Create a VTK dataset out of the given XYZ-like dataset.""")
    parser.add_argument("--hasweight","-w",
            action='store_const',const=True,default=False,
            help="Special version of the file: x y z w (per row)")

    parser.add_argument('--infile','-i',
            type=argparse.FileType('r'),
            help='The inputfile')
    parser.add_argument('--outfile','-o',
            type=str,
            help='The outputfile')
    args = parser.parse_args()
    w = args.hasweight
    createOutput(args.infile,args.outfile,w)
if __name__ == "__main__":
    main()
