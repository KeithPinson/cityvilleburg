#
# Properties of the N-Panel.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, StringProperty, IntProperty


class CVB_PanelProperties(PropertyGroup):
    """Panel properties saved to the blend file"""

    def modify_max_size(self, context):
        """max map size"""
        pass

    def update_sketch_name(self, context):
        """Combo name, seed, variant"""
        pass

    seed: IntProperty(
        name="Seed",
        description="Reproducible random sketch",
        default=1, min=1, max=32_767)

    sketch_variant: IntProperty(
        name="Variant",
        description="Custom sketch variant",
        default=0, min=0, max=999)

    sketch_name: StringProperty(
        name="",
        description="Sketch",
        default="City_1",
        update=update_sketch_name)

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


def cvb_panel_register():
    """Panel properties to register"""
    bpy.utils.register_class(CVB_PanelProperties)
    bpy.types.Scene.CVB = PointerProperty(name='CVB', type=CVB_PanelProperties)


def cvb_panel_unregister():
    """Panel properties for unregistering"""
    if bpy.types.Scene.CVB is not None:
        del bpy.types.Scene.CVB

    bpy.utils.unregister_class(CVB_PanelProperties)
