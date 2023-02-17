import bpy
from . import register_wrap
from . import model
from mmd_tools.operators.rigid_body import AddRigidBody
from . import import_csv
from mmd_tools.core import model as mmd_model
import re
import math
from functools import reduce

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
	
	if bpy.context.active_object.type == 'ARMATURE':
		return model.findArmature(bpy.context.active_object)
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

def apply_all_rigid_bodies(armature,rigid_body_data):
	

	if rigid_body_data: 
		for rigid_body in rigid_body_data:
			rigid_body_name = rigid_body['rigid_body_name']
			bone = rigid_body['bone_name']
			offset_loc = [rigid_body['offset_x'],rigid_body['offset_y'],rigid_body['offset_z']]
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
			create_rigid_body(armature,rigid_body_name,bone,offset_loc,name_j,name_e,collision_group_number,collision_group_mask, rigid_type,rigid_shape,size,mass,friction,bounce,linear_damping,angular_damping)
	

def create_rigid_body(armature,rigid_body_name,bone,offset_loc,name_j,name_e,collision_group_number,collision_group_mask, rigid_type,rigid_shape,size,mass,friction,bounce,linear_damping,angular_damping):

	
	
	#if rigid body exists, delete it
	for obj in armature.parent.children_recursive:
		if obj.mmd_type == 'RIGID_BODY' and obj.name == rigid_body_name:
			print ('deleting existing rigid_body:', obj.name)
			bpy.data.objects.remove(obj, do_unlink=True)

	
	#check if bone exists
	bpy.ops.object.mode_set(mode='EDIT')
	if bone in bpy.context.active_object.data.edit_bones:

		
		"""
		name_j = '$name_j'
		name_e = '$name_e'
		collision_group_number = 0
		collision_group_mask = [True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False] 
		rigid_type = '0' #'0'= Bone, '1' = Physics, '2' = Physics+Bone
		rigid_shape = 'SPHERE' #SPHERE, BOX, CAPSULE
		size = [0.6, 0.6, 0.6]  #X, Y, Z
		mass = 1 
		friction = 0.5
		bounce = 0 #restitution
		linear_damping = 0.04
		angular_damping = 0.1
		"""
		# Select the bone
		
		bpy.ops.armature.select_all(action='DESELECT')
		armature.data.edit_bones[bone].select = True
		armature.data.bones.active = armature.data.bones[bone]
			
		bpy.ops.mmd_tools.rigid_body_add(
			name_j= name_j
			,name_e= name_e
			,collision_group_number=collision_group_number
			,collision_group_mask=collision_group_mask
			,rigid_type=rigid_type
			,rigid_shape=rigid_shape
			,size=size
			,mass=mass
			,friction=friction
			,bounce=bounce
			,linear_damping=linear_damping
			,angular_damping=angular_damping
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
			print("Captured value:", chain_number )
		else:
			print("No match found.")
			
		rb_obj_chain = []
				
		armature = bpy.context.active_object.constraints['mmd_tools_rigid_parent'].target
		bone_name = bpy.context.active_object.constraints['mmd_tools_rigid_parent'].subtarget
		rigid_bodies = None

		#get the 'rigidbodies' object
		for object in armature.parent.children:
			if object.name == 'rigidbodies':
				rigid_bodies = object
		
		if rigid_bodies is not None:
			#get all rigid bodies that have the same chain number as object that was passed
			for rigid_body in rigid_bodies.children:
				
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
			print("Captured value:", chain_number )
		else:
			print("No match found.")
			
		rb_obj_chain = []
		
		armature = bpy.context.active_object.constraints['mmd_tools_rigid_parent'].target
		bone_name = bpy.context.active_object.constraints['mmd_tools_rigid_parent'].subtarget
		rigid_bodies = None

		#get the 'rigidbodies' object
		for object in armature.parent.children:
			if object.name == 'rigidbodies':
				rigid_bodies = object
		
		if rigid_bodies is not None:
			#get all rigid bodies that have the same chain number as object that was passed
			for rigid_body in rigid_bodies.children:
				
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
			obj.select_set(True)
	
	if bpy.context.selected_objects:
		bpy.context.view_layer.objects.active =  bpy.context.selected_objects[0]
		return bpy.context.selected_objects

def get_bone_from_rigid_body (obj = None):
	
	if obj is None and bpy.context.active_object is not None:
		obj = bpy.context.active_object
	
	if obj.mmd_type == 'RIGID_BODY':

		armature_obj_name = obj.constraints['mmd_tools_rigid_parent'].target.data.name   
		armature = bpy.data.armatures[armature_obj_name]
		
		rigid_body_bone_name = obj.constraints['mmd_tools_rigid_parent'].subtarget
		
		for bone in bpy.data.armatures[armature.name].bones:
			if bone.name == rigid_body_bone_name:
					return bone	

def get_rigid_body_bone_chain_origin(bone_obj):
	
	rigid_body_bone = bone_obj        
	
	armature_obj = None
	armature = None
	
	#get the armature and armature object
	if rigid_body_bone is not None:
		armature_name = rigid_body_bone.id_data.name
		obj = bpy.data.objects.get(armature_name)
				
		if obj.type == 'ARMATURE':
			armature_obj = obj
			armature = obj.data
		else:
			for child in obj.children_recursive:
				if child.type == 'ARMATURE':
					armature_obj = child
					armature = child.data
					break
		
	#store all rigid bodies and their associated bone for the armature in a list
	for child in armature_obj.parent.children:
		if child.name.startswith('rigidbodies'):
			rigidbodies_obj = child
			break

	rigid_body_bone_list = []

	for rigid_body_obj in rigidbodies_obj.children:
		rigid_body_bone_list.append((rigid_body_obj,rigid_body_obj.name,rigid_body_obj.constraints['mmd_tools_rigid_parent'].subtarget))
	
	rigid_body_bone_origin = rigid_body_bone   
		
	##Arbitrary number to make sure the while loop definitely exits at some point         
	i = 100
	while i >= 0:
		
		has_rigid_body = False
		has_only_one_child_bone = True
		has_use_connect_false = True
		
		#check if bone has a rigid body
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
		if (armature.bones[rigid_body_bone.name].use_connect) == False:
			has_use_connect_false = False
		
		rigid_body_bone = rigid_body_bone.parent
		
		if has_rigid_body == True and has_only_one_child_bone == True and has_use_connect_false == True:
			rigid_body_bone_origin = rigid_body_bone
		else:
			break           
		i = i-1

	return rigid_body_bone_origin
	
	
def get_rigid_body_chain_from_bone(rigid_body_bone_origin):
	
	armature_name = rigid_body_bone_origin.id_data.name
	
	obj = bpy.data.objects.get(armature_name)
	armature_obj = None
	
	if obj.type == 'ARMATURE':
		armature_obj = obj
	else:
		for child in obj.children_recursive:
			if child.type == 'ARMATURE':
				armature_obj = child
				break
			
	#store all rigid bodies and their associated bone for the armature in a list
	for child in armature_obj.parent.children:
		if child.name.startswith('rigidbodies'):
			rigidbodies_obj = child
			break
		
	rigid_body_bone_list = []
	
	for rigid_body_obj in rigidbodies_obj.children:
		rigid_body_bone_list.append((rigid_body_obj,rigid_body_obj.name,rigid_body_obj.constraints['mmd_tools_rigid_parent'].subtarget))

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

	"""
	selected_bones_working_list = selected_bones.copy()
	#initialize the bone order list
	for bone in selected_parent_bones:
		rigid_body_bone_chains.append([bone])
		selected_bones_working_list.remove(bone)
		

	#append the children to the parent bone on the bone order list
	for i,bone_chain in enumerate(rigid_body_bone_chains):
		for parent_bone in bone_chain:
			for child in parent_bone.children:
				if child in selected_bones:
					rigid_body_bone_chains[i].append(child)
					selected_bones_working_list.remove(child)

	#double checking to see if we have no orphans
	if len(selected_bones_working_list) != 0:
		for i in selected_bones_working_list:
			print ('orphan bone found that is not on a rigid body chain: ',i.name)

	return rigid_body_bone_chains
	"""
		


	




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
	if rigid_body_type is not None:
		obj.mmd_rigid.type = rigid_body_type
		#'0' = bone
		#'1' = physics
		#'2' = physics+bone
	if mass is not None:
		obj.rigid_body.mass = mass
	if restitution is not None:
		obj.rigid_body.restitution = restitution 
	if collision_group_number is not None:
		obj.mmd_rigid.collision_group_number = collision_group_number
	if collision_group_mask is not None:
		obj.mmd_rigid.collision_group_mask = collision_group_mask
		#collision_group_mask = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
	if friction is not None:
		obj.rigid_body.friction = friction
	if linear_damping is not None:
		obj.rigid_body.linear_damping = linear_damping
	if angular_damping is not None:
		obj.rigid_body.angular_damping = angular_damping



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


		


def transform_rigid_body_bone_chains_by_delta(rigid_body_bone_chain
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
	
	
	armature_obj_name = rigid_body_bone_chain[0][2].constraints['mmd_tools_rigid_parent'].target.data.name
	armature = bpy.data.armatures[armature_obj_name]

	bone_chain_head = armature.bones[rigid_body_bone_chain[0][1]]
	bone_chain_tail = armature.bones[rigid_body_bone_chain[len(rigid_body_bone_chain)-1][1]]
	body_chain_length = len(rigid_body_bone_chain)

	#print(body_chain_length)

	starting_rigid_body = rigid_body_bone_chain[0][2]
	ending_rigid_body = rigid_body_bone_chain[len(rigid_body_bone_chain)-1][2]
	
	for prop, var, start, end in [('location.x','location_x', location_x_start, location_x_end),
								('location.y','location_y', location_y_start, location_y_end),
								('location.z','location_z', location_z_start, location_z_end),
								('w','rotation_w', rotation_w_start, rotation_w_end),
								('x','rotation_x', rotation_x_start, rotation_x_end),
								('y','rotation_y', rotation_y_start, rotation_y_end),
								('z','rotation_z', rotation_z_start, rotation_z_end),
								('mmd_rigid.size[0]','size_x', size_x_start, size_x_end),
								('mmd_rigid.size[1]','size_y', size_y_start, size_y_end),
								('mmd_rigid.size[2]','size_z', size_z_start, size_z_end),
								('rigid_body.mass','mass', mass_start, mass_end),
								('rigid_body.restitution','restitution', restitution_start, restitution_end),
								('rigid_body.friction','friction', friction_start, friction_end),
								('rigid_body.linear_damping','linear_damping', linear_damping_start, linear_damping_end),
								('rigid_body.angular_damping','angular_damping', angular_damping_start, angular_damping_end)]:
		if start is not None and end is not None:

			if var in ['rotation_w','rotation_x','rotation_y','rotation_z']:
				if starting_rigid_body.rotation_mode == 'QUATERNION' and ending_rigid_body.rotation_mode == 'QUATERNION':
					start_value =  get_attribute(starting_rigid_body,'rotation_quaternion.' + prop) + start
					end_value =  get_attribute(ending_rigid_body,'rotation_quaternion.' + prop) + end
				elif starting_rigid_body.rotation_mode == 'AXIS_ANGLE' and ending_rigid_body.rotation_mode == 'AXIS_ANGLE':
					start_value =  get_attribute(starting_rigid_body,'rotation_axis_angle.' + prop) + start
					end_value =  get_attribute(ending_rigid_body,'rotation_axis_angle.' + prop) + end
				else:
					start_value =  get_attribute(starting_rigid_body,'rotation_euler.' + prop) + start
					end_value =  get_attribute(ending_rigid_body,'rotation_euler.' + prop) + end

			else:
				start_value = get_attribute(starting_rigid_body, prop) + start
				end_value = get_attribute(ending_rigid_body, prop) + end

			if var in ['size_x', 'size_y', 'size_z', 'mass', 'restitution', 'friction', 'linear_damping', 'angular_damping']:
				start_value = max(0, start_value)
				end_value = max(0, end_value)
			transform_rigid_body_bone_chain_property(rigid_body_bone_chain, var, start_value, end_value)
	
	
	
	


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
			
			else:
				print(armature_obj)
				print(armature_obj.type)
				print('this is not an armature!')
			

			bpy.context.view_layer.objects.active = active_obj



def _transform_rigid_body_bone_chains_by_delta(self,context):

	rigid_body_bone_chains = get_all_rigid_body_chains_from_selected()

	for rigid_body_bone_chain in rigid_body_bone_chains:

		transform_rigid_body_bone_chains_by_delta(
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
		)




def _transform_rigid_body_bone_chain(self,context):

	rigid_body_bone_chain = get_selected_rigid_bodies_in_bone_chain()

	"""
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'size_x',self.size_x_start,self.size_x_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'size_y',self.size_y_start,self.size_y_end)
	transform_rigid_body_bone_chain_property(rigid_body_bone_chain,'size_z',self.size_z_start,self.size_z_end)
	"""
	
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
	)


def _transform_selected_rigid_bodies(self,context):

	#obj = context.active_object 


	transform_selected_rigid_bodies(
		location_x=self.location_x if self.location_x_edit else None,
		location_y=self.location_y if self.location_y_edit else None,
		location_z=self.location_z if self.location_z_edit else None,
		rotation_mode=self.rotation_mode if self.rotation_mode_edit else None,
		rotation_w=self.rotation_w if self.rotation_w_edit else None,
		rotation_x=self.rotation_x if self.rotation_x_edit else None,
		rotation_y=self.rotation_y if self.rotation_y_edit else None,
		rotation_z=self.rotation_z if self.rotation_z_edit else None,
		size_x=self.size_x if self.size_x_edit else None,
		size_y=self.size_y if self.size_y_edit else None,
		size_z=self.size_z if self.size_z_edit else None,
	)

	

	



def create_rigid_bodies_from_csv(context):
	bpy.context.view_layer.objects.active = get_armature()
	armature = get_armature()

	RIGID_BODY_DICTIONARY = read_rigid_body_file ()
	
	apply_all_rigid_bodies(armature, RIGID_BODY_DICTIONARY)
	#apply_all_rigid_bodies(armature)

@register_wrap
class AddRigidBody(bpy.types.Operator):
	"""Add Rigid Bodies to a FFXIV Model (Converted to an MMD Model)"""
	bl_idname = "ffxiv_mmd_tools_helper.add_rigid_body"
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
class SelectVerticalSkirtRigidBodies(bpy.types.Operator):
	"""Select All Rigid Bodies in the vertical rigid body skirt chain"""
	bl_idname = "ffxiv_mmd_tools_helper.get_vertical_skirt_rigid_bodies"
	bl_label = "Select All Skirt Rigid Bodies in Vertical Chain"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.mmd_type == 'RIGID_BODY' and obj.name.startswith('skirt_')

	def execute(self, context):
		get_skirt_rigid_vertical_objects(context.active_object)
		return {'FINISHED'}

@register_wrap
class SelectHorizontalSkirtRigidBodies(bpy.types.Operator):
	"""Select All Rigid Bodies in the horizontal rigid body skirt chain with the same number"""
	bl_idname = "ffxiv_mmd_tools_helper.get_horizontal_skirt_rigid_bodies"
	bl_label = "Select All Skirt Rigid Bodies in Horizontal Chain"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.mmd_type == 'RIGID_BODY' and obj.name.startswith('skirt_')

	def execute(self, context):
		get_skirt_rigid_horizontal_objects(context.active_object)
		return {'FINISHED'}



@register_wrap
class SelectSkirtRigidBodies(bpy.types.Operator):
	"""Select All Rigid Bodies in a skirt """
	bl_idname = "ffxiv_mmd_tools_helper.get_skirt_rigid_bodies"
	bl_label = "Select All Skirt Rigid Bodies"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.mmd_type == 'RIGID_BODY' and obj.name.startswith('skirt_')

	def execute(self, context):
		find_rigid_bodies(startswith='skirt_')
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

@register_wrap
class SelectRigidBodyBoneChain(bpy.types.Operator):
	"""Get Rigid Bodies From Bone Chain"""
	bl_idname = "ffxiv_mmd_tools_helper.select_rigid_body_bone_chain"
	bl_label = "Get Rigid Bodies From Bone Chain"

	direction: bpy.props.EnumProperty(items = \
	[('ALL', 'ALL', 'ALL')\
		,('DOWN', 'DOWN', 'DOWN')\
	], name = "", default = 'DOWN')

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.mmd_type == 'RIGID_BODY'

	def execute(self, context):
		bone = get_bone_from_rigid_body(context.active_object)
		bone_chain_origin = get_rigid_body_bone_chain_origin(bone)
		if self.direction == 'ALL':
			get_rigid_body_chain_from_bone(bone_chain_origin)
		elif self.direction == 'DOWN':
			get_rigid_body_chain_from_bone(bone)
		return {'FINISHED'}




@register_wrap
class BatchUpdateRigidBodies(bpy.types.Operator):
	""" Bulk Update all Selected Rigid Bodies using the Active Rigid Body """
	bl_idname = "ffxiv_mmd_tools_helper.batch_update_rigid_bodies"
	bl_label = "Batch Update Rigid Bodies"
	bl_options = {'REGISTER','UNDO','PRESET','BLOCKING'} 

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

		self.location_x = obj.location.x
		self.location_y = obj.location.y
		self.location_z = obj.location.z
		self.rotation_mode = obj.rotation_mode
		if obj.rotation_mode == 'QUATERNION':
			self.rotation_w = obj.rotation_quaternion.w
			self.rotation_x = obj.rotation_quaternion.x
			self.rotation_y = obj.rotation_quaternion.y
			self.rotation_z = obj.rotation_quaternion.z
		elif obj.rotation_mode == 'AXIS_ANGLE':
			self.rotation_w = obj.rotation_axis_angle.w
			self.rotation_x = obj.rotation_axis_angle.x
			self.rotation_y = obj.rotation_axis_angle.y
			self.rotation_z = obj.rotation_axis_angle.z
		else:
			self.rotation_w = 0
			self.rotation_x = obj.rotation_euler.x
			self.rotation_y = obj.rotation_euler.y
			self.rotation_z = obj.rotation_euler.z
		self.size_x = obj.mmd_rigid.size[0]
		self.size_y = obj.mmd_rigid.size[1]
		self.size_z = obj.mmd_rigid.size[2]
		self.rigid_body_type = obj.mmd_rigid.type
		self.rigid_body_shape = obj.mmd_rigid.shape
		self.mass = obj.rigid_body.mass
		self.restitution = obj.rigid_body.restitution
		self.collision_group_number = obj.mmd_rigid.collision_group_number
		self.collision_group_mask = obj.mmd_rigid.collision_group_mask
		self.friction = obj.rigid_body.friction
		self.linear_damping = obj.rigid_body.linear_damping
		self.angular_damping = obj.rigid_body.angular_damping
		

		wm = context.window_manager		
		return wm.invoke_props_dialog(self, width=400)


	def draw(self, context):
		layout = self.layout

		obj = context.active_object 

		
		armature_name = context.active_object.constraints['mmd_tools_rigid_parent'].target
		bone_name = context.active_object.constraints['mmd_tools_rigid_parent'].subtarget
		

		row = layout.row()
		row.label(text='Active Object: '+ context.active_object.name)
		
		row.label(text='Active Object Bone: '+ bone_name)

		#c.prop(obj.mmd_rigid, 'name_j')
		#c.prop(obj.mmd_rigid, 'name_e')

		row = layout.row()
		row.label(text='Checkmark to apply to all selected rigid bodies')
		row = layout.row()
		c = row.column(align=True)
		c = row.column(align=True)
		c.label(text='Location:')
		c.label(text="")
		c.label(text="")
		c.label(text="")
		c = row.column(align=True)
		c.prop(self,"location_x",text="",toggle=False)
		c.prop(self,"location_y",text="",toggle=False)
		c.prop(self,"location_z",text="",toggle=False)
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

		row = layout.row()
		row = layout.row()
		c = row.column(align=True)
		if self.rotation_mode in('QUATERNION','AXIS_ANGLE'):
			c = row.column(align=True)
			c.label(text='Rotation')
			c.label(text='')
			c.label(text='')
			c.label(text='')
			c = row.column(align=True)
			c.prop(self,"rotation_w",index=0,text="W")
			c.prop(self,"rotation_x",index=1,text="X")
			c.prop(self,"rotation_y",index=2,text="Y")
			c.prop(self,"rotation_z",index=3,text="Z")
			c.operator("ffxiv_mmd_tools_helper.reset_rotation_rigid_bodies",text="Reset to bone")
			c = row.column(align=True)
			c.prop(self, "rotation_w_edit", text="")
			c.prop(self, "rotation_x_edit", text="")
			c.prop(self, "rotation_y_edit", text="")
			c.prop(self, "rotation_z_edit", text="")
		else:
			c = row.column(align=True)
			c.label(text='Rotation')
			c.label(text='')
			c.label(text='')
			c = row.column(align=True)
			c.prop(self,"rotation_x",index=1,text="X")
			c.prop(self,"rotation_y",index=2,text="Y")
			c.prop(self,"rotation_z",index=3,text="Z")
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
		if (self.size_x_edit or self.size_y_edit or self.size_z_edit):
			self.rigid_body_shape_edit = True
		row = g.row(align=True)
		row.prop(obj.mmd_rigid, 'shape', expand=True)
		row.prop(self, "rigid_body_shape_edit", text="")
		#c.column(align=True).prop(obj.mmd_rigid, 'size', text='')
		#row = g.row(align=True)
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
		#c.prop(obj.mmd_rigid, 'collision_group_mask')
		#col = c.column(align=True)
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
			w=self.rotation_quaternion.w
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
					location_x=self.location.x if self.location_x_edit else None,
					location_y=self.location.y if self.location_y_edit else None,
					location_z=self.location.z if self.location_z_edit else None,
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

	#checkbox to bulk edit
	location_x_edit: bpy.props.BoolProperty(default=False)
	location_y_edit: bpy.props.BoolProperty(default=False)
	location_z_edit: bpy.props.BoolProperty(default=False)
	rotation_w_edit: bpy.props.BoolProperty(default=False)
	rotation_x_edit: bpy.props.BoolProperty(default=False)
	rotation_y_edit: bpy.props.BoolProperty(default=False)
	rotation_z_edit: bpy.props.BoolProperty(default=False)
	size_x_edit:bpy.props.BoolProperty(default=False)
	size_y_edit:bpy.props.BoolProperty(default=False)
	size_z_edit:bpy.props.BoolProperty(default=False)
	mass_edit: bpy.props.BoolProperty(default=False)
	restitution_edit: bpy.props.BoolProperty(default=False)
	collision_group_number_edit: bpy.props.BoolProperty(default=False)
	collision_group_mask_edit: bpy.props.BoolProperty(default=False)
	friction_edit: bpy.props.BoolProperty(default=False)
	linear_damping_edit: bpy.props.BoolProperty(default=False)
	angular_damping_edit: bpy.props.BoolProperty(default=False)
	

	#original values
	rigid_body_bone_chain = None
	bone_head = None
	bone_tail = None
	rigid_body_length = None
	location_x_start: bpy.props.FloatProperty(default=0,unit='LENGTH',update=_transform_rigid_body_bone_chain)
	location_x_end: bpy.props.FloatProperty(default=0,unit='LENGTH',update=_transform_rigid_body_bone_chain)
	location_y_start: bpy.props.FloatProperty(default=0,unit='LENGTH',update=_transform_rigid_body_bone_chain)
	location_y_end: bpy.props.FloatProperty(default=0,unit='LENGTH',update=_transform_rigid_body_bone_chain)
	location_z_start: bpy.props.FloatProperty(default=0,unit='LENGTH',update=_transform_rigid_body_bone_chain)
	location_z_end: bpy.props.FloatProperty(default=0,unit='LENGTH',update=_transform_rigid_body_bone_chain)
	rotation_w_start: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chain)
	rotation_w_end: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chain)
	rotation_x_start: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chain)
	rotation_x_end: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chain)
	rotation_y_start: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chain)
	rotation_y_end: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chain)
	rotation_z_start: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chain)
	rotation_z_end: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chain)
	size_x_start:bpy.props.FloatProperty(default=0,min=0,precision=6,update=_transform_rigid_body_bone_chain)
	size_x_end:bpy.props.FloatProperty(default=0,min=0,precision=6,update=_transform_rigid_body_bone_chain)
	size_y_start:bpy.props.FloatProperty(default=0,min=0,precision=6,update=_transform_rigid_body_bone_chain)
	size_y_end:bpy.props.FloatProperty(default=0,min=0,precision=6,update=_transform_rigid_body_bone_chain)
	size_z_start:bpy.props.FloatProperty(default=0,min=0,precision=6,update=_transform_rigid_body_bone_chain)
	size_z_end:bpy.props.FloatProperty(default=0,min=0,precision=6,update=_transform_rigid_body_bone_chain)
	mass_start: bpy.props.FloatProperty(default=0,min=0,precision=6,unit='MASS')
	mass_end = bpy.props.FloatProperty(default=0,min=0,precision=6,unit='MASS')
	restitution_start = bpy.props.FloatProperty(default=0,min=0,max=1,precision=6)
	restitution_end = bpy.props.FloatProperty(default=0,min=0,max=1,precision=6)
	friction_start = bpy.props.FloatProperty(default=0,min=0,max=1,precision=6)
	friction_end = bpy.props.FloatProperty(default=0,min=0,max=1,precision=6)
	linear_damping_start = bpy.props.FloatProperty(default=0,min=0,max=1,precision=6)
	linear_damping_end = bpy.props.FloatProperty(default=0,min=0,max=1,precision=6)
	angular_damping_start = bpy.props.FloatProperty(default=0,min=0,max=1,precision=6)
	angular_damping_end = bpy.props.FloatProperty(default=0,min=0,max=1,precision=6)
	
	

	def invoke(self, context, event):

		#selected_objs = context.selected_objects
		
		self.rigid_body_bone_chain = get_selected_rigid_bodies_in_bone_chain()

		self.bone_head = self.rigid_body_bone_chain[0][1]
		self.bone_tail = self.rigid_body_bone_chain[len(self.rigid_body_bone_chain)-1][1]
		self.rigid_body_length = str(len(self.rigid_body_bone_chain))
		
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
		self.mass_edit = False
		self.restitution_edit = False
		self.friction_edit = False
		self.linear_damping_edit = False
		self.angular_damping_edit = False

		starting_rigid_body = self.rigid_body_bone_chain[0][2]
		ending_rigid_body = self.rigid_body_bone_chain[len(self.rigid_body_bone_chain)-1][2]

		self.location_x_start = starting_rigid_body.location.x
		self.location_x_end = ending_rigid_body.location.x
		self.location_y_start = starting_rigid_body.location.y
		self.location_y_end = ending_rigid_body.location.y
		self.location_z_start = starting_rigid_body.location.z
		self.location_z_end = ending_rigid_body.location.z
		if starting_rigid_body.rotation_mode == 'QUATERNION' and ending_rigid_body.rotation_mode == 'QUATERNION':
			self.rotation_w_start = starting_rigid_body.rotation_quaternion.w
			self.rotation_w_end = ending_rigid_body.rotation_quaternion.w
			self.rotation_x_start = starting_rigid_body.rotation_quaternion.x
			self.rotation_x_end = ending_rigid_body.rotation_quaternion.x
			self.rotation_y_start = starting_rigid_body.rotation_quaternion.y
			self.rotation_y_end = ending_rigid_body.rotation_quaternion.y
			self.rotation_z_start = starting_rigid_body.rotation_quaternion.z		
			self.rotation_z_end = ending_rigid_body.rotation_quaternion.z
		elif starting_rigid_body.rotation_mode == 'AXIS_ANGLE' and ending_rigid_body.rotation_mode == 'AXIS_ANGLE':
			self.rotation_w_start = starting_rigid_body.rotation_axis_angle.w
			self.rotation_w_end = ending_rigid_body.rotation_axis_angle.w
			self.rotation_x_start = starting_rigid_body.rotation_axis_angle.x
			self.rotation_x_end = ending_rigid_body.rotation_axis_angle.x
			self.rotation_y_start = starting_rigid_body.rotation_axis_angle.y
			self.rotation_y_end = ending_rigid_body.rotation_axis_angle.y
			self.rotation_z_start = starting_rigid_body.rotation_axis_angle.z		
			self.rotation_z_end = ending_rigid_body.rotation_axis_angle.z
		else:
			self.rotation_w_start = 0
			self.rotation_w_end = 0
			self.rotation_x_start = starting_rigid_body.rotation_euler.x
			self.rotation_x_end = ending_rigid_body.rotation_euler.x
			self.rotation_y_start = starting_rigid_body.rotation_euler.y
			self.rotation_y_end = ending_rigid_body.rotation_euler.y
			self.rotation_z_start = starting_rigid_body.rotation_euler.z		
			self.rotation_z_end = ending_rigid_body.rotation_euler.z
		self.size_x_start = starting_rigid_body.mmd_rigid.size[0]
		self.size_x_end = ending_rigid_body.mmd_rigid.size[0]
		self.size_y_start = starting_rigid_body.mmd_rigid.size[1]
		self.size_y_end = ending_rigid_body.mmd_rigid.size[1]
		self.size_z_start = starting_rigid_body.mmd_rigid.size[2]
		self.size_z_end = ending_rigid_body.mmd_rigid.size[2]
		self.mass_start= starting_rigid_body.rigid_body.mass
		self.mass_end= ending_rigid_body.rigid_body.mass
		self.restitution_start = starting_rigid_body.rigid_body.restitution
		self.restitution_end = ending_rigid_body.rigid_body.restitution
		self.friction_start = starting_rigid_body.rigid_body.friction
		self.friction_end = ending_rigid_body.rigid_body.friction
		self.linear_damping_start = starting_rigid_body.rigid_body.linear_damping
		self.linear_damping_end = ending_rigid_body.rigid_body.linear_damping
		self.angular_damping_start = starting_rigid_body.rigid_body.angular_damping
		self.angular_damping_end = ending_rigid_body.rigid_body.angular_damping
		

		wm = context.window_manager		
		return wm.invoke_props_dialog(self, width=400)


	def draw(self, context):
		layout = self.layout

		starting_rigid_body = self.rigid_body_bone_chain[0][2]
		ending_rigid_body = self.rigid_body_bone_chain[len(self.rigid_body_bone_chain)-1][2]

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
		obj = context.active_object 
		return obj is not None and is_selected_rigid_bodies_in_a_bone_chain()


	def execute(self, context):

		bpy.ops.object.mode_set(mode='OBJECT')
		
		for bone in self.rigid_body_bone_chain:
			print (bone)
		
		
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


@register_wrap
class BatchUpdateMultipleRigidBodyBoneChain(bpy.types.Operator):
	""" Update Multiple Rigid Bodies in a Bone Chain with by delta of start and end values """
	bl_idname = "ffxiv_mmd_tools_helper.batch_update_rigid_body_bone_chains"
	bl_label = "Update Multiple Rigid Bodies by Bone Chain by delta"
	bl_options = {'REGISTER','UNDO','PRESET','BLOCKING'} 

	#checkbox to bulk edit
	location_x_edit: bpy.props.BoolProperty(default=False)
	location_y_edit: bpy.props.BoolProperty(default=False)
	location_z_edit: bpy.props.BoolProperty(default=False)
	rotation_w_edit: bpy.props.BoolProperty(default=False)
	rotation_x_edit: bpy.props.BoolProperty(default=False)
	rotation_y_edit: bpy.props.BoolProperty(default=False)
	rotation_z_edit: bpy.props.BoolProperty(default=False)
	size_x_edit:bpy.props.BoolProperty(default=False)
	size_y_edit:bpy.props.BoolProperty(default=False)
	size_z_edit:bpy.props.BoolProperty(default=False)
	mass_edit: bpy.props.BoolProperty(default=False)
	restitution_edit: bpy.props.BoolProperty(default=False)
	collision_group_number_edit: bpy.props.BoolProperty(default=False)
	collision_group_mask_edit: bpy.props.BoolProperty(default=False)
	friction_edit: bpy.props.BoolProperty(default=False)
	linear_damping_edit: bpy.props.BoolProperty(default=False)
	angular_damping_edit: bpy.props.BoolProperty(default=False)
	

	#original values
	rigid_body_bone_chains = None
	bone_head = None
	bone_tail = None
	rigid_body_length = None
	location_x_start: bpy.props.FloatProperty(default=0,unit='LENGTH',update=_transform_rigid_body_bone_chains_by_delta)
	location_x_end: bpy.props.FloatProperty(default=0,unit='LENGTH',update=_transform_rigid_body_bone_chains_by_delta)
	location_y_start: bpy.props.FloatProperty(default=0,unit='LENGTH',update=_transform_rigid_body_bone_chains_by_delta)
	location_y_end: bpy.props.FloatProperty(default=0,unit='LENGTH',update=_transform_rigid_body_bone_chains_by_delta)
	location_z_start: bpy.props.FloatProperty(default=0,unit='LENGTH',update=_transform_rigid_body_bone_chains_by_delta)
	location_z_end: bpy.props.FloatProperty(default=0,unit='LENGTH',update=_transform_rigid_body_bone_chains_by_delta)
	rotation_w_start: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chains_by_delta)
	rotation_w_end: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chains_by_delta)
	rotation_x_start: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chains_by_delta)
	rotation_x_end: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chains_by_delta)
	rotation_y_start: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chains_by_delta)
	rotation_y_end: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chains_by_delta)
	rotation_z_start: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chains_by_delta)
	rotation_z_end: bpy.props.FloatProperty(default=0,unit='ROTATION',update=_transform_rigid_body_bone_chains_by_delta)
	size_x_start:bpy.props.FloatProperty(default=0,min=-1,precision=6,update=_transform_rigid_body_bone_chains_by_delta)
	size_x_end:bpy.props.FloatProperty(default=0,min=-1,precision=6,update=_transform_rigid_body_bone_chains_by_delta)
	size_y_start:bpy.props.FloatProperty(default=0,min=-1,precision=6,update=_transform_rigid_body_bone_chains_by_delta)
	size_y_end:bpy.props.FloatProperty(default=0,min=-1,precision=6,update=_transform_rigid_body_bone_chains_by_delta)
	size_z_start:bpy.props.FloatProperty(default=0,min=-1,precision=6,update=_transform_rigid_body_bone_chains_by_delta)
	size_z_end:bpy.props.FloatProperty(default=0,min=-1,precision=6,update=_transform_rigid_body_bone_chains_by_delta)
	mass_start: bpy.props.FloatProperty(default=0,min=-1,precision=6,unit='MASS')
	mass_end = bpy.props.FloatProperty(default=0,min=-1,precision=6,unit='MASS')
	restitution_start = bpy.props.FloatProperty(default=0,min=-1,max=1,precision=6)
	restitution_end = bpy.props.FloatProperty(default=0,min=-1,max=1,precision=6)
	friction_start = bpy.props.FloatProperty(default=0,min=-1,max=1,precision=6)
	friction_end = bpy.props.FloatProperty(default=0,min=-1,max=1,precision=6)
	linear_damping_start = bpy.props.FloatProperty(default=0,min=-1,max=1,precision=6)
	linear_damping_end = bpy.props.FloatProperty(default=0,min=-1,max=1,precision=6)
	angular_damping_start = bpy.props.FloatProperty(default=0,min=-1,max=1,precision=6)
	angular_damping_end = bpy.props.FloatProperty(default=0,min=-1,max=1,precision=6)
	
	

	def invoke(self, context, event):

		#selected_objs = context.selected_objects
		
		self.rigid_body_bone_chains = get_all_rigid_body_chains_from_selected()

		self.bone_head = self.rigid_body_bone_chains[0][0][1]
		self.bone_tail = self.rigid_body_bone_chains[0][len(self.rigid_body_bone_chains[0])-1][1]
		self.rigid_body_length = str(len(self.rigid_body_bone_chains[0]))
		
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
		self.mass_edit = False
		self.restitution_edit = False
		self.friction_edit = False
		self.linear_damping_edit = False
		self.angular_damping_edit = False

		starting_rigid_body = self.rigid_body_bone_chains[0][0][2]
		ending_rigid_body = self.rigid_body_bone_chains[0][len(self.rigid_body_bone_chains[0])-1][2]

		self.location_x_start = starting_rigid_body.location.x
		self.location_x_end = ending_rigid_body.location.x
		self.location_y_start = starting_rigid_body.location.y
		self.location_y_end = ending_rigid_body.location.y
		self.location_z_start = starting_rigid_body.location.z
		self.location_z_end = ending_rigid_body.location.z
		if starting_rigid_body.rotation_mode == 'QUATERNION' and ending_rigid_body.rotation_mode == 'QUATERNION':
			self.rotation_w_start = starting_rigid_body.rotation_quaternion.w
			self.rotation_w_end = ending_rigid_body.rotation_quaternion.w
			self.rotation_x_start = starting_rigid_body.rotation_quaternion.x
			self.rotation_x_end = ending_rigid_body.rotation_quaternion.x
			self.rotation_y_start = starting_rigid_body.rotation_quaternion.y
			self.rotation_y_end = ending_rigid_body.rotation_quaternion.y
			self.rotation_z_start = starting_rigid_body.rotation_quaternion.z		
			self.rotation_z_end = ending_rigid_body.rotation_quaternion.z
		elif starting_rigid_body.rotation_mode == 'AXIS_ANGLE' and ending_rigid_body.rotation_mode == 'AXIS_ANGLE':
			self.rotation_w_start = starting_rigid_body.rotation_axis_angle.w
			self.rotation_w_end = ending_rigid_body.rotation_axis_angle.w
			self.rotation_x_start = starting_rigid_body.rotation_axis_angle.x
			self.rotation_x_end = ending_rigid_body.rotation_axis_angle.x
			self.rotation_y_start = starting_rigid_body.rotation_axis_angle.y
			self.rotation_y_end = ending_rigid_body.rotation_axis_angle.y
			self.rotation_z_start = starting_rigid_body.rotation_axis_angle.z		
			self.rotation_z_end = ending_rigid_body.rotation_axis_angle.z
		else:
			self.rotation_w_start = 0
			self.rotation_w_end = 0
			self.rotation_x_start = starting_rigid_body.rotation_euler.x
			self.rotation_x_end = ending_rigid_body.rotation_euler.x
			self.rotation_y_start = starting_rigid_body.rotation_euler.y
			self.rotation_y_end = ending_rigid_body.rotation_euler.y
			self.rotation_z_start = starting_rigid_body.rotation_euler.z		
			self.rotation_z_end = ending_rigid_body.rotation_euler.z
		self.size_x_start = starting_rigid_body.mmd_rigid.size[0]
		self.size_x_end = ending_rigid_body.mmd_rigid.size[0]
		self.size_y_start = starting_rigid_body.mmd_rigid.size[1]
		self.size_y_end = ending_rigid_body.mmd_rigid.size[1]
		self.size_z_start = starting_rigid_body.mmd_rigid.size[2]
		self.size_z_end = ending_rigid_body.mmd_rigid.size[2]
		self.mass_start= starting_rigid_body.rigid_body.mass
		self.mass_end= ending_rigid_body.rigid_body.mass
		self.restitution_start = starting_rigid_body.rigid_body.restitution
		self.restitution_end = ending_rigid_body.rigid_body.restitution
		self.friction_start = starting_rigid_body.rigid_body.friction
		self.friction_end = ending_rigid_body.rigid_body.friction
		self.linear_damping_start = starting_rigid_body.rigid_body.linear_damping
		self.linear_damping_end = ending_rigid_body.rigid_body.linear_damping
		self.angular_damping_start = starting_rigid_body.rigid_body.angular_damping
		self.angular_damping_end = ending_rigid_body.rigid_body.angular_damping
		

		wm = context.window_manager		
		return wm.invoke_props_dialog(self, width=400)


	def draw(self, context):
		layout = self.layout

		starting_rigid_body = self.rigid_body_bone_chains[0][0][2]
		ending_rigid_body = self.rigid_body_bone_chains[0][len(self.rigid_body_bone_chains[0])-1][2]

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
		obj = context.active_object 
		return obj is not None 


	def execute(self, context):

		bpy.ops.object.mode_set(mode='OBJECT')
		
		
		for rigid_body_bone_chain in self.rigid_body_bone_chains:
		
			# Call the function and only pass the non-None parameters
			transform_rigid_body_bone_chains_by_delta(
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