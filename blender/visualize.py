# Load this file in blender and configure the last line before execution

import bpy

def connect_edges(obj):
    data = obj.data
    for i in range(1, len(data.vertices)):
        data.edges.add(1)
        edge = data.edges[-1]
        edge.vertices = (i-1, i)

def from_point_cloud(ob_name, coords, edges=[], faces=[], show_name = True):
    """Create point cloud object based on given coordinates and name.

    Keyword arguments:
    ob_name -- new object name
    coords -- float triplets eg: [(-1.0, 1.0, 0.0), (-1.0, -1.0, 0.0)]
    """

    # Create new mesh and a new object
    me = bpy.data.meshes.new(ob_name + "Mesh")
    ob = bpy.data.objects.new(ob_name, me)

    # Make a mesh from a list of vertices/edges/faces
    me.from_pydata(coords, edges, faces)

    # Display name and update the mesh
    ob.show_name = show_name
    me.update()
    
    return ob

def add_curve(name, coords):
    """
    coords -- list of tuples of 3 elements for coordiantes
    """
    
    # Create the object
    pc = from_point_cloud(name, coords, show_name = False)
    # Link object to the active collection
    bpy.context.collection.objects.link(pc)
    # Connect edges
    connect_edges(pc)
    
    return pc

def add_point(name, position):
    """
    coords -- tuple, e.g. (0.0, 0.0, 0.0)
    
    Example:
        add_point('my2', (1.0, 0.0, 0.0))
    """
    
    # Create the object
    pc = from_point_cloud(name, [(0.0, 0.0, 0.0)], show_name = True)
    pc.location = position
    # Link object to the active collection
    bpy.context.collection.objects.link(pc)
    
    # Alternatively Link object to scene collection
    #bpy.context.scene.collection.objects.link(pc)
    
    return pc

def animate(obj, locations, duration):
    i = 0
    for loc in locations:
        frame = i*duration
        # X, Y, and Z location to set
        obj.location = loc
        # Set the keyframe with that location, and which frame.
        obj.keyframe_insert(data_path="location", frame = frame)
        i += 1
        
    # Set handle interpolation to linear
    if obj.animation_data.action: # ensure the action is still available
        action = bpy.data.actions.get(obj.animation_data.action.name)
        for curve in action.fcurves:
            for pt in curve.keyframe_points:
                pt.interpolation = 'LINEAR'

def generate_visuals(meta, data, frame_duration):
    objects = meta['Objects'].split(' ')
    frames = int(meta['Frames'])

    # Generate orbit paths
    paths = {}
    # Initialize paths
    for obj in objects:
        paths[obj] = []
    # Group data points
    for d in data:
        name = d[0]
        coord = (d[2], d[3], d[4])
        paths[name].append(coord)
    # Generate path objects
    for obj in paths:
        add_curve(f'{obj}_orbit', paths[obj])
        
    # Generate animated points
    for obj in objects:
        p = add_point(obj, (0, 0, 0))
        animate(p, paths[obj],frame_duration)

def parse_file(path, unit_scale, frame_duration):
    meta = {}
    data = []
    
    with open(path) as file:
        for line in file:
            # End of section
            if line.strip() == '':
                break
            # Skip comment line
            if line.startswith('#'):
                continue
            # Meta data
            if line.startswith('@'):
                parts = line.lstrip('@').strip().split(':')
                key = parts[0].strip()
                value = parts[1].strip()
                meta[key] = value
                continue
            
            # Parse line
            parts = line.split(' ')
            if len(parts) != 5:
                raise Exception(f'Invalid line: {line}')
            
            # Extract line parts
            name = parts[0]
            frame = int(parts[1])
            x = float(parts[2]) * unit_scale
            y = float(parts[3]) * unit_scale
            z = float(parts[4]) * unit_scale
            
            # Save
            tuple = (name, frame, x, y, z)
            data.append(tuple)
    
    generate_visuals(meta, data, frame_duration)
    
    # Configure blender file settings for animation preview
    bpy.context.scene.frame_preview_start = 0 # Frame 0 is the initial condition
    bpy.context.scene.frame_preview_end = int(meta['Frames']) * frame_duration
    bpy.context.scene.use_preview_range = True # Set real time

import os
data_path = os.environ['PROJECT_REBOUND_DATA_FILE_PATH']
print(f'Data path: {data_path}')
parse_file(path = data_path, unit_scale = 100, frame_duration = 5)