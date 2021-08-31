"""Terrain Edit properties"""
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    PointerProperty, StringProperty, IntProperty, BoolProperty, EnumProperty)
from ..addon.preferences import cvb_icon


class CVB_TerrainProperties(PropertyGroup):
    # pylint: disable=invalid-name, line-too-long
    """Terrain properties saved to the blend file"""

    terrain_pen_list = [
        ('river', "River", "Pen to draw midline of river or stream", cvb_icon(bpy.context, "terrain_river_icon"), 1),
        ('ridge', "Ridge", "Pen to draw the ridge line", cvb_icon(bpy.context, 'terrain_ridge_icon'), 2),
        ('water', "Water", "Pen to mark the waterline of a pond or lake", cvb_icon(bpy.context, 'terrain_water_icon'), 3),
        ('tidal', "Tidal", "Pen to mark the high tide line of tidal water", cvb_icon(bpy.context, 'terrain_tidal_icon'), 4),
        ('flatten', "Flatten", "Weakly fills the low spots and cuts down the high spots", cvb_icon(bpy.context, 'terrain_flatten_icon'), 5)
    ]

    terrain_pen_prop: EnumProperty(
        name="",
        description="""Pen to use for editing the Terrain""",
        default='river',
        items=terrain_pen_list)

    terrain_help_prop: BoolProperty(
        name="Terrain Edit Help",
        description="""Show Terrain Edit cheat sheet""",
        default=False)

    terrain_clear_prop: BoolProperty(
        name="Terrain Clear",
        description="""Clear all terrain""",
        default=False)

    terrain_autogen_prop: BoolProperty(
        name="Terrain Auto-generate",
        description="""Clear all terrain and autogenerate new""",
        default=False)

