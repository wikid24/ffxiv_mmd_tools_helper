import bpy

def create_trapezoid_mesh(head_width, tail_width, height, head_offset, tail_offset, num_subdivisions):
    # Calculate the x-coordinates of the vertices

    # head verts
    head_start = -head_width / 2
    head_end = head_width / 2

    if num_subdivisions > 0:
        head_subdivision_distance = head_width / (num_subdivisions+1)
    else:
        head_subdivision_distance = head_width
    
    head_verts = []
    for i in range(num_subdivisions+2):
        x = head_start + i * head_subdivision_distance
        head_verts.append((x, 0, height+head_offset))

    # tail verts
    tail_start = -tail_width / 2
    tail_end = tail_width / 2

    if num_subdivisions > 0:
        tail_subdivision_distance = tail_width / (num_subdivisions+1)
    else:
        tail_subdivision_distance = tail_width
    
    tail_verts = []
    for i in range(num_subdivisions+2):
        x = tail_start + i * tail_subdivision_distance
        tail_verts.append((x, 0, tail_offset))

    # Define the vertices of the mesh
    verts = head_verts + tail_verts

    # Define the faces of the mesh
    num_head_verts = num_subdivisions + 2
    num_tail_verts = num_subdivisions + 2
    faces = []
    for i in range(num_subdivisions+1):
        j = i + 1
        a = i
        b = j
        c = j+num_tail_verts
        d = i+num_tail_verts
        faces.append((a, b, c, d))

    # Create a new mesh object
    mesh = bpy.data.meshes.new("Trapezoid Mesh")

    # Add the vertices and faces to the mesh
    mesh.from_pydata(verts, [], faces)

    # Update the mesh
    mesh.update()

    # Create a new object and link it to the scene
    obj = bpy.data.objects.new("Trapezoid Mesh", mesh)
    bpy.context.scene.collection.objects.link(obj)

    # Return the object
    return obj

# Call the function with user-defined head and tail distances and height
trapezoid_mesh = create_trapezoid_mesh(0.75, 1.75, 0.5,0.05,0.05,5)