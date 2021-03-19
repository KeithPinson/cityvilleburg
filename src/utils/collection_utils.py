"""Routines enforce a path system where collections are like
folders and objects are like files"""
#
# pylint: disable=line-too-long
#
# All interactions with the Blender collections should be
# done through these routines. Since collections and objects
# can be moved, renamed, or deleted, we use a path and file
# system where we treat collections as paths and objects as
# files.
#
# Blender's internal structure is peculiar enough that some
# explanation is necessary. A collection is not a tree that
# contains nodes, it is a node that contains trees (sort of).
#
# Every collection object has a "children" element which can
# contain more collections. It also has an "object" element
# which can contain objects. Collections and objects are what
# it collects, it also has flags for controlling ui features.
#
#   bpy.data.collections                                <== All collections are created (new) here.
#                                                           Name will be appended to if it already exists.
#
#   bpy.context.scene.collection.children               <== This is the root of the visible collection tree
#                                                           that can be seen in the Outliner.
#
#   bpy.data.collections.get("my_collection").children  <== Descendant collections linked (link) here
#
# Requirements:
#
# 1. Make sure new/link are paired and remove/unlink are paired to avoid an unexpected state.
# 2. Failure is preferred to letting Blender create a new collection
#    with an appended name, ie. "my_collection.001"
# 3. Append the sketchname to the sub-collection names to avoid confusing Blender renaming.
# 4. Use a path like string to specify the collection structure, eg. "/CVB/city1_g1x1.001/Sketch"
# 5. A path starts with the root "/" (no relative paths)
# 6. Since we can't control importations, do nothing to ignore case; ie. "city" and "City" are different
#
# Copyright (c) 2021 Keith Pinson
# pylint: enable=line-too-long


import re
import bpy


#    CVB
#        city1_g1x1.001
#            Sketch ~ city1_g1x1.001
#            Map ~ city1_g1x1.001
#            City ~ city1_g1x1.001
#                Tour ~ city1_g1x1.001
#                    Object
#

def extract_path(path_string):
    """Convert a path string to a list of names"""
    return re.findall(r"[^/\\]+", path_string)


def is_path_terminated(path_string):
    """Check to see if path is terminated with a slash"""
    return True if re.match(r".+[/\\]$", path_string) else False


def collection_children(path_string):
    """Return the list of children at the path location,
    make no distinction between failure and a path with no children"""

    children = []

    parts = extract_path(path_string)

    if parts:

        try:
            last_i = len(parts) - 1
            key = parts[last_i]

            coll = bpy.data.collections.get(key)

            if coll:
                children = coll.children.keys()

        except KeyError:
            return []

    return children


def collection_objects(path_string):
    """Return the list of objects at the path location,
    make no distinction between failure and a path with no objects"""

    blender_objects = []

    parts = extract_path(path_string)

    if parts:

        try:
            last_i = len(parts) - 1
            key = parts[last_i]

            coll = bpy.data.collections.get(key)

            if coll:
                blender_objects = coll.objects.keys()

        except KeyError:
            return []

    return blender_objects


def collection_add(path_string):
    """Walk the path and add collections that may be missing"""
    # Fail if the path already exists

    # pylint: disable=consider-using-enumerate

    parts = extract_path(path_string)

    part_added = ""

    # Check for and add the root collection if needed
    try:
        coll = bpy.data.collections[parts[0]]
    except KeyError:
        coll = new_root_node(path_string)
        part_added = parts[0]

    # Check for and add missing child collections
    for i in range(1, len(parts)):
        try:
            if coll:
                coll = coll.children[parts[i]]

        except KeyError:
            coll = new_collection_node(path_string, i)
            part_added = parts[i]

    return part_added


def collection_remove(path_string):
    """Remove the collection; will not remove root"""
    # TODO: Finish collection_remove()
    print(path_string)


def collection_tail(path_string):
    """Walk the path, return the tail collection"""

    # pylint: disable=consider-using-enumerate

    coll = None

    parts = extract_path(path_string)

    if parts:

        try:
            last_i = len(parts) - 1

            coll = bpy.data.collections[parts[0]]

            for i in range(1, len(parts)):
                if i != last_i or \
                        is_path_terminated(path_string) or \
                        coll.children.get(parts[i]):
                    coll = coll.children[parts[i]]  # Collection
                else:
                    break                           # Blender Object

        except KeyError:
            return None

    return coll


def new_collection_node(path_string, index):
    """Add a new collection below the root node"""

    new_node = None

    parts = extract_path(path_string)

    if not parts:
        return new_node

    if not 0 <= index < len(parts):
        return new_node

    if index == 0:
        # Skip this and just add the Root (eg CVB)
        return new_root_node(path_string)

    key = parts[index]

    parent_i = index - 1
    parent_key = parts[parent_i]

    parent_node = bpy.data.collections.get(parent_key)

    if parent_node and hasattr(parent_node, "children"):
        parent_coll = parent_node.children

        if parent_coll is not None and hasattr(parent_coll, "link"):
            new_node = bpy.data.collections.new(key)

            parent_coll.link(new_node)

    return new_node


def new_root_node(path_string):
    """Add a new collection root node"""

    new_node = None

    parts = extract_path(path_string)

    if not parts:
        return new_node

    try:

        key = parts[0]

        new_node = bpy.data.collections.new(key)  # This is the root node

        coll_node = bpy.context.scene.collection.children

        if coll_node and hasattr(coll_node, "link"):
            coll_node.link(new_node)

    except KeyError:
        if new_node:
            bpy.data.collections.remove(new_node)
            new_node = None

        return None

    return new_node


def path_found(path_string):
    """Walk the path, return true if it exists"""

    # pylint: disable=consider-using-enumerate

    parts = extract_path(path_string)

    if parts:

        try:
            last_i = len(parts) - 1

            coll = bpy.data.collections[parts[0]]

            for i in range(1, len(parts)):
                if i != last_i or \
                        is_path_terminated(path_string) or \
                        coll.children.get(parts[i]):
                    coll = coll.children[parts[i]]  # Collection
                else:
                    coll = coll.objects[parts[i]]   # Blender Object

        except KeyError:
            return False

    return True


def path_object(path_string):
    """Walk the path, return object if it exists"""

    # pylint: disable=consider-using-enumerate

    blender_object = None

    parts = extract_path(path_string)

    if parts:

        try:
            last_i = len(parts) - 1

            coll = bpy.data.collections[parts[0]]

            for i in range(1, len(parts)):
                if i != last_i or \
                        is_path_terminated(path_string) or \
                        coll.children.get(parts[i]):
                    coll = coll.children[parts[i]]  # Collection
                else:
                    blender_object = coll.objects[parts[i]]   # Blender Object

        except KeyError:
            return None

    return blender_object
