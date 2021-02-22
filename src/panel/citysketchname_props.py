"""City Name / Sketch Name properties"""
#
# Ideally we would like some sort of hybrid entry field
# that has a different pattern when text is being entered
# than when displayed. For example, the city name by itself
# is displayed during entry and allows the user to modify it,
# but during display the sketch name which incorporates the
# city name is displayed, city <==> city1_g1x1. This would be
# more compact and likely more intuitive for the user.
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

cvb_sketchname = sketchname_parse.SketchName()


def is_sketch_list_empty():
    return False


class CVB_CityNameProperties(PropertyGroup):
    # pylint: disable=invalid-name
    """City Name / Sketch Name properties"""

    def city_name_prop_update(self, context):
        """city_name_prop update callback"""

        # Do not set self.city_name_prop inside this callback, it
        # will cause runaway recursion
        name = self.city_name_prop

        print("city_name_prop_update()", name)

        if len(name) < 1:
            name = "city"

        global cvb_sketchname
        sketchname_string = cvb_sketchname.update_sketchname(city=name)

        # self.update_sketchname_list(sketchname_string)

    def sketch_names_get_next_variant(self, city, seed, style, x, y, tile=""):

        last_variant = 0

        return last_variant + 1

    # def sketch_names_add_name(self, sketch_name_record):
    #
    #     sketch_names = self.sketch_names_get_all()
    #
    #     # sketch_names.add(sketch_name_record["sketch_name"])
    #
    #     # Update the count regardless
    #     self.sketch_names_count_prop = len(sketch_names)
    #

    def sketch_names_get_all(self):
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
        """Combo name, seed, variant"""
        # return context.scene.CVB.city_name_field_prop + self.city_name_postfix()
        return context.scene.CVB.city_name_field_prop

    # For internal use
    sketch_names_count_prop: IntProperty(name="", description="", default=0)

    # The empty list should have a sketch name in it, but without the variant number
    # sketch_name_list =

    # ("city1_g1x1", "city1_g1x1", "Press + to generate sketch")

    def sketchnames_callback(scene, context):
        items = [
            ("city1_g1x1.001", "city1_g1x1.001", ""),
            ("city1_g1x1.002", "city1_g1x1.002", ""),
        ]

        items.insert(0, ("city1_g1x1", "city1_g1x1", "Press + to generate sketch"))

        return items

    sketch_name_prop: EnumProperty(
        name="",
        description="""City Sketches""",
        default=None,
        items=sketchnames_callback,
        update=sketch_name_update)
