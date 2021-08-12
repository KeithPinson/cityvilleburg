#
# Terrain is of two types: the Tile (local) terrain and the Region
# terrain. Typically a tile represents a 1x1 km square and a Region
# maybe 100x100 km in proportion. A compressed heightmap would be
# pushing a gigabyte in size to adequately represent the Region
# terrain. For that reason we don't use a raster-based solution to
# represent regional terrain.
#
# This package contains the modules to support Region and Tile
# terrains.
#
# Copyright (c) 2021 Keith Pinson