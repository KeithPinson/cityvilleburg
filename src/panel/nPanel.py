#
# The main interface to the city generator.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import Panel, Operator
from ..utils import icons
from ..addon.preferences import cvb_icon


#         column = layout.column(align=True)
#         column.separator()


class CVB_PT_Main(Panel):
    bl_label = 'Cityvilleburg'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CVB'
    bl_order = 1

    # (A) New Map Group Box
    #     -----------------
    #
    #   (B) New Map Button  (doubles as section title)
    #
    #       (C) Seed: Number
    #
    #           (D) Back/Next Stepper Buttons
    #           (E) Hide un-used maps Checkbox
    #
    #           [ The interface between this control and the map sketch is complex:
    #
    #               1. Gray out un-used map numbers
    #               2. By default there is no map drawing; checkboxes should grayed and
    #                  disabled if there is no map drawing; "+ New" should be displayed
    #                  for seed number
    #               3. If there is no map drawing and the "New Map" button is pressed,
    #                  then draw the map sketch from the random seed and then begin
    #                  the map generation process; checkboxes un-grayed
    #               3. Drawings that have been modified and cannot be
    #                  automatically regenerated are given a modified map number
    #               4. Changing the number should result in an immediate display
    #                  of the map drawing; if it is hidden it should be shown and
    #                  "Hide un-used" checkbox checked and "Hide Map Drawing" unchecked
    #           ]
    #
    #       (F) Hide Map Drawing Checkbox
    #
    #       (G) Map Max X: Number and Max Y: Number
    #
    #       (H) City Style Drop down
    #
    #           Chicago Grid  (A city modeled after the American grid system)
    #           Cybercity     (A city modeled on the if you can't build out, build up)
    #           Dodge         (A town with a main street)
    #           Nordingenton  (A hamlet, years ago built inside a defensive wall)

    # (L) Generate City Group Box
    #     -----------------------
    #
    #   (M) Generate City Button

    def draw(self, context):
        # TODO: Rescan the CVB layers so that we can gray-out controls appropriately

        # (A) New Map Group Box
        box = self.layout.box()

        # (B) New Map Button
        row = box.row(align=True)
        row.operator("object.new_map",
                     text="New Map",
                     icon_value=cvb_icon(context, "icon-new-map-l"))

        row = box.row(align=True)
        row.label(text="Seed:")
        # row.prop(cvb, 'cvb_new_map_seed', expand=False)

        # (L) New Map Group Box
        box = self.layout.box()

        # (M) Generate City Button
        row = box.row(align=True)
        row.operator("object.gen_city",
                     text="Generate City",
                     icon_value=cvb_icon(context, "icon-gen-city-l"))


class CVB_PT_Help(Panel):
    bl_label = 'Help'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CVB'
    bl_order = 99

    # TODO: Add a check to the preferences for this and also change preferences if closed
    # bl_options = {'DEFAULT_CLOSED'}

    # (V) Help Group Box
    #     --------------
    #
    #   (W) Video thumbnail
    #
    #       When playing standard controls pause, play, adjust volume, etc should be available
    #
    #   (X) HTML list of videos; clicking on item in list changes video in thumbnail; link to
    #       help page should be displayed
    #
    #   (Y) Button to online help

    def draw(self, context):
        self.layout.operator("object.help",
                             text="Getting Started",
                             icon='HELP')


class CVB_OT_NewMap(Operator):
    bl_idname = 'object.new_map'
    bl_label = 'New Map'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = """Create a new city map"""

    def execute(self, context):
        # TODO: Rescan the CVB layers so that can hide previous layers if necessary

        # if previous map layers
        # if( False ):
        #     pass  # Hide the previous layers

        # Create the new map
        bpy.ops.mesh.primitive_cube_add()

        return {"FINISHED"}


class CVB_OT_GenCity(Operator):
    bl_idname = 'object.gen_city'
    bl_label = 'Generate City'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = """Generate city from map"""

    def execute(self, context):
        # Generate the city
        bpy.ops.mesh.primitive_cube_add()

        return {"FINISHED"}


class CVB_OT_GettingStartedHelp(Operator):
    bl_idname = 'object.help'
    bl_label = 'Help Getting Started'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = """Help with Cityvilleburg"""

    def execute(self, context):
        # TODO: Rescan the CVB layers so that can hide previous layers if necessary

        # if previous map layers
        # if( False ):
        #     pass  # Hide the previous layers

        # Create the new map
        bpy.ops.mesh.primitive_cube_add()

        return {"FINISHED"}
