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


class CVB_OT_TerrainEdit(Operator):
    # pylint: disable=invalid-name
    """Terrain Editor"""
    bl_idname = 'cvb.terrain_edit'
    bl_label = 'Terrain Edit'
    bl_options = {"INTERNAL"}
    bl_description = """Edit the Terrain"""

    def execute(self, context):

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
        layout = self.layout

        # props = tool.operator_properties("cvb.terrain_edit")
        # preferences = bpy.context.preferences.addons[__package__].preferences

        col = layout.column()
        col.label(text="River")



