"""City Name and Sketch Name properties"""
#
# Ideally we would like some sort of hybrid entry field
# that combines display of the sketchname with entry of the
# city name -- this is why the file is named as it is. The
# hybrid entry field would have a different pattern when
# text is being entered than when displayed. For example,
# the city name by itself is displayed during entry and
# allows the user to modify it, but during display the
# sketch name which incorporates the city name is displayed,
# city <==> city1_g1x1. This would be more compact and likely
# more intuitive for the user.
#
# Unfortunately this doesn't seem to be possible in Blender
# as of v2.93, so we are left with taking two fields on the
# panel to display city and sketch names. (Incidentally we
# did experiment with less that satisfactory results with the
# sketchname in the panel header.)
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    PointerProperty, StringProperty, IntProperty, BoolProperty, EnumProperty)
from ..utils import sketchname_parse
from ..utils.collection_utils import collection_children


_CVB_SKETCH_NAME = sketchname_parse.SketchName()
_CVB_SKETCH_LIST = []  # We can't guarantee list to be always accurate

def is_sketch_list_empty():
    """Check to see if any sketches"""
    return len(_CVB_SKETCH_LIST) == 0


class CVB_CityNameProperties(PropertyGroup):
    # pylint: disable=invalid-name
    """City Name / Sketch Name properties"""

    def city_name_prop_update(self, context):
        """city_name_prop update callback"""

        # Do not set self.city_name_prop inside this callback, it
        # will cause runaway recursion
        name = self.city_name_prop

        if len(name) < 1:
            name = "city"

        sketchname_string = _CVB_SKETCH_NAME.update_sketchname(city=name)

        print(sketchname_string)

    def make_sketch_from_props(self, cvb):
        """Gather different properties that combine to form the sketchname"""

        city = self.city_name_prop
        seed = cvb.seed_prop
        style = cvb.sketch_style_prop
        x = cvb.sketch_x_prop if not cvb.using_tile_id_prop else cvb.sketch_xy_linked_prop
        y = cvb.sketch_y_prop if not cvb.using_tile_id_prop else cvb.sketch_xy_linked_prop
        tile = cvb.tile_id_prop if cvb.using_tile_id_prop else ""

        plain_sketchname = sketchname_parse.SketchName(
            city,           # city
            seed,           # seed
            style,          # style
            x,              # x
            y,              # y
            tile,           # tile
            0,              # variant
            "")             # import

        return plain_sketchname

    def refresh_sketch_list(self, cvb):
        """Extract the sketchnames found in the Blender Collections"""

        # We are going to refill the list so first clear it
        _CVB_SKETCH_LIST.clear()

        # Get the sketchname collection
        cvb_collections = collection_children("/CVB")

        if cvb_collections:

            for sketch_name in cvb_collections:
                sketch = sketchname_parse.SketchName()

                sketch.string_to_sketchname(sketch_name)

                _CVB_SKETCH_LIST.append(sketch)

    def sketch_names_get_next_variant(self, city, seed, style, x, y, tile=""):
        """Find the last variant value and increment it"""

        last_variant = 0

        for sketch in _CVB_SKETCH_LIST:
            if(sketch.city == city and
               sketch.seed == seed and
               sketch.style == style and
               sketch.x == x and
               sketch.y == y and
               sketch.tile == tile and
               sketch.variant > last_variant):

               last_variant = sketch.variant

        return last_variant + 1

    def sketch_names_get_all(self):
        """Return a list of just the sketch names"""

        sketch_names = list(())

        self.sketch_names_count_prop = len(sketch_names)

        return sketch_names

    city_name_prop: StringProperty(
        name="",
        default="city",
        description="""City Name\n(A filename compatible label limited in length)""",
        # We do not want options={'TEXTEDIT_UPDATE'}
        subtype='FILE_NAME',
        maxlen=28,
        update=city_name_prop_update)

    city_panel_header_prop: StringProperty(
        name="",
        description="""City name""",
        default="Cityvilleburg")

    def sketch_name_update(self, context):
        """Update other properties based off of the sketch name"""
        # This is only called if something in the list was selected

        cvb = context.scene.CVB

        sketch = sketchname_parse.SketchName()

        sketch.string_to_sketchname(cvb.city_props.sketch_name_prop)

        cvb.city_props.city_name_prop = sketch.city

    # The empty list should have a sketch name in it, but without the variant number
    # sketch_name_list =

    # ("city1_g1x1", "city1_g1x1", "Press + to generate sketch")

    def sketchnames_callback(scene, context):
        """Dynamically fill sketch_name_prop enums"""
        #
        # Be careful, this will be called every time the mouse passes over
        # the enum and for maybe a dozen times.
        #
        items = []

        for s in _CVB_SKETCH_LIST:
            if hasattr(s, "sketch_name"):
                items.append((s.sketch_name, s.sketch_name, ""))

        cvb = context.scene.CVB

        plain_sketchname = cvb.city_props.make_sketch_from_props(cvb)

        name = plain_sketchname.sketch_name

        # items.insert(0, ("city1_g1x1", "city1_g1x1", "Press + to generate sketch"))
        items.insert(0, (name, name, "Press + to generate sketch"))

        return items

    sketch_name_prop: EnumProperty(
        name="",
        description="""City Sketches""",
        default=None,
        items=sketchnames_callback,
        update=sketch_name_update)
