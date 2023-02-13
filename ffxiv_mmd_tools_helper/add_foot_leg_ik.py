import bpy
import math

from . import register_wrap
#from .panels.bones_ik import Add_MMD_foot_leg_IK_Panel
from . import model
from mmd_tools.core.bone import FnBone
from . import bone_tools


# def armature_diagnostic():
	# ENGLISH_LEG_BONES = ["knee_L", "knee_R", "ankle_L", "ankle_R", "toe_L", "toe_R"]
	# JAPANESE_LEG_BONES = ["左ひざ", "右ひざ", "左足首", "右足首", "左つま先", "右つま先"]
	# IK_BONE_NAMES = ["leg IK_L", "leg IK_R", "toe IK_L", "toe IK_R", "左足ＩＫ", "右足ＩＫ", "左つま先ＩＫ", "右つま先ＩＫ"]
	# ENGLISH_OK = True
	# JAPANESE_OK = True

	# print('\n\n\n', 'These English bones are needed to add IK:', '\n')
	# print(ENGLISH_LEG_BONES, '\n')
	# for b in ENGLISH_LEG_BONES:
		# if b not in bpy.context.active_object.data.bones.keys():
			# ENGLISH_OK = False
			# print('This bone is not in this armature:', '\n', b)
	# if ENGLISH_OK == True:
		# print('OK! All English-named bones are present which are needed to add leg IK')

	# print('\n', 'OR These Japanese bones are needed to add IK:', '\n')
	# print(JAPANESE_LEG_BONES, '\n')
	# for b in JAPANESE_LEG_BONES:
		# if b not in bpy.context.active_object.data.bones.keys():
			# JAPANESE_OK = False
			# print('This bone is not in this armature:', '\n', b)
	# if JAPANESE_OK == True:
		# print('OK! All Japanese-named bones are present which are needed to add leg IK', '\n')

	# print('\n', 'IK bone names', '\n')
	# for b in IK_BONE_NAMES:
		# if b in bpy.context.active_object.data.bones.keys():
			# print('This armature appears to already have IK bones. This bone seems to be an IK bone:', '\n', b)


def clear_IK(context):
	IK_target_bones = []
	IK_target_tip_bones = []
	bpy.context.view_layer.objects.active = get_armature()
	bpy.ops.object.mode_set(mode='POSE')
	english = ["knee_L", "knee_R", "ankle_L", "ankle_R", "toe_L", "toe_R"]
	japanese = ["左ひざ", "右ひざ", "左足首", "右足首", "左つま先", "右つま先"]
	japanese_L_R = ["ひざ.L", "ひざ.R", "足首.L", "足首.R", "つま先.L", "つま先.R"]
	leg_foot_bones = english + japanese + japanese_L_R
	for b in bpy.context.active_object.pose.bones.keys():
		if b in leg_foot_bones:
			for c in bpy.context.active_object.pose.bones[b].constraints:
				if c.type == "IK":
					print("c.target = ", c.target)
					if c.target == bpy.context.view_layer.objects.active:
						if c.subtarget is not None:
							print("c.subtarget = ", c.subtarget)
							if c.subtarget not in IK_target_bones:
								IK_target_bones.append(c.subtarget)
	for b in IK_target_bones:
		for c in bpy.context.active_object.pose.bones[b].children:
			if c.name not in IK_target_tip_bones:
				IK_target_tip_bones.append(c.name)
	bones_to_be_deleted = set(IK_target_bones + IK_target_tip_bones)
	print("bones to be deleted = ", bones_to_be_deleted)
	bpy.ops.object.mode_set(mode='EDIT')
	for b in bones_to_be_deleted:
		edit_bones.remove(edit_bones[b])
	bpy.ops.object.mode_set(mode='POSE')
	for b in bpy.context.active_object.pose.bones.keys():
		if b in leg_foot_bones:
			for c in bpy.context.active_object.pose.bones[b].constraints:
				bpy.context.active_object.pose.bones[b].constraints.remove(c)
				# if c.type == "IK":
					# bpy.context.active_object.pose.bones[b].constraints.remove(c)
				# if c.type == "LIMIT_ROTATION":
					# bpy.context.active_object.pose.bones[b].constraints.remove(c)

	bpy.ops.object.mode_set(mode='OBJECT')


def main(context):
	bpy.context.view_layer.objects.active = get_armature()
	armature=get_armature()

	#Searches through the bones of the armature and finds the knee, ankle and toe bones.
	ROOT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'root')
	LOWER_BODY = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'lower body')
	LEG_LEFT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'leg_L')
	LEG_RIGHT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'leg_R')
	KNEE_LEFT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'knee_L')
	KNEE_RIGHT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'knee_R')
	ANKLE_LEFT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'ankle_L')
	ANKLE_RIGHT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'ankle_R')
	TOE_LEFT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'toe_L')
	TOE_RIGHT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'toe_R')
	KNEE2_LEFT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'knee_2_L')
	KNEE2_RIGHT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'knee_2_R')

	bones = [ROOT,LOWER_BODY,LEG_LEFT,LEG_RIGHT,KNEE_LEFT,KNEE_RIGHT,ANKLE_LEFT,ANKLE_RIGHT,TOE_LEFT,TOE_RIGHT]
	bone_check_english = []
	bone_check_japanese = []
	bone_check_japaneseLR = [] 

	#test japanese or english
	for bone_name in bones:
		bone_check_english.append(bone_tools.is_bone_bone_type(armature,bone_name,"mmd_english"))

	for bone_name in bones:
		bone_check_japanese.append(bone_tools.is_bone_bone_type(armature,bone_name,"mmd_japanese"))

	for bone_name in bones:
		bone_check_japaneseLR.append(bone_tools.is_bone_bone_type(armature,bone_name,"mmd_japaneseLR"))

	mmd_bone_type = None

	#if all bone are the same type and are found (is_bone_bone_type=True)
	if all(bone_check_english):
		mmd_bone_type = 'mmd_english'
	elif all(bone_check_japanese):
		mmd_bone_type = 'mmd_japanese'
	elif all(bone_check_japaneseLR):
		mmd_bone_type = 'mmd_japaneseLR'
	else:
		print ('This is not an MMD armature. MMD bone names of knee, ankle and toe bones are required for this script to run.')
	print (mmd_bone_type)


	if mmd_bone_type:
		LEG_IK_ROOT_LEFT_BONE = bone_tools.get_bone_name_by_mmd_english_bone_name("leg IK_root_L",mmd_bone_type)
		LEG_IK_ROOT_RIGHT_BONE = bone_tools.get_bone_name_by_mmd_english_bone_name("leg IK_root_R",mmd_bone_type)
		LEG_IK_LEFT_BONE = bone_tools.get_bone_name_by_mmd_english_bone_name("leg IK_L",mmd_bone_type)
		LEG_IK_RIGHT_BONE = bone_tools.get_bone_name_by_mmd_english_bone_name("leg IK_R",mmd_bone_type)
		TOE_IK_LEFT_BONE = bone_tools.get_bone_name_by_mmd_english_bone_name("toe IK_L",mmd_bone_type)
		TOE_IK_RIGHT_BONE = bone_tools.get_bone_name_by_mmd_english_bone_name("toe IK_R",mmd_bone_type)
		LEG_LEFT_D = bone_tools.get_bone_name_by_mmd_english_bone_name("leg_L_D",mmd_bone_type)
		LEG_RIGHT_D = bone_tools.get_bone_name_by_mmd_english_bone_name("leg_R_D",mmd_bone_type)
		KNEE_LEFT_D = bone_tools.get_bone_name_by_mmd_english_bone_name("knee_L_D",mmd_bone_type)
		KNEE_RIGHT_D = bone_tools.get_bone_name_by_mmd_english_bone_name("knee_R_D",mmd_bone_type)
		ANKLE_LEFT_D = bone_tools.get_bone_name_by_mmd_english_bone_name("ankle_L_D",mmd_bone_type)
		ANKLE_RIGHT_D = bone_tools.get_bone_name_by_mmd_english_bone_name("ankle_R_D",mmd_bone_type)
		TOE_LEFT_EX = bone_tools.get_bone_name_by_mmd_english_bone_name("toe_L_EX",mmd_bone_type)
		TOE_RIGHT_EX = bone_tools.get_bone_name_by_mmd_english_bone_name("toe_R_EX",mmd_bone_type)
		KNEE2_LEFT_D = bone_tools.get_bone_name_by_mmd_english_bone_name("knee_2_L_D",mmd_bone_type)
		KNEE2_RIGHT_D = bone_tools.get_bone_name_by_mmd_english_bone_name("knee_2_R_D",mmd_bone_type)
		


	print('\n')



	if all([ROOT,LOWER_BODY,LEG_LEFT,LEG_RIGHT,KNEE_LEFT,KNEE_RIGHT,ANKLE_LEFT,ANKLE_RIGHT,TOE_LEFT,TOE_RIGHT]):

		bpy.ops.object.mode_set(mode='POSE')
		bpy.context.active_object.pose.bones[KNEE_LEFT].use_ik_limit_x = True
		bpy.context.active_object.pose.bones[KNEE_RIGHT].use_ik_limit_x = True

		#The IK bones are created
		create_IK_bones(armature,ANKLE_LEFT,LEG_IK_ROOT_LEFT_BONE,ROOT,ANKLE_RIGHT,LEG_IK_ROOT_RIGHT_BONE,LEG_IK_LEFT_BONE,LEG_IK_RIGHT_BONE,TOE_IK_LEFT_BONE,TOE_LEFT,TOE_IK_RIGHT_BONE,TOE_RIGHT)

		#Add IK constraints
		create_IK_constraints(KNEE_LEFT,LEG_IK_LEFT_BONE,KNEE_RIGHT,LEG_IK_RIGHT_BONE,ANKLE_LEFT,TOE_IK_LEFT_BONE,ANKLE_RIGHT,TOE_IK_RIGHT_BONE,KNEE2_LEFT,KNEE2_RIGHT)
		
		#create an 'IK' bone group and add the IK bones to it
		create_IK_bone_group(LEG_IK_ROOT_LEFT_BONE,LEG_IK_ROOT_RIGHT_BONE,LEG_IK_LEFT_BONE,LEG_IK_RIGHT_BONE,TOE_IK_LEFT_BONE,TOE_IK_RIGHT_BONE)

		#create control bones
		create_control_bones(armature,LEG_LEFT,LEG_RIGHT,KNEE_LEFT,KNEE_RIGHT,ANKLE_LEFT,ANKLE_RIGHT,TOE_LEFT,TOE_RIGHT,LOWER_BODY,LEG_LEFT_D,LEG_RIGHT_D,KNEE_LEFT_D,KNEE_RIGHT_D,ANKLE_LEFT_D,ANKLE_RIGHT_D,TOE_LEFT_EX,TOE_RIGHT_EX,KNEE2_LEFT,KNEE2_RIGHT,KNEE2_LEFT_D,KNEE2_RIGHT_D)

		bpy.context.active_object.data.display_type = 'OCTAHEDRAL'
	else:
		print('error--count not find one of these bones: root,lower body,leg_L,leg_R,knee_L,knee_R,ankle_L,ankle_R,toe_L,toe_R. aborted.')

def create_IK_bones(armature,ANKLE_LEFT,LEG_IK_ROOT_LEFT_BONE,ROOT,ANKLE_RIGHT,LEG_IK_ROOT_RIGHT_BONE,LEG_IK_LEFT_BONE,LEG_IK_RIGHT_BONE,TOE_IK_LEFT_BONE,TOE_LEFT,TOE_IK_RIGHT_BONE,TOE_RIGHT):

	bpy.ops.object.mode_set(mode='EDIT')
	edit_bones = bpy.context.active_object.data.edit_bones

	#check if IK bones already exist

	#measurements of the length of the foot bone which will used to calculate the lengths of the IK bones.
	LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length
	TWO_THIRDS_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length * 0.66
	HALF_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length * 0.5
	#QUARTER_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length * 0.25

	#The IK bones are created
	#LEG_IK_ROOT_LEFT_BONE
	bone = bone_tools.add_bone(armature,LEG_IK_ROOT_LEFT_BONE,parent_bone=edit_bones[ROOT],head=edit_bones[ANKLE_LEFT].head,tail=edit_bones[ANKLE_LEFT].head)
	bone.head.z = edit_bones[ANKLE_LEFT].head.z - TWO_THIRDS_LENGTH_OF_FOOT_BONE 

	#LEG_IK_ROOT_RIGHT_BONE
	bone = bone_tools.add_bone(armature,LEG_IK_ROOT_RIGHT_BONE,parent_bone=edit_bones[ROOT],head=edit_bones[ANKLE_RIGHT].head,tail=edit_bones[ANKLE_RIGHT].head)
	bone.head.z = edit_bones[ANKLE_RIGHT].head.z - TWO_THIRDS_LENGTH_OF_FOOT_BONE

	#LEG_IK_LEFT_BONE
	bone = bone_tools.add_bone(armature,LEG_IK_LEFT_BONE,parent_bone=edit_bones[LEG_IK_ROOT_LEFT_BONE],head=edit_bones[ANKLE_LEFT].head,tail=edit_bones[ANKLE_LEFT].head)
	bone.tail.y = edit_bones[ANKLE_LEFT].head.y + LENGTH_OF_FOOT_BONE

	#LEG_IK_RIGHT_BONE
	bone = bone_tools.add_bone(armature,LEG_IK_RIGHT_BONE,parent_bone=edit_bones[LEG_IK_ROOT_RIGHT_BONE],head=edit_bones[ANKLE_RIGHT].head,tail=edit_bones[ANKLE_RIGHT].head)
	bone.tail.y = edit_bones[ANKLE_RIGHT].head.y + LENGTH_OF_FOOT_BONE

	#TOE_IK_LEFT_BONE
	bone = bone_tools.add_bone(armature,TOE_IK_LEFT_BONE,parent_bone=edit_bones[LEG_IK_LEFT_BONE],head=edit_bones[TOE_LEFT].head,tail=edit_bones[TOE_LEFT].head)
	bone.tail.z = edit_bones[TOE_LEFT].head.z - HALF_LENGTH_OF_FOOT_BONE

	#TOE_IK_RIGHT_BONE
	bone = bone_tools.add_bone(armature,TOE_IK_RIGHT_BONE,parent_bone=edit_bones[LEG_IK_RIGHT_BONE],head=edit_bones[TOE_RIGHT].head,tail=edit_bones[TOE_RIGHT].head)
	bone.tail.z = edit_bones[TOE_RIGHT].head.z - HALF_LENGTH_OF_FOOT_BONE


def create_IK_constraints(KNEE_LEFT,LEG_IK_LEFT_BONE,KNEE_RIGHT,LEG_IK_RIGHT_BONE,ANKLE_LEFT,TOE_IK_LEFT_BONE,ANKLE_RIGHT,TOE_IK_RIGHT_BONE,KNEE2_LEFT,KNEE2_RIGHT):
		
	bpy.ops.object.mode_set(mode='POSE')
	pose_bones = bpy.context.object.pose.bones

	#LEFT KNEE
	bone_tools.create_ik_constraint(KNEE_LEFT, LEG_IK_LEFT_BONE, 2, True, 50, 0,180,0,0,0,0)
	if KNEE2_LEFT in [b.name for b in pose_bones]:
		pose_bones[KNEE_LEFT].constraints["IK"].iterations = 7
	bone_tools.create_MMD_limit_rotation_constraint(KNEE_LEFT,True,True,True,math.pi/360,math.pi,0,0,0,0,"LOCAL")

	#RIGHT KNEE
	bone_tools.create_ik_constraint(KNEE_RIGHT, LEG_IK_RIGHT_BONE, 2, True, 50, 0,180,0,0,0,0)
	if KNEE2_RIGHT in [b.name for b in pose_bones]:
		pose_bones[KNEE_RIGHT].constraints["IK"].iterations = 7
	bone_tools.create_MMD_limit_rotation_constraint(KNEE_RIGHT,True,True,True,math.pi/360,math.pi,0,0,0,0,"LOCAL")

	#j_asi_c_l
	if KNEE2_LEFT in [b.name for b in pose_bones]:
		bone_tools.create_ik_constraint(KNEE2_LEFT, LEG_IK_LEFT_BONE, 3, True, 48, 0,180,0,0,0,0)
		bone_tools.create_MMD_limit_rotation_constraint(KNEE2_LEFT,True,True,True,math.pi/360,math.pi,0,0,0,0,"LOCAL")

	#j_asi_c_r
	if KNEE2_RIGHT in [b.name for b in pose_bones]:
		bone_tools.create_ik_constraint(KNEE2_RIGHT, LEG_IK_RIGHT_BONE, 3, True, 48, 0,180,0,0,0,0)
		bone_tools.create_MMD_limit_rotation_constraint(KNEE2_RIGHT,True,True,True,math.pi/360,math.pi,0,0,0,0,"LOCAL")
	
	#ANKLE LEFT
	bone_tools.create_ik_constraint(ANKLE_LEFT, TOE_IK_LEFT_BONE, 1, True, 6, None, None, None, None, None, None)

	#ANKLE RIGHT
	bone_tools.create_ik_constraint(ANKLE_RIGHT, TOE_IK_RIGHT_BONE, 1, True, 6, None, None, None, None, None, None)

	if hasattr(bpy.context.object.pose.bones[KNEE_RIGHT], "mmd_bone"):
		pose_bones[KNEE_RIGHT].mmd_bone.ik_rotation_constraint = 2 # 180*2/math.pi
		pose_bones[KNEE_LEFT].mmd_bone.ik_rotation_constraint = 2 # 180*2/math.pi
		pose_bones[ANKLE_RIGHT].mmd_bone.ik_rotation_constraint = 4 #180*4/math.pi
		pose_bones[ANKLE_LEFT].mmd_bone.ik_rotation_constraint = 4 # 180*4/math.pi


def create_control_bones (armature,LEG_LEFT,LEG_RIGHT,KNEE_LEFT,KNEE_RIGHT,ANKLE_LEFT,ANKLE_RIGHT,TOE_LEFT,TOE_RIGHT,LOWER_BODY,LEG_LEFT_D,LEG_RIGHT_D,KNEE_LEFT_D,KNEE_RIGHT_D,ANKLE_LEFT_D,ANKLE_RIGHT_D,TOE_LEFT_EX,TOE_RIGHT_EX,KNEE2_LEFT,KNEE2_RIGHT,KNEE2_LEFT_D,KNEE2_RIGHT_D):

	#measurements of the length of the foot bone which will used to calculate the lengths of the IK bones.
	HALF_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length * 0.5
	QUARTER_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length * 0.25

	edit_bones = bpy.context.active_object.data.edit_bones

	bpy.ops.object.mode_set(mode='EDIT')

	#LEG_LEFT_D
	bone = bone_tools.add_bone(armature,LEG_LEFT_D,parent_bone=edit_bones[LOWER_BODY],head=edit_bones[LEG_LEFT].head,tail=edit_bones[LEG_LEFT].head)
	bone.tail.z = edit_bones[LEG_LEFT].head.z + HALF_LENGTH_OF_FOOT_BONE

	#LEG_RIGHT_D
	bone = bone_tools.add_bone(armature,LEG_RIGHT_D,parent_bone=edit_bones[LOWER_BODY],head=edit_bones[LEG_RIGHT].head,tail=edit_bones[LEG_RIGHT].head)
	bone.tail.z = edit_bones[LEG_RIGHT].head.z + HALF_LENGTH_OF_FOOT_BONE

	#KNEE_LEFT_D
	bone = bone_tools.add_bone(armature,KNEE_LEFT_D,parent_bone=edit_bones[LEG_LEFT_D],head=edit_bones[KNEE_LEFT].head,tail=edit_bones[KNEE_LEFT].head)
	bone.tail.z = edit_bones[KNEE_LEFT].head.z + HALF_LENGTH_OF_FOOT_BONE

	#KNEE_RIGHT_D
	bone = bone_tools.add_bone(armature,KNEE_RIGHT_D,parent_bone=edit_bones[LEG_RIGHT_D],head=edit_bones[KNEE_RIGHT].head,tail=edit_bones[KNEE_RIGHT].head)
	bone.tail.z = edit_bones[KNEE_RIGHT].head.z + HALF_LENGTH_OF_FOOT_BONE

	#j_asi_c_l_D
	if KNEE2_LEFT in [b.name for b in edit_bones]:
		bone = bone_tools.add_bone(armature,KNEE2_LEFT_D,parent_bone=edit_bones[KNEE_LEFT_D],head=edit_bones[KNEE2_LEFT].head,tail=edit_bones[KNEE2_LEFT].head)
		bone.tail.z = edit_bones[KNEE2_LEFT].head.z + HALF_LENGTH_OF_FOOT_BONE

	#j_asi_c_r_D
	if KNEE2_RIGHT in [b.name for b in edit_bones]:
		bone = bone_tools.add_bone(armature,KNEE2_RIGHT_D,parent_bone=edit_bones[KNEE_RIGHT_D],head=edit_bones[KNEE2_RIGHT].head,tail=edit_bones[KNEE2_RIGHT].head)
		bone.tail.z = edit_bones[KNEE2_RIGHT].head.z + HALF_LENGTH_OF_FOOT_BONE

	#ANKLE_LEFT_D
	bone = bone_tools.add_bone(armature,ANKLE_LEFT_D,parent_bone=edit_bones[KNEE_LEFT_D],head=edit_bones[ANKLE_LEFT].head,tail=edit_bones[ANKLE_LEFT].head)
	bone.tail.z = edit_bones[ANKLE_LEFT].head.z + HALF_LENGTH_OF_FOOT_BONE
	if KNEE2_LEFT in [b.name for b in edit_bones]:
		bone.parent = edit_bones[KNEE2_LEFT_D]

	#ANKLE_RIGHT_D
	bone = bone_tools.add_bone(armature,ANKLE_RIGHT_D,parent_bone=edit_bones[KNEE_RIGHT_D],head=edit_bones[ANKLE_RIGHT].head,tail=edit_bones[ANKLE_RIGHT].head)
	bone.tail.z = edit_bones[ANKLE_RIGHT].head.z + HALF_LENGTH_OF_FOOT_BONE
	if KNEE2_RIGHT in [b.name for b in edit_bones]:
		bone.parent = edit_bones[KNEE2_RIGHT_D]
	
	#TOE_LEFT_EX
	bone = bone_tools.add_bone(armature,TOE_LEFT_EX,parent_bone=edit_bones[ANKLE_LEFT_D],head=edit_bones[TOE_LEFT].head,tail=edit_bones[TOE_LEFT].tail)
	bone.head.z = bone.head.z + QUARTER_LENGTH_OF_FOOT_BONE
	bone.tail.z = bone.tail.z + QUARTER_LENGTH_OF_FOOT_BONE
	bone.head.y = bone.head.y + QUARTER_LENGTH_OF_FOOT_BONE
	bone.tail.y = bone.tail.y + QUARTER_LENGTH_OF_FOOT_BONE

	#TOE_RIGHT_EX
	bone = bone_tools.add_bone(armature,TOE_RIGHT_EX,parent_bone=edit_bones[ANKLE_RIGHT_D],head=edit_bones[TOE_RIGHT].head,tail=edit_bones[TOE_RIGHT].tail)
	bone.head.z = bone.head.z + QUARTER_LENGTH_OF_FOOT_BONE
	bone.tail.z = bone.tail.z + QUARTER_LENGTH_OF_FOOT_BONE
	bone.head.y = bone.head.y + QUARTER_LENGTH_OF_FOOT_BONE
	bone.tail.y = bone.tail.y + QUARTER_LENGTH_OF_FOOT_BONE

	#transfer weight to D and EX bones
	bone_tools.transfer_vertex_groups(get_armature(),LEG_LEFT,LEG_LEFT_D)
	bone_tools.transfer_vertex_groups(get_armature(),LEG_RIGHT,LEG_RIGHT_D)
	bone_tools.transfer_vertex_groups(get_armature(),KNEE_LEFT,KNEE_LEFT_D)
	bone_tools.transfer_vertex_groups(get_armature(),KNEE_RIGHT,KNEE_RIGHT_D)
	if KNEE2_LEFT in [b.name for b in bpy.context.object.pose.bones]:
		bone_tools.transfer_vertex_groups(get_armature(),KNEE2_LEFT,KNEE2_LEFT_D)
	if KNEE2_RIGHT in [b.name for b in bpy.context.object.pose.bones]:
		bone_tools.transfer_vertex_groups(get_armature(),KNEE2_RIGHT,KNEE2_RIGHT_D)
	bone_tools.transfer_vertex_groups(get_armature(),ANKLE_LEFT,ANKLE_LEFT_D)
	bone_tools.transfer_vertex_groups(get_armature(),ANKLE_RIGHT,ANKLE_RIGHT_D)
	bone_tools.transfer_vertex_groups(get_armature(),TOE_LEFT,TOE_LEFT_EX)
	bone_tools.transfer_vertex_groups(get_armature(),TOE_RIGHT,TOE_RIGHT_EX)

	#apply_additional_MMD_rotation
	bone_tools.apply_MMD_additional_rotation(get_armature(),LEG_LEFT,LEG_LEFT_D,1)
	bone_tools.apply_MMD_additional_rotation(get_armature(),LEG_RIGHT,LEG_RIGHT_D,1)
	bone_tools.apply_MMD_additional_rotation(get_armature(),KNEE_LEFT,KNEE_LEFT_D,1)
	bone_tools.apply_MMD_additional_rotation(get_armature(),KNEE_RIGHT,KNEE_RIGHT_D,1)
	if KNEE2_LEFT in [b.name for b in bpy.context.object.pose.bones]:
		bone_tools.apply_MMD_additional_rotation(get_armature(),KNEE2_LEFT,KNEE2_LEFT_D,1)
	if KNEE2_RIGHT in [b.name for b in bpy.context.object.pose.bones]:
		bone_tools.apply_MMD_additional_rotation(get_armature(),KNEE2_RIGHT,KNEE2_RIGHT_D,1)
	bone_tools.apply_MMD_additional_rotation(get_armature(),ANKLE_LEFT,ANKLE_LEFT_D,1)
	bone_tools.apply_MMD_additional_rotation(get_armature(),ANKLE_RIGHT,ANKLE_RIGHT_D,1)
	bone_tools.apply_MMD_additional_rotation(get_armature(),TOE_LEFT,TOE_LEFT_EX,1)
	bone_tools.apply_MMD_additional_rotation(get_armature(),TOE_RIGHT,TOE_RIGHT_EX,1)


def create_IK_bone_group(LEG_IK_ROOT_LEFT_BONE,LEG_IK_ROOT_RIGHT_BONE,LEG_IK_LEFT_BONE,LEG_IK_RIGHT_BONE,TOE_IK_LEFT_BONE,TOE_IK_RIGHT_BONE):

	pose = bpy.context.active_object.pose

	#create an 'IK' bone group and add the IK bones to it
	if 'IK' not in pose.bone_groups.keys():
		pose.bone_groups.new(name="IK")

	pose.bones[LEG_IK_ROOT_LEFT_BONE].bone_group = pose.bone_groups['IK']
	pose.bones[LEG_IK_ROOT_RIGHT_BONE].bone_group = pose.bone_groups['IK']
	pose.bones[LEG_IK_LEFT_BONE].bone_group = pose.bone_groups['IK']
	pose.bones[LEG_IK_RIGHT_BONE].bone_group = pose.bone_groups['IK']
	pose.bones[TOE_IK_LEFT_BONE].bone_group = pose.bone_groups['IK']
	pose.bones[TOE_IK_RIGHT_BONE].bone_group = pose.bone_groups['IK']

	print('added bones to IK bone group')


def get_armature():
	
	if bpy.context.selected_objects[0].type == 'ARMATURE':
		return model.findArmature(bpy.context.selected_objects[0])
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

@register_wrap
class Add_MMD_foot_leg_IK(bpy.types.Operator):
	"""Add foot and leg IK bones and constraints to MMD model"""
	bl_idname = "ffxiv_mmd_tools_helper.add_foot_leg_ik"
	bl_label = "Add foot leg IK to MMD model"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		clear_IK(context)
		main(context)
		return {'FINISHED'}