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

	#test japanese or english ("leg_R", "右足"), ("leg_L", "左足"),
	english = ["knee_L", "knee_R", "ankle_L", "ankle_R", "toe_L", "toe_R"]
	japanese = ["左ひざ", "右ひざ", "左足首", "右足首", "左つま先", "右つま先"] 
	japanese_L_R = ["ひざ.L", "ひざ.R", "足首.L", "足首.R", "つま先.L", "つま先.R"]

	keys = bpy.context.active_object.data.bones.keys()

	english_bones = all([e in keys for e in english])
	japanese_bones = all([j in keys for j in japanese])
	japanese_bones_L_R = all([j in keys for j in japanese_L_R])

	print('english_bones =', english_bones)
	print('japanese_bones =', japanese_bones)
	print('japanese_bones_L_R =', japanese_bones_L_R)
	print('\n\n')

	assert(english_bones == True or japanese_bones == True or japanese_bones_L_R == True), "This is not an MMD armature. MMD bone names of knee, ankle and toe bones are required for this script to run."

	IK_BONE_NAMES = ["leg IK_L", "leg IK_R", "toe IK_L", "toe IK_R", "左足ＩＫ", "右足ＩＫ", "左つま先ＩＫ", "右つま先ＩＫ", "足ＩＫ.L", "足ＩＫ.R", "つま先ＩＫ.L", "つま先ＩＫ.R"]
	ik_bones = any([ik in keys for ik in IK_BONE_NAMES])

	assert(ik_bones == False), "This armature already has MMD IK bone names."


	if english_bones == True:
		LEG_IK_ROOT_LEFT_BONE = "leg IK_root_L"
		LEG_IK_ROOT_RIGHT_BONE = "leg IK_root_R"
		LEG_IK_LEFT_BONE = "leg IK_L"
		LEG_IK_RIGHT_BONE = "leg IK_R"
		TOE_IK_LEFT_BONE = "toe IK_L"
		TOE_IK_RIGHT_BONE = "toe IK_R"
		"""
		LEG_IK_LEFT_BONE_TIP = "leg IK_L_t"
		LEG_IK_RIGHT_BONE_TIP = "leg IK_R_t"
		TOE_IK_LEFT_BONE_TIP = "toe IK_L_t"
		TOE_IK_RIGHT_BONE_TIP = "toe IK_R_t"
		"""
		LEG_LEFT_D = "leg_L_D"
		LEG_RIGHT_D = "leg_R_D"
		KNEE_LEFT_D = "knee_L_D"
		KNEE_RIGHT_D = "knee_R_D"
		ANKLE_LEFT_D = "ankle_L_D"
		ANKLE_RIGHT_D = "ankle_R_D"
		TOE_LEFT_EX = "toe_L_EX"
		TOE_RIGHT_EX = "toe_R_EX"
		ROOT = "root"
		WAIST_CANCEL_L = "waist_cancel_L"
		WAIST_CANCEL_R = "waist_cancel_R"


	if japanese_bones == True or japanese_bones_L_R == True:
		LEG_IK_ROOT_LEFT_BONE = "左足IK親"
		LEG_IK_ROOT_RIGHT_BONE = "右足IK親"
		LEG_IK_LEFT_BONE = "左足ＩＫ"
		LEG_IK_RIGHT_BONE = "右足ＩＫ"
		TOE_IK_LEFT_BONE = "左つま先ＩＫ"
		TOE_IK_RIGHT_BONE = "右つま先ＩＫ"
		"""
		LEG_IK_LEFT_BONE_TIP = "左足ＩＫ先"
		LEG_IK_RIGHT_BONE_TIP = "右足ＩＫ先"
		TOE_IK_LEFT_BONE_TIP = "左つま先ＩＫ先"
		TOE_IK_RIGHT_BONE_TIP = "右つま先ＩＫ先"
		"""
		LEG_LEFT_D = "左足D"
		LEG_RIGHT_D = "右足D"
		KNEE_LEFT_D = "左ひざD"
		KNEE_RIGHT_D = "右ひざD"
		ANKLE_LEFT_D = "左足首D"
		ANKLE_RIGHT_D = "右足首D"
		TOE_LEFT_EX = "左足先EX"
		TOE_RIGHT_EX = "右足先EX"
		ROOT = "全ての親"
		WAIST_CANCEL_L = "左腰キャンセル"
		WAIST_CANCEL_R = "右腰キャンセル"

		#Lists of possible names of knee, ankle and toe bones
	LOWER_BODY_BONES = ["lower body"," 下半身"," 下半身"]
	LEG_LEFT_BONES = ["leg_L", "左足", "足.L"]
	LEG_RIGHT_BONES = ["leg_R", "右足", "足.R"]
	KNEE_LEFT_BONES = ["knee_L", "左ひざ", "ひざ.L" ]
	KNEE_RIGHT_BONES = ["knee_R", "右ひざ", "ひざ.R"]
	ANKLE_LEFT_BONES = ["ankle_L", "左足首", "足首.L"]
	ANKLE_RIGHT_BONES = ["ankle_R", "右足首", "足首.R"]
	TOE_LEFT_BONES = ["toe_L", "左つま先", "つま先.L"]
	TOE_RIGHT_BONES = ["toe_R", "右つま先", "つま先.R"]
	WAIST_CANCEL_L_BONES = ["waist_cancel_L","左腰キャンセル","腰キャンセル.L"]
	WAIST_CANCEL_R_BONES = ["waist_cancel_R","右腰キャンセル","腰キャンセル.R"]

	print('\n')
	#Searches through the bones of the active armature and finds the knee, ankle and toe bones.
	for b in bpy.context.active_object.data.bones:
		if b.name in LOWER_BODY_BONES:
			LOWER_BODY = b.name
			print('LOWER_BODY = ', LOWER_BODY)
		if b.name in LEG_LEFT_BONES:
			LEG_LEFT = b.name
			print('LEG_LEFT = ', LEG_LEFT)
		if b.name in LEG_RIGHT_BONES:
			LEG_RIGHT = b.name
			print('LEG_RIGHT = ', LEG_RIGHT)
		if b.name in KNEE_LEFT_BONES:
			KNEE_LEFT = b.name
			print('KNEE_LEFT = ', KNEE_LEFT)
		if b.name in KNEE_RIGHT_BONES:
			KNEE_RIGHT = b.name
			print('KNEE_RIGHT = ', KNEE_RIGHT)
		if b.name in ANKLE_LEFT_BONES:
			ANKLE_LEFT = b.name
			print('ANKLE_LEFT = ', ANKLE_LEFT)
		if b.name in ANKLE_RIGHT_BONES:
			ANKLE_RIGHT = b.name
			print('ANKLE_RIGHT = ', ANKLE_RIGHT)
		if b.name in TOE_LEFT_BONES:
			TOE_LEFT = b.name
			print('TOE_LEFT = ', TOE_LEFT)
		if b.name in TOE_RIGHT_BONES:
			TOE_RIGHT = b.name
			print('TOE_RIGHT = ', TOE_RIGHT)
		if b.name in WAIST_CANCEL_L_BONES:
			WAIST_CANCEL_L = b.name
			print('WAIST_CANCEL_L = ', WAIST_CANCEL_L)
		if b.name in WAIST_CANCEL_R_BONES:
			WAIST_CANCEL_R = b.name
			print('WAIST_CANCEL_R = ', WAIST_CANCEL_R)

	bpy.ops.object.mode_set(mode='POSE')
	bpy.context.active_object.pose.bones[KNEE_LEFT].use_ik_limit_x = True
	bpy.context.active_object.pose.bones[KNEE_RIGHT].use_ik_limit_x = True

	#measurements of the length of the foot bone which will used to calculate the lengths of the IK bones.
	LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length
	TWO_THIRDS_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length * 0.66
	HALF_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length * 0.5
	QUARTER_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length * 0.25

	#The IK bones are created
	bpy.ops.object.mode_set(mode='EDIT')

	edit_bones = bpy.context.active_object.data.edit_bones


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


	bpy.ops.object.mode_set(mode='POSE')

	#Adds IK constraints

	#LEFT KNEE
	create_ik_constraint(KNEE_LEFT, LEG_IK_LEFT_BONE, 2, True, 50, 0,180,0,0,0,0)
	if 'j_asi_c_r' in [b.name for b in bpy.context.object.pose.bones]:
		bpy.context.object.pose.bones[KNEE_LEFT].constraints["IK"].iterations = 7
	create_MMD_limit_rotation_constraint(KNEE_LEFT,True,True,True,math.pi/360,math.pi,0,0,0,0,"LOCAL")

	#RIGHT KNEE
	create_ik_constraint(KNEE_RIGHT, LEG_IK_RIGHT_BONE, 2, True, 50, 0,180,0,0,0,0)
	if 'j_asi_c_r' in [b.name for b in bpy.context.object.pose.bones]:
		bpy.context.object.pose.bones[KNEE_RIGHT].constraints["IK"].iterations = 7
	create_MMD_limit_rotation_constraint(KNEE_RIGHT,True,True,True,math.pi/360,math.pi,0,0,0,0,"LOCAL")


	#j_asi_c_l
	if 'j_asi_c_l' in [b.name for b in bpy.context.object.pose.bones]:
		create_ik_constraint('j_asi_c_l', LEG_IK_LEFT_BONE, 3, True, 48, 0,180,0,0,0,0)
		create_MMD_limit_rotation_constraint('j_asi_c_l',True,True,True,math.pi/360,math.pi,0,0,0,0,"LOCAL")


	#j_asi_c_r
	if 'j_asi_c_r' in [b.name for b in bpy.context.object.pose.bones]:
		create_ik_constraint('j_asi_c_r', LEG_IK_RIGHT_BONE, 3, True, 48, 0,180,0,0,0,0)
		create_MMD_limit_rotation_constraint('j_asi_c_r',True,True,True,math.pi/360,math.pi,0,0,0,0,"LOCAL")

	
	#ANKLE LEFT
	create_ik_constraint(ANKLE_LEFT, TOE_IK_LEFT_BONE, 1, True, 6, None, None, None, None, None, None)

	#ANKLE RIGHT
	create_ik_constraint(ANKLE_RIGHT, TOE_IK_RIGHT_BONE, 1, True, 6, None, None, None, None, None, None)

	
	if hasattr(bpy.context.object.pose.bones[KNEE_RIGHT], "mmd_bone"):
		bpy.context.object.pose.bones[KNEE_RIGHT].mmd_bone.ik_rotation_constraint = 2 # 180*2/math.pi
		bpy.context.object.pose.bones[KNEE_LEFT].mmd_bone.ik_rotation_constraint = 2 # 180*2/math.pi
		bpy.context.object.pose.bones[ANKLE_RIGHT].mmd_bone.ik_rotation_constraint = 4 #180*4/math.pi
		bpy.context.object.pose.bones[ANKLE_LEFT].mmd_bone.ik_rotation_constraint = 4 # 180*4/math.pi

	
	#create an 'IK' bone group and add the IK bones to it
	create_IK_bone_group(LEG_IK_ROOT_LEFT_BONE,LEG_IK_ROOT_RIGHT_BONE,LEG_IK_LEFT_BONE,LEG_IK_RIGHT_BONE,TOE_IK_LEFT_BONE,TOE_IK_RIGHT_BONE)


	bpy.context.active_object.data.display_type = 'OCTAHEDRAL'


	#The D bones are created
	########## START D BONE CREATION HERE #######
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
	if 'j_asi_c_l' in [b.name for b in edit_bones]:
		bone = bone_tools.add_bone(armature,'j_asi_c_l_D',parent_bone=edit_bones[KNEE_LEFT_D],head=edit_bones['j_asi_c_l'].head,tail=edit_bones['j_asi_c_l'].head)
		bone.tail.z = edit_bones['j_asi_c_l'].head.z + HALF_LENGTH_OF_FOOT_BONE

	#j_asi_c_r_D
	if 'j_asi_c_r' in [b.name for b in edit_bones]:
		bone = bone_tools.add_bone(armature,'j_asi_c_r_D',parent_bone=edit_bones[KNEE_RIGHT_D],head=edit_bones['j_asi_c_r'].head,tail=edit_bones['j_asi_c_r'].head)
		bone.tail.z = edit_bones['j_asi_c_r'].head.z + HALF_LENGTH_OF_FOOT_BONE

	#ANKLE_LEFT_D
	bone = bone_tools.add_bone(armature,ANKLE_LEFT_D,parent_bone=edit_bones[KNEE_LEFT_D],head=edit_bones[ANKLE_LEFT].head,tail=edit_bones[ANKLE_LEFT].head)
	bone.tail.z = edit_bones[ANKLE_LEFT].head.z + HALF_LENGTH_OF_FOOT_BONE
	if 'j_asi_c_l' in [b.name for b in edit_bones]:
		bone.parent = edit_bones['j_asi_c_l_D']

	#ANKLE_RIGHT_D
	bone = bone_tools.add_bone(armature,ANKLE_RIGHT_D,parent_bone=edit_bones[KNEE_RIGHT_D],head=edit_bones[ANKLE_RIGHT].head,tail=edit_bones[ANKLE_RIGHT].head)
	bone.tail.z = edit_bones[ANKLE_RIGHT].head.z + HALF_LENGTH_OF_FOOT_BONE
	if 'j_asi_c_r' in [b.name for b in edit_bones]:
		bone.parent = edit_bones['j_asi_c_r_D']
	
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
	transfer_vertex_groups(get_armature(),LEG_LEFT,LEG_LEFT_D)
	transfer_vertex_groups(get_armature(),LEG_RIGHT,LEG_RIGHT_D)
	transfer_vertex_groups(get_armature(),KNEE_LEFT,KNEE_LEFT_D)
	transfer_vertex_groups(get_armature(),KNEE_RIGHT,KNEE_RIGHT_D)
	if 'j_asi_c_l' in [b.name for b in bpy.context.object.pose.bones]:
		transfer_vertex_groups(get_armature(),'j_asi_c_l','j_asi_c_l_D')
	if 'j_asi_c_r' in [b.name for b in bpy.context.object.pose.bones]:
		transfer_vertex_groups(get_armature(),'j_asi_c_r','j_asi_c_r_D')
	transfer_vertex_groups(get_armature(),ANKLE_LEFT,ANKLE_LEFT_D)
	transfer_vertex_groups(get_armature(),ANKLE_RIGHT,ANKLE_RIGHT_D)
	transfer_vertex_groups(get_armature(),TOE_LEFT,TOE_LEFT_EX)
	transfer_vertex_groups(get_armature(),TOE_RIGHT,TOE_RIGHT_EX)

	#apply_additional_MMD_rotation
	apply_MMD_additional_rotation(get_armature(),LEG_LEFT,LEG_LEFT_D,1)
	apply_MMD_additional_rotation(get_armature(),LEG_RIGHT,LEG_RIGHT_D,1)
	apply_MMD_additional_rotation(get_armature(),KNEE_LEFT,KNEE_LEFT_D,1)
	apply_MMD_additional_rotation(get_armature(),KNEE_RIGHT,KNEE_RIGHT_D,1)
	if 'j_asi_c_l' in [b.name for b in bpy.context.object.pose.bones]:
		apply_MMD_additional_rotation(get_armature(),'j_asi_c_l','j_asi_c_l_D',1)
	if 'j_asi_c_r' in [b.name for b in bpy.context.object.pose.bones]:
		apply_MMD_additional_rotation(get_armature(),'j_asi_c_r','j_asi_c_r_D',1)
	apply_MMD_additional_rotation(get_armature(),ANKLE_LEFT,ANKLE_LEFT_D,1)
	apply_MMD_additional_rotation(get_armature(),ANKLE_RIGHT,ANKLE_RIGHT_D,1)
	apply_MMD_additional_rotation(get_armature(),TOE_LEFT,TOE_LEFT_EX,1)
	apply_MMD_additional_rotation(get_armature(),TOE_RIGHT,TOE_RIGHT_EX,1)

	########## END D BONE CREATION HERE #######

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



def create_ik_constraint(bone_name, subtarget, chain_count, use_tail, iterations, 
						ik_min_x=None, ik_max_x=None, ik_min_y=None, ik_max_y=None, ik_min_z=None, ik_max_z=None):

	bone = bpy.context.object.pose.bones[bone_name]

	bone.constraints.new("IK")
	bone.constraints["IK"].target = bpy.context.active_object
	bone.constraints["IK"].subtarget = subtarget
	bone.constraints["IK"].chain_count = chain_count
	bone.constraints["IK"].use_tail = use_tail
	bone.constraints["IK"].iterations = iterations

	if ik_min_x is not None:
		bone.ik_min_x = ik_min_x
	if ik_max_x is not None:
		bone.ik_max_x = ik_max_x
	if ik_min_y is not None:
		bone.ik_min_y = ik_min_y
	if ik_max_y is not None:
		bone.ik_max_y = ik_max_y
	if ik_min_z is not None:
		bone.ik_min_z = ik_min_z
	if ik_max_z is not None:
		bone.ik_max_z = ik_max_z


def create_MMD_limit_rotation_constraint(bone_name,use_limit_x,use_limit_y,use_limit_z,min_x,max_x,min_y,max_y,min_z,max_z,owner_space):

		bone = bpy.context.object.pose.bones[bone_name]
		bone.constraints.new("LIMIT_ROTATION")
		bone.constraints["Limit Rotation"].use_limit_x = use_limit_x
		bone.constraints["Limit Rotation"].use_limit_y = use_limit_y
		bone.constraints["Limit Rotation"].use_limit_z = use_limit_z
		bone.constraints["Limit Rotation"].min_x = min_x
		bone.constraints["Limit Rotation"].max_x = max_x
		bone.constraints["Limit Rotation"].min_y = min_y
		bone.constraints["Limit Rotation"].max_y = max_y
		bone.constraints["Limit Rotation"].min_z = min_z
		bone.constraints["Limit Rotation"].max_z = max_z
		bone.constraints["Limit Rotation"].owner_space = owner_space
		bone.constraints["Limit Rotation"].name = "mmd_ik_limit_override"

		#fixes axis issue on bone roll
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.context.active_object.data.edit_bones[bone_name].roll = 0
		bpy.ops.object.mode_set(mode='POSE')




def duplicate_bone(bone_name,prefix,parent_name):
	bpy.ops.object.mode_set(mode='EDIT')
	edit_bones = bpy.context.active_object.data.edit_bones

	bone = bpy.context.active_object.data.bones[bone_name]
	
	print ("new bone name:"+prefix+bone.name)
	copy_bone = edit_bones.new(prefix+bone.name)
	copy_bone.parent = edit_bones[parent_name]
	return copy_bone


def transfer_vertex_groups(armature,source_bone_name, target_bone_name):
	bpy.ops.object.mode_set(mode='OBJECT')
	
	if armature and armature.type == 'ARMATURE':
		meshes = [obj for obj in bpy.data.objects if obj.type == 'MESH' and (obj.parent == armature or obj.parent.parent == armature) ]
		for mesh in meshes:
			for vg in mesh.vertex_groups:
				#print(vg.name)
				if vg.name == source_bone_name:
					vg.name = target_bone_name
					print('transferred vertex groups for',mesh.name,'from',source_bone_name,'to',target_bone_name)


def apply_MMD_additional_rotation (armature,additional_transform_bone_name, target_bone_name,influence):

	pose_bone = armature.pose.bones[target_bone_name]
	pose_bone.mmd_bone.has_additional_rotation = True
	pose_bone.mmd_bone.additional_transform_bone = additional_transform_bone_name
	pose_bone.mmd_bone.additional_transform_influence = influence
	FnBone.apply_additional_transformation(armature)
	#FnBone.clean_additional_transformation(armature)
	print ('set additional rotation for',target_bone_name,'to',additional_transform_bone_name,'influence:',influence)
	
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