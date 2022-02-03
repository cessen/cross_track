#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================

bl_info = {
    "name": "Cross Track",
    "version": (0, 1, 0),
    "author": "Nathan Vegdahl",
    "blender": (2, 92, 0),
    "description": "Blender addon to track a 3D location trianglulated from two 2D camera tracks",
    "location": "Empty properties",
    # "doc_url": "",
    "category": "Animation",
}

import re

import bpy
from bpy.types import Camera, Context


#========================================================


def get_associated_camera(obj):
    cam = None
    for con in obj.constraints:
        if con.type == 'FOLLOW_TRACK':
            if con.camera != None:
                cam = con.camera
    return cam

# Creates an empty that tracks the intersection of the lines
# defined by the locations of the object pairs in pair_1 and
# pair_2.
def add_cross_track_empty(pair_1, pair_2, context):
    print(pair_1)
    print(pair_2)
    # TODO


#========================================================


class CrossTrackPanel(bpy.types.Panel):
    """Find the point of crossing lines."""
    bl_label = "Cross Track"
    bl_idname = "DATA_PT_cross_track"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        return (context.active_object != None) and (context.active_object.type == 'EMPTY')

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout

        col = layout.column()
        col.operator("object.cross_track_add_empty")


class CrossTrackAddEmpty(bpy.types.Operator):
    """Adds an empty that tracks the triangulated position from two selected tracking empties"""
    bl_idname = "object.cross_track_add_empty"
    bl_label = "Add Cross-Track Empty"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) != 2:
            return False
        camera_1 = get_associated_camera(context.selected_objects[0])
        camera_2 = get_associated_camera(context.selected_objects[1])
        return (camera_1 != camera_2) and (camera_1 != None) and (camera_2 != None)

    def execute(self, context):
        obj_1 = context.selected_objects[0]
        obj_2 = context.selected_objects[1]
        camera_1 = get_associated_camera(obj_1)
        camera_2 = get_associated_camera(obj_2)
        add_cross_track_empty([camera_1, obj_1], [camera_2, obj_2], context)        
        return {'FINISHED'}


#========================================================


def register():
    bpy.utils.register_class(CrossTrackPanel)
    bpy.utils.register_class(CrossTrackAddEmpty)


def unregister():
    bpy.utils.unregister_class(CrossTrackPanel)
    bpy.utils.unregister_class(CrossTrackAddEmpty)


if __name__ == "__main__":
    register()
