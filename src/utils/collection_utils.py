"""Routines for creating and finding collections used by CVB"""
#
# All interactions with the Blender collections should be
# done through these routines.
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
    return re.findall("[^/]+", path_string)


def collection_exist(path_string):
    """Walk the collection path, return true if it can be completed"""

    parts = extract_path(path_string)

    if parts:

        try:
            coll = bpy.data.collections[parts[0]]

            sketchname = parts[1]
            coll = coll.children[sketchname]

            for p in parts[2:]:
                coll = coll.children[p + " ~ " + sketchname]

        except KeyError:
            return False

    return True


def collection_children(path_string):
    """Return the list of children at the path location,
    make no distinction between failure and a path with no children"""

    children = []

    parts = extract_path(path_string)

    if parts:

        try:
            coll = bpy.data.collections[parts[0]]

            sketchname = parts[1]
            coll = coll.children[sketchname]

            for p in parts[2:]:
                coll = coll.children[p + " ~ " + sketchname]

            children = coll.children.keys()

        except KeyError:
            return []

    return children


def collection_verify(path_string):
    """Walk the collection path, verify that links are correct"""

    missing_node_was_found = False

    parts = extract_path(path_string)

    if not parts:
        return False

    try:
        for i in range(len(parts)):

            key = parts[i] if i < 2 else parts[i] + " ~ " + parts[1]

            coll = bpy.data.collections.get(key)

            if coll is not None and missing_node_was_found:
                return False

            if coll is None:
                missing_node_was_found = True

    except KeyError:
        return False

    return True


def collection_first_missing(path_string):
    """Walk the collection path, find the first missing"""

    first_missing_found_at = -1

    parts = extract_path(path_string)

    if not parts:
        return first_missing_found_at

    try:

        for i in range(len(parts)):

            key = parts[i] if i < 2 else parts[i] + " ~ " + parts[1]

            coll = bpy.data.collections.get(key)

            if coll is None:
                first_missing_found_at = i
                break

    except KeyError:
        return -1

    return first_missing_found_at


def collection_add(path_string):
    """Walk the list and add the tail end that may be missing."""
    # We cannot try to add nodes with the same name. We need to verify only
    # the tail end nodes need to be added, otherwise fail.

    result = False

    # First verify the integrity of the collections
    if not collection_verify(path_string):
        return result

    add_at = collection_first_missing(path_string)

    if add_at == -1:
        return result

    parts = extract_path(path_string)

    if not parts:
        return result

    result = True
    for i in range(add_at, len(parts)):

        new_node = new_collection_node(path_string, i)

        if not new_node:
            result = False
            break

    return result


def collection_remove(path_string):
    # TODO: Finish collection_remove()
    pass


def new_collection_node(path_string, index):
    """Add a new collection below the root node"""

    new_node = None

    parts = extract_path(path_string)

    if not parts:
        return new_node

    if not (0 <= index < len(parts)):
        return new_node

    if index == 0:
        # Skip this and just add the Root (eg CVB)
        return new_root_node(path_string)

    key = parts[index] if index < 2 else "{} ~ {}".format(parts[index], parts[1])

    parent_i = index - 1
    parent_key = parts[parent_i] if parent_i < 2 else "{} ~ {}".format(parts[parent_i], parts[1])

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
