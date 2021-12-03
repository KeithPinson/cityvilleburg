"""Routines for creating and finding objects used by CVB"""
# pylint: disable=line-too-long
#
# All interactions with the Blender Objects should be
# done through these routines.
#
# Structurally Collections and Objects are tight coupled
# and maybe it might be better to combine the collection
# and object utils into a single module, but for now because
# they have separate concerns, we will keep them separate.
#
# Specifically Collections will be concerned with navigating
# the tree structure and Objects will be concerned with
# creation and manipulation of the Blender Objects.
#
# Requirements:
#
# 1. Be able to identify the CVB object (even if crudely by
#    using the name)
# 2. No navigating the Blender tree hierarchy, leave that for
#    the collection_utils
#
# Copyright (c) 2021 Keith Pinson
# pylint: enable=line-too-long

import bpy

from .collection_utils import collection_tail, collection_objects, path_object


def object_add(collection_path, object_name, blender_object):
    """Add the object to the collections"""
    added_object = bpy.data.objects.get(object_name)

    if added_object:
        print("Object already added:", object_name)
        # if obj and obj.type == 'MESH':
        #     bpy.context.view_layer.objects.active = obj
        #     bpy.context.view_layer.objects.active.select_set(True)

    else:
        added_object = bpy.data.objects.new(object_name, blender_object)

        if added_object:
            coll = collection_tail(collection_path)
            coll.objects.link(added_object)

    return added_object


def object_add_material(blender_object, material_name, material_color, metallic, roughness):
    """Add a material if it is not found with viewport color, metallic, and roughness"""
    mat = bpy.data.materials.get(material_name)

    if mat is None:
        mat = bpy.data.materials.new(name=material_name)

    if mat is not None:
        mat.diffuse_color = material_color
        mat.metallic = metallic
        mat.roughness = roughness

        if blender_object.data.materials:
            # Overwrite first material
            blender_object.data.materials[0] = mat
        else:
            blender_object.data.materials.append(mat)

    return mat


def object_get(object_path_and_name):
    """Return the object if found"""
    object_found = path_object(object_path_and_name)

    return object_found


def object_get_or_add_empty(collection_path, empty_name, radius=1.0, display_type='PLAIN_AXES'):
    """Get or add the empty wanted"""

    empty_object = bpy.data.objects.get(empty_name)

    if not empty_object:
        empty_object = bpy.data.objects.new(empty_name, None)

        if empty_object:
            coll = collection_tail(collection_path)
            coll.objects.link(empty_object)
            empty_object.empty_display_size = radius
            empty_object.empty_display_type = display_type

    return empty_object


def object_make_active(object_path_and_name):

    # Clear the selections
    for obj in bpy.data.objects:
        obj.select_set(False)

    obj = object_get(object_path_and_name)

    if obj and obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        bpy.context.view_layer.objects.active.select_set(True)

    return obj


def object_parent_all(blender_object, collection_path_and_name):
    """Parent all child objects found at the path to the Blender object"""
    child_names = collection_objects(collection_path_and_name)

    if blender_object:
        for child_name in child_names:
            child_object = bpy.data.objects.get(child_name)

            if child_object:
                child_object.parent = blender_object
