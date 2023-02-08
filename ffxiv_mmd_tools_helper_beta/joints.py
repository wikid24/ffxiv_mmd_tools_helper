import bpy
from . import register_wrap
from . import model
from . import import_csv
import math
from mmd_tools.operators.rigid_body import AddRigidBody

"""
@register_wrap
class JointsPanel(bpy.types.Panel):
	#Joints panel#
	bl_label = "Joints panel"
	bl_idname = "OBJECT_PT_joints_panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.add_joints", text = "Add Joints to Rigid Bodies")
		row = layout.row()
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

def read_joints_file():
	
	JOINTS_DICTIONARY = None
	JOINTS_DICTIONARY = import_csv.use_csv_joints_dictionary()
	#convert the list into a dictionary with a header
	JOINTS_DICTIONARY = [dict(zip(JOINTS_DICTIONARY[0],row)) for row in JOINTS_DICTIONARY[1:]]
	#convert the values in 'use_bone_rotation' into a bool
	for row in JOINTS_DICTIONARY:
		row['use_bone_rotation'] = bool(row['use_bone_rotation'])
	
	return JOINTS_DICTIONARY

def create_joint(armature,rigid_body_1,rigid_body_2,use_bone_rotation,limit_linear_lower,limit_linear_upper,limit_angular_lower,limit_angular_upper, spring_linear,spring_angular):

	#check if joint exists, if it does delete it
	for obj in armature.parent.children_recursive:
		if obj.mmd_type == 'JOINT': 
			if (obj.rigid_body_constraint.object1 is None or obj.rigid_body_constraint.object2 is None ):
				print ('deleting joint with missing rigid body object1 or object2:', obj.name)
				bpy.data.objects.remove(obj, do_unlink=True)
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
		#joint.rotation_euler[0] = 0 #sets x rotation to 0
		bpy.context.view_layer.objects.active = joint
		print ('created joint: ',joint.name)
		
		return joint
	else: 
		print ('could not find either \'', rigid_body_1, '\' or \'',rigid_body_2,'\' to create joint')

def apply_all_joints(armature,joints_data):
	
	if joints_data: 
		for joint in joints_data:
			rigid_body_1 = joint['rigid_body_1']
			rigid_body_2 = joint['rigid_body_2']
			use_bone_rotation = joint['use_bone_rotation']
			limit_linear_lower = [joint['linear_min_x'],joint['linear_min_y'],joint['linear_min_z']]
			limit_linear_upper = [joint['linear_max_x'],joint['linear_max_y'],joint['linear_max_z']]
			limit_angular_lower = [math.radians(joint['angular_min_x']),math.radians(joint['angular_min_y']),math.radians(joint['angular_min_z'])]
			limit_angular_upper = [math.radians(joint['angular_max_x']),math.radians(joint['angular_max_y']),math.radians(joint['angular_max_z'])]
			spring_linear = [joint['linear_spring_x'],joint['linear_spring_y'],joint['linear_spring_z']]
			spring_angular= [joint['angular_spring_x'],joint['angular_spring_y'],joint['angular_spring_z']]

			create_joint(armature,rigid_body_1,rigid_body_2,use_bone_rotation,limit_linear_lower,limit_linear_upper,limit_angular_lower,limit_angular_upper, spring_linear,spring_angular)
			
def main(context):
	bpy.context.view_layer.objects.active = get_armature()
	armature = get_armature()

	JOINTS_DICTIONARY = read_joints_file ()
	apply_all_joints(armature, JOINTS_DICTIONARY)


@register_wrap
class AddJoints(bpy.types.Operator):
	"""Add Joints to a FFXIV Model (Converted to an MMD Model)"""
	bl_idname = "ffxiv_mmd_tools_helper.add_joints"
	bl_label = "Replace bones renaming"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		main(context)
		return {'FINISHED'}