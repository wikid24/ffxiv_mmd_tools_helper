import bpy
import math
import mathutils
from . import register_wrap
from . import model
from . import boneMaps_renamer
from . import add_foot_leg_ik
from . import skirt
from mmd_tools.core.bone import FnBone


def all_materials_mmd_ambient_white():
	for m in bpy.data.materials:
		if "mmd_tools_rigid" not in m.name:
			m.mmd_material.ambient_color[0] == 1.0
			m.mmd_material.ambient_color[1] == 1.0
			m.mmd_material.ambient_color[2] == 1.0


def combine_2_bones_1_bone(parent_bone_name, child_bone_name):
	bpy.ops.object.mode_set(mode='EDIT')
	child_bone_tail = bpy.context.active_object.data.edit_bones[child_bone_name].tail
	bpy.context.active_object.data.edit_bones[parent_bone_name].tail = child_bone_tail
	bpy.context.active_object.data.edit_bones.remove(bpy.context.active_object.data.edit_bones[child_bone_name])
	bpy.ops.object.mode_set(mode='POSE')
	print("Combined 2 bones: ", parent_bone_name, child_bone_name)

def combine_2_vg_1_vg(parent_vg_name, child_vg_name):
	#re-weight all vertex groups to the parent and delete the child
	for o in bpy.context.scene.objects:
		if o.type == 'MESH':
			if parent_vg_name in o.vertex_groups.keys():
				if child_vg_name in o.vertex_groups.keys():
					for v in o.data.vertices:
						for g in v.groups:
							if o.vertex_groups[g.group] == o.vertex_groups[child_vg_name]:
								o.vertex_groups[parent_vg_name].add([v.index], o.vertex_groups[child_vg_name].weight(v.index), 'ADD')
					o.vertex_groups.remove(o.vertex_groups[child_vg_name])
					print("Combined 2 vertex groups: ", parent_vg_name, child_vg_name)

	#rename all orphaned vertex groups in the step above from the deleted child to the parent
	for o in bpy.context.scene.objects:
		if o.type == 'MESH':
			if (child_vg_name in o.vertex_groups.keys()) and (parent_vg_name not in o.vertex_groups.keys()):
				for v in o.data.vertices:
					for g in v.groups:
						if o.vertex_groups[g.group].name == child_vg_name:
							o.vertex_groups[child_vg_name].name = parent_vg_name
							print("renamed orphaned child vg ",child_vg_name, " on ", o.name," to ", parent_vg_name)


					

def analyze_selected_parent_child_bone_pair():
	selected_bones = []

	for b in bpy.context.active_object.pose.bones:
		if b.bone.select == True:
			selected_bones.append(b.bone.name)

	if len(selected_bones) != 2:
		print("Exactly 2 bones must be selected." , len(selected_bones), "are selected.")
		return None, None
	if len(selected_bones) == 2:

		if bpy.context.active_object.data.bones[selected_bones[0]].parent == bpy.context.active_object.data.bones[selected_bones[1]]:
			parent_bone_name = selected_bones[1]
			child_bone_name = selected_bones[0]
			return parent_bone_name, child_bone_name
			combine_2_bones_1_bone(parent_bone, child_bone)
			combine_2_vg_1_vg(parent_bone, child_bone)

		if bpy.context.active_object.data.bones[selected_bones[1]].parent == bpy.context.active_object.data.bones[selected_bones[0]]:
			parent_bone_name = selected_bones[0]
			child_bone_name = selected_bones[1]
			return parent_bone_name, child_bone_name
			combine_2_bones_1_bone(parent_bone, child_bone)
			combine_2_vg_1_vg(parent_bone, child_bone)

		if bpy.context.active_object.data.bones[selected_bones[0]].parent != bpy.context.active_object.data.bones[selected_bones[1]]:
			if bpy.context.active_object.data.bones[selected_bones[1]].parent != bpy.context.active_object.data.bones[selected_bones[0]]:
				print("Combining 2 bones to 1 bone requires a parent-child bone pair to be selected. There is no parent-child relationship between the 2 selected bones.")
				return None, None

	bpy.ops.object.mode_set(mode='POSE')

def delete_unused_bones():
	print('\n')
	bpy.ops.object.mode_set(mode='EDIT')
	bones_to_be_deleted = []

	for b in bpy.context.active_object.data.edit_bones:
		if 'unused' in b.name.lower():
			bones_to_be_deleted.append(b.name)

	for b in bones_to_be_deleted:
		bpy.context.active_object.data.edit_bones.remove(bpy.context.active_object.data.edit_bones[b])
		print("removed bone  ", b)

	bpy.ops.object.mode_set(mode='POSE')

def delete_unused_vertex_groups():
	print('\n')
	for o in bpy.context.scene.objects:
		if o.type == 'MESH':
			delete_these = []
			for vg in o.vertex_groups:
				if 'unused' in vg.name.lower():
					if vg.name not in delete_these:
						delete_these.append(vg.name)
			for vg in delete_these:
				if vg in o.vertex_groups.keys():
					o.vertex_groups.remove(o.vertex_groups[vg])
					print('removed vertex group  ', vg)

def test_is_mmd_english_armature():
	mmd_english = True
	bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
	mmd_english_test_bone_names = ['upper body', 'neck', 'head', 'shoulder_L', 'arm_L', 'elbow_L', 'wrist_L', 'leg_L', 'knee_L', 'ankle_L', 'shoulder_R', 'arm_R', 'elbow_R', 'wrist_R', 'leg_R', 'knee_R', 'ankle_R']
	missing_mmd_english_test_bone_names = []
	for b in mmd_english_test_bone_names:
		if b not in bpy.context.active_object.data.bones.keys():
			missing_mmd_english_test_bone_names.append(b)
	if len(missing_mmd_english_test_bone_names) > 0:
		print("Missing mmd_english test bone names = ", missing_mmd_english_test_bone_names)
		print('\n')
		print("This armature appears not to be an mmd_english armature")
		mmd_english = False
	return mmd_english


def correct_root_center():
	print('\n')
	if test_is_mmd_english_armature() == True:
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
		#for o in mesh_objects:
		#	if "center" in o.vertex_groups.keys():
		#		if "center" in bpy.context.active_object.data.bones.keys():
		#			bpy.context.active_object.data.bones["center"].name = "lower body"
		#			print("Renamed center bone to lower body bone.")
		#			bpy.ops.object.mode_set(mode='EDIT')
		#			bpy.context.active_object.data.edit_bones["lower body"].tail.z = 0.5 * (bpy.context.active_object.data.edit_bones["leg_L"].head.z + bpy.context.active_object.data.edit_bones["leg_R"].head.z)
		#bpy.ops.object.mode_set(mode='OBJECT')

		# if there is no "center" bone in the armature, a center bone is added
		if "center" not in bpy.context.active_object.data.bones.keys():
			bpy.ops.object.mode_set(mode='EDIT')
			center_bone = bpy.context.active_object.data.edit_bones.new("center")
			print("Added center bone.")
			center_bone.head = 0.25 * (bpy.context.active_object.data.edit_bones["knee_L"].head + bpy.context.active_object.data.edit_bones["knee_R"].head + bpy.context.active_object.data.edit_bones["leg_L"].head + bpy.context.active_object.data.edit_bones["leg_R"].head)
			center_bone.head.y = 0
			center_bone.tail.z = center_bone.head.z - 0.7
			center_bone.parent = bpy.context.active_object.data.edit_bones["root"]
			if "lower body" in bpy.context.active_object.data.edit_bones.keys():
				bpy.context.active_object.data.edit_bones["lower body"].parent = bpy.context.active_object.data.edit_bones["center"]
			if "upper body" in bpy.context.active_object.data.edit_bones.keys():
				bpy.context.active_object.data.edit_bones["upper body"].parent = bpy.context.active_object.data.edit_bones["center"]
		bpy.ops.object.mode_set(mode='OBJECT')

	if test_is_mmd_english_armature() == False:
		print("This operator will only work on an armature with mmd_english bone names. First rename bones to mmd_english and then try running this operator again.")


def correct_groove():
	print('\n')
	bpy.ops.object.mode_set(mode='OBJECT')
	if test_is_mmd_english_armature() == True:
		bpy.ops.object.mode_set(mode='EDIT')

			# if there is no "groove" bone in the armature, a groove bone is added
		if "groove" not in bpy.context.active_object.data.bones.keys():
			bpy.ops.object.mode_set(mode='EDIT')
			groove = bpy.context.active_object.data.edit_bones.new("groove")
			print("Added groove bone.")
			groove.head = bpy.context.active_object.data.edit_bones["center"].head
			groove.head.z = 0.01 + groove.head.z
			groove.tail.z = 0.1 + (groove.head.z)
			groove.parent = bpy.context.active_object.data.edit_bones["center"]
			if "lower body" in bpy.context.active_object.data.edit_bones.keys():
				bpy.context.active_object.data.edit_bones["lower body"].parent = bpy.context.active_object.data.edit_bones["groove"]
			if "upper body" in bpy.context.active_object.data.edit_bones.keys():
				bpy.context.active_object.data.edit_bones["upper body"].parent = bpy.context.active_object.data.edit_bones["groove"]
		bpy.ops.object.mode_set(mode='OBJECT')

	if test_is_mmd_english_armature() == False:
		print("This operator will only work on an armature with mmd_english bone names. First rename bones to mmd_english and then try running this operator again.")

def correct_waist():
	print('\n')
	bpy.ops.object.mode_set(mode='OBJECT')
	if test_is_mmd_english_armature() == True:
		bpy.ops.object.mode_set(mode='EDIT')

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

	if test_is_mmd_english_armature() == False:
		print("This operator will only work on an armature with mmd_english bone names. First rename bones to mmd_english and then try running this operator again.")
		

def correct_waist_cancel():
	print('\n')
	bpy.ops.object.mode_set(mode='EDIT')
	if test_is_mmd_english_armature() == True:
		bpy.ops.object.mode_set(mode='EDIT')
		#measurements of the length of the foot bone which will used to calculate the lengths of the new bones.
		LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones["ankle_L"].length
		HALF_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones["ankle_L"].length * 0.5
		QUARTER_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones["ankle_L"].length * 0.25
		TWENTIETH_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones["ankle_L"].length * 0.05
		FOURTIETH_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones["ankle_L"].length * 0.025

		if "waist_cancel_L" not in bpy.context.active_object.data.bones.keys():
			waist_cancel_L = bpy.context.active_object.data.edit_bones.new("waist_cancel_L")
			waist_cancel_L.head = bpy.context.active_object.data.edit_bones["leg_L"].head
			waist_cancel_L.tail = bpy.context.active_object.data.edit_bones["leg_L"].head
			waist_cancel_L.parent = bpy.context.active_object.data.edit_bones["lower body"]
			waist_cancel_L.tail.z = bpy.context.active_object.data.edit_bones["leg_L"].head.z + HALF_LENGTH_OF_FOOT_BONE
			print("Added waist_cancel_L bone.")

		if "leg_L" in bpy.context.active_object.data.edit_bones.keys():
			bpy.context.active_object.data.edit_bones["leg_L"].parent = bpy.context.active_object.data.edit_bones["waist_cancel_L"]

		if "waist_cancel_R" not in bpy.context.active_object.data.bones.keys():
			waist_cancel_R = bpy.context.active_object.data.edit_bones.new("waist_cancel_R")
			waist_cancel_R.head = bpy.context.active_object.data.edit_bones["leg_R"].head
			waist_cancel_R.tail = bpy.context.active_object.data.edit_bones["leg_R"].head
			waist_cancel_R.tail.z = bpy.context.active_object.data.edit_bones["leg_R"].head.z + HALF_LENGTH_OF_FOOT_BONE
			waist_cancel_R.parent = bpy.context.active_object.data.edit_bones["lower body"]
			print("Added waist_cancel_R bone.")

		if "leg_R" in bpy.context.active_object.data.edit_bones.keys():
			bpy.context.active_object.data.edit_bones["leg_R"].parent = bpy.context.active_object.data.edit_bones["waist_cancel_R"]
		bpy.ops.object.mode_set(mode='OBJECT')

	if test_is_mmd_english_armature() == False:
		print("This operator will only work on an armature with mmd_english bone names. First rename bones to mmd_english and then try running this operator again.")


def correct_view_cnt():
	print('\n')
	if test_is_mmd_english_armature() == True:
		bpy.ops.object.mode_set(mode='EDIT')

		# if there is no "view_cnt" bone in the armature, a root bone is added
		if "view cnt" not in bpy.context.active_object.data.edit_bones.keys():
			view_cnt = bpy.context.active_object.data.edit_bones.new('view cnt')
			view_cnt.head[:] = (0,0,0)
			view_cnt.tail[:] = (0,0,0.08)
			print("Added MMD 'view cnt' bone.")
		bpy.ops.object.mode_set(mode='OBJECT')

	if test_is_mmd_english_armature() == False:
		print("This operator will only work on an armature with mmd_english bone names. First rename bones to mmd_english and then try running this operator again.")


def add_extra_finger_bones(armature,hand_mesh): 
	
	print('\n')
	if test_is_mmd_english_armature() == True:
		bpy.ops.object.mode_set(mode='EDIT')


		correct_finger(armature,hand_mesh,'fore2_L','fore3_L')
		correct_finger(armature,hand_mesh,'little2_L','little3_L')
		correct_finger(armature,hand_mesh,'third2_L','third3_L')
		correct_finger(armature,hand_mesh,'middle2_L','middle3_L')
		correct_finger(armature,hand_mesh,'fore2_R','fore3_R')
		correct_finger(armature,hand_mesh,'little2_R','little3_R')
		correct_finger(armature,hand_mesh,'third2_R','third3_R')
		correct_finger(armature,hand_mesh,'middle2_R','middle3_R')
	
	if test_is_mmd_english_armature() == False:
		print("This operator will only work on an armature with mmd_english bone names. First rename bones to mmd_english and then try running this operator again.")

			

def correct_finger(armature, hand_mesh,source_bone,new_bone):


	if new_bone not in armature.data.bones.keys():

		# set the armature to Edit Mode
		bpy.context.view_layer.objects.active = armature
		bpy.ops.object.mode_set(mode='EDIT')

		# select the bone
		bpy.ops.armature.select_all(action='DESELECT')
		armature.data.edit_bones[source_bone].select = True

		# get the head and tail positions of the old bone
		source_bone_head = armature.data.bones[source_bone].head
		source_bone_tail = armature.data.bones[source_bone].tail

		# get the midpoint of the old bone
		midpoint = (source_bone_head + source_bone_tail) / 2

		# subdivide the bone into two separate bones
		bpy.ops.armature.subdivide()

		# set the armature to Object Mode
		bpy.ops.object.mode_set(mode='OBJECT')

		# rename the new bone
		armature.data.bones[source_bone + ".001"].name = new_bone

		# get the vertex group
		mesh_vertex_groups = hand_mesh.vertex_groups[source_bone]

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
		new_vertex_group = hand_mesh.vertex_groups.new(name=new_bone)

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


def add_bone_to_group (bone_name,bone_group):
	if bone_name in bpy.context.active_object.pose.bones:
		bone = bpy.context.active_object.pose.bones[bone_name]
		bone.bone_group = bpy.context.active_object.pose.bone_groups[bone_group]
	else:
		print("bone: " +  bone_name + " does not exist in currently selected object")




def correct_bones_length():

	bpy.ops.object.mode_set(mode='EDIT')

	#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
	armature = bpy.context.view_layer.objects.active


	fix_bone_length(armature,'shoulder_L','arm_L')
	fix_bone_length(armature,'shoulder_R','arm_R')
	fix_bone_length(armature,'arm_L','elbow_L')
	fix_bone_length(armature,'arm_R','elbow_R')
	fix_bone_length(armature,'elbow_L','wrist_L')
	fix_bone_length(armature,'elbow_R','wrist_R')
		

def fix_bone_length(armature,source_bone,target_bone):

	source_bone = armature.data.edit_bones[source_bone]
	target_bone = armature.data.edit_bones[target_bone]

	source_bone.tail = target_bone.head

def add_extra_titty_bones(armature):

	armature = bpy.context.view_layer.objects.active
	bpy.ops.object.mode_set(mode='EDIT')

	titty = armature.data.edit_bones['j_mune_l']

	duplicate_bone = armature.data.edit_bones.new(titty.name + "_tip")
	duplicate_bone.head = titty.head
	duplicate_bone.tail = titty.tail
	duplicate_bone.length = titty.length * 1.25
	duplicate_bone.head = titty.tail
	duplicate_bone.roll = titty.roll
	duplicate_bone.parent = titty

	titty = armature.data.edit_bones['j_mune_r']

	duplicate_bone = armature.data.edit_bones.new(titty.name + "_tip")
	duplicate_bone.head = titty.head
	duplicate_bone.tail = titty.tail
	duplicate_bone.length = titty.length * 1.25
	duplicate_bone.head = titty.tail
	duplicate_bone.roll = titty.roll
	duplicate_bone.parent = titty

def add_eye_control_bone():
	armature = bpy.context.view_layer.objects.active
	bpy.ops.object.mode_set(mode='EDIT')

	eye_L_bone = armature.data.edit_bones.get("eye_L")
	eye_R_bone = armature.data.edit_bones.get("eye_R")
	head_bone = armature.data.edit_bones.get("head")
	
	eyes_bone = None
	if armature.data.edit_bones.get("eyes") is None:
		eyes_bone = armature.data.edit_bones.new("eyes")
		
		eyes_bone.head = 0.5 * (eye_L_bone.head + eye_R_bone.head)
		eyes_bone.head.z = eyes_bone.head.z + (2 * (eye_L_bone.length + eye_R_bone.length))
		eyes_bone.length = eye_L_bone.length
			
		eyes_bone.parent = head_bone
		
		#flip the orientation of the bone
		eye_controller_bone_head = eyes_bone.head.copy()
		eye_controller_bone_tail = eyes_bone.tail.copy()
		eyes_bone.head = eye_controller_bone_tail
		eyes_bone.tail = eye_controller_bone_head
			
	else:
		eyes_bone = armature.data.edit_bones.get("eyes")
	
	#THIS IS THE ONLY WAY I GOT IT TO WORK IS BY hard_coding the bone name, do not change this code
	setup_MMD_additional_rotation(armature,'eyes','eye_L',1)
	setup_MMD_additional_rotation(armature,'eyes','eye_R',1)
	
	armature.data.edit_bones.active = eyes_bone
	FnBone.apply_additional_transformation(armature)
	

def setup_MMD_additional_rotation (armature,additional_transform_bone, target_bone,influence):
	pose_bone = armature.pose.bones.get(target_bone)
	pose_bone.mmd_bone.has_additional_rotation = True
	pose_bone.mmd_bone.is_additional_transform_dirty = True
	pose_bone.mmd_bone.additional_transform_bone = additional_transform_bone

	#FnBone.apply_additional_transformation(armature)
	#FnBone.clean_additional_transformation(armature)


def add_bone(armature, bone_name, length, head, tail, parent_bone):
    # Create a new bone
    new_bone = armature.data.edit_bones.new(bone_name)
    # Set the length of the bone
    new_bone.head = head
    new_bone.tail = tail
    new_bone.length = length
    # Point the bone directly upwards
    new_bone.roll = 0
    new_bone.parent = parent_bone
    return new_bone

def create_twist_support_bones(armature,source_bone,bone_1,bone_2,bone_3,additional_rotation_bone):


    if armature:
        # Get the armature in edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        # Get the source bone
        source_bone = armature.data.edit_bones.get(source_bone)
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
            _bone_1 = add_bone(armature, bone_1, length * 0.30, pos1, pos1 + mathutils.Vector((0, 0, length * 0.1)),source_bone)
            _bone_2 = add_bone(armature, bone_2, length * 0.30, pos2, pos2 + mathutils.Vector((0, 0, length * 0.1)),source_bone)
            _bone_3 = add_bone(armature, bone_3, length * 0.30, pos3, pos3 + mathutils.Vector((0, 0, length * 0.1)),source_bone)
            
            bpy.ops.object.mode_set(mode='POSE')
            
            # Select all bones in the armature
            for bone in armature.pose.bones:
                bone.bone.select = True
            
            setup_MMD_additional_rotation(armature,additional_rotation_bone,bone_1, 0.25)
            setup_MMD_additional_rotation(armature,additional_rotation_bone,bone_2, 0.50)
            setup_MMD_additional_rotation(armature,additional_rotation_bone,bone_3, 0.75)
            
            
            armature.data.edit_bones.active = source_bone
            FnBone.apply_additional_transformation(armature)
            
            # Return to object mode
            bpy.ops.object.mode_set(mode='OBJECT')
    else:
        print("Armature object not found")

def correct_arm_wrist_twist():
	
	bpy.ops.object.mode_set(mode='EDIT')
	# set the armature to Edit Mode
	armature = bpy.context.view_layer.objects.active
	
	#parent the elbow bone to the arm twist
	arm_twist_L = armature.data.edit_bones["n_hkata_l"]
	arm_twist_R = armature.data.edit_bones["n_hkata_r"]
	elbow_L = armature.data.edit_bones["elbow_L"]
	elbow_R = armature.data.edit_bones["elbow_R"]
	elbow_L.parent = arm_twist_L
	elbow_R.parent = arm_twist_R

	#parent the wrist bone to the wrist twist
	wrist_twist_L = armature.data.edit_bones["n_hte_l"]
	wrist_twist_R = armature.data.edit_bones["n_hte_r"]
	wrist_L = armature.data.edit_bones["wrist_L"]
	wrist_R = armature.data.edit_bones["wrist_R"]
	wrist_L.parent = wrist_twist_L
	wrist_R.parent = wrist_twist_R
	
	#rename the bones
	arm_twist_L.name = 'arm_twist_L'
	arm_twist_R.name = 'arm_twist_R'
	wrist_twist_L.name = 'wrist_twist_L'
	wrist_twist_R.name = 'wrist_twist_R'
	
	#bpy.ops.object.mode_set(mode='POSE')
	#lock rotation to the Y axis only
	
	armature.pose.bones.get(arm_twist_L.name).lock_rotation = [True,False,True]
	armature.pose.bones.get(arm_twist_R.name).lock_rotation = [True,False,True]
	armature.pose.bones.get(wrist_twist_L.name).lock_rotation = [True,False,True]
	armature.pose.bones.get(wrist_twist_R.name).lock_rotation = [True,False,True]


	create_twist_support_bones(armature,'arm_L','arm_twist_1_L','arm_twist_2_L','arm_twist_3_L','arm_twist_L')
	create_twist_support_bones(armature,'arm_R','arm_twist_1_R','arm_twist_2_R','arm_twist_3_R','arm_twist_R')
	create_twist_support_bones(armature,'elbow_L','wrist_twist_1_L','wrist_twist_2_L','wrist_twist_3_L','wrist_twist_L')
	create_twist_support_bones(armature,'elbow_R','wrist_twist_1_R','wrist_twist_2_R','wrist_twist_3_R','wrist_twist_R')


    
def setup_MMD_additional_rotation (armature,additional_transform_bone, target_bone, influence):
    pose_bone = armature.pose.bones.get(target_bone)
    pose_bone.mmd_bone.has_additional_rotation = True
    pose_bone.mmd_bone.is_additional_transform_dirty = True
    pose_bone.mmd_bone.additional_transform_influence = influence
    pose_bone.mmd_bone.additional_transform_bone = additional_transform_bone

    #FnBone.apply_additional_transformation(armature)
    #FnBone.clean_additional_transformation(armature)    
    

def add_shoulder_control_bones():
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
    shoulder_P_L = add_bone(armature, 'shoulder_P_L',shoulder_L.length,shoulder_L.head ,shoulder_L.head,j_sebo_c)
    shoulder_P_R = add_bone(armature, 'shoulder_P_R',shoulder_R.length,shoulder_R.head ,shoulder_R.head,j_sebo_c)

    shoulder_C_L = add_bone(armature, 'shoulder_C_L',shoulder_L.length,shoulder_L.tail ,shoulder_L.tail,shoulder_L)
    shoulder_C_R = add_bone(armature, 'shoulder_C_R',shoulder_R.length,shoulder_R.tail ,shoulder_R.tail,shoulder_R)

    #add_bone(armature, bone_name, length, head, tail, parent_bone)

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
    
    setup_MMD_additional_rotation (armature,'shoulder_P_L', 'shoulder_C_L', -1.0)
    setup_MMD_additional_rotation (armature,'shoulder_P_R', 'shoulder_C_R', -1.0)
    FnBone.apply_additional_transformation(armature)

"""
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
"""

def fix_object_axis():
	bpy.ops.object.mode_set(mode='OBJECT')
	obj = bpy.context.view_layer.objects.active
	#rotate object 90 degrees on x axis
	obj.rotation_euler = [math.radians(90), 0, 0]
	
	bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
	
	armature = model.find_MMD_Armature(bpy.context.object)
	
	#bpy.ops.object.mode_set(mode='EDIT')

	##commented out because current bone roll is needed otherwise wonky stuff with inverted bones happens when trying to perform transforms
	#for bone in armature.data.edit_bones:
	#	bone.roll = 0
	#bpy.ops.object.mode_set(mode='OBJECT')

def main(context):
	# print(bpy.context.scene.selected_miscellaneous_tools)
	if bpy.context.scene.selected_miscellaneous_tools == "combine_2_bones":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		parent_bone_name, child_bone_name = analyze_selected_parent_child_bone_pair()
		if parent_bone_name is not None:
			if child_bone_name is not None:
				combine_2_vg_1_vg(parent_bone_name, child_bone_name)
				combine_2_bones_1_bone(parent_bone_name, child_bone_name)
	if bpy.context.scene.selected_miscellaneous_tools == "delete_unused":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		delete_unused_bones()
		delete_unused_vertex_groups()
	if bpy.context.scene.selected_miscellaneous_tools == "mmd_ambient_white":
		all_materials_mmd_ambient_white()
	if bpy.context.scene.selected_miscellaneous_tools == "correct_root_center":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		correct_root_center()
	if bpy.context.scene.selected_miscellaneous_tools == "correct_groove":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		correct_groove()
	if bpy.context.scene.selected_miscellaneous_tools == "correct_waist":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		correct_waist()
	if bpy.context.scene.selected_miscellaneous_tools == "correct_waist_cancel":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		correct_waist_cancel()
	if bpy.context.scene.selected_miscellaneous_tools == "correct_view_cnt":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		correct_view_cnt()
	if bpy.context.scene.selected_miscellaneous_tools == "correct_bones_lengths":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		correct_bones_length()
	if bpy.context.scene.selected_miscellaneous_tools == "fix_object_axis":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		fix_object_axis()
	if bpy.context.scene.selected_miscellaneous_tools == "add_extra_finger_bones":
		mesh = bpy.context.view_layer.objects.active
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		add_extra_finger_bones(armature,mesh)
	if bpy.context.scene.selected_miscellaneous_tools == "add_extra_titty_bones":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		add_extra_titty_bones(armature)
	if bpy.context.scene.selected_miscellaneous_tools == "add_eye_control_bone":
		armature = bpy.context.view_layer.objects.active
		add_eye_control_bone()
	if bpy.context.scene.selected_miscellaneous_tools == "correct_arm_wrist_twist":
		armature = bpy.context.view_layer.objects.active
		correct_arm_wrist_twist()
	if bpy.context.scene.selected_miscellaneous_tools == "add_shoulder_control_bones":
		armature = bpy.context.view_layer.objects.active
		add_shoulder_control_bones()



@register_wrap
class MiscellaneousTools(bpy.types.Operator):
	"""Miscellanous Tools"""
	bl_idname = "ffxiv_mmd_tools_helper.miscellaneous_tools"
	bl_label = "Miscellaneous Tools"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.selected_miscellaneous_tools = bpy.props.EnumProperty(items = \
	[('none', 'none', 'none')\
	, ("fix_object_axis", "Fix Object Axis (90 degrees)","Fix Object Axis (90 degrees)") \
	, ("combine_2_bones", "Combine 2 bones", "Combine a parent-child pair of bones and their vertex groups to 1 bone and 1 vertex group")\
	, ("delete_unused", "Delete unused bones and unused vertex groups", "Delete all bones and vertex groups which have the word 'unused' in them")\
	, ("mmd_ambient_white", "All materials MMD ambient color white", "Change the MMD ambient color of all materials to white")\
	, ("correct_root_center", "Correct MMD Root and Center bones", "Correct MMD root and center bones")\
	, ("correct_groove", "Correct MMD Groove bone", "Correct MMD Groove bone")\
	, ("correct_waist", "Correct MMD Waist bone", "Correct MMD Waist bone")\
	, ("correct_waist_cancel", "Correct waist cancel left and right bones", "Correct waist cancel left and right bones")\
	, ("correct_view_cnt", "Correct MMD 'view cnt' bone", "Correct MMD 'view cnt' bone")\
	, ("correct_bones_lengths", "Correct Bone Lengths and Roll", "Correct Bone Lengths and Roll")\
	, ("add_extra_finger_bones", "Add Extra Finger Bones", "Add Extra Finger Bones")\
	#, ("add_extra_titty_bones", "add_extra_titty_bones", "add_extra_titty_bones")\
	, ("add_eye_control_bone", "Add Eye Control Bone (SELECT 'eyes' bone and run again)", "Add Eye Control Bone (SELECT 'eyes' bone and run again)")\
	, ("correct_arm_wrist_twist", "Correct Arm Twist Bones", "Correct Arm Twist Bones")\
	, ("add_shoulder_control_bones", "Add Shoulder Control Bones", "Add Shoulder Control Bones")\
	], name = "Function", default = 'none')

	@classmethod
	def poll(cls, context):
		obj = context.active_object 
		return obj is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}