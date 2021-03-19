"""City Sketch Blender Object"""
#
# Conceptually a sketch of a map is a simple drawing.
# To support a map drawing tool we use Grease Pencil
# constrained to an x-y plane.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from mathutils import Vector, Matrix, geometry


class CitySketch:

    sketch_name = ""
    x_length = 0
    y_length = 0
    obj = None

    verts = []
    edges = []
    faces = []

    def __init__(
            self,
            sketch_name,
            x_length,
            y_length):

        self.sketch_name = sketch_name
        self.x_length = x_length
        self.y_length = y_length
        self.obj = bpy.data.meshes.new(sketch_name)

        (a, b, c) = (x_length*.5, y_length*.5, 0)

        self.verts = [Vector((a, b, c)), Vector((-a, b, c)),
                      Vector((-a, -b, c)), Vector((a, -b, c))]

        self.edges = [(0, 1), (1, 2),
                      (2, 3), (3, 0)]

        self.faces = [(0, 1, 2, 3)]

        self.obj.from_pydata(self.verts, self.edges, self.faces)
