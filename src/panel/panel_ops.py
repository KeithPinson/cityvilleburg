"""Operators of the N-Key-Panel"""
#
# The operators of the N-Key-Panel.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import Operator
from ..utils.collection_utils import collection_add
from ..utils.object_utils import object_add, object_get_or_add_empty, object_parent_all
from ..citySketch import sketch_object


class CVB_OT_NewSketchButton(Operator):
    # pylint: disable=invalid-name
    """New Sketch Button"""
    bl_idname = 'cvb.new_sketch_button'
    bl_label = 'New'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = """Add a new City Map Sketch"""

    def execute(self, context):
        """Operator to add a New Sketch behaves like a button when only execute() is defined"""

        #
        # Example With Empties
        #
        # The one master empty is used to control the transforms of the sketch,
        # map
        # CVB [collection]
        #   City1_g1x1.001 [collection]
        #     City1_g1x1.001 Transform [empty of cube shape] Hide in viewport   (parent)
        #       Sketch ~ City1_g1x1.001 [collection]
        #         Sketch Plane ~ City1_g1x1.001	[plane mesh]					(child)

        cvb = context.scene.CVB

        size = (cvb.sketch_xy_linked_prop, cvb.sketch_xy_linked_prop) if \
            cvb.using_tile_id_prop else (cvb.sketch_x_prop, cvb.sketch_y_prop)

        new_sketchname = cvb.city_props.sketch_name_with_next_variant(cvb)

        if not new_sketchname:
            return {"CANCEL"}

        # Collection
        sketch_path = "/CVB/{0}/Sketch ~ {0}".format(new_sketchname)
        collection_add(sketch_path)

        # Sketch Object
        sketch_name = "Sketch"
        object_add(sketch_path, sketch_name, sketch_object.CitySketch(sketch_name, size[0], size[1]).obj)

        # Transform Empty
        cvb_path = "/CVB/{0}".format(new_sketchname)
        empty_name = "{0} Transform".format(new_sketchname)
        empty = object_get_or_add_empty(cvb_path, empty_name, radius=0.12, display_type='CUBE')

        if empty:
            object_parent_all(empty, sketch_path)

        # Refresh the list after we've done everything
        cvb.city_props.refresh_sketch_list(cvb)

        cvb.city_props.update_city_name_prop(context)

        return {"FINISHED"}
