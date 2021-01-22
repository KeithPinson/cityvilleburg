#
# Pertinent city generator preferences and settings
# that apply to the Blender workspace. None of these
# settings are saved or effect the actual blend file
# itself.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import AddonPreferences


blidname = __package__.split(".")[0]


class CVB_AddonPreferences(AddonPreferences):
    bl_idname = blidname

    add_bevel: bpy.props.EnumProperty(
        items=[
            ('bevel', 'Add bevel', '', '', 0),
            ('no_bevel', 'No bevel', '', '', 1)
        ],
        default='no_bevel'
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text='Add bevel modifier:')
        row = layout.row()
        row.prop(self, 'add_bevel', expand=True)
