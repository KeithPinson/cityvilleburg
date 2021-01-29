#
# Properties of the N-Panel.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, StringProperty, EnumProperty


def modify_max_size(self, context):
    pass

class CVB_PanelProperties(PropertyGroup):

    seed: StringProperty(name="seed")

    max_width: StringProperty(
        name="",
        description="Max Width",
        default="1000",
        update=modify_max_size)

    max_height: StringProperty(
        name="",
        description="Max Height",
        default="1000",
        update=modify_max_size)

