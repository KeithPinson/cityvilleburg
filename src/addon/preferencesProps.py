#
# Properties of the Add Preferences.
#
# Copyright (c) 2021 Keith Pinson

import bpy
import os
from pathlib import Path
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, StringProperty, EnumProperty


class CVB_AddonPreferenceProps(PropertyGroup):
    bl_idname = __package__.split(".")[0]

    cvb_asset_folder: StringProperty("File Path",
                                     default=str(Path(__file__).parent.parent.joinpath('assets')),
                                     subtype='DIR_PATH')
