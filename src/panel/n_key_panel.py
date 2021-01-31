"""City Generator N-Key-Panel """
#
# The main interface to the city generator. This is
# where the buttons and controls are to sketch the
# city map, create the map, and generate the city are.
#
# The panel properties can be found in the
# bpy.context.scene.CVB object.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import Panel, Operator
from ..addon.preferences import cvb_icon


#         column = layout.column(align=True)
#         column.separator()


class CVB_PT_Main(Panel):
    # pylint: disable=invalid-name
    """Main Panel of the N-Key Panels"""
    bl_label = 'Cityvilleburg'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CVB'
    bl_order = 1

    # (A) New Map Group Box
    #     -----------------
    #
    #   Cities are composed of multiple layers:
    #
    #       (1) Sketch
    #       (2) Map
    #       (3) Terrain
    #       (4) City
    #
    #   A sketch is used to make a map. A map and terrain combine to make a city.
    #   Cities which are composed of many parts can be manipulated to effect the
    #   map and the terrain. And, changing the map, changes the sketch.
    #
    #   (B) New Map Button  (doubles as section title)
    #
    #       (C) Seed: A number used to make a reproducible random sketch
    #
    #           (D) Back/Next Stepper Buttons
    #
    #           (E) A "+ New" or City Name Drop-Down Box
    #
    #               - Pressing "+ New" defaults to the word "City_" prepended to the
    #                 seed number, followed by decimal in the usual Blender fashion,
    #                 eg. "City_1.001"
    #
    #               - "+ New" Should remain an option to select in the drop down box
    #
    #               - Selecting a name should change the seed number displayed in (C)
    #
    #               - After "+ New" is pressed the complete random sketch be drawn
    #
    #       (F) Hide sketch Checkbox
    #
    #       (G) Map X: Number and Y: Number
    #
    #       (H) Map Style Drop down
    #
    #           Chicago Grid    (A city map modeled after the American grid system)
    #           Cyber Scrapers  (A city map modeled on the if you can't build out, build up)
    #           Dodge 1880      (A town map with a main street)
    #           Nordingenton    (A layout from years ago when cities formed inside a defensive wall)

    # (L) Generate City Group Box
    #     -----------------------
    #
    #   (M) Generate City Button

    def draw(self, context):
        cvb = context.scene.CVB

        panel_column = self.layout

        # (A) New Map Group Box
        new_map_group_box = panel_column.box()

        # (B) New Map Button
        new_map_button = new_map_group_box.row(align=True)
        new_map_button.operator("object.new_map",
                                text="New Map",
                                icon_value=cvb_icon(context, "icon-new-map-l"))

        new_map_button_options = new_map_group_box.box()

        # (C) Seed
        # TODO: Set the seed value in the add-on preferences too
        # seed = cvb_prefs(context).cvb_seed
        seed_stepper = new_map_button_options.row(align=True)

        #       (D) Back/Next (handled by Blender by default)
        seed_stepper.prop(cvb, "seed_prop", text="Seed")

        #       (E) City Name Drop Down
        city_name_dropdown = new_map_button_options.row(align=True)
        city_name_dropdown.prop(cvb, "sketch_name_prop", text="Sketch")

        #       (F) Hide sketch
        hide_sketch_checkbox = new_map_button_options.row(align=True)

        are_cities_in_list = len(cvb.sketch_name_list) > 1
        hide_sketch_checkbox.enabled = are_cities_in_list
        hide_sketch_checkbox.prop(cvb, "sketch_visible_prop", text="Show Sketch?")

        #       (G) Map X,Y
        sketch_x_y = new_map_button_options.row(align=True)
        sketch_x_y.prop(cvb, "sketch_x_prop", text="X")
        sketch_x_y.prop(cvb, "sketch_y_prop", text="Y")

        #       (H) Map Style Drop Down
        map_style_dropdown = new_map_button_options.row(align=True)
        map_style_dropdown.prop(cvb, "sketch_style_prop", text="Style")

        # (L) New Map Group Box
        box = self.layout.box()

        # (M) Generate City Button
        row = box.row(align=True)
        row.operator("object.gen_city",
                     text="Generate City",
                     icon_value=cvb_icon(context, "icon-gen-city-l"))


class CVB_PT_Help(Panel):
    # pylint: disable=invalid-name
    """Help Panel of the N-Key Panels"""
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
    # pylint: disable=invalid-name
    """New Map Button"""
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
    # pylint: disable=invalid-name
    """Generate City Button"""
    bl_idname = 'object.gen_city'
    bl_label = 'Generate City'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = """Generate city from map"""

    def execute(self, context):
        # Generate the city
        bpy.ops.mesh.primitive_cube_add()

        return {"FINISHED"}


class CVB_OT_GettingStartedHelp(Operator):
    # pylint: disable=invalid-name
    """Help Operator"""
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
