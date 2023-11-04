import bpy
import math
import re
from . import register_wrap
from . import bones_renamer
from . import rigid_body
from . import joints
from . import model



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
        #bone.roll = math.atan2(y_tail, x_tail) # Set bone roll to match orientation
        # Calculate the offset to the bone roll
        #if x_scale == 0:
            #offset = math.pi / 2.0
    # else:
        # offset = math.atan(y_scale / x_scale)

        # Apply the offset to the bone roll
        #bone.roll += offset



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



    #select all bones and recalculate bone roll to the global z axis
    bpy.ops.armature.select_all(action='SELECT')
    bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')

    
    # Search all objects for one that uses this mesh
    for obj in bpy.data.objects:
        if obj.data == arm:
            # Object found
            return obj


def reset_skirt_obj():
    
    skirt_children = []
    
    for obj in bpy.data.objects:
        if obj.name == "skirt_obj":
            
            for child in obj.children:
                if child.name.startswith("new_skirt_shape"):
                    #Remove active material from skirt_shape mesh
                    active_mat = child.active_material
                    if active_mat is not None:
                        child.active_material = None
                    bpy.data.materials.remove(active_mat)
                    #remove the new_skirt_shape mesh
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

    #create skirt material and assign it to the mesh
    skirt_mat = bpy.data.materials.new(name="new_skirt_mat")
    skirt_mat.use_nodes = True
    skirt_mat.node_tree.nodes["Principled BSDF"].inputs[21].default_value = 0.1 #set alpha to 10%
    skirt_mesh.active_material = skirt_mat
    skirt_mesh.active_material.blend_method = 'BLEND'
    
            
            
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

    bpy.ops.material.new()

    
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
    
    armature = model.findArmature(mesh_obj)

    if armature is not None:
    #if mesh_obj.parent == bpy.data.objects['skirt_obj']:
        #delete all existing vertex groups that start with 'j_sk_'
        # Get a list of vertex groups to delete
        vertex_groups_to_delete = [vg for vg in mesh_obj.vertex_groups if (vg.name.startswith("j_sk_"))]

        # Delete the vertex groups
        for vg in vertex_groups_to_delete:
            mesh_obj.vertex_groups.remove(vg)
    else:
        print("mesh must be a part of the skirt_obj")

def delete_unused_skirt_vertex_groups(mesh_obj,armature_obj):
    
        #delete all existing vertex groups that start with 'skirt_' if the bone doesn't exist
        # Get a list of all skirt vertex groups and bones
        vertex_groups_list = [vg for vg in mesh_obj.vertex_groups if (vg.name.startswith("skirt_"))]
        skirt_bones_list = [bone for bone in armature_obj.pose.bones if (bone.name.startswith("skirt_"))]

        # Delete the vertex groups
        for vg in vertex_groups_list:
            bone_found = False
            for bone in skirt_bones_list:
                if bone.name == vg.name:
                    bone_found = True
            if bone_found==False:
                mesh_obj.vertex_groups.remove(vg)
    
            
        

def move_bones_and_skirt_to_ffxiv_model(armature):
        

    bpy.ops.object.mode_set(mode='OBJECT')

    #armature = bpy.data.objects['n_root']
    meshes = []

    skirt_obj = bpy.data.objects['skirt_obj']


    #get all the meshes in skirt_obj that are not 'new_skirt_shape'
    for child in skirt_obj.children:
        if child.type == 'MESH' and child.name != 'new_skirt_shape':
            meshes.append(child)
            
        #remove the material from new_skirt_shape object
        if child.type == 'MESH' and child.name == 'new_skirt_shape':
            active_mat = child.active_material
            if active_mat is not None:
                child.active_material = None
                bpy.data.materials.remove(active_mat)
        


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

    #delete the new_skirt_shape mesh and material
    

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
    lower_body_bone = None
    for bone in armature.data.edit_bones:
        if bone.name in lower_body_bone_names:
            lower_body_bone = bone
            #print(lower_body_bone)
            
    #get all the skirt bone parents and set their parent to the lower body bone
    for bone in armature.data.edit_bones:
        if bone.name.startswith('skirt_') and bone.name.endswith('_0'):
            bone.parent = lower_body_bone


    #if new_skirt_arm exists and there's no object, delete it
    for armature in bpy.data.armatures:
        if armature.name == 'new_skirt_arm':
            if bpy.data.objects.get(armature.name):
                obj = bpy.data.objects.get(armature.name)
                #if obj and obj.children:
                    #print(obj.name)
            else:
                bpy.data.armatures.remove(armature)
                print('deleted armature: new_skirt_arm')


def get_min_skirt_chain_number_from_list(skirt_name_list,index_pos):

    min_chain_number = None
    for skirt_name in skirt_name_list:
            
            #first_skirt_bone_name = skirt_bones[0].pose.bones[0].name
            #get the skirt chain number (last number after skirt_)
            result = re.search("^skirt_(\d+)_(\d+)$", skirt_name)
            if result:
                
                chain_number = result.group(index_pos)
                if min_chain_number is None:
                    min_chain_number = chain_number
                elif int(chain_number) < int(min_chain_number):
                        min_chain_number = chain_number   
                        
            else:
                print("No match found.")

    return min_chain_number


"""
def _skirt_reset_to_default(self,context):
    
    props = GenerateSkirtModal
    self.num_bone_parents = #props.bl_rna.properties["num_bone_parents"].default
    self.num_bone_children = props.bl_rna.properties["num_bone_children"].default
    self.num_segments = props.bl_rna.properties["num_segments"].default
    self.num_subdivisions = props.bl_rna.properties["num_subdivisions"].default
    self.height = props.bl_rna.properties["height"].default
    self.radius_head = props.bl_rna.properties["radius_head"].default
    self.floor_offset = props.bl_rna.properties["floor_offset"].default
    self.radius_tail = props.bl_rna.properties["radius_tail"].default
    self.x_scale = props.bl_rna.properties["x_scale"].default
    self.y_scale = props.bl_rna.properties["y_scale"].default
        
"""

@register_wrap
class GenerateSkirtModal(bpy.types.Operator):
    bl_idname = "ffxiv_mmd.generate_skirt_modal"
    bl_label = "Create New Skirt"
    bl_options = {'REGISTER', 'BLOCKING','UNDO','PRESET'}

    def _skirt_shape_update(self, context):
        props = GenerateSkirtModal
        props.num_bone_parents = self.num_bone_parents
        props.num_segments = self.num_segments
        props.num_subdivisions = self.num_subdivisions
        props.radius_tail = self.radius_tail
        props.radius_head = self.radius_head
        props.height = self.height
        props.floor_offset =  self.floor_offset
        props.x_scale = self.x_scale
        props.y_scale = self.y_scale
        props.num_bone_children = self.num_bone_children
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
    
    
    num_bone_parents: bpy.props.IntProperty(name="Bone Chains:", default=16, min =0, update =_skirt_shape_update)
    num_bone_children: bpy.props.IntProperty(name="Bone Chain Children:", default=13, min=3, update =_skirt_shape_update)
    num_segments: bpy.props.IntProperty(name="Mesh Segments:", default=16, min = 0, update =_skirt_shape_update)
    num_subdivisions: bpy.props.IntProperty(name="Mesh Subdivisions:", default=5,min=1, update =_skirt_shape_update)
    height: bpy.props.FloatProperty(name="Top Height:", default=0.98,min=0, update =_skirt_shape_update)
    radius_head: bpy.props.FloatProperty(name="Top Radius:", default=0.12,min=0, update =_skirt_shape_update)
    floor_offset: bpy.props.FloatProperty(name="Bottom Height:", default=0.05,min = 0, update =_skirt_shape_update)
    radius_tail: bpy.props.FloatProperty(name="Bottom Radius:", default=0.32,min=0, update =_skirt_shape_update)
    x_scale: bpy.props.FloatProperty(name="X Scale:", default=1.3,min=0, update =_skirt_shape_update)
    y_scale: bpy.props.FloatProperty(name="Y Scale:", default=1.0,min=0, update =_skirt_shape_update)

    

    def execute(self, context):
    # props = GenerateSkirtModal

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
    bl_idname = "ffxiv_mmd.move_mesh_to_new_skirt_btn"
    bl_label = "Move Mesh to New Skirt"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        
        # Get the object by name
        skirt_obj = bpy.data.objects.get("skirt_obj")

        # Check if the object exists
        if skirt_obj:
            return context.active_object is not None and context.active_object.type =='MESH'

    def execute(self, context):
        mesh_obj = bpy.context.view_layer.objects.active
        skirt_obj = bpy.data.objects['skirt_obj']
        transfer_mesh_to_new_skirt (mesh_obj,skirt_obj)
        bpy.context.view_layer.objects.active = mesh_obj
        return {'FINISHED'}


@register_wrap
class WeightPaintTransferToMesh(bpy.types.Operator):
    bl_idname = "ffxiv_mmd.weight_paint_transfer_to_mesh_btn"
    bl_label = "Weight Paint Transfer to Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # Get the object by name
        skirt_obj = bpy.data.objects.get("skirt_obj")

        # Check if the object exists
        if skirt_obj:
            return context.active_object is not None and context.active_object.type =='MESH' and context.active_object.parent == skirt_obj

    def execute(self, context):
        mesh_obj = bpy.context.view_layer.objects.active
        new_skirt_shape = bpy.data.objects['new_skirt_shape']
        weight_paint_transfer (mesh_obj,new_skirt_shape)
        return {'FINISHED'}
    


@register_wrap
class DeleteFFXIVSkirtVertexGroups(bpy.types.Operator):
    bl_idname = "ffxiv_mmd.delete_ffxiv_skirt_vertex_groups"
    bl_label = "Delete FFXIV/Unused Skirt Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        mesh_obj = bpy.context.view_layer.objects.active
        armature_obj = model.findArmature(mesh_obj)
        delete_ffxiv_skirt_vertex_groups (mesh_obj)
        delete_unused_skirt_vertex_groups(mesh_obj,armature_obj)
        return {'FINISHED'}

@register_wrap
class MergeBonesAndMeshToFFXIVModel(bpy.types.Operator):
    bl_idname = "ffxiv_mmd.merge_bones_and_meshes_to_ffxiv_model"
    bl_label = "Merge bones and all meshes in skirt_obj to the selected armature"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        skirt_obj_exist = False

        if 'skirt_obj' in bpy.data.objects:
            skirt_obj_exist = True

        return obj is not None and obj.type == 'ARMATURE'  and skirt_obj_exist

    def execute(self, context):
        armature = bpy.context.view_layer.objects.active
        move_bones_and_skirt_to_ffxiv_model (armature)
        return {'FINISHED'}

@register_wrap
class GenerateSkirtRigidBodies(bpy.types.Operator):
    bl_idname = "ffxiv_mmd.generate_skirt_rigid_bodies"
    bl_label = "Generate all the skirt Rigid Bodies"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        
        if bpy.context.active_object is not None:
            obj = context.active_object

            contains_skirt_bones = False
            is_mmd_armature = False
            armature = None

            if model.find_MMD_Armature(obj) is not None:
                armature = model.find_MMD_Armature(obj)
                is_mmd_armature = True


            if armature is not None:

                for bone in armature.data.bones:
                    if bone.name.startswith('skirt_'):
                        contains_skirt_bones = True
                        break

            return obj is not None and is_mmd_armature and contains_skirt_bones
        return False

    def execute(self, context):
        armature = bpy.context.view_layer.objects.active
        root = model.findRoot(armature)
        bpy.ops.object.mode_set(mode='OBJECT')

        #delete all the existing rigid bodies and joints for skirt 
        for obj in root.children_recursive:
            if obj.mmd_type == 'RIGID_BODY' and obj.name.startswith('skirt_'):
                
                
                for obj_joint in root.children_recursive:
                    if obj_joint.mmd_type == 'JOINT':
                        if (obj_joint.rigid_body_constraint.object1 == obj or obj_joint.rigid_body_constraint.object2 == obj):
                            bpy.data.objects.remove(obj_joint,do_unlink=True)

                bpy.data.meshes.remove(obj.data,do_unlink=True)
                #bpy.data.objects.remove(obj, do_unlink=True)
                
        

        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')
        skirt_bones = bones_renamer.find_bone_names(startswith='skirt_',append_to_selected=False)

        #get the minimum vertical chain number and chain head number from skirt bones
        bone_names = []
        for bone in skirt_bones:
            if bone.name.startswith('skirt_'):
                bone_names.append(bone.name)
                #print(bone.name)

        min_chain_number = get_min_skirt_chain_number_from_list(bone_names,1)
        min_chain_head_number = get_min_skirt_chain_number_from_list(bone_names,2)
        
        print ('Min Chain Number:',min_chain_number)
        print ('Min Head Chain Number:',min_chain_head_number)


        #create all the rigid bodies with some presets
        bpy.ops.mmd_tools.rigid_body_add(
            name_j = "$name_j"
            ,name_e = "$name_e"
            ,collision_group_number= 6
            ,collision_group_mask= (False, False, False, False, False,False, True, False, False, False, False, False, False, False, False, False)
            ,rigid_type= "1" #'0'= Bone, '1' = Physics, '2' = Physics+Bone
            ,rigid_shape="BOX" #SPHERE, BOX, CAPSULE
            ,size= [0.6,0.15,0.6] #size #size[0] = X, size[1] = Y, size[2] = Z
            ,mass=0.5
            #,friction=friction
            #,bounce=bounce  #restitution
            ,linear_damping=0.9
            ,angular_damping= 0.999
        )

        #get head to tail
        bpy.ops.object.mode_set(mode='OBJECT')
        rigid_body.find_rigid_bodies(startswith='skirt_',append_to_selected=False)
        rigid_body_bone_chains = rigid_body.get_all_rigid_body_chains_from_selected()
        rigid_body_bone_chains_data=  rigid_body.get_all_rigid_body_chains_dictionary(rigid_body_bone_chains)
        #make the tail of the rigid bodies a bit wider by 0.05
        for i in rigid_body_bone_chains_data:
            rigid_body.transform_rigid_body_bone_chain(
                        rigid_body_bone_chain=rigid_body_bone_chains_data[i]['chain_data'],
                        size_x_start= rigid_body_bone_chains_data[i]['head']['size_x'],
                        size_x_end=0.05 + rigid_body_bone_chains_data[i]['tail']['size_x'],
                    )



        #get head+1 to tail
        #rigid_body.find_rigid_bodies(startswith='skirt_1_1',append_to_selected=False)[0]
        rigid_body.find_rigid_bodies(startswith='skirt_'+min_chain_number+'_'+str((int(min_chain_head_number)+1)),append_to_selected=False)[0]
        bpy.ops.ffxiv_mmd.select_skirt_rigid_bodies(direction='HORIZONTAL')
        bpy.ops.ffxiv_mmd.select_rigid_body_bone_chain(direction='DOWN')
        #set mass for head+1 to tail to 0.1 to 0.02
        rigid_body_bone_chains = rigid_body.get_all_rigid_body_chains_from_selected()
        rigid_body_bone_chains_data=  rigid_body.get_all_rigid_body_chains_dictionary(rigid_body_bone_chains)
        for i in rigid_body_bone_chains_data:
            rigid_body.transform_rigid_body_bone_chain(
                        rigid_body_bone_chain=rigid_body_bone_chains_data[i]['chain_data'],
                        mass_start=0.1,
                        mass_end=0.02,
                        )

        #get head+2 to tail
        #rigid_body.find_rigid_bodies(startswith='skirt_1_2',append_to_selected=False)[0]
        rigid_body.find_rigid_bodies(startswith='skirt_'+min_chain_number+'_'+str((int(min_chain_head_number)+2)),append_to_selected=False)[0]
        bpy.ops.ffxiv_mmd.select_skirt_rigid_bodies(direction='HORIZONTAL')
        bpy.ops.ffxiv_mmd.select_rigid_body_bone_chain(direction='DOWN')
        #set linear_damping for head+1 to tail to 1 to 0.555
        rigid_body_bone_chains = rigid_body.get_all_rigid_body_chains_from_selected()
        rigid_body_bone_chains_data=  rigid_body.get_all_rigid_body_chains_dictionary(rigid_body_bone_chains)
        for i in rigid_body_bone_chains_data:
            rigid_body.transform_rigid_body_bone_chain(
                        rigid_body_bone_chain=rigid_body_bone_chains_data[i]['chain_data'],
                        linear_damping_start=1,
                        linear_damping_end=0.555,
                        )
            

        bpy.ops.object.mode_set(mode='OBJECT')
        rigid_body.find_rigid_bodies(startswith='skirt_',append_to_selected=False)
        bpy.context.view_layer.objects.active = armature

        return {'FINISHED'}


@register_wrap
class GenerateSkirtJoints(bpy.types.Operator):
    bl_idname = "ffxiv_mmd.generate_skirt_joints"
    bl_label = "Generate all the skirt Rigid Body Joints"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        
        if bpy.context.active_object is not None:
            obj = context.active_object

            contains_skirt_rigidbodies = False
            is_mmd_armature = False
            armature = None
            root = None

            if model.find_MMD_Armature(obj) is not None:
                armature = model.find_MMD_Armature(obj)
                root = model.findRoot(armature)
                is_mmd_armature = True


            if armature is not None:

                for child in root.children_recursive:
                    if child.mmd_type == 'RIGID_BODY' and child.name.startswith('skirt_'):
                        contains_skirt_rigidbodies = True
                        break
                
            return obj is not None and is_mmd_armature  and contains_skirt_rigidbodies
        return False

    def execute(self, context):
        armature = bpy.context.view_layer.objects.active

        bpy.ops.object.mode_set(mode='OBJECT')

        #find the lower body bone
        lower_body_bone_names = ['lower body','下半身','j_kosi']
        lower_body_bone = None
        for bone in armature.data.edit_bones:
            if bone.name in lower_body_bone_names:
                lower_body_bone = bone
            #print(lower_body_bone)

       

            lower_body_rigid = rigid_body.find_rigid_bodies(startswith=lower_body_bone.name,append_to_selected=False)[0]
            rigid_body_list = rigid_body.find_rigid_bodies(startswith='skirt_',append_to_selected=False)
            #rigid_body_bone_chains = rigid_body.get_all_rigid_body_chains_from_selected()

        if lower_body_bone is None or lower_body_rigid is None:
            print("Error: No rigid body or bone named 'lower body','下半身' or 'j_kosi' found to pin the skirt's joints to. Create this rigid body to continue")
        else:
            #create vertical joints, pinned to lower body rigid
            joints.create_vertical_joints(rigid_body_pin_obj=lower_body_rigid
                                        ,use_bone_rotation=True
                                        ,limit_linear_lower=[0,0,0]
                                        ,limit_linear_upper=[0,0,0]
                                        ,limit_angular_lower=[0,0,0]
                                        ,limit_angular_upper=[0,0,0]
                                        ,spring_linear=[0,0,0]
                                        ,spring_angular=[0,0,0])

            
            rigid_body_list_with_number_index = rigid_body.get_rigid_body_list_with_number_index(rigid_body_list)
            grouped_rigid_bodies_by_index_pos = rigid_body.get_grouped_rigid_body_list_by_index_position (rigid_body_list_with_number_index,1)
            #create horizontal joints, wrap around = True. This should really be a parameter that gets passed to this operator? If it is a half skirt (like on Neo-Ishgardian Top) or cape (like Obsolete Android's Cloak of Aiming)
            joints.create_horizontal_joints(rigid_body_chains=grouped_rigid_bodies_by_index_pos
                                            ,wrap_around=True
                                            ,use_bone_rotation=True
                                        ,limit_linear_lower=[-0.05313,0,0]
                                        ,limit_linear_upper=[0.05313,0,0]
                                        ,limit_angular_lower=[0,0,0]
                                        ,limit_angular_upper=[0,0,0]
                                        ,spring_linear=[0,0,0]
                                        ,spring_angular=[0,0,0]
            )

            

            rigid_body.find_rigid_bodies(startswith='skirt_',append_to_selected=False)
            joints.get_joints_from_selected_rigid_bodies()


        return {'FINISHED'}


