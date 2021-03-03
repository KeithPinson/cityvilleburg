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
import json

# pylint: disable=too-many-arguments, too-many-instance-attributes, too-many-locals

_CVB_PENDING_NAME = ""


def build_sketchname_string(city, seed, style, x, y, tile="", variant=0, import_name="", ascii_only=False):
    # pylint: disable=invalid-name, too-many-locals
    """From the parameters build and return the Sketch Name string"""

    sketch_name = ""
    global _CVB_PENDING_NAME
    _CVB_PENDING_NAME = ""

    # Make sure one set of parameters are set or the other (import name)
    if not verify_sketchname_parameters(city, seed, style, x, y, import_name):
        return sketch_name

    #
    # Import Name
    #
    if len(import_name) > 0:

        # We are going to enforce the same rules for file names
        t_name = format_file_name(import_name)

        sketch_name = """{name}""".format(name=t_name)

        return sketch_name

    # The tile needs to either be an empty string or a zero-filled,
    # five digit, numeric string preceded by a dash (-)
    t_tile = ""

    if tile != "":
        try:
            v = int(str(tile).lstrip('-'))
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

    # The StringProperty subtype='FILE_NAME' does not validate characters. It
    # instead effects the display and shows the string as a shortened 20 character
    # filename with a few dots in the middle, replacing the removed characters.
    # So, we still need to remove invalid characters
    t_city = format_city_name(city, max_length=28, ascii_only=ascii_only)

    # Seeds should be an integer greater than zero if set
    try:
        t_seed = str(int(seed) if int(seed) > 0 else "")
    except ValueError:
        t_seed = ""

    # We only use the first letter
    try:
        t_style = style[0]
    except IndexError:
        t_style = ""

    # X and Y size follow the same rules: Basically convert to km or indicate meters
    t_x = convert_length_to_km_string(x)
    t_y = convert_length_to_km_string(y)

    # Validate the strings before building the record
    if(len(t_city) > 0 and
       len(t_seed) > 0 and
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

    _CVB_PENDING_NAME = sketch_name
    return sketch_name


def convert_length_to_km_string(length):
    """Convert length like 1000 to '1' or 30 to '30M'"""

    try:
        t_length = int(length)

        if t_length < 1000:
            length_str = str(t_length) + "M"
        else:
            length_str = str(int(t_length / 1000))

    except ValueError:
        length_str = ""

    return length_str


def format_city_name(city, max_length=100, ascii_only=False):
    # pylint: disable=line-too-long
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
        t_city = "" + city

        # Remove leading/following quotes
        t_city = t_city.strip("""\"""")
        t_city = t_city.strip("""\'""")

        # Remove <>:"/\|?* and _
        t_city = format_file_name(t_city)
        t_city = t_city.replace("_", "")  # Underscore is reserved as a delimiter in the sketchname

        # Capitalize words and remove spaces
        t_city = t_city.title()  # Make sure to remove underscores before calling this
        t_city = t_city.replace(" ", "")

        # Truncate the city name to an arbitrary number of characters
        if len(t_city) > max_length:
            # Two-dot-leader; Unicode 0x2025 character
            two_dot = ".." if ascii_only else "‥"
            end_length = 5
            delimiter_length = len(two_dot)
            front_length = max_length - end_length - delimiter_length

            t_city = t_city[:front_length] + two_dot + t_city[-end_length:]

    except TypeError:
        t_city = ""

    return t_city


def format_file_name(file_name):
    """Format the string so that it is valid file format"""

    try:
        t_file_name = file_name

        # Remove <>:"/\|?* and _
        t_file_name = re.sub(r"[<>:\"/\\|?*]", "", t_file_name)

    except TypeError:
        t_file_name = ""

    return t_file_name


def verify_sketchname_parameters(city, seed, style, x, y, import_name):
    """Verify that we are not trying to set import name and other parameters"""
    # pylint: disable=invalid-name

    is_valid = True

    if not isinstance(city, str) or len(city) == 0:
        is_valid = False

    if not str(seed).isnumeric():
        is_valid = False

    if not isinstance(style, str) or len(style) == 0:
        is_valid = False

    if not str(x).isnumeric():
        is_valid = False

    if not str(y).isnumeric():
        is_valid = False

    # We are okay if everything is invalid but we have an import_name
    if not is_valid and (isinstance(import_name, str) and len(import_name) > 0):
        is_valid = True

    return is_valid


class SketchName:
    """Unless imported, Sketches are identified by a combination of parameters"""

    sketch_name = ""
    city = ""
    seed = ""
    style = ""
    x = ""
    y = ""
    tile = ""
    variant = 0
    import_name = ""

    def __init__(
            self,
            city="",
            seed="",
            style="",
            x="",
            y="",
            tile="",
            variant=0,
            import_name=""):

        self.update_sketchname(city, seed, style, x, y, tile, variant, import_name)

    def string_to_sketchname(self, sketchname_string):
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
        # /(?:(?:(\w+)(?:(?:\#?)([\d]+)))_([a-zA-Z0-9])([^x]+)x([0-9]+M?)(?:(?:\-)([0-9]+))?(?:(?:.)([\d]{3}))?)|(.+)/gm
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
        # Motown
        #

        # Regex that captures the format as described above, resulting in:
        #    city, seed, style, x, y, tile, variant
        rex = r"""(?:(?:(\w+)(?:(?:\#?)([\d]+)))_([a-zA-Z0-9])([^x]+)x([0-9]+M?)(?:(?:\-)([0-9]+))?(?:(?:.)([\d]{3}))?)|(.+)"""

        m = re.match(rex, sketchname_string)

        if m is not None:
            city, seed, style, x, y, tile, variant, import_name = m.groups()

            self.sketch_name = sketchname_string
            self.city = city
            self.seed = seed
            self.style = style
            self.x = x
            self.y = y
            self.tile = tile if tile is not None else ""
            self.variant = variant if variant is not None else 0
            self.import_name = import_name if import_name is not None else ""

    def sketchname_string(self):
        """Extract the Sketch Name string and return it"""

        return self.sketch_name

    def sketchname_string_plain(self):
        """Return the sketchname string without the variant"""

        plain_sketchname_string = build_sketchname_string(
            self.city,
            self.seed,
            self.style,
            self.x,
            self.y,
            self.tile)

        return plain_sketchname_string

    def to_json(self) -> str:
        result = ""

        json_str = """{{\
            "sketch_name": "{sketch_name}",\
            "city": "{city}",\
            "seed": "{seed}",\
            "style": "{style}",\
            "x": "{x}",\
            "y": "{y}",\
            "tile": "{tile}",\
            "variant": {variant},\
            "import_name": "{import_name}"\
        }}""".format(
            sketch_name=self.sketch_name,
            city=self.city,
            seed=self.seed,
            style=self.style,
            x=self.x,
            y=self.y,
            tile=self.tile,
            variant=self.variant,
            import_name=self.import_name
        )

        result = json_str

        return result


    def update_sketchname(
            self,
            city="",
            seed="",
            style="",
            x="",
            y="",
            tile="",
            variant=0,
            import_name=""):

        # pylint: disable=invalid-name
        """Usage: update_sketchname( city="London" ) for example to change the city member"""

        #
        # No matter what changes we must change the sketch_name string
        #
        # Everything else we make the change it as given
        #
        # The sketchname record is defined in string_to_sketchname()
        #

        t_city = city if city != "" else self.city
        t_seed = seed if seed != "" else self.seed
        t_style = style if style != "" else self.style
        t_x = x if x != "" else self.x
        t_y = y if y != "" else self.y
        t_tile = tile if tile != "" else self.tile
        t_variant = variant if variant != 0 else self.variant
        t_import_name = import_name if import_name != "" else self.import_name

        t_sketch_name = build_sketchname_string(
            t_city,
            t_seed,
            t_style,
            t_x,
            t_y,
            t_tile,
            t_variant,
            t_import_name)

        self.sketch_name = t_sketch_name
        self.city = t_city
        self.seed = t_seed
        self.style = t_style
        self.x = t_x
        self.y = t_y
        self.tile = t_tile
        self.variant = t_variant
        self.import_name = t_import_name

        return t_sketch_name

# pylint: enable=too-many-arguments
