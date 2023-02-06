import bpy
import math
from . import register_wrap


def create_mesh_cylinder(num_segments, radius_tail, radius_head, height, floor_offset, x_scale, y_scale,subdivisions):
    # Create a cylinder mesh
    mesh = bpy.data.meshes.new("Cylinder")

    verts = []
    faces = []

    # Create a loop to add the vertices to the mesh
    for i in range(num_segments + 1):
        angle = 2 * math.pi * i / num_segments
        for j in range(subdivisions + 1):
            if j == 0:
                z = floor_offset
                radius = radius_tail
            elif j == subdivisions:
                z = height #- floor_offset
                radius = radius_head
            else:
                z = (height - floor_offset)  * j / subdivisions + floor_offset
                radius = radius_tail + (radius_head - radius_tail) * j / subdivisions
            x = radius * x_scale * math.cos(angle)
            y = radius * y_scale * math.sin(angle)
            verts.append((x, y, z))

    # Create a loop to add the faces to the mesh
    for i in range(num_segments):
        for j in range(subdivisions):
            a = (subdivisions + 1) * i + j
            b = (subdivisions + 1) * i + j + 1
            c = (subdivisions + 1) * (i + 1) + j + 1
            faces.extend([(a, b, c), (c, a, (subdivisions + 1) * (i + 1) + j)])

    mesh.from_pydata(verts, [], faces)
    mesh.update()

    # Subdivide the edges of the mesh
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.new("Cylinder", mesh)
    bpy.context.collection.objects.link(obj)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(number_cuts=subdivisions)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Search all objects for one that uses this mesh
    for obj in bpy.data.objects:
        if obj.data == mesh:
            # Object found
            return obj


def create_bone_cylinder(num_bone_parents, radius_tail, radius_head, height,floor_offset, x_scale, y_scale, num_subdivisions):
    # Create a new armature object
    armature = bpy.data.armatures.new(name="skirt")
    obj = bpy.data.objects.new(name="skirt", object_data=armature)
    #obj.data.name = "skirt_arm"

    # Add the armature to the scene
    bpy.context.collection.objects.link(obj)
    
    # Set the armature to edit mode
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    # Create a loop to add the bones to the armature
    for i in range(num_bone_parents):
        
        sub_bone_list = []
        
        angle = 2 * math.pi * i / num_bone_parents
        x_tail = radius_tail * math.cos(angle) * x_scale
        y_tail = radius_tail * math.sin(angle) * y_scale
        tail = (x_tail, y_tail, 0 + floor_offset)
        
        x_head = radius_head * math.cos(angle) * x_scale
        y_head = radius_head * math.sin(angle) * y_scale
        head = (x_head, y_head, height)
        
        # Add a bone
        bone = obj.data.edit_bones.new(f"skirt_{i}_0")
        bone.head = head
        bone.tail = tail
        bone.roll = math.atan2(tail[1] - head[1], tail[0] - head[0])
        sub_bone_list.append(bone)
        
        parent_bone = bone
        # Align bone roll with the radius
        
        # Subdivide the bone
        for j in range(1, num_subdivisions):
            sub_head = (
                head[0] + (tail[0] - head[0]) * j / num_subdivisions,
                head[1] + (tail[1] - head[1]) * j / num_subdivisions,
                head[2] + (tail[2] - head[2]) * j / num_subdivisions,
            )
            sub_tail = (
                head[0] + (tail[0] - head[0]) * (j + 1) / num_subdivisions,
                head[1] + (tail[1] - head[1]) * (j + 1) / num_subdivisions,
                head[2] + (tail[2] - head[2]) * (j + 1) / num_subdivisions,
            )
            sub_bone = obj.data.edit_bones.new(f"skirt_{i}_{j}")
            sub_bone.parent = sub_bone_list[j-1]
            sub_bone.use_connect = True
            sub_bone.head = sub_head
            sub_bone.tail = sub_tail
            sub_bone.roll = parent_bone.roll
            sub_bone_list.append(sub_bone) 
        parent_bone.tail = sub_bone_list[1].head
    
    # Search all objects for one that uses this mesh
    for obj in bpy.data.objects:
        if obj.data == armature:
            # Object found
            return obj


def main():
    bpy.ops.object.mode_set(mode='OBJECT')
    
    skirt_arm = bpy.data.objects.get('skirt')
    
    if skirt_arm is not None:
        skirt_arm.select_set(True)

        # Remove the object
        bpy.ops.object.delete()
    
    # Define the parameters for the cone of bones & the cylinder
    num_bone_parents = 16
    num_segments = 16
    num_subdivisions = 5
    radius_tail = 0.32
    radius_head = 0.12
    height = 1.05604
    floor_offset = 0.3
    x_scale = 1.3
    y_scale = 1.0
    num_bone_children = 13
    #curve_factor = 2




    # Create the mesh cylinder
    skirt_mesh = create_mesh_cylinder(num_segments, radius_tail, radius_head, height, x_scale, y_scale,num_subdivisions)
    ## create the bone cylinder
    skirt_arm = create_bone_cylinder(num_bone_parents, radius_tail, radius_head, height, x_scale, y_scale, num_bone_children)
            
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Deselect all objects
    for o in bpy.context.view_layer.objects:
        o.select_set(False)

    # Select the mesh and make it the active object
    skirt_mesh.select_set(True)
    bpy.context.view_layer.objects.active = skirt_mesh
    
    # Create an armature and make it the active object
    bpy.context.view_layer.objects.active = skirt_arm
    
    # Parent the mesh to the armature
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    
    # Enable automatic weights
    #bpy.ops.object.vertex_group_assign()
    


@register_wrap
class Add_Skirt(bpy.types.Operator):
    bl_idname = "ffxiv_mmd_tools_helper.add_skirt"
    bl_label = "Convert MMD Cameras to Blender cameras"
    bl_options = {'REGISTER', 'UNDO'}

    # @classmethod
    # def poll(cls, context):
        # return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}