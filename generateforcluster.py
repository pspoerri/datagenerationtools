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

import circles
from numpy import arange
#numberOfPoints = map(lambda x:2**x,range(10,13))
numberOfPoints = [2**13]
#radius = map(lambda x:2**x,range(4,8))
radius = [2**8]
speed  = map(lambda x:2**x,arange(0,5,0.2))
angles = [[0,10,20,30,40,50,60,70,80,90]]
weight = 1.0

stime = 0.0
etime = 2.0
dt = 0.1
theta = 0.5
dumpperiod = 1


def filename(prefix,number,radius,speed,special):
  return prefix+"_n"+str(number)+"_r"+str(radius)+"_s"+str(speed)+"_"+special



prefix = "circles"
for np in numberOfPoints:
  for r in radius:
    for s in speed:
      for a in angles:
        x,y,z,w,vx,vy,vz = circles.generateCircle(a,np,r,weight,s)
        fname = filename("circles",np,r,s,"a"+("_".join(map(lambda x: str(x),a))))
        print fname
        f = open(fname,'w')
        circles.printInput(f,w,x,y,z,vx,vy,vz) 
