"""Operators of the N-Key-Panel"""
#
# The operators of the N-Key-Panel.
#
# Copyright (c) 2021 Keith Pinson

import bpy
from bpy.types import Operator

from bpy.props import (
    PointerProperty, StringProperty, IntProperty, BoolProperty, EnumProperty)


class CVB_OT_NewSketch(Operator):
    # pylint: disable=invalid-name
    """New Sketch Button"""
    bl_idname = 'object.new_sketch_button'
    bl_label = 'New'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = """Add a new City Map Sketch"""

    def execute(self, context):
        # Make a new sketch
        bpy.ops.mesh.primitive_plane_add(size=50)

        return {"FINISHED"}


class CVB_OT_EditCityName(Operator):
    # pylint: disable=invalid-name
    """New Sketch Button"""
    # bl_property = "text_prop"  # Focus
    bl_idname = 'entry.city_name_field'
    bl_label = ""
    # bl_options = {"REGISTER", "UNDO"}
    bl_options = {"UNDO"}
    bl_description = """A shorter version of the city name"""

    test_data: StringProperty(
        name="",
        description="""Recommended city filename""",
        default="ttt Cityvilleburg")


    # city_name_text = bpy.props.StringProperty(
    #     name="City Name Here",
    #     description="The name of the city",
    #     default="city")

    # def __init__(self):
    #     print("__init__()")
    #
    # def __del__(self):
    #     print("__del__()")

    # def draw(self, context): We do not want to override this definition

    def execute(self, context):
        print("execute()")
        print(dir(self))
        print()
        print(self.properties)
        print()
        print(self.properties.test_data)
        # print()
        # print(dir(context))
        #
        # self.report({'INFO'}, "Mouse coords are %d %d" % (self.x, self.y))

        city_name_text = bpy.props.StringProperty(
            name="City Name Here",
            description="The name of the city",
            default="city")

        if self.layout != None:
            self.layout.label(text="test")

        return {"FINISHED"}

    # def invoke(self, context, event):
    #     print("invoke()")
    #
    #     # context.window_manager.modal_handler_add(self)
    #     # bpy.context.area.type = "TEXT_EDITOR"
    #     #
    #     # return {'RUNNING_MODAL'}
    #
    #     # self.x = event.mouse_x
    #     # self.y = event.mouse_y
    #     # return self.execute(context)
    #
    #     # wm = context.window_manager
    #     # return wm.invoke_props_dialog(self)
    #
    #     return {"RUNNING_MODAL"}

        # return {"FINISHED"}

    # def modal(self, context, event):
    #     # print("modal()")
    #
    #     if event.type == 'MOUSEMOVE':
    #         self.execute(context)
    #     elif event.type == 'LEFTMOUSE':
    #         print("modal()", event.type)
    #         return {'FINISHED'}
    #     elif event.type in {'RIGHTMOUSE', 'ESC'}:
    #         print("modal()", event.type)
    #         return {'CANCELLED'}
    #
    #     # return {'PASS_THROUGH'}
    #     return {'RUNNING_MODAL'}

    # @classmethod
    # def poll(cls, context):
    #     ob = context.active_object
    #     return ((ob is not None) and (ob.mode == "OBJECT") and
    #             (ob.type == "MESH") and (context.mode == "OBJECT"))

    # @classmethod
    # def poll(cls, context):
    #     return (context.active_object is not None) and (context.active_object.mode != 'EDIT')



