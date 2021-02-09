"""city Generator N-Key-Panel """
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
    bl_label = ''  # Leave blank and use draw_header()
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CVB'
    bl_order = 1

    def draw_header(self, context):
        layout = self.layout
        header_row = layout.column()
        header_row.alignment = 'CENTER'
        header_row.use_property_decorate = True
        header_row.prop(context.scene.CVB, "city_filename_prop", text="", emboss=False)


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
    #       Sketch Options:
    #
    #           (C) City Name Drop-Down Box
    #
    #               - City names are displayed
    #
    #               - Drop down is disabled if no city names
    #
    #               - If city name is selected seed, type, size are updated
    #
    #           (D) City Name Field
    #
    #               - Default city name is "City" <seed> "_" <type> <size> <tile> <variant>
    #
    #                 Where:
    #                       <seed> is integer
    #                       <type> is 1 letter
    #                       <size> is X km integer, "x", Y km integer and for values less than 1 km
    #                                               meter integers followed by "m"
    #                       <tile> is optional 5 decimal, leading zero integer, preceded by "-"
    #                       Optional <variant> is "." followed by 3 decimal incremental integer
    #
    #               - Editing name is disabled if no seed,type,size match
    #
    #           (E) New Button
    #
    #               - Displayed name is added to City Names
    #
    #               - Name field is enabled and can be changed
    #
    #               - No variant until sketch itself is edited
    #
    #           (F) Seed: A number used to make a reproducible random sketch
    #
    #               - Integer: 1 to 2^15-1
    #               - Back/Next Stepper Buttons
    #
    #           (G) Map Style Drop down
    #
    #               "g" Chicago Grid    (A city map modeled after the American grid system)
    #               "s" Cyber Scrapers  (A city map modeled on the if you can't build out, build up)
    #               "h" Dodge 1880      (A town map with a main street)
    #               "c" Nordingenton    (A layout from years ago when cities formed inside a defensive wall)
    #
    #           (H) Map X: Size and Y: Size (in meter integers)
    #
    #           (I) Hide sketch Checkbox
    #
    #           (J) Scale sketch Checkbox
    #
    #               - Toggle between the Map X,Y size and a proportion equivalent of the
    #                 shortest dimension to 10 Meters
    #
    #           (K) Farm Tile Id Checkbox
    #
    #               - Sequential positive decimal number starting with zero
    #
    #               - Display tile distance in positive/negative, x and y offsets from tile zero
    #
    #               - Change Map to be square

    # (L) Generate city Group Box
    #     -----------------------
    #
    #   (M) Generate city Button

    def draw(self, context):
        cvb = context.scene.CVB

        panel_column = self.layout

        # (A) New Map Group Box
        new_map_group_box = panel_column.box()

        # (B) New Map Button
        new_map_button = new_map_group_box.row(align=True)
        new_map_button.scale_y = 1.3
        new_map_button.operator("object.new_map",
                                text="New Map",
                                icon_value=cvb_icon(context, "icon-new-map-l"))

        are_cities_in_list = len(cvb.sketch_name_list) > 0

        # New Map Options Box
        new_map_button_options = new_map_group_box.box()

        #       city Name Entry Row
        city_name_entry = new_map_button_options.row(align=True).box().row()

        #           (C) city Name Drop Down
        city_name_dropdown = city_name_entry.column().split(factor=0.25)
        city_name_dropdown.enabled = are_cities_in_list
        city_name_dropdown.prop(cvb, "sketch_name_prop", text="", icon_only=True, icon='MESH_GRID')

        #           (D) city Name Field
        city_name_field = city_name_entry.column()
        # city_name_field.enabled = False
        city_name_field.prop(cvb, "city_name_field_prop", text="")

        #           (E) "+" button
        city_name_plus_button = city_name_entry.column()
        city_name_plus_button.operator("object.new_sketch", text="", icon='ADD')

        #       (F) Seed
        # TODO: Set the seed value in the add-on preferences too
        # seed = cvb_prefs(context).cvb_seed
        seed_stepper = new_map_button_options.row(align=True)
        seed_stepper.prop(cvb, "seed_prop", text="Seed")

        #       (G) Map Style Drop Down
        map_style_dropdown = new_map_button_options.row(align=True)
        map_style_dropdown.prop(cvb, "sketch_style_prop", text="Style")

        #       (H) Map X,Y
        sketch_x_y = new_map_button_options.row(align=True)
        if cvb.using_tile_id_prop:
            sketch_x_y.prop(cvb, "sketch_xy_linked_prop", text="X")
            sketch_x_y.label(text="", icon='LINKED')
            sketch_x_y.prop(cvb, "sketch_xy_linked_prop", text="Y")
        else:
            sketch_x_y.prop(cvb, "sketch_x_prop", text="X")
            sketch_x_y.prop(cvb, "sketch_y_prop", text="Y")

        #       Hide/Scale Row
        hide_scale_row = new_map_button_options.row(align=True)

        #       (I) Hide sketch
        hide_sketch_checkbox = hide_scale_row.column()

        hide_sketch_checkbox.enabled = are_cities_in_list
        hide_sketch_checkbox.prop(cvb, "sketch_visible_prop", text="Show Sketch?")

        #       (J) Scale sketch
        # TODO: Either use the cast modifier or geometry nodes in 2.92

        #       (K) Farm? and Tile Id
        tile_id_box = new_map_button_options.row(align=True).box()

        tile_id_row = tile_id_box.row(align=True)

        render_farm_checkbox = tile_id_row.column()
        render_farm_checkbox.prop(cvb, "using_tile_id_prop", text="Multi tile?")

        if cvb.using_tile_id_prop:
            tile_position = tile_id_row.column()
            tile_position.enabled = False
            tile_position.prop(cvb, "tile_position_prop", text="")

        if cvb.using_tile_id_prop:
            tile_id_stepper = tile_id_box.row(align=True)
            tile_id_stepper.prop(cvb, "tile_id_prop", text="Tile #")


        # (L) Generate city Group Box
        generate_city_group_box = panel_column.box()

        # (M) Generate city Button
        generate_city_button = generate_city_group_box.row(align=True)
        generate_city_button.scale_y = 1.3
        generate_city_button.operator("object.gen_city",
                                      text="Generate city",
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
    """Generate city Button"""
    bl_idname = 'object.gen_city'
    bl_label = 'Generate city'
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
