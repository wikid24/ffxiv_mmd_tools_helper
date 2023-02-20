import bpy
from . import register_wrap
from . import model
from . import import_csv
import math
from mmd_tools.operators.rigid_body import AddRigidBody
from mmd_tools.core import model as mmd_model
from functools import reduce 
from . import rigid_body


def get_attribute(obj, attr_name):
    if "[" in attr_name and "]" in attr_name:
        attr_base, index_str = attr_name.split("[")
        index = int(index_str.strip("]"))
        attr_value = reduce(getattr, attr_base.split("."), obj)
        return getattr(attr_value, f"__getitem__")(index)
    else:
        return reduce(getattr, attr_name.split("."), obj)


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

def read_joints_file():
	
	JOINTS_DICTIONARY = None
	JOINTS_DICTIONARY = import_csv.use_csv_joints_dictionary()
	#convert the list into a dictionary with a header
	JOINTS_DICTIONARY = [dict(zip(JOINTS_DICTIONARY[0],row)) for row in JOINTS_DICTIONARY[1:]]
	#convert the values in 'use_bone_rotation' into a bool
	for row in JOINTS_DICTIONARY:
		row['use_bone_rotation'] = bool(row['use_bone_rotation'])
	
	return JOINTS_DICTIONARY

def create_joint(armature,joint_name,rigid_body_1,rigid_body_2,use_bone_rotation,limit_linear_lower,limit_linear_upper,limit_angular_lower,limit_angular_upper, spring_linear,spring_angular):

	#check if joint exists, if it does delete it
	for obj in armature.parent.children_recursive:
		if obj.mmd_type == 'JOINT': 
			#error handling: delete a joint if it does not have both object 1 AND object 2 filled out
			if (obj.rigid_body_constraint.object1 is None or obj.rigid_body_constraint.object2 is None ):
				print ('deleting joint with missing rigid body object1 or object2:', obj.name)
				bpy.data.objects.remove(obj, do_unlink=True)
			#error handling: if both object 1 and object 2 are found, delete the existing joint
			elif (obj.rigid_body_constraint.object1.name == rigid_body_1 or  obj.rigid_body_constraint.object1.name == rigid_body_2):
				if (obj.rigid_body_constraint.object2.name == rigid_body_1 or  obj.rigid_body_constraint.object2.name == rigid_body_2):
					print ('deleting existing joint:', obj.name)
					bpy.data.objects.remove(obj, do_unlink=True)
	
	object_1 = None
	object_2 = None

	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action='DESELECT')    

	#object 1
	for obj in armature.parent.children_recursive:
		if obj.mmd_type == 'RIGID_BODY' and obj.name == rigid_body_1:
			object_1 = obj
			object_1.select_set(True)
			bpy.context.view_layer.objects.active = object_1
	#object 2
	for obj in armature.parent.children_recursive:
		if obj.mmd_type == 'RIGID_BODY' and obj.name == rigid_body_2:
			object_2 = obj
			object_2.select_set(True)
			bpy.context.view_layer.objects.active = object_2
			
	if (object_1 is not None) and (object_2 is not None):
		#create the joint
		bpy.ops.mmd_tools.joint_add(
			use_bone_rotation= use_bone_rotation
			,limit_linear_lower= limit_linear_lower
			,limit_linear_upper=limit_linear_upper
			,limit_angular_lower=limit_angular_lower
			,limit_angular_upper=limit_angular_upper
			,spring_linear=spring_linear
			,spring_angular=spring_angular
		)
		
		joint = bpy.context.view_layer.objects.active
		joint.name = joint_name
		#joint.rotation_euler[0] = 0 #sets x rotation to 0
		bpy.context.view_layer.objects.active = joint
		print ('created joint: ',joint.name)
		
		return joint
	else: 
		print ('could not find either \'', rigid_body_1, '\' or \'',rigid_body_2,'\' to create joint')

def apply_all_joints(armature,joints_data):
	
	if joints_data: 
		for joint in joints_data:
			joint_name = joint['joint_name']
			rigid_body_1 = joint['rigid_body_1']
			rigid_body_2 = joint['rigid_body_2']
			use_bone_rotation = joint['use_bone_rotation']
			limit_linear_lower = [joint['linear_min_x'],joint['linear_min_y'],joint['linear_min_z']]
			limit_linear_upper = [joint['linear_max_x'],joint['linear_max_y'],joint['linear_max_z']]
			limit_angular_lower = [math.radians(joint['angular_min_x']),math.radians(joint['angular_min_y']),math.radians(joint['angular_min_z'])]
			limit_angular_upper = [math.radians(joint['angular_max_x']),math.radians(joint['angular_max_y']),math.radians(joint['angular_max_z'])]
			spring_linear = [joint['linear_spring_x'],joint['linear_spring_y'],joint['linear_spring_z']]
			spring_angular= [joint['angular_spring_x'],joint['angular_spring_y'],joint['angular_spring_z']]

			create_joint(armature,joint_name,rigid_body_1,rigid_body_2,use_bone_rotation,limit_linear_lower,limit_linear_upper,limit_angular_lower,limit_angular_upper, spring_linear,spring_angular)
			
def is_joint_horizontal(joint_obj):

	if joint_obj.mmd_type == 'JOINT':
		rigid_body1 = joint_obj.rigid_body_constraint.object1
		rigid_body2 = joint_obj.rigid_body_constraint.object2
		bone1 = rigid_body.get_bone_from_rigid_body(rigid_body1)
		bone2 = rigid_body.get_bone_from_rigid_body(rigid_body2)

		if bone1.parent == bone2 or bone2.parent == bone1:
			return False
		else:
			return True


def is_joint_vertical(joint_obj):

	if joint_obj.mmd_type == 'JOINT':
		rigid_body1 = joint_obj.rigid_body_constraint.object1
		rigid_body2 = joint_obj.rigid_body_constraint.object2
		bone1 = rigid_body.get_bone_from_rigid_body(rigid_body1)
		bone2 = rigid_body.get_bone_from_rigid_body(rigid_body2)

		if bone1.parent == bone2 or bone2.parent == bone1:
			return True
		else:
			return False

#returns a list of joints from the rigid body 
def get_joints_from_rigid_body(rigid_body_obj):

	joints_obj = None

	rigid_body_joints = []

	if rigid_body_obj.mmd_type == 'RIGID_BODY': 

		for obj in bpy.context.active_object.parent.parent.children:
			if obj.name.startswith('joints'):
				joints_obj = obj
				break

		if joints_obj:
			for joint in joints_obj.children:
				if joint.rigid_body_constraint.object1.name == rigid_body_obj.name:
					rigid_body_joints.append(joint)
				if joint.rigid_body_constraint.object2.name == rigid_body_obj.name:
					rigid_body_joints.append(joint)

		return rigid_body_joints
	else:
		print('obj',rigid_body_obj.name,'has no joints')




def get_joint_transform_data(joint_obj):
	
	joint_dict = {
	
		'armature':None
		,'joint': None
		,'rigid_body_1': None
		,'rigid_body_2': None
		,'joint_type':None
		,'limit_linear_lower':()
		,'limit_linear_upper':None
		,'limit_angular_lower':None
		,'limit_angular_upper':None
		,'spring_linear':None
		,'spring_angular':None

		}

	properties = [
			#('armature','location','.x'),
			#('joint','location','.x'),
			('rigid_body_1','','rigid_body_constraint.object1',''),
			('rigid_body_2','', 'rigid_body_constraint.object2',''),
			('limit_linear_lower',0,'rigid_body_constraint.limit_lin_','x_lower'),
			('limit_linear_lower',1,'rigid_body_constraint.limit_lin_','y_lower'),
			('limit_linear_lower',2,'rigid_body_constraint.limit_lin_','z_lower'),
			('limit_linear_upper',0,'rigid_body_constraint.limit_lin_','x_upper'),
			('limit_linear_upper',1,'rigid_body_constraint.limit_lin_','y_upper'),
			('limit_linear_upper',2,'rigid_body_constraint.limit_lin_','z_upper'),
			('limit_angular_lower',0,'rigid_body_constraint.limit_ang_','x_lower'),
			('limit_angular_lower',1,'rigid_body_constraint.limit_ang_','y_lower'),
			('limit_angular_lower',2,'rigid_body_constraint.limit_ang_','z_lower'),
			('limit_angular_upper',0,'rigid_body_constraint.limit_ang_','x_upper'),
			('limit_angular_upper',1,'rigid_body_constraint.limit_ang_','y_upper'),
			('limit_angular_upper',2,'rigid_body_constraint.limit_ang_','z_upper'),
			('spring_linear',0,'mmd_joint.spring_linear','[0]'),
			('spring_linear',1,'mmd_joint.spring_linear','[1]'),
			('spring_linear',2,'mmd_joint.spring_linear','[2]'),
			('spring_angular',0,'mmd_joint.spring_angular','[0]'),
			('spring_angular',1,'mmd_joint.spring_angular','[1]'),
			('spring_angular',2,'mmd_joint.spring_angular','[2]'),

			]

	if joint_obj.mmd_type == 'JOINT':
		
		#get the armature
		for obj in joint_obj.parent.parent.children_recursive:
			if obj.type =='ARMATURE':
				armature_obj = obj
				break

		joint_dict['armature']=armature_obj
		joint_dict['joint']=joint_obj
		
		limit_linear_lower = [0 for i in range(3)]
		limit_linear_upper = [0 for i in range(3)]
		limit_angular_lower = [0 for i in range(3)]
		limit_angular_upper = [0 for i in range(3)]
		spring_linear = [0 for i in range(3)]
		spring_angular = [0 for i in range(3)]

		for prop_name,prop_suffix,ext_property,ext_suffix in properties:
			
			if prop_name == 'limit_linear_lower':
				limit_linear_lower[prop_suffix] = get_attribute(joint_obj, ext_property + ext_suffix)
			elif prop_name == 'limit_linear_upper':
				limit_linear_upper[prop_suffix] = get_attribute(joint_obj, ext_property + ext_suffix)
			elif prop_name == 'limit_angular_lower':
				limit_angular_lower[prop_suffix]= get_attribute(joint_obj, ext_property + ext_suffix)
			elif prop_name == 'limit_angular_upper':
				limit_angular_upper[prop_suffix]= get_attribute(joint_obj, ext_property + ext_suffix)
			elif prop_name == 'spring_linear':
				spring_linear[prop_suffix]= get_attribute(joint_obj, ext_property + ext_suffix)
			elif prop_name == 'spring_angular':
				spring_angular[prop_suffix]= get_attribute(joint_obj, ext_property + ext_suffix)
			else:
				joint_dict[prop_name+prop_suffix] = get_attribute(joint_obj, ext_property + ext_suffix)

		joint_dict['limit_linear_lower'] = limit_linear_lower
		joint_dict['limit_linear_upper'] = limit_linear_upper
		joint_dict['limit_angular_lower'] = limit_angular_lower
		joint_dict['limit_angular_upper'] = limit_angular_upper
		joint_dict['spring_linear'] = spring_linear
		joint_dict['spring_angular'] = spring_angular

		if is_joint_vertical(joint_obj)==True:
			joint_dict['joint_type'] = 'VERTICAL'
		else:
			joint_dict['joint_type'] = 'HORIZONTAL'

		return joint_dict


def get_joints_from_selected_rigid_bodies():

	selected_objs = None

	rigid_body_list_unsorted = []
	joints_lists_unsorted = []
	joint_list_sorted = set()

	if bpy.context.selected_objects is not None and len(bpy.context.selected_objects) > 1:
		selected_objs = bpy.context.selected_objects

		#check if all selected objects are rigid bodies
		for obj in selected_objs:
			if obj.mmd_type =='RIGID_BODY':
				rigid_body_list_unsorted.append(obj)

		#get all joints lists from the selected rigid bodies
		if rigid_body_list_unsorted is not None:
			for rigid_body_obj in rigid_body_list_unsorted:
				joints_lists_unsorted.append(get_joints_from_rigid_body(rigid_body_obj))

		#get the joint from each joint list
		if joints_lists_unsorted is not None:
			for joint_list in joints_lists_unsorted:
				for joint in joint_list:
					joint_data = get_joint_transform_data(joint)
					if joint_data['rigid_body_1'] in rigid_body_list_unsorted and joint_data['rigid_body_2'] in rigid_body_list_unsorted:
						joint_list_sorted.add(joint)

		#if there are joints, return the list
		if joint_list_sorted is not None:
			return joint_list_sorted

def select_joints_from_selected_rigid_bodies(append_to_selected=False):

	joints_list = get_joints_from_selected_rigid_bodies()

	if joints_list is not None and len(joints_list)>=1:
		#set the active object to the first joint it sees
		for joint in joints_list:
			if bpy.context.view_layer.objects.active is not None:
				bpy.context.view_layer.objects.active = joint
				break

		if append_to_selected==True:
			if bpy.context.selected_objects is not None:
				for selected_obj in bpy.context.selected_objects:
					#deselect all objects
					if selected_obj.mmd_type != 'JOINT':
						selected_obj.select_set(False)
		else:
			bpy.ops.object.select_all(action='DESELECT')

		for joint in joints_list:
			joint.hide = False
			joint.select_set(True)
	else:
		print('there are no joints to select')
		



def create_rigid_bodies_from_csv(context):
	bpy.context.view_layer.objects.active = get_armature()
	armature = get_armature()

	JOINTS_DICTIONARY = read_joints_file ()
	apply_all_joints(armature, JOINTS_DICTIONARY)


@register_wrap
class AddJointsFromFile(bpy.types.Operator):
	"""Add Joints to a FFXIV Model (Converted to an MMD Model)"""
	bl_idname = "ffxiv_mmd_tools_helper.create_joints_from_csv"
	bl_label = "Replace bones renaming"
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
class SelectJointsFromRigidBodies(bpy.types.Operator):
	"""Get Joints From Selected Rigid Bodies"""
	bl_idname = "ffxiv_mmd_tools_helper.select_joints_from_rigid_bodies"
	bl_label = "Get Joints From Selected Rigid Bodies"


	@classmethod
	def poll(cls, context):
		#obj = context.active_object
		selected_objs = context.selected_objects

		is_all_rigid_bodies_and_joints = True

		if selected_objs is not None:
			if len(selected_objs) > 1:
				for selected_obj in selected_objs:
					if selected_obj.mmd_type not in ['RIGID_BODY','JOINT']:
						is_all_rigid_bodies_and_joints = False		

			else:
				is_all_rigid_bodies_and_joints = False

		return is_all_rigid_bodies_and_joints #obj is not None and obj.mmd_type == 'RIGID_BODY'

	def execute(self, context):
		select_joints_from_selected_rigid_bodies()
		return {'FINISHED'}