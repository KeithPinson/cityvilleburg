"""City Name / City File Name combo property"""
#
# Like a file name that doesn't show the file extension until
# the user has hit enter, we want the user to only be able to
# modify the city name but we want to show the recommended file
# name after they have hit enter. For example,
#
#           city    ==>     city1_g1x1
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    PointerProperty, StringProperty, IntProperty, BoolProperty, EnumProperty)

cvb_vals = {"cityFile": "", "city": ""}

class CVB_CityNameProperties(PropertyGroup):
    # pylint: disable=invalid-name
    """City name / City filename properties"""

    def __init__(self):
        print("props")

    def city_name_postfix(self):
        """<seed> "_" <type> <size> <tile> <variant>"""

        v_type = "g"
        v_size = "1x1"
        v_tile = ""
        v_variant = ""

        postfix = """{seed}-{type}{size}{tile}{vari}""".format(
            seed=1,  # self.seed_prop,
            type=v_type,
            size=v_size,
            tile=v_tile,
            vari=v_variant)

        return postfix

    def city_name_prop_update(self, context):
        """city_name_prop update callback"""
        # Do not set self.city_name_prop inside this callback, it
        # will cause runaway recursion
        name = self.city_name_prop

        print("city_name_prop_update()", name)

        if len(name) < 1:
            name = "city"

        cvb_vals["city"] = name
        cvb_vals["cityFile"] = name + self.city_name_postfix()
        # self.city_panel_header_prop = "CVB – " + cvb_vals["city"]

    city_name_prop: StringProperty(
        name="",
        default="""city""",
        description="""City Name""",
        # We do NOT want options={'TEXTEDIT_UPDATE'}
        subtype='FILE_NAME',
        maxlen=28,
        update=city_name_prop_update)

    city_panel_header_prop: StringProperty(
        name="",
        description="""City name""",
        default="Cityvilleburg")
