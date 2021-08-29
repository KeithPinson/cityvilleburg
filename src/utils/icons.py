#
# Helper to collect and display icons in Blender.
#
# Copyright (c) 2021 Keith Pinson

import os
import pathlib
import bpy
import bpy.utils.previews


class IconCollection:
    icons_collection = None
    file_dir = os.path.dirname(__file__)
    icons_dir = pathlib.Path(file_dir).parent.parent.joinpath('assets')

    def __init__(self):
        self.icons_collection = bpy.utils.previews.new()  # ImagePreviewCollection

    def __del__(self):
        if self.icons_collection is not None:
            bpy.utils.previews.remove(self.icons_collection)

    def get_icon_id(self, name):
        found_icon = self.get_icon(name)

        if not found_icon or found_icon.icon_size[0] == 0:
            print("Icon file not found: ", name)
            return ''

        return found_icon.icon_id

    def get_icon(self, name):
        if name in self.icons_collection:
            return self.icons_collection[name]

        file_path = os.path.join(self.icons_dir, name)

        ext = None
        if os.path.isfile(file_path + ".png"):
            ext = ".png"
        elif os.path.isfile(file_path + ".jpg"):
            ext = ".jpg"
        # "svg" not supported

        preview = self.icons_collection.load(name, file_path + ext, "IMAGE") if ext else None

        return preview
