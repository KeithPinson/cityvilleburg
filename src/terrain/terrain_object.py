"""Region Terrain Blender Object"""
#
# The region terrain Map is like a raised relief map
# but modeled in 3D inside Blender. It does not use
# topographical elevations but instead uses concepts
# like ridge lines and river lines that can be
# pulled up or pushed down to make the elevations.
# It is not meant to be precise but quick with a
# look of realism.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from mathutils import Vector, Matrix, geometry


class RegionTerrainMap:

    map_name = ""
    x_length = 0
    y_length = 0
    obj = None

    verts = []
    edges = []
    faces = []

    def __init__(
            self,
            map_name,
            x_length,
            y_length):

        self.map_name = map_name
        self.x_length = x_length
        self.y_length = y_length
        self.obj = bpy.data.meshes.new(map_name)

        (a, b, c) = (x_length*.5, y_length*.5, 0)

        self.verts = [Vector((a, b, c)), Vector((-a, b, c)),
                      Vector((-a, -b, c)), Vector((a, -b, c))]

        self.edges = [(0, 1), (1, 2),
                      (2, 3), (3, 0)]

        self.faces = [(0, 1, 2, 3)]

        self.obj.from_pydata(self.verts, self.edges, self.faces)
