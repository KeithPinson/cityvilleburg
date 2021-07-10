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
#      and things like a long ridge should continue across tiles
#


class fassGrid:

    _default_order = 11
    _sector_width = 9  # Sectors are square
    _xy_to_sector, _sector_to_xy, _sector_to_qrx = None, None, None

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

    # The L-System his highly recursive, instead we will loop and make dictionaries to translate positions
    def _cvb_qr_loop(self, soft_order):
        """Return: xy_to_tile, tile_to_xy, tile_to_qrx"""

        n = 0
        d = ""
        c = 'N'
        pos = (0, 0)
        w = {(0, 0): 0}  # xy_to_sector
        u = {0: (0, 0)}  # sector_to_xy
        v = {0: "X"}     # sector_to_qrx

        def move(direction, position):
            pos = position

            if direction is 'N':
                pos = (position[0], position[1] - 1)
            elif direction is 'S':
                pos = (position[0], position[1] + 1)
            elif direction is 'W':
                pos = (position[0] - 1, position[1])
            elif direction is 'E':
                pos = (position[0] + 1, position[1])

            return pos

        def turn(leftright, direction):
            c = direction

            if direction is 'N':
                c = 'E' if leftright is '-' else 'W'
            elif direction is 'S':
                c = 'E' if leftright is '+' else 'W'
            elif direction is 'W':
                c = 'N' if leftright is '-' else 'S'
            elif direction is 'E':
                c = 'N' if leftright is '+' else 'S'

            return c

        for i in range(0, soft_order):
            if i is 0:
                n = 0
                d = "X"
                c = 'N'
                w = {(0, 0): 0}
                u = {0: (0, 0)}
                v = {0: "X"}
                pos = move(c, pos)
                n += 1
                c = turn('-', c)
            else:
                for j in range(i + 1):
                    d = "r" if (i % 2) == 0 else "R"
                    w[pos] = n
                    u[n] = pos
                    v[n] = d

                    if j < i:
                        pos = move(c, pos)
                        n += 1
                    else:
                        c = turn('-', c)
                        pos = move(c, pos)
                        n += 1

                for _ in range(i):
                    d = "Q" if (i % 2) == 0 else "q"
                    w[pos] = n
                    u[n] = pos
                    v[n] = d

                    pos = move(c, pos)
                    n += 1
                c = turn('-', c)

        return w, u, v

    def _fass_order(self):
        return cvb_prefs(bpy.context).cvb_terrain_region_order if cvb_prefs(bpy.context) else self._default_order

    def __init__(self):
        (self._xy_to_sector, self._sector_to_xy, self._sector_to_qrx) = self._cvb_qr_loop(self._fass_order())

    def _get_sector_from_top_left(self, x, y):
        result = -1

        # fassOrderWidth = 9
        #
        # width = (fassOfOrder)*fassOrderWidth
        # maxTile = width * width
        #
        # if tileNumber >= maxTile:
        #     return result

        return -1

    def _get_sector_xy(self, tile_id):
        sector_id = int(tile_id  / self._sector_width**2)
        return self._sector_to_xy[sector_id]

    def get_tile_xy(self, tile_id):
        sector_x, sector_y = self._get_sector_xy(tile_id)

        # print("x,y", sector_x, ",", sector_y)

        return sector_x, sector_y

    def get_tile_id(self, x, y):
        pass

    def get_tile_id_from_top_left(self, x, y):
        pass

    def get_grid_size(self, x, y):
        pass

    def get_last_tile(self):
        return (self._fass_order() * 9) ** 2 - 1

    def get_grid_corners(self):
        max_tile = int(self._fass_order() * 9 / 2)
        return (-max_tile, -max_tile, max_tile, max_tile)