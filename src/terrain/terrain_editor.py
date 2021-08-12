"""Terrain Editor"""
#
# The Terrain Editor is a heads-up style display
# in the 3D Viewport. It is only one object; a plane,
# no ability to add anything but it can be modified.
# With special tools mountain ridges and rivers can
# be drawn and modified. When changes are made in
# the Terrain Editor they are echoed in the
# terrain mesh of the 3D Viewport.
#
# Copyright (c) 2021 Keith Pinson

class CVB_OT_SketchEditButton(Operator):
    # pylint: disable=invalid-name
    """City Sketch Button"""
    bl_idname = 'cvb.sketch_edit_button'
    bl_label = 'City Sketch'
    bl_options = {"INTERNAL"}
    bl_description = """Edit the city sketch"""

    def execute(self, context):

        cvb = context.scene.CVB




