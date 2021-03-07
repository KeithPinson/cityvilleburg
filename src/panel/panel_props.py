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
# pylint: disable=relative-beyond-top-level
from .citysketchname_props import CVB_CityNameProperties, is_sketch_list_empty


class CVB_PanelProperties(PropertyGroup):
    # pylint: disable=invalid-name, line-too-long
    """Panel properties saved to the blend file"""

    def decode_style(self, coded_style):

        styles_found = \
            [s[0] for s in self.sketch_style_list if s[0].startswith(coded_style)]

        if styles_found:
            style = styles_found[0]
        else:
            style = self.sketch_style_list[0][0]

        return style

    def encode_style(self, style):
        result = style[0] if style else self.sketch_style_list[0][0][0]

        return result

    def update_seed(self, context):
        """Seed update"""
        cvb = context.scene.CVB
        cvb.city_props.refresh_sketch_list(cvb)

    def update_sketch_style(self, context):
        """Sketch style update"""
        cvb = context.scene.CVB
        cvb.city_props.refresh_sketch_list(cvb)

    def update_sketch_visibility(self, context):
        """Toggle visibility of sketch layer"""

    def update_sketch_xy_linked(self, context):
        """Sketch xy linked update"""
        cvb = context.scene.CVB
        cvb.city_props.refresh_sketch_list(cvb)

    def update_sketch_x(self, context):
        """Sketch x update"""
        cvb = context.scene.CVB
        cvb.city_props.refresh_sketch_list(cvb)

    def update_sketch_y(self, context):
        """Sketch y update"""
        cvb = context.scene.CVB
        cvb.city_props.refresh_sketch_list(cvb)

    def update_tile_id(self, context):
        """Impacts the file name """
        cvb = context.scene.CVB
        cvb.city_props.refresh_sketch_list(cvb)

    city_props: PointerProperty(type=CVB_CityNameProperties)

    seed_prop: IntProperty(
        name="Seed",
        description="""Reproducible random sketch id""",
        default=1, min=1, max=32_767,
        update=update_seed)

    # First letter of first element must be unique (it is used in city filename)
    sketch_style_list = [
        ('grid', "Grid Plan City", "A city map modeled after the planned grid system"),
        ('medieval', "Medieval City Style", "A layout from years ago when cities formed inside a defensive wall"),
        ('skyscrapers', "Skyscraper City Style", "A city map modeled on the if you can't build out, build up"),
        ('western', "Western City Style", "A town built along a thoroughfare; water, rail, or road")
    ]

    sketch_style_prop: EnumProperty(
        name="",
        description="""Style hint that affects map sketch""",
        default='grid',
        items=sketch_style_list,
        update=update_sketch_style)

    sketch_visible_prop: BoolProperty(
        name="Sketch Visibility",
        description="""Toggle Sketch Visibility""" if
        not is_sketch_list_empty() else "Inactive until New Sketch",
        default=not is_sketch_list_empty(),
        update=update_sketch_visibility)

    sketch_xy_linked_prop: IntProperty(
        name="Sketch XY",
        description="""Sketch XY size""",
        min=1,
        max=10_000,
        step=100,
        default=1000,
        update=update_sketch_xy_linked)

    sketch_x_prop: IntProperty(
        name="Sketch X",
        description="""Sketch X size""",
        min=1,
        max=10_000,
        step=100,
        default=1000,
        update=update_sketch_x)

    sketch_y_prop: IntProperty(
        name="Sketch Y",
        description="""Sketch Y size""",
        min=1,
        max=10_000,
        step=100,
        default=1000,
        update=update_sketch_y)

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
        description="""Facilitates rendering across multiple files for one single city""",
        default=False)

    # Internal number, typically incremented when new sketch is added
    variant_prop: IntProperty(
        name="Variant",
        description="""Sketch variant""",
        default=0, min=0, max=999)


def cvb_panel_register():
    """Panel properties to register"""
    bpy.utils.register_class(CVB_CityNameProperties)
    bpy.utils.register_class(CVB_PanelProperties)
    # pylint: disable=assignment-from-no-return
    bpy.types.Scene.CVB = PointerProperty(name='CVB', type=CVB_PanelProperties)
    # pylint: enable=assignment-from-no-return


def cvb_panel_unregister():
    """Panel properties for unregistering"""
    if bpy.types.Scene.CVB is not None:
        del bpy.types.Scene.CVB

    bpy.utils.unregister_class(CVB_PanelProperties)
    bpy.utils.unregister_class(CVB_CityNameProperties)
