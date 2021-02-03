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
    bl_idname = 'object.new_sketch'
    bl_label = 'New'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = """New city map sketch"""

    def execute(self, context):
        # Make a new sketch
        bpy.ops.mesh.primitive_plane_add(size=50)

        return {"FINISHED"}
