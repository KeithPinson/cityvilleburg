#
# Pertinent city generator preferences and settings
# that apply to the Blender workspace. None of these
# settings are saved in or effect the actual blend file
# itself.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import StringProperty
from .preferencesProps import CVB_AddonPreferenceProps


class CVB_AddonPreferences(AddonPreferences):
    bl_idname = __package__.split(".")[0]

    cvb_icons = None
    cvb_thumbnails = None

    def draw(self, context):
        column = self.layout.column()

        self.draw_assets_path(column)

    def draw_assets_path(self, layout):

        box = layout.box()

        row = box.row()
        row.label(text='Assets Folder')

        box = row.box()
        column = box.column()

        row = column.row(align=True)
        row.prop(self, 'assets_folder', text='Location')


def cvb_icon(context, icon_name):
    prefs = context.preferences.addons['cityvilleburg'].preferences
    cvb_icons = prefs.cvb_icons

    return cvb_icons.get_icon_id(icon_name)
