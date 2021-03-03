"""Operators of the N-Key-Panel"""
#
# The operators of the N-Key-Panel.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import Operator
from ..utils.collection_utils import collection_add

# save for later => from .citysketchname_props import CVB_CityNameProperties


class CVB_OT_NewSketchButton(Operator):
    # pylint: disable=invalid-name
    """New Sketch Button"""
    bl_idname = 'cvb.new_sketch_button'
    bl_label = 'New'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = """Add a new City Map Sketch"""

    def execute(self, context):
        cvb = context.scene.CVB

        new_sketchname = cvb.city_props.sketch_name_with_next_variant(cvb)

        if not new_sketchname:
            return {"CANCEL"}

        path = "/CVB/{}/Sketch".format(new_sketchname)
        collection_add(path)

        # Make a new sketch
        bpy.ops.mesh.primitive_plane_add(size=50)

        # Refresh the list after we've done everything
        cvb.city_props.refresh_sketch_list(cvb)

        return {"FINISHED"}
