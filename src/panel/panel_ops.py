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
        # Make a new sketch
        bpy.ops.mesh.primitive_plane_add(size=50)

        cvb = context.scene.CVB

        plain_sketchname = cvb.city_props.make_sketch_from_props(cvb)

        new_variant = cvb.city_props.sketch_names_get_next_variant(
            city=plain_sketchname.city,
            seed=plain_sketchname.seed,
            style=plain_sketchname.style,
            x=plain_sketchname.x,
            y=plain_sketchname.y,
            tile=plain_sketchname.tile
        ) if plain_sketchname else 0

        plain_sketchname.update_sketchname(variant=new_variant)

        name = plain_sketchname.sketch_name

        if name:
            path = "/CVB/{}/Sketch".format(name)

            collection_add(path)

        return {"FINISHED"}
