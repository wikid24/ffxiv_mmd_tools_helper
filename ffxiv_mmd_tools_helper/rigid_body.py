import bpy
from . import register_wrap
from . import model
from mmd_tools.operators.rigid_body import AddRigidBody
from . import import_csv
from mmd_tools.core import model as mmd_model
import re
import math
from functools import reduce
from . import bones_renamer
import mathutils

def get_attribute(obj, attr_name):
    if "[" in attr_name and "]" in attr_name:
        attr_base, index_str = attr_name.split("[")
        index = int(index_str.strip("]"))
        attr_value = reduce(getattr, attr_base.split("."), obj)
        return getattr(attr_value, f"__getitem__")(index)
    else:
        return reduce(getattr, attr_name.split("."), obj)


def read_rigid_body_file():
	
	RIGID_BODY_DICTIONARY = None
	RIGID_BODY_DICTIONARY = import_csv.use_csv_rigid_body_dictionary()

	#convert the list into a dictionary with a header
	RIGID_BODY_DICTIONARY = [dict(zip(RIGID_BODY_DICTIONARY[0],row)) for row in RIGID_BODY_DICTIONARY[1:]]

	#convert the values in 'collision_group_mask' into a boolean list
	for row in RIGID_BODY_DICTIONARY:
		#print(row['collision_group_mask'])
		#if (row['collision_group_mask']) == 0.0:
			#row['collision_group_mask'] = str('0')
		if isinstance(row['collision_group_mask'], float):
			row['collision_group_mask'] = str(int(row['collision_group_mask']))
		index_values = str(row['collision_group_mask']).split('\\')
		bool_list = [str(i) in index_values for i in range(16)]
		row['collision_group_mask'] = bool_list
		#print('converted to',row['collision_group_mask'])

	return RIGID_BODY_DICTIONARY

def get_armature():
	
	if bpy.context.active_object is not None:
		if bpy.context.active_object.type == 'ARMATURE':
			return bpy.context.active_object
			#return model.findArmature(bpy.context.active_object)
	elif bpy.context.selected_objects[0] is not None:
		if model.findArmature(bpy.context.selected_objects[0]) is not None:
			return model.findArmature(bpy.context.selected_objects[0])
		for child in  bpy.context.selected_objects[0].parent.children:
			if child.type == 'ARMATURE':
				return child
		for child in  bpy.context.selected_objects[0].parent.parent.children:
			if child.type == 'ARMATURE':
				return child
	else:
		print ('could not find armature for selected object:', bpy.context.selected_objects[0].name)

def get_armature_from_rigid_body(obj):
	
	if obj is not None:
		if obj.mmd_type=='RIGID_BODY':
			return model.find_MMD_Armature(obj)

	else:
		print ('could not find armature for obj:','obj')

def apply_all_rigid_bodies(armature,rigid_body_data):
	

	if rigid_body_data: 
		for rigid_body in rigid_body_data:
			rigid_body_name = rigid_body['rigid_body_name']
			bone = rigid_body['bone_name']
			offset_loc = [rigid_body['offset_x'],rigid_body['offset_y'],rigid_body['offset_z']]
			offset_rot = [rigid_body['offset_rot_x'],rigid_body['offset_rot_y'],rigid_body['offset_rot_z']]
			reset_rot = [rigid_body['reset_rot_x'],rigid_body['reset_rot_y'],rigid_body['reset_rot_z']]
			
			name_j = rigid_body['name_j']
			name_e = rigid_body['name_e']
			collision_group_number = int(rigid_body['collision_group'])
			collision_group_mask = rigid_body['collision_group_mask']
			rigid_type = str(int(rigid_body['rigid_type'])) #'0'= Bone, '1' = Physics, '2' = Physics+Bone
			rigid_shape = rigid_body['rigid_shape']  #SPHERE, BOX, CAPSULE        
			size = [rigid_body['x'], rigid_body['y'],rigid_body['z']]  #size[0] = X, size[1] = Y, size[2] = Z
			mass = rigid_body['mass']
			friction = rigid_body['friction'] 
			bounce = rigid_body['bounce']  #restitution
			linear_damping = rigid_body['linear_damping']
			angular_damping = rigid_body['angular_damping']
			

			bpy.context.view_layer.objects.active = armature
			create_rigid_body(armature,rigid_body_name,bone,offset_loc,offset_rot,reset_rot,name_j,name_e,collision_group_number,collision_group_mask, rigid_type,rigid_shape,size,mass,friction,bounce,linear_damping,angular_damping)
	

def create_rigid_body(armature,rigid_body_name,bone,offset_loc,offset_rot,reset_rot,name_j,name_e,collision_group_number,collision_group_mask, rigid_type,rigid_shape,size,mass,friction,bounce,linear_damping,angular_damping):

	
	#if rigid body exists, delete it
	for obj in armature.parent.children_recursive:
		if obj.mmd_type == 'RIGID_BODY' and obj.name == rigid_body_name:
			print ('deleting existing rigid_body:', obj.name)
			bpy.data.objects.remove(obj, do_unlink=True)

	
	#check if bone exists
	bpy.ops.object.mode_set(mode='EDIT')
	if bone in bpy.context.active_object.data.edit_bones:


		# Select the bone		
		bpy.ops.armature.select_all(action='DESELECT')
		armature.data.edit_bones[bone].select = True
		armature.data.bones.active = armature.data.bones[bone]
			
		bpy.ops.mmd_tools.rigid_body_add(
			name_j= name_j #'$name_j'
			,name_e= name_e #'$name_e'
			,collision_group_number=collision_group_number #0
			,collision_group_mask=collision_group_mask #[True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False] 
			,rigid_type=rigid_type #'0' #'0'= Bone, '1' = Physics, '2' = Physics+Bone
			,rigid_shape=rigid_shape #[0.6, 0.6, 0.6]  #X, Y, Z
			,size=size #float
			,mass=mass #float
			,friction=friction #float
			,bounce=bounce #restitution #float
			,linear_damping=linear_damping #float
			,angular_damping=angular_damping #float
		)
		
		rigid_body = bpy.context.view_layer.objects.active

		#set rigid_body_name
		rigid_body.name = rigid_body_name

		#set the size to match what the MMD Rigid Body Panel displays as the size
		if rigid_shape == 'SPHERE':
			rigid_body.mmd_rigid.size = [max(size[0], 1e-3),0,0] #radius,y,z
		elif rigid_shape == 'BOX':
			rigid_body.mmd_rigid.size = [max(size[0], 1e-3),max(size[1] , 1e-3),max(size[2] , 1e-3)] #x,y,z
		elif rigid_shape == 'CAPSULE':
			rigid_body.mmd_rigid.size = [max(size[0], 1e-3),max(size[1], 1e-3),0] #radius,diameter,z
			
		#set the offset
		#rigid_body.delta_location.x = offset_loc[0]
		#rigid_body.delta_location.y = offset_loc[1]
		#rigid_body.delta_location.z = offset_loc[2]
		rigid_body.location.x = rigid_body.location.x + offset_loc[0]
		rigid_body.location.y = rigid_body.location.y + offset_loc[1]
		rigid_body.location.z = rigid_body.location.z + offset_loc[2]

		offset_rot_euler = mathutils.Euler((math.radians(offset_rot[0]),math.radians(offset_rot[1]),math.radians(offset_rot[2])), 'XYZ')
		

		if rigid_body.rotation_mode == 'QUATERNION':
			if reset_rot[0] =='y':
				rigid_body.rotation_quaternion[0] = 0
				rigid_body.rotation_quaternion[1] = 0
			if reset_rot[1] =='y':
				rigid_body.rotation_quaternion[2] = 0
			if reset_rot[2] =='y':
				rigid_body.rotation_quaternion[3] = 0

			offset_rot_quaternion = offset_rot_euler.to_quaternion()
			rigid_body.rotation_quaternion[0] +=  offset_rot_quaternion[0] 
			rigid_body.rotation_quaternion[1] +=  offset_rot_quaternion[1] 
			rigid_body.rotation_quaternion[2] +=  offset_rot_quaternion[2] 
			rigid_body.rotation_quaternion[3] +=  offset_rot_quaternion[3]

		if rigid_body.rotation_mode == 'AXIS_ANGLE':
			if reset_rot[0] =='y':
				rigid_body.rotation_axis_angle[0] = 0
				rigid_body.rotation_axis_angle[1] = 0
			if reset_rot[1] =='y':
				rigid_body.rotation_axis_angle[2] = 0
			if reset_rot[2] =='y':
				rigid_body.rotation_axis_angle[3] = 0

			offset_rot_axis_angle = offset_rot_euler.to_matrix()
			rigid_body.rotation_axis_angle[0] += offset_rot_axis_angle[0]
			rigid_body.rotation_axis_angle[1] += offset_rot_axis_angle[1]
			rigid_body.rotation_axis_angle[2] += offset_rot_axis_angle[2]
			rigid_body.rotation_axis_angle[3] += offset_rot_axis_angle[3]
		else:
			if reset_rot[0] =='y':
				rigid_body.rotation_euler.x = 0
			if reset_rot[1] =='y':
				rigid_body.rotation_euler.y = 0
			if reset_rot[2] =='y':
				rigid_body.rotation_euler.z = 0

			rigid_body.rotation_euler.x += offset_rot_euler[0] 
			rigid_body.rotation_euler.y += offset_rot_euler[1]
			rigid_body.rotation_euler.z += offset_rot_euler[2]


		
		print ('created rigid body: ',rigid_body.name)
		return rigid_body
	else:
		print ('bone ',bone,' does not exist')


def get_skirt_rigid_vertical_objects(obj):
	
	bpy.ops.object.mode_set(mode='OBJECT')
	
	if obj.mmd_type == 'RIGID_BODY' and obj.name.startswith('skirt_'):

		#get the skirt chain number (first number after skirt_)
		result = re.search("^skirt_(\d+)_(\d+)$", obj.name)
		if result:
			chain_number = int(result.group(1))
			print("Skirt Chain number:", chain_number )
		else:
			print("No match found.")
			
		rb_obj_chain = []
				
		armature = get_armature_from_rigid_body(obj)

		bone_name = bpy.context.active_object.mmd_rigid.bone
		rigid_bodies = None

		#get the 'rigidbodies' object
		for object in armature.parent.children:
			if object.name == 'rigidbodies':
				rigid_bodies = object
		
		if rigid_bodies is not None:
			#get all rigid bodies that have the same chain number as object that was passed
			for rigid_body in rigid_bodies.parent.children_recursive:
				#if it finds it, add it to the rb_obj_chain list
				if rigid_body.name.startswith('skirt_'+str(chain_number)+'_') and rigid_body.mmd_type == 'RIGID_BODY':
					rb_obj_chain.append(rigid_body)
		
		if rb_obj_chain is not None:
			# Deselect all objects
			bpy.ops.object.select_all(action='DESELECT')
			#select all in chain    
			for rb_obj in rb_obj_chain:
				rb_obj.select_set(True)
				
			return rb_obj_chain
				
def get_skirt_rigid_horizontal_objects(obj):
	
	bpy.ops.object.mode_set(mode='OBJECT')
	
	if obj.mmd_type == 'RIGID_BODY' and obj.name.startswith('skirt_'):
		#get the skirt chain number (last number after skirt_)
		result = re.search("^skirt_(\d+)_(\d+)$", obj.name)
		if result:
			chain_number = int(result.group(2))
			print("Skirt Chain link number:", chain_number )
		else:
			print("No match found.")
			
		rb_obj_chain = []
		
		armature = get_armature_from_rigid_body(obj)
		bone_name = bpy.context.active_object.mmd_rigid.bone
		rigid_bodies = None

		#get the 'rigidbodies' object
		for object in armature.parent.children:
			if object.name == 'rigidbodies':
				rigid_bodies = object
		
		if rigid_bodies is not None:
			#get all rigid bodies that have the same chain number as object that was passed
			for rigid_body in rigid_bodies.parent.children_recursive:
				
				#if it finds it, add it to the rb_obj_chain list
				if rigid_body.name.endswith('_'+str(chain_number)) and rigid_body.mmd_type == 'RIGID_BODY':
					rb_obj_chain.append(rigid_body)        
				
		if rb_obj_chain is not None:
			
			# Deselect all objects
			bpy.ops.object.select_all(action='DESELECT')
		
			#select all in chain    
			for rb_obj in rb_obj_chain:
				rb_obj.select_set(True)
		
			return rb_obj_chain

def get_rigid_body_list_with_number_index (rigid_body_list):

    #get all rigid bodies and the numbers contained within the name, 
    #store it on an list

    rigid_body_list_with_number_index = []

    if rigid_body_list is not None:
        for obj in rigid_body_list:
            if obj.mmd_type == 'RIGID_BODY':
                matches = re.findall(r'\d+', obj.name)
                numbers = [m for m in matches]
                rigid_body_list_with_number_index.append((obj,obj.name,numbers))

        return rigid_body_list_with_number_index

def get_grouped_rigid_body_list_by_index_position (rigid_body_list_with_index,target_index_pos):

    #print the length of index positions in grouped_rigid_body_list
    #print(len(rigid_body_list_with_index[-1][2]),' index positions for',rigid_body_list_with_index[-1][1],' :', rigid_body_list_with_index[-1][2])
    
    if rigid_body_list_with_index is not None:
        #sort the list by the values at index position [2][0] (first index)
        sorted_rigid_bodies = sorted(rigid_body_list_with_index, key=lambda x: x[2][target_index_pos])

        # Group the rigid bodies with the same value at rigid_body_name_index_values[2][selected_index_pos] into a list of lists
        grouped_rigid_body_dict_by_index_pos = {}
        for rigid_body in rigid_body_list_with_index:
            index_pos = rigid_body[2][target_index_pos]
            if index_pos in grouped_rigid_body_dict_by_index_pos:
                grouped_rigid_body_dict_by_index_pos[index_pos].append(rigid_body)
            else:
                grouped_rigid_body_dict_by_index_pos[index_pos] = [rigid_body]

                
        #convert the dictionary keys into a list
        grouped_rigid_body_list_by_index_pos = []
        
        for index_pos_value, rigid_bodies in grouped_rigid_body_dict_by_index_pos.items():
            grouped_rigid_body_list_by_index_pos.append(rigid_bodies)
            #print(f"Rigid bodies with value {index_pos_value}:")
            #for rigid_body in rigid_bodies:
                #print(rigid_body)
        
        return  grouped_rigid_body_list_by_index_pos

def select_rigid_bodies_in_grouped_list(grouped_rigid_body_list,index_pos):
    
    #deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    
    if grouped_rigid_body_list is not None:
        for i in grouped_rigid_body_list[index_pos]:
            i[0].select_set(True)


def reconstruct_string_split_by_number_index(string,indexed_values):
    
    # Split the input string into non-numeric and numeric parts
    parts = re.split(r'(\d+)', string)
    nonnumeric_parts = [p for p in parts if not p.isdigit()]
    numeric_parts = [int(p) for p in parts if p.isdigit()]

    # Replace the numeric parts with the corresponding numbers
    if len(numeric_parts) < 2:
        raise ValueError('Must be at least 2 numeric parts in name:'+string+'. Found:'+str(len(numeric_parts)))
    
    elif len(numeric_parts) == len(indexed_values):
        for i in range(len(indexed_values)):
            numeric_parts[i] = indexed_values[i]
    else:
        raise ValueError('Number of numeric parts does not match number of indexed_values')
        
    reconstructed_dict = {}
    reconstructed_dict['nonnumeric_parts'] = nonnumeric_parts
    reconstructed_dict['numeric_parts'] = numeric_parts
    

    # Concatenate the non-numeric and numeric parts to reconstruct the string
    reconstructed = ''
    for i in range(len(reconstructed_dict['nonnumeric_parts'])):
        reconstructed += reconstructed_dict['nonnumeric_parts'][i]
        #print(nonnumeric_parts[i])
        if i < len(reconstructed_dict['numeric_parts']):
            reconstructed += str(reconstructed_dict['numeric_parts'][i])
            #print(numeric_parts[i])
    
    #print('total number of numeric indexes:',len(numeric_parts))
    #print (reconstructed)
            
    return reconstructed_dict
    #return reconstructed
    
    
    

def find_rigid_bodies(startswith=None,endswith=None,contains=None,append_to_selected=None):

	bpy.ops.object.mode_set(mode='OBJECT')
	
	obj = bpy.context.active_object

	if obj.type == 'ARMATURE':
		search_scope = bpy.context.object.parent.children_recursive
	else:
		search_scope = bpy.context.object.parent.parent.children_recursive

	if startswith is None:
		startswith = ''
	if endswith is None:
		endswith = ''
	if contains is None:
		contains = ''
	if append_to_selected is None:
		append_to_selected = False

	if append_to_selected==False:
		bpy.ops.object.select_all(action='DESELECT')
		
	for obj in search_scope:
		if obj.mmd_type=='RIGID_BODY' and obj.name.startswith(str(startswith)) and obj.name.endswith(str(endswith)) and contains in obj.name:
			obj.hide=False
			obj.select_set(True)
	
	if bpy.context.selected_objects:
		bpy.context.view_layer.objects.active =  bpy.context.selected_objects[0]
		return bpy.context.selected_objects

def get_bone_from_rigid_body (obj = None):
	
	if obj is None and bpy.context.active_object is not None:
		obj = bpy.context.active_object
	
	if obj.mmd_type == 'RIGID_BODY':

		#armature_obj = get_armature() #.name #obj.constraints['mmd_tools_rigid_parent'].target.data.name   
		armature_obj = get_armature_from_rigid_body(obj)

		#print(armature_obj,":",armature_obj.name)

		rigid_body_bone_name = obj.mmd_rigid.bone
		for bone in armature_obj.data.bones:
			if bone.name == rigid_body_bone_name:
					return bone	
		
	

def get_joints_from_rigid_body (obj = None):

	if obj is None and bpy.context.active_object is not None:
		obj = bpy.context.active_object
	
	if obj.mmd_type == 'RIGID_BODY':
		print("this is a rigid body!")

	#TO BE COMPLETED


def get_rigid_body_bone_chain_origin(bone_obj,rigid_body_bone_list=None):
	
	#because changing between edit mode and object mode messes all ID references up, need to do it first
	#need to store the NAME, not the object or data
	active_object = bpy.context.view_layer.objects.active
	rigid_body_bone_name = bone_obj.name
	armature_name = bone_obj.id_data.name

	
	
	if bpy.data.objects[armature_name].type != 'ARMATURE':
		for child in bpy.data.objects[armature_name].children:
			if child.type == 'ARMATURE':
				armature_name=child.name
				break

	#start mmd_bone_use_connect stuff
	bone_list = []

	
	#unhide the armature so we can find the bones we need
	armature_obj = bpy.data.objects.get(armature_name)
	is_armature_hidden = armature_obj.hide
	if armature_obj.hide == True:
		armature_obj.hide = False
		
	bpy.context.view_layer.objects.active = armature_obj
	bpy.ops.object.mode_set(mode='EDIT')
	
	#bpy.context.active_object.data.edit_bones['skirt_12_1'].get('mmd_bone_use_connect')
	for bone in bpy.context.active_object.data.edit_bones:
		if bone not in bone_list:
			blender_use_connect_flag = bone.use_connect
			mmd_use_connect_flag = bone.get('mmd_bone_use_connect')
			use_connect = None
			
			#get the appropriate use_connect flag regardless if physics is on or off
			if mmd_use_connect_flag == None:
				use_connect = blender_use_connect_flag  
			elif mmd_use_connect_flag == 1:
				use_connect = True
			else:
				use_connect = False
					
			bone_list.append((bone.name,use_connect))    

	bpy.ops.object.mode_set(mode='OBJECT')    
	#end mmd_bone_use_connect stuff

	#initialize all variables to what they were before edit mode
	bpy.context.view_layer.objects.active = active_object
	armature_obj = bpy.data.objects[armature_name]
	armature = armature_obj.data
	rigid_body_bone = armature.bones[rigid_body_bone_name]
	
	#performance increase
	if rigid_body_bone_list == None:
		rigid_body_bone_list = get_rigid_body_bone_list(armature_obj)


	rigid_body_bone_origin = rigid_body_bone

	##Arbitrary number to make sure the while loop definitely exits at some point         
	i = 100
	while i >= 0:
		
		has_rigid_body = False
		has_only_one_child_bone = True
		has_use_connect_false = True
		
		#check if bone has a rigid body and if physics is on for it
		for bone in rigid_body_bone_list:
			if rigid_body_bone.name == bone[2]:
				has_rigid_body = True
				break
			
		###TO DO - check if bone has only ONE rigid body
			
		#check if bone's parent has only one child
		for siblings in rigid_body_bone.parent.children:
			if siblings.name != rigid_body_bone.name:
				has_only_one_child_bone = False
				break
				
		#check if bone is not connected physically to another bone
		for bone in bone_list:
			if bone[0] == armature.bones[rigid_body_bone.name]:
				#if use_connect flag is false
				if bone[1] == False:
				#if (armature.bones[rigid_body_bone.name].use_connect) == False:
					has_use_connect_false = False
				break
		
		rigid_body_bone = rigid_body_bone.parent
		
		if has_rigid_body == True and has_only_one_child_bone == True and has_use_connect_false == True:
			rigid_body_bone_origin = rigid_body_bone
		else:
			break
		i = i-1
		
	#return the hidden flag if armature was hidden prior to running this function
	armature_obj.hide = is_armature_hidden

	return rigid_body_bone_origin


def get_rigid_body_bone_list(obj):

	#armature_obj = bpy.data.objects.get(rigid_body_bone_origin.id_data.name)
	root = model.findRoot(obj)

	rigid_body_bone_list = []
	
	#get all the rigid bodies in the root object
	for obj in root.children_recursive: #armature_obj.parent.children_recursive:
		if obj.mmd_type == 'RIGID_BODY':
			rigid_body_bone_list.append((obj,obj.name,obj.mmd_rigid.bone))

	return rigid_body_bone_list


def select_rigid_body_bone_chain_from_bone(rigid_body_bone_origin,rigid_body_bone_list=None,current_bone_name=None):

	#print('rigid body bone origin:',rigid_body_bone_origin, ' current bone: ',current_bone_name)



	#performance increase
	if rigid_body_bone_list is None:
		rigid_body_bone_list = get_rigid_body_bone_list(rigid_body_bone_origin)


	#set the first in the rigid body bone chain list to the bone origin
	for rigid_body in rigid_body_bone_list:
		if rigid_body[2] == rigid_body_bone_origin.name:
			rigid_body[0].select_set(True)
			break
							
	#starting from origin, select all children
	for bone_child in rigid_body_bone_origin.children_recursive:
		#if the bone_child is on the rigid body bone list, add it
		for rigid_body in rigid_body_bone_list:
			if rigid_body[2] == bone_child.name:
				rigid_body[0].select_set(True)
				#prevents the for loop from going any further than the current bone
				if bone_child.name == current_bone_name:
					return

	
	
	
def get_rigid_body_chain_from_bone(rigid_body_bone_origin):
	
	
	armature_obj = bpy.data.objects.get(rigid_body_bone_origin.id_data.name)
	root = model.findRoot(armature_obj)
	rigid_body_bone_list = []
	
	#get all the rigid bodies in the root object
	for obj in root.children_recursive: #armature_obj.parent.children_recursive:
		if obj.mmd_type == 'RIGID_BODY':
			rigid_body_bone_list.append((obj,obj.name,obj.mmd_rigid.bone))

	rigid_body_bone_chain = []
	

	#set the first in the rigid body bone chain list to the bone origin
	for rigid_body in rigid_body_bone_list:
			if rigid_body[2] == rigid_body_bone_origin.name:
				rigid_body_bone_chain.append((rigid_body[0],rigid_body_bone_origin))
				rigid_body[0].select_set(True)
				
	#add all children to the bone chain        
	for bone_child in rigid_body_bone_origin.children_recursive:
		for rigid_body in rigid_body_bone_list:
			if rigid_body[2] == bone_child.name:
				rigid_body_bone_chain.append((rigid_body[0],bone_child))                
				rigid_body[0].select_set(True)

	unique_bones = []
	sorted_unique_bones = []

	#sort the bones in order from parent to child (we'll need this in a later function for specifying min/max values
	for i in rigid_body_bone_chain:
		if i[1] not in unique_bones:
			unique_bones.append(i[1])            
			
	for i,bone in enumerate(unique_bones):
		sorted_unique_bones.append((i,bone))
		
	sorted_rigid_body_bone_chain = []

	#sort the rigid bodies in order from bone parent to child
	for i,item in enumerate(rigid_body_bone_chain):
		for bone in sorted_unique_bones:
			if item[1]==bone[1]:
				sorted_rigid_body_bone_chain.append((bone[0],bone[1],i,item[0]))
				
	return sorted_rigid_body_bone_chain
	
def is_selected_rigid_bodies_in_a_bone_chain ():

	is_selected_a_bone_chain = True
	selected_objs = None

	if bpy.context.selected_objects is not None:
		selected_objs = bpy.context.selected_objects
	
	#check if all selected are rigid bodies
	if selected_objs is not None:
		for obj in selected_objs:
			if obj.mmd_type != 'RIGID_BODY':
				#print ('selected obj:',obj.name,' is not a rigid body')
				is_selected_a_bone_chain = False
				return False

	bone_list = []

	#check if all selected objects have an associated bone
	for obj in selected_objs:			
		bone = None
		bone = get_bone_from_rigid_body(obj)
		if bone is None:
			#print ('selected obj:',obj.name,' does is not attached to a bone')
			is_selected_a_bone_chain = False
			return False
		else:
			if bone not in bone_list:
				bone_list.append(bone)
			
	#check if there is at least two bones in bone list
	if len(bone_list) < 2:
		#print ('at least two bones from rigid bodies must be selected')
		is_selected_a_bone_chain = False
		return False

	#check if all the bones are in a parent/child relationship
	for i in range(len(bone_list)-1):
		if bone_list[i+1].parent != bone_list[i]:
			#print ('rigid body:', selected_objs[i+1].name, ' bone:', bone_list[i+1].name, ' is not in a bone chain')
			is_selected_a_bone_chain = False
			return False

	return is_selected_a_bone_chain

def get_selected_rigid_bodies_in_bone_chain (rigid_body_bone_chain=None):
	
	if(is_selected_rigid_bodies_in_a_bone_chain()):

		selected_objs = None

		if bpy.context.selected_objects is not None:
			selected_objs = bpy.context.selected_objects

		bone_list = []
		rigid_body_bone_chain = []
		
		#check if all selected objects have an associated bone
		for obj in selected_objs:			
			bone = None
			bone = get_bone_from_rigid_body(obj)
			rigid_body = obj
			if bone is None:
				print ('selected obj:',obj.name,'  is not attached to a bone')
				is_selected_a_bone_chain = False
				return False
			else:
				bone_list.append(bone)
				rigid_body_bone_chain.append((rigid_body,bone.name))

		# Sort bone_list from parent to child
		sorted_bone_list = [bone_list[0]]
		current_bone = bone_list[0]
		while current_bone.children:
			current_bone = current_bone.children[0]
			sorted_bone_list.append(current_bone)
		
		#enumerate the bone list
		enumerated_bone_list = []
		for i,bone in enumerate(sorted_bone_list):
			enumerated_bone_list.append((i,bone.name))    

		#append the bone order to the rigid body list
		sorted_rigid_body_bone_chain = []
		for bone in enumerated_bone_list:
			for rigid_body in rigid_body_bone_chain:
				if rigid_body[1] == bone[1]:
					sorted_rigid_body_bone_chain.append((bone[0],bone[1],rigid_body[0]))
					
		return sorted_rigid_body_bone_chain
        
def get_all_rigid_body_chains_from_selected():

	selected_objs = bpy.context.selected_objects
	unsorted_bones = []

	#get all bones from the selected objects
	for obj in selected_objs:
		if obj.mmd_type == 'RIGID_BODY':
			bone = get_bone_from_rigid_body(obj)
			if bone not in unsorted_bones:
				unsorted_bones.append(bone)

	selected_bones = unsorted_bones
	selected_bone_names = set(b.name for b in selected_bones)

	#get the parent bones of the all the rigid body chains
	for bone in selected_bones:
		for child in bone.children_recursive:
			if child.name in selected_bone_names:
				selected_bone_names.remove(child.name)

	selected_parent_bones = [b for b in selected_bones if b.name in selected_bone_names]

	rigid_body_bone_chains = []
	
	for parent_bone in selected_parent_bones:
		rigid_body_chain = get_rigid_body_chain_from_bone(parent_bone)
		#remove the third column and format it to make it like the other rigid_body_bone_chain variables used by the transform_rigid_body functions
		new_rigid_body_chain = [(x[0], x[1].name, x[3]) for x in rigid_body_chain]
		rigid_body_bone_chains.append(new_rigid_body_chain)

	return rigid_body_bone_chains

def get_all_rigid_body_chains_dictionary(rigid_body_bone_chains):

	rigid_body_bone_chains_data = {}

	#for each rigid body bone chain, get the head and tail metadata
	for i, chain in enumerate(rigid_body_bone_chains):
		start_rigid_body = chain[0][2] # get the data for the first rigid body in the chain
		start_rigid_body_data = get_rigid_body_transform_data(start_rigid_body)
		end_rigid_body = chain[-1][2]  # get the data for the last rigid body in the chain
		end_rigid_body_data = get_rigid_body_transform_data(end_rigid_body)
		chain_length = int(len(chain)/2)
		chain_data = {
			"head": start_rigid_body_data,
			"tail": end_rigid_body_data,
			"chain_length": chain_length,
			"chain_data": chain
		}
		rigid_body_bone_chains_data[i] = chain_data

	return rigid_body_bone_chains_data
		
def get_rigid_body_transform_data(obj):
	
	rigid_body_dict = {
	
		'armature':None
		,'bone':None
		,'rigid_body': None
		,'location_x': None
		,'location_y': None
		,'location_z':None
		,'rotation_mode':None
		,'rotation_w':None
		,'rotation_x':None
		,'rotation_y':None
		,'rotation_z':None
		,'size_x':None
		,'size_y':None
		,'size_z':None
		,'rigid_body_type':None
		,'rigid_body_shape':None
		,'mass':None
		,'restitution':None
		,'collision_group_number':None
		,'collision_group_mask':None
		,'friction':None
		,'linear_damping':None
		,'angular_damping':None
		}

	properties = [

			('location_x','location','.x'),
			('location_y','location','.y'),
			('location_z', 'location','.z'),
			('rotation_mode','rotation_mode',''),
			('rotation_w','rotation_quaternion','.w'),
			('rotation_x','rotation_quaternion','.x'),
			('rotation_y','rotation_quaternion','.y'),
			('rotation_z','rotation_quaternion','.z'),
			('rotation_w','rotation_axis_angle','[0]'),
			('rotation_x','rotation_axis_angle','[1]'),
			('rotation_y','rotation_axis_angle','[2]'),
			('rotation_z','rotation_axis_angle','[3]'),
			#('rotation_w','rotation_euler','.w'),
			('rotation_x','rotation_euler','.x'),
			('rotation_y','rotation_euler','.y'),
			('rotation_z','rotation_euler','.z'),
			('size_x','mmd_rigid.size','[0]'),
			('size_y','mmd_rigid.size','[1]'),
			('size_z','mmd_rigid.size','[2]'),
			('rigid_body_type','mmd_rigid.type',''),
			('rigid_body_shape','mmd_rigid.shape',''),
			('mass','rigid_body.mass',''),
			('collision_group_number','mmd_rigid.collision_group_number',''),
			('collision_group_mask','mmd_rigid.collision_group_mask',''),
			('restitution','rigid_body.restitution',''),
			('friction','rigid_body.friction',''),
			('linear_damping','rigid_body.linear_damping',''),
			('angular_damping','rigid_body.angular_damping','')]

	if obj.mmd_type == 'RIGID_BODY':
		
		
		#armature_obj = get_armature() #obj.constraints['mmd_tools_rigid_parent'].target.data.name   
		armature_obj = get_armature_from_rigid_body(obj)		
		armature = armature_obj.data

		#armature = bpy.data.armatures[armature_obj]        
		rigid_body_dict['armature'] = armature
		bone = obj.mmd_rigid.bone
		rigid_body_dict['bone'] = bone
		rigid_body_dict['rigid_body'] = obj

		for prop_name,ext_property,suffix in properties:
			
			if prop_name in ['rotation_w','rotation_x','rotation_y','rotation_z']:
				if rigid_body_dict['rotation_mode'] in ('QUATERNION','AXIS_ANGLE'):
					rigid_body_dict[prop_name] = get_attribute(obj, ext_property + suffix)
				
				elif rigid_body_dict['rotation_mode'] not in ('QUATERNION','AXIS_ANGLE') and rigid_body_dict['rotation_mode'] is not None:
					if prop_name in ['rotation_x','rotation_y','rotation_z']:
						rigid_body_dict[prop_name] = get_attribute(obj, ext_property + suffix)
					if prop_name in ['rotation_w']:
						rigid_body_dict['rotation_w']=0

			else:
				rigid_body_dict[prop_name] = get_attribute(obj, ext_property + suffix)

		return rigid_body_dict

def transform_rigid_body(obj=None
						,location_x=None,location_y=None,location_z=None
						,rotation_mode=None,rotation_w=None,rotation_x = None,rotation_y=None,rotation_z=None
						,size_x=None,size_y=None,size_z=None
						,rigid_body_type=None, rigid_body_shape=None,mass=None,restitution=None
						,collision_group_number=None, collision_group_mask=None, friction=None
						,linear_damping=None,angular_damping=None):


	if obj is None and bpy.context.active_object is not None:
		if bpy.context.active_object.mmd_type == 'RIGID_BODY':
			obj=bpy.context.active_object

	if location_x is not None:
		obj.location.x = location_x
	if location_y is not None:
		obj.location.y = location_y
	if location_z is not None:
		obj.location.z = location_z
	if rotation_mode is not None:
		obj.rotation_mode = rotation_mode
	if rotation_w is not None:
		if obj.rotation_mode == 'QUATERNION':
			obj.rotation_quaternion.w = rotation_w
		elif obj.rotation_mode == 'AXIS_ANGLE':
			obj.rotation_axis_angle.w = rotation_w
	if rotation_x is not None:
		if obj.rotation_mode == 'QUATERNION':
			obj.rotation_quaternion.x = rotation_x
		elif obj.rotation_mode == 'AXIS_ANGLE':
			obj.rotation_axis_angle.x = rotation_x
		else:
			obj.rotation_euler.x = rotation_x
	if rotation_y is not None:
		if obj.rotation_mode == 'QUATERNION':
			obj.rotation_quaternion.y = rotation_y
		elif obj.rotation_mode == 'AXIS_ANGLE':
			obj.rotation_axis_angle.y = rotation_y
		else:
			obj.rotation_euler.y = rotation_y
	if rotation_z is not None:
		if obj.rotation_mode == 'QUATERNION':
			obj.rotation_quaternion.z = rotation_z
		elif obj.rotation_mode == 'AXIS_ANGLE':
			obj.rotation_axis_angle.z = rotation_z
		else:
			obj.rotation_euler.z = rotation_z

	if rigid_body_shape is not None:
		#BOX
		#SPHERE
		#CAPSULE
		obj.mmd_rigid.shape = rigid_body_shape

	
	if (size_x is not None or size_y is not None or size_z is not None):
		if size_x is None:
			size_x = obj.mmd_rigid.size[0]    
		if size_y is None:
			size_y = obj.mmd_rigid.size[1]    
		if size_z is None:
			size_z = obj.mmd_rigid.size[2] 
		obj.mmd_rigid.size = [max(size_x, 1e-3),max(size_y , 1e-3),max(size_z, 1e-3)]
	
	"""
	if size_x is not None:
		obj.mmd_rigid.size[0]  = size_x
	if size_y is not None:
		obj.mmd_rigid.size[1]  = size_y
	if size_z is not None:
		obj.mmd_rigid.size[2]  = size_z
	"""
	if rigid_body_type is not None:
		obj.mmd_rigid.type = rigid_body_type
		#'0' = bone
		#'1' = physics
		#'2' = physics+bone
	if mass is not None:
		obj.rigid_body.mass = max(0,mass)
	if restitution is not None:
		obj.rigid_body.restitution = max(0,restitution)
	if collision_group_number is not None:
		obj.mmd_rigid.collision_group_number = collision_group_number
	if collision_group_mask is not None:
		obj.mmd_rigid.collision_group_mask = collision_group_mask
		#collision_group_mask = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
	if friction is not None:
		obj.rigid_body.friction = max(0,friction)
	if linear_damping is not None:
		obj.rigid_body.linear_damping = max(0,linear_damping)
	if angular_damping is not None:
		obj.rigid_body.angular_damping = max(0,angular_damping)



def transform_selected_rigid_bodies(
									location_x=None,location_y=None,location_z=None
									,rotation_mode=None, rotation_w=None, rotation_x = None,rotation_y=None,rotation_z=None
									,size_x=None,size_y=None,size_z=None
									,rigid_body_type=None, rigid_body_shape=None,mass=None,restitution=None
									,collision_group_number=None, collision_group_mask=None, friction=None
									,linear_damping=None,angular_damping=None):
	
	selected_objects = bpy.context.selected_objects
	
	is_all_rigid_bodies = True
	
	for sel_objs in selected_objects:
		if sel_objs.mmd_type != 'RIGID_BODY':
			is_all_rigid_bodies = False
			
	if is_all_rigid_bodies:        
		for obj in selected_objects:

			transform_rigid_body(obj
								,location_x=location_x,location_y=location_y,location_z=location_z
								,rotation_mode=rotation_mode,rotation_w=rotation_w,rotation_x=rotation_x,rotation_y=rotation_y,rotation_z=rotation_z
								,size_x=size_x,size_y=size_y,size_z=size_z
								,rigid_body_type=rigid_body_type, rigid_body_shape=rigid_body_shape,mass=mass,restitution=restitution
								,collision_group_number=collision_group_number, collision_group_mask=collision_group_mask, friction=friction
								,linear_damping=linear_damping,angular_damping=angular_damping)

	else: 
		print('Not all selected objects are rigid bodies. Select only rigid bodies')
	
def transform_rigid_body_bone_chain(rigid_body_bone_chain
									,location_x_start=None,location_x_end=None
									,location_y_start=None,location_y_end=None
									,location_z_start=None,location_z_end=None
									,rotation_w_start=None,rotation_w_end=None
									,rotation_x_start=None,rotation_x_end=None
									,rotation_y_start=None,rotation_y_end=None
									,rotation_z_start=None,rotation_z_end=None
									,size_x_start=None,size_x_end=None
									,size_y_start=None,size_y_end=None
									,size_z_start=None,size_z_end=None
									,mass_start=None,mass_end=None
									,restitution_start=None,restitution_end=None
									,friction_start=None,friction_end=None
									,linear_damping_start=None,linear_damping_end=None
									,angular_damping_start=None,angular_damping_end=None
									):
	
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'location_x',location_x_start,location_x_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'location_y',location_y_start,location_y_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'location_z',location_z_start,location_z_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'rotation_w',rotation_w_start,rotation_w_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'rotation_x',rotation_x_start,rotation_x_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'rotation_y',rotation_y_start,rotation_y_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'rotation_z',rotation_z_start,rotation_z_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'size_x',size_x_start,size_x_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'size_y',size_y_start,size_y_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'size_z',size_z_start,size_z_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'mass',mass_start,mass_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'restitution',restitution_start,restitution_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'friction',friction_start,friction_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'linear_damping',linear_damping_start,linear_damping_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'angular_damping',angular_damping_start,angular_damping_end)


def transform_rigid_body_bone_chain_property(rigid_body_bone_chain,prop,start_value,end_value):

	#get all the unique bones from the rigid body bone chain
	bone_list = []
	for obj in rigid_body_bone_chain:
		if obj[1] not in bone_list:
			bone_list.append((obj[0],obj[1]))
	
	num_objects = len(bone_list)

	# Loop through the list of objects and set the value for each one
	prop_list = []
	if start_value is not None and end_value is not None:
		current_value = start_value
		value_increment = (end_value - start_value) / (num_objects - 1)
		for obj in bone_list:
			prop_list.append((obj[0],obj[1],current_value))
			current_value += value_increment

		#transform each rigid body value
		for rigid_body in rigid_body_bone_chain:
			for bone in prop_list:
				if rigid_body[1] == bone[1]:
					transform_rigid_body(obj=rigid_body[2], **{prop: bone[2]})
					break


def reset_rigid_body_location_to_bone(rigid_body_obj):

		if rigid_body_obj.mmd_type == 'RIGID_BODY':

			active_obj = bpy.context.active_object
			bone = get_bone_from_rigid_body(rigid_body_obj)

			if bpy.data.objects[bone.id_data.name].type != 'ARMATURE':
				for obj in bpy.data.objects[bone.id_data.name].children_recursive:
					if obj.type == 'ARMATURE':
						armature_obj = obj
						break
			else:
				armature_obj = bpy.data.objects[bone.id_data.name]

			if (armature_obj.type == 'ARMATURE'):
				
				is_armature_hidden = armature_obj.hide
				if armature_obj.hide == True:
					armature_obj.hide = False
				
				bpy.context.view_layer.objects.active= armature_obj
				bpy.ops.object.mode_set(mode='EDIT')
				ebone = armature_obj.data.edit_bones[bone.name]
				#print(bone.type)

				transform_rigid_body(obj=rigid_body_obj
									,location_x=(ebone.head.x + ebone.tail.x) /2
									,location_y=(ebone.head.y + ebone.tail.y) /2
									,location_z=(ebone.head.z + ebone.tail.z) /2
									)
									
				bpy.ops.object.mode_set(mode='OBJECT')
				armature_obj.select_set(False)
				armature_obj.hide = is_armature_hidden
				
			bpy.context.view_layer.objects.active = active_obj

def reset_rigid_body_rotation_to_bone(rigid_body_obj):

		if rigid_body_obj.mmd_type == 'RIGID_BODY':

			active_obj = bpy.context.active_object
			bone = get_bone_from_rigid_body(rigid_body_obj)
			
			if bpy.data.objects[bone.id_data.name].type != 'ARMATURE':
				for obj in bpy.data.objects[bone.id_data.name].children_recursive:
					if obj.type == 'ARMATURE':
						armature_obj = obj
						break
			else:
				armature_obj = bpy.data.objects[bone.id_data.name]

			if (armature_obj.type == 'ARMATURE'):
				is_armature_hidden = armature_obj.hide
				if armature_obj.hide == True:
					armature_obj.hide = False

				bpy.context.view_layer.objects.active= armature_obj
				bpy.ops.object.mode_set(mode='EDIT')
				rot = bone.matrix_local.to_euler('YXZ')
				rot.rotate_axis('X', math.pi/2)

				transform_rigid_body(obj=rigid_body_obj
									,rotation_mode="YXZ"
									,rotation_x=rot[0]
									,rotation_y=rot[1]
									,rotation_z=rot[2]
									)
									
				bpy.ops.object.mode_set(mode='OBJECT')
				armature_obj.select_set(False)
				armature_obj.hide = is_armature_hidden
			
			else:
				print('this is not a rigid body!')
			
			bpy.context.view_layer.objects.active = active_obj

def _transform_rigid_body_bone_chain(self,context):

	rigid_body_bone_chain = get_selected_rigid_bodies_in_bone_chain()

	transform_rigid_body_bone_chain(
						rigid_body_bone_chain=rigid_body_bone_chain,
						location_x_start=self.location_x_start if self.location_x_edit else None,
						location_x_end=self.location_x_end if self.location_x_edit else None,
						location_y_start=self.location_y_start if self.location_y_edit else None,
						location_y_end=self.location_y_end if self.location_y_edit else None,
						location_z_start=self.location_z_start if self.location_z_edit else None,
						location_z_end=self.location_z_end if self.location_z_edit else None,
						rotation_w_start=self.rotation_w_start if self.rotation_w_edit else None,
						rotation_w_end=self.rotation_w_end if self.rotation_w_edit else None,
						rotation_x_start=self.rotation_x_start if self.rotation_x_edit else None,
						rotation_x_end=self.rotation_x_end if self.rotation_x_edit else None,
						rotation_y_start=self.rotation_y_start if self.rotation_y_edit else None,
						rotation_y_end=self.rotation_y_end if self.rotation_y_edit else None,
						rotation_z_start=self.rotation_z_start if self.rotation_z_edit else None,
						rotation_z_end=self.rotation_z_end if self.rotation_z_edit else None,
						size_x_start=self.size_x_start if self.size_x_edit else None,
						size_x_end=self.size_x_end if self.size_x_edit else None,
						size_y_start=self.size_y_start if self.size_y_edit else None,
						size_y_end=self.size_y_end if self.size_y_edit else None,
						size_z_start=self.size_z_start if self.size_z_edit else None,
						size_z_end=self.size_z_end if self.size_z_edit else None,
	)

def create_rigid_bodies_from_csv(context):

	active_obj = bpy.context.active_object
	armature = model.find_MMD_Armature(active_obj)
	bpy.context.view_layer.objects.active = armature 

	RIGID_BODY_DICTIONARY = read_rigid_body_file ()
	
	apply_all_rigid_bodies(armature, RIGID_BODY_DICTIONARY)
	#apply_all_rigid_bodies(armature)

@register_wrap
class AddRigidBodyFromFile(bpy.types.Operator):
	"""Add Rigid Bodies to a FFXIV Model (Converted to an MMD Model)"""
	bl_idname = "ffxiv_mmd_tools_helper.create_rigid_bodies_from_csv"
	bl_label = "Add Rigid Bodies from CSV"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		root = mmd_model.Model.findRoot(obj)
		return obj is not None and obj.type == 'ARMATURE' and root is not None

	def execute(self, context):
		create_rigid_bodies_from_csv(context)
		return {'FINISHED'}


@register_wrap
class SelectSkirtRigidBodies(bpy.types.Operator):
	"""Select Rigid Bodies in a skirt """
	bl_idname = "ffxiv_mmd_tools_helper.select_skirt_rigid_bodies"
	bl_label = "Select All Skirt Rigid Bodies"
	bl_options = {'REGISTER', 'UNDO'}

	direction = bpy.props.EnumProperty(items = \
	[('ALL', 'ALL', 'ALL')\
		,('VERTICAL','VERTICAL','VERTICAL')
		,('HORIZONTAL', 'HORIZONTAL', 'HORIZONTAL')\
	], name = "", default = 'ALL')

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.mmd_type == 'RIGID_BODY' and obj.name.startswith('skirt_')

	def execute(self, context):

		if self.direction == 'ALL':
			find_rigid_bodies(startswith='skirt_')
		elif self.direction == 'VERTICAL':
			get_skirt_rigid_vertical_objects(context.active_object)
		elif self.direction == 'HORIZONTAL':
			get_skirt_rigid_horizontal_objects(context.active_object)
		return {'FINISHED'}

@register_wrap
class GetBoneFromRigidBody(bpy.types.Operator):
	"""Get Bone From Active Rigid Body """
	bl_idname = "ffxiv_mmd_tools_helper.get_bone_from_rigid_body"
	bl_label = "Get Bone From Active Rigid Body "
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.mmd_type == 'RIGID_BODY'

	def execute(self, context):
		obj = context.active_object
		bone = get_bone_from_rigid_body(obj)
		bones_renamer.find_bone_names(startswith=bone.name, endswith=bone.name,append_to_selected=False)
		return {'FINISHED'}

@register_wrap
class ResetLocationRigidBodies(bpy.types.Operator):
	"""Reset Location of selected Rigid Bodies back to match bone """
	bl_idname = "ffxiv_mmd_tools_helper.reset_location_rigid_bodies"
	bl_label = "Reset the Location of Rigid Bodies back to bone"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.mmd_type == 'RIGID_BODY'

	def execute(self, context):
		selected_objs = bpy.context.selected_objects
		for obj in selected_objs:
			reset_rigid_body_location_to_bone(obj)
		return {'FINISHED'}

@register_wrap
class ResetRotationRigidBodies(bpy.types.Operator):
	"""Reset Rotation of selected Rigid Bodies back to match bone """
	bl_idname = "ffxiv_mmd_tools_helper.reset_rotation_rigid_bodies"
	bl_label = "Reset the Rotation of Rigid Bodies back to bone"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.mmd_type == 'RIGID_BODY'

	def execute(self, context):
		selected_objs = bpy.context.selected_objects
		for obj in selected_objs:
			reset_rigid_body_rotation_to_bone(obj)
		return {'FINISHED'}

@register_wrap
class FindRigidBodies(bpy.types.Operator):
	"""Find Rigid Bodies """
	bl_idname = "ffxiv_mmd_tools_helper.find_rigid_bodies"
	bl_label = "Find Rigid Bodies"
	bl_options = {'REGISTER', 'UNDO'}

	append_to_selected = bpy.props.BoolProperty(name="Append", default=False)
	bpy.types.Scene.rigidbody_startswith = bpy.props.StringProperty(name="", description="", default="", maxlen=0, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)
	bpy.types.Scene.rigidbody_endswith = bpy.props.StringProperty(name="", description="", default="", maxlen=0, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)
	bpy.types.Scene.rigidbody_contains = bpy.props.StringProperty(name="", description="", default="", maxlen=0, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None

	def execute(self, context):
		find_rigid_bodies(startswith=context.scene.rigidbody_startswith,endswith=context.scene.rigidbody_endswith,contains=context.scene.rigidbody_contains,append_to_selected=self.append_to_selected)
		return {'FINISHED'}

@register_wrap
class ClearFindRigidBodies(bpy.types.Operator):
	"""Clear Find Rigid Bodies """
	bl_idname = "ffxiv_mmd_tools_helper.clear_find_rigid_bodies"
	bl_label = "Clear Find Rigid Bodies"

	def execute(self, context):
		context.scene.rigidbody_startswith = ''
		context.scene.rigidbody_endswith = ''
		context.scene.rigidbody_contains = ''
		return {'FINISHED'}

#from mmd_tools.operators.rigid_body import AddRigidBody

@register_wrap
class CreateRigidBodies(bpy.types.Operator):
	"""Create Rigid Bodies From Selected Bones"""
	bl_idname = "ffxiv_mmd_tools_helper.create_rigid_bodies"
	bl_label = "Create Rigid Bodies From Selected Bones"

	@classmethod
	def poll(cls, context):
		active_obj = context.active_object
		is_active_a_bone = True
		is_in_edit_or_pose_mode = True
		
		if bpy.context.object.mode not in ('EDIT','POSE'):
			is_in_edit_or_pose_mode = False

		if active_obj.type != 'ARMATURE':
			is_active_a_bone = False

		return is_active_a_bone and is_in_edit_or_pose_mode

	def execute(self, context):
		bpy.ops.mmd_tools.rigid_body_add('INVOKE_DEFAULT')
		return {'FINISHED'}



@register_wrap
class SelectRigidBodyBoneChain(bpy.types.Operator):
	"""Get Rigid Bodies From Bone Chain"""
	bl_idname = "ffxiv_mmd_tools_helper.select_rigid_body_bone_chain"
	bl_label = "Get Rigid Bodies From Bone Chain"

	direction: bpy.props.EnumProperty(items = \
	[('ALL', 'ALL', 'ALL')\
		,('UP','UP','UP')
		,('DOWN', 'DOWN', 'DOWN')\
	], name = "", default = 'DOWN')

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.mmd_type == 'RIGID_BODY'

	def execute(self, context):

		if bpy.context.selected_objects:
			selected_objs = context.selected_objects

			rigid_body_bone_list = get_rigid_body_bone_list(context.active_object)

			for obj in selected_objs:
				if obj.mmd_type == 'RIGID_BODY':
					#print (obj.name)
					bone = get_bone_from_rigid_body(obj)
					bone_name = bone.name
					if self.direction == 'DOWN':
						#get_rigid_body_chain_from_bone(bone)
						select_rigid_body_bone_chain_from_bone(bone,rigid_body_bone_list)
						
					elif self.direction == 'ALL':
						bone_chain_origin = get_rigid_body_bone_chain_origin(bone)
						#get_rigid_body_chain_from_bone(bone_chain_origin)
						select_rigid_body_bone_chain_from_bone(bone_chain_origin,rigid_body_bone_list)

					elif self.direction == 'UP':
						bone_chain_origin = get_rigid_body_bone_chain_origin(bone)
						select_rigid_body_bone_chain_from_bone(bone_chain_origin,rigid_body_bone_list,bone_name)

		return {'FINISHED'}


def _transform_selected_rigid_bodies(self,context):
	if BatchUpdateRigidBodies.initialization == True:
		if context.active_object is not None:

			obj = context.active_object 
			if obj.mmd_type == 'RIGID_BODY':

				root = model.findRoot(obj)
				if root.mmd_root.is_built == False:


						transform_rigid_body(
							obj=obj,
							location_x=self.location_x if self.location_x_edit == False else None,
							location_y=self.location_y if self.location_y_edit == False else None,
							location_z=self.location_z if self.location_z_edit == False  else None,
							rotation_mode=self.rotation_mode if self.rotation_mode_edit == False  else None,
							rotation_w=self.rotation_w if self.rotation_w_edit == False  else None,
							rotation_x=self.rotation_x if self.rotation_x_edit == False  else None,
							rotation_y=self.rotation_y if self.rotation_y_edit == False else None,
							rotation_z=self.rotation_z if self.rotation_z_edit == False else None,
							rigid_body_shape=obj.mmd_rigid.shape if self.rigid_body_shape_edit == False else None,
							size_x=self.size_x if self.size_x_edit == False else None,
							size_y=self.size_y if self.size_y_edit == False else None,
							size_z=self.size_z if self.size_z_edit == False else None,
						)


						transform_selected_rigid_bodies(
							location_x=self.location_x if self.location_x_edit else None,
							location_y=self.location_y if self.location_y_edit else None,
							location_z=self.location_z if self.location_z_edit else None,
							rotation_mode=self.rotation_mode if self.rotation_mode_edit else None,
							rotation_w=self.rotation_w if self.rotation_w_edit else None,
							rotation_x=self.rotation_x if self.rotation_x_edit else None,
							rotation_y=self.rotation_y if self.rotation_y_edit else None,
							rotation_z=self.rotation_z if self.rotation_z_edit else None,
							rigid_body_shape=obj.mmd_rigid.shape if self.rigid_body_shape_edit else None,
							size_x=self.size_x if self.size_x_edit else None,
							size_y=self.size_y if self.size_y_edit else None,
							size_z=self.size_z if self.size_z_edit else None,
						)





@register_wrap
class BatchUpdateRigidBodies(bpy.types.Operator):
	""" Bulk Update all Selected Rigid Bodies using the Active Rigid Body """
	bl_idname = "ffxiv_mmd_tools_helper.batch_update_rigid_bodies"
	bl_label = "Batch Update Rigid Bodies"
	bl_options = {'REGISTER','UNDO','PRESET'} 

	initialization=False

	#checkbox to bulk edit
	location_x_edit: bpy.props.BoolProperty(default=False)
	location_y_edit: bpy.props.BoolProperty(default=False)
	location_z_edit: bpy.props.BoolProperty(default=False)
	rotation_mode_edit: bpy.props.BoolProperty(default=False)
	rotation_w_edit: bpy.props.BoolProperty(default=False)
	rotation_x_edit: bpy.props.BoolProperty(default=False)
	rotation_y_edit: bpy.props.BoolProperty(default=False)
	rotation_z_edit: bpy.props.BoolProperty(default=False)
	size_x_edit: bpy.props.BoolProperty(default=False)
	size_y_edit: bpy.props.BoolProperty(default=False)
	size_z_edit: bpy.props.BoolProperty(default=False)
	rigid_body_type_edit: bpy.props.BoolProperty(default=False)
	rigid_body_shape_edit: bpy.props.BoolProperty(default=False)
	mass_edit: bpy.props.BoolProperty(default=False)
	restitution_edit: bpy.props.BoolProperty(default=False)
	collision_group_number_edit: bpy.props.BoolProperty(default=False)
	collision_group_mask_edit: bpy.props.BoolProperty(default=False)
	friction_edit: bpy.props.BoolProperty(default=False)
	linear_damping_edit: bpy.props.BoolProperty(default=False)
	angular_damping_edit: bpy.props.BoolProperty(default=False)


	#obj = bpy.context.active_object
	#original values
	location_x: bpy.props.FloatProperty(name='location_x',default=0,unit='LENGTH',update=_transform_selected_rigid_bodies)
	location_y: bpy.props.FloatProperty(name='location_y',default=0,unit='LENGTH',update=_transform_selected_rigid_bodies)
	location_z:  bpy.props.FloatProperty(name='location_z',default=0,unit='LENGTH',update=_transform_selected_rigid_bodies)
	rotation_mode: bpy.props.EnumProperty(items = [\
			('QUATERNION', 'Quaternion(WXYZ)', 'Quaternion(WXYZ)')\
			,('XYZ', 'XYZ Euler', 'XYZ Euler')\
			,('XZY', 'XZY Euler', 'XZY Euler')\
			,('YXZ', 'YXZ Euler', 'YXZ Euler')\
			,('YZX', 'YZX Euler', 'YZX Euler')\
			,('ZXY', 'ZXY Euler', 'ZXY Euler')\
			,('ZYX', 'ZYX Euler', 'ZYX Euler')\
			,('AXIS_ANGLE', 'Axis Angle', 'Axis Angle')\
			],update=_transform_selected_rigid_bodies)

	rotation_w: bpy.props.FloatProperty(name='rotation_w',default=0,unit='ROTATION',update=_transform_selected_rigid_bodies)
	rotation_x: bpy.props.FloatProperty(name='rotation_x',default=0,unit='ROTATION',update=_transform_selected_rigid_bodies)
	rotation_y: bpy.props.FloatProperty(name='rotation_y',default=0,unit='ROTATION',update=_transform_selected_rigid_bodies)
	rotation_z: bpy.props.FloatProperty(name='rotation_z',default=0,unit='ROTATION',update=_transform_selected_rigid_bodies)
	size_x: bpy.props.FloatProperty(name='size_x',default=0,min=0,precision=6,update=_transform_selected_rigid_bodies)
	size_y: bpy.props.FloatProperty(name='size_y',default=0,min=0,precision=6,update=_transform_selected_rigid_bodies)
	size_z: bpy.props.FloatProperty(name='size_z',default=0,min=0,precision=6,update=_transform_selected_rigid_bodies)
	rigid_body_type: None
	rigid_body_shape: None
	mass: None
	restitution: None
	collision_group_number: None
	collision_group_mask: None
	friction: None
	linear_damping: None
	angular_damping: None




	def invoke(self, context, event):
		BatchUpdateRigidBodies.initialization = False

		self.location_x_edit = False
		self.location_y_edit = False
		self.location_z_edit = False
		self.rotation_mode_edit = False
		self.rotation_w_edit = False
		self.rotation_x_edit = False
		self.rotation_y_edit = False
		self.rotation_z_edit = False
		self.size_x_edit = False
		self.size_y_edit = False
		self.size_z_edit = False
		self.rigid_body_type_edit = False
		self.rigid_body_shape_edit = False
		self.mass_edit = False
		self.restitution_edit = False
		self.collision_group_number_edit = False
		self.collision_group_mask_edit = False
		self.friction_edit = False
		self.linear_damping_edit = False
		self.angular_damping_edit = False

		obj = context.active_object 

		#BUGFIX: snapshot all the values before changing them
		self.obj_location = obj.location.copy()
		self.obj_rigid_body_shape = obj.mmd_rigid.shape
		self.obj_size_x = obj.mmd_rigid.size[0]
		self.obj_size_y = obj.mmd_rigid.size[1]
		self.obj_size_z = obj.mmd_rigid.size[2]
		self.obj_rotation_mode = obj.rotation_mode
		self.obj_rotation_quaternion = obj.rotation_quaternion.copy()
		self.obj_rotation_axis_angle = obj.rotation_axis_angle
		self.obj_rotation_euler = obj.rotation_euler.copy()
		self.obj_rigid_body_type = obj.mmd_rigid.type

		self.obj_mass = obj.rigid_body.mass
		self.obj_restitution = obj.rigid_body.restitution
		self.obj_collision_group_number = obj.mmd_rigid.collision_group_number
		self.obj_collision_group_mask = obj.mmd_rigid.collision_group_mask
		self.obj_friction = obj.rigid_body.friction
		self.obj_linear_damping = obj.rigid_body.linear_damping
		self.obj_angular_damping = obj.rigid_body.angular_damping
		

		self.location_x = self.obj_location[0]
		self.location_y = self.obj_location[1]
		self.location_z = self.obj_location[2]
		self.rotation_mode = self.obj_rotation_mode
		if obj.rotation_mode == 'QUATERNION':
			self.rotation_w = self.obj_rotation_quaternion.w #obj.rotation_quaternion.w
			self.rotation_x = self.obj_rotation_quaternion.x
			self.rotation_y = self.obj_rotation_quaternion.y
			self.rotation_z = self.obj_rotation_quaternion.z
		
		elif obj.rotation_mode == 'AXIS_ANGLE':
			self.rotation_w = self.obj_rotation_axis_angle.w
			self.rotation_x = self.obj_rotation_axis_angle.x
			self.rotation_y = self.obj_rotation_axis_angle.y
			self.rotation_z = self.obj_rotation_axis_angle.z
		
		else:
			self.rotation_w = 0
			self.rotation_x = self.obj_rotation_euler.x
			self.rotation_y = self.obj_rotation_euler.y
			self.rotation_z = self.obj_rotation_euler.z
		self.rigid_body_shape = self.obj_rigid_body_shape #obj.mmd_rigid.shape
		self.size_x = self.obj_size_x #obj.mmd_rigid.size[0]
		self.size_y = self.obj_size_y #obj.mmd_rigid.size[1]
		self.size_z = self.obj_size_z #obj.mmd_rigid.size[2]
		self.rigid_body_type = self.obj_rigid_body_type #obj.mmd_rigid.type

		self.mass = self.obj_mass #obj.rigid_body.mass
		self.restitution = self.obj_restitution #obj.rigid_body.restitution
		self.collision_group_number = self.obj_collision_group_number #obj.mmd_rigid.collision_group_number
		self.collision_group_mask = self.obj_collision_group_mask #obj.mmd_rigid.collision_group_mask
		self.friction = self.obj_friction #obj.rigid_body.friction
		self.linear_damping = self.obj_linear_damping #obj.rigid_body.linear_damping
		self.angular_damping = self.obj_angular_damping#obj.rigid_body.angular_damping

		wm = context.window_manager		
		return wm.invoke_props_dialog(self, width=400)


	def draw(self, context):
		BatchUpdateRigidBodies.initialization = True

		obj = context.active_object 		
		root = model.findRoot(obj)
		bone_name = context.active_object.mmd_rigid.bone
		
		layout = self.layout
		row = layout.row()
		row.label(text='Active Object: '+ context.active_object.name)
		row.label(text='Active Object Bone: '+ bone_name)
		#c.prop(obj.mmd_rigid, 'name_j')
		#c.prop(obj.mmd_rigid, 'name_e')
		row = layout.row()
		row.label(text='Number of selected rigid bodies: '+ str(len(bpy.context.selected_objects)))
		row = layout.row()
		row.label(text='Unchecked: Active only. Checked: All selected')
		row = layout.row()
		c = layout.column()
		c = row.column(align=True)
		c = row.column(align=True)
		c.alignment = 'RIGHT'
		if root.mmd_root.is_built == True:
			c.label(text="Turn off Physics to change location")	
		else:
			c.label(text='Location: X')
			c.label(text="Y")
			c.label(text="Z")
			c.label(text="")
			c = row.column(align=True)
			c.alignment = 'LEFT'
			c.prop(self,"location_x",toggle=False, text="")
			c.prop(self,"location_y",toggle=False, text="")
			c.prop(self,"location_z",toggle=False, text="")
			c.operator("ffxiv_mmd_tools_helper.reset_location_rigid_bodies",text="Reset to bone")
			c = row.column(align=True)
			c.prop(self, "location_x_edit", text="")
			c.prop(self, "location_y_edit", text="")
			c.prop(self, "location_z_edit", text="")	

		#checkbox logic for rotation_mode
		if (self.rotation_w_edit or self.rotation_x_edit or self.rotation_y_edit or self.rotation_z_edit):
			self.rotation_mode_edit = True
		elif (self.rotation_w_edit==False and self.rotation_x_edit==False and self.rotation_y_edit==False and self.rotation_z_edit==False):
			self.rotation_mode_edit = False

		#row = layout.row()
		#row = layout.row()
		c = layout.column()
		c = row.column(align=True)
		c = row.column(align=True)
		if root.mmd_root.is_built == True:
			c.label(text="Turn off Physics to change rotation")	
		else:
			if self.rotation_mode in('QUATERNION','AXIS_ANGLE'):
				c = row.column(align=True)
				c.alignment = 'RIGHT'
				c.label(text='Rotation: W')
				c.label(text='X')
				c.label(text='Y')
				c.label(text='Z')
				c = row.column(align=True)
				c.alignment = 'LEFT'
				c.prop(self,"rotation_w",index=0, text="")
				c.prop(self,"rotation_x",index=1, text="")
				c.prop(self,"rotation_y",index=2, text="")
				c.prop(self,"rotation_z",index=3, text="")
				c.operator("ffxiv_mmd_tools_helper.reset_rotation_rigid_bodies",text="Reset to bone")
				c = row.column(align=True)
				c.prop(self, "rotation_w_edit", text="")
				c.prop(self, "rotation_x_edit", text="")
				c.prop(self, "rotation_y_edit", text="")
				c.prop(self, "rotation_z_edit", text="")
			else:
				c = row.column(align=True)
				c.alignment = 'RIGHT'
				c.label(text='Rotation: X')
				c.label(text='Y')
				c.label(text='Z')
				c = row.column(align=True)
				c.alignment = 'LEFT'
				c.prop(self,"rotation_x",index=1, text="")
				c.prop(self,"rotation_y",index=2, text="")
				c.prop(self,"rotation_z",index=3, text="")
				c.operator("ffxiv_mmd_tools_helper.reset_rotation_rigid_bodies",text="Reset to bone")
				c = row.column(align=True)
				c.prop(self, "rotation_x_edit", text="")
				c.prop(self, "rotation_y_edit", text="")
				c.prop(self, "rotation_z_edit", text="")
		row = layout.row()
		c = row.column(align=True)
		c.label(text='Rotation Mode')
		c = row.column(align=True)
		c.prop(self,"rotation_mode",text="")
		c = row.column(align=True)
		c.prop(self, "rotation_mode_edit", text="")
		row = layout.row()
		c = row.column(align=True)
		row.prop(obj.mmd_rigid, 'type', expand=True)
		c = row.column(align=True)
		row.prop(self, "rigid_body_type_edit", text="")

		c = layout.column(align=True)
		c.enabled = obj.mode == 'OBJECT'
		g = c.grid_flow(row_major=True, align=True)
		#if (self.size_x_edit or self.size_y_edit or self.size_z_edit):
			#self.rigid_body_shape_edit = True
		row = g.row(align=True)
		row.prop(obj.mmd_rigid, 'shape', expand=True)
		row.prop(self, "rigid_body_shape_edit", text="")
		g = c.grid_flow(row_major=True, align=True,columns=1)
		if obj.mmd_rigid.shape == 'SPHERE':	
			row = g.row(align=True)
			row.prop(self, 'size_x',text='Radius', expand=True)
			row.prop(self, "size_x_edit", text="")
		elif obj.mmd_rigid.shape == 'BOX':	
			row = g.row(align=True)
			row.prop(self, 'size_x',text='Size X', expand=True)
			row.prop(self, "size_x_edit", text="")
			row = g.row(align=True)
			row.prop(self, 'size_y',text='Size Y', expand=True)
			row.prop(self, "size_y_edit", text="")
			row = g.row(align=True)
			row.prop(self, 'size_z',text='Size Z', expand=True)
			row.prop(self, "size_z_edit", text="")
		elif obj.mmd_rigid.shape == 'CAPSULE':	
			row = g.row(align=True)
			row.prop(self, 'size_x',text='Radius', expand=True)
			row.prop(self, "size_x_edit", text="")
			row = g.row(align=True)
			row.prop(self, 'size_y',text='Height', expand=True)
			row.prop(self, "size_y_edit", text="")
		row = layout.row() 
		c = layout.column()
		g = c.grid_flow(row_major=True)
		row = g.row(align=True)
		row.prop(obj.rigid_body, 'mass')
		row.prop(self, "mass_edit", text="")
		row = g.row(align=True)		
		row.prop(obj.rigid_body, 'restitution')
		row.prop(self, "restitution_edit", text="")
		row = g.row(align=True)
		row.prop(obj.mmd_rigid, 'collision_group_number')
		row.prop(self, "collision_group_number_edit", text="")
		row = g.row(align=True)
		row.prop(obj.rigid_body, 'friction')
		row.prop(self, "friction_edit", text="")
		c = layout.column()
		g = c.grid_flow(row_major=True, align=True)
		row = g.row(align=True)
		row.label(text='Collision Group Mask:')
		row.prop(self, "collision_group_mask_edit", text="")
		c = layout.column()
		col = c.column(align=True)
		row = col.row(align=True)
		for i in range(0, 8):
			row.prop(obj.mmd_rigid, 'collision_group_mask', index=i, text=str(i), toggle=True)
		row = col.row(align=True)
		for i in range(8, 16):
			row.prop(obj.mmd_rigid, 'collision_group_mask', index=i, text=str(i), toggle=True)
		c = layout.column()
		c.label(text='Damping')
		g = c.grid_flow(row_major=True, align=True)
		row = g.row(align=True)
		row.prop(obj.rigid_body, 'linear_damping')
		row.prop(self, "linear_damping_edit", text="")
		row = g.row(align=True)
		row.prop(obj.rigid_body, 'angular_damping')
		row.prop(self, "angular_damping_edit", text="")
		row = layout.row()

	@classmethod
	def poll(cls, context):
		obj = context.active_object 
		return obj is not None and obj.mmd_type == 'RIGID_BODY'


	def execute(self, context):

		bpy.ops.object.mode_set(mode='OBJECT')
		
		obj = context.active_object 

		w=None
		x=None
		y=None
		z=None

		if obj.rotation_mode == ('QUATERNION'):
			w=obj.rotation_quaternion.w
			x=obj.rotation_quaternion.x
			y=obj.rotation_quaternion.y
			z=obj.rotation_quaternion.z
		elif obj.rotation_mode == ('AXIS_ANGLE'):
			w=obj.rotation_axis_angle.w
			x=obj.rotation_axis_angle.x
			y=obj.rotation_axis_angle.y
			z=obj.rotation_axis_angle.z
		else:
			x=obj.rotation_euler.x
			y=obj.rotation_euler.y
			z=obj.rotation_euler.z

		# Call the function and only pass the non-None parameters
		transform_selected_rigid_bodies(
					location_x=self.location_x if self.location_x_edit else None,
					location_y=self.location_y if self.location_y_edit else None,
					location_z=self.location_z if self.location_z_edit else None,
					rotation_mode=obj.rotation_mode if self.rotation_mode_edit else None,
					rotation_w=self.rotation_w if self.rotation_w_edit else None,
					rotation_x=self.rotation_x if self.rotation_x_edit else None,
					rotation_y=self.rotation_y if self.rotation_y_edit else None,
					rotation_z=self.rotation_z if self.rotation_z_edit else None,
					size_x=self.size_x if self.size_x_edit else None,
					size_y=self.size_y if self.size_y_edit else None,
					size_z=self.size_z if self.size_z_edit else None,
					rigid_body_type=obj.mmd_rigid.type if self.rigid_body_type_edit else None,
					rigid_body_shape=obj.mmd_rigid.shape if self.rigid_body_shape_edit else None,
					mass=obj.rigid_body.mass if self.mass_edit else None,
					restitution=obj.rigid_body.restitution if self.restitution_edit else None,
					collision_group_number=obj.mmd_rigid.collision_group_number if self.collision_group_number_edit else None,
					collision_group_mask=obj.mmd_rigid.collision_group_mask if self.collision_group_mask_edit else None,
					friction=obj.rigid_body.friction if self.friction_edit else None,
					linear_damping=obj.rigid_body.linear_damping if self.linear_damping_edit else None,
					angular_damping=obj.rigid_body.angular_damping if self.angular_damping_edit else None,
				)

		return {'FINISHED'}



@register_wrap
class BatchUpdateRigidBodyBoneChain(bpy.types.Operator):
	""" Update Rigid Bodies in a Bone Chain with Start and End values """
	bl_idname = "ffxiv_mmd_tools_helper.batch_update_rigid_body_bone_chain"
	bl_label = "Update Rigid Bodies by Bone Chain"
	bl_options = {'REGISTER','UNDO','PRESET','BLOCKING'} 

	#original values
	rigid_body_bone_chain = None
	bone_head = None
	bone_tail = None
	rigid_body_length = None
	
	#create property_start, property_end, and property_edit values
	prop_create = [
			('location_x','bpy.props.FloatProperty(default=0,unit=\'LENGTH\',update=_transform_rigid_body_bone_chain)'),
			('location_y', 'bpy.props.FloatProperty(default=0,unit=\'LENGTH\',update=_transform_rigid_body_bone_chain)'),
			('location_z', 'bpy.props.FloatProperty(default=0,unit=\'LENGTH\',update=_transform_rigid_body_bone_chain)'),
			('rotation_w', 'bpy.props.FloatProperty(default=0,unit=\'ROTATION\',update=_transform_rigid_body_bone_chain)'),
			('rotation_x', 'bpy.props.FloatProperty(default=0,unit=\'ROTATION\',update=_transform_rigid_body_bone_chain)'),
			('rotation_y', 'bpy.props.FloatProperty(default=0,unit=\'ROTATION\',update=_transform_rigid_body_bone_chain)'),
			('rotation_z', 'bpy.props.FloatProperty(default=0,unit=\'ROTATION\',update=_transform_rigid_body_bone_chain)'),
			('size_x', 'bpy.props.FloatProperty(default=0,min=0,precision=6,update=_transform_rigid_body_bone_chain)'),
			('size_y', 'bpy.props.FloatProperty(default=0,min=0,precision=6,update=_transform_rigid_body_bone_chain)'),
			('size_z', 'bpy.props.FloatProperty(default=0,min=0,precision=6,update=_transform_rigid_body_bone_chain)'),
			('mass', 'bpy.props.FloatProperty(default=0,min=0,precision=6,unit=\'MASS\')'),
			('restitution', 'bpy.props.FloatProperty(default=0,min=0,max=1,precision=6)'),
			('friction', 'bpy.props.FloatProperty(default=0,min=0,max=1,precision=6)'),
			('linear_damping', 'bpy.props.FloatProperty(default=0,min=0,max=1,precision=6)'),
			('angular_damping', 'bpy.props.FloatProperty(default=0,min=0,max=1,precision=6)'),
		]

	for property,prop_type in prop_create:
		exec(f'{property}_start = {prop_type}')
		exec(f'{property}_end = {prop_type}')
		exec(f'{property}_edit = bpy.props.BoolProperty(default=False)')



	def invoke(self, context, event):

		#selected_objs = context.selected_objects
		
		self.rigid_body_bone_chain = get_selected_rigid_bodies_in_bone_chain()

		self.bone_head = self.rigid_body_bone_chain[0][1]
		self.bone_tail = self.rigid_body_bone_chain[-1][1]
		self.rigid_body_length = str(len(self.rigid_body_bone_chain))
		

		starting_rigid_body = self.rigid_body_bone_chain[0][2]
		ending_rigid_body = self.rigid_body_bone_chain[-1][2]

		
		properties = [
					('location_x','location','.x', starting_rigid_body, ending_rigid_body),
					('location_y','location','.y', starting_rigid_body, ending_rigid_body),
					('location_z', 'location','.z',starting_rigid_body, ending_rigid_body),
					#('rotation_mode','rotation_mode','', starting_rigid_body, ending_rigid_body),
					('rotation_w','rotation_quaternion','.w', starting_rigid_body, ending_rigid_body),
					('rotation_x','rotation_quaternion','.x', starting_rigid_body, ending_rigid_body),
					('rotation_y','rotation_quaternion','.y', starting_rigid_body, ending_rigid_body),
					('rotation_z','rotation_quaternion','.z', starting_rigid_body, ending_rigid_body),
					('rotation_w','rotation_axis_angle','[0]', starting_rigid_body, ending_rigid_body),
					('rotation_x','rotation_axis_angle','[1]', starting_rigid_body, ending_rigid_body),
					('rotation_y','rotation_axis_angle','[2]', starting_rigid_body, ending_rigid_body),
					('rotation_z','rotation_axis_angle','[3]', starting_rigid_body, ending_rigid_body),
					('rotation_w','rotation_euler','.w', starting_rigid_body, ending_rigid_body),
					('rotation_x','rotation_euler','.x', starting_rigid_body, ending_rigid_body),
					('rotation_y','rotation_euler','.y', starting_rigid_body, ending_rigid_body),
					('rotation_z','rotation_euler','.z', starting_rigid_body, ending_rigid_body),
					('size_x','mmd_rigid.size','[0]', starting_rigid_body, ending_rigid_body),
					('size_y','mmd_rigid.size','[1]', starting_rigid_body, ending_rigid_body),
					('size_z','mmd_rigid.size','[2]', starting_rigid_body, ending_rigid_body),
					('mass','rigid_body.mass','', starting_rigid_body, ending_rigid_body),
					('restitution','rigid_body.restitution','', starting_rigid_body, ending_rigid_body),
					('friction','rigid_body.friction','', starting_rigid_body, ending_rigid_body),
					('linear_damping','rigid_body.linear_damping','', starting_rigid_body, ending_rigid_body),
					('angular_damping','rigid_body.angular_damping','', starting_rigid_body, ending_rigid_body)]

		# loop through properties and initialize the variables

		#equivalent to writing
		#self.[internal property name]_start = [starting rigid body variable name].([external property name]+[external property suffix]
		#self.[internal property name]_end = [ending rigid body variable name].([external property name]+[external property suffix]

		for int_prop,ext_prop,ext_prop_suffix,starting_rigid,ending_rigid in properties:
			
			if int_prop in ['rotation_w','rotation_x','rotation_y','rotation_z']:
				if get_attribute(starting_rigid,'rotation_mode') == 'QUATERNION' and get_attribute(ending_rigid,'rotation_mode') == 'QUATERNION':
					setattr(self,int_prop + '_start', get_attribute(starting_rigid,ext_prop+ext_prop_suffix))
					setattr(self,int_prop + '_end', get_attribute(ending_rigid,ext_prop+ext_prop_suffix))
				elif get_attribute(starting_rigid,'rotation_mode') == 'AXIS_ANGLE' and get_attribute(ending_rigid,'rotation_mode') == 'AXIS_ANGLE':
					setattr(self,int_prop + '_start', get_attribute(starting_rigid,ext_prop+ext_prop_suffix))
					setattr(self,int_prop + '_end', get_attribute(ending_rigid,ext_prop+ext_prop_suffix))
				else: 
					if int_prop == 'rotation_w' and ext_prop=='rotation_euler':
						self.rotation_w_start = 0
						self.rotation_w_end = 0
					else:
						setattr(self,int_prop + '_start', get_attribute(starting_rigid,ext_prop+ext_prop_suffix))
						setattr(self,int_prop + '_end', get_attribute(ending_rigid,ext_prop+ext_prop_suffix))
			else:
				setattr(self,int_prop + '_start', get_attribute(starting_rigid,ext_prop+ext_prop_suffix))
				setattr(self,int_prop + '_end', get_attribute(ending_rigid,ext_prop+ext_prop_suffix))
			
			#set all the edit flags to false
			setattr(self,int_prop+'_edit',False)

		#if rotation mode is euler, set it to 0
		if get_attribute(starting_rigid_body,'rotation_mode') not in ('QUATERNION','AXIS_ANGLE') and get_attribute(starting_rigid_body,'rotation_mode') not in ('QUATERNION','AXIS_ANGLE'):
			self.rotation_w_start = 0
			self.rotation_w_end = 0
		

		wm = context.window_manager		
		return wm.invoke_props_dialog(self, width=400)


	def draw(self, context):
		layout = self.layout
		
		starting_rigid_body = self.rigid_body_bone_chain[0][2]
		ending_rigid_body = self.rigid_body_bone_chain[-1][2]

		obj = context.active_object
		root = model.findRoot(obj)

		row = layout.row()
		row.label(text='# Rigid Bodies in Bone Chain: '+ self.rigid_body_length)

		row = layout.row()
		row.label(text='Checkmark to apply to all rigid bodies in bone chain')

		row = layout.row() 
		c = layout.column(align=True)
		row = c.row()
		row.label(text="Property")
		row.label(text="Start Value")
		row.label(text="End Value")
		row = c.row()
		row.label(text="Bone Chain")
		row.label(text=self.bone_head)
		row.label(text=self.bone_tail)
		row = c.row()
		if root.mmd_root.is_built == True:
			row = c.row()
			row.alignment = 'CENTER'
			row.label(text="Turn off Physics in MMD Tools to change location / rotation")	
		else:
			#g = c.grid_flow(row_major=True, align=True,columns=1)
			row.label(text='Location X')
			row.prop(self, 'location_x_start',expand=True, text="")
			row.prop(self, 'location_x_end',expand=True, text="")
			row.prop(self, "location_x_edit", text="")
			row = c.row()
			row.label(text='Location Y')
			row.prop(self, 'location_y_start',expand=True, text="")
			row.prop(self, 'location_y_end',expand=True, text="")
			row.prop(self, "location_y_edit", text="")
			row = c.row()
			row.label(text='Location Z')
			row.prop(self, 'location_z_start',expand=True, text="")
			row.prop(self, 'location_z_end',expand=True, text="")
			row.prop(self, "location_z_edit", text="")
			row = c.row()
			if starting_rigid_body.rotation_mode == 'QUATERNION' and ending_rigid_body.rotation_mode == 'QUATERNION':	
				row = c.row()
				row.label(text='Rotation W')
				row.prop(self, 'rotation_w_start',expand=True, text="")
				row.prop(self, 'rotation_w_end',expand=True, text="")
				row.prop(self, "rotation_w_edit", text="")
				row = c.row()
				row.label(text='Rotation X')
				row.prop(self, 'rotation_x_start',expand=True, text="")
				row.prop(self, 'rotation_x_end',expand=True, text="")
				row.prop(self, "rotation_x_edit", text="")
				row = c.row()
				row.label(text='Rotation Y')
				row.prop(self, 'rotation_y_start',expand=True, text="")
				row.prop(self, 'rotation_y_end',expand=True, text="")
				row.prop(self, "rotation_y_edit", text="")
				row = c.row()
				row.label(text='Rotation Z')
				row.prop(self, 'rotation_z_start',expand=True, text="")
				row.prop(self, 'rotation_z_end',expand=True, text="")
				row.prop(self, "rotation_z_edit", text="")
			elif starting_rigid_body.rotation_mode == 'AXIS_ANGLE' and ending_rigid_body.rotation_mode == 'AXIS_ANGLE':	
				row = c.row()
				row.label(text='Rotation W')
				row.prop(self, 'rotation_w_start',expand=True, text="")
				row.prop(self, 'rotation_w_end',expand=True, text="")
				row.prop(self, "rotation_w_edit", text="")
				row = c.row()
				row.label(text='Rotation X')
				row.prop(self, 'rotation_x_start',expand=True, text="")
				row.prop(self, 'rotation_x_end',expand=True, text="")
				row.prop(self, "rotation_x_edit", text="")
				row = c.row()
				row.label(text='Rotation Y')
				row.prop(self, 'rotation_y_start',expand=True, text="")
				row.prop(self, 'rotation_y_end',expand=True, text="")
				row.prop(self, "rotation_y_edit", text="")
				row = c.row()
				row.label(text='Rotation Z')
				row.prop(self, 'rotation_z_start',expand=True, text="")
				row.prop(self, 'rotation_z_end',expand=True, text="")
				row.prop(self, "rotation_z_edit", text="")
			else:	
				row = c.row()
				row.label(text='Rotation X')
				row.prop(self, 'rotation_x_start',expand=True, text="")
				row.prop(self, 'rotation_x_end',expand=True, text="")
				row.prop(self, "rotation_x_edit", text="")
				row = c.row()
				row.label(text='Rotation Y')
				row.prop(self, 'rotation_y_start',expand=True, text="")
				row.prop(self, 'rotation_y_end',expand=True, text="")
				row.prop(self, "rotation_y_edit", text="")
				row = c.row()
				row.label(text='Rotation Z')
				row.prop(self, 'rotation_z_start',expand=True, text="")
				row.prop(self, 'rotation_z_end',expand=True, text="")
				row.prop(self, "rotation_z_edit", text="")
		row = c.row()
		if starting_rigid_body.mmd_rigid.shape == 'SPHERE' and ending_rigid_body.mmd_rigid.shape == 'SPHERE':	
			row = c.row()
			row.label(text='Radius')
			row.prop(self, 'size_x_start',expand=True, text="")
			row.prop(self, 'size_x_end',expand=True, text="")
			row.prop(self, "size_x_edit", text="")
		elif starting_rigid_body.mmd_rigid.shape == 'BOX' and ending_rigid_body.mmd_rigid.shape == 'BOX':	
			row = c.row()
			row.label(text='Size X')
			row.prop(self, 'size_x_start', expand=True, text="")
			row.prop(self, 'size_x_end', expand=True, text="")
			row.prop(self, "size_x_edit", text="")
			row = c.row()
			row.label(text='Size Y')
			row.prop(self, 'size_y_start', expand=True, text="")
			row.prop(self, 'size_y_end',expand=True, text="")
			row.prop(self, "size_y_edit", text="")
			row = c.row()
			row.label(text='Size Z')
			row.prop(self, 'size_z_start', expand=True, text="")
			row.prop(self, 'size_z_end', expand=True, text="")
			row.prop(self, "size_z_edit", text="")
		elif starting_rigid_body.mmd_rigid.shape == 'CAPSULE' and ending_rigid_body.mmd_rigid.shape == 'CAPSULE':	
			row = c.row()
			row.label(text='Radius')
			row.prop(self, 'size_x_start', expand=True, text="")
			row.prop(self, 'size_x_end', expand=True, text="")
			row.prop(self, "size_x_edit", text="")
			row = c.row()
			row.label(text='Height')
			row.prop(self, 'size_y_start', expand=True, text="")
			row.prop(self, 'size_y_end', expand=True, text="")
			row.prop(self, "size_y_edit", text="")
		row = c.row()
		row.label(text="Mass")
		row.prop(self, 'mass_start',text="")
		row.prop(self, 'mass_end',text="")
		row.prop(self, "mass_edit", text="")
		row = c.row()		
		row.label(text="Restitution")
		row.prop(self, 'restitution_start',text="",slider=True)
		row.prop(self, 'restitution_end',text="",slider=True)
		row.prop(self, "restitution_edit", text="")
		row = c.row()
		row.label(text="Friction")
		row.prop(self, 'friction_start',text="",slider=True)
		row.prop(self, 'friction_end',text="",slider=True)
		row.prop(self, "friction_edit", text="")
		row = c.row()
		row.label(text="Linear Damping")
		row.prop(self, 'linear_damping_start',text="",slider=True)
		row.prop(self, 'linear_damping_end',text="",slider=True)
		row.prop(self, "linear_damping_edit", text="")
		row = c.row()
		row.label(text="Angular Damping")
		row.prop(self, 'angular_damping_start',text="",slider=True)
		row.prop(self, 'angular_damping_end',text="",slider=True)
		row.prop(self, "angular_damping_edit", text="")
		row = c.row()


	@classmethod
	def poll(cls, context):
		is_in_bone_chain = is_selected_rigid_bodies_in_a_bone_chain()
		obj = context.active_object 
		return obj is not None and is_in_bone_chain == True


	def execute(self, context):

		bpy.ops.object.mode_set(mode='OBJECT')
		
		#for bone in self.rigid_body_bone_chain:
			#print (bone)
		
		
		# Call the function and only pass the non-None parameters
		transform_rigid_body_bone_chain(
					rigid_body_bone_chain=self.rigid_body_bone_chain,
					location_x_start=self.location_x_start if self.location_x_edit else None,
					location_x_end=self.location_x_end if self.location_x_edit else None,
					location_y_start=self.location_y_start if self.location_y_edit else None,
					location_y_end=self.location_y_end if self.location_y_edit else None,
					location_z_start=self.location_z_start if self.location_z_edit else None,
					location_z_end=self.location_z_end if self.location_z_edit else None,
					rotation_w_start=self.rotation_w_start if self.rotation_w_edit else None,
					rotation_w_end=self.rotation_w_end if self.rotation_w_edit else None,
					rotation_x_start=self.rotation_x_start if self.rotation_x_edit else None,
					rotation_x_end=self.rotation_x_end if self.rotation_x_edit else None,
					rotation_y_start=self.rotation_y_start if self.rotation_y_edit else None,
					rotation_y_end=self.rotation_y_end if self.rotation_y_edit else None,
					rotation_z_start=self.rotation_z_start if self.rotation_z_edit else None,
					rotation_z_end=self.rotation_z_end if self.rotation_z_edit else None,
					size_x_start=self.size_x_start if self.size_x_edit else None,
					size_x_end=self.size_x_end if self.size_x_edit else None,
					size_y_start=self.size_y_start if self.size_y_edit else None,
					size_y_end=self.size_y_end if self.size_y_edit else None,
					size_z_start=self.size_z_start if self.size_z_edit else None,
					size_z_end=self.size_z_end if self.size_z_edit else None,
					mass_start=self.mass_start if self.mass_edit else None,
					mass_end=self.mass_end if self.mass_edit else None,
					restitution_start=self.restitution_start if self.restitution_edit else None,
					restitution_end=self.restitution_end if self.restitution_edit else None,
					friction_start=self.friction_start if self.friction_edit else None,
					friction_end=self.friction_edit if self.friction_edit else None,
					linear_damping_start=self.linear_damping_start if self.linear_damping_edit else None,
					linear_damping_end=self.linear_damping_end if self.linear_damping_edit else None,
					angular_damping_start=self.angular_damping_start if self.angular_damping_edit else None,
					angular_damping_end=self.angular_damping_end if self.angular_damping_edit else None
				)
		
		return {'FINISHED'}

def _transform_rigid_body_bone_chains_by_delta(self,context):

	rigid_body_bone_chains_data = BatchUpdateMultipleRigidBodyBoneChain.rigid_body_bone_chains_data

	for i in rigid_body_bone_chains_data:
	
		# Call the function and only pass the non-None parameters
		transform_rigid_body_bone_chain(
					rigid_body_bone_chain= rigid_body_bone_chains_data[i]['chain_data'],
					location_x_start=self.location_x_start + rigid_body_bone_chains_data[i]['head']['location_x'] if self.location_x_edit else None,
					location_x_end=self.location_x_end + rigid_body_bone_chains_data[i]['tail']['location_x'] if self.location_x_edit else None,
					location_y_start=self.location_y_start + rigid_body_bone_chains_data[i]['head']['location_y'] if self.location_y_edit else None,
					location_y_end=self.location_y_end + rigid_body_bone_chains_data[i]['tail']['location_y'] if self.location_y_edit else None,
					location_z_start=self.location_z_start + rigid_body_bone_chains_data[i]['head']['location_z'] if self.location_z_edit else None,
					location_z_end=self.location_z_end + rigid_body_bone_chains_data[i]['tail']['location_z'] if self.location_z_edit else None,
					rotation_w_start=self.rotation_w_start + rigid_body_bone_chains_data[i]['head']['rotation_w'] if self.rotation_w_edit else None,
					rotation_w_end=self.rotation_w_end + rigid_body_bone_chains_data[i]['tail']['rotation_w'] if self.rotation_w_edit else None,
					rotation_x_start=self.rotation_x_start + rigid_body_bone_chains_data[i]['head']['rotation_x'] if self.rotation_x_edit else None,
					rotation_x_end=self.rotation_x_end + rigid_body_bone_chains_data[i]['tail']['rotation_x'] if self.rotation_x_edit else None,
					rotation_y_start=self.rotation_y_start + rigid_body_bone_chains_data[i]['head']['rotation_y'] if self.rotation_y_edit else None,
					rotation_y_end=self.rotation_y_end + rigid_body_bone_chains_data[i]['tail']['rotation_y'] if self.rotation_y_edit else None,
					rotation_z_start=self.rotation_z_start + rigid_body_bone_chains_data[i]['head']['rotation_z'] if self.rotation_z_edit else None,
					rotation_z_end=self.rotation_z_end + rigid_body_bone_chains_data[i]['tail']['rotation_z'] if self.rotation_z_edit else None,
					size_x_start=self.size_x_start + rigid_body_bone_chains_data[i]['head']['size_x'] if self.size_x_edit else None,
					size_x_end=self.size_x_end + rigid_body_bone_chains_data[i]['tail']['size_x'] if self.size_x_edit else None,
					size_y_start=self.size_y_start + rigid_body_bone_chains_data[i]['head']['size_y'] if self.size_y_edit else None,
					size_y_end=self.size_y_end + rigid_body_bone_chains_data[i]['tail']['size_y'] if self.size_y_edit else None,
					size_z_start=self.size_z_start + rigid_body_bone_chains_data[i]['head']['size_z'] if self.size_z_edit else None,
					size_z_end=self.size_z_end + rigid_body_bone_chains_data[i]['tail']['size_z'] if self.size_z_edit else None,
					#mass_start=self.mass_start + rigid_body_bone_chains_data[i]['head']['mass'] if self.mass_edit else None,
					#mass_end=self.mass_end + rigid_body_bone_chains_data[i]['tail']['mass'] if self.mass_edit else None,
					#restitution_start=self.restitution_start + rigid_body_bone_chains_data[i]['head']['restitution'] if self.restitution_edit else None,
					#restitution_end=self.restitution_end + rigid_body_bone_chains_data[i]['tail']['restitution'] if self.restitution_edit else None,
					#friction_start=self.friction_start + rigid_body_bone_chains_data[i]['head']['friction'] if self.friction_edit else None,
					#friction_end=self.friction_edit + rigid_body_bone_chains_data[i]['tail']['friction'] if self.friction_edit else None,
					#linear_damping_start=self.linear_damping_start + rigid_body_bone_chains_data[i]['head']['linear_damping']  if self.linear_damping_edit else None,
					#linear_damping_end=self.linear_damping_end + rigid_body_bone_chains_data[i]['tail']['linear_damping'] if self.linear_damping_edit else None,
					#angular_damping_start=self.angular_damping_start + rigid_body_bone_chains_data[i]['head']['angular_damping'] if self.angular_damping_edit else None,
					#angular_damping_end=self.angular_damping_end + rigid_body_bone_chains_data[i]['tail']['angular_damping'] if self.angular_damping_edit else None
				)
		
@register_wrap
class ResetValue_BatchUpdateMultipleRigidBodyBoneChain(bpy.types.Operator):
	""" Resets the value back to 0 """
	bl_idname = "ffxiv_mmd_tools_helper.reset_batch_update_property"
	bl_label = " Resets the value back to 0"
	
	"""
	property: bpy.props.EnumProperty(items = \
		[('ALL', 'ALL', 'ALL')\
			,('UP','UP','UP')
			,('DOWN', 'DOWN', 'DOWN')\
		], name = "", default = 'DOWN')
	"""
	prop_list_items = [
			('location_x_start','location_x_start','location_x_start'),
			('location_x_end','location_x_end','location_x_end'),
			('location_y_start', 'location_y_start', 'location_y_start'),
			('location_y_end', 'location_y_end', 'location_y_end'),
			('location_z_start', 'location_z_start', 'location_z_start'),
			('location_z_end', 'location_z_end', 'location_z_end'),
			('rotation_w_start', 'rotation_w_start', 'rotation_w_start'),
			('rotation_w_end', 'rotation_w_end', 'rotation_w_end'),
			('rotation_x_start', 'rotation_x_start', 'rotation_x_start'),
			('rotation_x_end', 'rotation_x_end', 'rotation_x_end'),
			('rotation_y_start', 'rotation_y_start', 'rotation_y_start'),
			('rotation_y_end', 'rotation_y_end', 'rotation_y_end'),
			('rotation_z_start', 'rotation_z_start', 'rotation_z_start'),
			('rotation_z_end', 'rotation_z_end', 'rotation_z_end'),
			('size_x_start', 'size_x_start', 'size_x_start'),
			('size_x_end', 'size_x_end', 'size_x_end'),
			('size_y_end', 'size_y_end', 'size_y_end'),
			('size_z_start', 'size_z_start', 'size_z_start'),
			('size_z_end', 'size_z_end', 'size_z_end'),
			('mass_start','mass_start','mass_start'),
			('mass_end', 'mass_end', 'mass_end'),
			('restitution_start','restitution_start','restitution_start'),
			('restitution_end', 'restitution_end', 'restitution_end'),
			('friction_start','friction_start','friction_start'),
			('friction_end', 'friction_end', 'friction_end'),
			('linear_damping_start','linear_damping_start','linear_damping_start'),
			('linear_damping_end', 'linear_damping_end', 'linear_damping_end'),
			('angular_damping_start', 'angular_damping_start', 'angular_damping_start'),
			('angular_damping_end','angular_damping_end','angular_damping_end'),
		]
	

	prop: bpy.props.EnumProperty(items = prop_list_items, name = "", default = 'location_x_start')

	def execute(self, context):
		cls = BatchUpdateMultipleRigidBodyBoneChain
		

		for prop_list_item in ResetValue_BatchUpdateMultipleRigidBodyBoneChain.prop_list_items:
			if prop_list_item[0] == self.prop:
				print ('at least we got here, location x start is:',cls.location_x_start)
				setattr(cls,self.prop,0)
				break
		
		return {'FINISHED'}




@register_wrap
class BatchUpdateMultipleRigidBodyBoneChain(bpy.types.Operator):
	""" Update Multiple Rigid Bodies in a Bone Chain by delta of start and end values """
	bl_idname = "ffxiv_mmd_tools_helper.batch_update_rigid_body_bone_chains"
	bl_label = "Update Multiple Rigid Bodies in Bone Chains by delta"
	bl_options = {'REGISTER','UNDO','PRESET','BLOCKING'} 
	
	rigid_body_bone_chains = []
	rigid_body_bone_chains_data = {}

	rigid_body_bone_chains = None #= get_all_rigid_body_chains_from_selected()
	rigid_body_bone_chains_data = None # = get_all_rigid_body_chains_dictionary(rigid_body_bone_chains)


	number_of_bone_chains = None
	number_of_rigid_bodies = None

	#create property_start, property_end, and property_edit values
	props_init = [
			('location_x','bpy.props.FloatProperty(default=0,unit=\'LENGTH\',update=_transform_rigid_body_bone_chains_by_delta)'),
			('location_y', 'bpy.props.FloatProperty(default=0,unit=\'LENGTH\',update=_transform_rigid_body_bone_chains_by_delta)'),
			('location_z', 'bpy.props.FloatProperty(default=0,unit=\'LENGTH\',update=_transform_rigid_body_bone_chains_by_delta)'),
			('rotation_w', 'bpy.props.FloatProperty(default=0,unit=\'ROTATION\',update=_transform_rigid_body_bone_chains_by_delta)'),
			('rotation_x', 'bpy.props.FloatProperty(default=0,unit=\'ROTATION\',update=_transform_rigid_body_bone_chains_by_delta)'),
			('rotation_y', 'bpy.props.FloatProperty(default=0,unit=\'ROTATION\',update=_transform_rigid_body_bone_chains_by_delta)'),
			('rotation_z', 'bpy.props.FloatProperty(default=0,unit=\'ROTATION\',update=_transform_rigid_body_bone_chains_by_delta)'),
			('size_x', 'bpy.props.FloatProperty(default=0,min=-1,precision=6,update=_transform_rigid_body_bone_chains_by_delta)'),
			('size_y', 'bpy.props.FloatProperty(default=0,min=-1,precision=6,update=_transform_rigid_body_bone_chains_by_delta)'),
			('size_z', 'bpy.props.FloatProperty(default=0,min=-1,precision=6,update=_transform_rigid_body_bone_chains_by_delta)'),
			('mass', 'bpy.props.FloatProperty(default=0,min=0.001,precision=6,unit=\'MASS\',update=_transform_rigid_body_bone_chains_by_delta)'),
			('restitution', 'bpy.props.FloatProperty(default=0,min=0,max=1,precision=6,update=_transform_rigid_body_bone_chains_by_delta)'),
			('friction', 'bpy.props.FloatProperty(default=0,min=0,max=1,precision=6,update=_transform_rigid_body_bone_chains_by_delta)'),
			('linear_damping', 'bpy.props.FloatProperty(default=0,min=0,max=1,precision=6,update=_transform_rigid_body_bone_chains_by_delta)'),
			('angular_damping', 'bpy.props.FloatProperty(default=0,min=0,max=1,precision=6,update=_transform_rigid_body_bone_chains_by_delta)'),
		]

	for property,prop_type in props_init:
		exec(f'{property}_start = {prop_type}')
		exec(f'{property}_end = {prop_type}')
		exec(f'{property}_edit = bpy.props.BoolProperty(default=False)')


	def invoke(self, context, event):

		rigid_body_bone_chains = get_all_rigid_body_chains_from_selected()
		BatchUpdateMultipleRigidBodyBoneChain.rigid_body_bone_chains_data = get_all_rigid_body_chains_dictionary(rigid_body_bone_chains)
		self.rigid_body_bone_chains_data = BatchUpdateMultipleRigidBodyBoneChain.rigid_body_bone_chains_data

		for property,prop_type in self.props_init:
			setattr(self,property+'_start',0)
			setattr(self,property+'_end',0)
			setattr(self,property+'_edit',False)

		#selected_objs = context.selected_objects
		
		
		#for i in self.rigid_body_bone_chains_data:
			#print('chain:', str(i),' head:',self.rigid_body_bone_chains_data[i]['head']['bone'], ' tail:',self.rigid_body_bone_chains_data[i]['tail']['bone'])

		self.number_of_bone_chains = len(self.rigid_body_bone_chains_data)
		self.number_of_rigid_bodies = 0
		for i in self.rigid_body_bone_chains_data:
			#print(self.rigid_body_bone_chains_data[i]['chain_length'])
			self.number_of_rigid_bodies = self.number_of_rigid_bodies + self.rigid_body_bone_chains_data[i]['chain_length']
			
		wm = context.window_manager		
		return wm.invoke_props_dialog(self, width=400)


	def draw(self, context):
		layout = self.layout

		obj=context.active_object
		root = model.findRoot(obj)
		
		starting_rigid_body = self.rigid_body_bone_chains_data[0]['head']
		ending_rigid_body = self.rigid_body_bone_chains_data[0]['tail']

		#self.number_of_bone_chains = len(self.rigid_body_bone_chains_data)
		#self.number_of_rigid_bodies = 0
		#for i in self.rigid_body_bone_chains_data:
			#self.number_of_rigid_bodies += self.rigid_body_bone_chains_data[i]['chain_length']

		row = layout.row()
		row.label(text='Rigid Body Bone Chains: ' + str(self.number_of_bone_chains))
		row = layout.row()
		row.label(text='Total Selected Rigid Bodies: '+ str(self.number_of_rigid_bodies))

		row = layout.row()
		row.label(text='Checkmark to apply to all rigid bodies in bone chain')

		row = layout.row() 
		c = layout.column(align=True)
		row = c.row()
		row.label(text="")
		row.label(text="Bone Head Delta")
		row.label(text="Bone Tail Delta")
		if root.mmd_root.is_built == True:
			row = c.row()
			row.alignment = 'CENTER'
			row.label(text="Turn off Physics in MMD Tools to change location / rotation")	
		else:
			row = c.row()
			row.label(text='Location X')
			row.prop(self, 'location_x_start',expand=True, text="")
			#row.operator("ffxiv_mmd_tools_helper.reset_batch_update_property", text='',icon='TRASH').prop ='location_x_start'
			row.prop(self, 'location_x_end',expand=True, text="")
			row.prop(self, "location_x_edit", text="")
			row = c.row()
			row.label(text='Location Y')
			row.prop(self, 'location_y_start',expand=True, text="")
			row.prop(self, 'location_y_end',expand=True, text="")
			row.prop(self, "location_y_edit", text="")
			row = c.row()
			row.label(text='Location Z')
			row.prop(self, 'location_z_start',expand=True, text="")
			row.prop(self, 'location_z_end',expand=True, text="")
			row.prop(self, "location_z_edit", text="")
			row = c.row()
			if (starting_rigid_body['rotation_mode'] == 'QUATERNION' and ending_rigid_body['rotation_mode'] == 'QUATERNION') \
				or (starting_rigid_body['rotation_mode'] == 'AXIS_ANGLE' and ending_rigid_body['rotation_mode'] == 'AXIS_ANGLE'):	
				row = c.row()
				row.label(text='Rotation W')
				row.prop(self, 'rotation_w_start',expand=True, text="")
				row.prop(self, 'rotation_w_end',expand=True, text="")
				row.prop(self, "rotation_w_edit", text="")
			row = c.row()
			row.label(text='Rotation X')
			row.prop(self, 'rotation_x_start',expand=True, text="")
			row.prop(self, 'rotation_x_end',expand=True, text="")
			row.prop(self, "rotation_x_edit", text="")
			row = c.row()
			row.label(text='Rotation Y')
			row.prop(self, 'rotation_y_start',expand=True, text="")
			row.prop(self, 'rotation_y_end',expand=True, text="")
			row.prop(self, "rotation_y_edit", text="")
			row = c.row()
			row.label(text='Rotation Z')
			row.prop(self, 'rotation_z_start',expand=True, text="")
			row.prop(self, 'rotation_z_end',expand=True, text="")
			row.prop(self, "rotation_z_edit", text="")
		row = c.row()
		if starting_rigid_body['rigid_body_shape'] == 'SPHERE' and ending_rigid_body['rigid_body_shape'] == 'SPHERE':		
			row = c.row()
			row.label(text='Radius')
			row.prop(self, 'size_x_start',expand=True, text="")
			row.prop(self, 'size_x_end',expand=True, text="")
			row.prop(self, "size_x_edit", text="")
		elif starting_rigid_body['rigid_body_shape'] == 'BOX' and ending_rigid_body['rigid_body_shape'] == 'BOX':		
			row = c.row()
			row.label(text='Size X')
			row.prop(self, 'size_x_start', expand=True, text="")
			row.prop(self, 'size_x_end', expand=True, text="")
			row.prop(self, "size_x_edit", text="")
			row = c.row()
			row.label(text='Size Y')
			row.prop(self, 'size_y_start', expand=True, text="")
			row.prop(self, 'size_y_end',expand=True, text="")
			row.prop(self, "size_y_edit", text="")
			row = c.row()
			row.label(text='Size Z')
			row.prop(self, 'size_z_start', expand=True, text="")
			row.prop(self, 'size_z_end', expand=True, text="")
			row.prop(self, "size_z_edit", text="")
		elif starting_rigid_body['rigid_body_shape'] == 'CAPSULE' and ending_rigid_body['rigid_body_shape'] == 'CAPSULE':		
			row = c.row()
			row.label(text='Radius')
			row.prop(self, 'size_x_start', expand=True, text="")
			row.prop(self, 'size_x_end', expand=True, text="")
			row.prop(self, "size_x_edit", text="")
			row = c.row()
			row.label(text='Height')
			row.prop(self, 'size_y_start', expand=True, text="")
			row.prop(self, 'size_y_end', expand=True, text="")
			row.prop(self, "size_y_edit", text="")
		row = c.row()
		row.label(text="")
		row.label(text="Bone Head Absolute")
		row.label(text="Bone Tail Absolute")
		row = c.row()
		row.label(text="Mass")
		row.prop(self, 'mass_start',text="")
		row.prop(self, 'mass_end',text="")
		row.prop(self, "mass_edit", text="")
		row = c.row()		
		row.label(text="Restitution")
		row.prop(self, 'restitution_start',text="",slider=True)
		row.prop(self, 'restitution_end',text="",slider=True)
		row.prop(self, "restitution_edit", text="")
		row = c.row()
		row.label(text="Friction")
		row.prop(self, 'friction_start',text="",slider=True)
		row.prop(self, 'friction_end',text="",slider=True)
		row.prop(self, "friction_edit", text="")
		row = c.row()
		row.label(text="Linear Damping")
		row.prop(self, 'linear_damping_start',text="",slider=True)
		row.prop(self, 'linear_damping_end',text="",slider=True)
		row.prop(self, "linear_damping_edit", text="")
		row = c.row()
		row.label(text="Angular Damping")
		row.prop(self, 'angular_damping_start',text="",slider=True)
		row.prop(self, 'angular_damping_end',text="",slider=True)
		row.prop(self, "angular_damping_edit", text="")
		row = c.row()


	@classmethod
	def poll(cls, context):
		obj = context.active_object 
		
		selected_objs = None

		is_all_selected_rigid_bodies = True
		
		if context.selected_objects:
			selected_objs = context.selected_objects
		else:
			is_all_selected_rigid_bodies = False
		
		if selected_objs is None:
			is_all_selected_rigid_bodies = False
		else:
			if len(selected_objs) < 2:
				is_all_selected_rigid_bodies = False
			else:
				for i in selected_objs:
					if i.mmd_type != 'RIGID_BODY':
						is_all_selected_rigid_bodies = False

		return obj is not None and obj.mmd_type == 'RIGID_BODY' and is_all_selected_rigid_bodies == True


	def execute(self, context):

		bpy.ops.object.mode_set(mode='OBJECT')
			
		
		for i in self.rigid_body_bone_chains_data:
		
			# Call the function and only pass the non-None parameters
			transform_rigid_body_bone_chain(
						rigid_body_bone_chain=self.rigid_body_bone_chains_data[i]['chain_data'],
						location_x_start=self.location_x_start + self.rigid_body_bone_chains_data[i]['head']['location_x'] if self.location_x_edit else None,
						location_x_end=self.location_x_end + self.rigid_body_bone_chains_data[i]['tail']['location_x'] if self.location_x_edit else None,
						location_y_start=self.location_y_start + self.rigid_body_bone_chains_data[i]['head']['location_y'] if self.location_y_edit else None,
						location_y_end=self.location_y_end + self.rigid_body_bone_chains_data[i]['tail']['location_y'] if self.location_y_edit else None,
						location_z_start=self.location_z_start + self.rigid_body_bone_chains_data[i]['head']['location_z'] if self.location_z_edit else None,
						location_z_end=self.location_z_end + self.rigid_body_bone_chains_data[i]['tail']['location_z'] if self.location_z_edit else None,
						rotation_w_start=self.rotation_w_start + self.rigid_body_bone_chains_data[i]['head']['rotation_w'] if self.rotation_w_edit else None,
						rotation_w_end=self.rotation_w_end + self.rigid_body_bone_chains_data[i]['tail']['rotation_w'] if self.rotation_w_edit else None,
						rotation_x_start=self.rotation_x_start + self.rigid_body_bone_chains_data[i]['head']['rotation_x'] if self.rotation_x_edit else None,
						rotation_x_end=self.rotation_x_end + self.rigid_body_bone_chains_data[i]['tail']['rotation_x'] if self.rotation_x_edit else None,
						rotation_y_start=self.rotation_y_start + self.rigid_body_bone_chains_data[i]['head']['rotation_y'] if self.rotation_y_edit else None,
						rotation_y_end=self.rotation_y_end + self.rigid_body_bone_chains_data[i]['tail']['rotation_y'] if self.rotation_y_edit else None,
						rotation_z_start=self.rotation_z_start + self.rigid_body_bone_chains_data[i]['head']['rotation_z'] if self.rotation_z_edit else None,
						rotation_z_end=self.rotation_z_end + self.rigid_body_bone_chains_data[i]['tail']['rotation_z'] if self.rotation_z_edit else None,
						size_x_start=self.size_x_start + self.rigid_body_bone_chains_data[i]['head']['size_x'] if self.size_x_edit else None,
						size_x_end=self.size_x_end + self.rigid_body_bone_chains_data[i]['tail']['size_x'] if self.size_x_edit else None,
						size_y_start=self.size_y_start + self.rigid_body_bone_chains_data[i]['head']['size_y'] if self.size_y_edit else None,
						size_y_end=self.size_y_end + self.rigid_body_bone_chains_data[i]['tail']['size_y'] if self.size_y_edit else None,
						size_z_start=self.size_z_start + self.rigid_body_bone_chains_data[i]['head']['size_z'] if self.size_z_edit else None,
						size_z_end=self.size_z_end + self.rigid_body_bone_chains_data[i]['tail']['size_z'] if self.size_z_edit else None,
						mass_start=self.mass_start if self.mass_edit else None,
						mass_end=self.mass_end if self.mass_edit else None,
						restitution_start=self.restitution_start if self.restitution_edit else None,
						restitution_end=self.restitution_end if self.restitution_edit else None,
						friction_start=self.friction_start if self.friction_edit else None,
						friction_end=self.friction_end if self.friction_edit else None,
						linear_damping_start=self.linear_damping_start if self.linear_damping_edit else None,
						linear_damping_end=self.linear_damping_end if self.linear_damping_edit else None,
						angular_damping_start=self.angular_damping_start if self.angular_damping_edit else None,
						angular_damping_end=self.angular_damping_end if self.angular_damping_edit else None
					)
			
		return {'FINISHED'}