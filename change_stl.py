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


# whenver I run blender and python, I have to do this for some reason because
# it forgets all the other libraries :(
# Actually, I figured this out...
# So it's Python3 so some libraries aren't in Python 3, OBVIOUSLY, DUHHH
sys.path.append(['/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python27.zip', \
'/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7', \
'/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-darwin', \
'/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac', \
'/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac/lib-scriptpackages',\
'/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-tk', \
'/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-old', \
'/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload', \
'/Users/jvkyleeclarin/Library/Python/2.7/lib/python/site-packages', \
'/usr/local/lib/python2.7/site-packages', \
'/usr/local/Cellar/numpy/1.13.1_1/libexec/nose/lib/python2.7/site-packages', \
'/usr/local/Cellar/protobuf/3.5.0/libexec/lib/python2.7/site-packages', \
'/usr/local/lib/python2.7/site-packages/wx-3.0-osx_cocoa', 
'/Library/Python/2.7/site-packages',\
'/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python', \
'/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC',\
'/Library/Python/2.7/site-packages/pip-9.0.1-py2.7.egg',\
'/Library/Python/2.7/site-packages/MeshPy-2016.1.2-py2.7-macosx-10.13-intel.egg', \
'/Library/Python/2.7/site-packages/pytest-3.3.1-py2.7.egg', \
'/Library/Python/2.7/site-packages/pytools-2017.6-py2.7.egg', \
'/Library/Python/2.7/site-packages/pluggy-0.6.0-py2.7.egg', \
'/Library/Python/2.7/site-packages/attrs-17.3.0-py2.7.egg', \
'/Library/Python/2.7/site-packages/py-1.5.2-py2.7.egg', \
'/Library/Python/2.7/site-packages/appdirs-1.4.3-py2.7.egg', '/Library/Python/2.7/site-packages', \
'/Library/Python/2.7/site-packages/'])

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



"""
OLD CODE BELOW
"""



#bpy.ops.object.select_all(action='TOGGLE')
#v.select_set()

#bm.to_mesh(me)
#bm.free()
# export object with its name as file name

#bpy.context.active_object = object

'''
vertices = x
# Define the 12 triangles composing the cube
faces = y
# Create the mesh
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        cube.vectors[i][j] = vertices[f[j],:]
cube.save('new_stl_file.stl') 
'''

'''
    # this works because of numpy
    # your_mesh.v0[0:2] += x.astype(float)
    init_x = your_mesh.vectors[0][0:3,0:1]
    for place in range(0,len(init_x)):
        x_init = init_x[place]
        mask = np.any(your_mesh.vectors[:,0:3,0:1] == x_init, axis=1, keepdims=False)
        sys.stderr.write(str(your_mesh.vectors[mask.astype(int),0:3,0:1][1]) + '\n')
        your_mesh.vectors[mask.astype(int),0:3,0:1] += x
        sys.stderr.write(str(your_mesh.vectors[mask.astype(int),0:3,0:1][1]) + '\n')
        #mask = np.any(your_mesh.v0[:,0:1] == x_init, axis=1, keepdims=False)
        #your_mesh.v0[mask.astype(int),0:1] += x
        #mask = np.any(your_mesh.v1[:,0:1] == x_init, axis=1, keepdims=False)
        #your_mesh.v1[mask.astype(int),0:1] += x
        #mask = np.any(your_mesh.v2[:,0:1] == x_init, axis=1, keepdims=False)
        #your_mesh.v2[mask.astype(int),0:1] += x
    #init_y = [your_mesh.vectors[0][0:3,1:2]]
    #for y_init in init_y:
    #    np.where(any(your_mesh.vectors[:,0:3,1:2]==y_init),your_mesh.vectors,y_init+y)

    #for place in range(0,len(your_mesh.vectors)):
    #    mask = your_mesh.vectors[place][0:3,0:1]
    #    sys.stderr.write(str(mask.any()))
    #    if mask.any():
    #        your_mesh.vectors[place][0:3,0:1] += x
    #    mask = your_mesh.vectors[place][0:3,1:2] == init_y
    #    if mask.any():
    #        your_mesh.vectors[place][0:3,1:2] += y

    # your_mesh.v1[0:2] += y
'''

'''
def spiral(segs=30):
    verts = []
    edges = []
    z=0
    n = 3
    position = bpy.context.scene.cursor_location
    print(bpy.context.scene.cursor_location)
    a = 0.5
    for i in range(segs):
        t = n * 2 * pi * (i)/ segs
        # parametric eqn of a helix
        x, y, z = (a * sin(t), a  * cos(t),  a * t / n)

        verts.append((x,y,z))

    for i in range(len(verts) - 1):
        edges.append((i, i+1))
    mesh = bpy.data.meshes.new("Spiral")
    object = bpy.data.objects.new("Spiral", mesh)
    print(verts, edges)
    object.location = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(object)
    mesh.from_pydata(verts,edges, [])
    mesh.update(calc_edges=True)

spiral()
'''

'''
if obj is not None:
    verts = ...
    edges = [(2, 0), (0, 1), (1, 3), (3, 2), (6, 2), (3, 7), (7, 6), (4, 6), (7, 5), (5, 4), (0, 4), (5, 1), ]
    faces = [(0, 1, 3, 2, ), (2, 3, 7, 6, ), (6, 7, 5, 4, ), (4, 5, 1, 0, ), (2, 6, 4, 0, ), (7, 3, 1, 5, ), ]
    mesh = bpy.data.meshes.new("Spiral")
    bpy.ops.object.mode_set(mode='EDIT')
    object = bpy.data.objects.new("Spiral", mesh)
    mesh.from_pydata(verts, edges, faces)
    mesh.update()
    mesh.update()
'''

'''
bm.verts.new((2.0, 2.0, 2.0))
bm.verts.new((-2.0, 2.0, 2.0))
bm.verts.new((-2.0, -2.0, 2.0))

bm.faces.new((bm.verts[i] for i in range(-3,0)))

bm.verts.new((2.0, 2.0, -2.0))
bm.verts.new((-2.0, 2.0, -2.0))
bm.verts.new((-2.0, -2.0, -2.0))
bm.verts.new((2.0, -2.0, -2.0))

bm.faces.new((bm.verts[i] for i in range(-4,0)))
'''

'''
bpy.ops.transform.translate(
value=(2,0,0),
constraint_axis=(True, False, False),
constraint_orientation='GLOBAL',
mirror=False,
proportional='DISABLED',
proportional_edit_falloff='SMOOTH',
proportional_size=1,
release_confirm=True)
'''

'''
for f in bm.faces:
if x == 0:
    active_median = f.calc_center_median()
    x += 1
f.select = False
if (f.calc_center_median()-active_median).length <= 3:
    f.select = True
'''

'''
# load arrays
x_change = np.array((sys.argv[2]))
y_change = np.array((sys.argv[3]))
# change into the proper type
x_change = x_change.astype(float)
y_change = y_change.astype(float)
'''