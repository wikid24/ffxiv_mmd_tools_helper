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

"""
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
"""
def get_armature(obj):
	
	root = model.findRoot(obj)

	if obj is not None:
		if root is not None:
			return model.find_MMD_Armature(obj)

	else:
		print ('could not find armature for obj:','obj')


def read_joints_file():
	
	JOINTS_DICTIONARY = None
	JOINTS_DICTIONARY = import_csv.use_csv_joints_dictionary()
	#convert the list into a dictionary with a header
	JOINTS_DICTIONARY = [dict(zip(JOINTS_DICTIONARY[0],row)) for row in JOINTS_DICTIONARY[1:]]
	#convert the values in 'use_bone_rotation' into a bool
	for row in JOINTS_DICTIONARY:
		row['use_bone_rotation'] = bool(row['use_bone_rotation'])
	
	return JOINTS_DICTIONARY

def create_joint(armature,joint_name,rigid_body_1,rigid_body_2,use_bone_rotation=None
				,limit_linear_lower=None,limit_linear_upper=None
				,limit_angular_lower=None,limit_angular_upper=None
				, spring_linear=None,spring_angular=None):

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
			use_bone_rotation= use_bone_rotation if use_bone_rotation is not None else None
			,limit_linear_lower= limit_linear_lower if limit_linear_lower is not None else None
			,limit_linear_upper=limit_linear_upper if limit_linear_upper is not None else None
			,limit_angular_lower=limit_angular_lower if limit_angular_lower is not None else None
			,limit_angular_upper=limit_angular_upper if limit_angular_upper is not None else None
			,spring_linear=spring_linear if spring_linear is not None else None
			,spring_angular=spring_angular if spring_angular is not None else None
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
	else:
		return False


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
		,'limit_linear_lower':None
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


def get_rigid_body_from_joint(joint_obj,rigid_number):

	if joint_obj.mmd_type == 'JOINT':
		if rigid_number == '1':
			return joint_obj.rigid_body_constraint.object1
		elif rigid_number == '2':
			return joint_obj.rigid_body_constraint.object2

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

def select_horizontal_joints_from_selected_joints():
	
	selected_objs = None

	if bpy.context.selected_objects is not None:
		selected_objs = bpy.context.selected_objects
		for selected_obj in selected_objs:
			if is_joint_horizontal(selected_obj) == False:
				selected_obj.select_set(False)

def select_vertical_joints_from_selected_joints():
	
	selected_objs = None

	if bpy.context.selected_objects is not None:
		selected_objs = bpy.context.selected_objects
		for selected_obj in selected_objs:
			if is_joint_vertical(selected_obj) == False:
				selected_obj.select_set(False)



def transform_joint(joint_obj
					,rigid_body_1=None,rigid_body_2=None
					,use_bone_rotation=None
					,limit_linear_lower_x=None,limit_linear_lower_y=None,limit_linear_lower_z=None
					,limit_linear_upper_x=None,limit_linear_upper_y=None,limit_linear_upper_z=None
					,limit_angular_lower_x=None,limit_angular_lower_y=None,limit_angular_lower_z=None
					,limit_angular_upper_x=None,limit_angular_upper_y=None,limit_angular_upper_z=None
					,spring_linear_x=None,spring_linear_y=None,spring_linear_z=None
					,spring_angular_x=None,spring_angular_y=None,spring_angular_z=None
					):

			if rigid_body_1 is not None:
				joint_obj.rigid_body_constraint.object1 = rigid_body_1
			if rigid_body_2 is not None:
				joint_obj.rigid_body_constraint.object2 = rigid_body_2
			if use_bone_rotation is not None:
				print('figure out what this does!')
			if limit_linear_lower_x is not None:
				joint_obj.rigid_body_constraint.limit_lin_x_lower = limit_linear_lower_x
			if limit_linear_lower_y is not None:
				joint_obj.rigid_body_constraint.limit_lin_y_lower = limit_linear_lower_y
			if limit_linear_lower_z is not None:
				joint_obj.rigid_body_constraint.limit_lin_z_lower = limit_linear_lower_z
			if limit_linear_upper_x is not None:
				joint_obj.rigid_body_constraint.limit_lin_x_upper = limit_linear_upper_x
			if limit_linear_upper_y is not None:
				joint_obj.rigid_body_constraint.limit_lin_y_upper = limit_linear_upper_y
			if limit_linear_upper_z is not None:
				joint_obj.rigid_body_constraint.limit_lin_z_upper = limit_linear_upper_z
			if limit_angular_lower_x is not None:
				joint_obj.rigid_body_constraint.limit_ang_x_lower = limit_angular_lower_x
			if limit_angular_lower_y is not None:
				joint_obj.rigid_body_constraint.limit_ang_y_lower = limit_angular_lower_y
			if limit_angular_lower_z is not None:
				joint_obj.rigid_body_constraint.limit_ang_z_lower = limit_angular_lower_z
			if limit_angular_upper_x is not None:
				joint_obj.rigid_body_constraint.limit_ang_x_upper = limit_angular_upper_x
			if limit_angular_upper_y is not None:
				joint_obj.rigid_body_constraint.limit_ang_y_upper = limit_angular_upper_y
			if limit_angular_upper_z is not None:
				joint_obj.rigid_body_constraint.limit_ang_z_upper = limit_angular_upper_z
			if spring_linear_x is not None:
				joint_obj.mmd_joint.spring_linear[0] = spring_linear_x
			if spring_linear_y is not None:
				joint_obj.mmd_joint.spring_linear[1] = spring_linear_y
			if spring_linear_z is not None:
				joint_obj.mmd_joint.spring_linear[2] = spring_linear_z
			if spring_angular_x is not None:
				joint_obj.mmd_joint.spring_angular[0] = spring_angular_x
			if spring_angular_y is not None:
				joint_obj.mmd_joint.spring_angular[1] = spring_angular_y
			if spring_angular_z is not None:
				joint_obj.mmd_joint.spring_angular[2] = spring_angular_z
		
	
def create_rigid_bodies_from_csv(context):
	
	obj = context.active_object
	armature = get_armature(obj)
	
	bpy.context.view_layer.objects.active = armature #get_armature()
	

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
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		#obj = context.active_object
		selected_objs = context.selected_objects

		is_all_rigid_bodies_and_joints = True
		is_atleast_one_rigid_body = False

		if selected_objs is not None:
			if len(selected_objs) > 1:
				for selected_obj in selected_objs:
					if selected_obj.mmd_type not in ['RIGID_BODY','JOINT']:
						is_all_rigid_bodies_and_joints = False		
					if selected_obj.mmd_type == 'RIGID_BODY':
						is_atleast_one_rigid_body = True

			else:
				is_all_rigid_bodies_and_joints = False

		return is_all_rigid_bodies_and_joints and is_atleast_one_rigid_body #obj is not None and obj.mmd_type == 'RIGID_BODY'

	def execute(self, context):
		select_joints_from_selected_rigid_bodies(append_to_selected=True)
		return {'FINISHED'}

@register_wrap
class SelectRigidBodyFromJoint(bpy.types.Operator):
	"""Get Rigid Body From Active Joint """
	bl_idname = "ffxiv_mmd_tools_helper.select_rigid_body_from_joint"
	bl_label = "Get Bone From Active Rigid Body "
	bl_options = {'REGISTER', 'UNDO'}

	rigid_number = bpy.props.EnumProperty(items = \
	[('1', '1', '1')\
		,('2','2','2')
	], name = "", default = '1')

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.mmd_type == 'JOINT'

	def execute(self, context):
		obj = context.active_object
		rigid_body = get_rigid_body_from_joint(joint_obj=obj,rigid_number=self.rigid_number)
		rigid_body.hide = False
		rigid_body.select_set(True)
		return {'FINISHED'}

@register_wrap
class SelectVerticalHorizontalJoints(bpy.types.Operator):
	"""Select Vertical or Horizontal Joints from Selected Joints"""
	bl_idname = "ffxiv_mmd_tools_helper.select_vertical_horizontal_joints"
	bl_label = "Select Vertical or Horizontal Joints from Selected Joints"
	bl_options = {'REGISTER', 'UNDO'}

	direction: bpy.props.EnumProperty(items = \
	[('VERTICAL', 'VERTICAL', 'VERTICAL')\
		,('HORIZONTAL', 'HORIZONTAL', 'HORIZONTAL')\
	], name = "", default = None)

	@classmethod
	def poll(cls, context):
		#obj = context.active_object
		selected_objs = context.selected_objects

		is_all_joints = True

		if selected_objs is not None:
			if len(selected_objs) > 0:
				for selected_obj in selected_objs:
					if selected_obj.mmd_type != 'JOINT':
						is_all_joints = False		
			else:
				is_all_joints = False
		else:
			is_all_joints = False

		return is_all_joints #obj is not None and obj.mmd_type == 'RIGID_BODY'

	def execute(self, context):
		if self.direction == 'VERTICAL':
			select_vertical_joints_from_selected_joints()
		elif self.direction == 'HORIZONTAL':
			select_horizontal_joints_from_selected_joints()
		return {'FINISHED'}

@register_wrap
class CreateJoints(bpy.types.Operator):
	"""Create Joints From Selected Rigid Bodies"""
	bl_idname = "ffxiv_mmd_tools_helper.create_joints"
	bl_label = "Create Joints From Selected Rigid Bodies"

	@classmethod
	def poll(cls, context):
		selected_objs = context.selected_objects
		is_selected_all_rigid_bodies = True
		is_in_object_mode = True
		is_at_least_2_rigids = True
		
		if bpy.context.object.mode != 'OBJECT':
			is_in_object_mode = False

		for selected_obj in selected_objs:
			if selected_obj.mmd_type != 'RIGID_BODY':
				is_selected_all_rigid_bodies = False
				break

		if len(selected_objs) < 2:
			is_at_least_2_rigids = False

		

		return is_in_object_mode and is_selected_all_rigid_bodies and is_at_least_2_rigids

	def execute(self, context):
		bpy.ops.mmd_tools.joint_add('INVOKE_DEFAULT')
		return {'FINISHED'}


@register_wrap
class BatchUpdateJoints(bpy.types.Operator):
	""" Bulk Update all Selected Joints using the Active Joint """
	bl_idname = "ffxiv_mmd_tools_helper.batch_update_joints"
	bl_label = "Batch Update Joints"
	bl_options = {'REGISTER','UNDO','PRESET','BLOCKING'} 


	joints = [] #= get_all_rigid_body_chains_from_selected()
	joints_data = [] # = get_all_rigid_body_chains_dictionary(rigid_body_bone_chains)

	number_of_joints = 0
	number_of_vertical_joints = 0
	number_of_horizontal_joints = 0

	#create property,and property_edit 

	props_init = {
		('limit_linear','_lower','bpy.props.FloatProperty(default=0,precision=2)')
		,('limit_linear','_upper','bpy.props.FloatProperty(default=0,precision=2)')
		,('limit_angular','_lower','bpy.props.FloatProperty(default=0,unit=\'ROTATION\')')
		,('limit_angular','_upper','bpy.props.FloatProperty(default=0,unit=\'ROTATION\')')
		,('spring_linear','','bpy.props.FloatProperty(default=0,precision=2)')
		,('spring_angular','','bpy.props.FloatProperty(default=0,precision=2)')
		}
	
	for prop,prop_suffix,prop_type in props_init:
		#create all the properties
		if prop in ('limit_linear','limit_angular','spring_linear','spring_angular'):
			#equivalent to 'writing limit_linear_x_lower_edit = bpy.props.FloatProperty(default=0,precision=2)'
			exec(f'{prop}_x{prop_suffix} = {prop_type}')
			exec(f'{prop}_x{prop_suffix}_edit = bpy.props.BoolProperty(default=False)')
			exec(f'{prop}_y{prop_suffix} = {prop_type}')
			exec(f'{prop}_y{prop_suffix}_edit = bpy.props.BoolProperty(default=False)')
			exec(f'{prop}_z{prop_suffix} = {prop_type}')
			exec(f'{prop}_z{prop_suffix}_edit = bpy.props.BoolProperty(default=False)')
	"""
	#limit_linear_x_lower = bpy.props.FloatProperty(default=0,precision=2)
	#limit_linear_x_lower_edit = bpy.props.BoolProperty(default=False)
	"""


	def invoke(self, context, event):
		
		self.joints = [] #= get_all_rigid_body_chains_from_selected()
		self.joints_data = [] # = get_all_rigid_body_chains_dictionary(rigid_body_bone_chains)
		selected_objs = None

		#get all joints from selected objects
		if context.selected_objects is not None:
			selected_objs = context.selected_objects
			for selected_obj in  selected_objs:
				if selected_obj.mmd_type =='JOINT':
					self.joints.append(selected_obj)
		


		for joint in self.joints:
			#print(joint.name)
			self.joints_data.append( get_joint_transform_data(joint))

		#set the joint counters
		self.number_of_joints = 0
		self.number_of_vertical_joints = 0
		self.number_of_horizontal_joints = 0

		for joint in self.joints_data:
			if joint['joint_type'] == 'VERTICAL':
				self.number_of_vertical_joints += 1
			if joint['joint_type'] == 'HORIZONTAL':
				self.number_of_vertical_joints += 1

		#initialize all properties with the first object in joints_data
		#equivalent to writing 'limit_linear_x_lower = joints_data[0]['limit_linear_x_lower'][0]'
		for prop,prop_suffix,prop_type in self.props_init:
			if prop in ('limit_linear','limit_angular','spring_linear','spring_angular'):
				setattr(self,prop + '_x' + prop_suffix,self.joints_data[0][prop+prop_suffix][0])
				setattr(self,prop + '_x' + prop_suffix+'_edit',False)
				setattr(self,prop + '_y' + prop_suffix,self.joints_data[0][prop+prop_suffix][1])
				setattr(self,prop + '_y' + prop_suffix+'_edit',False)
				setattr(self,prop + '_z' + prop_suffix,self.joints_data[0][prop+prop_suffix][2])
				setattr(self,prop + '_z' + prop_suffix+'_edit',False)




		wm = context.window_manager		
		return wm.invoke_props_dialog(self, width=400)


	def draw(self, context):
		layout = self.layout

		obj = context.active_object 

		#set the joint counters
		self.number_of_joints = 0
		self.number_of_vertical_joints = 0
		self.number_of_horizontal_joints = 0

		self.number_of_joints = len(self.joints_data)

		for joint in self.joints_data:
			if joint['joint_type'] == 'VERTICAL':
				self.number_of_vertical_joints += 1
			if joint['joint_type'] == 'HORIZONTAL':
				self.number_of_horizontal_joints += 1

		
		row = layout.row()
		row.label(text='Selected Joints: '+str(self.number_of_joints))
		row.label(text='Vertical: '+str(self.number_of_vertical_joints))
		row.label(text='Horizontal: '+str(self.number_of_horizontal_joints))
		row = layout.row()
		row.label(text='Checkmark to apply to all selected joints')
		row = layout.row()
		c = row.column(align=True)
		c = row.column(align=True)
		c.alignment = 'RIGHT'
		c.label(text='Limit Linear Lower:')
		c.label(text="")
		c.label(text="")
		c = row.column(align=True)
		c.prop(self,"limit_linear_x_lower",text="X",toggle=False)
		c.prop(self,"limit_linear_y_lower",text="Y",toggle=False)
		c.prop(self,"limit_linear_z_lower",text="Z",toggle=False)
		c = row.column(align=True)
		c.prop(self, "limit_linear_x_lower_edit", text="")
		c.prop(self, "limit_linear_y_lower_edit", text="")
		c.prop(self, "limit_linear_z_lower_edit", text="")	
		row = layout.row()
		c = row.column(align=True)
		c = row.column(align=True)
		c.alignment = 'RIGHT'
		c.label(text='Limit Linear Upper:')
		c.label(text="")
		c.label(text="")
		c = row.column(align=True)
		c.prop(self,"limit_linear_x_upper",text="X",toggle=False)
		c.prop(self,"limit_linear_y_upper",text="Y",toggle=False)
		c.prop(self,"limit_linear_z_upper",text="Z",toggle=False)
		c = row.column(align=True)
		c.prop(self, "limit_linear_x_upper_edit", text="")
		c.prop(self, "limit_linear_y_upper_edit", text="")
		c.prop(self, "limit_linear_z_upper_edit", text="")	
		row = layout.row()
		c = row.column(align=True)
		c = row.column(align=True)
		c.alignment = 'RIGHT'
		c.label(text='Limit Angular Lower:')
		c.label(text="")
		c.label(text="")
		c = row.column(align=True)
		c.prop(self,"limit_angular_x_lower",text="X",toggle=False)
		c.prop(self,"limit_angular_y_lower",text="Y",toggle=False)
		c.prop(self,"limit_angular_z_lower",text="Z",toggle=False)
		c = row.column(align=True)
		c.prop(self, "limit_angular_x_lower_edit", text="")
		c.prop(self, "limit_angular_y_lower_edit", text="")
		c.prop(self, "limit_angular_z_lower_edit", text="")	
		row = layout.row()
		c = row.column(align=True)
		c = row.column(align=True)
		c.alignment = 'RIGHT'
		c.label(text='Limit Angular Upper:')
		c.label(text="")
		c.label(text="")
		c = row.column(align=True)
		c.prop(self,"limit_angular_x_upper",text="X",toggle=False)
		c.prop(self,"limit_angular_y_upper",text="Y",toggle=False)
		c.prop(self,"limit_angular_z_upper",text="Z",toggle=False)
		c = row.column(align=True)
		c.prop(self, "limit_angular_x_upper_edit", text="")
		c.prop(self, "limit_angular_y_upper_edit", text="")
		c.prop(self, "limit_angular_z_upper_edit", text="")	
		row = layout.row()
		c = row.column(align=True)
		c = row.column(align=True)
		c.alignment = 'RIGHT'
		c.label(text='Spring Linear:')
		c.label(text="")
		c.label(text="")
		c = row.column(align=True)
		c.prop(self,"spring_linear_x",text="X",toggle=False)
		c.prop(self,"spring_linear_y",text="Y",toggle=False)
		c.prop(self,"spring_linear_z",text="Z",toggle=False)
		c = row.column(align=True)
		c.prop(self, "spring_linear_x_edit", text="")
		c.prop(self, "spring_linear_y_edit", text="")
		c.prop(self, "spring_linear_z_edit", text="")	
		row = layout.row()
		c = row.column(align=True)
		c = row.column(align=True)
		c.alignment = 'RIGHT'
		c.label(text='Spring Angular:')
		c.label(text="")
		c.label(text="")
		c = row.column(align=True)
		c.prop(self,"spring_angular_x",text="X",toggle=False)
		c.prop(self,"spring_angular_y",text="Y",toggle=False)
		c.prop(self,"spring_angular_z",text="Z",toggle=False)
		c = row.column(align=True)
		c.prop(self, "spring_angular_x_edit", text="")
		c.prop(self, "spring_angular_y_edit", text="")
		c.prop(self, "spring_angular_z_edit", text="")	


	@classmethod
	def poll(cls, context):
		#obj = context.active_object 
		#return obj is not None and obj.mmd_type == 'JOINT'

		selected_objs = context.selected_objects

		is_all_joints = True

		if selected_objs is not None:
			if len(selected_objs) > 0:
				for selected_obj in selected_objs:
					if selected_obj.mmd_type != 'JOINT':
						is_all_joints = False		
			else:
				is_all_joints = False
		else:
			is_all_joints = False

		return is_all_joints

	


	def execute(self, context):

		bpy.ops.object.mode_set(mode='OBJECT')
		
		for joint in self.joints:

			transform_joint(
				joint_obj=joint
				,limit_linear_lower_x = self.limit_linear_x_lower if self.limit_linear_x_lower_edit else None
				,limit_linear_lower_y = self.limit_linear_y_lower if self.limit_linear_y_lower_edit else None
				,limit_linear_lower_z = self.limit_linear_z_lower if self.limit_linear_z_lower_edit else None
				,limit_linear_upper_x = self.limit_linear_x_upper if self.limit_linear_x_upper_edit else None
				,limit_linear_upper_y = self.limit_linear_y_upper if self.limit_linear_y_upper_edit else None
				,limit_linear_upper_z = self.limit_linear_z_upper if self.limit_linear_z_upper_edit else None
				,limit_angular_lower_x = self.limit_angular_x_lower if self.limit_angular_x_lower_edit else None
				,limit_angular_lower_y = self.limit_angular_y_lower if self.limit_angular_y_lower_edit else None
				,limit_angular_lower_z = self.limit_angular_z_lower if self.limit_angular_z_lower_edit else None
				,limit_angular_upper_x = self.limit_angular_x_upper if self.limit_angular_x_upper_edit else None
				,limit_angular_upper_y = self.limit_angular_y_upper if self.limit_angular_y_upper_edit else None
				,limit_angular_upper_z = self.limit_angular_z_upper if self.limit_angular_z_upper_edit else None
				,spring_linear_x = self.spring_linear_x if self.spring_linear_x_edit else None
				,spring_linear_y = self.spring_linear_y if self.spring_linear_y_edit else None
				,spring_linear_z = self.spring_linear_z if self.spring_linear_z_edit else None
				,spring_angular_x = self.spring_angular_x if self.spring_angular_x_edit else None
				,spring_angular_y = self.spring_angular_y if self.spring_angular_y_edit else None
				,spring_angular_z = self.spring_angular_z if self.spring_angular_z_edit else None
				)

		return {'FINISHED'}

def create_vertical_joints(rigid_body_pin_obj = None,use_bone_rotation=None
							,limit_linear_lower=None,limit_linear_upper=None
							,limit_angular_lower=None,limit_angular_upper=None
							,spring_linear=None,spring_angular=None):

		selected_objs = []
		if bpy.context.selected_objects:
			selected_objs = bpy.context.selected_objects

		for obj in selected_objs:
			if obj.mmd_type != 'RIGID_BODY':
				obj.select_set(False)

		#sort the selected rigid bodies into rigid body bone chains
		rigid_body_bone_chains = rigid_body.get_all_rigid_body_chains_from_selected()

		active_obj = bpy.context.active_object
		armature = model.find_MMD_Armature(active_obj)
		#root = model.findRoot(active_obj)

		
		total_joints_count = 0
	

		if rigid_body_bone_chains is not None:

			for i,chain in enumerate(rigid_body_bone_chains):

				chain_joints_count = 0

				#starting with the 1st joint to the 2nd last joint (chain[:-1]), start creating joints
				for j,chain_obj in enumerate(chain[:-1]):

					#chain_obj[2] is the rigid body object
					rigid_body_1 = chain[j][2].name
					rigid_body_2 = chain[j+1][2].name

					joint = create_joint(armature=armature
								,joint_name = 'J.v-'+rigid_body_1+'-'+ rigid_body_2
								,rigid_body_1=rigid_body_1
								,rigid_body_2=rigid_body_2
								,use_bone_rotation=True
								,limit_linear_lower= [0,0,0]#limit_linear_lower
								,limit_linear_upper= [0,0,0]#limit_linear_upper
								,limit_angular_lower= [0,0,0]#limit_angular_lower
								,limit_angular_upper= [0,0,0]#limit_angular_upper
								,spring_linear= [0,0,0]#spring_linear
								,spring_angular=[0,0,0]#spring_angular
								)
					
					if joint:
						chain_joints_count+=1


				#creates the joint to connect the first object to the pin object
				if rigid_body_pin_obj is not None:
					rigid_body_1 = rigid_body_pin_obj.name
					rigid_body_2 = chain[0][2].name

					joint = create_joint(armature=armature
								,joint_name = 'J.v-'+rigid_body_1+'-'+rigid_body_2
								,rigid_body_1=rigid_body_1
								,rigid_body_2=rigid_body_2
								,use_bone_rotation=True
								,limit_linear_lower= [0,0,0]#limit_linear_lower
								,limit_linear_upper= [0,0,0]#limit_linear_upper
								,limit_angular_lower= [0,0,0]#limit_angular_lower
								,limit_angular_upper= [0,0,0]#limit_angular_upper
								,spring_linear= [0,0,0]#spring_linear
								,spring_angular=[0,0,0]#spring_angular
								)
					if joint:
						chain_joints_count+=1
				
				total_joints_count += chain_joints_count
				#total_joints += len(chain)


				incl_pin = ''
				if rigid_body_pin_obj is not None:
					incl_pin = '+ rigid body pin'

				print('chain ',i,' created ',chain_joints_count,' vertical joints ',' for ',str(len(chain)),' rigid bodies in chain',incl_pin)		

		
		#get all the rigid bodies and select all the joints added
		if bpy.context.selected_objects:
			#deselect all objects
			for selected_objs in bpy.context.selected_objects:
						obj.select_set(False)

		#select all the rigid bodies from the rigid body bone chain
		for chain in rigid_body_bone_chains:
			for rigid_body_obj in chain:
				rigid_body_obj[2].select_set(True)

		#also get the rigid body pin object
		if rigid_body_pin_obj is not None:
				if rigid_body_pin_obj.mmd_type == 'RIGID_BODY':
					rigid_body_pin_obj.select_set(True)

		#select all the joints that were just created
		select_joints_from_selected_rigid_bodies(append_to_selected=False)
		select_vertical_joints_from_selected_joints()
		
		print(total_joints_count,' vertical joints created for ',len(rigid_body_bone_chains),' rigid body bone chains')
		
		


@register_wrap
class BatchCreateVerticalJoints(bpy.types.Operator):
	""" Create Vertical Joints from Selected Rigid Bodies"""
	bl_idname = "ffxiv_mmd_tools_helper.batch_create_vertical_joints"
	bl_label = "Create Vertical Joints from Selected Rigid Bodies"
	bl_options = {'REGISTER','UNDO','PRESET'} 
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"

	bpy.types.Scene.vertical_joint_pin = bpy.props.PointerProperty(
		type=bpy.types.Object
		,poll=lambda self, obj: obj.mmd_type == 'RIGID_BODY' and obj not in bpy.context.selected_objects,
		)
	
	def invoke(self, context, event):
		wm = context.window_manager      
		return wm.invoke_props_dialog(self, width=400)

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text='(Optional) Pin the head to a rigid body')
		row.prop(context.scene, "vertical_joint_pin", text="")

	@classmethod
	def poll(cls, context):
		is_all_rigid_bodies = True
		is_at_least_2_rigid_bodies_selected = False
		if context.selected_objects:
			selected_objs = context.selected_objects
			for selected_obj in selected_objs:
				if selected_obj.mmd_type != 'RIGID_BODY':
					is_all_rigid_bodies = False
					break
			if len(selected_objs) >= 2:
				is_at_least_2_rigid_bodies_selected = True

		return is_all_rigid_bodies and is_at_least_2_rigid_bodies_selected #and rigid_body.is_selected_rigid_bodies_in_a_bone_chain()

	def execute(self, context):
		if context.scene.vertical_joint_pin:
			create_vertical_joints(rigid_body_pin_obj=context.scene.vertical_joint_pin)
		else:
			create_vertical_joints()
		return {'FINISHED'}


def create_horizontal_joints( rigid_body_chains
							,wrap_around = None,use_bone_rotation = None
							,limit_linear_lower=None,limit_linear_upper=None
							,limit_angular_lower=None,limit_angular_upper=None
							,spring_linear=None,spring_angular=None):

		active_obj = bpy.context.active_object
		armature = model.find_MMD_Armature(active_obj)
		#root = model.findRoot(active_obj)

		total_joints = 0

		if rigid_body_chains is not None:
			
			for i,chain in enumerate(rigid_body_chains):
				
				chain_joints_count = 0

				#starting with the 1st joint to the 2nd last joint (chain[:-1]), start creating joints
				for j,chain_obj in enumerate(chain[:-1]):

					rigid_body_1 = chain[j][1]
					rigid_body_2 = chain[j+1][1]

					joint = create_joint(armature=armature
								,joint_name = 'J.h-'+rigid_body_1+'-'+ rigid_body_2
								,rigid_body_1=rigid_body_1
								,rigid_body_2=rigid_body_2
								,use_bone_rotation=True
								,limit_linear_lower= [0,0,0]#limit_linear_lower
								,limit_linear_upper= [0,0,0]#limit_linear_upper
								,limit_angular_lower= [0,0,0]#limit_angular_lower
								,limit_angular_upper= [0,0,0]#limit_angular_upper
								,spring_linear= [0,0,0]#spring_linear
								,spring_angular=[0,0,0]#spring_angular
								)
					if joint:
						chain_joints_count+=1

				
				#creates the last joint to connect the first object to teh last object
				if wrap_around == True:
					rigid_body_1 = chain[-1][1]
					rigid_body_2 = chain[0][1]

					joint = create_joint(armature=armature
								,joint_name = 'J.h-'+rigid_body_1+'-'+rigid_body_2
								,rigid_body_1=rigid_body_1
								,rigid_body_2=rigid_body_2
								,use_bone_rotation=True
								,limit_linear_lower= [0,0,0]#limit_linear_lower
								,limit_linear_upper= [0,0,0]#limit_linear_upper
								,limit_angular_lower= [0,0,0]#limit_angular_lower
								,limit_angular_upper= [0,0,0]#limit_angular_upper
								,spring_linear= [0,0,0]#spring_linear
								,spring_angular=[0,0,0]#spring_angular
								)
					if joint:
						chain_joints_count+=1

				total_joints += len(chain)

				#fix this its broken
				print('chain ',i,' created ',chain_joints_count,' horizontal joints ',' for ',len(chain),' rigid bodies in chain')
				

		
		#get all the rigid bodies and select all the joints added
		if bpy.context.selected_objects:
			#deselect all objects
			for selected_objs in bpy.context.selected_objects:
						selected_objs.select_set(False)

		#select all the rigid bodies from the rigid body bone chain
		for chain in rigid_body_chains:
			for rigid_body_obj in chain:
				rigid_body_obj[0].select_set(True)

		

		#select all the joints that were just created
		select_joints_from_selected_rigid_bodies(append_to_selected=False)
		select_horizontal_joints_from_selected_joints()
		
		print(total_joints,' horizontal joints created for ',len(rigid_body_chains),' rigid body chains')
		
		
						





@register_wrap
class BatchCreateHorizontalJoints(bpy.types.Operator):
	""" Create Horizontal Joints from Selected Rigid Bodies"""
	bl_idname = "ffxiv_mmd_tools_helper.batch_create_horizontal_joints"
	bl_label = "Create Horizontal Joints from Selected Rigid Bodies"
	bl_options = {'REGISTER','UNDO','PRESET'} 
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"

	def _update_prop (self,context):
		props = BatchCreateHorizontalJoints
		props.scope_startswith = self.scope_startswith
		props.scope_contains = self.scope_contains
		props.scope_endswith = self.scope_endswith
		props.wrap_around = self.wrap_around
		

	def _update_enum_callback(scene, context):
		props = BatchCreateHorizontalJoints
		item_list = BatchCreateHorizontalJoints.item_list
		return item_list

	def _update_index_pos(self, context):
		props = BatchCreateHorizontalJoints
		props.index_position = int(self.index_position_enum)
		props.grouped_rigid_bodies_by_index_pos = rigid_body.get_grouped_rigid_body_list_by_index_position (props.rigid_body_list_with_number_index,props.index_position)
		
		if props.grouped_rigid_bodies_by_index_pos is not None:
			props.rigid_body_chain_index = 0
			rigid_body.select_rigid_bodies_in_grouped_list(props.grouped_rigid_bodies_by_index_pos,props.rigid_body_chain_index)

	scope_startswith = bpy.props.StringProperty(update=_update_prop)
	scope_contains = bpy.props.StringProperty(update=_update_prop)
	scope_endswith = bpy.props.StringProperty(update=_update_prop)
	message = ''
	search_scope_objects = None
	sample_rigid_body = None
	item_list = None
	index_position_enum = bpy.props.EnumProperty(items = _update_enum_callback,default=None,update=_update_index_pos)
	index_position = None
	rigid_body_list_with_number_index = None
	grouped_rigid_bodies_by_index_pos = None
	rigid_body_chain_index = None
	wrap_around = bpy.props.BoolProperty(default=False,name='Connect Ending Rigid to Starting Rigid',update=_update_prop)
	limit_linear_lower = None
	limit_linear_upper = None
	limit_angular_lower = None 
	limit_angular_upper = None
	spring_linear = None
	spring_angular = None


		
	def invoke(self, context, event):
		props = BatchCreateHorizontalJoints
		props.message = ''
		props.search_scope_objects = None
		props.sample_rigid_body = None
		props.item_list = None
		#props.index_position_enum
		props.index_position = None
		props.rigid_body_list_with_number_index = None
		props.grouped_rigid_bodies_by_index_pos = None
		props.rigid_body_chain_index = None
		props.limit_linear_lower = None
		props.limit_linear_upper = None
		props.limit_angular_lower = None 
		props.limit_angular_upper = None
		props.spring_linear = None
		props.spring_angular = None

		wm = context.window_manager      
		return wm.invoke_props_dialog(self, width=400)

	def draw(self, context):
		props = BatchCreateHorizontalJoints


		layout = self.layout
		row = layout.row()
		row.label(text='*****************************************')
		row = layout.row()
		row.label(text='Input Horizontal Rigid Body Search Scope:')
		row = layout.row()
		col = row.column(align=True)
		grid = col.grid_flow(align=True)
		row = grid.row(align=True)
		row.label(text='Starts w/')
		row.label(text='Contains')
		row.label(text='Ends w/')
		row = grid.row(align=True)
		row.prop(self,"scope_startswith", text = "")
		row.prop(self,"scope_contains", text = "")
		row.prop(self,"scope_endswith", text = "")

		row = grid.row(align=True)
		row.operator("ffxiv_mmd_tools_helper.horizontal_joints_find_rigids", text = 'Find', icon='VIEWZOOM')
		#row.operator("ffxiv_mmd_tools_helper.clear_horizontal_joints_find_rigids", text='',icon='TRASH')
		row = layout.row()
		row.label(text='*****************************************')
		row = layout.row()
		row.label(text=self.message)
		if props.search_scope_objects is not None:
			row = layout.row()
			row.label(text='Sample Rigid Body: '+props.sample_rigid_body[1])
			row.label(text=str(len(props.sample_rigid_body[2])) + ' numbers found: '+ str(props.sample_rigid_body[2]) )
			row = layout.row()
			row.label(text='Specify which value indicates a horizontal rigid body chain: ')
			row = layout.row()
			row.prop(self,'index_position_enum',expand=True)
			row.label (text='index position is: ' + self.index_position_enum)
			if props.grouped_rigid_bodies_by_index_pos is not None:
				row = layout.row()
				col = row.column()
				col.operator("ffxiv_mmd_tools_helper.horizontal_joints_find_rigids_by_index",text='UP').direction = 'UP'
				col.label(text = 'Rigid Body Chain: ' + str(props.rigid_body_chain_index))
				col.label(text = 'Starting Rigid Body: ' + str(props.grouped_rigid_bodies_by_index_pos[props.rigid_body_chain_index][0][1]) )
				col.label(text = 'Ending Rigid Body: ' + str(props.grouped_rigid_bodies_by_index_pos[props.rigid_body_chain_index][-1][1]) )
				col.operator("ffxiv_mmd_tools_helper.horizontal_joints_find_rigids_by_index",text='DOWN').direction = 'DOWN'
				row = layout.row()
				col = row.column()
				row.prop(self,'wrap_around')
				

	@classmethod
	def poll(cls, context):
		return True #is_all_rigid_bodies and is_at_least_2_rigid_bodies_selected #and rigid_body.is_selected_rigid_bodies_in_a_bone_chain()

	def execute(self, context):
		props = BatchCreateHorizontalJoints




		create_horizontal_joints(props.grouped_rigid_bodies_by_index_pos
								,wrap_around=props.wrap_around if props.wrap_around is not None else None
								,limit_linear_lower=None if props.limit_linear_lower is not None else None
								,limit_linear_upper=None if props.limit_linear_upper is not None else None
								,limit_angular_lower=None if props.limit_angular_lower is not None else None
								,limit_angular_upper=None if props.limit_angular_upper is not None else None
								,spring_linear=None if props.spring_linear is not None else None
								,spring_angular=None if props.spring_angular is not None else None
							)


		return {'FINISHED'}



@register_wrap
class HorizontalJointsFindRigidBodies(bpy.types.Operator):
	#Find Rigid Bodies
	bl_idname = "ffxiv_mmd_tools_helper.horizontal_joints_find_rigids"
	bl_label = "Find Rigid Bodies"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		props = BatchCreateHorizontalJoints
		#print(props.scope_startswith)
		results = None
		results = rigid_body.find_rigid_bodies(startswith=props.scope_startswith,endswith=props.scope_endswith,contains=props.scope_contains,append_to_selected=False)
		if results is not None:
			props.message = str(len(results)) + ' Rigid Bodies in search scope'
			props.search_scope_objects = results
			props.rigid_body_list_with_number_index = rigid_body.get_rigid_body_list_with_number_index(props.search_scope_objects)
			props.sample_rigid_body = props.rigid_body_list_with_number_index[-1]	
			print(props.rigid_body_list_with_number_index[-1])
			
			#create the index values for rigid_body_list_with_number_index[-1] (used in the EnumProperty)
			item_list = []
			for i,value in enumerate(props.sample_rigid_body[2]):
				item_list.append((str(i),str(value),'\''+str(value)+'\' in \''+ props.sample_rigid_body[1] + '\' at index pos ' + str(i) ))
			props.item_list = item_list

			props.rigid_body_chain_index = 0
		else:
			props.message = ''
			props.search_scope_objects = None


		return {'FINISHED'}

@register_wrap
class ClearFindRigidBodies(bpy.types.Operator):
	"""Clear Find Horizontal Joint Rigid Bodies """
	bl_idname = "ffxiv_mmd_tools_helper.clear_horizontal_joints_find_rigids"
	bl_label = "Clear Find Horizontal Joint Rigid Bodies"

	def execute(self, context):
		props = BatchCreateHorizontalJoints
		props.scope_startswith = ''
		props.scope_endswith = ''
		props.scope_contains = ''
		return {'FINISHED'}

@register_wrap
class HorizontalJointsFindRigidBodiesByIndexPosition(bpy.types.Operator):
	#Find Rigid Bodies
	bl_idname = "ffxiv_mmd_tools_helper.horizontal_joints_find_rigids_by_index"
	bl_label = "Find Rigid Bodies"
	bl_options = {'REGISTER', 'UNDO'}

	direction = bpy.props.EnumProperty(items = \
	[('UP', 'UP', 'UP')\
		,('DOWN','DOWN','DOWN')
	], name = "", default = 'UP')

	def execute(self, context):
		props = BatchCreateHorizontalJoints
		props.grouped_rigid_bodies_by_index_pos = rigid_body.get_grouped_rigid_body_list_by_index_position (props.rigid_body_list_with_number_index,props.index_position)
		if self.direction == 'UP':
			props.rigid_body_chain_index += 1
			props.rigid_body_chain_index = min(len(props.grouped_rigid_bodies_by_index_pos)-1,props.rigid_body_chain_index)
		if self.direction == 'DOWN':
			props.rigid_body_chain_index -= 1
			props.rigid_body_chain_index = max(0,props.rigid_body_chain_index)

		rigid_body.select_rigid_bodies_in_grouped_list(props.grouped_rigid_bodies_by_index_pos,props.rigid_body_chain_index)

		return {'FINISHED'}