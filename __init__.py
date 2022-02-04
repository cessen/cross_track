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

import bpy
from mathutils import Vector
from bpy.types import Camera, Context


#========================================================

HELPER_PY_TEXT_NAME = "cross_track_v0_1_0_helpers.py"
HELPER_PY_TEXT = """# CrossTrack v0.1.0
import bpy
from mathutils import Vector

def cross_track_v0_1_0(la0, la1, lb0, lb1):
    # The origin point and direction of line 1 and line 2.
    p1 = Vector(la0)
    d1 = Vector(la1) - p1
    p2 = Vector(lb0)
    d2 = Vector(lb1) - p2

    n = d1.cross(d2)
    n1 = d1.cross(n)
    n2 = d2.cross(n)

    # The closest points between line 1 and line 2.
    c1 = p1 + (d1 * (p2 - p1).dot(n2) / d1.dot(n2))
    c2 = p2 + (d2 * (p1 - p2).dot(n1) / d2.dot(n1))

    # Return the average of the closest points.
    return (c1 + c2) * 0.5

bpy.app.driver_namespace['cross_track_v0_1_0'] = cross_track_v0_1_0
"""

def get_associated_camera(obj):
    cam = None
    for con in obj.constraints:
        if con.type == 'FOLLOW_TRACK':
            if con.camera != None:
                cam = con.camera
    return cam


# Creates the variables needed for our drivers.
def make_driver_variables(driver, pair_1, pair_2):
    # First point of line A.
    la0_x = driver.variables.new()
    la0_y = driver.variables.new()
    la0_z = driver.variables.new()
    la0_x.name = "la0_x"
    la0_y.name = "la0_y"
    la0_z.name = "la0_z"
    la0_x.type = 'TRANSFORMS'
    la0_y.type = 'TRANSFORMS'
    la0_z.type = 'TRANSFORMS'
    la0_x.targets[0].transform_type = 'LOC_X'
    la0_y.targets[0].transform_type = 'LOC_Y'
    la0_z.targets[0].transform_type = 'LOC_Z'
    la0_x.targets[0].transform_space = 'WORLD_SPACE'
    la0_y.targets[0].transform_space = 'WORLD_SPACE'
    la0_z.targets[0].transform_space = 'WORLD_SPACE'
    la0_x.targets[0].id = pair_1[0]
    la0_y.targets[0].id = pair_1[0]
    la0_z.targets[0].id = pair_1[0]

    # Second point of line A.
    la1_x = driver.variables.new()
    la1_y = driver.variables.new()
    la1_z = driver.variables.new()
    la1_x.name = "la1_x"
    la1_y.name = "la1_y"
    la1_z.name = "la1_z"
    la1_x.type = 'TRANSFORMS'
    la1_y.type = 'TRANSFORMS'
    la1_z.type = 'TRANSFORMS'
    la1_x.targets[0].transform_type = 'LOC_X'
    la1_y.targets[0].transform_type = 'LOC_Y'
    la1_z.targets[0].transform_type = 'LOC_Z'
    la1_x.targets[0].transform_space = 'WORLD_SPACE'
    la1_y.targets[0].transform_space = 'WORLD_SPACE'
    la1_z.targets[0].transform_space = 'WORLD_SPACE'
    la1_x.targets[0].id = pair_1[1]
    la1_y.targets[0].id = pair_1[1]
    la1_z.targets[0].id = pair_1[1]

    # First point of line B.
    lb0_x = driver.variables.new()
    lb0_y = driver.variables.new()
    lb0_z = driver.variables.new()
    lb0_x.name = "lb0_x"
    lb0_y.name = "lb0_y"
    lb0_z.name = "lb0_z"
    lb0_x.type = 'TRANSFORMS'
    lb0_y.type = 'TRANSFORMS'
    lb0_z.type = 'TRANSFORMS'
    lb0_x.targets[0].transform_type = 'LOC_X'
    lb0_y.targets[0].transform_type = 'LOC_Y'
    lb0_z.targets[0].transform_type = 'LOC_Z'
    lb0_x.targets[0].transform_space = 'WORLD_SPACE'
    lb0_y.targets[0].transform_space = 'WORLD_SPACE'
    lb0_z.targets[0].transform_space = 'WORLD_SPACE'
    lb0_x.targets[0].id = pair_2[0]
    lb0_y.targets[0].id = pair_2[0]
    lb0_z.targets[0].id = pair_2[0]

    # Second point of line B.
    lb1_x = driver.variables.new()
    lb1_y = driver.variables.new()
    lb1_z = driver.variables.new()
    lb1_x.name = "lb1_x"
    lb1_y.name = "lb1_y"
    lb1_z.name = "lb1_z"
    lb1_x.type = 'TRANSFORMS'
    lb1_y.type = 'TRANSFORMS'
    lb1_z.type = 'TRANSFORMS'
    lb1_x.targets[0].transform_type = 'LOC_X'
    lb1_y.targets[0].transform_type = 'LOC_Y'
    lb1_z.targets[0].transform_type = 'LOC_Z'
    lb1_x.targets[0].transform_space = 'WORLD_SPACE'
    lb1_y.targets[0].transform_space = 'WORLD_SPACE'
    lb1_z.targets[0].transform_space = 'WORLD_SPACE'
    lb1_x.targets[0].id = pair_2[1]
    lb1_y.targets[0].id = pair_2[1]
    lb1_z.targets[0].id = pair_2[1]


# Creates an empty that tracks the intersection of the lines
# defined by the locations of the object pairs in pair_1 and
# pair_2.
def add_cross_track_empty(pair_1, pair_2, context):
    # Create our empty.
    obj = bpy.data.objects.new("CrossEmpty", None)
    context.scene.collection.objects.link(obj)

    # Make sure our helper python text block exists, is
    # registered and is marked for auto-run.
    if HELPER_PY_TEXT_NAME not in bpy.data.texts:
        text = bpy.data.texts.new(HELPER_PY_TEXT_NAME)
        text.write(HELPER_PY_TEXT)
        exec(HELPER_PY_TEXT)
    bpy.data.texts[HELPER_PY_TEXT_NAME].use_module = True

    driver_text_base = "cross_track_v0_1_0((la0_x, la0_y, la0_z), (la1_x, la1_y, la1_z), (lb0_x, lb0_y, lb0_z), (lb1_x, lb1_y, lb1_z))"

    # Create the drivers for each dimension.
    x_driver = obj.driver_add("location", 0).driver
    x_driver.type = 'SCRIPTED'
    x_driver.expression = driver_text_base + "[0]"
    make_driver_variables(x_driver, pair_1, pair_2)

    y_driver = obj.driver_add("location", 1).driver
    y_driver.type = 'SCRIPTED'
    y_driver.expression = driver_text_base + "[1]"
    make_driver_variables(y_driver, pair_1, pair_2)

    z_driver = obj.driver_add("location", 2).driver
    z_driver.type = 'SCRIPTED'
    z_driver.expression = driver_text_base + "[2]"
    make_driver_variables(z_driver, pair_1, pair_2)


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
