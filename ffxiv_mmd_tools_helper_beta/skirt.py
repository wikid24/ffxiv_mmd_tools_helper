import bpy
import math
from . import register_wrap



def create_skirt_mesh(num_segments, radius_tail, radius_head, height, floor_offset, x_scale, y_scale,subdivisions):
    # Create a cylinder mesh
    mesh = bpy.data.meshes.new("new_skirt_shape")

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
    obj = bpy.data.objects.new("new_skirt_shape", mesh)
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
            break


def create_skirt_bones(num_bone_parents, radius_tail, radius_head, height,floor_offset, x_scale, y_scale, num_subdivisions):
    
    #if new_skirt_arm doesn't exist, create it 
    arm = None
    for armature in bpy.data.armatures:
        if armature.name.startswith("new_skirt_arm"):
            arm = armature
            break
    if arm == None:
        arm = bpy.data.armatures.new(name="new_skirt_arm")
    
    #if new_skirt_obj doesn't exist, create it
    obj = None
    for object in bpy.data.objects:
        if object.name.startswith("skirt_obj"):
            obj = object
            break
    if obj == None:        
        obj = bpy.data.objects.new(name="skirt_obj", object_data=arm)
        # Add the skirt_obj to the scene
        bpy.context.collection.objects.link(obj)
    #obj.data.name = "skirt_arm"
    
    # Set the skirt_obj to edit mode
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
        if obj.data == arm:
            # Object found
            return obj


def reset_skirt_obj():
    
    skirt_children = []
    
    for obj in bpy.data.objects:
        if obj.name == "skirt_obj":
            
            #remove the new_skirt_shape mesh
            for child in obj.children:
                if child.name.startswith("new_skirt_shape"):
                    for mesh in bpy.data.meshes:
                        if mesh.name == child.name:
                            bpy.data.meshes.remove(mesh)
                            break
                else:
                    skirt_children.append(child)
            
            #delete the new skirt armature                        
            if obj.data.name == "new_skirt_arm":
                bpy.data.armatures.remove(obj.data)

            break
        
    
    return skirt_children    

def generate_new_skirt(num_bone_parents,num_segments,num_subdivisions,radius_tail,radius_head,height,floor_offset,x_scale,y_scale,num_bone_children):
    #main code
    bpy.ops.object.mode_set(mode='OBJECT')

    #removes the new skirt object before creating a new one and stores the children in a list
    skirt_obj_children = reset_skirt_obj()
    
   # Make the armature the active object
    bpy.context.view_layer.objects.active = bpy.context.view_layer.objects[-1]    
    
    """
    # Define the parameters for the cone of bones & the cylinder
    num_bone_parents = 16
    num_segments = 16
    num_subdivisions = 5
    radius_tail = 0.32
    radius_head = 0.12
    height = 0.98
    floor_offset = 0.05
    x_scale = 1.3
    y_scale = 1.0
    num_bone_children = 13
    #curve_factor = 2
    """

    # Create the skirt mesh and bones armature
    skirt_mesh = create_skirt_mesh(num_segments, radius_tail, radius_head, height,floor_offset , x_scale, y_scale,num_subdivisions)
    skirt_arm = create_skirt_bones(num_bone_parents, radius_tail, radius_head, height, floor_offset,x_scale, y_scale, num_bone_children)
            
            
    bpy.ops.object.mode_set(mode='OBJECT')
    # Deselect all objects
    for o in bpy.context.view_layer.objects:
        o.select_set(False)

    # Select the mesh and make it the active object
    skirt_mesh.select_set(True)
    bpy.context.view_layer.objects.active = skirt_mesh

    # Make the armature the active object
    bpy.context.view_layer.objects.active = skirt_arm

    # Parent the mesh to the armature
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    
    #smooth out the weight paint
    # Deselect all objects
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    skirt_arm.select_set(True)
    skirt_mesh.select_set(True)
    bpy.context.view_layer.objects.active = skirt_mesh
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.object.vertex_group_smooth(group_select_mode='ALL', factor=1, repeat=1, expand=0)


    
    #parents the skirt_obj_children to the new skirt armature
    if skirt_obj_children:
        for child in skirt_obj_children:
            child.parent = skirt_arm
    

def transfer_mesh_to_new_skirt(mesh_obj, skirt_obj):
    
    
    if skirt_obj.type == 'ARMATURE' and skirt_obj.name =='skirt_obj':
    
        if mesh_obj.type == 'MESH':
            
            bpy.ops.object.mode_set(mode='OBJECT')
            # Deselect all objects
            for o in bpy.context.view_layer.objects:
                o.select_set(False)
            
            # Select the mesh and make it the active object
            mesh_obj.select_set(True)
            bpy.context.view_layer.objects.active = mesh_obj

            # Make the armature the active object
            skirt_obj.select_set(True)
            bpy.context.view_layer.objects.active = skirt_obj
            
            bpy.ops.object.parent_set(type = 'OBJECT',keep_transform = True)
                
        else:
            print('current active object, ',mesh_obj.name,' not a mesh')
    else:
        print('create the skirt_obj before running this command')
        
  
def clean_up_weight_paint(mesh_obj,armature_obj):

    # Make sure the armature object is in pose mode
    bpy.context.view_layer.objects.active = armature_obj
    bpy.ops.object.mode_set(mode='POSE')

    # Loop through the bones in the armature object at the top of the skirt
    for bone in armature_obj.pose.bones:
        if bone.name.startswith('skirt_') and bone.name.endswith('_0'):
            # Get the corresponding vertex group in the mesh object
            vgroup = mesh_obj.vertex_groups.get(bone.name)
            if vgroup:
                # Go to weight paint mode
                bpy.context.view_layer.objects.active = mesh_obj
                bpy.ops.object.mode_set(mode='WEIGHT_PAINT')

                # Get the head height of the bone
                head_height = bone.head[2]

                # Loop through the vertices in the mesh object
                for v in mesh_obj.data.vertices:
                    # Check if the vertex is in the vertex group
                    for g in v.groups:
                        if g.group == vgroup.index:
                            # Get the weight for the vertex in the vertex group
                            weight = g.weight
                            # Set the weight to 0 if the vertex height is higher than the bone's head height
                            if v.co[2] > head_height:
                                vgroup.add([v.index], 0, 'REPLACE')

                # Go back to object mode
                #bpy.ops.object.mode_set(mode='OBJECT')


def weight_paint_transfer (mesh_obj,new_skirt_shape):

    bpy.ops.object.mode_set(mode='OBJECT')

    # Make the armature the active object
    mesh_obj.select_set(True)
    bpy.context.view_layer.objects.active = mesh_obj
    
    #find the armature modifier and delete it
    arm_modifier_name = None
    
    for mod in mesh_obj.modifiers:
        print(mod.name,' ',mod.type)
        if mod.type == 'ARMATURE':
            arm_modifier_name = mod.name
            mesh_obj.modifiers.remove(mesh_obj.modifiers[mod.name])
            
    #delete all existing vertex groups that start with 'skirt_'
    # Get a list of vertex groups to delete
    vertex_groups_to_delete = [vg for vg in mesh_obj.vertex_groups if (vg.name.startswith("skirt_"))]

    # Delete the vertex groups
    for vg in vertex_groups_to_delete:
        mesh_obj.vertex_groups.remove(vg)
            
    #select the new_skirt mesh, then the mesh object, then go to weight paint mode
    
    # Deselect all objects
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
        
    # Select the new_skirt_shape as the active object
    new_skirt_shape.select_set(True)
    bpy.context.view_layer.objects.active = new_skirt_shape
    
    # Select the mesh and make it the active object
    mesh_obj.select_set(True)
    bpy.context.view_layer.objects.active = mesh_obj

    #set the mode to WEIGHT_PAINT MODE
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
    
    #do the weight paint transfer
    bpy.ops.object.data_transfer(use_reverse_transfer=True
            , data_type='VGROUP_WEIGHTS'
            , use_create=True
            , vert_mapping='POLYINTERP_NEAREST'
            , use_object_transform=True
            , ray_radius=5
            , layers_select_src='NAME'
            , layers_select_dst='ALL'
            , mix_mode='REPLACE'
            , mix_factor=1)
    
    #arm_modifier_name = 'n_root'
    
    #re-add the armature modifier
    arm_modifier = mesh_obj.modifiers.new(name = arm_modifier_name,type='ARMATURE')
    arm_modifier.object = bpy.data.objects[arm_modifier_name]
    
    armature = bpy.data.objects['skirt_obj']
    clean_up_weight_paint(mesh_obj,armature)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = mesh_obj
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
  

def delete_ffxiv_skirt_vertex_groups(mesh_obj):
    
    if mesh_obj.parent == bpy.data.objects['skirt_obj']:
        #delete all existing vertex groups that start with 'j_sk_'
        # Get a list of vertex groups to delete
        vertex_groups_to_delete = [vg for vg in mesh_obj.vertex_groups if (vg.name.startswith("j_sk_"))]

        # Delete the vertex groups
        for vg in vertex_groups_to_delete:
            mesh_obj.vertex_groups.remove(vg)
    else:
        print("mesh must be a part of the skirt_obj")

def move_bones_and_skirt_to_ffxiv_model(armature):
        

    bpy.ops.object.mode_set(mode='OBJECT')

    #armature = bpy.data.objects['n_root']
    meshes = []

    skirt_obj = bpy.data.objects['skirt_obj']


    #get all the meshes in skirt_obj that are not 'new_skirt_shape'
    for child in skirt_obj.children:
        if child.type == 'MESH' and child.name != 'new_skirt_shape':
            meshes.append(child)


    # Deselect all objects
    for o in bpy.context.view_layer.objects:
        o.select_set(False)

    if meshes != None:
        #move all the meshes into the armature
        for mesh in meshes:
            mesh.select_set(True)    
        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

    #delete the new_skirt_shape mesh
    new_skirt_shape = bpy.data.meshes['new_skirt_shape']
    if new_skirt_shape != None:
        bpy.data.meshes.remove(new_skirt_shape)


            
    # Deselect all objects
    for o in bpy.context.view_layer.objects:
        o.select_set(False)

    skirt_obj.select_set(True)
    bpy.context.view_layer.objects.active = skirt_obj

    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature

    #merge the skirt bones into the armature
    bpy.ops.object.join()

    bpy.ops.object.mode_set(mode='EDIT')

    #find the lower body bone
    lower_body_bone_names = ['lower body','下半身','j_kosi']
    lower_bone_bone = None
    for bone in armature.data.edit_bones:
        if bone.name in lower_body_bone_names:
            lower_body_bone = bone
            #print(lower_body_bone)
            
    #get all the skirt bone parents and set their parent to the lower body bone
    for bone in armature.data.edit_bones:
        if bone.name.startswith('skirt_') and bone.name.endswith('_0'):
            bone.parent = lower_body_bone
        





def _skirt_shape_update(self, context):

    bpy.context.space_data.shading.type = 'WIREFRAME'

    generate_new_skirt(
            self.num_bone_parents
            ,self.num_segments
            ,self.num_subdivisions
            ,self.radius_tail
            ,self.radius_head
            ,self.height
            ,self.floor_offset
            ,self.x_scale
            ,self.y_scale
            ,self.num_bone_children
            )

@register_wrap
class GenerateSkirtModal(bpy.types.Operator):
    bl_idname = "object.generate_skirt_modal"
    bl_label = "Create New Skirt"
    bl_options = {'REGISTER', 'BLOCKING','UNDO','PRESET'}
    
    num_bone_parents: bpy.props.IntProperty(name="Bone Parents", default=16, min =1, update =_skirt_shape_update)
    num_bone_children: bpy.props.IntProperty(name="Number of Bone Children", default=13, min=2, update =_skirt_shape_update)
    num_segments: bpy.props.IntProperty(name="Mesh Segments", default=16, min = 4, update =_skirt_shape_update)
    num_subdivisions: bpy.props.IntProperty(name="Mesh Subdivisions:", default=5,min=1, update =_skirt_shape_update)
    height: bpy.props.FloatProperty(name="Head Height", default=0.98,min=0, update =_skirt_shape_update)
    radius_head: bpy.props.FloatProperty(name="Head Radius", default=0.12,min=0, update =_skirt_shape_update)
    floor_offset: bpy.props.FloatProperty(name="Tail Height", default=0.05,min = 0, update =_skirt_shape_update)
    radius_tail: bpy.props.FloatProperty(name="Tail Radius", default=0.32,min=0, update =_skirt_shape_update)
    x_scale: bpy.props.FloatProperty(name="X Scale", default=1.3,min=0, update =_skirt_shape_update)
    y_scale: bpy.props.FloatProperty(name="Y Scale", default=1.0,min=0, update =_skirt_shape_update)


    def execute(self, context):
        generate_new_skirt(
            self.num_bone_parents
            ,self.num_segments
            ,self.num_subdivisions
            ,self.radius_tail
            ,self.radius_head
            ,self.height
            ,self.floor_offset
            ,self.x_scale
            ,self.y_scale
            ,self.num_bone_children
            )
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.space_data.shading.type = 'MATERIAL'
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

      


@register_wrap
class MoveMeshToNewSkirt(bpy.types.Operator):
    bl_idname = "object.move_mesh_to_new_skirt_btn"
    bl_label = "Move Mesh to New Skirt"
    bl_options = {'REGISTER', 'UNDO'}

    # @classmethod
    # def poll(cls, context):
        # return context.active_object is not None

    def execute(self, context):
        mesh_obj = bpy.context.view_layer.objects.active
        skirt_obj = bpy.data.objects['skirt_obj']
        transfer_mesh_to_new_skirt (mesh_obj,skirt_obj)
        return {'FINISHED'}


@register_wrap
class WeightPaintTransferToMesh(bpy.types.Operator):
    bl_idname = "object.weight_paint_transfer_to_mesh_btn"
    bl_label = "Weight Paint Transfer to Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    # @classmethod
    # def poll(cls, context):
        # return context.active_object is not None

    def execute(self, context):
        mesh_obj = bpy.context.view_layer.objects.active
        new_skirt_shape = bpy.data.objects['new_skirt_shape']
        weight_paint_transfer (mesh_obj,new_skirt_shape)
        return {'FINISHED'}

@register_wrap
class DeleteFFXIVSkirtVertexGroups(bpy.types.Operator):
    bl_idname = "object.delete_ffxiv_skirt_vertex_groups"
    bl_label = "Delete FFXIV Skirt Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    # @classmethod
    # def poll(cls, context):
        # return context.active_object is not None

    def execute(self, context):
        mesh_obj = bpy.context.view_layer.objects.active
        delete_ffxiv_skirt_vertex_groups (mesh_obj)
        return {'FINISHED'}

@register_wrap
class MergeBonesAndMeshToFFXIVModel(bpy.types.Operator):
    bl_idname = "object.merge_bones_and_meshes_to_ffxiv_model"
    bl_label = "Delete FFXIV Skirt Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    # @classmethod
    # def poll(cls, context):
        # return context.active_object is not None

    def execute(self, context):
        armature = bpy.context.view_layer.objects.active
        move_bones_and_skirt_to_ffxiv_model (armature)
        return {'FINISHED'}
