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
_CVB_SKETCH_NAME_ENUMS_NUM = 0


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

    def get_sketch_name(self):

        sketch_name = _CVB_SKETCH_NAME_ENUMS[_CVB_SKETCH_NAME_ENUMS_NUM][1]\
            if _CVB_SKETCH_NAME_ENUMS else "[City1_g1x1]"

        return sketch_name

    def refresh_sketch_list(self, cvb):
        """Rebuild sketch name strings by pulling from the Blender Collections"""
        # Currently this is called everytime the panel draws()

        # We are going to refresh 3 global variables
        global _CVB_SKETCH_LIST, _CVB_SKETCH_NAME_ENUMS, _CVB_SKETCH_NAME_ENUMS_NUM

        #
        # 1. Refresh the list of sketches found in the Outliner of
        #    the Blender Collections
        #
        # We assume the user may have deleted something, so start from scratch
        _CVB_SKETCH_LIST.clear()

        # Get the sketchname collection
        cvb_collections = collection_children("/CVB")

        if cvb_collections:

            for sketch_name in cvb_collections:
                sketch = sketchname_parse.SketchName()

                sketch.string_to_sketchname(sketch_name)

                _CVB_SKETCH_LIST.append(sketch)

        #
        # 2. Fill enums -- We assume the _CVB_SKETCH_LIST
        #                  is current and correct
        #
        enums = []
        enum_number = 1

        for s in _CVB_SKETCH_LIST:
            if hasattr(s, "sketch_name"):
                enums.append((s.sketch_name, s.sketch_name, "", enum_number))
                enum_number += 1

        enums.sort()

        #
        # 3. Insert the pending sketch name that may be added
        #
        pending_sketch_name = cvb.city_props.sketch_name_with_no_variant(cvb)

        sketches_found = [sk for sk in _CVB_SKETCH_LIST if sk.sketch_name.startswith(pending_sketch_name)]

        if not sketches_found:
            # Insert the pending first
            pending_display_name = "[" + pending_sketch_name + "]"
            enums.insert(
                0,
                (pending_sketch_name, pending_display_name, "Press + to generate sketch", 0))

        # Renumber the enums
        for i in range(len(enums)):
            enums[i] = (enums[i][0], enums[i][1], enums[i][2], i)

        _CVB_SKETCH_NAME_ENUMS.clear()
        _CVB_SKETCH_NAME_ENUMS.extend(enums)

        #
        # 4. Adjust the default enum to match the props
        #
        if sketches_found:
            ids_found = \
                [item[3] for item in _CVB_SKETCH_NAME_ENUMS if item[0].startswith(pending_sketch_name)]

            if(ids_found):
                _CVB_SKETCH_NAME_ENUMS_NUM = ids_found[-1:].pop()  # Use the last found

        else:
            _CVB_SKETCH_NAME_ENUMS_NUM = 0

    def refresh_sketch_name(self, cvb):
        """Set the current sketch name"""

        global _CVB_SKETCHNAME
        del _CVB_SKETCHNAME
        _CVB_SKETCHNAME = self.sketchname(cvb)

        # print(_CVB_SKETCHNAME.to_json())

    def set_sketch_name(self, value):
        return

    def sketch_name_items_callback(scene, context):
        """Dynamically fill sketch_name_prop enums"""

        #
        # This will be called frequently as the mouse passes over the enum
        #

        cvb = context.scene.CVB
        cvb.city_props.refresh_sketch_list(cvb)

        # We assume the global vars are upto data
        global _CVB_SKETCH_NAME_ENUMS

        return _CVB_SKETCH_NAME_ENUMS

    def sketch_name_with_next_variant(self, cvb):
        """Find the last variant value and increment it"""

        plain_sketch_name = self.sketch_name_with_no_variant(cvb)

        last_variant = 0

        variances_found = \
            [sk.variant for sk in _CVB_SKETCH_LIST if sk.sketch_name.startswith(plain_sketch_name)]

        if variances_found:
            variances_found.sort()

            last_variant = variances_found[-1:].pop()

        try:
            new_variant = int(last_variant) + 1
        except ValueError:
            new_variant = 1

        cvb.variant_prop = new_variant

        props = self._get_properties(cvb, variant=new_variant)

        plain_sketch_name = sketchname_parse.build_sketchname_string(
            props['city'],
            props['seed'],
            cvb.encode_style(props['style']),
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
            cvb.encode_style(props['style']),
            props['x'],
            props['y'],
            props['tile'],
            0,
            props['import_name'],
            ascii_only=ascii_only)

        return plain_sketch_name

    def sketchname(self, cvb):
        """Gather properties and combine to form the sketchname class"""

        props = self._get_properties(cvb)

        sketch = sketchname_parse.SketchName(
            props['city'],
            props['seed'],
            cvb.encode_style(props['style']),
            props['x'],
            props['y'],
            props['tile'],
            props['variant'],
            props['import_name'])

        return sketch

    def update_city_name_prop(self, context):
        """city_name_prop update callback"""

        # Do not set self.city_name_prop inside this callback, it
        # will cause runaway recursion
        name = self.city_name_prop

        if len(name) < 1:
            name = "city"

        global _CVB_SKETCH_NAME_ENUMS, _CVB_SKETCH_NAME_ENUMS_NUM
        current_sketch_name = _CVB_SKETCH_NAME_ENUMS[_CVB_SKETCH_NAME_ENUMS_NUM][0]

    def update_sketch_name(self, context):
        """Update other properties based off of the sketch name"""
        # This is only called if something in the list was selected

        cvb = context.scene.CVB if context else bpy.context.scene.CVB

        this_name = cvb.city_props.sketch_name_enum_prop

        #
        # Set selected enum number
        #
        global _CVB_SKETCH_NAME_ENUMS_NUM
        _CVB_SKETCH_NAME_ENUMS_NUM = \
            [item[3] for item in _CVB_SKETCH_NAME_ENUMS if item[0] == this_name].pop()

        #
        # Update panel properties based on sketchname
        #
        sketches = [sk for sk in _CVB_SKETCH_LIST if sk.sketch_name == this_name]

        sketch = sketches[0] if sketches else None

        if not sketch:
            # Derive the sketch from the sketch name
            sketch = sketchname_parse.SketchName()
            sketch.string_to_sketchname(this_name)

        if sketch:
            if len(sketch.import_name) > 0:
                cvb.city_props.city_panel_header_prop = "Cityvilleburg – Import"
                cvb.city_props.sketch_name_prop = sketch.import_name            # import_name
            else:
                cvb.city_props.city_panel_header_prop = "Cityvilleburg"
                cvb.city_props.sketch_name_prop = sketch.get_sketch_name()      # sketch_name
                cvb.city_props.city_name_prop = sketch.get_city()               # city
                cvb.seed_prop = sketch.get_seed()                               # seed
                cvb.sketch_style_prop = cvb.decode_style(sketch.get_style())    # style
                cvb.sketch_x_prop = sketch.get_x()                              # x
                cvb.sketch_y_prop = sketch.get_y()                              # y
                cvb.tile_id_prop = sketch.get_tile()                            # tile
                cvb.variant_prop = sketch.get_variant()                         # variant

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

    sketch_name_prop: StringProperty(
        name="",
        default="",
        description="""Static Sketch Name\nAutomatically generated name for copying.\nEdits will be discarded.""",
        get=get_sketch_name,
        set=set_sketch_name,
        subtype='NONE')

    sketch_name_enum_prop: EnumProperty(
        name="",
        description="""City Sketches""",
        default=None,
        items=sketch_name_items_callback,
        update=update_sketch_name)
