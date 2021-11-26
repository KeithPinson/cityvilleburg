"""Terrain Editor"""
#
# The Terrain Editor is a heads-up style display
# in the 3D Viewport. It is only one object; a plane,
# no ability to add anything but it can be modified.
# With special tools mountain ridges and rivers can
# be drawn and modified. When changes are made in
# the Terrain Editor they are reflected in the
# terrain mesh of the 3D Viewport.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import Panel, Operator, WorkSpaceTool
from ..utils.collection_utils import collection_add
from ..utils.object_utils import\
    object_add, object_get_or_add_empty, object_parent_all, object_make_active
from . import terrain_object


def terrain_outliner(context):
    """Check to see if the terrain region map exists and add it if it does not."""

    #
    # Example Outliner:
    #
    # CVB [collection]
    #   City1_g1x1.001 [collection]
    #     .
    #     .
    #     .
    #   Terrain [collection]        <-- This
    #      Region_Map               <--   and this is what we need to check for

    cvb = context.scene.CVB

    size = 10
    subdivision_per_meter = 8

    # Collection
    sketch_path = "/CVB/Region Terrain"
    collection_add(sketch_path)

    # Sketch Object
    map_name = "Region Terrain Map"
    object_add(sketch_path, map_name, terrain_object.RegionTerrainMap(map_name, size, size).obj)

    # Transform Empty
    sketch_name = "Region Terrain Transform"
    object_add(sketch_path, sketch_name, None)


def build_terrain_edit_rig(context):

    terrain_outliner(context)

    cvb = context.scene.CVB

    size = (cvb.sketch_xy_linked_prop, cvb.sketch_xy_linked_prop) if \
        cvb.using_tile_id_prop else (cvb.sketch_x_prop, cvb.sketch_y_prop)

    sketchname = cvb.city_props.get_sketch_name()
    print(sketchname)

    print("build_terrain_edit_rig()")


def teardown_terrain_edit_rig(context):

    print("teardown_terrain_edit_rig()")


class CVB_OT_TerrainEdit(Operator):
    # pylint: disable=invalid-name
    """Terrain Editor"""
    bl_idname = 'cvb.terrain_edit'
    bl_label = 'Terrain Edit'
    bl_options = {"INTERNAL"}
    bl_description = """Edit the Terrain"""

    def execute(self, context):
        """Display the terrain editor, create terrain map if needed"""

        cvb = context.scene.CVB


class CVB_PT_Terrain(Panel):
    bl_idname = "CVB_PT_Terrain"
    # bl_parent_id = "CVB_Main"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    bl_category = "CVB"
    bl_context = 'objectmode'
    bl_label = "Terrain"
    # bl_options = {'HIDE_HEADER'}

    bl_order = 33

    @classmethod
    def poll(cls, context):
        cvb = context.scene.CVB

        if cvb.visible_terrain_editor_prop:
            return True
        else:
            return False

    def draw(self, context):
        cvb = context.scene.CVB

        # props = tool.operator_properties("cvb.terrain_edit")
        # preferences = bpy.context.preferences.addons[__package__].preferences

        terrain_pens = self.layout.box()

        terrain_pens.prop(cvb.terrain_props, "terrain_pen_prop", text="Terrain Pen",
                          expand=True, emboss=True)
        terrain_pens.scale_y = 1.3
        terrain_pens.alignment = 'CENTER'

        terrain_buttons_row = terrain_pens.row(align=True)

        terrain_buttons_row.operator("cvb.terrain_help_button",
                                     text="?",
                                     depress=cvb.terrain_props.terrain_help_prop)

        terrain_buttons_row.operator("cvb.terrain_clear_button",
                                     text="clear",
                                     depress=cvb.terrain_props.terrain_clear_prop)

        terrain_buttons_row.operator("cvb.terrain_autogen_button",
                                     text="autogen",
                                     depress=cvb.terrain_props.terrain_autogen_prop)

class CVB_OT_TerrainHelpButton(Operator):
    # pylint: disable=invalid-name
    """Terrain Help Button"""
    bl_idname = 'cvb.terrain_help_button'
    bl_label = 'Terrain Help'
    bl_options = {"INTERNAL"}
    bl_description = """Show Terrain Help Cheat Sheet"""

    def execute(self, context):

        cvb = context.scene.CVB

        return {"FINISHED"}

class CVB_OT_TerrainClearButton(Operator):
    # pylint: disable=invalid-name
    """Terrain Clear Button"""
    bl_idname = 'cvb.terrain_clear_button'
    bl_label = 'Terrain Clear'
    bl_options = {"INTERNAL"}
    bl_description = """Clear all terrain"""

    def execute(self, context):

        cvb = context.scene.CVB

        return {"FINISHED"}

class CVB_OT_TerrainAutogenButton(Operator):
    # pylint: disable=invalid-name
    """Terrain Autogen Button"""
    bl_idname = 'cvb.terrain_autogen_button'
    bl_label = 'Terrain Autogen'
    bl_options = {"INTERNAL"}
    bl_description = """Clear all terrain and auto-generate new"""

    def execute(self, context):

        cvb = context.scene.CVB

        return {"FINISHED"}

