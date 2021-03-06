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
from .citysketchname_props import is_sketch_list_empty


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
        self.layout.label(text=context.scene.CVB.city_props.city_panel_header_prop)

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
    #   Changes to any layer can have affects up and down the layers. Cities which
    #   are composed of many parts can be manipulated to effect the map and the
    #   terrain. And, changing the map, changes the sketch.
    #
    #   (B) New Map Button  (doubles as section title)
    #
    #       Sketch Options: draw_n_panel()
    #       -or-
    #       Import Option: draw_n_panel_for_imports()
    #
    # (L) Generate city Group Box
    #     -----------------------
    #
    #   (M) Generate city Button

    def draw(self, context):
        """Draw the main N-key panel either normally or for imports"""

        #
        # This is called everytime the mouse enter an element's border
        #

        cvb = context.scene.CVB

        panel_column = self.layout

        # (A) New Map Group Box
        new_map_group_box = panel_column.box()

        # (B) New Map Button
        new_map_button = new_map_group_box.row(align=True)
        new_map_button.scale_y = 1.3
        new_map_button.operator("cvb.new_map_button",
                                text="New Map",
                                icon_value=cvb_icon(context, "icon-new-map-l"))

        # New Map Options Box
        new_map_button_options = new_map_group_box.box()

        if len(cvb.import_name_prop) > 0:
            self.draw_n_panel_for_imports(context, new_map_button_options)
        else:
            self.draw_n_panel(context, new_map_button_options)

        # (L) Generate city Group Box
        generate_city_group_box = panel_column.box()

        # (M) Generate city Button
        generate_city_button = generate_city_group_box.row(align=True)
        generate_city_button.scale_y = 1.3
        generate_city_button.operator("cvb.gen_city_button",
                                      text="Generate city",
                                      icon_value=cvb_icon(context, "icon-gen-city-l"))

        cvb.city_props.refresh_sketch_name(cvb)

    #
    #  Sketch Options:
    #
    #      (C) City Name Entry Field
    #
    #          - City Name as a simple string without the seed, size and other
    #            parameter. It is editable.
    #
    #          - It must be filename compatible
    #
    #      (D) New Button
    #
    #          - Displayed name is added to City Names
    #
    #          - Name field is enabled and can be changed
    #
    #          - No variant until sketch itself is edited
    #
    #      (E) Sketch Name Drop-Down Box
    #
    #          - Sketch names are displayed
    #
    #          - Drop down is disabled if no sketches available
    #
    #          - If a sketch name is selected then city, seed, type, size are updated
    #
    #          - Sketch name is <city> <seed> "_" <type> <size> <tile> <variant>
    #
    #            Where:
    #                  <city> is a filename compatible string in addition:
    #                         no underscores, no spaces, and not quoted
    #                  <seed> is integer
    #                  <type> is 1 letter
    #                  <size> is XxY, where X and Y are kilometers expressed as integers,
    #                         or for values less than 1 km, meters express as integers
    #                         followed by the letter "m"
    #                  <tile> is optional 5 decimal, leading zero integer, preceded by "-"
    #                  <variant> is "." followed by 3 decimal incremental integer starting
    #                            with 001
    #
    #          - Editing name is disabled if no seed,type,size match
    #
    #      (F) Seed: A number used to make a reproducible random sketch
    #
    #          - Integer: 1 to 2^15-1
    #          - Back/Next Stepper Buttons
    #
    #      (G) Map Style Drop down
    #
    #          'grid'
    #              Grid Plan City
    #              (A city map modeled after the planned grid system)
    #          'medieval'
    #              Medieval City Style
    #              (A layout from years ago when cities formed inside a defensive wall)
    #          'skyscrapers'
    #              Skyscraper City Style
    #              (A city map modeled on the if you can't build out, build up)
    #          'western'
    #              Western City Style
    #              (A town built along a thoroughfare; water, rail, or road)
    #
    #      (H) Map X: Size and Y: Size (in meter integers)
    #
    #      (I) Hide sketch Checkbox
    #
    #      (J) Scale sketch Checkbox
    #
    #          - Toggle between the Map X,Y size and a proportion equivalent of the
    #            shortest dimension to 10 Meters
    #
    #      (K) Tile Id Checkbox
    #
    #          - Sequential positive decimal number starting with zero
    #
    #          - Display tile distance in positive/negative, x and y offsets from tile zero
    #
    #          - Change Map to be square
    #

    def draw_n_panel(self, context, layout):
        # pylint: disable=too-many-locals
        """Draw the main N-key panel"""

        cvb = context.scene.CVB

        are_sketches_in_list = not is_sketch_list_empty()

        new_map_button_options = layout

        #       city Name Entry Row
        city_name_entry = new_map_button_options.row(align=True).box()

        #           (C) City Name Field
        city_name_field = city_name_entry.row(align=True)
        city_name_field.prop(cvb.city_props, "city_name_prop", text="")

        #           (D) "+" button
        city_name_plus_button = city_name_field.split()
        city_name_plus_button.operator("cvb.new_sketch_button", text="", icon='ADD')

        #       (E) Sketch Name Dropdown
        # Current programmatic control is limited so deconstruct the dropdown
        sketch_name_entry = new_map_button_options.row(align=True)
        sketch_name_field = sketch_name_entry.row(align=True)  # The sketch name
        sketch_name_field.prop(cvb.city_props, "sketch_name_prop", text="", emboss=True)

        sketch_name_dropdown = sketch_name_field  # The sketch names dropdown
        sketch_name_dropdown.enabled = True  # There will always be something in the list
        sketch_name_dropdown.prop(
            cvb.city_props,
            "sketch_name_enum_prop",
            text="",
            icon_only=True,
            icon='MESH_GRID')

        #       (F) Seed
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

        hide_sketch_checkbox.enabled = are_sketches_in_list
        hide_sketch_checkbox.prop(cvb, "sketch_visible_prop", text="Show Sketch?")

        #       (J) Scale sketch
        # TODO: Either use the cast modifier or geometry nodes in 2.92

        #       (K) Tile Id
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

        cvb.city_props.refresh_sketch_name(cvb)

    #
    #  Import Options:
    #
    #      (E) Sketch Name Drop-Down Box
    #
    #          - Sketch names are displayed as well as imports
    #
    #          - Import name is displayed as the selected enumerator
    #
    def draw_n_panel_for_imports(self, context, layout):
        """Draw the main N-key panel for imports"""

        cvb = context.scene.CVB

        #       (E) Sketch Name Dropdown
        # Current programmatic control is limited so deconstruct the dropdown
        import_name_entry = layout.row(align=True)
        import_name_field = import_name_entry.row(align=True)  # The sketch name
        import_name_field.prop(cvb, "import_name_prop", text="", emboss=False)

        sketch_name_dropdown = import_name_field  # The sketch names dropdown
        sketch_name_dropdown.enabled = True  # There will always be something in the list
        sketch_name_dropdown.prop(
            cvb.city_props,
            "sketch_name_enum_prop",
            text="",
            icon_only=True,
            icon='MESH_GRID')


class CVB_PT_Help(Panel):
    # pylint: disable=invalid-name
    """Help Panel of the N-Key Panels"""
    bl_label = 'Help'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CVB'
    bl_order = 99

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
        self.layout.operator("cvb.getting_started_help",
                             text="Getting Started",
                             icon='HELP')


class CVB_OT_NewMapButton(Operator):
    # pylint: disable=invalid-name
    """New Map Button"""
    bl_idname = 'cvb.new_map_button'
    bl_label = 'New Map'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = """Create a new city map"""

    def execute(self, context):
        # if previous map layers
        # if( False ):
        #     pass  # Hide the previous layers

        # Create the new map
        bpy.ops.mesh.primitive_cube_add()

        return {"FINISHED"}


class CVB_OT_GenCityButton(Operator):
    # pylint: disable=invalid-name
    """Generate city Button"""
    bl_idname = 'cvb.gen_city_button'
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
    bl_idname = 'cvb.getting_started_help'
    bl_label = 'Help Getting Started'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = """Help with Cityvilleburg"""

    def execute(self, context):
        # if previous map layers
        # if( False ):
        #     pass  # Hide the previous layers

        # Create the new map
        bpy.ops.mesh.primitive_cube_add()

        return {"FINISHED"}
