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


#gets the equivalent primary bones from armature and returns the primary bonename type (mmd_english,mmd_english_alt, mmd_japanese, mmd_japaneseLR etc...)
def get_primary_bonetype (armature):
	bone_list = {'root','neck','head','center','center_2','upper body','upper body 2','upper body 3','lower body','shoulder_L','arm_L','elbow_L','wrist_L'
			,'thumb0_L','thumb1_L','thumb2_L','fore1_L','fore2_L','fore3_L','middle1_L','middle2_L','middle3_L','third1_L','third2_L','third3_L','little1_L','little2_L','little3_L'
			,'shoulder_R','arm_R','elbow_R','wrist_R',
			'thumb0_R','thumb1_R','thumb2_R','fore1_R','fore2_R','fore3_R','middle1_R','middle2_R','middle3_R','third1_R','third2_R','third3_R','little1_R','little2_R','little3_R'
			,'leg_L','knee_L','ankle_L','toe_L','leg_R','knee_R','ankle_R','toe_R','eye_L','eye_R','waist'}
	
	bone_finds = []
		
	for bone in bone_list:
		if bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,bone):
			armature_bone_name = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,bone)
			bone_finds.append(armature_bone_name)

	bone_types = ['mmd_english', 'mmd_english_alt','mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv','mmd_kaito']

	max_counter = 0
	max_bone_type = None

	for bone_type in bone_types:
		counter = sum(1 for bone in bone_finds if bone_tools.is_bone_bone_type(armature, bone, bone_type))
		if counter > max_counter:
			max_counter = counter
			max_bone_type = bone_type

	return max_bone_type
		
def correct_root_center(armature):

	bone_type = get_primary_bonetype(armature)
	
	if armature and bone_type not in ('mmd_english', 'mmd_english_alt','mmd_japanese', 'mmd_japaneseLR'):
		raise TypeError(f"Primary bone type detected '{bone_type}' is not recognized as an MMD bone type. Rename bones to one of the MMD types (English, EnglishAlt, Japanese, JapaneseLR) and then try again.")
	else:

		print('\ncorrect_root_center():')
		#if model.is_mmd_english() == True:
			
		bpy.ops.object.mode_set(mode='EDIT')

		root_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'root'))
		center_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'center'))
		center_2_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'center_2'))

		# if there is no "root" bone in the armature, a root bone is added
		if not root_bone:
			root_bone = armature.data.edit_bones.new(bone_tools.get_bone_name(bone_type,'root'))
			root_bone.head[:] = (0,0,0)
			root_bone.tail[:] = (0,0,0.7)
			print(f"Added MMD root bone: {root_bone.name}")
				
		# if there is no "center" bone in the armature, a center bone is added
		if center_bone is None:
			center_bone = armature.data.edit_bones.new(bone_tools.get_bone_name(bone_type,'center'))
			print(f"Added MMD center bone: {center_bone.name}")
			center_bone.head = 0.25 * (armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"knee_L")].head \
									+ armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"knee_R")].head \
									+ armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"leg_L")].head \
									+ armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"leg_R")].head)
			center_bone.head.y = 0
			center_bone.tail.z = root_bone.head.z #center_bone.head.z - 0.7

		# set center_bone parent and children
		if center_bone and root_bone:
			center_bone.parent = root_bone
			center_bone.use_connect = False

			bone_list = ['waist','lower body','upper body']

			for mmd_e_bone_name in bone_list:
				bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,mmd_e_bone_name))
				if bone:
					bone.parent = center_bone
				
		# if there is no "center_2" bone in the armature, a center_2 bone is added
		if center_2_bone is None:
			center_2_bone = armature.data.edit_bones.new(bone_tools.get_bone_name(bone_type,"center_2"))
			print(f"Added center_2 bone:{center_2_bone.name}")
		
		# set center_2_bone parent and children
		if center_2_bone and center_bone:
			center_2_bone.matrix = center_bone.matrix
			center_2_bone.tail = center_bone.tail
			center_2_bone.parent = center_bone

			#loop through all the child bones of center and make center_2 the parent
			for child_bone in center_bone.children:
				child_bone.parent = center_2_bone
			
		bpy.ops.object.mode_set(mode='OBJECT')

		
	

def correct_groove(armature):

	bone_type = get_primary_bonetype(armature)
	
	if bone_type not in ('mmd_english', 'mmd_english_alt','mmd_japanese', 'mmd_japaneseLR'):
		raise TypeError(f"Primary bone type detected '{bone_type}' is not recognized as an MMD bone type. Rename bones to one of the MMD types (English, EnglishAlt, Japanese, JapaneseLR) and then try again.")
	else:

		print('\ncorrect_groove():')
		
		bpy.ops.object.mode_set(mode='EDIT')

		center_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'center'))
		center_2_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'center_2'))
			
		groove_parent_bone = center_2_bone or center_bone or None
		
		groove_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'groove'))
		groove_2_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'groove_2'))
		lower_body_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'lower body'))
		upper_body_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'upper body'))

		# if there is no "groove" bone in the armature, a groove bone is added
		if not groove_bone:
			
			groove_bone = armature.data.edit_bones.new(bone_tools.get_bone_name(bone_type,'groove'))
			#groove.head = armature.data.edit_bones["center"].head
			groove_bone.head = groove_parent_bone.head
			groove_bone.head.z = 0.01 + groove_bone.head.z
			groove_bone.tail.z = 0.1 + (groove_bone.head.z)
			#groove.parent = armature.data.edit_bones["center"]
			print(f"Added groove bone: {groove_bone.name}")

		# set groove children
		if groove_bone:
			groove_bone.parent = groove_parent_bone
			if lower_body_bone:
				lower_body_bone.parent = groove_bone
			if upper_body_bone:
				upper_body_bone.parent = groove_bone
			
		# if there is no "groove_2" bone in the armature, a groove_2 bone is added
		if not groove_2_bone:
			groove_2_bone = armature.data.edit_bones.new(bone_tools.get_bone_name(bone_type,'groove_2'))
			print(f"Added groove_2 bone:{groove_2_bone.name}")
				
			if groove_bone:
				groove_2_bone.matrix = groove_bone.matrix
				groove_2_bone.tail = groove_bone.tail
				groove_2_bone.parent = groove_bone

				#loop through all the child bones of center and make center_2 the parent
				for child_bone in groove_bone.children:
					child_bone.parent = groove_2_bone

		bpy.ops.object.mode_set(mode='OBJECT')


def correct_waist(armature):

	bone_type = get_primary_bonetype(armature)
	
	if armature and bone_type not in ('mmd_english', 'mmd_english_alt','mmd_japanese', 'mmd_japaneseLR'):
		raise TypeError(f"Primary bone type detected '{bone_type}' is not recognized as an MMD bone type. Rename bones to one of the MMD types (English, EnglishAlt, Japanese, JapaneseLR) and then try again.")
	else:
		bpy.ops.object.mode_set(mode='EDIT')
		
		waist_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'waist'))
		groove_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'groove'))
		groove_2_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'groove_2'))
		waist_parent = groove_2_bone or groove_bone
		lower_body_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'lower body'))
		upper_body_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'upper body'))

		

		# if there is no "waist" bone in the armature, a waist bone is added
		if not waist_bone:
			waist_bone = armature.data.edit_bones.new(bone_tools.get_bone_name(bone_type,'waist'))
			waist_bone.head = upper_body_bone.head
			waist_bone.tail = waist_bone.head
			waist_bone.tail.z = waist_bone.tail.z - 0.05
			waist_bone.length = upper_body_bone.length * 0.5


		# adjust the waist bone
		waist_bone.name = bone_tools.get_bone_name(bone_type,'waist')
		waist_bone.tail = waist_bone.head
		waist_bone.head.z = waist_bone.tail.z - 0.05
		waist_bone.head.y = waist_bone.tail.y + 0.03
		waist_bone.roll = 0
		#waist.parent = armature.data.edit_bones["groove"]
		waist_bone.parent = waist_parent
		if lower_body_bone:
			lower_body_bone.parent = waist_bone
		if upper_body_bone:
			upper_body_bone.parent = waist_bone
		print("inverted the waist bone.")

		bpy.ops.object.mode_set(mode='OBJECT')
		

def correct_waist_cancel(armature):

	bone_type = get_primary_bonetype(armature)
	
	if armature and bone_type not in ('mmd_english', 'mmd_english_alt','mmd_japanese', 'mmd_japaneseLR'):
		raise TypeError(f"Primary bone type detected '{bone_type}' is not recognized as an MMD bone type. Rename bones to one of the MMD types (English, EnglishAlt, Japanese, JapaneseLR) and then try again.")
	else:
		bpy.ops.object.mode_set(mode='EDIT')

		#measurements of the length of the foot bone which will used to calculate the lengths of the new bones.
		HALF_LENGTH_OF_FOOT_BONE = armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"ankle_L")].length * 0.5
		
		lower_body_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'lower body'))
		leg_l_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'leg_L'))
		leg_r_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'leg_R'))
		waist_cancel_L_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'waist_cancel_L'))
		waist_cancel_R_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'waist_cancel_R'))

		if not waist_cancel_L_bone:
			waist_cancel_L_bone = bone_tools.add_bone(armature,bone_tools.get_bone_name(bone_type,'waist_cancel_L'), parent_bone= lower_body_bone, head= leg_l_bone.head, tail= leg_l_bone.head)
			waist_cancel_L_bone.tail.z = leg_l_bone.head.z + HALF_LENGTH_OF_FOOT_BONE
			print(f"Added waist_cancel_l bone: {waist_cancel_L_bone.name}")


		if leg_l_bone:
			leg_l_bone.parent = waist_cancel_L_bone

		if not waist_cancel_R_bone:
			waist_cancel_R_bone = bone_tools.add_bone(armature,bone_tools.get_bone_name(bone_type,'waist_cancel_R'), parent_bone= lower_body_bone,head=leg_r_bone.head,tail=leg_r_bone.head)
			waist_cancel_R_bone.tail.z = leg_l_bone.head.z + HALF_LENGTH_OF_FOOT_BONE
			print(f"Added waist_cancel_r bone: {waist_cancel_R_bone.name}")

		if leg_r_bone:
			leg_r_bone.parent = waist_cancel_R_bone
	
		#make waist_cancel a control bone for waist
		bpy.ops.object.mode_set(mode='POSE')
		armature = bpy.context.view_layer.objects.active
		waist_bone = armature.pose.bones.get(bone_tools.get_bone_name(bone_type,'waist'))
		waist_cancel_L_bone = armature.pose.bones.get(bone_tools.get_bone_name(bone_type,'waist_cancel_L'))
		waist_cancel_R_bone = armature.pose.bones.get(bone_tools.get_bone_name(bone_type,'waist_cancel_R'))
		bone_tools.apply_MMD_additional_rotation (armature,waist_bone.name, waist_cancel_L_bone.name, -1.0)
		bone_tools.apply_MMD_additional_rotation (armature,waist_bone.name, waist_cancel_R_bone.name, -1.0)
		#FnBone.apply_additional_transformation(armature)

		bpy.ops.object.mode_set(mode='OBJECT')


def correct_view_cnt(armature):

	bone_type = get_primary_bonetype(armature)
	
	if armature and bone_type not in ('mmd_english', 'mmd_english_alt','mmd_japanese', 'mmd_japaneseLR'):
		raise TypeError(f"Primary bone type detected '{bone_type}' is not recognized as an MMD bone type. Rename bones to one of the MMD types (English, EnglishAlt, Japanese, JapaneseLR) and then try again.")
	else:
		bpy.ops.object.mode_set(mode='EDIT')

		view_cnt_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,"view cnt"))

		# if there is no "view_cnt" bone in the armature, a root bone is added
		if not view_cnt_bone:
			view_cnt_bone = armature.data.edit_bones.new(bone_tools.get_bone_name(bone_type,"view cnt"))
			view_cnt_bone.head[:] = (0,0,0)
			view_cnt_bone.tail[:] = (0,0,0.08)
			print(f"Added MMD 'view cnt' bone: {view_cnt_bone.name}")
		bpy.ops.object.mode_set(mode='OBJECT')

	

def add_extra_finger_bones(armature,hand_mesh): 
	print('\nadd_extra_finger_bones(armature,hand_mesh):')
	
	bone_type = get_primary_bonetype(armature)
	
	if armature and bone_type not in ('mmd_english', 'mmd_english_alt','mmd_japanese', 'mmd_japaneseLR'):
		raise TypeError(f"Primary bone type detected '{bone_type}' is not recognized as an MMD bone type. Rename bones to one of the MMD types (English, EnglishAlt, Japanese, JapaneseLR) and then try again.")
	else:
		bpy.ops.object.mode_set(mode='EDIT')

		correct_finger(armature,hand_mesh,bone_tools.get_bone_name(bone_type,'fore2_L'),bone_tools.get_bone_name(bone_type,'fore3_L'))
		correct_finger(armature,hand_mesh,bone_tools.get_bone_name(bone_type,'little2_L'),bone_tools.get_bone_name(bone_type,'little3_L'))
		correct_finger(armature,hand_mesh,bone_tools.get_bone_name(bone_type,'third2_L'),bone_tools.get_bone_name(bone_type,'third3_L'))
		correct_finger(armature,hand_mesh,bone_tools.get_bone_name(bone_type,'middle2_L'),bone_tools.get_bone_name(bone_type,'middle3_L'))
		correct_finger(armature,hand_mesh,bone_tools.get_bone_name(bone_type,'fore2_R'),bone_tools.get_bone_name(bone_type,'fore3_R'))
		correct_finger(armature,hand_mesh,bone_tools.get_bone_name(bone_type,'little2_R'),bone_tools.get_bone_name(bone_type,'little3_R'))
		correct_finger(armature,hand_mesh,bone_tools.get_bone_name(bone_type,'third2_R'),bone_tools.get_bone_name(bone_type,'third3_R'))
		correct_finger(armature,hand_mesh,bone_tools.get_bone_name(bone_type,'middle2_R'),bone_tools.get_bone_name(bone_type,'middle3_R'))
		print('added third finger bones')

		bpy.ops.object.mode_set(mode='OBJECT')
	
			

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

def correct_bones_length(armature):

	bone_type = get_primary_bonetype(armature)
	
	if armature and bone_type not in ('mmd_english', 'mmd_english_alt','mmd_japanese', 'mmd_japaneseLR'):
		raise TypeError(f"Primary bone type detected '{bone_type}' is not recognized as an MMD bone type. Rename bones to one of the MMD types (English, EnglishAlt, Japanese, JapaneseLR) and then try again.")
	else:
		bpy.ops.object.mode_set(mode='EDIT')

		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		fix_bone_length(armature,bone_tools.get_bone_name(bone_type,'shoulder_L'),bone_tools.get_bone_name(bone_type,'arm_L'))
		fix_bone_length(armature,bone_tools.get_bone_name(bone_type,'shoulder_R'),bone_tools.get_bone_name(bone_type,'arm_R'))
		fix_bone_length(armature,bone_tools.get_bone_name(bone_type,'arm_L'),bone_tools.get_bone_name(bone_type,'elbow_L'))
		fix_bone_length(armature,bone_tools.get_bone_name(bone_type,'arm_R'),bone_tools.get_bone_name(bone_type,'elbow_R'))
		fix_bone_length(armature,bone_tools.get_bone_name(bone_type,'elbow_L'),bone_tools.get_bone_name(bone_type,'wrist_L'))
		fix_bone_length(armature,bone_tools.get_bone_name(bone_type,'elbow_R'),bone_tools.get_bone_name(bone_type,'wrist_R'))
		print('reset bone length for shoulder/arm/elbow')

		bpy.ops.object.mode_set(mode='OBJECT')

def add_breast_tip_bones(armature):
	print('\nadd_breast_tip_bones(armature):')
	bone_type = get_primary_bonetype(armature)
	
	if armature and bone_type not in ('mmd_english', 'mmd_english_alt','mmd_japanese', 'mmd_japaneseLR'):
		raise TypeError(f"Primary bone type detected '{bone_type}' is not recognized as an MMD bone type. Rename bones to one of the MMD types (English, EnglishAlt, Japanese, JapaneseLR) and then try again.")
	else:
		bpy.ops.object.mode_set(mode='EDIT')
	
		breast = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'bust_L'))
		if breast and armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'bust_2_L')) is None:
			bone = bone_tools.add_bone(armature,bone_tools.get_bone_name(bone_type,'bust_2_L'),parent_bone=breast,head=breast.head,tail=breast.tail,length=breast.length*1.25)
			bone.head = breast.tail
			bone.roll = breast.roll

		breast = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'bust_R'))
		if breast and armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,'bust_2_R')) is None:
			bone = bone_tools.add_bone(armature,bone_tools.get_bone_name(bone_type,'bust_2_R'),parent_bone=breast,head=breast.head,tail=breast.tail,length=breast.length*1.25)
			bone.head = breast.tail
			bone.roll = breast.roll

		bpy.ops.object.mode_set(mode='OBJECT')

def add_eye_control_bone(armature):
	print('\nadd_eye_control_bone():')
	bone_type = get_primary_bonetype(armature)

	if armature and bone_type not in ('mmd_english', 'mmd_english_alt','mmd_japanese', 'mmd_japaneseLR'):
		raise TypeError(f"Primary bone type detected '{bone_type}' is not recognized as an MMD bone type. Rename bones to one of the MMD types (English, EnglishAlt, Japanese, JapaneseLR) and then try again.")
	else:
		bpy.ops.object.mode_set(mode='EDIT')

		eye_L_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,"eye_L"))
		eye_R_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,"eye_R"))
		head_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,"head"))
		
		eyes_bone = armature.data.edit_bones.get(bone_tools.get_bone_name(bone_type,"eyes"))
		if not eyes_bone:
			eyes_bone = armature.data.edit_bones.new(bone_tools.get_bone_name(bone_type,"eyes"))
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
				
		bone_tools.apply_MMD_additional_rotation(armature,bone_tools.get_bone_name(bone_type,'eyes'),bone_tools.get_bone_name(bone_type,'eye_L'),1)
		bone_tools.apply_MMD_additional_rotation(armature,bone_tools.get_bone_name(bone_type,'eyes'),bone_tools.get_bone_name(bone_type,'eye_R'),1)	

		bpy.ops.object.mode_set(mode='POSE')
		#set bones as tip bones
		armature.pose.bones[bone_tools.get_bone_name(bone_type,'eyes')].mmd_bone.is_tip = True


		bpy.ops.object.mode_set(mode='OBJECT')

	



def add_arm_wrist_twist(armature):
	bone_type = get_primary_bonetype(armature)

	if armature and bone_type not in ('mmd_english', 'mmd_english_alt','mmd_japanese', 'mmd_japaneseLR'):
		raise TypeError(f"Primary bone type detected '{bone_type}' is not recognized as an MMD bone type. Rename bones to one of the MMD types (English, EnglishAlt, Japanese, JapaneseLR) and then try again.")
	else:
		bpy.ops.object.mode_set(mode='EDIT')
	
		# set the armature to Edit Mode
		armature = bpy.context.view_layer.objects.active
		
		#parent the elbow bone to the arm twist
		arm_twist_L = armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"arm_twist_L")]
		arm_twist_R = armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"arm_twist_R")]
		elbow_L = armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"elbow_L")]
		elbow_R = armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"elbow_R")]
		elbow_L.parent = arm_twist_L
		elbow_R.parent = arm_twist_R

		#parent the wrist bone to the wrist twist
		wrist_twist_L = armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"wrist_twist_L")]
		wrist_twist_R = armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"wrist_twist_R")]
		wrist_L = armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"wrist_L")]
		wrist_R = armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"wrist_R")]
		wrist_L.parent = wrist_twist_L
		wrist_R.parent = wrist_twist_R
		
		armature.pose.bones.get(arm_twist_L.name).lock_rotation = [True,False,True]
		armature.pose.bones.get(arm_twist_R.name).lock_rotation = [True,False,True]
		armature.pose.bones.get(wrist_twist_L.name).lock_rotation = [True,False,True]
		armature.pose.bones.get(wrist_twist_R.name).lock_rotation = [True,False,True]


		####### DO NOT TOUCH ANYWHERE BELOW THIS CODE, IT WILL BREAK BLENDER IF YOU DO#################	
		create_twist_support_bones(armature,'arm_L','arm_twist_1_L','arm_twist_2_L','arm_twist_3_L','arm_twist_L',bone_type)
		create_twist_support_bones(armature,'arm_R','arm_twist_1_R','arm_twist_2_R','arm_twist_3_R','arm_twist_R',bone_type)
		create_twist_support_bones(armature,'elbow_L','wrist_twist_1_L','wrist_twist_2_L','wrist_twist_3_L','wrist_twist_L',bone_type)
		create_twist_support_bones(armature,'elbow_R','wrist_twist_1_R','wrist_twist_2_R','wrist_twist_3_R','wrist_twist_R',bone_type)

		#used to move the wrist_twist to elbow's tail
		offset_bone_by_parents_tail(bone_tools.get_bone_name(bone_type,'elbow_L'),bone_tools.get_bone_name(bone_type,'wrist_twist_L'), 0.33)
		offset_bone_by_parents_tail(bone_tools.get_bone_name(bone_type,'elbow_R'),bone_tools.get_bone_name(bone_type,'wrist_twist_R'), 0.33)


		bpy.ops.object.mode_set(mode='OBJECT')

def create_twist_support_bones(armature,source_bone_name,bone_1_name,bone_2_name,bone_3_name,additional_rotation_bone_name,bone_type):
	if armature:
		# Get the armature in edit mode
		bpy.ops.object.mode_set(mode='EDIT')

		armature.data['source_bone_name']  = bone_tools.get_bone_name(bone_type,source_bone_name)
		armature.data['bone_1_name'] = bone_tools.get_bone_name(bone_type,bone_1_name)
		armature.data['bone_2_name'] = bone_tools.get_bone_name(bone_type,bone_2_name)	
		armature.data['bone_3_name'] = bone_tools.get_bone_name(bone_type,bone_3_name)
		armature.data['additional_rotation_bone_name'] = bone_tools.get_bone_name(bone_type,additional_rotation_bone_name)
	
		# Get the source bone
		print ('######')
		print (armature.data['source_bone_name'])
		print (bone_type)
		print (armature.name)

		
		source_bone = armature.data.edit_bones[armature.data['source_bone_name']]


		#source_bone.name = bone_tools.get_bone_name(bone_type,armature.data['source_bone_name'])


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
			_bone_1 = bone_tools.add_bone(armature, armature.data['bone_1_name'] ,parent_bone=source_bone,length= length * 0.30,head= pos1,tail= pos1 + mathutils.Vector((0, 0, length * 0.1)))
			_bone_2 = bone_tools.add_bone(armature, armature.data['bone_2_name'] ,parent_bone=source_bone,length= length * 0.30,head= pos2,tail= pos2 + mathutils.Vector((0, 0, length * 0.1)))
			_bone_3 = bone_tools.add_bone(armature, armature.data['bone_3_name'] ,parent_bone=source_bone,length= length * 0.30,head= pos3,tail= pos3 + mathutils.Vector((0, 0, length * 0.1)))

			
			bpy.ops.object.mode_set(mode='POSE')

			additional_rotation_bone = armature.pose.bones.get(armature.data['additional_rotation_bone_name'])
			additional_rotation_bone = bone_tools.get_bone_name(bone_type,armature.data['additional_rotation_bone_name'])

			#set bones as tip bones
			armature.pose.bones[armature.data['bone_1_name']].mmd_bone.is_tip = True
			armature.pose.bones[armature.data['bone_2_name']].mmd_bone.is_tip = True
			armature.pose.bones[armature.data['bone_3_name']].mmd_bone.is_tip = True

			#apply additional rotation
			bone_tools.apply_MMD_additional_rotation(armature,armature.data['additional_rotation_bone_name'],armature.data['bone_1_name'], 0.25)
			bone_tools.apply_MMD_additional_rotation(armature,armature.data['additional_rotation_bone_name'],armature.data['bone_2_name'], 0.50)
			bone_tools.apply_MMD_additional_rotation(armature,armature.data['additional_rotation_bone_name'],armature.data['bone_3_name'], 0.75)

			armature.data.pop('source_bone_name')
			armature.data.pop('bone_1_name')
			armature.data.pop('bone_2_name')
			armature.data.pop('bone_3_name')
			armature.data.pop('additional_rotation_bone_name')
			
			# Return to object mode
			bpy.ops.object.mode_set(mode='OBJECT')
	else:
		print("Armature object not found")


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


def add_shoulder_control_bones(armature):
	print('\nadd_shoulder_control_bones():')

	bone_type = get_primary_bonetype(armature)

	if armature and bone_type not in ('mmd_english', 'mmd_english_alt','mmd_japanese', 'mmd_japaneseLR'):
		raise TypeError(f"Primary bone type detected '{bone_type}' is not recognized as an MMD bone type. Rename bones to one of the MMD types (English, EnglishAlt, Japanese, JapaneseLR) and then try again.")
	else:
		bpy.ops.object.mode_set(mode='EDIT')

		#get the bones
		shoulder_L = armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"shoulder_L")]
		shoulder_R = armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"shoulder_R")]
		arm_L = armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"arm_L")]
		arm_R = armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"arm_R")]
		upper_body_3 = armature.data.edit_bones[bone_tools.get_bone_name(bone_type,"upper body 3")]

		#create new bones
		shoulder_P_L = bone_tools.add_bone(armature,bone_tools.get_bone_name(bone_type, 'shoulder_P_L'),parent_bone=upper_body_3,length=shoulder_L.length,head=shoulder_L.head ,tail=shoulder_L.head)
		shoulder_P_R = bone_tools.add_bone(armature,bone_tools.get_bone_name(bone_type, 'shoulder_P_R'),parent_bone=upper_body_3,length=shoulder_R.length,head=shoulder_R.head ,tail=shoulder_R.head)
		shoulder_C_L = bone_tools.add_bone(armature,bone_tools.get_bone_name(bone_type, 'shoulder_C_L'),parent_bone=shoulder_L,length=shoulder_L.length,head=shoulder_L.tail ,tail=shoulder_L.tail)
		shoulder_C_R = bone_tools.add_bone(armature,bone_tools.get_bone_name(bone_type, 'shoulder_C_R'),parent_bone=shoulder_R,length=shoulder_R.length,head=shoulder_R.tail ,tail=shoulder_R.tail)

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
		armature.pose.bones[bone_tools.get_bone_name(bone_type,'shoulder_P_L')].mmd_bone.is_tip = True
		armature.pose.bones[bone_tools.get_bone_name(bone_type,'shoulder_C_L')].mmd_bone.is_tip = True
		armature.pose.bones[bone_tools.get_bone_name(bone_type,'shoulder_P_R')].mmd_bone.is_tip = True
		armature.pose.bones[bone_tools.get_bone_name(bone_type,'shoulder_C_R')].mmd_bone.is_tip = True
		
		
		bone_tools.apply_MMD_additional_rotation (armature,bone_tools.get_bone_name(bone_type,'shoulder_P_L'), bone_tools.get_bone_name(bone_type,'shoulder_C_L'), -1.0)
		bone_tools.apply_MMD_additional_rotation (armature,bone_tools.get_bone_name(bone_type,'shoulder_P_R'), bone_tools.get_bone_name(bone_type,'shoulder_C_R'), -1.0)
		#FnBone.apply_additional_transformation(armature)

		bpy.ops.object.mode_set(mode='OBJECT')
	


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
		j_sebo_c = armature.data.edit_bones.get(bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'upper body 3'))
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

	armature = model.findArmature(context.active_object)
	context.view_layer.objects.active = armature

	selected_bone_tool = bpy.context.scene.selected_bone_tool
	if selected_bone_tool == "delete_unused_bones":
		miscellaneous_tools.flag_unused_bones()
		miscellaneous_tools.delete_unused_bones()
	if selected_bone_tool == "correct_root_center":
		correct_root_center(armature)
	if selected_bone_tool == "correct_groove":
		correct_groove(armature)
	if selected_bone_tool == "correct_waist":
		correct_waist(armature)
	if selected_bone_tool == "correct_waist_cancel":
		correct_waist_cancel(armature)
	if selected_bone_tool == "correct_view_cnt":
		correct_view_cnt(armature)
	if selected_bone_tool == "correct_bones_lengths":
		correct_bones_length(armature)
	if selected_bone_tool == "add_eye_control_bone":
		add_eye_control_bone(armature)
	if selected_bone_tool == "add_arm_wrist_twist":
		add_arm_wrist_twist(armature)
	if selected_bone_tool == "add_shoulder_control_bones":
		add_shoulder_control_bones(armature)
	if selected_bone_tool == "add_leg_foot_ik":
		armature = bpy.context.view_layer.objects.active
		bpy.ops.object.mode_set(mode='OBJECT')
		add_foot_leg_ik.clear_IK(context)
		add_foot_leg_ik.main(context)
		bpy.ops.object.mode_set(mode='OBJECT')
	if selected_bone_tool == "auto_fix_mmd_bone_names":
		context.view_layer.objects.active  = model.findArmature(context.active_object)
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
		bpy.context.view_layer.objects.active  = model.findArmature(context.active_object)
		armature = bpy.context.view_layer.objects.active
		add_extra_finger_bones(armature,mesh)
	if selected_bone_tool == "add_breast_tip_bones":
		bpy.context.view_layer.objects.active  = model.findArmature(context.active_object)
		armature = bpy.context.view_layer.objects.active
		add_breast_tip_bones(armature)
	if selected_bone_tool == "merge_double_jointed_knee":
		bpy.context.view_layer.objects.active  = model.findArmature(context.active_object)
		armature = bpy.context.view_layer.objects.active
		merge_double_jointed_knee(armature,context)
	if selected_bone_tool == "run_1_to_12":
		#delete unused bones
		bpy.context.view_layer.objects.active  = model.findArmature(context.active_object)
		armature = context.view_layer.objects.active
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
		bpy.context.view_layer.objects.active  = model.findArmature(context.active_object)
		armature = context.view_layer.objects.active
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
	, ("correct_root_center", "2  -  Correct MMD Root, Center and Center_2 bones", "Adds MMD root, center and center_2 bones if missing")\
	, ("correct_groove", "3  -  Correct MMD Groove and Groove_2 bones", "Adds MMD groove and groove_2 bones if missing")\
	, ("correct_waist", "4  -  Correct MMD Waist bone", "Moves MMD Waist bone")\
	, ("correct_waist_cancel", "5  -  Correct Waist Cancel L/R bones", "Adds 'waist_cancel_l/r' bones if missing")\
	, ("correct_view_cnt", "6  -  Correct MMD 'view cnt' bone", "Adds 'view_cnt' bone if missing")\
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