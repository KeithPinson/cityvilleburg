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
from bpy.props import (
    PointerProperty, StringProperty, IntProperty, BoolProperty, EnumProperty)


class CVB_PanelProperties(PropertyGroup):
    # pylint: disable=invalid-name
    """Panel properties saved to the blend file"""

    def modify_sketch_size(self, context):
        """max map size"""
        return 1000

    def update_sketch_name(self, context):
        """Combo name, seed, variant"""
        return "City_1"

    def update_sketch_visibility(self, context):
        """Toggle visibility of sketch layer"""
        return True

    seed: IntProperty(
        name="Seed",
        description="Reproducible random sketch",
        default=1, min=1, max=32_767)

    sketch_variant: IntProperty(
        name="Variant",
        description="Custom sketch variant",
        default=0, min=0, max=999)

    sketch_name: StringProperty(
        name="Sketch Name",
        description="Sketch",
        default="+  New",
        update=update_sketch_name)

    sketch_visible: BoolProperty(
        name="Sketch Visibility",
        description="Sketch Visible?",
        default=True,
        update=update_sketch_visibility)

    sketch_x: IntProperty(
        name="Sketch X",
        description="Sketch X",
        min=1,
        max=10_000,
        step=100,
        default=1000,
        update=modify_sketch_size)

    sketch_y: IntProperty(
        name="Sketch Y",
        description="Sketch Y",
        min=1,
        max=10_000,
        step=100,
        default=1000,
        update=modify_sketch_size)

    city_style_list = [
        ('grid', "Chicago Grid", "A city map modeled after the American grid system"),
        ('skyscrapers', "Cyber Scrapers", "A city map modeled on the if you can't build out, build up"),
        ('western', "Dodge 1880", "A town map with a main street"),
        ('medieval', "Nordingenton", "A layout from years ago when cities formed inside a defensive wall")
    ]

    sketch_map_style: EnumProperty(
        name="",
        description="Style hint that affects map sketch",
        default='grid',
        items=city_style_list)


def cvb_panel_register():
    """Panel properties to register"""
    bpy.utils.register_class(CVB_PanelProperties)
    bpy.types.Scene.CVB = PointerProperty(name='CVB', type=CVB_PanelProperties)


def cvb_panel_unregister():
    """Panel properties for unregistering"""
    if bpy.types.Scene.CVB is not None:
        del bpy.types.Scene.CVB

    bpy.utils.unregister_class(CVB_PanelProperties)
