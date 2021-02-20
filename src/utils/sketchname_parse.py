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


# pylint: disable=too-many-arguments


def format_city_name(city):
    """Format the city name string for incorporating into Sketch Name string"""
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
        t_city = re.sub(r"[<>:\"/\\\|?*]", "", t_city)

        # Capitalize words and remove spaces
        t_city = t_city.title()  # Underscores have to be removed before calling this
        t_city = t_city.replace(" ", "")

    except TypeError:
        t_city = ""
    else:
        t_city = ""

    return t_city


def convert_length_to_km_string(length):
    """Convert length like 1000 to '1' or 30 to '30M'"""

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
    # pylint: disable=line-too-long, invalid-name
    """Parse Sketch Name string to get its components returned as a dict"""

    # The sketch name should have the following format:
    #
    #     {city}{seed}_{style}{x}x{y}{tile}{variant}
    #
    #     Where the optional tile will have a leading hyphen character, and
    #     the variant (which may be blank if not added) will have a leading dot.
    #
    # -------------------------------------
    #
    # Can confirm on regex101.com
    #
    # /(?:(\w+)(?:(?:\#?)([\d]+)))_([a-zA-Z0-9])([^x]+)x([0-9]+M?)(?:(?:\-)([0-9]+))?(?:(?:.)([\d]{3}))?/gm
    #
    # City1_g1x1
    # City1_g10x20
    # City1_g30Mx30M
    # City1_g1x1-00001
    # City1_g10x20-00002
    # City1_g30Mx30M-00003
    # City1_g30Mx30M.001
    # City1_g1x1-00001.002
    # TauCeti5#1_g30Mx30M.001
    # TauCeti5#1_g1x1-00001.002
    #

    sketch_name_record = None

    # Regex that captures the format as described above, resulting in:
    #    city, seed, style, x, y, tile, variant
    rex = r"""(?:(\w+)(?:(?:\#?)([\d]+)))_([a-zA-Z0-9])([^x]+)x([0-9]+M?)(?:(?:\-)([0-9]+))?(?:(?:.)([\d]{3}))?"""

    m = re.match(rex, sketchname_string)

    if m is not None:
        city, seed, style, x, y, tile, variant = m.groups()

        if tile is None:
            tile = ""

        if variant is None:
            variant = 0

        sketch_name_record = {
            "sketch_name": sketchname_string,
            "city": city,
            "seed": seed,
            "style": style,
            "x": x,
            "y": y,
            "tile": tile,
            "variant": variant
        }

    return sketch_name_record


def sketchname_to_string(sketchname):
    """Extract the Sketch Name string and return it"""

    sketch_name_string = ""

    if sketchname is not None:
        try:
            if len(sketchname['sketch_name']) > 0:
                sketch_name_string = sketchname['sketch_name']
        except KeyError:
            sketch_name_string = ""

    return sketch_name_string


def build_sketchname_string(city, seed, style, x, y, tile="", variant=0):
    # pylint: disable=invalid-name, too-many-locals
    """From the parameters build and return the Sketch Name string"""

    sketch_name = ""

    # The tile needs to either be an empty string or a zero-filled,
    # five digit, numeric string preceded by a dash (-)
    t_tile = ""

    if tile != "":
        try:
            v = int(tile.lstrip('-'))
            t_tile = "-" + str(v).zfill(5)
        except ValueError:
            t_tile = ""

    # Variant needs to either be an empty string or a zero-filled,
    # three digit, numeric string preceded by a dot (.)
    t_variant = ""

    try:
        v = int(variant)

        if v > 0:
            t_variant = "." + str(v).zfill(3)

    except ValueError:
        t_variant = ""

    # If subtype='FILE_NAME' was used with the StringProperty we should be
    # passed a filename compatible string, however we still may need to remove
    # quoting and spaces, so we will format the string making no assumptions
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

        # We'll add a # character if the city name ends in a number
        last_letter = t_city[-1:]
        if last_letter.isnumeric():
            t_city = t_city + "#"

        # Example: city1_g1x1
        sketch_name = """{city}{seed}_{style}{x}x{y}{tile}{variant}""". \
            format(
                city=t_city,
                seed=t_seed,
                style=t_style,
                x=t_x,
                y=t_y,
                tile=t_tile,
                variant=t_variant)

    return sketch_name

# pylint: enable=too-many-arguments
