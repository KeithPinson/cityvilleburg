#
# Helper to collect and display icons in Blender.
#
# Copyright (c) 2021 Keith Pinson

import os
import pathlib
import bpy


class IconCollection:
    icons_collection = None
    file_dir = os.path.dirname(__file__)
    icons_dir = pathlib.Path(file_dir).parent.parent.joinpath('res')

    def __init__(self):
        self.icons_collection = bpy.utils.previews.new()

    def __del__(self):
        if self.icons_collection is not None:
            bpy.utils.previews.remove(self.icons_collection)

    def get_icon_id(self, name):
        found_icon = self.get_icon(name)

        if found_icon.icon_size[0] == 0:
            print("Icon file not found: ", name)

        return found_icon.icon_id

    def get_icon(self, name):
        if name in self.icons_collection:
            return self.icons_collection[name]

        return self.icons_collection.load(name, os.path.join(self.icons_dir, name + ".png"), "IMAGE")
