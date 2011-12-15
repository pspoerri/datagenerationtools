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
import numpy
def plot(x, y, z):
  import matplotlib as mpl
  from mpl_toolkits.mplot3d import Axes3D
  import matplotlib.pyplot as plt
  fig = plt.figure()
  ax = fig.gca(projection='3d')
  ax.scatter(x, y, z, label='parametric curve')
  ax.legend()  
  plt.show()

def printInput(stream, w, lx, ly, lz, lvx, lvy, lvz):
  for i in zip(w,lx,ly,lz,lvx,lvy,lvz):
    stream.write(" {a[0]} {a[1]} {a[2]} {a[3]} {a[4]} {a[5]} {a[6]} \n".format(a=i))

class Rectangle:
  """ Circle class """
  def __init__(self, n, weight=1.0, left=0.0, right=1.0, 
          pointDstrFunction=lambda x:x,
          speed_function=lambda x:x):
    x = linspace(left, right, n)
    y = x;
    z = x;

    self.x = []
    self.y = []
    self.z = []

    self.vx = []
    self.vy = []
    self.vz = []
    for tx in x:
        for ty in y:
            for tz in z:
                mx, my, mz = pointDstrFunction((tx, ty, tz))
                vx, vy, vz = speed_function((mx,my,mz))
                self.x.append(mx)
                self.y.append(my)
                self.z.append(mz)
    
                self.vx.append(vx)
                self.vy.append(vy)
                self.vz.append(vz)
    self.w = [weight]*len(self.x)

  def plot(self,x,y,z):
    """ Plot the circle """
    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(x, y, z, label='parametric curve')
    ax.legend()
    plt.show()

def generate_equidistant_dataset(n, weight=1.0):
    rect = Rectangle(n, weight)
    return (rect.x, rect.y, rect.z, rect.w, rect.vx, rect.vy, rect.vz)

def main():
  """ Main Function"""

  
  parser = argparse.ArgumentParser(description="""Create a dataset""")
 
  """ Arguments needed for all commands """
  parser.add_argument('number', metavar='N',
      type=int, nargs=1, 
      help='The number of elements per side')

  parser.add_argument('--display', '-d',
      action='store_const',const=True,default=False,
      help='Display the dataset')
  parser.add_argument('--file','-f',nargs='?',
      type=argparse.FileType('wb'), default=sys.stdout,
      help='The outputfile')

  parser.add_argument('--weight','-w',metavar='W', 
      type=float, nargs='?',
      help='The weight of the individual particles',
      default=1.0)

  
  args = parser.parse_args()

  elements = args.number[0]
  weight=args.weight
 
  print elements
  x,y,z,w,vx,vy,vz = generate_equidistant_dataset(elements, weight)
  """ Display the values """
  if (args.display):
    plot(x,y,z)

  """ Dump them to std or file"""
  printInput(args.file,w,x,y,z,vx,vy,vz)
if __name__ == "__main__":
    main()
