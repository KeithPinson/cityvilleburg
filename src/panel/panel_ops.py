"""Operators of the N-Key-Panel"""
#
# The operators of the N-Key-Panel.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import Operator
from ..utils import sketchname_parse
from ..utils.collection_utils import collection_add


class CVB_OT_NewSketchButton(Operator):
    # pylint: disable=invalid-name
    """New Sketch Button"""
    bl_idname = 'cvb.new_sketch_button'
    bl_label = 'New'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = """Add a new City Map Sketch"""

    def execute(self, context):
        # Make a new sketch
        bpy.ops.mesh.primitive_plane_add(size=50)

        cvb = context.scene.CVB

        plain_sketchname = cvb.city_props.make_sketch_from_props(cvb)

        name = plain_sketchname.sketch_name

        if name:
            path = "/CVB/{}/Sketch".format(name)

            collection_add(path)

        return {"FINISHED"}
