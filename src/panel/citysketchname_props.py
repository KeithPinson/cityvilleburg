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
# as of v2.93, so we are left with using two fields on the
# panel to display city and sketch names. (Incidentally we
# did experiment with one city field and with sketchname
# displayed in the panel header. Less room was taken but
# it was confusing to decipher what was going on.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    PointerProperty, StringProperty, IntProperty, BoolProperty, EnumProperty)
from ..utils import sketchname_parse
from ..utils.collection_utils import collection_children

# Globals needed by Blender
_CVB_SKETCHNAME = sketchname_parse.SketchName()
_CVB_SKETCH_LIST = []  # We can't guarantee list to be always accurate
_CVB_SKETCH_NAME_ENUMS = []


def is_sketch_list_empty():
    """Check to see if any sketches"""
    return len(_CVB_SKETCH_LIST) == 0


def is_import():
    """Check to see if sketch is an import"""
    return len(_CVB_SKETCHNAME.import_name) > 0


class CVB_CityNameProperties(PropertyGroup):
    # pylint: disable=invalid-name
    """City Name / Sketch Name properties"""

    def _get_properties(self, cvb, variant=-1, import_name=""):

        components = {
            'city': "",
            'seed': "",
            'style': "",
            'x': "",
            'y': "",
            'tile': "",
            'variant': 0,
            'import_name': import_name
        } if import_name else {
            'city': self.city_name_prop,
            'seed': cvb.seed_prop,
            'style': cvb.sketch_style_prop,
            'x': cvb.sketch_x_prop if not cvb.using_tile_id_prop else cvb.sketch_xy_linked_prop,
            'y': cvb.sketch_y_prop if not cvb.using_tile_id_prop else cvb.sketch_xy_linked_prop,
            'tile': cvb.tile_id_prop if cvb.using_tile_id_prop else "",
            'variant': variant if variant >= 0 else cvb.variant_prop,
            'import_name': ""
        }

        return components

    def refresh_sketch_list(self, cvb):
        """Rebuild sketch name strings by pulling from the Blender Collections"""
        # Currently this is called everytime the panel draws()

        # We are going to refill the list so first clear it
        _CVB_SKETCH_LIST.clear()

        # Get the sketchname collection
        cvb_collections = collection_children("/CVB")

        if cvb_collections:

            for sketch_name in cvb_collections:
                sketch = sketchname_parse.SketchName()

                sketch.string_to_sketchname(sketch_name)

                _CVB_SKETCH_LIST.append(sketch)

    def refresh_sketch_name(self, cvb):
        """Set the current sketch name"""

        global _CVB_SKETCHNAME
        del _CVB_SKETCHNAME
        _CVB_SKETCHNAME = self.sketch_name(cvb)

        # print(_CVB_SKETCHNAME.to_json())

    def sketch_name_items_callback(scene, context):
        """Dynamically fill sketch_name_prop enums"""

        # Be careful, this will be called every time the mouse passes over
        # the enum and for maybe a dozen times.

        items = []

        #
        # 1. Fill items -- We assume the _CVB_SKETCH_LIST
        #                  is current and correct
        #
        for s in _CVB_SKETCH_LIST:
            if hasattr(s, "sketch_name"):
                items.append((s.sketch_name, s.sketch_name, ""))

        #
        # 2. Add example sketch name that may be added
        #
        cvb = context.scene.CVB

        plain_sketch_name = cvb.city_props.sketch_name_with_no_variant(cvb)

        sketches = [sk for sk in _CVB_SKETCH_LIST if sk.sketch_name.startswith(plain_sketch_name)]

        if not sketches:
            pending_name = "[" + plain_sketch_name + "]"
            items.insert(0, (plain_sketch_name, pending_name, "Press + to generate sketch"))

        global _CVB_SKETCH_NAME_ENUMS
        _CVB_SKETCH_NAME_ENUMS.clear()
        _CVB_SKETCH_NAME_ENUMS.extend(items)

        return _CVB_SKETCH_NAME_ENUMS

    def sketch_name_with_next_variant(self, cvb):
        """Find the last variant value and increment it"""

        plain_sketchname = self.sketch_name_with_no_variant(cvb)

        last_variant = 0

        for sketch in _CVB_SKETCH_LIST:

            new_variant = last_variant

            try:
                new_variant = int(sketch.variant)
            except ValueError:
                new_variant = last_variant

            this_plain_sketchname = sketch.sketchname_string_plain()

            if(this_plain_sketchname == plain_sketchname and
               new_variant > last_variant):

                last_variant = new_variant

        cvb.variant_prop = last_variant + 1

        props = self._get_properties(cvb, variant=(last_variant + 1))

        plain_sketch_name = sketchname_parse.build_sketchname_string(
            props['city'],
            props['seed'],
            props['style'],
            props['x'],
            props['y'],
            props['tile'],
            props['variant'],
            props['import_name'])

        return plain_sketch_name

    def sketch_name_with_no_variant(self, cvb, ascii_only=False):
        """Gather properties to form the sketch name string less the variant"""

        props = self._get_properties(cvb)

        plain_sketch_name = sketchname_parse.build_sketchname_string(
            props['city'],
            props['seed'],
            props['style'],
            props['x'],
            props['y'],
            props['tile'],
            0,
            props['import_name'],
            ascii_only=ascii_only)

        return plain_sketch_name

    def sketch_name(self, cvb):
        """Gather properties and combine to form the sketchname class"""

        props = self._get_properties(cvb)

        sketchname = sketchname_parse.SketchName(
            props['city'],
            props['seed'],
            props['style'],
            props['x'],
            props['y'],
            props['tile'],
            props['variant'],
            props['import_name'])

        return sketchname

    def update_city_name_prop(self, context):
        """city_name_prop update callback"""

        # Do not set self.city_name_prop inside this callback, it
        # will cause runaway recursion
        name = self.city_name_prop

        if len(name) < 1:
            name = "city"

    def update_sketch_name(self, context):
        """Update other properties based off of the sketch name"""
        # This is only called if something in the list was selected

        cvb = context.scene.CVB

        sketch = sketchname_parse.SketchName()

        sketch.string_to_sketchname(cvb.city_props.sketch_name_prop)

        # Update panel properties based on sketchname

        cvb.city_props.refresh_sketch_list(cvb)

        cvb.city_props.city_name_prop = sketch.city

    city_name_prop: StringProperty(
        name="",
        default="city",
        description="""City Name""",
        subtype='NONE',  # 'FILE_NAME' currently does not filter "[<>:\"/\\|?*]" chars
        # The options={'TEXTEDIT_UPDATE'} will not fix FILE_NAME not filtering
        maxlen=100,
        update=update_city_name_prop)

    city_panel_header_prop: StringProperty(
        name="",
        description="""City name""",
        default="Cityvilleburg")

    sketch_name_prop: EnumProperty(
        name="",
        description="""City Sketches""",
        default=None,
        items=sketch_name_items_callback,
        update=update_sketch_name)
