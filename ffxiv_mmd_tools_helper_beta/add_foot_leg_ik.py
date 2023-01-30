import bpy
import math

from . import register_wrap
from . import model
from mmd_tools.core.bone import FnBone

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

@register_wrap
class Add_MMD_foot_leg_IK_Panel(bpy.types.Panel):
	"""Add foot and leg IK bones and constraints to MMD model"""
	bl_idname = "OBJECT_PT_mmd_add_foot_leg_ik"
	bl_label = "Add foot leg IK to MMD model"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="Add leg and foot IK to MMD model", icon="ARMATURE_DATA")
		row = layout.row()
		row.operator("object.add_foot_leg_ik", text = "Add leg and foot IK to MMD model")
		row = layout.row()
		row = layout.row()

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
		bpy.context.active_object.data.edit_bones.remove(bpy.context.active_object.data.edit_bones[b])
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
	TWENTIETH_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length * 0.05
	FOURTIETH_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length * 0.025


	#The IK bones are created
	bpy.ops.object.mode_set(mode='EDIT')

	bone = bpy.context.active_object.data.edit_bones.new(LEG_IK_ROOT_LEFT_BONE)
	bone.head = bpy.context.active_object.data.edit_bones[ANKLE_LEFT].head
	bone.tail = bpy.context.active_object.data.edit_bones[ANKLE_LEFT].head
	bone.head.z = bpy.context.active_object.data.edit_bones[ANKLE_LEFT].head.z - TWO_THIRDS_LENGTH_OF_FOOT_BONE 
	if ROOT in bpy.context.active_object.data.edit_bones.keys():
		print(ROOT, ROOT in bpy.context.active_object.data.edit_bones.keys())
		bone.parent = bpy.context.active_object.data.edit_bones[ROOT]
		print(bone, bone.parent)

		bone = bpy.context.active_object.data.edit_bones.new(LEG_IK_ROOT_RIGHT_BONE)
	bone.head = bpy.context.active_object.data.edit_bones[ANKLE_RIGHT].head
	bone.tail = bpy.context.active_object.data.edit_bones[ANKLE_RIGHT].head
	bone.head.z = bpy.context.active_object.data.edit_bones[ANKLE_RIGHT].head.z - TWO_THIRDS_LENGTH_OF_FOOT_BONE
	if ROOT in bpy.context.active_object.data.edit_bones.keys():
		print(ROOT, ROOT in bpy.context.active_object.data.edit_bones.keys())
		bone.parent = bpy.context.active_object.data.edit_bones[ROOT]
		print(bone, bone.parent)


	bone = bpy.context.active_object.data.edit_bones.new(LEG_IK_LEFT_BONE)
	bone.head = bpy.context.active_object.data.edit_bones[ANKLE_LEFT].head
	bone.tail = bpy.context.active_object.data.edit_bones[ANKLE_LEFT].head
	bone.tail.y = bpy.context.active_object.data.edit_bones[ANKLE_LEFT].head.y + LENGTH_OF_FOOT_BONE
	if ROOT in bpy.context.active_object.data.edit_bones.keys():
		print(ROOT, ROOT in bpy.context.active_object.data.edit_bones.keys())
		bone.parent = bpy.context.active_object.data.edit_bones[LEG_IK_ROOT_LEFT_BONE]
		print(bone, bone.parent)


	bone = bpy.context.active_object.data.edit_bones.new(LEG_IK_RIGHT_BONE)
	bone.head = bpy.context.active_object.data.edit_bones[ANKLE_RIGHT].head
	bone.tail = bpy.context.active_object.data.edit_bones[ANKLE_RIGHT].head
	bone.tail.y = bpy.context.active_object.data.edit_bones[ANKLE_RIGHT].head.y + LENGTH_OF_FOOT_BONE
	if ROOT in bpy.context.active_object.data.edit_bones.keys():
		print(ROOT, ROOT in bpy.context.active_object.data.edit_bones.keys())
		bone.parent = bpy.context.active_object.data.edit_bones[LEG_IK_ROOT_RIGHT_BONE]
		print(bone, bone.parent)


	bone = bpy.context.active_object.data.edit_bones.new(TOE_IK_LEFT_BONE)
	bone.head = bpy.context.active_object.data.edit_bones[TOE_LEFT].head
	bone.tail = bpy.context.active_object.data.edit_bones[TOE_LEFT].head
	bone.tail.z = bpy.context.active_object.data.edit_bones[TOE_LEFT].head.z - HALF_LENGTH_OF_FOOT_BONE
	print('bone = ', bone)
	bone.parent = bpy.context.active_object.data.edit_bones[LEG_IK_LEFT_BONE]
	bone.use_connect = False

	bone = bpy.context.active_object.data.edit_bones.new(TOE_IK_RIGHT_BONE)
	bone.head = bpy.context.active_object.data.edit_bones[TOE_RIGHT].head
	bone.tail = bpy.context.active_object.data.edit_bones[TOE_RIGHT].head
	bone.tail.z = bpy.context.active_object.data.edit_bones[TOE_RIGHT].head.z - HALF_LENGTH_OF_FOOT_BONE
	bone.parent = bpy.context.active_object.data.edit_bones[LEG_IK_RIGHT_BONE]
	bone.use_connect = False

	
	#The D bones are created
	########## START D BONE CREATION HERE #######
	bpy.ops.object.mode_set(mode='EDIT')
	bone = bpy.context.active_object.data.edit_bones.new(LEG_LEFT_D)
	bone.head = bpy.context.active_object.data.edit_bones[LEG_LEFT].head
	bone.tail = bpy.context.active_object.data.edit_bones[LEG_LEFT].head
	bone.tail.z = bpy.context.active_object.data.edit_bones[LEG_LEFT].head.z + HALF_LENGTH_OF_FOOT_BONE
	print('bone = ', bone)
	bone.parent = bpy.context.active_object.data.edit_bones[LOWER_BODY]
	bone.use_connect = False
	
	bone = bpy.context.active_object.data.edit_bones.new(LEG_RIGHT_D)
	bone.head = bpy.context.active_object.data.edit_bones[LEG_RIGHT].head
	bone.tail = bpy.context.active_object.data.edit_bones[LEG_RIGHT].head
	bone.tail.z = bpy.context.active_object.data.edit_bones[LEG_RIGHT].head.z + HALF_LENGTH_OF_FOOT_BONE
	print('bone = ', bone)
	bone.parent = bpy.context.active_object.data.edit_bones[LOWER_BODY]
	bone.use_connect = False
	
	bone = bpy.context.active_object.data.edit_bones.new(KNEE_LEFT_D)
	bone.head = bpy.context.active_object.data.edit_bones[KNEE_LEFT].head
	bone.tail = bpy.context.active_object.data.edit_bones[KNEE_LEFT].head
	bone.tail.z = bpy.context.active_object.data.edit_bones[KNEE_LEFT].head.z + HALF_LENGTH_OF_FOOT_BONE
	print('bone = ', bone)
	bone.parent = bpy.context.active_object.data.edit_bones[LEG_LEFT_D]
	bone.use_connect = False
	
	bone = bpy.context.active_object.data.edit_bones.new(KNEE_RIGHT_D)
	bone.head = bpy.context.active_object.data.edit_bones[KNEE_RIGHT].head
	bone.tail = bpy.context.active_object.data.edit_bones[KNEE_RIGHT].head
	bone.tail.z = bpy.context.active_object.data.edit_bones[KNEE_RIGHT].head.z + HALF_LENGTH_OF_FOOT_BONE
	print('bone = ', bone)
	bone.parent = bpy.context.active_object.data.edit_bones[LEG_RIGHT_D]
	bone.use_connect = False

	if 'j_asi_c_l' in [b.name for b in bpy.context.active_object.data.edit_bones]:
		bone = bpy.context.active_object.data.edit_bones.new('j_asi_c_l_d')
		bone.head = bpy.context.active_object.data.edit_bones['j_asi_c_l'].head
		bone.tail = bpy.context.active_object.data.edit_bones['j_asi_c_l'].head
		bone.tail.z = bpy.context.active_object.data.edit_bones['j_asi_c_l'].head.z + HALF_LENGTH_OF_FOOT_BONE
		print('bone = ', bone)
		bone.parent = bpy.context.active_object.data.edit_bones[KNEE_LEFT_D]
		bone.use_connect = False

	if 'j_asi_c_r' in [b.name for b in bpy.context.active_object.data.edit_bones]:
		bone = bpy.context.active_object.data.edit_bones.new('j_asi_c_r_d')
		bone.head = bpy.context.active_object.data.edit_bones['j_asi_c_r'].head
		bone.tail = bpy.context.active_object.data.edit_bones['j_asi_c_r'].head
		bone.tail.z = bpy.context.active_object.data.edit_bones['j_asi_c_r'].head.z + HALF_LENGTH_OF_FOOT_BONE
		print('bone = ', bone)
		bone.parent = bpy.context.active_object.data.edit_bones[KNEE_RIGHT_D]
		bone.use_connect = False

	bone = bpy.context.active_object.data.edit_bones.new(ANKLE_LEFT_D)
	bone.head = bpy.context.active_object.data.edit_bones[ANKLE_LEFT].head
	bone.tail = bpy.context.active_object.data.edit_bones[ANKLE_LEFT].head
	bone.tail.z = bpy.context.active_object.data.edit_bones[ANKLE_LEFT].head.z + HALF_LENGTH_OF_FOOT_BONE
	print('bone = ', bone)

	if 'j_asi_c_l' in [b.name for b in bpy.context.active_object.data.edit_bones]:
		bone.parent = bpy.context.active_object.data.edit_bones['j_asi_c_l_d']
	else:
		bone.parent = bpy.context.active_object.data.edit_bones[KNEE_LEFT_D]
	bone.use_connect = False
	
	bone = bpy.context.active_object.data.edit_bones.new(ANKLE_RIGHT_D)
	bone.head = bpy.context.active_object.data.edit_bones[ANKLE_RIGHT].head
	bone.tail = bpy.context.active_object.data.edit_bones[ANKLE_RIGHT].head
	bone.tail.z = bpy.context.active_object.data.edit_bones[ANKLE_RIGHT].head.z + HALF_LENGTH_OF_FOOT_BONE
	print('bone = ', bone)

	if 'j_asi_c_r' in [b.name for b in bpy.context.active_object.data.edit_bones]:
		bone.parent = bpy.context.active_object.data.edit_bones['j_asi_c_r_d']
	else:
		bone.parent = bpy.context.active_object.data.edit_bones[KNEE_RIGHT_D]
	bone.use_connect = False
	
	
	bone = bpy.context.active_object.data.edit_bones.new(TOE_LEFT_EX)
	bone.head = bpy.context.active_object.data.edit_bones[TOE_LEFT].head
	bone.tail = bpy.context.active_object.data.edit_bones[TOE_LEFT].tail
	bone.head.z = bone.head.z + QUARTER_LENGTH_OF_FOOT_BONE
	bone.tail.z = bone.tail.z + QUARTER_LENGTH_OF_FOOT_BONE
	bone.head.y = bone.head.y + QUARTER_LENGTH_OF_FOOT_BONE
	bone.tail.y = bone.tail.y + QUARTER_LENGTH_OF_FOOT_BONE
	bone.parent = bpy.context.active_object.data.edit_bones[ANKLE_LEFT_D]
	bone.use_connect = False

	bone = bpy.context.active_object.data.edit_bones.new(TOE_RIGHT_EX)
	bone.head = bpy.context.active_object.data.edit_bones[TOE_RIGHT].head
	bone.tail = bpy.context.active_object.data.edit_bones[TOE_RIGHT].tail
	bone.head.z = bone.head.z + QUARTER_LENGTH_OF_FOOT_BONE
	bone.tail.z = bone.tail.z + QUARTER_LENGTH_OF_FOOT_BONE
	bone.head.y = bone.head.y + QUARTER_LENGTH_OF_FOOT_BONE
	bone.tail.y = bone.tail.y + QUARTER_LENGTH_OF_FOOT_BONE
	bone.parent = bpy.context.active_object.data.edit_bones[ANKLE_RIGHT_D]
	bone.use_connect = False


	"""
	bpy.ops.object.mode_set(mode='POSE')
	#if "toe IK_L_t" in bpy.context.active_object.pose.bones.keys():
	#bpy.context.active_object.pose.bones[TOE_LEFT_EX].bone.hide = True
	if hasattr(bpy.context.active_object.pose.bones[TOE_LEFT_EX], "mmd_bone"):
		bpy.context.active_object.pose.bones[TOE_LEFT_EX].mmd_bone.is_visible = False
		bpy.context.active_object.pose.bones[TOE_LEFT_EX].mmd_bone.is_controllable = False
		bpy.context.active_object.pose.bones[TOE_LEFT_EX].mmd_bone.is_tip = True
	bpy.ops.object.mode_set(mode='EDIT')

	bone = bpy.context.active_object.data.edit_bones.new(TOE_RIGHT_EX)
	bone.head = bpy.context.active_object.data.edit_bones[TOE_RIGHT].head
	bone.tail = bpy.context.active_object.data.edit_bones[TOE_RIGHT].tail
	bone.head.z = bone.head.z + QUARTER_LENGTH_OF_FOOT_BONE
	bone.tail.z = bone.tail.z + QUARTER_LENGTH_OF_FOOT_BONE
	bone.head.y = bone.head.y + QUARTER_LENGTH_OF_FOOT_BONE
	bone.tail.y = bone.tail.y + QUARTER_LENGTH_OF_FOOT_BONE
	bone.parent = bpy.context.active_object.data.edit_bones[ANKLE_RIGHT_D]
	bone.use_connect = False
	bpy.ops.object.mode_set(mode='POSE')
	#if "toe IK_R_t" in bpy.context.active_object.pose.bones.keys():
	#bpy.context.active_object.pose.bones[TOE_IK_RIGHT_BONE_TIP].bone.hide = True
	if hasattr(bpy.context.active_object.pose.bones[TOE_RIGHT_EX], "mmd_bone"):
		bpy.context.active_object.pose.bones[TOE_RIGHT_EX].mmd_bone.is_visible = False
		bpy.context.active_object.pose.bones[TOE_RIGHT_EX].mmd_bone.is_controllable = False
		bpy.context.active_object.pose.bones[TOE_RIGHT_EX].mmd_bone.is_tip = True
	bpy.ops.object.mode_set(mode='EDIT')

	"""

	#transfer weight to D and EX bones
	transfer_vertex_groups(get_armature(),LEG_LEFT,LEG_LEFT_D)
	transfer_vertex_groups(get_armature(),LEG_RIGHT,LEG_RIGHT_D)
	transfer_vertex_groups(get_armature(),KNEE_LEFT,KNEE_LEFT_D)
	transfer_vertex_groups(get_armature(),KNEE_RIGHT,KNEE_RIGHT_D)
	if 'j_asi_c_l' in [b.name for b in bpy.context.object.pose.bones]:
		transfer_vertex_groups(get_armature(),'j_asi_c_l','j_asi_c_l_d')
	if 'j_asi_c_r' in [b.name for b in bpy.context.object.pose.bones]:
		transfer_vertex_groups(get_armature(),'j_asi_c_r','j_asi_c_r_d')
	transfer_vertex_groups(get_armature(),ANKLE_LEFT,ANKLE_LEFT_D)
	transfer_vertex_groups(get_armature(),ANKLE_RIGHT,ANKLE_RIGHT_D)
	transfer_vertex_groups(get_armature(),TOE_LEFT,TOE_LEFT_EX)
	transfer_vertex_groups(get_armature(),TOE_RIGHT,TOE_RIGHT_EX)

	#apply_additional_MMD_rotation
	apply_MMD_additional_rotation(get_armature(),LEG_LEFT,LEG_LEFT_D)
	apply_MMD_additional_rotation(get_armature(),LEG_RIGHT,LEG_RIGHT_D)
	apply_MMD_additional_rotation(get_armature(),KNEE_LEFT,KNEE_LEFT_D)
	apply_MMD_additional_rotation(get_armature(),KNEE_RIGHT,KNEE_RIGHT_D)
	if 'j_asi_c_l' in [b.name for b in bpy.context.object.pose.bones]:
		apply_MMD_additional_rotation(get_armature(),'j_asi_c_l','j_asi_c_l_d')
	if 'j_asi_c_r' in [b.name for b in bpy.context.object.pose.bones]:
		apply_MMD_additional_rotation(get_armature(),'j_asi_c_r','j_asi_c_r_d')
	apply_MMD_additional_rotation(get_armature(),ANKLE_LEFT,ANKLE_LEFT_D)
	apply_MMD_additional_rotation(get_armature(),ANKLE_RIGHT,ANKLE_RIGHT_D)
	apply_MMD_additional_rotation(get_armature(),TOE_LEFT,TOE_LEFT_EX)
	apply_MMD_additional_rotation(get_armature(),TOE_RIGHT,TOE_RIGHT_EX)

	########## END D BONE CREATION HERE #######

	bpy.ops.object.mode_set(mode='POSE')

	#Adds IK constraints

	#LEFT KNEE
	bpy.context.object.pose.bones[KNEE_LEFT].constraints.new("IK")
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["IK"].target = bpy.context.active_object
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["IK"].subtarget = LEG_IK_LEFT_BONE
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["IK"].chain_count = 2
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["IK"].use_tail = True
	if 'j_asi_c_l' in [b.name for b in bpy.context.object.pose.bones]:
		bpy.context.object.pose.bones[KNEE_LEFT].constraints["IK"].iterations = 7
	else:
		bpy.context.object.pose.bones[KNEE_LEFT].constraints["IK"].iterations = 50
	bpy.context.object.pose.bones[KNEE_LEFT].ik_min_x = 0
	bpy.context.object.pose.bones[KNEE_LEFT].ik_max_x = 180
	bpy.context.object.pose.bones[KNEE_LEFT].ik_min_y = 0
	bpy.context.object.pose.bones[KNEE_LEFT].ik_max_y = 0
	bpy.context.object.pose.bones[KNEE_LEFT].ik_min_z = 0
	bpy.context.object.pose.bones[KNEE_LEFT].ik_max_z = 0


	bpy.context.object.pose.bones[KNEE_LEFT].constraints.new("LIMIT_ROTATION")
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].use_limit_x = True
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].use_limit_y = True
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].use_limit_z = True
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].min_x = math.pi/360 #radians = 0.5 degrees
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].max_x = math.pi #radians = 180 degrees

	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].min_y = 0
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].max_y = 0
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].min_z = 0
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].max_z = 0

	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].owner_space = "LOCAL"
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].name = "mmd_ik_limit_override"

	#RIGHT KNEE
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints.new("IK")
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["IK"].target = bpy.context.active_object
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["IK"].subtarget = LEG_IK_RIGHT_BONE
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["IK"].chain_count = 2
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["IK"].use_tail = True
	if 'j_asi_c_r' in [b.name for b in bpy.context.object.pose.bones]:
		bpy.context.object.pose.bones[KNEE_RIGHT].constraints["IK"].iterations = 7
	else:
		bpy.context.object.pose.bones[KNEE_LEFT].constraints["IK"].iterations = 50
	bpy.context.object.pose.bones[KNEE_RIGHT].ik_min_x = 0
	bpy.context.object.pose.bones[KNEE_RIGHT].ik_max_x = 180
	bpy.context.object.pose.bones[KNEE_RIGHT].ik_min_y = 0
	bpy.context.object.pose.bones[KNEE_RIGHT].ik_max_y = 0
	bpy.context.object.pose.bones[KNEE_RIGHT].ik_min_z = 0
	bpy.context.object.pose.bones[KNEE_RIGHT].ik_max_z = 0


	bpy.context.object.pose.bones[KNEE_RIGHT].constraints.new("LIMIT_ROTATION")
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].use_limit_x = True
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].use_limit_y = True
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].use_limit_z = True
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].min_x = math.pi/360 #radians = 0.5 degrees
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].max_x = math.pi #radians = 180 degrees
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].min_y = 0
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].max_y = 0
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].min_z = 0
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].max_z = 0
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].owner_space = "LOCAL"
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].name = "mmd_ik_limit_override"


	#j_asi_c_l
	if 'j_asi_c_l' in [b.name for b in bpy.context.object.pose.bones]:
		bpy.context.object.pose.bones['j_asi_c_l'].constraints.new("IK")
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["IK"].target = bpy.context.active_object
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["IK"].subtarget = LEG_IK_LEFT_BONE
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["IK"].chain_count = 3
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["IK"].use_tail = True
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["IK"].iterations = 48
		bpy.context.object.pose.bones['j_asi_c_l'].ik_min_x = 0
		bpy.context.object.pose.bones['j_asi_c_l'].ik_max_x = 180
		bpy.context.object.pose.bones['j_asi_c_l'].ik_min_y = 0
		bpy.context.object.pose.bones['j_asi_c_l'].ik_max_y = 0
		bpy.context.object.pose.bones['j_asi_c_l'].ik_min_z = 0
		bpy.context.object.pose.bones['j_asi_c_l'].ik_max_z = 0

		bpy.context.object.pose.bones['j_asi_c_l'].constraints.new("LIMIT_ROTATION")
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["Limit Rotation"].use_limit_x = True
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["Limit Rotation"].use_limit_y = True
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["Limit Rotation"].use_limit_z = True
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["Limit Rotation"].min_x = math.pi/360 #radians = 0.5 degrees
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["Limit Rotation"].max_x = math.pi #radians = 180 degrees
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["Limit Rotation"].min_y = 0
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["Limit Rotation"].max_y = 0
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["Limit Rotation"].min_z = 0
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["Limit Rotation"].max_z = 0
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["Limit Rotation"].owner_space = "LOCAL"
		bpy.context.object.pose.bones['j_asi_c_l'].constraints["Limit Rotation"].name = "mmd_ik_limit_override"


	#j_asi_c_r
	if 'j_asi_c_r' in [b.name for b in bpy.context.object.pose.bones]:
		bpy.context.object.pose.bones['j_asi_c_r'].constraints.new("IK")
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["IK"].target = bpy.context.active_object
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["IK"].subtarget = LEG_IK_RIGHT_BONE
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["IK"].chain_count = 3
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["IK"].use_tail = True
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["IK"].iterations = 48
		bpy.context.object.pose.bones['j_asi_c_r'].ik_min_x = 0
		bpy.context.object.pose.bones['j_asi_c_r'].ik_max_x = 180
		bpy.context.object.pose.bones['j_asi_c_r'].ik_min_y = 0
		bpy.context.object.pose.bones['j_asi_c_r'].ik_max_y = 0
		bpy.context.object.pose.bones['j_asi_c_r'].ik_min_z = 0
		bpy.context.object.pose.bones['j_asi_c_r'].ik_max_z = 0


		bpy.context.object.pose.bones['j_asi_c_r'].constraints.new("LIMIT_ROTATION")
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["Limit Rotation"].use_limit_x = True
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["Limit Rotation"].use_limit_y = True
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["Limit Rotation"].use_limit_z = True
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["Limit Rotation"].min_x = math.pi/360 #radians = 0.5 degrees
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["Limit Rotation"].max_x = math.pi #radians = 180 degrees
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["Limit Rotation"].min_y = 0
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["Limit Rotation"].max_y = 0
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["Limit Rotation"].min_z = 0
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["Limit Rotation"].max_z = 0
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["Limit Rotation"].owner_space = "LOCAL"
		bpy.context.object.pose.bones['j_asi_c_r'].constraints["Limit Rotation"].name = "mmd_ik_limit_override"
	
	#ANKLE LEFT
	bpy.context.object.pose.bones[ANKLE_LEFT].constraints.new("IK")
	bpy.context.object.pose.bones[ANKLE_LEFT].constraints["IK"].target = bpy.context.active_object
	bpy.context.object.pose.bones[ANKLE_LEFT].constraints["IK"].subtarget = TOE_IK_LEFT_BONE
	bpy.context.object.pose.bones[ANKLE_LEFT].constraints["IK"].chain_count = 1
	bpy.context.object.pose.bones[ANKLE_LEFT].constraints["IK"].use_tail = True
	bpy.context.object.pose.bones[ANKLE_LEFT].constraints["IK"].iterations = 6

	# bpy.context.object.pose.bones[ANKLE_LEFT].constraints.new("DAMPED_TRACK")
	# bpy.context.object.pose.bones[ANKLE_LEFT].constraints["Damped Track"].target = bpy.context.active_object
	# bpy.context.object.pose.bones[ANKLE_LEFT].constraints["Damped Track"].subtarget = KNEE_LEFT
	# bpy.context.object.pose.bones[ANKLE_LEFT].constraints["Damped Track"].track_axis = 'TRACK_Y'
	# bpy.context.object.pose.bones[ANKLE_LEFT].constraints["Damped Track"].name = "mmd_ik_target_override"

	#ANKLE RIGHT
	bpy.context.object.pose.bones[ANKLE_RIGHT].constraints.new("IK")
	bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].target = bpy.context.active_object
	bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].subtarget = TOE_IK_RIGHT_BONE
	bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].chain_count = 1
	bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].use_tail = True
	bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].iterations = 6

	# bpy.context.object.pose.bones[ANKLE_RIGHT].constraints.new("DAMPED_TRACK")
	# bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["Damped Track"].target = bpy.context.active_object
	# bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["Damped Track"].subtarget = KNEE_LEFT
	# bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["Damped Track"].track_axis = 'TRACK_Y'
	# bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["Damped Track"].name = "mmd_ik_target_override"

	
	if hasattr(bpy.context.object.pose.bones[KNEE_RIGHT], "mmd_bone"):
		bpy.context.object.pose.bones[KNEE_RIGHT].mmd_bone.ik_rotation_constraint = 2 # 180*2/math.pi
		bpy.context.object.pose.bones[KNEE_LEFT].mmd_bone.ik_rotation_constraint = 2 # 180*2/math.pi
		bpy.context.object.pose.bones[ANKLE_RIGHT].mmd_bone.ik_rotation_constraint = 4 #180*4/math.pi
		bpy.context.object.pose.bones[ANKLE_LEFT].mmd_bone.ik_rotation_constraint = 4 # 180*4/math.pi

	"""
	#TOE LEFT
	bpy.context.object.pose.bones[TOE_LEFT].constraints.new("DAMPED_TRACK")
	bpy.context.object.pose.bones[TOE_LEFT].constraints["Damped Track"].target = bpy.context.active_object
	bpy.context.object.pose.bones[TOE_LEFT].constraints["Damped Track"].subtarget = ANKLE_LEFT
	bpy.context.object.pose.bones[TOE_LEFT].constraints["Damped Track"].track_axis = 'TRACK_Y'
	bpy.context.object.pose.bones[TOE_LEFT].constraints["Damped Track"].name = "mmd_ik_target_override"

	#TOE RIGHT
	bpy.context.object.pose.bones[TOE_RIGHT].constraints.new("DAMPED_TRACK")
	bpy.context.object.pose.bones[TOE_RIGHT].constraints["Damped Track"].target = bpy.context.active_object
	bpy.context.object.pose.bones[TOE_RIGHT].constraints["Damped Track"].subtarget = ANKLE_RIGHT
	bpy.context.object.pose.bones[TOE_RIGHT].constraints["Damped Track"].track_axis = 'TRACK_Y'
	bpy.context.object.pose.bones[TOE_RIGHT].constraints["Damped Track"].name = "mmd_ik_target_override"
	"""

	
	#create an 'IK' bone group and add the IK bones to it
	if 'IK' not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name="IK")

	bpy.context.active_object.pose.bones[LEG_IK_ROOT_LEFT_BONE].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[LEG_IK_ROOT_RIGHT_BONE].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[LEG_IK_LEFT_BONE].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[LEG_IK_RIGHT_BONE].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[TOE_IK_LEFT_BONE].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[TOE_IK_RIGHT_BONE].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	"""
	bpy.context.active_object.pose.bones[LEG_IK_LEFT_BONE_TIP].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[LEG_IK_RIGHT_BONE_TIP].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[TOE_IK_LEFT_BONE_TIP].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[TOE_IK_RIGHT_BONE_TIP].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	"""
	bpy.context.active_object.data.display_type = 'OCTAHEDRAL'


	bpy.context.active_object.data.display_type = 'OCTAHEDRAL'

def duplicate_bone(bone_name,prefix,parent_name):
	bpy.ops.object.mode_set(mode='EDIT')
	bone = bpy.context.active_object.data.bones[bone_name]
	print ("new bone name:"+prefix+bone.name)
	copy_bone = bpy.context.active_object.data.edit_bones.new(prefix+bone.name)
	copy_bone.parent = bpy.context.active_object.data.edit_bones[parent_name]
	return copy_bone


def transfer_vertex_groups(armature,source_bone, target_bone):
	bpy.ops.object.mode_set(mode='OBJECT')
	
	if armature and armature.type == 'ARMATURE':
		meshes = [obj for obj in bpy.data.objects if obj.type == 'MESH' and (obj.parent == armature or obj.parent.parent == armature) ]
		for mesh in meshes:
			for vg in mesh.vertex_groups:
				#print(vg.name)
				if vg.name == source_bone:
					vg.name = target_bone


def apply_MMD_additional_rotation (armature,additional_transform_bone, target_bone):

	pose_bone = armature.pose.bones[target_bone]
	pose_bone.mmd_bone.has_additional_rotation = True
	pose_bone.mmd_bone.additional_transform_bone = additional_transform_bone

	FnBone.apply_additional_transformation(armature)
	#FnBone.clean_additional_transformation(armature)
	
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
	bl_idname = "object.add_foot_leg_ik"
	bl_label = "Add foot leg IK to MMD model"

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		clear_IK(context)
		main(context)
		return {'FINISHED'}