"""Routines for identifying grids in a matrix"""
#
# By default a city map is a 1 KM square tile and a grid consists
# of 99x99 tiles with tile 0 is at the center. If we were to model
# one of the largest cities on Earth, Tokyo-Yokohama, it would just
# fit inside this space.
#
# It is simply not possible to model and render a 7,000 sqKM city
# in one shot since,
#
#     - Procedural generation works on the 1 sqKM level,
#       but chokes on the 1000 sqKM level
#     - Quantity of human-scale details would require some
#       sort of third-party database solution
#     - Terrain maps start to push into multiple GB size
#       in order to give the level of detail needed
#
# The only solution is to carve the city up into tiles and for
# Blender files to be germane to just the single tile referenced.
#
# With that in mind we develop with the following requirements:
#
# 1. A tile size can be specified in meters wide and high
# 2. A grid can consist of one tile or many tiles
# 3. If a grid consists of more than 1 tile then the grid and tiles must be square
# 4. The first tile should be at the center of the grid
# 5. Adding tiles should follow some sort of FASS style, space-filling curve model
# 6. Tiles should be numbered sequentially
# 7. A tile's position is measured in tiles not meters where the first tile is 0,0
#    and the tile to the right and down is 1,1 or to the left and up is -1,-1
# 8. Calculating the tile's x,y position should be sub-300 ms time
# 9. Given a x,y coordinate, the tile number should be calculated in sub-300 ms time
#
# Copyright (c) 2021 Keith Pinson

import bpy
from ..addon.preferences import cvb_prefs

#
# Terms Used:
#
#   Tile        The area, by default 1 KM x 1 KM, that the Blender file is editing
#   Sector      A region consisting of 9x9 tiles
#
# Considerations:
#
#    - A typical FASS curve grows quadratically -- we want growth to be something more linear
#      see: ...res/"Spiral Space Filling Curve - 4th order.gif"
#           ...res/"Square Spirangle.gif"
#    - We need some sort of system to recreate the curve identically between blender files
#      (We will be using a Lindenmayer system, https://en.wikipedia.org/wiki/L-system)
#    - Simple spiral around the city center is not ideal since we would move rapidly
#      from one side of the city to the other
#    - The total number of tiles is configurable
#    - Ultimately what drives the design is the need to have features flow seamlessly
#      from one tile to another, across the city. For example, roads should not step
#      at tile edges and things like a long ridge should continue across tiles
#


class fassGrid:

    _default_order = 11
    _sector_width = 9  # Sectors are square
    _xy_to_sector, _sector_to_xy, _sector_to_qrx = None, None, None
    _atX_xy_to_tile, _atQ_xy_to_tile, _atR_xy_to_tile = None, None, None
    _atX_tile_to_xy, _atQ_tile_to_xy, _atR_tile_to_xy = None, None, None

    # L-System for the spiralling guiding curve (L-System is best used for drawing a curve)
    # @Q, @R, @X are the FASS curves at each step of the guided curve (they will be hard-coded)
    _cvb_fass = (
        90,
        "@X-D",
        {'A': "A>@R",
         'B': "B>@Q",
         'C': "C@R>@RA->@QB>-",
         'D': "C"
        }
    )

    def _move(self, direction, position):
        pos = position

        if direction == 'N':
            pos = (position[0], position[1] - 1)
        elif direction == 'S':
            pos = (position[0], position[1] + 1)
        elif direction == 'W':
            pos = (position[0] - 1, position[1])
        elif direction == 'E':
            pos = (position[0] + 1, position[1])

        return pos

    def _turn(self, leftright, direction):
        c = direction

        if direction == 'N':
            c = 'E' if leftright == '-' else 'W'
        elif direction == 'S':
            c = 'E' if leftright == '+' else 'W'
        elif direction == 'W':
            c = 'N' if leftright == '-' else 'S'
        elif direction == 'E':
            c = 'N' if leftright == '+' else 'S'

        return c

    # The L-System his highly recursive, instead we will loop and make dictionaries to translate positions
    def _cvb_qr_loop_converters(self, soft_order):
        """Return: xy_to_sector, sector_to_xy, sector_to_qrx"""

        n = 0
        d = ""
        c = 'N'
        pos = (0, 0)
        w = {(0, 0): 0}  # xy_to_sector
        u = {0: (0, 0)}  # sector_to_xy
        v = {0: "X"}     # sector_to_qrx

        for i in range(0, soft_order):
            if i == 0:
                n = 0
                d = "X"
                c = 'N'
                w = {(0, 0): 0}
                u = {0: (0, 0)}
                v = {0: "X"}
                pos = self._move(c, pos)
                n += 1
                c = self._turn('-', c)
            else:
                for j in range(i + 1):
                    d = "r" if (i % 2) == 0 else "R"
                    w[pos] = n
                    u[n] = pos
                    v[n] = d

                    if j < i:
                        pos = self._move(c, pos)
                        n += 1
                    else:
                        c = self._turn('-', c)
                        pos = self._move(c, pos)
                        n += 1

                for _ in range(i):
                    d = "Q" if (i % 2) == 0 else "q"
                    w[pos] = n
                    u[n] = pos
                    v[n] = d

                    pos = self._move(c, pos)
                    n += 1
                c = self._turn('-', c)

        return w, u, v

    # Convert a passed FASS string like, "+>->->>->>->>>-+>>->>-" to
    # conversion dictionaries, like {0:(0,0), 1:(0,-1), 2:(1,-1), 3:(1,0), 4:(1,1), ...}
    def _cvb_fass_converters(self, fass_string, heading):
        """Return: xy_to_tile, tile_to_xy, tile_to_qrx"""

        n = 0
        d = ""
        c = heading
        pos = (0, 0)
        w = {(0, 0): 0}  # xy_to_tile
        u = {0: (0, 0)}  # tile_to_xy

        for k in fass_string:

            if k == '-' or k == '+':
                c = self._turn(k, c)
            elif k == '>':
                pos = self._move(c, pos)
                n += 1
            else:
                continue

            w[pos] = n
            u[n] = pos

        return w, u

    def _fass_order(self):
        return cvb_prefs(bpy.context).cvb_terrain_region_order if cvb_prefs(bpy.context) else self._default_order

    def _get_xy_in_sector(self, atLetter, starting_xy, relative_tile_id):

        if atLetter == "Q":
            x, y = 0, 0
        elif atLetter == "q":
            x, y = 0, 0
        elif atLetter == "R":
            x, y = 0, 0
        else:  # atLetter == "r":
            x, y = 0, 0

        return x, y

    def __init__(self):
        (self._xy_to_sector, self._sector_to_xy, self._sector_to_qrx) = self._cvb_qr_loop_converters(self._fass_order())

        _atX = "+>->->>->>->>>-+>>->>->->+>+>>+>>->>->->+>+>->>-" \
               ">->+>+>>+>>->-+>>->>->->+>+>>+>>->>->->+>+>>+>>-" \
               ">>->->+>+>->>->->+>+>>+>>->>->->+>+>>+>>-"

        _atQ = "->+>+>->->>->>+>>+>+>->->>->>+>>>+>>+>+>->->>->>+" \
               ">>+>+>->->>->>+>>+>+>->->+>>>+>>+>+>->->>->+>+>->" \
               "->>->>+>>+>+>->->>->>+->->>+>>+>+>->->"

        _atR = ">+>+>->->>->>+>+->>+>>+>+>->->>->>+>>+>+>->->+>>+>" \
               "+>->->>->>+->->+>+>->->>->>+>>+>+>->->>->>+>>+>+>-" \
               ">->>->>+->->>+>>+>+>->->>->>+>>+>+>->->+"

        (self._atX_xy_to_tile, self._atX_tile_to_xy) = self._cvb_fass_converters(_atX, 'E')
        (self._atQ_xy_to_tile, self._atQ_tile_to_xy) = self._cvb_fass_converters(_atQ, 'N')
        (self._atR_xy_to_tile, self._atR_tile_to_xy) = self._cvb_fass_converters(_atR, 'E')

    def _get_sector_number(self, x, y):

        offset_x = x + int((self._fass_order()*self._sector_width) / 2)
        offset_y = y + int((self._fass_order()*self._sector_width) / 2)

        offset_sector_x = int(offset_x / self._sector_width)
        offset_sector_y = int(offset_y / self._sector_width)

        sector_x = offset_sector_x - int(self._fass_order() / 2)
        sector_y = offset_sector_y - int(self._fass_order() / 2)

        return self._xy_to_sector[(sector_x, sector_y)]

    def _get_sector_xy(self, tile_id):
        length = len(self._sector_to_xy)
        sector_id = int(tile_id / self._sector_width**2)
        return self._sector_to_xy[sector_id] \
            if sector_id < length else self._sector_to_xy[length-1]

    def _get_sector_qrx(self, tile_id):
        length = len(self._sector_to_xy)
        sector_id = int(tile_id / self._sector_width**2)
        return self._sector_to_qrx[sector_id] \
            if sector_id < length else self._sector_to_xy[length-1]

    def get_tile_xy(self, tile_id):
        sector_x, sector_y = self._get_sector_xy(tile_id)
        x, y = 0, 0
        x_offset, y_offset = 0, 0
        qrx = self._get_sector_qrx(tile_id)

        pos = int(tile_id % self._sector_width**2)

        if qrx == 'X':
            pos = pos if pos < len(self._atX_tile_to_xy) else 0
            x, y = self._atX_tile_to_xy[pos]
            x_offset = 0
            y_offset = 0

        elif qrx == 'Q':
            pos = pos if pos < len(self._atQ_tile_to_xy) else 0
            x_offset = (self._sector_width * sector_x) - int(self._sector_width / 2)
            y_offset = (self._sector_width * sector_y) + int(self._sector_width / 2)
            x, y = self._atQ_tile_to_xy[pos]


        elif qrx == 'R':
            pos = pos if pos < len(self._atR_tile_to_xy) else 0
            x_offset = (self._sector_width * sector_x) - int(self._sector_width / 2)
            y_offset = (self._sector_width * sector_y) + int(self._sector_width / 2)
            x, y = self._atR_tile_to_xy[pos]

        elif qrx == 'q':
            pos = pos if pos < len(self._atQ_tile_to_xy) else 0
            x_offset = (self._sector_width * sector_x) + int(self._sector_width / 2)
            y_offset = (self._sector_width * sector_y) - int(self._sector_width / 2)
            x, y = self._atQ_tile_to_xy[pos]
            x = -x
            y = -y

        elif qrx == 'r':
            pos = pos if pos < len(self._atR_tile_to_xy) else 0
            x_offset = (self._sector_width * sector_x) + int(self._sector_width / 2)
            y_offset = (self._sector_width * sector_y) - int(self._sector_width / 2)
            x, y = self._atR_tile_to_xy[pos]
            x = -x
            y = -y

        x = x + x_offset
        y = y + y_offset

        return x, y

    def get_tile_id(self, x, y):

        tile_id = 0

        abs_max = int(self._fass_order() * self._sector_width / 2)

        if x < -abs_max:
            x = -abs_max
        elif x > abs_max:
            x = abs_max

        if y < -abs_max:
            y = -abs_max
        elif y > abs_max:
            y = abs_max

        sector_number = self._get_sector_number(x, y)
        qrx = self._sector_to_qrx[sector_number]
        sector_x, sector_y = self._sector_to_xy[sector_number]

        tile_id_offset = sector_number * (self._sector_width ** 2)

        corner_x = (x + abs_max) % self._sector_width
        corner_y = (y + abs_max) % self._sector_width

        if qrx == 'X':
            pos_x = x
            pos_y = y
            tile_id = self._atX_xy_to_tile[(pos_x, pos_y)]
        elif qrx == 'Q':
            pos_x = corner_x - 0
            pos_y = corner_y - (self._sector_width - 1)
            tile_id = self._atQ_xy_to_tile[(pos_x, pos_y)]
        elif qrx == 'R':
            pos_x = corner_x - 0
            pos_y = corner_y - (self._sector_width - 1)
            tile_id = self._atR_xy_to_tile[(pos_x, pos_y)]
        elif qrx == 'q':
            pos_x = corner_x - (self._sector_width - 1)
            pos_y = corner_y - 0
            pos_x = -pos_x
            pos_y = -pos_y
            tile_id = self._atQ_xy_to_tile[(pos_x, pos_y)]
        elif qrx == 'r':
            pos_x = corner_x - (self._sector_width - 1)
            pos_y = corner_y - 0
            pos_x = -pos_x
            pos_y = -pos_y
            tile_id = self._atR_xy_to_tile[(pos_x, pos_y)]

        tile_id = tile_id + tile_id_offset

        return tile_id

    def get_tile_id_offset_top_left(self, x, y):
        offset_x = x - int((self._fass_order()*self._sector_width) / 2)
        offset_y = y - int((self._fass_order()*self._sector_width) / 2)
        return self.get_tile_id(offset_x, offset_y)

    def get_grid_size(self):
        return (self._fass_order()*self._sector_width) ** 2

    def get_last_tile(self):
        return (self._fass_order() * 9) ** 2 - 1

    def get_grid_corners(self):
        max_tile = int(self._fass_order() * 9 / 2)
        return (-max_tile, -max_tile, max_tile, max_tile)