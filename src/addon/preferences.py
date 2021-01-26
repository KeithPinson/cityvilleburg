#
# Pertinent city generator preferences and settings
# that apply to the Blender workspace. None of these
# settings are saved in or effect the actual blend file
# itself.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import PointerProperty, StringProperty
from .preferencesProps import CVB_AddonPreferenceProps
from ..utils.icons import IconCollection
# from ..utils.thumbnails import ThumbnailCollection


class CVB_AddonPreferences(AddonPreferences):
    bl_idname = __package__.split(".")[0]

    cvb_icons = None
    cvb_thumbnails = None
    cvb_properties = None

    def draw(self, context):
        column = self.layout.column()

        box = column.box()

        row = box.row()
        row.label(text='Assets Folder')

        # box = row.box()
        # column = box.column()
        #
        # row = column.row(align=True)
        # row.prop(cvb_prefs(context).cvb_properties, 'cvb_asset_folder', text='Location')


def cvb_addon_register():
    CVB_AddonPreferences.cvb_icons = IconCollection()

    CVB_AddonPreferences.cvb_properties = PointerProperty(type=CVB_AddonPreferenceProps)


def cvb_addon_unregister():
    if CVB_AddonPreferences.cvb_icons is not None:
        del CVB_AddonPreferences.cvb_icons


def cvb_prefs(context):
    return context.preferences.addons['cityvilleburg'].preferences


def cvb_icon(context, icon_name):
    cvb_icons = cvb_prefs(context).cvb_icons

    return cvb_icons.get_icon_id(icon_name)
