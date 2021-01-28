#
# Pertinent city generator preferences and settings
# that apply to the Blender workspace. These settings
# are not meant to be saved in or effect the actual
# blend file itself -- we will do that elsewhere.
#
# Copyright (c) 2021 Keith Pinson

import bpy
import pathlib
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import PointerProperty, StringProperty, IntProperty
from ..utils.icons import IconCollection
# from ..utils.thumbnails import ThumbnailCollection


class CVB_SketchIdProperties(PropertyGroup):
    bl_idname = "cvb_SketchSeedProperties"

    def auto_increment(self):
        pass

    seed: IntProperty(
        name='Seed',
        description='Seed to reproduce the random sketch',
        default=1,
        min=1)

    variant: IntProperty(
        name='Variant',
        description='Alterations of the provided sketch are marked as a variant',
        default=1,
        min=0)

    name: StringProperty(
        name="SketchID",
        description="Sketch ID",
        default="1.0")


class CVB_AddonPreferences(AddonPreferences):
    bl_idname = __package__.split(".")[0]

    #
    # Serialized properties
    #
    # Registration occurs when Blender is started so we
    # should try to do our own late binding (no reason
    # to tie up resources unnecessarily)
    #
    cvb_icons = None
    cvb_thumbnails = None
    cvb_properties = None
    cvb_seed: PointerProperty(type=CVB_SketchIdProperties)

    cvb_asset_folder: StringProperty("File Path",
                                     default=str(pathlib.Path(__file__).parent.parent.parent.joinpath('assets')),
                                     subtype='DIR_PATH')

    def draw(self, context):
        preferences_column = self.layout.column()

        # Assets Folder Entry
        assets_folder = preferences_column.box().column().split(factor=0.2)

        #       Label
        assets_folder_label = assets_folder
        assets_folder_label.label(text='Assets Folder')

        #       Field
        assets_folder_field = assets_folder
        assets_folder_field.prop(self, 'cvb_asset_folder', text='')


def cvb_addon_register():
    CVB_AddonPreferences.cvb_icons = IconCollection()


def cvb_addon_unregister():
    if CVB_AddonPreferences.cvb_icons is not None:
        del CVB_AddonPreferences.cvb_icons


def cvb_prefs(context):
    return context.preferences.addons['cityvilleburg'].preferences


def cvb_icon(context, icon_name):
    cvb_icons = cvb_prefs(context).cvb_icons

    return cvb_icons.get_icon_id(icon_name)
