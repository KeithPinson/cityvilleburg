"""Operators of the N-Key-Panel"""
#
# The operators of the N-Key-Panel.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import Operator


class CVB_OT_NewSketch(Operator):
    # pylint: disable=invalid-name
    """New Sketch Button"""
    bl_idname = 'object.new_sketch_button'
    bl_label = 'New'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = """Add a new City Map Sketch"""

    def execute(self, context):
        # Make a new sketch
        bpy.ops.mesh.primitive_plane_add(size=50)

        return {"FINISHED"}


class CVB_OT_EditCityName(Operator):
    # pylint: disable=invalid-name
    """New Sketch Button"""
    bl_idname = 'entry.city_name_field'
    bl_label = 'City Name'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = """Short, filename compatible, city name"""

    def draw(self, context):
        pass

    def execute(self, context):
        #

        return {"FINISHED"}

    def invoke(self):
        pass

    # @classmethod
    # def poll(cls, context):
    #     ob = context.active_object
    #     return ((ob is not None) and (ob.mode == "OBJECT") and
    #             (ob.type == "MESH") and (context.mode == "OBJECT"))

    # @classmethod
    # def poll(cls, context):
    #     return (context.active_object is not None) and (context.active_object.mode != 'EDIT')



