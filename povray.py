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

HEADER = """
#include "colors.inc"
#include "shapes.inc"
#include "textures.inc"
#include "stones.inc"
#include "stars.inc"

#declare r = 0;
#declare w = 100;
#declare pos = <0,0,0>;
#declare weight = 1.0;

#declare star = sphere{ 
      <0,0,0>, 0.99 hollow on          
      interior{
           media{
              absorption rgb<0.0, 0.0, 0.0>
              scattering { 5 rgb<1.0, 1.0, 1.0> eccentricity +0.1 }
              density { spherical 
                  color_map{
                    [0.00 rgb <0,0,0>]
                    [0.05 rgb <0.1,0.1,0.5>]
                    [0.2 rgb <0.2,0.2,0.6>]
                    [0.5 rgb <0.5,0.5,0.8>]
                    [0.7 rgb <0.6,0.6,0.85>]
                    [0.9 rgb <0.7,0.7,0.95>]
                    [1.0 rgb <1.0,1.0,1.0>]
      } } } }
      texture {
         pigment {color White 1.00 filter 1.00}
         finish {
            reflection 0.0 
      } }
}

"""

OBJECT = """
#declare pos = <{x}, {y}, {z}>;
#declare weight = {w};
star
"""
# OBJECT = """
# union {{
#     sphere {{
#         <{x}, {y}, {z}>, {w}
#         texture {{
#             pigment {{color rgb <1, 1, 0.6>}}
#             finish {{ambient 1 diffuse 1}}
#         }}
#     }}
#     light_source {{
#         <{x}, {y}, {z}>
#         color White
#    }}
# }}
# """

END = """
camera {
/*	location <0, w, (-1.6 + 3.2 * clock)*r> */
    location <0, w, 0>
	right 16/9*x
}
"""

class PovRayWriter:

    def __init__(self,prefix="topov_"):
        self.prefix = prefix
        self.n = 0

    def get_filename(self):
        return self.prefix+str(self.n)+".pov"

    def write_snapshot(self, x, y, z, w=[]):
        f = open(self.get_filename(),'wb')
        if w==[]:
            w = [1]*len(x)
        f.write(HEADER)
        for tx, ty, tz, tw in zip(x,y,z,w):
            f.write(OBJECT.format(x=tx, y=ty, z=tz, w=tw))

        self.n += 1
        f.write(END)
        f.close()
