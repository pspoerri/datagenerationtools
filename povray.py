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
#include "shapes.inc"
#include "colors.inc"
#include "textures.inc"
#include "stones.inc"
#include "stars.inc"

#declare r = 100;
#declare w = 0;
"""

OBJECT = """
union {{
    sphere {{
        <{x}, {y}, {z}>, {w}
        texture {{
            pigment {{color rgb <1, 1, 0.6>}}
            finish {{ambient 1 diffuse 1}}
        }}
    }}
    light_source {{
        <{x}, {y}, {z}>
        color White
   }}
}}
"""

END = """
camera {
	location <0, w, (-1.6 + 3.2 * clock)*r>
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
