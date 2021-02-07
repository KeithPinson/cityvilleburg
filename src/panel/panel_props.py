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

    def city_name_postfix(self, context):
        """<seed> "_" <type> <size> <tile> <variant>"""

        cvb = context.scene.CVB

        postfix = cvb.seed_prop
        postfix = postfix + "-"
        postfix = postfix + "g"
        postfix = postfix + "1x1"
        postfix = postfix + "00000" if cvb.using_tile_id_prop else ""
        postfix = postfix + ""

        return postfix

    def modify_sketch_size(self, context):
        """max map size"""
        return 1000

    def update_sketch_name(self, context):
        """Combo name, seed, variant"""
        return context.scene.CVB.city_field_prop + self.city_name_postfix(context)

    def update_sketch_visibility(self, context):
        """Toggle visibility of sketch layer"""
        return True

    def update_tile_id(self, context):
        """Impacts the file name """
        return 0

    city_field_prop: StringProperty(
        name="",
        default="city",
        description="""City Name""",
        update=None
    )

    seed_prop: IntProperty(
        name="Seed",
        description="""Reproducible random sketch""",
        default=1, min=1, max=32_767)

    sketch_variant_prop: IntProperty(
        name="Variant",
        description="""Custom sketch variant""",
        default=0, min=0, max=999)

    sketch_name_list = []

    sketch_name_prop: EnumProperty(
        name="",
        description="""Names of city sketches""",
        default=None,
        items=sketch_name_list,
        update=update_sketch_name)

    sketch_visible_prop: BoolProperty(
        name="Sketch Visibility",
        description="""Toggle Sketch Visibility""" if len(sketch_name_list) > 0 else "Inactive until New Sketch",
        default=True if len(sketch_name_list) > 0 else False,
        update=update_sketch_visibility)

    sketch_x_prop: IntProperty(
        name="Sketch X",
        description="""Sketch X""",
        min=1,
        max=10_000,
        step=100,
        default=1000,
        update=modify_sketch_size)

    sketch_y_prop: IntProperty(
        name="Sketch Y",
        description="""Sketch Y""",
        min=1,
        max=10_000,
        step=100,
        default=1000,
        update=modify_sketch_size)

    sketch_style_list = [
        ('grid', "Chicago Grid", "A city map modeled after the American grid system"),
        ('skyscrapers', "Cyber Scrapers", "A city map modeled on the if you can't build out, build up"),
        ('western', "Dodge 1880", "A town map with a main street"),
        ('medieval', "Nordingenton", "A layout from years ago when cities formed inside a defensive wall")
    ]

    sketch_style_prop: EnumProperty(
        name="",
        description="""Style hint that affects map sketch""",
        default='grid',
        items=sketch_style_list)

    tile_id_prop: IntProperty(
        name="",
        description="""Unique ID of tile""",
        default=0, min=0, max=32_767,
        update=update_tile_id)

    using_tile_id_prop: BoolProperty(
        name="Multi-file Renders",
        description="""Check to facilitate rendering across multiple files for a single city""",
        default=False)



def cvb_panel_register():
    """Panel properties to register"""
    bpy.utils.register_class(CVB_PanelProperties)
    bpy.types.Scene.CVB = PointerProperty(name='CVB', type=CVB_PanelProperties)


def cvb_panel_unregister():
    """Panel properties for unregistering"""
    if bpy.types.Scene.CVB is not None:
        del bpy.types.Scene.CVB

    bpy.utils.unregister_class(CVB_PanelProperties)
