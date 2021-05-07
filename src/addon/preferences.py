"""The Preferences of the Blender Add-on"""
#
# Pertinent city generator preferences and settings
# that apply to the Blender workspace. These settings
# are not meant to be saved in or effect the actual
# blend file itself -- we will do that elsewhere.
#
# Copyright (c) 2021 Keith Pinson

import pathlib
from bpy.types import AddonPreferences
from bpy.props import StringProperty, IntProperty
from ..utils.icons import IconCollection


class CVB_AddonPreferences(AddonPreferences):
    # pylint: disable=invalid-name
    """Class used to display add-on preferences"""
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

    # This seed is hidden and should match the value in the N-panel
    cvb_seed: IntProperty(
        name='Seed',
        description='Last seed value used',
        default=1,
        min=1,
    )

    cvb_asset_folder_prop: \
        StringProperty(name="File Path",
                       default=str(pathlib.Path(__file__).parent.parent.parent.joinpath('assets')),
                       subtype='DIR_PATH')

    cvb_terrain_region_metric: IntProperty(
        name='Metric',
        description="Given a metric m, the region size is (m*2+1)^2 tiles across",
        min=1,
        max=16,
        default=5,
    )

    def draw(self, context):
        # pylint: disable=unused-argument,no-member
        """Override of AddonPreferences draw() method"""
        preferences_column = self.layout.column()

        # Regional Size Entry; using the formula, (m*2+1)^2 tiles across
        region_size = preferences_column.box()

        #       Label
        region_size_label = region_size.row().column().split()
        region_size_label.label(text='Region Size')

        #       Field
        region_size_field = region_size_label
        region_size_field.prop(self, 'cvb_terrain_region_metric', slider=True)

        #       Translation
        region_size_translation = region_size_field
        region_size_translation.column()
        s = (self.cvb_terrain_region_metric*2+1)**2
        region_size_translation.label(text="{} by {} tiles".format(s,s))

        # Assets Folder Entry
        assets_folder = preferences_column.box()

        #       Label
        assets_folder_label = assets_folder.row().column().split(factor=0.2)
        assets_folder_label.label(text='Assets Folder')

        #       Field
        assets_folder_field = assets_folder_label
        assets_folder_field.prop(self, 'cvb_asset_folder_prop', text='')

        #       Instructions
        assets_folder_text = assets_folder.row().column()
        assets_folder_text.row().label(text="       This folder is used internally by the add-on and should only ")
        assets_folder_text.row().label(text="       be changed if disk space is an issue.")


def cvb_addon_register():
    """Lower level support to register"""
    CVB_AddonPreferences.cvb_icons = IconCollection()


def cvb_addon_unregister():
    """Lower level support for unregistering"""
    if CVB_AddonPreferences.cvb_icons is not None:
        del CVB_AddonPreferences.cvb_icons


def cvb_prefs(context):
    """Convenience function to get the add-on preferences object"""
    return context.preferences.addons['cityvilleburg'].preferences


def cvb_icon(context, icon_name):
    """Late binding support of add-on icons"""
    cvb_icons = cvb_prefs(context).cvb_icons

    return cvb_icons.get_icon_id(icon_name)
