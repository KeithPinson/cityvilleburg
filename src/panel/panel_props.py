"""Properties of the N-Key-Panel"""
#
# The properties of the N-Key-Panel. We want to store these
# in the Blend file and to facilitate this we need to
# put the properties in a class derived from the
# PropertyGroup.
#
# It is not obvious but if we attach the properties to
# the bpy.types.Scene object then Blender will keep the
# the properties in the bpy.context.scene object and
# the properties will be saved in the file.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import PropertyGroup
from bpy.props import PointerProperty, StringProperty, IntProperty


class CVB_PanelProperties(PropertyGroup):
    # pylint: disable=invalid-name
    """Panel properties saved to the blend file"""

    def modify_max_size(self, context):
        """max map size"""
        return 1000

    def update_sketch_name(self, context):
        """Combo name, seed, variant"""
        return "City_1"

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
