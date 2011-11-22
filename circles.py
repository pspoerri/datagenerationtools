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
def plot(x,y,z):
  import matplotlib as mpl
  from mpl_toolkits.mplot3d import Axes3D
  import matplotlib.pyplot as plt
  fig = plt.figure()
  ax = fig.gca(projection='3d')
  ax.scatter(x, y, z, label='parametric curve')
  ax.legend()  
  plt.show()

def printInput(stream,w,lx,ly,lz,lvx,lvy,lvz):
  for i in zip(w,lx,ly,lz,lvx,lvy,lvz):
    stream.write(" {a[0]} {a[1]} {a[2]} {a[3]} {a[4]} {a[5]} {a[6]} \n".format(a=i))

class Circle:
  """ Circle class """
  def __init__(self,r,n,w,angle,speed,skip=False,pointDstrFunction=lambda x:x):
    k = n+1
    theta=linspace(0.0,2.0*pi,n+1)[0:n]
    """ If skip is set, then two values are to avoid having two particles on top of each other """
    if (skip):
      if (n%2==0):
        theta = array(theta[1:n/2].tolist()+theta[n/2+1:].tolist())
      else:
        theta = array(theta[1:])

    x = cos(theta)
    y = sin(theta)
    vx = -y*speed
    vy = x*speed

    x=x*r
    y=y*r
    z=zeros(len(x))
    
    # Process Coordinates
    m=self.rotationMatrixX(angle)
    t = m*mat([x,y,z])
    d = map(pointDstrFunction,zip(t[0,:].tolist()[0], t[1,:].tolist()[0], t[2,:].tolist()[0]))
    self.x, self.y, self.z = zip(*d)
    # Process 
    v = matrix(zeros([size(t,0), size(t,1)]))
    axis = self.xAxisTransform(angle)
    for i in range(len(theta)):
      """ Rotate the speed vector to let it point in a tangential direction """
      vt = cross((axis.H),(t[:,i].H))
      """ Normalize it """
      vt = vt/sqrt(vt[0][0]*vt[0][0]+vt[0][1]*vt[0][1]+vt[0][2]*vt[0][2])*speed
      v[:,i] = transpose(vt)

    self.vx = v[0,:].tolist()[0]
    self.vy = v[1,:].tolist()[0]
    self.vz = v[2,:].tolist()[0]

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

  def xAxisTransform(self,angle):
    """ Rotate around the X-Axis """
    return self.rotationMatrixX(angle)*array([[0],[0],[1]])
  
  def rotationMatrixX(self,angle):
    a = float(angle)
    return mat([[1.0,0.0,0.0],
                [0.0,cos(a),-sin(a)],
                [0.0,sin(a),cos(a)]])
  
  def rotationMatrixZ(self,angle):
    a = float(angle)
    return mat([[cos(a),-sin(a),0.0],
                [sin(a), cos(a),0.0],
                [0.0   , 0.0   ,1.0]])

def generateCylinder(shift,points,radius,weight,speed):
  """ Generate a cylinder """
  x = []
  y = []
  z = []
  vx = []
  vy = []
  vz = []
  
  i = 0;  
  
  for s in shift:
    pointDstrFunction = lambda x:(x[0],x[1],x[2]+s)
    circle = Circle(radius,points,weight,0.0,speed,False,pointDstrFunction)
    x += circle.x
    y += circle.y
    z += circle.z
    vx += circle.vx
    vy += circle.vy
    vz += circle.vz
    i += 1
  
  w = [weight]*len(x)
  return (x,y,z,w,vx,vy,vz)


def generateCircle(angles,points,radius,weight,speed):
  """ Generate circles"""
  x = []
  y = []
  z = []
  vx = []
  vy = []
  vz = []
  
  i = 0;  
  
  for a in angles:
    if (i==0):
      circle = Circle(radius,points,weight,float(a)/180.0*pi,speed,False)
    else:
      circle = Circle(radius,points,weight,float(a)/180.0*pi,speed,True)
    x += circle.x
    y += circle.y
    z += circle.z
    vx += circle.vx
    vy += circle.vy
    vz += circle.vz
    i += 1
  
  w = [weight]*len(x)
  return (x,y,z,w,vx,vy,vz)

def main():
  """ Main Function"""

  parser = argparse.ArgumentParser(description="""Create a dataset with rotated circles around the x-axis.
      The angles denote the angles in centigrades.""")
 
  parser.add_argument('--radius','-r',metavar='R',
      type=float,nargs='?',default=1.0,
      help='The radius of the sphere')
  parser.add_argument('pointscircle',metavar='N', 
      type=int, nargs=1,
      help='The number of particles per circle in the sphere')
  parser.add_argument('--angles','-a',metavar='A', 
      type=float, nargs='*',default=[0.0],
      help='The angle of the different spheres, A in [0,90+]')
  parser.add_argument('--weight','-w',metavar='W', 
      type=float, nargs='?',
      help='The weight of the individual particles',
      default=1.0)
  parser.add_argument('--speed','-s',metavar='S',
      type=float, nargs='?', default=1.0,
      help='The speed of the individual particles')
  
  parser.add_argument('--shift','-S',metavar='SH',
      type=float, nargs='*', default=[0.0])
  
  parser.add_argument('--cylinder','-C',
      action='store_const',const=True,default=False,
      help="""Create a cylinder instead of rotating circles
      Don\'t forget to specify the shift.""")

  parser.add_argument('--display','-d',
      action='store_const',const=True,default=False,
      help='Display the dataset')
  parser.add_argument('--file','-f',nargs='?',
      type=argparse.FileType('wb'), default=sys.stdout,
      help='The outputfile')
  args = parser.parse_args()
  print args

  points=args.pointscircle[0]
  radius=args.radius
  weight=args.weight
  speed=args.speed
  if args.cylinder:
    shift = args.shift
    x,y,z,w,vx,vy,vz = generateCylinder(shift,points,radius,weight,speed)
  else:
    angles=args.angles  
    x,y,z,w,vx,vy,vz = generateCircle(angles,points,radius,weight,speed)

  """ Display the values """
  if (args.display):
    plot(x,y,z)

  """ Dump them to std or file"""
  printInput(args.file,w,x,y,z,vx,vy,vz)
if __name__ == "__main__":
    main()
