import bpy
import mathutils
from . import register_wrap
from . import model
#from . import import_csv
from mmd_tools.core.bone import FnBone
#import mmd_tools.core.model as mmd_model
from . import miscellaneous_tools
from . import bone_tools
from . import add_foot_leg_ik
from . import add_hand_arm_ik

def correct_root_center():
	print('\ncorrect_root_center():')
	if model.is_mmd_english() == True:
		bpy.ops.object.mode_set(mode='EDIT')

		# if there is no "root" bone in the armature, a root bone is added
		if "root" not in bpy.context.active_object.data.edit_bones.keys():
			root_bone = bpy.context.active_object.data.edit_bones.new('root')
			root_bone.head[:] = (0,0,0)
			root_bone.tail[:] = (0,0,0.7)
			if "center" in bpy.context.active_object.data.edit_bones.keys():
				bpy.context.active_object.data.edit_bones["center"].parent = bpy.context.active_object.data.edit_bones["root"]
				bpy.context.active_object.data.edit_bones["center"].use_connect = False
			print("Added MMD root bone.")
		bpy.ops.object.mode_set(mode='OBJECT')

		# if the "center" bone has a vertex group, it is renamed to "lower body"
		#mesh_objects = model.find_MMD_MeshesList(bpy.context.active_object)
		#if mesh_objects is None:
		#	mesh_objects = model.findMeshesList(bpy.context.active_object)
		#if mesh_objects is not None:
		#	for o in mesh_objects:
		#		if "center" in o.vertex_groups.keys():
		#			if "center" in bpy.context.active_object.data.bones.keys():
		#				bpy.context.active_object.data.bones["center"].name = "lower body"
		#				print("Renamed center bone to lower body bone.")
		#				bpy.ops.object.mode_set(mode='EDIT')
		#				bpy.context.active_object.data.edit_bones["lower body"].tail.z = 0.5 * (bpy.context.active_object.data.edit_bones["leg_L"].head.z + bpy.context.active_object.data.edit_bones["leg_R"].head.z)
		#	bpy.ops.object.mode_set(mode='OBJECT')

		# if there is no "center" bone in the armature, a center bone is added
		if "center" not in bpy.context.active_object.data.bones.keys():
			bpy.ops.object.mode_set(mode='EDIT')
			center_bone = bpy.context.active_object.data.edit_bones.new("center")
			print("Added center bone.")
			center_bone.head = 0.25 * (bpy.context.active_object.data.edit_bones["knee_L"].head + bpy.context.active_object.data.edit_bones["knee_R"].head + bpy.context.active_object.data.edit_bones["leg_L"].head + bpy.context.active_object.data.edit_bones["leg_R"].head)
			center_bone.head.y = 0
			center_bone.tail.z = root_bone.head.z #center_bone.head.z - 0.7
			center_bone.parent = bpy.context.active_object.data.edit_bones["root"]
			if "lower body" in bpy.context.active_object.data.edit_bones.keys():
				bpy.context.active_object.data.edit_bones["lower body"].parent = bpy.context.active_object.data.edit_bones["center"]
			if "upper body" in bpy.context.active_object.data.edit_bones.keys():
				bpy.context.active_object.data.edit_bones["upper body"].parent = bpy.context.active_object.data.edit_bones["center"]
		bpy.ops.object.mode_set(mode='OBJECT')

	else:
		print("Rename bones to MMD_English and then try again.")


def correct_groove():
	print('\ncorrect_groove():')
	bpy.ops.object.mode_set(mode='OBJECT')
	if model.is_mmd_english() == True:
		bpy.ops.object.mode_set(mode='EDIT')

		# if there is no "groove" bone in the armature, a groove bone is added
		if "groove" not in bpy.context.active_object.data.bones.keys():
			bpy.ops.object.mode_set(mode='EDIT')
			groove = bpy.context.active_object.data.edit_bones.new("groove")
			groove.head = bpy.context.active_object.data.edit_bones["center"].head
			groove.head.z = 0.01 + groove.head.z
			groove.tail.z = 0.1 + (groove.head.z)
			groove.parent = bpy.context.active_object.data.edit_bones["center"]
			if "lower body" in bpy.context.active_object.data.edit_bones.keys():
				bpy.context.active_object.data.edit_bones["lower body"].parent = bpy.context.active_object.data.edit_bones["groove"]
			if "upper body" in bpy.context.active_object.data.edit_bones.keys():
				bpy.context.active_object.data.edit_bones["upper body"].parent = bpy.context.active_object.data.edit_bones["groove"]
			print("Added groove bone.")
		bpy.ops.object.mode_set(mode='OBJECT')

	else:
		print("Rename bones to MMD_English and then try again.")

def correct_waist():
	print('\ncorrect_waist():')
	bpy.ops.object.mode_set(mode='OBJECT')
	if model.is_mmd_english() == True:
		bpy.ops.object.mode_set(mode='EDIT')


		# if there is no "waist" bone in the armature, a waist bone is added
		if "waist" not in bpy.context.active_object.data.bones.keys():
			waist = bpy.context.active_object.data.edit_bones.new("waist")
			waist.head = bpy.context.active_object.data.edit_bones["upper body"].head
			waist.tail = waist.head
			waist.tail.z = waist.tail.z - 0.05
			waist.length = bpy.context.active_object.data.edit_bones["upper body"].length * 0.5




		# adjust the waist bone
		bpy.ops.object.mode_set(mode='EDIT')
		waist = bpy.context.active_object.data.edit_bones["waist"]
		waist.name = "waist"
		waist.tail = waist.head
		waist.head.z = waist.tail.z - 0.05
		waist.head.y = waist.tail.y + 0.03
		waist.roll = 0
		waist.parent = bpy.context.active_object.data.edit_bones["groove"]
		if "lower body" in bpy.context.active_object.data.edit_bones.keys():
			bpy.context.active_object.data.edit_bones["lower body"].parent = waist
		if "upper body" in bpy.context.active_object.data.edit_bones.keys():
			bpy.context.active_object.data.edit_bones["upper body"].parent = waist
		print("inverted the waist bone.")
		bpy.ops.object.mode_set(mode='OBJECT')

	else:
		print("Rename bones to MMD_English and then try again.")
		

def correct_waist_cancel():
	print('\ncorrect_waist_cancel():')
	bpy.ops.object.mode_set(mode='EDIT')
	if model.is_mmd_english() == True:
		bpy.ops.object.mode_set(mode='EDIT')
		#measurements of the length of the foot bone which will used to calculate the lengths of the new bones.
		HALF_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones["ankle_L"].length * 0.5

		edit_bones = bpy.context.active_object.data.edit_bones
		armature = bpy.context.active_object

		if "waist_cancel_L" not in bpy.context.active_object.data.bones.keys():
			bone = bone_tools.add_bone(armature,'waist_cancel_L',parent_bone=edit_bones["lower body"],head=edit_bones['leg_L'].head,tail=edit_bones['leg_L'].head)
			bone.tail.z = edit_bones["leg_L"].head.z + HALF_LENGTH_OF_FOOT_BONE

		if "leg_L" in bpy.context.active_object.data.edit_bones.keys():
			edit_bones["leg_L"].parent = edit_bones["waist_cancel_L"]

		if "waist_cancel_R" not in bpy.context.active_object.data.bones.keys():
			bone = bone_tools.add_bone(armature,'waist_cancel_R',parent_bone=edit_bones["lower body"],head=edit_bones['leg_R'].head,tail=edit_bones['leg_R'].head)
			bone.tail.z = edit_bones["leg_L"].head.z + HALF_LENGTH_OF_FOOT_BONE

		if "leg_R" in bpy.context.active_object.data.edit_bones.keys():
			edit_bones["leg_R"].parent = edit_bones["waist_cancel_R"]
	
		#make waist_cancel a control bone for waist
		bpy.ops.object.mode_set(mode='POSE')
		armature = bpy.context.view_layer.objects.active
		bone_tools.apply_MMD_additional_rotation (armature,'waist', 'waist_cancel_L', -1.0)
		bone_tools.apply_MMD_additional_rotation (armature,'waist', 'waist_cancel_R', -1.0)
		#FnBone.apply_additional_transformation(armature)

		bpy.ops.object.mode_set(mode='OBJECT')

	else:
		print("Rename bones to MMD_English and then try again.")


def correct_view_cnt():
	print('\ncorrect_view_cnt():')
	if model.is_mmd_english() == True:
		bpy.ops.object.mode_set(mode='EDIT')

		# if there is no "view_cnt" bone in the armature, a root bone is added
		if "view cnt" not in bpy.context.active_object.data.edit_bones.keys():
			view_cnt = bpy.context.active_object.data.edit_bones.new('view cnt')
			view_cnt.head[:] = (0,0,0)
			view_cnt.tail[:] = (0,0,0.08)
			print("Added MMD 'view cnt' bone.")
		bpy.ops.object.mode_set(mode='OBJECT')

	else:
		print("Rename bones to MMD_English and then try again.")


def add_extra_finger_bones(armature,hand_mesh): 
	print('\nadd_extra_finger_bones(armature,hand_mesh):')
	if model.is_mmd_english() == True:
		bpy.ops.object.mode_set(mode='EDIT')

		correct_finger(armature,hand_mesh,'fore2_L','fore3_L')
		correct_finger(armature,hand_mesh,'little2_L','little3_L')
		correct_finger(armature,hand_mesh,'third2_L','third3_L')
		correct_finger(armature,hand_mesh,'middle2_L','middle3_L')
		correct_finger(armature,hand_mesh,'fore2_R','fore3_R')
		correct_finger(armature,hand_mesh,'little2_R','little3_R')
		correct_finger(armature,hand_mesh,'third2_R','third3_R')
		correct_finger(armature,hand_mesh,'middle2_R','middle3_R')
		print('added third finger bones')

		bpy.ops.object.mode_set(mode='OBJECT')
	
	else:
		print("Rename bones to MMD_English and then try again.")

			

def correct_finger(armature, hand_mesh,source_bone_name,new_bone_name):

	if new_bone_name not in armature.data.bones.keys():

		# set the armature to Edit Mode
		bpy.context.view_layer.objects.active = armature
		bpy.ops.object.mode_set(mode='EDIT')

		# select the bone
		bpy.ops.armature.select_all(action='DESELECT')
		armature.data.edit_bones[source_bone_name].select = True

		# get the head and tail positions of the old bone
		source_bone_head = armature.data.bones[source_bone_name].head
		source_bone_tail = armature.data.bones[source_bone_name].tail

		# get the midpoint of the old bone
		midpoint = (source_bone_head + source_bone_tail) / 2

		# subdivide the bone into two separate bones
		bpy.ops.armature.subdivide()

		# set the armature to Object Mode
		bpy.ops.object.mode_set(mode='OBJECT')

		# rename the new bone
		armature.data.bones[source_bone_name + ".001"].name = new_bone_name

		#armature.select_set(True)
		#hand_mesh.select_set(True)
		#bpy.context.view_layer.objects.active = armature
		
		

		####AUTOMATIC WEIGHT PAINTING METHOD####
		# Deselect all objects
		bpy.ops.object.select_all(action='DESELECT')

		for o in bpy.context.view_layer.objects:
			o.select_set(False)

		bpy.data.objects[armature.name].select_set(True)
		bpy.data.objects[hand_mesh.name].select_set(True)
		bpy.context.view_layer.objects.active = bpy.data.objects[hand_mesh.name]
		bpy.ops.object.mode_set(mode='WEIGHT_PAINT')

		#deselect all bones
		for b in bpy.data.armatures[armature.name].bones:
			b.select = False

		bpy.data.armatures[armature.name].bones[source_bone_name].select=True
		bpy.data.armatures[armature.name].bones[new_bone_name].select=True

		bpy.ops.paint.weight_from_bones(type='AUTOMATIC')
		
		

		"""
		### Manual Method###
		# get the vertex group
		mesh_vertex_groups = hand_mesh.vertex_groups[source_bone_name]

		# iterate over the vertices of the mesh
		for vertex in hand_mesh.data.vertices:
			# iterate over the vertex groups of the vertex
			for group in vertex.groups:
				if group.group == mesh_vertex_groups.index:
					# calculate the distance between the vertex and the midpoint of the old bone
					vertex_location = hand_mesh.matrix_world @ vertex.co
					dist = (vertex_location - midpoint).length

					# if the distance is less than half of the distance between the bones, transfer the weight to the new bone
					if dist < (source_bone_tail - source_bone_head).length / 2:
						group.weight = 1.0

		# create a new vertex group for the new bone
		new_vertex_group = hand_mesh.vertex_groups.new(name=new_bone_name)

		# assign the new vertex group to the new bone
		for vertex in hand_mesh.data.vertices:
			for group in vertex.groups:
				if group.group == mesh_vertex_groups.index and group.weight == 1.0:
					new_vertex_group.add([vertex.index], group.weight, 'REPLACE')

		# remove the weight from the original vertex group
		for vertex in hand_mesh.data.vertices:
			for group in vertex.groups:
				if group.group == mesh_vertex_groups.index and group.weight == 0.0:
					hand_mesh.vertex_groups.remove(mesh_vertex_groups)
		"""


		


def fix_bone_length(armature,source_bone_name,target_bone_name):
	source_bone = armature.data.edit_bones[source_bone_name]
	target_bone = armature.data.edit_bones[target_bone_name]
	source_bone.tail = target_bone.head

	#source_bone.tail = target_bone.head
	#source_bone.roll = source_bone_roll

	# Deselect all bones in edit mode
	#bpy.ops.armature.select_all(action='DESELECT')
	
	#bpy.context.object.data.edit_bones.active = source_bone
	#source_bone.data.select = True

	#recalculate bone roll
	#bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Y')
	#bpy.context.active_object.data.bones.active = bpy.data.armatures[armature.name].bones[source_bone.name]

def correct_bones_length():
	print('\ncorrect_bones_length():')
	if model.is_mmd_english() == True:
		bpy.ops.object.mode_set(mode='EDIT')

		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		fix_bone_length(armature,'shoulder_L','arm_L')
		fix_bone_length(armature,'shoulder_R','arm_R')
		fix_bone_length(armature,'arm_L','elbow_L')
		fix_bone_length(armature,'arm_R','elbow_R')
		fix_bone_length(armature,'elbow_L','wrist_L')
		fix_bone_length(armature,'elbow_R','wrist_R')
		print('reset bone length for shoulder/arm/elbow')

		bpy.ops.object.mode_set(mode='OBJECT')
	else:
		print("Rename bones to MMD_English and then try again.")

def add_breast_tip_bones(armature):
	print('\nadd_breast_tip_bones(armature):')
	armature = bpy.context.view_layer.objects.active
	bpy.ops.object.mode_set(mode='EDIT')

	breast = armature.data.edit_bones['j_mune_l']
	if (breast.name + "_tip") not in bpy.context.active_object.data.edit_bones.keys():
		bone = bone_tools.add_bone(armature,breast.name + "_tip",parent_bone=breast,head=breast.head,tail=breast.tail,length=breast.length*1.25)
		bone.head = breast.tail
		bone.roll = breast.roll

	breast = armature.data.edit_bones['j_mune_r']
	if (breast.name + "_tip") not in bpy.context.active_object.data.edit_bones.keys():
		bone = bone_tools.add_bone(armature,breast.name + "_tip",parent_bone=breast,head=breast.head,tail=breast.tail,length=breast.length*1.25)
		bone.head = breast.tail
		bone.roll = breast.roll

	bpy.ops.object.mode_set(mode='OBJECT')

def add_eye_control_bone():
	print('\nadd_eye_control_bone():')
	if model.is_mmd_english() == True:
		armature = bpy.context.view_layer.objects.active
		bpy.ops.object.mode_set(mode='EDIT')

		eye_L_bone = armature.data.edit_bones.get("eye_L")
		eye_R_bone = armature.data.edit_bones.get("eye_R")
		head_bone = armature.data.edit_bones.get("head")
		
		eyes_bone = None
		if armature.data.edit_bones.get("eyes") is None:
			eyes_bone = armature.data.edit_bones.new("eyes")
			eyes_bone.head = 0.5 * (eye_L_bone.head + eye_R_bone.head)
			#eyes_bone.head.z = eyes_bone.head.z + (2 * (eye_L_bone.length + eye_R_bone.length))
			eyes_bone.head.y = eye_L_bone.head.y
			eyes_bone.length = eye_L_bone.length
			eyes_bone.tail.y = eyes_bone.head.y - eye_L_bone.length
			eyes_bone.tail.z = eyes_bone.head.z
			eyes_bone.parent = head_bone
			
			#flip the orientation of the bone
			#eye_controller_bone_head = eyes_bone.head.copy()
			#eye_controller_bone_tail = eyes_bone.tail.copy()
			#eyes_bone.head = eye_controller_bone_tail
			#eyes_bone.tail = eye_controller_bone_head

			print ('added eyes control bone' )
				
		else:
			eyes_bone = armature.data.edit_bones.get("eyes")
		
		bone_tools.apply_MMD_additional_rotation(armature,'eyes','eye_L',1)
		bone_tools.apply_MMD_additional_rotation(armature,'eyes','eye_R',1)	

		bpy.ops.object.mode_set(mode='POSE')
		#set bones as tip bones
		armature.pose.bones['eyes'].mmd_bone.is_tip = True


		bpy.ops.object.mode_set(mode='OBJECT')

	else:
		print("Rename bones to MMD_English and then try again.")
	

def create_twist_support_bones(armature,source_bone_name,bone_1_name,bone_2_name,bone_3_name,additional_rotation_bone_name):
	if armature:
		# Get the armature in edit mode
		bpy.ops.object.mode_set(mode='EDIT')
		# Get the source bone
		source_bone = armature.data.edit_bones.get(source_bone_name)
		if source_bone:
			# Get the length of the arm_L bone
			length = source_bone.length
			# Get the start and end points of the arm_L bone
			start = source_bone.head
			end = source_bone.tail
			# Calculate the positions of the three new bones
			pos1 = start + (end - start) * 0.25
			pos2 = start + (end - start) * 0.5
			pos3 = start + (end - start) * 0.75
			# Add the three new bones
			_bone_1 = bone_tools.add_bone(armature, bone_1_name,parent_bone=source_bone,length= length * 0.30,head= pos1,tail= pos1 + mathutils.Vector((0, 0, length * 0.1)))
			_bone_2 = bone_tools.add_bone(armature, bone_2_name,parent_bone=source_bone,length= length * 0.30,head= pos2,tail= pos2 + mathutils.Vector((0, 0, length * 0.1)))
			_bone_3 = bone_tools.add_bone(armature, bone_3_name,parent_bone=source_bone,length= length * 0.30,head= pos3,tail= pos3 + mathutils.Vector((0, 0, length * 0.1)))



			
			bpy.ops.object.mode_set(mode='POSE')
			#set bones as tip bones
			armature.pose.bones[bone_1_name].mmd_bone.is_tip = True
			armature.pose.bones[bone_2_name].mmd_bone.is_tip = True
			armature.pose.bones[bone_3_name].mmd_bone.is_tip = True

			#apply additional rotation
			bone_tools.apply_MMD_additional_rotation(armature,additional_rotation_bone_name,bone_1_name, 0.25)
			bone_tools.apply_MMD_additional_rotation(armature,additional_rotation_bone_name,bone_2_name, 0.50)
			bone_tools.apply_MMD_additional_rotation(armature,additional_rotation_bone_name,bone_3_name, 0.75)


			
			# Return to object mode
			bpy.ops.object.mode_set(mode='OBJECT')
	else:
		print("Armature object not found")

def add_arm_wrist_twist():
	print('\nadd_arm_wrist_twist():')
	if model.is_mmd_english() == True:
	
		bpy.ops.object.mode_set(mode='EDIT')
		# set the armature to Edit Mode
		armature = bpy.context.view_layer.objects.active
		
		#parent the elbow bone to the arm twist
		arm_twist_L = armature.data.edit_bones["arm_twist_L"]
		arm_twist_R = armature.data.edit_bones["arm_twist_R"]
		elbow_L = armature.data.edit_bones["elbow_L"]
		elbow_R = armature.data.edit_bones["elbow_R"]
		elbow_L.parent = arm_twist_L
		elbow_R.parent = arm_twist_R

		#parent the wrist bone to the wrist twist
		wrist_twist_L = armature.data.edit_bones["wrist_twist_L"]
		wrist_twist_R = armature.data.edit_bones["wrist_twist_R"]
		wrist_L = armature.data.edit_bones["wrist_L"]
		wrist_R = armature.data.edit_bones["wrist_R"]
		wrist_L.parent = wrist_twist_L
		wrist_R.parent = wrist_twist_R
		
		armature.pose.bones.get(arm_twist_L.name).lock_rotation = [True,False,True]
		armature.pose.bones.get(arm_twist_R.name).lock_rotation = [True,False,True]
		armature.pose.bones.get(wrist_twist_L.name).lock_rotation = [True,False,True]
		armature.pose.bones.get(wrist_twist_R.name).lock_rotation = [True,False,True]

		create_twist_support_bones(armature,'arm_L','arm_twist_1_L','arm_twist_2_L','arm_twist_3_L','arm_twist_L')
		create_twist_support_bones(armature,'arm_R','arm_twist_1_R','arm_twist_2_R','arm_twist_3_R','arm_twist_R')
		create_twist_support_bones(armature,'elbow_L','wrist_twist_1_L','wrist_twist_2_L','wrist_twist_3_L','wrist_twist_L')
		create_twist_support_bones(armature,'elbow_R','wrist_twist_1_R','wrist_twist_2_R','wrist_twist_3_R','wrist_twist_R')

		#used to move the wrist_twist to elbow's tail
		offset_bone_by_parents_tail('elbow_L','wrist_twist_L', 0.33)
		offset_bone_by_parents_tail('elbow_R','wrist_twist_R', 0.33)

		bpy.ops.object.mode_set(mode='OBJECT')


	else:
		print("Rename bones to MMD_English and then try again.")


def offset_bone_by_parents_tail(parent,child,percentage_of_parent):
    
    bpy.ops.object.mode_set(mode='EDIT')


    parent = bpy.context.active_object.data.edit_bones[parent]
    child = bpy.context.active_object.data.edit_bones[child]

    child.head = parent.head
    child.tail = parent.tail    
    child.length = (parent.length * percentage_of_parent)
    child.head = child.tail
    child.tail = parent.tail
    
def set_bone_to_target_bone_axis(source_bone_name,target_bone_name,target_bone_head_or_tail,axis):
	
	bpy.ops.object.mode_set(mode='EDIT')

	source_bone = bpy.context.active_object.data.edit_bones[source_bone_name]
	target_bone = bpy.context.active_object.data.edit_bones[target_bone_name]
	
	if axis == 'x':  
		if target_bone_head_or_tail == 'head':
			target_bone.head.x = source_bone.head.x
			target_bone.tail.x = source_bone.head.x
		if target_bone_head_or_tail == 'tail':
			target_bone.head.x = source_bone.tail.x
			target_bone.tail.x = source_bone.tail.x

	if axis == 'y':  
		if target_bone_head_or_tail == 'head':
			target_bone.head.y = source_bone.head.y
			target_bone.tail.y = source_bone.head.y
		if target_bone_head_or_tail == 'tail':
			target_bone.head.y = source_bone.tail.y
			target_bone.tail.y = source_bone.tail.y

	if axis == 'z':  
		if target_bone_head_or_tail == 'head':
			target_bone.head.z = source_bone.head.z
			target_bone.tail.z = source_bone.head.z
		if target_bone_head_or_tail == 'tail':
			target_bone.head.z = source_bone.tail.z
			target_bone.tail.z = source_bone.tail.z

		
def offset_bone_by_source_bone(source_bone_name,target_bone_name,head_or_tail,axis,percentage_of_source):
	
	bpy.ops.object.mode_set(mode='EDIT')

	source_bone = bpy.context.active_object.data.edit_bones[source_bone_name]
	target_bone = bpy.context.active_object.data.edit_bones[target_bone_name]
	
	if head_or_tail == 'head':
		if axis == 'x':
			offset = (source_bone.length) * (1 - percentage_of_source)        
			target_bone.head.x = source_bone.tail.x - offset
			
		elif axis == 'y':
			offset = (source_bone.length) * (1 - percentage_of_source)
			target_bone.head.y = source_bone.tail.y - offset
		elif axis == 'z':
			offset = (source_bone.length) * (1 - percentage_of_source)
			target_bone.head.z = source_bone.tail.z - offset

	if head_or_tail == 'tail':
		if axis == 'x':
			offset = (source_bone.length) * (1 - percentage_of_source)        
			target_bone.tail.x = source_bone.tail.x - offset
			
		elif axis == 'y':
			offset = (source_bone.length) * (1 - percentage_of_source)
			target_bone.tail.y = source_bone.tail.y - offset
		elif axis == 'z':
			offset = (source_bone.length) * (1 - percentage_of_source)
			target_bone.tail.z = source_bone.tail.z - offset


def add_shoulder_control_bones():
	print('\nadd_shoulder_control_bones():')
	if model.is_mmd_english() == True:

		bpy.ops.object.mode_set(mode='EDIT')
		# set the armature to Edit Mode
		armature = bpy.context.view_layer.objects.active

		#get the bones
		shoulder_L = armature.data.edit_bones["shoulder_L"]
		shoulder_R = armature.data.edit_bones["shoulder_R"]
		arm_L = armature.data.edit_bones["arm_L"]
		arm_R = armature.data.edit_bones["arm_R"]
		j_sebo_c = armature.data.edit_bones["j_sebo_c"]

		#create new bones
		shoulder_P_L = bone_tools.add_bone(armature, 'shoulder_P_L',parent_bone=j_sebo_c,length=shoulder_L.length,head=shoulder_L.head ,tail=shoulder_L.head)
		shoulder_P_R = bone_tools.add_bone(armature, 'shoulder_P_R',parent_bone=j_sebo_c,length=shoulder_R.length,head=shoulder_R.head ,tail=shoulder_R.head)
		shoulder_C_L = bone_tools.add_bone(armature, 'shoulder_C_L',parent_bone=shoulder_L,length=shoulder_L.length,head=shoulder_L.tail ,tail=shoulder_L.tail)
		shoulder_C_R = bone_tools.add_bone(armature, 'shoulder_C_R',parent_bone=shoulder_R,length=shoulder_R.length,head=shoulder_R.tail ,tail=shoulder_R.tail)

		#set the new bone's positions vertical
		shoulder_P_L.tail.z = shoulder_P_L.tail.z - (shoulder_P_L.length * 0.25)
		shoulder_P_R.tail.z = shoulder_P_R.tail.z - (shoulder_P_R.length * 0.25)
		shoulder_C_L.tail.z = shoulder_C_L.tail.z - (shoulder_C_L.length * 0.25)
		shoulder_C_R.tail.z = shoulder_C_R.tail.z - (shoulder_C_R.length * 0.25)

		#make shoulder_C bones the parent of the arm bones
		arm_L.parent = shoulder_C_L
		arm_R.parent = shoulder_C_R
		shoulder_L.parent = shoulder_P_L
		shoulder_R.parent = shoulder_P_R

		#make shoulder_C a control bone for shoulder_P
		
		bpy.ops.object.mode_set(mode='POSE')
				
		# Select all bones in the armature
		for bone in armature.pose.bones:
			bone.bone.select = True

		#set bones as tip bones
		armature.pose.bones['shoulder_P_L'].mmd_bone.is_tip = True
		armature.pose.bones['shoulder_C_L'].mmd_bone.is_tip = True
		armature.pose.bones['shoulder_P_R'].mmd_bone.is_tip = True
		armature.pose.bones['shoulder_C_R'].mmd_bone.is_tip = True
		
		
		bone_tools.apply_MMD_additional_rotation (armature,'shoulder_P_L', 'shoulder_C_L', -1.0)
		bone_tools.apply_MMD_additional_rotation (armature,'shoulder_P_R', 'shoulder_C_R', -1.0)
		#FnBone.apply_additional_transformation(armature)

		bpy.ops.object.mode_set(mode='OBJECT')
	
	else:
		print("Rename bones to MMD_English and then try again.")


def merge_double_jointed_knee(armature, context):
	print('\n')
	
	if model.is_mmd_english() == True:

		bpy.ops.object.mode_set(mode='POSE')

		#get the bones
		knee_L = bpy.context.active_object.pose.bones['knee_L']
		knee_R = bpy.context.active_object.pose.bones['knee_R']
		j_asi_c_l = bpy.context.active_object.pose.bones['j_asi_c_l']
		j_asi_c_r = bpy.context.active_object.pose.bones['j_asi_c_r']

		for pbone in armature.pose.bones:
			pbone.bone.select = False

		knee_L.bone.select = True
		j_asi_c_l.bone.select = True

		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		parent_bone_name, child_bone_name = miscellaneous_tools.analyze_selected_parent_child_bone_pair()
		if parent_bone_name is not None:
			if child_bone_name is not None:
				miscellaneous_tools.combine_2_vg_1_vg(parent_bone_name, child_bone_name)
				miscellaneous_tools.combine_2_bones_1_bone(parent_bone_name, child_bone_name)

		bpy.ops.object.mode_set(mode='POSE')

		for pbone in armature.pose.bones:
			pbone.bone.select = False

		knee_R.bone.select = True
		j_asi_c_r.bone.select = True

		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		parent_bone_name, child_bone_name = miscellaneous_tools.analyze_selected_parent_child_bone_pair()
		if parent_bone_name is not None:
			if child_bone_name is not None:
				miscellaneous_tools.combine_2_vg_1_vg(parent_bone_name, child_bone_name)
				miscellaneous_tools.combine_2_bones_1_bone(parent_bone_name, child_bone_name)

		#if there is foot/leg IK added already, re-run it
		if 'leg IK_L' in  armature.data.edit_bones.keys() or 'leg IK_L' in  armature.data.bones.keys():
			print("hello!")
			armature = bpy.context.view_layer.objects.active
			bpy.ops.object.mode_set(mode='OBJECT')
			add_foot_leg_ik.clear_IK(context)
			add_foot_leg_ik.main(context)
			bpy.ops.object.mode_set(mode='OBJECT')

	
	else:
		print("Rename bones to MMD_English and then try again.")

def set_bust_size(bust_scale=None,bust_xyz=None):
	print('\n')
	armature = model.findArmature(bpy.context.active_object)

	if armature is not None:
		bpy.context.view_layer.objects.active = armature

		bpy.ops.object.mode_set(mode='POSE')
		bust_L = armature.pose.bones.get('j_mune_l')
		bust_R = armature.pose.bones.get('j_mune_r')
		bust_core = armature.pose.bones.get('j_mune_core')

		scale_x = 1
		scale_y = 1
		scale_z = 1
			
		if (bust_L is not None and bust_R is not None) or (bust_core is not None):

			if bust_xyz is not None:
				scale_x = bust_xyz[0]
				scale_y = bust_xyz[1]
				scale_z = bust_xyz[2]

			elif bust_scale is not None:
				scale_x = 0.92 + (bust_scale * 0.16)
				scale_y = 0.816 + (bust_scale * 0.368)
				scale_z = 0.8 + (bust_scale * 0.4)

				#x @ 1 = 0.922
				#y @ 1 = 0.804
				#z @ 1 = 0.82


				#x @ 100 = 1.08
				#y @ 100 = 1.2
				#z @ 100 = 1.184

			if bust_L and bust_R:
				bust_L.scale= (scale_z,scale_y,scale_x)
				bust_R.scale= (scale_z,scale_y,scale_x)

				#insert a keyframe at frame 0 to set the bust size
				bust_L.keyframe_insert(data_path='scale', frame=0)
				bust_R.keyframe_insert(data_path='scale', frame=0)

			if bust_core:
				bust_core.scale = (scale_x,scale_y,scale_z)
				#insert a keyframe at frame 0 to set the bust size
				bust_core.keyframe_insert(data_path='scale', frame=0)

			

def convert_ffxiv_boobs_to_genshin_boobs(context,armature):

	bpy.ops.object.mode_set(mode='EDIT')

	j_mune_l = armature.data.edit_bones.get('j_mune_l')
	j_mune_r = armature.data.edit_bones.get('j_mune_r')

	boob_core = None

	if armature.data.edit_bones.get('j_mune_core') == None:
		boob_core = armature.data.edit_bones.new('j_mune_core')
	else:
		boob_core = armature.data.edit_bones.get('j_mune_core')
	
	if boob_core:
		boob_core.head = (j_mune_l.head + j_mune_r.head) / 2
		boob_core.head.y -= (j_mune_l.length/2)
		boob_core.length = 0
		boob_core.length = j_mune_l.length
		#upper_body_2_name = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'upper body 3')
		j_sebo_c = armature.data.edit_bones.get('j_sebo_c')
		boob_core.parent = j_sebo_c

	bone_list = [j_mune_l,j_mune_r]

	for bone in bone_list:

		top_boob = None
		bot_boob = None

		if armature.data.edit_bones.get(bone.name + '_top') == None:
			top_boob = armature.data.edit_bones.new(bone.name + '_top')
		else:
			armature.data.edit_bones.get(bone.name + '_top')

		if top_boob:
			top_boob.matrix = bone.matrix
			top_boob.tail = bone.tail
			#top_boob.length = j_mune_l.length
			top_boob.head.z += (top_boob.length /2)
			top_boob.tail.z += (top_boob.length /2)
			#top_boob.head.y -= (top_boob.length /2)
			top_boob.parent = boob_core
		
		
		if armature.data.edit_bones.get(bone.name + '_bot') == None:
			bot_boob = armature.data.edit_bones.new(bone.name + '_bot')
		else:
			bot_boob = armature.data.edit_bones.get(bone.name + '_bot')

		if bot_boob:
			bot_boob.matrix = bone.matrix
			bot_boob.tail = bone.tail
			#bot_boob.length = j_mune_r.length
			bot_boob.head.z -= (bot_boob.length /2)
			bot_boob.tail.z -= (bot_boob.length /2)
			#bot_boob.head.y -= (bot_boob.length /2)
			bot_boob.parent = boob_core

		#bot_boob_tip = armature.data.edit_bones.new(bot_boob.name + '_tip')
		#bot_boob_tip.parent = bot_boob
		#bot_boob_tip.head = bot_boob.tail
		#bot_boob_tip.length = 0
		#bot_boob_tip.length = bot_boob.length

		bone.name = bone.name+'_mid'
		bone.head = top_boob.tail
		bone.tail = bot_boob.tail
		bone.parent = top_boob
		

		#bone_tip = armature.data.edit_bones.new(bone.name + '_tip')
		#bone_tip.parent = bone
		#bone_tip.head = bone.tail
		#bone_tip.length = 0 
		#bone_tip.length = (bone.length) *0.66



		



def main(context):


	selected_bone_tool = bpy.context.scene.selected_bone_tool
	if selected_bone_tool == "delete_unused_bones":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		miscellaneous_tools.flag_unused_bones()
		miscellaneous_tools.delete_unused_bones()
	if selected_bone_tool == "correct_root_center":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		correct_root_center()
	if selected_bone_tool == "correct_groove":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		correct_groove()
	if selected_bone_tool == "correct_waist":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		correct_waist()
	if selected_bone_tool == "correct_waist_cancel":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		correct_waist_cancel()
	if selected_bone_tool == "correct_view_cnt":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		correct_view_cnt()
	if selected_bone_tool == "correct_bones_lengths":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		correct_bones_length()
	if selected_bone_tool == "add_eye_control_bone":
		armature = bpy.context.view_layer.objects.active
		add_eye_control_bone()
	if selected_bone_tool == "add_arm_wrist_twist":
		armature = bpy.context.view_layer.objects.active
		add_arm_wrist_twist()
	if selected_bone_tool == "add_shoulder_control_bones":
		armature = bpy.context.view_layer.objects.active
		add_shoulder_control_bones()
	if selected_bone_tool == "add_leg_foot_ik":
		armature = bpy.context.view_layer.objects.active
		bpy.ops.object.mode_set(mode='OBJECT')
		add_foot_leg_ik.clear_IK(context)
		add_foot_leg_ik.main(context)
		bpy.ops.object.mode_set(mode='OBJECT')
	if selected_bone_tool == "auto_fix_mmd_bone_names":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		bone_tools.auto_fix_mmd_bone_names(armature)
		bpy.ops.object.mode_set(mode='OBJECT')
	if selected_bone_tool == "add_hand_arm_ik":
		armature = bpy.context.view_layer.objects.active
		bpy.ops.object.mode_set(mode='OBJECT')
		add_hand_arm_ik.clear_IK(context)
		add_hand_arm_ik.main(context)
		bpy.ops.object.mode_set(mode='OBJECT')


	if selected_bone_tool == "add_extra_finger_bones":
		mesh = bpy.context.view_layer.objects.active
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		add_extra_finger_bones(armature,mesh)
	if selected_bone_tool == "add_breast_tip_bones":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		add_breast_tip_bones(armature)
	if selected_bone_tool == "merge_double_jointed_knee":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		merge_double_jointed_knee(armature,context)
	if selected_bone_tool == "run_1_to_12":
		#delete unused bones
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		miscellaneous_tools.flag_unused_bones()
		miscellaneous_tools.delete_unused_bones()
		correct_root_center()
		correct_groove()
		correct_waist()
		correct_waist_cancel()
		correct_view_cnt()
		correct_bones_length()
		add_eye_control_bone()
		add_arm_wrist_twist()
		add_shoulder_control_bones()
		#leg_IK
		bpy.ops.object.mode_set(mode='OBJECT')
		add_foot_leg_ik.clear_IK(context)
		add_foot_leg_ik.main(context)
		#auto_fix bone names
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		bone_tools.auto_fix_mmd_bone_names(armature)
		bpy.ops.object.mode_set(mode='OBJECT')
	if selected_bone_tool == 'adjust_arm_position':
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.context.object.data.use_mirror_x = True

		offset_bone_by_source_bone('j_sebo_c','shoulder_L','head','x',1.15)
		offset_bone_by_source_bone('j_sebo_c','shoulder_L','head','y',1)
		offset_bone_by_source_bone('j_sebo_c','shoulder_L','head','z',0.75)
		offset_bone_by_source_bone('j_sebo_c','shoulder_L','tail','x',2.56)
		offset_bone_by_source_bone('j_sebo_c','shoulder_L','tail','z',0.33)
		offset_bone_by_source_bone('j_sebo_c','shoulder_L','tail','y',0.825)
		arm_L = bpy.context.active_object.data.edit_bones['arm_L']
		shoulder_L = bpy.context.active_object.data.edit_bones['shoulder_L']
		arm_L.head = shoulder_L.tail
		arm_L.tail.x = arm_L.tail.x * 0.98
		arm_L.tail.y = arm_L.tail.y * 0.7
		arm_L.tail.z = arm_L.tail.z * 1.008
		elbow_L = bpy.context.active_object.data.edit_bones['elbow_L']
		elbow_L.head = arm_L.tail
		elbow_L.tail.x = elbow_L.tail.x * 0.979
		#elbow_L.tail.y = elbow_L.tail.y * 0.999
		wrist_L = bpy.context.active_object.data.edit_bones['wrist_L']
		wrist_L.head = elbow_L.tail
		wrist_L.tail.x = wrist_L.tail.x * 0.965
		"""
		offset_bone_by_source_bone('j_sebo_c','shoulder_R','head','x',1/1.15)
		offset_bone_by_source_bone('j_sebo_c','shoulder_R','head','y',1)
		offset_bone_by_source_bone('j_sebo_c','shoulder_R','head','z',0.75)
		offset_bone_by_source_bone('j_sebo_c','shoulder_R','tail','x',-0.56)
		offset_bone_by_source_bone('j_sebo_c','shoulder_R','tail','z',0.33)
		offset_bone_by_source_bone('j_sebo_c','shoulder_R','tail','y',0.825)
		arm_R = bpy.context.active_object.data.edit_bones['arm_R']
		shoulder_R = bpy.context.active_object.data.edit_bones['shoulder_R']
		arm_R.head = shoulder_R.tail
		arm_R.tail.x = arm_R.tail.x * 0.98
		arm_R.tail.y = arm_R.tail.y * 0.7
		arm_R.tail.z = arm_R.tail.z * 1.008
		elbow_R = bpy.context.active_object.data.edit_bones['elbow_R']
		elbow_R.head = arm_R.tail
		"""
		bpy.context.object.data.use_mirror_x = False
		bpy.ops.object.mode_set(mode='OBJECT')
	if selected_bone_tool == "convert_ffxiv_boobs_to_genshin_boobs":
		armature = None
		bpy.context.view_layer.objects.active  = model.findArmature(context.active_object)
		armature = bpy.context.view_layer.objects.active
		if armature:
			bpy.ops.object.mode_set(mode='OBJECT')
			convert_ffxiv_boobs_to_genshin_boobs(context,armature)


@register_wrap
class BoneTools(bpy.types.Operator):
	"""Bone Creation/Adjustment Tools"""
	bl_idname = "ffxiv_mmd.bone_tools"
	bl_label = "Bone Tools"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.selected_bone_tool = bpy.props.EnumProperty(items = \
	[('none', 'none', 'none')\
	, ("run_1_to_12", "Run Steps 1 to 12", "Run Steps 1 to 12")\
	, ("delete_unused_bones", "1  -  Remove unused bones (no vertex groups)", "Remove unused bones (no vertex groups)")\
	, ("correct_root_center", "2  -  Correct MMD Root and Ce nter bones", "Correct MMD root and center bones")\
	, ("correct_groove", "3  -  Correct MMD Groove bone", "Correct MMD Groove bone")\
	, ("correct_waist", "4  -  Correct MMD Waist bone", "Correct MMD Waist bone")\
	, ("correct_waist_cancel", "5  -  Correct Waist Cancel L/R bones", "Correct waist cancel left and right bones")\
	, ("correct_view_cnt", "6  -  Correct MMD 'view cnt' bone", "Correct MMD 'view cnt' bone")\
	, ("correct_bones_lengths", "7  -  Correct Shoulder/Arm/Elbow Bone Lengths", "Correct Shoulder/Arm/Elbow Bone Lengths")\
	, ("add_eye_control_bone", "8  -  Add Eyes Control Bone", "Add Eye Control Bone (SELECT 'eyes' bone and run again)")\
	, ("add_arm_wrist_twist", "9  -  Add Arm Twist Bones", "Add Arm Twist Bones")\
	, ("add_shoulder_control_bones", "10-  Add Shoulder Control Bones", "Add Shoulder Control Bones")\
	, ("add_leg_foot_ik", "11-  Add Leg/Foot IK", "Add Leg/Foot IK")\
	, ("auto_fix_mmd_bone_names", "12-  Auto-Fix MMD Japanese/English Bone Names", "Auto-Fix MMD Japanese/English Bone Names")\
	, ("add_hand_arm_ik", "13-  Add Hand/Arm IK", "Add Hand/Arm IK")\
	, ("add_extra_finger_bones", "14- Add Extra Finger Bones (select finger mesh first)", "Add Extra Finger Bones (select finger mesh first)")\
	, ("add_breast_tip_bones", "15- Add Extra Breast Tip Bones", "Add Extra Breast Tip Bones")\
	, ("merge_double_jointed_knee", "16- Merge Double-Jointed Knee (FFXIV PMX Export Only)", "Merge Double-Jointed Knee (FFXIV PMX Export Only)")\
	, ("adjust_arm_position", "EXPERIMENTAL - Adjust Arm Position for FFXIV Models", "Hard-Coded values to better align arms")\
	, ("convert_ffxiv_boobs_to_genshin_boobs", "Convert FFXIV Boobs to Genshin Boobs", "Convert FFXIV Boobs to Genshin Boobs")\
	], name = "", default = 'run_1_to_12')

	@classmethod
	def poll(cls, context):
		obj = context.active_object 
		if bpy.context.scene.selected_bone_tool  == 'add_extra_finger_bones':
			return obj is not None and obj.type == 'MESH'
		else:
			return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		main(context)
		return {'FINISHED'}


@register_wrap
class FFXIVBustSlider(bpy.types.Operator):
	"""Slider for FFXIV Bust"""
	bl_idname = "ffxiv_mmd.bust_slider"
	bl_label = "FFXIV Bust Slider"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.bust_slider = bpy.props.IntProperty(name='Bust',default=50,min=0, soft_min=0,soft_max=300)

	@classmethod
	def poll(cls, context):
		is_ffxiv_bust = False

		if context.active_object is not None:
			obj = context.active_object	
			
			armature = model.findArmature(obj)
			if armature is not None:
				j_mune_l = armature.pose.bones.get('j_mune_l')
				j_mune_r = armature.pose.bones.get('j_mune_r')
				j_mune_core = armature.pose.bones.get('j_mune_core')
				if (j_mune_l is not None and j_mune_r is not None) or (j_mune_core is not None):
					is_ffxiv_bust =True
		
		return is_ffxiv_bust
				

	def execute(self, context):
		set_bust_size(context.scene.bust_slider/100)
		return {'FINISHED'}