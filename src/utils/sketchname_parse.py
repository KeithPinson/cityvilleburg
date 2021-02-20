"""Convert between Sketch Name and string"""
#
# Facilitate converting back and forth between Sketch Name
# and string.
#
# The Sketch Name encodes some of the key properties of the
# sketch map. There doesn't seem to be a clear way to store
# this information other than as a string. In addition, if
# we did try to store this information as a record, there
# are multiple points where the user could modify or delete
# the record. So, we will be storing the Sketch Name as a
# string in just one location. The definitions in this file
# aid in this design goal.
#
# The Sketch Name is composed of the:
#
#   - City name
#   - Seed
#   - City type
#   - X and Y dimensions
#   - Tile ID (optional if only 1 tile)
#
# In addition there is a variant number. It is stored
# separately from the Sketch Name although it may be
# concatenated to the Sketch Name string.
#
# Copyright (c) 2021 Keith Pinson

import re
import bpy


def format_city_name(city):
    #
    # The string must:
    #
    #   1) Be filename compatible
    #   2) Must not contain an underscore, "_"
    #   3) Each word must be capitalized
    #   4) All space must be removed
    #   5) Not be quoted
    #

    try:
        t_city = city

        # Remove leading/following quotes
        t_city = t_city.strip("""\"""")
        t_city = t_city.strip("""\'""")

        # Remove <>:"/\|?* and _
        t_city = re.sub("[<>:\"/\\\|?*]", "", t_city)

        # Capitalize words and remove spaces
        t_city = t_city.title()  # Underscores have to be removed first
        t_city = t_city.replace(" ", "")

        # t_city = t_city.encode('ascii', 'ignore')  # This is probably overkill

    except TypeError:
        t_city = ""
    else:
        t_city = ""

    return t_city


def convert_length_to_km_string(length):
    length_str = ""

    try:
        t_length = int(length)

        if t_length < 1000:
            length_str = str(t_length) + "M"
        else:
            length_str = str(int(t_length / 1000))
    except ValueError:
        length_str = ""

    return length_str


def string_to_sketchname(sketchname_string):

    # The sketch name should have the following format:
    #
    #     {city}{seed}_{style}{x}x{y}{tile}
    #
    #     Where the optional tile will have a leading hyphen character.

    sketch_name_record = None

    # First break the string at the underscore into a,b halves
    a, b = sketchname_string.split('_')

    # Handle the case where the city name ends in with a number
    pos = str(a).find('#')

    if pos < 0:
        m = re.match("([^\d]+)([\d]+)", a)
        city, seed = m.groups()
    else:
        # The city and seed were delimited with a hash symbol
        city, seed = a.split('#')

    m = re.match("([a-zA-Z0-9])([^x]+)x([0-9]+M?)(\-[0-9]+)?", b)
    style, x, y, tile = m.groups()

    if tile is not None:
        tile.lstrip('-')

    sketchname = build_sketchname_string(city, seed, style, x, y, tile)

    if len(sketchname) > 0:

        sketch_name_record = {
            "sketch_name": sketchname,
            "city": city,
            "seed": seed,
            "style": style,
            "x": x,
            "y": y,
            "tile": tile,
            "variant": 0
        }

    return sketch_name_record


def sketchname_to_string(sketchname):
    sketch_name_string = ""

    try:
        if len(sketchname['sketchname_name']) > 0:
            sketch_name_string = sketchname['sketchname']
    except ValueError:
        sketch_name_string = ""

    return sketch_name_string


def build_sketchname_string(city, seed, style, x, y, tile=""):
    sketch_name = ""

    # The tile needs to either be an empty string or a zero-filled
    # numeric string preceded by a dash
    t_tile = tile

    if tile != "":
        try:
            v = int(tile.lstrip('-'))
            tile = "-" + str(v).zfill(5)
        except ValueError:
            tile = ""

    # A filename compatible city name string could be quoted and contain spaces
    t_city = format_city_name(city)

    # We don't really do anything with the seed
    t_seed = int(seed)

    # We only use the first letter
    t_style = style[0]

    # X and Y size follow the same rules: Basically convert to km or indicate meters
    t_x = convert_length_to_km_string(x)
    t_y = convert_length_to_km_string(y)

    # Validate the strings before building the record
    if(len(t_city) > 0 and
       t_seed > 0 and
       len(t_style) > 0 and
       len(t_x) > 0 and
       len(t_y) > 0):

        # We'll had a # character if the city name ends in a number
        last_letter = t_city[-1:]
        if last_letter.isnumeric:
            t_city = t_city + "#"

        # Example: city1_g1x1
        sketch_name = """{city}{seed}_{style}{x}x{y}{tile}""". \
            format(city=t_city, seed=t_seed, style=t_style, x=t_x, y=t_y, tile=t_tile)

    return sketch_name


def get_variant_from_string():
    variant = None

    return variant


def add_variant_to_string(sketchname_string, variant):
    result_string = ""
    variant_string = ""

    try:
        variant = int(variant)

        if 0 < variant < 1000:
            variant_string = str(variant)

    except ValueError:
        variant_string = ""

    if (validate_sketchname_string(sketchname_string) and
            len(variant_string) > 0):
        result_string = sketchname_string + "." + variant_string

    return result_string


def trim_variant_from_string():
    sketch_name_string = ""

    return sketch_name_string


def validate_sketchname_string(sketchname_string):
    record = string_to_sketchname(sketchname_string)

    return record is not None


def city_name_postfix(self):
    """<seed> "_" <type> <size> <tile> <variant>"""

    v_type = "g"
    v_size = "1x1"
    v_tile = ""
    v_variant = ""

    postfix = """{seed}_{type}{size}{tile}{vari}""".format(
        seed=1,  # self.seed_prop,
        type=v_type,
        size=v_size,
        tile=v_tile,
        vari=v_variant)

    return postfix
