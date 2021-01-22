#
# The main interface to the city generator.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import Panel, Operator
from .. utils import icons
from ..addon.preferences import cvb_icon


# class panel_frame(Panel):
#     bl_idname = 'cvb.panel'
#     bl_label = 'CVB'
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'CVB'
#
#
#     def draw(self, context):
#         layout = self.layout
#         #preference = get_preferences().property
#         column = layout.column(align=True)
#
#         column.separator()


class CVB_PT_PanelFrame(Panel):
    bl_label = 'Map'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CVB'

    def draw(self, context):
        self.layout.operator("object.new_map",
                             text="New Map",
                             icon_value=cvb_icon(context, "icon-new-map-l"))


class CVB_OT_PanelMapSegment(Operator):
    bl_idname = 'object.new_map'
    bl_label = 'New Map'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()

        return {"FINISHED"}
