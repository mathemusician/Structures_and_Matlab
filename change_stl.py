# written by Jv Kyle Eclarin
#
# to run blender portion
# cd /Applications/blender-2.79-rc2-macOS-10.6/blender.app/Contents/MacOS/
# ./blender /Users/jvkyleeclarin/Desktop/test.blend --background --python /Users/jvkyleeclarin/Desktop/change_stl.py


import sys
import numpy as np


def change_stl():
    '''
This makes the stl input in matlab make sense
    '''
    from stl import mesh
    your_mesh = mesh.Mesh.from_file('Cylinder.stl')
    your_mesh.save('new_stl_file.stl') 

import os
from random import randint

def reshape():
    '''
Move vertices in test.blend
    '''
    import bpy, bmesh
    import mathutils
    path = bpy.path.abspath('/Users/jvkyleeclarin/Desktop/')
    if not os.path.exists(path):
        print('Go to change_stl.py and configure line 58')
        # os.makedirs(path)
    new_v_list = get_my_string().split()
    new_v_list = list(map(float, new_v_list))
    new_v_list = np.array(new_v_list).astype(float)
    bpy.ops.object.mode_set(mode='OBJECT')
    mat_loc = mathutils.Matrix.Translation((2.0, 3.0, 4.0))

    for object in bpy.context.selected_objects:
        # deselect all meshes
        bpy.ops.object.select_all(action='DESELECT')

        # select the object
        object.select = True
        bpy.ops.object.mode_set(mode='EDIT')
        obj = bpy.context.edit_object
        me = obj.data
        # Get a BMesh representation
        bm = bmesh.from_edit_mesh(me)
        # this is a coordinate like Vector((0,0,0))
        active_median = 0
        # selects only the vertices I need
        place = -1 # because indexing starts at 0
        if obj.mode == 'EDIT':
            for v in bm.verts:
                bpy.ops.object.vertex_group_select()
                if v.select:
                    place += 1
                    x = v.co[0]
                    y = v.co[1]
                    x_abs = abs(x)
                    y_abs = abs(y)
                    inner_diameter = 1
                    outer_diameter = 1.1
                    n = new_v_list[place]
                    n = n*(outer_diameter-inner_diameter)/outer_diameter
                    x = n*(x/(x_abs+y_abs))
                    y = n*(y/(x_abs+y_abs))
                    bmesh.ops.translate(
                    bm,
                    verts=[v],
                    vec=( x, y, 0.0 ))
        bpy.ops.object.mode_set(mode='OBJECT')
        fPath = str((path + object.name + '.stl'))
        bpy.ops.export_mesh.stl(filepath=fPath)

def get_my_string():
    """Returns the file inputFn"""

    inputFn = "/Users/jvkyleeclarin/Desktop/vertices.txt"

    try:
        with open(inputFn) as inputFileHandle:
            return inputFileHandle.read()

    except IOError:
        sys.stderr.write( "[myScript] - Error: Could not open %s\n" % (inputFn) )
        sys.exit(-1)

if __name__ == '__main__':
    if str(sys.argv[1]) == "change_stl":
        change_stl()
    else:
        reshape()
