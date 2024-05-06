import bpy
from . import register_wrap
from . import model
from mmd_tools.core.bone import FnBone
from . import bone_tools


def armature_diagnostic():
	ENGLISH_ARM_BONES = ["elbow_L", "elbow_R", "wrist_L", "wrist_R", "middle1_L", "middle1_R"]
	JAPANESE_ARM_BONES = ["左ひじ", "右ひじ", "左手首", "右手首", "左中指１", "右中指１"]
	IK_BONE_NAMES = ["elbow IK_L", "elbow IK_R", "middle1 IK_L", "middle1 IK_R"]
	ENGLISH_OK = True
	JAPANESE_OK = True

	print('\n\n\n', 'These English bones are needed to add hand IK:', '\n')
	print(ENGLISH_ARM_BONES, '\n')
	for b in ENGLISH_ARM_BONES:
		if b not in bpy.context.active_object.data.bones.keys():
			ENGLISH_OK = False
			print('This bone is not in this armature:', '\n', b)
	if ENGLISH_OK == True:
		print('OK! All English-named bones are present which are needed to add hand IK')

	print('\n', 'OR These Japanese bones are needed to add IK:', '\n')
	print(JAPANESE_ARM_BONES, '\n')
	for b in JAPANESE_ARM_BONES:
		if b not in bpy.context.active_object.data.bones.keys():
			JAPANESE_OK = False
			print('This bone is not in this armature:', '\n', b)
	if JAPANESE_OK == True:
		print('OK! All Japanese-named bones are present which are needed to add hand IK', '\n')

	print('\n', 'hand IK bones which are already in the armature = ', '\n')
	for b in IK_BONE_NAMES:
		if b in bpy.context.active_object.data.bones.keys():
			print('This armature appears to already have hand IK bones. This bone seems to be a hand IK bone:', '\n', b)


def clear_IK(context):
	IK_target_bones = []
	IK_target_tip_bones = []
	armature = model.findArmature(bpy.context.active_object)
	bpy.context.view_layer.objects.active = armature
	bpy.ops.object.mode_set(mode='POSE')
	english = ["elbow_L", "elbow_R", "wrist_L", "wrist_R", "middle1_L", "middle1_R"]
	english_alt = ["LeftElbow", "RightElbow", "LeftWrist", "RightWrist", "LeftMiddleFinger1", "RightMiddleFinger1"]
	japanese = ["左ひじ", "右ひじ", "左手首", "右手首", "左中指１", "右中指１"]
	japanese_L_R = ["ひじ.L", "ひじ.R", "手首.L", "手首.R", "中指１.L", "中指１.R"]
	# IK_BONE_NAMES = ["elbow IK_L", "elbow IK_R", "middle1 IK_L", "middle1 IK_R"]
	arm_hand_bones = english + japanese + japanese_L_R + english_alt
	for b in bpy.context.active_object.pose.bones.keys():
		if b in arm_hand_bones:
			for c in armature.pose.bones[b].constraints:
				if c.type == "IK":
					print("c.target = ", c.target)
					if c.target == bpy.context.view_layer.objects.active:
						if c.subtarget is not None:
							print("c.subtarget = ", c.subtarget)
							if c.subtarget not in IK_target_bones:
								IK_target_bones.append(c.subtarget)
	for b in IK_target_bones:
		for c in armature.pose.bones[b].children:
			if c.name not in IK_target_tip_bones:
				IK_target_tip_bones.append(c.name)
	bones_to_be_deleted = set(IK_target_bones + IK_target_tip_bones)
	print("bones to be deleted = ", bones_to_be_deleted)
	bpy.ops.object.mode_set(mode='EDIT')
	for b in bones_to_be_deleted:
		bpy.context.active_object.data.edit_bones.remove(armature.data.edit_bones[b])
	bpy.ops.object.mode_set(mode='POSE')
	for b in bpy.context.active_object.pose.bones.keys():
		if b in arm_hand_bones:
			for c in armature.pose.bones[b].constraints:
				armature.pose.bones[b].constraints.remove(c)
	
	bpy.ops.object.mode_set(mode='OBJECT')


def main(context):

	bpy.context.view_layer.objects.active = get_armature()
	armature=get_armature()

	bone_type = bone_tools.get_primary_bonetype(armature)

	if bone_type not in ('mmd_english', 'mmd_english_alt','mmd_japanese', 'mmd_japaneseLR'):
		raise TypeError(f"Primary bone type detected '{bone_type}' is not recognized as an MMD bone type. Rename bones to one of the MMD types (English, EnglishAlt, Japanese, JapaneseLR) and then try again.")
	else:

		bpy.context.view_layer.objects.active = armature
		edit_bones = armature.data.edit_bones

		#Lists of possible names of elbow, wrist and middle1 bones
		SHOULDER_LEFT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,"shoulder_L")
		SHOULDER_RIGHT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,"shoulder_R")
		ARM_LEFT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,"elbow_L")
		ARM_RIGHT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature, "elbow_R")
		ELBOW_LEFT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature, "wrist_L")
		ELBOW_RIGHT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature, "wrist_R")
		WRIST_LEFT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature, "middle1_L")
		WRIST_RIGHT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature, "middle1_R")
		ROOT = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,'root')
		#SHOULDER_LEFT_D = "shoulder_L_D"
		#SHOULDER_RIGHT_D = "shoulder_R_D"
  		
		ELBOW_LEFT_IK = bone_tools.get_bone_name(bone_type,'elbow_IK_L')
		ELBOW_RIGHT_IK = bone_tools.get_bone_name(bone_type,'elbow_IK_R')
		FINGER_MIDDLE_LEFT_IK = bone_tools.get_bone_name(bone_type,'middle1_IK_L')
		FINGER_MIDDLE_RIGHT_IK = bone_tools.get_bone_name(bone_type,'middle1_IK_R')
		ELBOW_LEFT_IK_TIP = bone_tools.get_bone_name(bone_type,'elbow_IK_L_t')
		ELBOW_RIGHT_IK_TIP =  bone_tools.get_bone_name(bone_type,'elbow_IK_R_t')
		FINGER_MIDDLE_LEFT_IK_TIP = bone_tools.get_bone_name(bone_type,'middle1_IK_L_t')
		FINGER_MIDDLE_RIGHT_IK_TIP = bone_tools.get_bone_name(bone_type,'middle1_IK_R_t')


		#ARM_LEFT_D = bone_tools.get_bone_name(bone_type,"arm_L_D")
		#ARM_RIGHT_D = bone_tools.get_bone_name(bone_type,"arm_R_D")
		#ELBOW_LEFT_D = bone_tools.get_bone_name(bone_type,"elbow_L_D")
		#ELBOW_RIGHT_D = bone_tools.get_bone_name(bone_type,"elbow_R_D")
		#WRIST_LEFT_D = bone_tools.get_bone_name(bone_type,"wrist_L_D")
		#WRIST_RIGHT_D = bone_tools.get_bone_name(bone_type,"wrist_R_D")

	

		#measurements of the length of the elbow bone which will used to calculate the lengths of the IK bones.
		DOUBLE_LENGTH_OF_ELBOW_BONE = armature.data.bones.get(ELBOW_LEFT).length * 2
		TWENTIETH_LENGTH_OF_ELBOW_BONE = armature.data.bones.get(ELBOW_LEFT).length * 0.05
		QUARTER_LENGTH_OF_ELBOW_BONE = armature.data.bones.get(ELBOW_LEFT).length * 0.25

		bpy.ops.object.mode_set(mode='EDIT')


		# if ARM_LEFT == "左ひじ" or ARM_LEFT == "ひじ.L" or ARM_LEFT == "elbow_L":

		#The IK bones are created, with English bone names.
		bone = bone_tools.add_bone(armature,ELBOW_LEFT_IK,parent_bone=edit_bones[ROOT],head=edit_bones[ELBOW_LEFT].head,tail=edit_bones[ELBOW_LEFT].head)
		bone.tail.z = armature.data.edit_bones[ELBOW_LEFT].head.z - DOUBLE_LENGTH_OF_ELBOW_BONE

		bone = bone_tools.add_bone(armature,ELBOW_RIGHT_IK,parent_bone=edit_bones[ROOT],head=edit_bones[ELBOW_RIGHT].head,tail=edit_bones[ELBOW_RIGHT].head)
		bone.tail.z = armature.data.edit_bones[ELBOW_RIGHT].head.z - DOUBLE_LENGTH_OF_ELBOW_BONE

		bone = bone_tools.add_bone(armature,FINGER_MIDDLE_LEFT_IK,parent_bone=edit_bones[ELBOW_LEFT_IK],head=edit_bones[WRIST_LEFT].head,tail=edit_bones[WRIST_LEFT].head)
		bone.tail.z = armature.data.edit_bones[WRIST_LEFT].head.z - DOUBLE_LENGTH_OF_ELBOW_BONE
		bone.use_connect = False

		bone = bone_tools.add_bone(armature,FINGER_MIDDLE_RIGHT_IK,parent_bone=edit_bones[ELBOW_RIGHT_IK],head=edit_bones[WRIST_RIGHT].head,tail=edit_bones[WRIST_RIGHT].head)
		bone.tail.z = armature.data.edit_bones[WRIST_RIGHT].head.z - DOUBLE_LENGTH_OF_ELBOW_BONE
		bone.use_connect = False

		bone = bone_tools.add_bone(armature,ELBOW_LEFT_IK_TIP,parent_bone=edit_bones[ELBOW_LEFT_IK],head=edit_bones[ELBOW_LEFT_IK].head,tail=edit_bones[ELBOW_LEFT_IK].head)
		bone.tail.y = bone.tail.y + TWENTIETH_LENGTH_OF_ELBOW_BONE
		bone.use_connect = False
		bpy.ops.object.mode_set(mode='POSE')
		armature.pose.bones[ELBOW_LEFT_IK_TIP].bone.hide = True
		if hasattr(armature.pose.bones[ELBOW_LEFT_IK_TIP], "mmd_bone"):
			armature.pose.bones[ELBOW_LEFT_IK_TIP].mmd_bone.is_visible = False
			armature.pose.bones[ELBOW_LEFT_IK_TIP].mmd_bone.is_controllable = False
			armature.pose.bones[ELBOW_LEFT_IK_TIP].mmd_bone.is_tip = True
		bpy.ops.object.mode_set(mode='EDIT')

		bone = bone_tools.add_bone(armature,ELBOW_RIGHT_IK_TIP,parent_bone=edit_bones[ELBOW_RIGHT_IK],head=edit_bones[ELBOW_RIGHT_IK].head,tail=edit_bones[ELBOW_RIGHT_IK].head)
		bone.tail.y = bone.tail.y + TWENTIETH_LENGTH_OF_ELBOW_BONE
		bone.use_connect = False
		bpy.ops.object.mode_set(mode='POSE')
		armature.pose.bones[ELBOW_RIGHT_IK_TIP].bone.hide = True
		if hasattr(armature.pose.bones[ELBOW_RIGHT_IK_TIP], "mmd_bone"):
			armature.pose.bones[ELBOW_RIGHT_IK_TIP].mmd_bone.is_visible = False
			armature.pose.bones[ELBOW_RIGHT_IK_TIP].mmd_bone.is_controllable = False
			armature.pose.bones[ELBOW_RIGHT_IK_TIP].mmd_bone.is_tip = True
		bpy.ops.object.mode_set(mode='EDIT')

		bone = bone_tools.add_bone(armature,FINGER_MIDDLE_LEFT_IK_TIP,parent_bone=edit_bones[FINGER_MIDDLE_LEFT_IK],head=edit_bones[FINGER_MIDDLE_LEFT_IK].head,tail=edit_bones[FINGER_MIDDLE_LEFT_IK].head)
		bone.tail.z = bone.tail.z - TWENTIETH_LENGTH_OF_ELBOW_BONE
		bone.use_connect = False
		bpy.ops.object.mode_set(mode='POSE')
		armature.pose.bones[FINGER_MIDDLE_LEFT_IK_TIP].bone.hide = True
		if hasattr(armature.pose.bones[FINGER_MIDDLE_LEFT_IK_TIP], "mmd_bone"):
			armature.pose.bones[FINGER_MIDDLE_LEFT_IK_TIP].mmd_bone.is_visible = False
			armature.pose.bones[FINGER_MIDDLE_LEFT_IK_TIP].mmd_bone.is_controllable = False
			armature.pose.bones[FINGER_MIDDLE_LEFT_IK_TIP].mmd_bone.is_tip = True
		bpy.ops.object.mode_set(mode='EDIT')

		bone = bone_tools.add_bone(armature,FINGER_MIDDLE_RIGHT_IK_TIP,parent_bone=edit_bones[FINGER_MIDDLE_RIGHT_IK],head=edit_bones[FINGER_MIDDLE_RIGHT_IK].head,tail=edit_bones[FINGER_MIDDLE_RIGHT_IK].head)
		bone.tail.z = bone.tail.z - TWENTIETH_LENGTH_OF_ELBOW_BONE
		bone.use_connect = False
		bpy.ops.object.mode_set(mode='POSE')
		armature.pose.bones[FINGER_MIDDLE_RIGHT_IK_TIP].bone.hide = True
		if hasattr(armature.pose.bones[FINGER_MIDDLE_RIGHT_IK_TIP], "mmd_bone"):
			armature.pose.bones[FINGER_MIDDLE_RIGHT_IK_TIP].mmd_bone.is_visible = False
			armature.pose.bones[FINGER_MIDDLE_RIGHT_IK_TIP].mmd_bone.is_controllable = False
			armature.pose.bones[FINGER_MIDDLE_RIGHT_IK_TIP].mmd_bone.is_tip = True
		bpy.ops.object.mode_set(mode='EDIT')

		"""
		#The D bones are created
		########## START D BONE CREATION HERE #######
		bpy.ops.object.mode_set(mode='EDIT')
		bone = armature.data.edit_bones.new(ARM_LEFT_D)
		bone.head = armature.data.edit_bones[ARM_LEFT].head
		bone.tail = armature.data.edit_bones[ARM_LEFT].head
		bone.tail.z = armature.data.edit_bones[ARM_LEFT].head.z + QUARTER_LENGTH_OF_ELBOW_BONE
		print('bone = ', bone)
		bone.parent = armature.data.edit_bones[SHOULDER_LEFT]
		bone.use_connect = False
		
		bone = armature.data.edit_bones.new(ARM_RIGHT_D)
		bone.head = armature.data.edit_bones[ARM_RIGHT].head
		bone.tail = armature.data.edit_bones[ARM_RIGHT].head
		bone.tail.z = armature.data.edit_bones[ARM_RIGHT].head.z + QUARTER_LENGTH_OF_ELBOW_BONE
		print('bone = ', bone)
		bone.parent = armature.data.edit_bones[SHOULDER_RIGHT]
		bone.use_connect = False
		
		bone = armature.data.edit_bones.new(ELBOW_LEFT_D)
		bone.head = armature.data.edit_bones[ELBOW_LEFT].head
		bone.tail = armature.data.edit_bones[ELBOW_LEFT].head
		bone.tail.z = armature.data.edit_bones[ELBOW_LEFT].head.z + QUARTER_LENGTH_OF_ELBOW_BONE
		print('bone = ', bone)
		bone.parent = armature.data.edit_bones[ARM_LEFT_D]
		bone.use_connect = False
		
		bone = armature.data.edit_bones.new(ELBOW_RIGHT_D)
		bone.head = armature.data.edit_bones[ELBOW_RIGHT].head
		bone.tail = armature.data.edit_bones[ELBOW_RIGHT].head
		bone.tail.z = armature.data.edit_bones[ELBOW_RIGHT].head.z + QUARTER_LENGTH_OF_ELBOW_BONE
		print('bone = ', bone)
		bone.parent = armature.data.edit_bones[ARM_RIGHT_D]
		bone.use_connect = False

		bone = armature.data.edit_bones.new(WRIST_LEFT_D)
		bone.head = armature.data.edit_bones[WRIST_LEFT].head
		bone.tail = armature.data.edit_bones[WRIST_LEFT].head
		bone.tail.z = armature.data.edit_bones[WRIST_LEFT].head.z + QUARTER_LENGTH_OF_ELBOW_BONE
		print('bone = ', bone)
		bone.parent = armature.data.edit_bones[ELBOW_LEFT]
		bone.use_connect = False
		
		bone = armature.data.edit_bones.new(WRIST_RIGHT_D)
		bone.head = armature.data.edit_bones[WRIST_RIGHT].head
		bone.tail = armature.data.edit_bones[WRIST_RIGHT].head
		bone.tail.z = armature.data.edit_bones[WRIST_RIGHT].head.z + QUARTER_LENGTH_OF_ELBOW_BONE
		print('bone = ', bone)
		bone.parent = armature.data.edit_bones[ELBOW_RIGHT]
		bone.use_connect = False
		


		#transfer weight to D and EX bones
		transfer_vertex_groups(get_armature(),ARM_LEFT,ARM_LEFT_D)
		transfer_vertex_groups(get_armature(),ARM_RIGHT,ARM_RIGHT_D)
		transfer_vertex_groups(get_armature(),ELBOW_LEFT,ELBOW_LEFT_D)
		transfer_vertex_groups(get_armature(),ELBOW_RIGHT,ELBOW_RIGHT_D)
		transfer_vertex_groups(get_armature(),WRIST_LEFT,WRIST_LEFT_D)
		transfer_vertex_groups(get_armature(),WRIST_RIGHT,WRIST_RIGHT_D)
		
		#apply_additional_MMD_rotation
		apply_MMD_additional_rotation(get_armature(),ARM_LEFT,ARM_LEFT_D)
		apply_MMD_additional_rotation(get_armature(),ARM_RIGHT,ARM_RIGHT_D)
		apply_MMD_additional_rotation(get_armature(),ELBOW_LEFT,ELBOW_LEFT_D)
		apply_MMD_additional_rotation(get_armature(),ELBOW_RIGHT,ELBOW_RIGHT_D)
		apply_MMD_additional_rotation(get_armature(),WRIST_LEFT,WRIST_LEFT_D)
		apply_MMD_additional_rotation(get_armature(),WRIST_RIGHT,WRIST_RIGHT_D)

		########## END D BONE CREATION HERE #######
		"""


		bpy.ops.object.mode_set(mode='POSE')

		#Adds IK constraints
		bone_tools.create_ik_constraint(ARM_LEFT,ELBOW_LEFT_IK,2,True,48)
		# armature.pose.bones[ELBOW_LEFT].constraints["IK"].use_location = False

		# armature.pose.bones[ARM_LEFT].constraints.new("LIMIT_ROTATION")
		# armature.pose.bones[ARM_LEFT].constraints["Limit Rotation"].use_limit_x = True
		# armature.pose.bones[ARM_LEFT].constraints["Limit Rotation"].min_x = math.pi/360 #radians = 0.5 degrees
		# armature.pose.bones[ARM_LEFT].constraints["Limit Rotation"].max_x = math.pi #radians = 180 degrees
		# armature.pose.bones[ARM_LEFT].constraints["Limit Rotation"].owner_space = "POSE"
		# armature.pose.bones[ARM_LEFT].constraints["Limit Rotation"].name = "mmd_ik_limit_override"

		bone_tools.create_ik_constraint(ARM_RIGHT,ELBOW_RIGHT_IK,2,True,48)
		# armature.pose.bones[ELBOW_RIGHT].constraints["IK"].use_location = False

		# armature.pose.bones[ARM_RIGHT].constraints.new("LIMIT_ROTATION")
		# armature.pose.bones[ARM_RIGHT].constraints["Limit Rotation"].use_limit_x = True
		# armature.pose.bones[ARM_RIGHT].constraints["Limit Rotation"].min_x = math.pi/360 #radians = 0.5 degrees
		# armature.pose.bones[ARM_RIGHT].constraints["Limit Rotation"].max_x = math.pi #radians = 180 degrees
		# armature.pose.bones[ARM_RIGHT].constraints["Limit Rotation"].owner_space = "POSE"
		# armature.pose.bones[ARM_RIGHT].constraints["Limit Rotation"].name = "mmd_ik_limit_override"

		# armature.pose.bones[ELBOW_LEFT].constraints.new("DAMPED_TRACK")
		# armature.pose.bones[ELBOW_LEFT].constraints["Damped Track"].target = bpy.context.active_object
		# armature.pose.bones[ELBOW_LEFT].constraints["Damped Track"].subtarget = ARM_LEFT
		# armature.pose.bones[ELBOW_LEFT].constraints["Damped Track"].track_axis = 'TRACK_Y'
		# armature.pose.bones[ELBOW_LEFT].constraints["Damped Track"].name = "mmd_ik_target_override"

		bone_tools.create_ik_constraint(ELBOW_LEFT,FINGER_MIDDLE_LEFT_IK,1,True,6)
		# armature.pose.bones[WRIST_LEFT].constraints["IK"].use_location = False

		# armature.pose.bones[ELBOW_RIGHT].constraints.new("DAMPED_TRACK")
		# armature.pose.bones[ELBOW_RIGHT].constraints["Damped Track"].target = bpy.context.active_object
		# armature.pose.bones[ELBOW_RIGHT].constraints["Damped Track"].subtarget = ARM_LEFT
		# armature.pose.bones[ELBOW_RIGHT].constraints["Damped Track"].track_axis = 'TRACK_Y'
		# armature.pose.bones[ELBOW_RIGHT].constraints["Damped Track"].name = "mmd_ik_target_override"

		bone_tools.create_ik_constraint(ELBOW_RIGHT,FINGER_MIDDLE_RIGHT_IK,1,True,6)
		# armature.pose.bones[WRIST_RIGHT].constraints["IK"].use_location = False

		if hasattr(armature.pose.bones[ARM_RIGHT], "mmd_bone"):
			armature.pose.bones[ARM_RIGHT].mmd_bone.ik_rotation_constraint = 2 # 180*2/math.pi
			armature.pose.bones[ARM_LEFT].mmd_bone.ik_rotation_constraint = 2 # 180*2/math.pi
			armature.pose.bones[ELBOW_RIGHT].mmd_bone.ik_rotation_constraint = 4 #180*4/math.pi
			armature.pose.bones[ELBOW_LEFT].mmd_bone.ik_rotation_constraint = 4 # 180*4/math.pi

		#create an 'IK' bone group and add the IK bones to it
		if 'IK' not in bpy.context.active_object.pose.bone_groups.keys():
			bpy.context.active_object.pose.bone_groups.new(name="IK")

		armature.pose.bones[ELBOW_LEFT_IK].bone_group = armature.pose.bone_groups['IK']
		armature.pose.bones[ELBOW_RIGHT_IK].bone_group =armature.pose.bone_groups['IK']
		armature.pose.bones[FINGER_MIDDLE_LEFT_IK].bone_group = armature.pose.bone_groups['IK']
		armature.pose.bones[FINGER_MIDDLE_RIGHT_IK].bone_group = armature.pose.bone_groups['IK']
		armature.pose.bones[ELBOW_LEFT_IK_TIP].bone_group = armature.pose.bone_groups['IK']
		armature.pose.bones[ELBOW_RIGHT_IK_TIP].bone_group = armature.pose.bone_groups['IK']
		armature.pose.bones[FINGER_MIDDLE_LEFT_IK_TIP].bone_group = armature.pose.bone_groups['IK']
		armature.pose.bones[FINGER_MIDDLE_RIGHT_IK_TIP].bone_group = armature.pose.bone_groups['IK']



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
class Add_MMD_Hand_Arm_IK(bpy.types.Operator):
	"""Add hand and arm IK bones and constraints to active MMD model"""
	bl_idname = "ffxiv_mmd.add_hand_arm_ik"
	bl_label = "Add Hand Arm IK to MMD model"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		clear_IK(context)
		main(context)
		return {'FINISHED'}