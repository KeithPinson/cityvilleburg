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

from math import isclose

import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    PointerProperty, StringProperty, IntProperty, BoolProperty, EnumProperty)
# pylint: disable=relative-beyond-top-level
from .citysketchname_props import CVB_CityNameProperties, is_sketch_list_empty
from ..utils.collection_utils import viewlayer_collections, collection_sibling_names
from ..utils.object_utils import object_get, object_get_or_add_empty, object_parent_all
from ..utils.fass_grid import fassGrid



def _mini_factor(t, n):
    """For a square scale vector: factor will result in a NxN x, y geometry"""
    # This is intended for tiles. As the lengths of x and y diverge, the
    # resulting geometry will approach 2Nx0
    f = 1

    if len(t) > 1:
        a = t[0]
        b = t[1]
        f = 2*n / (a + b) if (a + b) > 0 else 1

    return f


class CVB_PanelProperties(PropertyGroup):
    # pylint: disable=invalid-name, line-too-long
    """Panel properties saved to the blend file"""

    _grid = fassGrid()

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

    def get_mini_sketch(self):
        """Check the size of the Transform empty to determine if mini sketch"""
        is_full = True

        cvb = bpy.context.scene.CVB
        sketch_name = cvb.city_props.sketch_name_prop

        # Get the empty
        transform_object = object_get("/CVB/{0}/{0} Transform".format(sketch_name))

        if transform_object and hasattr(transform_object, "scale") and transform_object.scale:
            is_full = isclose(1.0, transform_object.scale[0], abs_tol=0.0001)

        return not is_full

    def mini_sketch_add_or_toggle(self, is_mini=True):
        """Adds or modifies the Transform empty to change the size of the sketch"""

        #
        # Requirements:
        #   1. Shrink the size of the sketch and related map,terrain,city to
        #      to a footprint factor of 10x10 to 20x~0 depending on aspect ratio
        #   2. Center sketch to the tile zero position
        #   3. Hide any other sketches and related maps,terrains,cities
        #

        cvb = bpy.context.scene.CVB

        sketch_name = cvb.city_props.sketch_name_prop if not \
            len(cvb.import_name_prop) > 0 else ""

        if not sketch_name:
            return

        # Make sure the view layers are in sync
        scene = viewlayer_collections("/CVB/{0}".format(sketch_name))

        if scene:
            scene.exclude = False

        self.sketch_visibility_toggle(cvb.sketch_visible_prop)

        #
        # 1. Shrink Sketch
        #

        # Use the props for size rather than extracting size from sketch name
        size = (cvb.sketch_xy_linked_prop, cvb.sketch_xy_linked_prop) if \
            cvb.using_tile_id_prop else (cvb.sketch_x_prop, cvb.sketch_y_prop)

        factor = _mini_factor(size, 10)

        empty = self.parent_to_sketch(sketch_name)

        if empty:
            empty.scale = (factor, factor, factor) if is_mini else (1, 1, 1)

        #
        # 2. Center to Tile Zero
        #
        tile_position = 0 if is_mini else cvb.tile_id_prop
        self.move_tile_position(empty, tile_position)

        #
        # 3. Hide other Sketches
        #
        sketch_path = "/CVB/{0}".format(sketch_name)
        sibling_sketch_names = collection_sibling_names(sketch_path)

        for sibling_sketch_name in sibling_sketch_names:
            scene = viewlayer_collections("/CVB/{0}".format(sibling_sketch_name))

            if scene:
                scene.exclude = is_mini

            # To keep everything toggling in sync make sure these are not mini
            empty = self.parent_to_sketch(sibling_sketch_name)

            if empty:
                empty.scale = (1, 1, 1)

    def move_tile_position(self, empty, tile_id):

        if empty:
            # TODO: Get position based off tile_id
            pass

    def parent_to_sketch(self, sketch_name):

        sketch_path = "/CVB/{0}".format(sketch_name)
        empty_name = "{0} Transform".format(sketch_name)
        empty = object_get_or_add_empty(
            sketch_path, empty_name, radius=0.12, display_type='CUBE')

        if empty:
            object_parent_all(empty, "/CVB/{0}/Sketch ~ {0}".format(sketch_name))
            object_parent_all(empty, "/CVB/{0}/Map ~ {0}".format(sketch_name))
            object_parent_all(empty, "/CVB/{0}/Terrain ~ {0}".format(sketch_name))
            object_parent_all(empty, "/CVB/{0}/City ~ {0}".format(sketch_name))

        return empty

    def set_mini_sketch(self, value):
        """Toggle the mini sketch"""
        self.mini_sketch_add_or_toggle(value)

    def set_seed(self, value):
        """Keeps the addon preference seed in sync"""
        if cvb_prefs(bpy.context):
            if cvb_prefs(bpy.context).cvb_seed:
                cvb_prefs(bpy.context).cvb_seed = value

    def sketch_visibility_toggle(self, is_visible=True):
        """Turns the visibility of the sketch off or on"""
        cvb = bpy.context.scene.CVB

        sketch_name = cvb.city_props.sketch_name_prop if not \
            len(cvb.import_name_prop) > 0 else ""

        if sketch_name:
            scene = viewlayer_collections("/CVB/{0}/Sketch ~ {0}".format(sketch_name))

            if scene:
                scene.exclude = not is_visible

    def update_seed(self, context):
        """Seed update"""
        cvb = context.scene.CVB
        cvb.city_props.refresh_sketch_list(cvb)
        self.set_seed(cvb.seed_prop)

    def update_sketch_style(self, context):
        """Sketch style update"""
        cvb = context.scene.CVB
        cvb.city_props.refresh_sketch_list(cvb)

    def update_sketch_visibility(self, context):
        """Toggle visibility of sketch layer"""
        cvb = context.scene.CVB
        self.sketch_visibility_toggle(cvb.sketch_visible_prop)

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
        (x,y)  = self._grid.get_tile_xy(cvb.tile_id_prop)
        cvb.tile_position_prop = "{0:+04d} {1:+04d}".format(x,y)
        cvb.city_props.refresh_sketch_list(cvb)

    # def update_tile_position(self, context):
    #     """Translation of tile id to position"""
    #     cvb = context.scene.CVB
    #     cvb.sketch_xy_linked_prop =
    #     (x,y)  = self._grid.get_tile_xy(cvb.tile_id_prop)
    #     print(cvb.tile_id_prop, "{0:+04d} {1:+04d}".format(x,y))

    city_props: PointerProperty(type=CVB_CityNameProperties)

    import_name_prop: StringProperty(
        name="",
        description="""Imported Sketch""",
        default="")

    seed_prop: IntProperty(
        name="Seed",
        description="""Reproducible random sketch id""",
        default=1, min=1, max=32_767,
        update=update_seed)

    sketch_minimized_prop: BoolProperty(
        name="Mini Sketch Toggle",
        description="""Toggle Sketch Size""" if
        not is_sketch_list_empty() else "Inactive until New Sketch",
        get=get_mini_sketch,
        set=set_mini_sketch)

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
        default=True,
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
        default=0, min=0, max=_grid.get_last_tile(),
        update=update_tile_id)

    tile_position_prop: StringProperty(
        name="",
        description="""Matrix position from central tile""",
        default="+000 +000")
        # update=update_tile_position)

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
