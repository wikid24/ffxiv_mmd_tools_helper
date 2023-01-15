import bpy
import math

from . import register_wrap
from . import model

@register_wrap
class MiscellaneousToolsPanel(bpy.types.Panel):
	"""Miscellaneous Tools panel"""
	bl_label = "Miscellaneous Tools Panel"
	bl_idname = "OBJECT_PT_miscellaneous_tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout

		row = layout.row()
		layout.prop(context.scene, "selected_miscellaneous_tools")
		row = layout.row()
		row.label(text="Miscellaneous Tools", icon='WORLD_DATA')
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.miscellaneous_tools", text = "Execute Function")

def all_materials_mmd_ambient_white():
	for m in bpy.data.materials:
		if "mmd_tools_rigid" not in m.name:
			m.mmd_material.ambient_color[0] == 1.0
			m.mmd_material.ambient_color[1] == 1.0
			m.mmd_material.ambient_color[2] == 1.0

def import_nala():

	bpy.ops.import_scene.fbx( \
	filepath=r'C:\Users\wikid\OneDrive\Documents\TexTools\Saved\FullModel\Nala V3\Nala V3.fbx'\
	, primary_bone_axis='X' \
	, secondary_bone_axis='Y' \
	, use_manual_orientation=True \
	, axis_forward='Y' \
	, axis_up='Z'
)

"""

bpy.ops.import_scene.fbx('INVOKE_DEFAULT')

bpy.ops.import_scene.fbx(filepath='', directory='', filter_glob='*.fbx', files=None, 
ui_tab='MAIN', use_manual_orientation=False, global_scale=1.0, bake_space_transform=False, 
use_custom_normals=True, colors_type='SRGB', use_image_search=True, use_alpha_decals=False, 
decal_offset=0.0, use_anim=True, anim_offset=1.0, use_subsurf=False, use_custom_props=True, 
use_custom_props_enum_as_string=True, ignore_leaf_bones=False, force_connect_children=False, 
automatic_bone_orientation=False, primary_bone_axis='X', secondary_bone_axis='Y', use_prepost_rot=True, axis_forward='-Z', axis_up='Y'


"""


def fix_object_axis():
	bpy.ops.object.mode_set(mode='OBJECT')
	obj = bpy.context.view_layer.objects.active
	obj.rotation_euler = [math.radians(90), 0, 0]
	bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)





def combine_2_bones_1_bone(parent_bone_name, child_bone_name):
	bpy.ops.object.mode_set(mode='EDIT')
	child_bone_tail = bpy.context.active_object.data.edit_bones[child_bone_name].tail
	bpy.context.active_object.data.edit_bones[parent_bone_name].tail = child_bone_tail
	bpy.context.active_object.data.edit_bones.remove(bpy.context.active_object.data.edit_bones[child_bone_name])
	bpy.ops.object.mode_set(mode='POSE')
	print("Combined 2 bones: ", parent_bone_name, child_bone_name)

def combine_2_vg_1_vg(parent_vg_name, child_vg_name):
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
			# combine_2_bones_1_bone(parent_bone, child_bone)
			# combine_2_vg_1_vg(parent_bone, child_bone)

		if bpy.context.active_object.data.bones[selected_bones[1]].parent == bpy.context.active_object.data.bones[selected_bones[0]]:
			parent_bone_name = selected_bones[0]
			child_bone_name = selected_bones[1]
			return parent_bone_name, child_bone_name
			# combine_2_bones_1_bone(parent_bone, child_bone)
			# combine_2_vg_1_vg(parent_bone, child_bone)

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
		waist.tail = waist.head
		waist.head.z = waist.tail.z - 0.05
		waist.head.y = waist.tail.y + 0.03
		waist.roll = 0
		waist.parent = bpy.context.active_object.data.edit_bones["groove"]
		if "lower body" in bpy.context.active_object.data.edit_bones.keys():
			bpy.context.active_object.data.edit_bones["lower body"].parent = bpy.context.active_object.data.edit_bones["waist"]
		if "upper body" in bpy.context.active_object.data.edit_bones.keys():
			bpy.context.active_object.data.edit_bones["upper body"].parent = bpy.context.active_object.data.edit_bones["waist"]
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


def create_bone_groups():
	print('\n')
	if test_is_mmd_english_armature() == True:
		bpy.ops.object.mode_set(mode='EDIT')
	
	#create an 'IK' bone group and add the IK bones to it
	bpy.ops.object.mode_set(mode='POSE')
	if 'IK' not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name="IK")
#	bpy.context.active_object.pose.bones['leg IK_L'].bone_group = bpy.context.active_object.pose.bone_groups['IK']
#	bpy.context.active_object.pose.bones['leg IK_R'].bone_group = bpy.context.active_object.pose.bone_groups['IK']
#	bpy.context.active_object.pose.bones['toe IK_L'].bone_group = bpy.context.active_object.pose.bone_groups['IK']
#	bpy.context.active_object.pose.bones['toe IK_R'].bone_group = bpy.context.active_object.pose.bone_groups['IK']
#	bpy.context.active_object.pose.bones['leg IK_L_t'].bone_group = bpy.context.active_object.pose.bone_groups['IK']
#	bpy.context.active_object.pose.bones['leg IK_R_t'].bone_group = bpy.context.active_object.pose.bone_groups['IK']
#	bpy.context.active_object.pose.bones['toe IK_L_t'].bone_group = bpy.context.active_object.pose.bone_groups['IK']
#	bpy.context.active_object.pose.bones['toe IK_R_t'].bone_group = bpy.context.active_object.pose.bone_groups['IK']

	#create an 'センター'(center) bone group and add the base bones to it
	bpy.ops.object.mode_set(mode='POSE')
	if 'root' not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name="root")
	bpy.context.active_object.pose.bones['root'].bone_group = bpy.context.active_object.pose.bone_groups['root']
	bpy.context.active_object.pose.bones['center'].bone_group = bpy.context.active_object.pose.bone_groups['root']
	bpy.context.active_object.pose.bones['groove'].bone_group = bpy.context.active_object.pose.bone_groups['root']
	bpy.context.active_object.pose.bones['waist'].bone_group = bpy.context.active_object.pose.bone_groups['root']

	#create an 'skirt' bone group and add the base bones to it
	bpy.ops.object.mode_set(mode='POSE')
	if 'skirt' not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name="skirt")
	bpy.context.active_object.pose.bones['skirt_fr_L_a'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_fr_L_b'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_fr_L_c'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
#bpy.context.active_object.pose.bones['skirt_fr_L_d'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_fr_R_a'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_fr_R_b'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_fr_R_c'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
#bpy.context.active_object.pose.bones['skirt_fr_R_d'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_s_L_a'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_s_L_b'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_s_L_c'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
#bpy.context.active_object.pose.bones['skirt_s_L_d'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_s_R_a'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_s_R_b'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_s_R_c'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
#bpy.context.active_object.pose.bones['skirt_s_R_d'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_b_L_a'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_b_L_b'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_b_L_c'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
#bpy.context.active_object.pose.bones['skirt_b_L_d'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_b_R_a'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_b_R_b'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
	bpy.context.active_object.pose.bones['skirt_b_R_c'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']
#bpy.context.active_object.pose.bones['skirt_b_R_d'].bone_group = bpy.context.active_object.pose.bone_groups['skirt']

	#create an 'armor' bone group and add the base bones to it
	bpy.ops.object.mode_set(mode='POSE')
	if 'armor' not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name="armor")
	bpy.context.active_object.pose.bones['armor_cape_L'].bone_group = bpy.context.active_object.pose.bone_groups['armor']
	bpy.context.active_object.pose.bones['armor_cape_R'].bone_group = bpy.context.active_object.pose.bone_groups['armor']
	bpy.context.active_object.pose.bones['armor_waist_1_l'].bone_group = bpy.context.active_object.pose.bone_groups['armor']
	bpy.context.active_object.pose.bones['armor_waist_1_r'].bone_group = bpy.context.active_object.pose.bone_groups['armor']
	bpy.context.active_object.pose.bones['armor_waist_2_l'].bone_group = bpy.context.active_object.pose.bone_groups['armor']
	bpy.context.active_object.pose.bones['armor_waist_2_r'].bone_group = bpy.context.active_object.pose.bone_groups['armor']
	bpy.context.active_object.pose.bones['clothes_elbow_L'].bone_group = bpy.context.active_object.pose.bone_groups['armor']
	bpy.context.active_object.pose.bones['clothes_elbow_R'].bone_group = bpy.context.active_object.pose.bone_groups['armor']
	bpy.context.active_object.pose.bones['armor_shouldpad_R'].bone_group = bpy.context.active_object.pose.bone_groups['armor']
	bpy.context.active_object.pose.bones['armor_shouldpad_l'].bone_group = bpy.context.active_object.pose.bone_groups['armor']
	bpy.context.active_object.pose.bones['armor_forearm_R'].bone_group = bpy.context.active_object.pose.bone_groups['armor']
	bpy.context.active_object.pose.bones['dummy_L'].bone_group = bpy.context.active_object.pose.bone_groups['armor']
	bpy.context.active_object.pose.bones['dummy_R'].bone_group = bpy.context.active_object.pose.bone_groups['armor']
	bpy.context.active_object.pose.bones['armor_forearm_L'].bone_group = bpy.context.active_object.pose.bone_groups['armor']

	#create an 'arms' bone group and add the base bones to it
	bpy.ops.object.mode_set(mode='POSE')
	if 'arms' not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name="arms")
	bpy.context.active_object.pose.bones['shoulder_L'].bone_group = bpy.context.active_object.pose.bone_groups['arms']
	bpy.context.active_object.pose.bones['arm_L'].bone_group = bpy.context.active_object.pose.bone_groups['arms']
	bpy.context.active_object.pose.bones['arm twist_L'].bone_group = bpy.context.active_object.pose.bone_groups['arms']
	bpy.context.active_object.pose.bones['elbow_L'].bone_group = bpy.context.active_object.pose.bone_groups['arms']
#	bpy.context.active_object.pose.bones['wrist twist_L'].bone_group = bpy.context.active_object.pose.bone_groups['arms']
	bpy.context.active_object.pose.bones['wrist_L'].bone_group = bpy.context.active_object.pose.bone_groups['arms']
	bpy.context.active_object.pose.bones['shoulder_R'].bone_group = bpy.context.active_object.pose.bone_groups['arms']
	bpy.context.active_object.pose.bones['arm_R'].bone_group = bpy.context.active_object.pose.bone_groups['arms']
	bpy.context.active_object.pose.bones['arm twist_R'].bone_group = bpy.context.active_object.pose.bone_groups['arms']
	bpy.context.active_object.pose.bones['elbow_R'].bone_group = bpy.context.active_object.pose.bone_groups['arms']
#	bpy.context.active_object.pose.bones['wrist twist_R'].bone_group = bpy.context.active_object.pose.bone_groups['arms']
	bpy.context.active_object.pose.bones['wrist_R'].bone_group = bpy.context.active_object.pose.bone_groups['arms']

	#create a 'face' bone group and add the base bones to it
	bpy.ops.object.mode_set(mode='POSE')
	if 'face' not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name="face")
	bpy.context.active_object.pose.bones['eye_L'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['eye_R'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['nostrils'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['head cheek left 1'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['head cheek right 1'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['head mouth corner left'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['head mouth corner right'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['head eyebrow left 2'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['head eyebrow right 2'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['j_f_memoto'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['head eyebrow left 1'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['head eyebrow right 1'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['j_f_ulip_a'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['head lip upper middle'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['head eyelid left upper'].bone_group = bpy.context.active_object.pose.bone_groups['face']
	bpy.context.active_object.pose.bones['head eyelid right upper'].bone_group = bpy.context.active_object.pose.bone_groups['face']

#create a 'hair' bone group and add the base bones to it
	bpy.ops.object.mode_set(mode='POSE')
	if 'hair' not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name="hair")
#	bpy.context.active_object.pose.bones['j_ex_h0005_ke_b'].bone_group = bpy.context.active_object.pose.bone_groups['hair']
#	bpy.context.active_object.pose.bones['j_ex_h0005_ke_f'].bone_group = bpy.context.active_object.pose.bone_groups['hair']
	bpy.context.active_object.pose.bones['hair l'].bone_group = bpy.context.active_object.pose.bone_groups['hair']
	bpy.context.active_object.pose.bones['hair r'].bone_group = bpy.context.active_object.pose.bone_groups['hair']
	bpy.context.active_object.pose.bones['hair_side_L'].bone_group = bpy.context.active_object.pose.bone_groups['hair']
	bpy.context.active_object.pose.bones['hair_back_a'].bone_group = bpy.context.active_object.pose.bone_groups['hair']
	bpy.context.active_object.pose.bones['hair_back_b'].bone_group = bpy.context.active_object.pose.bone_groups['hair']

#create a 'head' bone group and add the base bones to it
	bpy.ops.object.mode_set(mode='POSE')
	if 'head' not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name="head")
	bpy.context.active_object.pose.bones['neck'].bone_group = bpy.context.active_object.pose.bone_groups['head']
	bpy.context.active_object.pose.bones['head'].bone_group = bpy.context.active_object.pose.bone_groups['head']
	bpy.context.active_object.pose.bones['head jaw'].bone_group = bpy.context.active_object.pose.bone_groups['head']
	bpy.context.active_object.pose.bones['j_f_dlip_a'].bone_group = bpy.context.active_object.pose.bone_groups['head']
	bpy.context.active_object.pose.bones['head lip lower middle'].bone_group = bpy.context.active_object.pose.bone_groups['head']
	bpy.context.active_object.pose.bones['head eyelid left lower'].bone_group = bpy.context.active_object.pose.bone_groups['head']
	bpy.context.active_object.pose.bones['head eyelid right lower'].bone_group = bpy.context.active_object.pose.bone_groups['head']
	bpy.context.active_object.pose.bones['L ear'].bone_group = bpy.context.active_object.pose.bone_groups['head']
	bpy.context.active_object.pose.bones['n_ear_a_l'].bone_group = bpy.context.active_object.pose.bone_groups['head']
	bpy.context.active_object.pose.bones['n_ear_b_l'].bone_group = bpy.context.active_object.pose.bone_groups['head']
	bpy.context.active_object.pose.bones['R ear'].bone_group = bpy.context.active_object.pose.bone_groups['head']
	bpy.context.active_object.pose.bones['n_ear_a_r'].bone_group = bpy.context.active_object.pose.bone_groups['head']
	bpy.context.active_object.pose.bones['n_ear_b_r'].bone_group = bpy.context.active_object.pose.bone_groups['head']
	bpy.context.active_object.pose.bones['hat_bunny_ears_L'].bone_group = bpy.context.active_object.pose.bone_groups['head']
	bpy.context.active_object.pose.bones['hat_bunny_ears_R'].bone_group = bpy.context.active_object.pose.bone_groups['head']

#create a legs bone gruop and add the base bones to it
	bpy.ops.object.mode_set(mode='POSE')
	if 'legs' not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name="legs")
	bpy.context.active_object.pose.bones['leg_L'].bone_group = bpy.context.active_object.pose.bone_groups['legs']
	bpy.context.active_object.pose.bones['knee_L'].bone_group = bpy.context.active_object.pose.bone_groups['legs']
	bpy.context.active_object.pose.bones['j_asi_c_l'].bone_group = bpy.context.active_object.pose.bone_groups['legs']
	bpy.context.active_object.pose.bones['ankle_L'].bone_group = bpy.context.active_object.pose.bone_groups['legs']
	bpy.context.active_object.pose.bones['toe_L'].bone_group = bpy.context.active_object.pose.bone_groups['legs']
	bpy.context.active_object.pose.bones['leg_R'].bone_group = bpy.context.active_object.pose.bone_groups['legs']
	bpy.context.active_object.pose.bones['knee_R'].bone_group = bpy.context.active_object.pose.bone_groups['legs']
	bpy.context.active_object.pose.bones['j_asi_c_r'].bone_group = bpy.context.active_object.pose.bone_groups['legs']
	bpy.context.active_object.pose.bones['ankle_R'].bone_group = bpy.context.active_object.pose.bone_groups['legs']
	bpy.context.active_object.pose.bones['toe_R'].bone_group = bpy.context.active_object.pose.bone_groups['legs']

#torso
	bpy.ops.object.mode_set(mode='POSE')
	if 'torso' not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name="torso")
	bpy.context.active_object.pose.bones['waist'].bone_group = bpy.context.active_object.pose.bone_groups['torso']
	bpy.context.active_object.pose.bones['lower body'].bone_group = bpy.context.active_object.pose.bone_groups['torso']
	bpy.context.active_object.pose.bones['upper body'].bone_group = bpy.context.active_object.pose.bone_groups['torso']
	bpy.context.active_object.pose.bones['upper body 2'].bone_group = bpy.context.active_object.pose.bone_groups['torso']
	bpy.context.active_object.pose.bones['bust_L'].bone_group = bpy.context.active_object.pose.bone_groups['torso']
	bpy.context.active_object.pose.bones['bust_R'].bone_group = bpy.context.active_object.pose.bone_groups['torso']


	#create a 'root' bone group and add the 'view cnt' bone to it
	bpy.ops.object.mode_set(mode='POSE')
	if 'root' not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name="root")
	bpy.context.active_object.pose.bones['root'].bone_group = bpy.context.active_object.pose.bone_groups['root']
	bpy.context.active_object.pose.bones['view cnt'].bone_group = bpy.context.active_object.pose.bone_groups['root']
	bpy.context.active_object.pose.bones['center'].bone_group = bpy.context.active_object.pose.bone_groups['root']
	bpy.context.active_object.pose.bones['groove'].bone_group = bpy.context.active_object.pose.bone_groups['root']


	bpy.context.active_object.data.display_type = 'OCTAHEDRAL'
	
	if test_is_mmd_english_armature() == False:
		print("This operator will only work on an armature with mmd_english bone names. First rename bones to mmd_english and then try running this operator again.")


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
	if bpy.context.scene.selected_miscellaneous_tools == "create_bone_groups":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		create_bone_groups()
	if bpy.context.scene.selected_miscellaneous_tools == "correct_bone_lengths":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		correct_bone_lengths()
	if bpy.context.scene.selected_miscellaneous_tools == "import_nala":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		import_nala()
	if bpy.context.scene.selected_miscellaneous_tools == "fix_object_axis":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		fix_object_axis()




@register_wrap
class MiscellaneousTools(bpy.types.Operator):
	"""Miscellanous Tools"""
	bl_idname = "ffxiv_mmd_tools_helper.miscellaneous_tools"
	bl_label = "Miscellaneous Tools"

	bpy.types.Scene.selected_miscellaneous_tools = bpy.props.EnumProperty(items = \
	[('none', 'none', 'none')\
	, ("import_nala", "import_nala","import_nala") \
	, ("fix_object_axis", "fix object axis","fix object axis") \
	, ("combine_2_bones", "Combine 2 bones", "Combine a parent-child pair of bones and their vertex groups to 1 bone and 1 vertex group")\
	, ("delete_unused", "Delete unused bones and unused vertex groups", "Delete all bones and vertex groups which have the word 'unused' in them")\
	, ("mmd_ambient_white", "All materials MMD ambient color white", "Change the MMD ambient color of all materials to white")\
	, ("correct_root_center", "Correct MMD Root and Center bones", "Correct MMD root and center bones")\
	, ("correct_groove", "Correct MMD Groove bone", "Correct MMD Groove bone")\
	, ("correct_waist", "Correct MMD Waist bone", "Correct MMD Waist bone")\
	, ("correct_waist_cancel", "Correct waist cancel left and right bones", "Correct waist cancel left and right bones")\
	, ("correct_view_cnt", "Correct MMD 'view cnt' bone", "Correct MMD 'view cnt' bone")\
	, ("create_bone_groups", "Create Bone Groups", "Create Bone Groups")\
	, ("correct_bone_lengths", "Correct Bone Lengths and Roll", "Correct Bone Lengths and Roll")\
	], name = "Select Function:", default = 'none')

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}