"""City Generator N-Key-Panel """
#
# The main interface to the city generator. This is
# where the buttons and controls are to sketch the
# city map, create the map, and generate the city are.
#
# The panel properties can be found in the
# bpy.context.scene.CVB object.
#
# After registering, the panels will be inserted automatically
# as specified by the bl_category and bl_order.
#
#   The N-panel has the following hierarchical outline:
#
#       Cityvileburg
#       ------------
#
#       (i) New Map
#
#           (1) City Sketch Settings
#
#               (A) Sketch Generate
#               (B) Sketch Select
#               (C) City Name
#               (D) Seed
#               (E) City Style
#               (F) Tile Size
#
#           (2) Display Controls
#
#               (G) Show Sketch
#               (H) Show Miniature size
#               (I) Tile ID
#
#           (3) Sketch Edit
#
#           (4) Terrain Edit
#
#       (ii) Generate City
#
#       Help
#       ----
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import Panel, Operator
from ..addon.preferences import cvb_icon, cvb_prefs
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

    #   Cities are composed of multiple layers:
    #
    #       - Sketch
    #       - Map
    #       - Terrain
    #       - City
    #
    #   A sketch is used to make a map. A map and terrain combine to make a city.
    #   Changes to any one layer can have affect layers above and below.
    #
    #       Sketch -> Map, Map + Terrain -> City
    #
    #   Additionally, maps are broken up so that they can be worked on and rendered
    #   in sizes that are manageable, these are referred to as tiles and the array of tiles
    #   is the grid. The default tile size is 1000 by 1000 meters and the default grid size
    #   is 99 by 99 tiles.
    #
    def draw(self, context):   # <== This is the Roman Numeral level; break everything into the respective hierarchy
        """Draw the main N-key panel either normally or for imports"""

        #
        # This is called everytime the mouse enters an element's border
        #

        cvb = context.scene.CVB

        panel_column = self.layout

        new_map_group_box = panel_column.box()

        # (i) New Map
        self.draw_new_map_button(context, new_map_group_box)

        #     (1) City Sketch Settings
        new_map_button_options = new_map_group_box.box()

        if len(cvb.import_name_prop) > 0:
            self.draw_city_sketch_settings_for_imports(context, new_map_button_options)
        else:
            self.draw_city_sketch_settings(context, new_map_button_options)

        #     (2) Display Controls
        self.draw_display_controls(context, new_map_group_box.box())

        edit_buttons = new_map_group_box.box()
        edit_buttons_row = edit_buttons.row(align=True)

        #     (3) Sketch Edit
        self.draw_city_sketch_button(context, edit_buttons_row)

        #     (4) Terrain Edit
        self.draw_terrain_edit_button(context, edit_buttons_row)

        # (ii) Generate City
        self.draw_generate_city_button(context, panel_column.box())

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
    #       (L) Sketch Edit
    #       (M) Terrain Edit

    #           (1) City Sketch Settings
    #
    #               (A) Sketch Generate
    #               (B) Sketch Select
    #               (C) City Name
    #               (D) Seed
    #               (E) City Style
    #               (F) Tile Size
    #

    def draw_city_sketch_settings(self, context, layout):
        # pylint: disable=too-many-locals
        """Draw the main N-key panel"""

        cvb = context.scene.CVB

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
    def draw_city_sketch_settings_for_imports(self, context, layout):
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

    #           (2) Display Controls
    #
    #               (G) Show Sketch
    #               (H) Show Miniature size
    #               (I) Tile ID
    #
    #           (3) Sketch Edit
    #
    #           (4) Terrain Edit

    def draw_generate_city_button(self, context, layout):
        """Draw the Generate City Button"""

        generate_city_button = layout.row(align=True)
        generate_city_button.scale_y = 1.3
        generate_city_button.operator("cvb.gen_city_button",
                                      text="Generate city",
                                      icon_value=cvb_icon(context, "icon-gen-city-l"))

    def draw_new_map_button(self, context, layout):
        """Draw the New Map Button"""

        new_map_button = layout.row(align=True)
        new_map_button.scale_y = 1.3
        new_map_button.operator("cvb.new_map_button",
                                text="New Map",
                                icon_value=cvb_icon(context, "icon-new-map-l"))

    def draw_display_controls(self, context, layout):
        """Draw the Display Controls"""

        cvb = context.scene.CVB

        are_sketches_in_list = not is_sketch_list_empty()

        #       Hide/Scale Row
        hide_scale_row = layout.row(align=True).column().split(factor=0.66)

        #       (I) Hide sketch
        hide_sketch_checkbox = hide_scale_row

        hide_sketch_checkbox.enabled = are_sketches_in_list
        hide_sketch_checkbox.prop(cvb, "sketch_visible_prop", text="Show Sketch?")

        #       (J) Scale sketch
        scale_sketch_checkbox = hide_scale_row

        scale_sketch_checkbox.enabled = are_sketches_in_list
        scale_sketch_checkbox.prop(cvb, "sketch_minimized_prop", text="Mini?")

        #       (K) Tile Id
        tile_id_box = layout.row(align=True).box()

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



    def draw_city_sketch_button(self, context, layout):
        """Draw the Sketch Edit Button"""

        cvb = context.scene.CVB

        sketch_edit_button = layout.row(align=True)
        sketch_edit_button.scale_y = 1.1
        # sketch_edit_button.prop(cvb, "visible_city_sketch_prop", text="")
        sketch_edit_button.operator("cvb.sketch_edit_button",
                                    text="City Sketch",
                                    depress=cvb.visible_city_sketch_prop)

    def draw_terrain_edit_button(self, context, layout):
        """Draw the Terrain Edit Button"""

        cvb = context.scene.CVB

        terrain_edit_button = layout.row(align=True)
        terrain_edit_button.scale_y = 1.1
        terrain_edit_button.operator("cvb.terrain_edit_button",
                                     text="Terrain",
                                     depress=cvb.visible_terrain_editor_prop)


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


class CVB_OT_SketchEditButton(Operator):
    # pylint: disable=invalid-name
    """City Sketch Button"""
    bl_idname = 'cvb.sketch_edit_button'
    bl_label = 'City Sketch'
    bl_options = {"INTERNAL"}
    bl_description = """Edit the city sketch"""

    def execute(self, context):

        cvb = context.scene.CVB

        cvb.visible_city_sketch_prop = not cvb.visible_city_sketch_prop

        if cvb.visible_city_sketch_prop:
            cvb.visible_terrain_editor_prop = False

        print("city/terrain:", cvb.visible_city_sketch_prop, cvb.visible_terrain_editor_prop)

        if cvb.visible_city_sketch_prop:
            return {"RUNNING_MODAL"}
        else:
            return {"FINISHED"}


class CVB_OT_TerrainEditButton(Operator):
    # pylint: disable=invalid-name
    """Terrain Edit Button"""
    bl_idname = 'cvb.terrain_edit_button'
    bl_label = 'Terrain Edit'
    bl_options = {"INTERNAL"}
    bl_description = """Edit the terrain"""

    def execute(self, context):

        cvb = context.scene.CVB

        cvb.visible_terrain_editor_prop = not cvb.visible_terrain_editor_prop

        if cvb.visible_terrain_editor_prop:
            cvb.visible_city_sketch_prop = False

        print("city/terrain:", cvb.visible_city_sketch_prop, cvb.visible_terrain_editor_prop)

        if cvb.visible_terrain_editor_prop:
            return {"RUNNING_MODAL"}
        else:
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
