import bpy
import mathutils
from . import register_wrap
from . import model
from . import import_csv
from mmd_tools.core.bone import FnBone


def correct_root_center():
	print('\n')
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

	else:
		print("Rename bones to MMD_English and then try again.")


def correct_groove():
	print('\n')
	bpy.ops.object.mode_set(mode='OBJECT')
	if model.is_mmd_english() == True:
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

	else:
		print("Rename bones to MMD_English and then try again.")

def correct_waist():
	print('\n')
	bpy.ops.object.mode_set(mode='OBJECT')
	if model.is_mmd_english() == True:
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

	else:
		print("Rename bones to MMD_English and then try again.")
		

def correct_waist_cancel():
	print('\n')
	bpy.ops.object.mode_set(mode='EDIT')
	if model.is_mmd_english() == True:
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

	else:
		print("Rename bones to MMD_English and then try again.")


def correct_view_cnt():
	print('\n')
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
	
	print('\n')
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
	
	else:
		print("Rename bones to MMD_English and then try again.")

			

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


def fix_bone_length(armature,source_bone,target_bone):

	source_bone = armature.data.edit_bones[source_bone]
	target_bone = armature.data.edit_bones[target_bone]

	source_bone.tail = target_bone.head

def correct_bones_length():

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
	else:
		print("Rename bones to MMD_English and then try again.")



def add_breast_tip_bones(armature):

	armature = bpy.context.view_layer.objects.active
	bpy.ops.object.mode_set(mode='EDIT')

	breast = armature.data.edit_bones['j_mune_l']

	if (breast.name + "_tip") not in bpy.context.active_object.data.edit_bones.keys():
		duplicate_bone = armature.data.edit_bones.new(breast.name + "_tip")
		duplicate_bone.head = breast.head
		duplicate_bone.tail = breast.tail
		duplicate_bone.length = breast.length * 1.25
		duplicate_bone.head = breast.tail
		duplicate_bone.roll = breast.roll
		duplicate_bone.parent = breast

	breast = armature.data.edit_bones['j_mune_r']

	if (breast.name + "_tip") not in bpy.context.active_object.data.edit_bones.keys():
		duplicate_bone = armature.data.edit_bones.new(breast.name + "_tip")
		duplicate_bone.head = breast.head
		duplicate_bone.tail = breast.tail
		duplicate_bone.length = breast.length * 1.25
		duplicate_bone.head = breast.tail
		duplicate_bone.roll = breast.roll
		duplicate_bone.parent = breast

def add_eye_control_bone():

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
	else:
		print("Rename bones to MMD_English and then try again.")
	

def setup_MMD_additional_rotation (armature,additional_transform_bone, target_bone,influence):
	pose_bone = armature.pose.bones.get(target_bone)
	pose_bone.mmd_bone.has_additional_rotation = True
	pose_bone.mmd_bone.is_additional_transform_dirty = True
	pose_bone.mmd_bone.additional_transform_bone = additional_transform_bone

	#FnBone.apply_additional_transformation(armature)
	#FnBone.clean_additional_transformation(armature)


def add_bone(armature, bone_name, length, head, tail, parent_bone):
    
	new_bone = None

	# Create a new bone
	if (bone_name) not in bpy.context.active_object.data.edit_bones.keys():
		new_bone = armature.data.edit_bones.new(bone_name)
	else:
		new_bone = bpy.context.active_object.data.edit_bones[bone_name]
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

def add_arm_wrist_twist():

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
		
		#rename the bones
		#arm_twist_L.name = 'arm_twist_L'
		#arm_twist_R.name = 'arm_twist_R'
		#wrist_twist_L.name = 'wrist_twist_L'
		#wrist_twist_R.name = 'wrist_twist_R'
		
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

	else:
		print("Rename bones to MMD_English and then try again.")


    
def setup_MMD_additional_rotation (armature,additional_transform_bone, target_bone, influence):
    pose_bone = armature.pose.bones.get(target_bone)
    pose_bone.mmd_bone.has_additional_rotation = True
    pose_bone.mmd_bone.is_additional_transform_dirty = True
    pose_bone.mmd_bone.additional_transform_influence = influence
    pose_bone.mmd_bone.additional_transform_bone = additional_transform_bone

    #FnBone.apply_additional_transformation(armature)
    #FnBone.clean_additional_transformation(armature)    
    

def add_shoulder_control_bones():

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
	
	else:
		print("Rename bones to MMD_English and then try again.")

def get_csv_bones_by_bone_group(bone_group_type, target_columns):

	csv_data = import_csv.use_csv_bone_metadata_ffxiv_dictionary()

	#get the header column
	header = csv_data[0]
	#get the index of mmd_bone_group_eng
	mmd_bone_group_index = header.index(bone_group_type)
	#get the index of the bone groups passed to it
	column_data_indices = [header.index(target_column) for target_column in target_columns]
	
	#set() means it will not add something if it already is on the list
	bone_list = set()
	
	for column_index in column_data_indices:
		for row in csv_data[1:]:
			#filter out any values where the column is None
			if row[column_index] is not None:			
				bone_list.add((row[mmd_bone_group_index],row[column_index]))

	#sort the list by the first column
	sorted_bone_list = sorted(bone_list, key=lambda x: x[0])
	return sorted_bone_list

def main(context):
	
	selected_bone_tool = bpy.context.scene.selected_bone_tool

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
	if selected_bone_tool == "add_extra_finger_bones":
		mesh = bpy.context.view_layer.objects.active
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		add_extra_finger_bones(armature,mesh)
	if selected_bone_tool == "add_breast_tip_bones":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		add_breast_tip_bones(armature)



@register_wrap
class BoneTools(bpy.types.Operator):
	"""Bone Creation/Adjustment Tools"""
	bl_idname = "ffxiv_mmd_tools_helper.bone_tools"
	bl_label = "Miscellaneous Tools"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.selected_bone_tool = bpy.props.EnumProperty(items = \
	[('none', 'none', 'none')\
	, ("correct_root_center", "Correct MMD Root and Center bones", "Correct MMD root and center bones")\
	, ("correct_groove", "Correct MMD Groove bone", "Correct MMD Groove bone")\
	, ("correct_waist", "Correct MMD Waist bone", "Correct MMD Waist bone")\
	, ("correct_waist_cancel", "Correct waist cancel left and right bones", "Correct waist cancel left and right bones")\
	, ("correct_view_cnt", "Correct MMD 'view cnt' bone", "Correct MMD 'view cnt' bone")\
	, ("correct_bones_lengths", "Correct Bone Lengths and Roll", "Correct Bone Lengths and Roll")\
	, ("add_eye_control_bone", "Add Eye Control Bone (SELECT 'eyes' bone and run again)", "Add Eye Control Bone (SELECT 'eyes' bone and run again)")\
	, ("add_arm_wrist_twist", "Add Arm Twist Bones", "Add Arm Twist Bones")\
	, ("add_shoulder_control_bones", "Add Shoulder Control Bones", "Add Shoulder Control Bones")\
	, ("add_extra_finger_bones", "Add Extra Finger Bones", "Add Extra Finger Bones")\
	#, ("add_breast_tip_bones", "Add Breast Tip Bones", "Add Breast Tip Bones")\
	], name = "", default = 'none')

	@classmethod
	def poll(cls, context):
		obj = context.active_object 
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		main(context)
		return {'FINISHED'}


@register_wrap
class ShowHideBoneNames(bpy.types.Operator):
	"""Toggle Bone Name Display On or Off"""
	bl_idname = "ffxiv_mmd_tools_helper.bone_names_showhide"
	bl_label = "Show or Hide the Bone Name"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		if context.object.data.show_names == True:
			context.object.data.show_names = False
		else:
			context.object.data.show_names = True
		return {'FINISHED'}