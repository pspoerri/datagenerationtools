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

import sys
import argparse
from numpy import *
from circles import plot, Circle, printInput

def main():
  """ Main Function"""

  parser = argparse.ArgumentParser(description='Create a dataset with n circles creating a cylinder around the z-axis')
 
  parser.add_argument('--radius','-r',metavar='R',
      type=float,nargs='?',default=1.0,
      help='The radius of the sphere')
  parser.add_argument('--pointscircle','-n',metavar='N', 
      type=int, nargs=1,
      help='The number of particles per circle in the sphere')

  parser.add_argument('--weight','-w',metavar='W', 
      type=float, nargs='?',
      help='The weight of the individual particles',
      default=1.0)
  parser.add_argument('--speed','-s',metavar='S',
      type=float, nargs='?', default=1.0,
      help='The speed of the individual particles')
  parser.add_argument('--display','-d',
      action='store_const',const=True,default=False,
      help='Display the dataset')
  parser.add_argument('--file','-f',nargs='?',
      type=argparse.FileType('wb'), default=sys.stdout,
      help='The outputfile')
  args = parser.parse_args()
  print args

  angles=args.angles
  points=args.pointscircle[0]
  radius=args.radius
  weight=args.weight
  speed=args.speed
  x,y,z,w,vx,vy,vz = generateDataset(angles,points,radius,weight,speed)
  """ Display the values """
  if (args.display):
    plot(x,y,z)

  """ Dump them to std or file"""
  printInput(args.file,w,x,y,z,vx,vy,vz)
if __name__ == "__main__":
    main()
