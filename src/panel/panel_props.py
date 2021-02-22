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
from .citysketchname_props import CVB_CityNameProperties, is_sketch_list_empty


class CVB_PanelProperties(PropertyGroup):
    # pylint: disable=invalid-name
    """Panel properties saved to the blend file"""

    def modify_sketch_size(self, context):
        """max map size"""
        return 1000

    def update_sketch_visibility(self, context):
        """Toggle visibility of sketch layer"""
        return True

    def update_tile_id(self, context):
        """Impacts the file name """
        return 0

    # sketch_names_prop: Pointer

    city_props: PointerProperty(type=CVB_CityNameProperties)

    seed_prop: IntProperty(
        name="Seed",
        description="""Reproducible random sketch id""",
        default=1, min=1, max=32_767)

    sketch_variant_prop: IntProperty(
        name="Variant",
        description="""Custom sketch variant""",
        default=0, min=0, max=999)

    sketch_visible_prop: BoolProperty(
        name="Sketch Visibility",
        description="""Toggle Sketch Visibility""" if not is_sketch_list_empty() else "Inactive until New Sketch",
        default=True if not is_sketch_list_empty() else False,
        update=update_sketch_visibility)

    sketch_xy_linked_prop: IntProperty(
        name="Sketch XY",
        description="""Sketch XY size""",
        min=1,
        max=10_000,
        step=100,
        default=1000,
        update=modify_sketch_size)

    sketch_x_prop: IntProperty(
        name="Sketch X",
        description="""Sketch X size""",
        min=1,
        max=10_000,
        step=100,
        default=1000,
        update=modify_sketch_size)

    sketch_y_prop: IntProperty(
        name="Sketch Y",
        description="""Sketch Y size""",
        min=1,
        max=10_000,
        step=100,
        default=1000,
        update=modify_sketch_size)

    # First letter of first element must be unique (it is used in city filename)
    sketch_style_list = [
        ('grid', "Grid Style City", "A city map modeled after the American grid system"),
        ('medieval', "Medieval City Style", "A layout from years ago when cities formed inside a defensive wall"),
        ('skyscrapers', "Skyscraper City Style", "A city map modeled on the if you can't build out, build up"),
        ('western', "Western City Style", "A town built along a thoroughfare; water, rail, or road")
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

    tile_position_prop: StringProperty(
        name="",
        description="""Matrix position from central tile""",
        default="+000 +003")

    using_tile_id_prop: BoolProperty(
        name="Multi-file Renders",
        description="""Facilitates rendering across multiple files for one   single city""",
        default=False)


def cvb_panel_register():
    """Panel properties to register"""
    bpy.utils.register_class(CVB_CityNameProperties)
    bpy.utils.register_class(CVB_PanelProperties)
    bpy.types.Scene.CVB = PointerProperty(name='CVB', type=CVB_PanelProperties)


def cvb_panel_unregister():
    """Panel properties for unregistering"""
    if bpy.types.Scene.CVB is not None:
        del bpy.types.Scene.CVB

    bpy.utils.unregister_class(CVB_PanelProperties)
    bpy.utils.unregister_class(CVB_CityNameProperties)
