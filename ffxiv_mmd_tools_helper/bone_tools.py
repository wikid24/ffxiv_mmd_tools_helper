import bpy
from . import register_wrap
from . import model
from . import import_csv
import mmd_tools.core.model as mmd_model



def add_bone(armature, bone_name, parent_bone, length=None, head=None, tail=None,use_connect=None):
	
	new_bone = None

	# Create a new bone
	if (bone_name) not in bpy.context.active_object.data.edit_bones.keys():
		new_bone = armature.data.edit_bones.new(bone_name)
	else:
		new_bone = bpy.context.active_object.data.edit_bones[bone_name]
	# Set the length of the bone
	if head is not None:
		new_bone.head = head
	if tail is not None:
		new_bone.tail = tail
	if length is not None:
		new_bone.length = length
	# Point the bone directly upwards
	new_bone.roll = 0
	msg = 'added bone ' + bone_name

	if parent_bone.name in bpy.context.active_object.data.edit_bones.keys():
		new_bone.parent = parent_bone
		msg += ' parented to ' + parent_bone.name

	if use_connect is not None:
		new_bone.use_connect = use_connect
	
	print(msg)
	
	return new_bone



def get_csv_metadata_by_bone_type(metadata_column, bone_types):

	csv_data = import_csv.use_csv_bone_metadata_ffxiv_dictionary()

	#get the header column
	header = csv_data[0]
	#get the index of the column we need
	metadata_index = header.index(metadata_column)
	#get the index of the bone types passed to it
	bone_type_indices = [header.index(target_column) for target_column in bone_types]
	
	#set() means it will not add something if it already is on the list
	bone_list = set()
	
	for bone_type in bone_type_indices:
		for row in csv_data[1:]:
			#filter out any blank columns from the metadata_index column
			if row[metadata_index] is not None:
				#filter out any values where the bone type is None
				if row[bone_type] is not None:			
					bone_list.add((row[metadata_index],row[bone_type]))

	#sort the list by the first column
	sorted_bone_list = sorted(bone_list, key=lambda x: x[0])
	return sorted_bone_list

def hide_special_bones(armature):

	#Get bones from the metadata dictionary
	target_columns = ['mmd_english', 'mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv']
	FFXIV_BONE_METADATA_DICTIONARY = get_csv_metadata_by_bone_type("hidden", target_columns)

	if FFXIV_BONE_METADATA_DICTIONARY is not None:

		bpy.ops.object.mode_set(mode='POSE')

		for pbone in armature.pose.bones:
			pbone.bone.select = False

		for pbone in armature.pose.bones:
			for metadata_bone in FFXIV_BONE_METADATA_DICTIONARY:
				if pbone.name == metadata_bone[1]:
					pbone.bone.select = True
		
		#hide all selected bones
		bpy.ops.pose.hide()




def get_csv_metadata_by_bone_type(metadata_column, bone_types):

	csv_data = import_csv.use_csv_bone_metadata_ffxiv_dictionary()

	#get the header column
	header = csv_data[0]
	#get the index of the column we need
	metadata_index = header.index(metadata_column)
	#get the index of the bone types passed to it
	bone_type_indices = [header.index(target_column) for target_column in bone_types]
	
	#set() means it will not add something if it already is on the list
	bone_list = set()
	
	for bone_type in bone_type_indices:
		for row in csv_data[1:]:
			#filter out any blank columns from the metadata_index column
			if row[metadata_index] is not None:
				#filter out any values where the bone type is None
				if row[bone_type] is not None:			
					bone_list.add((row[metadata_index],row[bone_type]))

	#sort the list by the first column
	sorted_bone_list = sorted(bone_list, key=lambda x: x[0])
	return sorted_bone_list

#MOVE VERTEX GROUP / BONE ORDER TO A SPECIFIC POSITION
def vgmove(delta):
	direction = 'UP' if delta > 0 else 'DOWN'
	for i in range(abs(delta)):
		bpy.ops.object.vertex_group_move(direction=direction)

def move_vg_to_pos(mesh, vg_name, target_pos):    
	
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.context.view_layer.objects.active = mesh
	#search for vg_name in mesh

	for vg in mesh.vertex_groups:
	
		if vg.name == vg_name:
			#set the active index to the matching criteria
			print(mesh.name,'-', vg_name,'-', target_pos)
			mesh.vertex_groups.active_index = vg.index
			#get delta from the current index position to the target position
			delta = vg.index - min(target_pos, len(mesh.vertex_groups) - 1)
			#call vgmove to set the vg to that specific position
			vgmove(delta)        

def set_mmd_bone_order(armature):

	#Get bones from the metadata dictionary
	target_columns = ['mmd_english', 'mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv']
	FFXIV_BONE_METADATA_DICTIONARY = get_csv_metadata_by_bone_type("PMXE_bone_order", target_columns)

	if FFXIV_BONE_METADATA_DICTIONARY is not None:

		bpy.ops.object.mode_set(mode='POSE')

		mmd_bone_order_list = []
		
		#run through the bone dictionary
		for metadata_bone in FFXIV_BONE_METADATA_DICTIONARY:
			for pbone in armature.pose.bones:
				#if it finds a match
				if pbone.name == metadata_bone[1]:
					#append it to the list as well as the bone order number
					mmd_bone_order_list.append ((pbone.name,metadata_bone[0]))
		
		#sort the list according to the bone order number (cast to int first since bone order is treated as a string)
		mmd_bone_order_list.sort(key=lambda x: int(x[1]))

		sorted_mmd_bone_order_list = []        

		#enumerate the list so gaps between the bone order numbers are ignored
		for i,mmd_bone in enumerate(mmd_bone_order_list):
			sorted_mmd_bone_order_list.append((mmd_bone[0],i))            
		
		#get the mesh that holds the bone_order_override modifier    
		root_object = mmd_model.FnModel.find_root(bpy.context.active_object)
		bone_order_mesh_object = mmd_model.FnModel.find_bone_order_mesh_object(root_object)
	
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.context.view_layer.objects.active = bone_order_mesh_object
	
		#add missing vertex groups
		mmd_model.FnModel.add_missing_vertex_groups_from_bones(root_object, bone_order_mesh_object, search_in_all_meshes=True)
	
		#since bones should have same name as vertex group in bone_order_override, can just call the function
		for i,bone in enumerate(sorted_mmd_bone_order_list):
			move_vg_to_pos(bone_order_mesh_object, bone[0],i)

	#Get deformation tier from the metadata dictionary
	target_columns = ['mmd_english', 'mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv']
	FFXIV_BONE_METADATA_DICTIONARY = get_csv_metadata_by_bone_type("PMXE_deform_tier", target_columns)

	if FFXIV_BONE_METADATA_DICTIONARY is not None:

		bpy.context.view_layer.objects.active = armature

		bpy.ops.object.mode_set(mode='POSE')

		mmd_bone_order_list = []
		
		#run through the bone dictionary
		for metadata_bone in FFXIV_BONE_METADATA_DICTIONARY:
			for pbone in armature.pose.bones:
				#if it finds a match
				if pbone.name == metadata_bone[1]:
					pbone.mmd_bone.transform_order = int(metadata_bone[0])

def lock_position_rotation_bones(armature):

	#Get bones from the metadata dictionary
	target_columns = ['mmd_english', 'mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv']
	FFXIV_BONE_METADATA_DICTIONARY = get_csv_metadata_by_bone_type("disable_rotate", target_columns)

	if FFXIV_BONE_METADATA_DICTIONARY is not None:

		bpy.ops.object.mode_set(mode='POSE')
		
		#run through the bone dictionary
		for metadata_bone in FFXIV_BONE_METADATA_DICTIONARY:
			for pbone in armature.pose.bones:
				#if it finds a match
				if pbone.name == metadata_bone[1]:
					pbone.lock_rotation[0] = True
					pbone.lock_rotation[1] = True
					pbone.lock_rotation[2] = True
					pbone.lock_rotation_w = True


	#Get bones from the metadata dictionary
	target_columns = ['mmd_english', 'mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv']
	FFXIV_BONE_METADATA_DICTIONARY = get_csv_metadata_by_bone_type("disable_move", target_columns)

	if FFXIV_BONE_METADATA_DICTIONARY is not None:

		bpy.ops.object.mode_set(mode='POSE')
		
		#run through the bone dictionary
		for metadata_bone in FFXIV_BONE_METADATA_DICTIONARY:
			for pbone in armature.pose.bones:
				#if it finds a match
				if pbone.name == metadata_bone[1]:
					pbone.lock_location[0] = True
					pbone.lock_location[1] = True
					pbone.lock_location[2] = True			


def set_fixed_axis_local_axis_bones(armature):

	#Get bones from the metadata dictionary
	target_columns = ['mmd_english', 'mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv']
	FFXIV_BONE_METADATA_DICTIONARY = get_csv_metadata_by_bone_type("fixed_axis", target_columns)

	if FFXIV_BONE_METADATA_DICTIONARY is not None:

		bpy.ops.object.mode_set(mode='POSE')
		
		#run through the bone dictionary
		for metadata_bone in FFXIV_BONE_METADATA_DICTIONARY:
			for pbone in armature.pose.bones:
				#if it finds a match
				if pbone.name == metadata_bone[1]:
					print("fixed axis:",pbone.name)
					pbone.mmd_bone.enabled_fixed_axis = True
					bpy.context.active_object.data.bones.active = armature.data.bones[pbone.name]
					bpy.ops.mmd_tools.bone_fixed_axis_setup(type='LOAD')
					#bpy.ops.mmd_tools.bone_fixed_axis_setup(type='APPLY')



	#Get bones from the metadata dictionary
	target_columns = ['mmd_english', 'mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv']
	FFXIV_BONE_METADATA_DICTIONARY = get_csv_metadata_by_bone_type("local_axis", target_columns)

	if FFXIV_BONE_METADATA_DICTIONARY is not None:

		bpy.ops.object.mode_set(mode='POSE')
		
		#run through the bone dictionary
		for metadata_bone in FFXIV_BONE_METADATA_DICTIONARY:
			for pbone in armature.pose.bones:
				#if it finds a match
				if pbone.name == metadata_bone[1]:
					print("local axis:",pbone.name)
					pbone.mmd_bone.enabled_local_axes = True
					bpy.context.active_object.data.bones.active = armature.data.bones[pbone.name]
					bpy.ops.mmd_tools.bone_local_axes_setup(type='LOAD')
					#bpy.ops.mmd_tools.bone_local_axes_setup(type='APPLY')

def auto_fix_mmd_bone_names(armature):

	#Get bones from the metadata dictionary
	target_columns = ['mmd_english', 'mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv']
	FFXIV_BONE_METADATA_DICTIONARY_MMD_J = get_csv_metadata_by_bone_type("mmd_japanese", target_columns)
	FFXIV_BONE_METADATA_DICTIONARY_MMD_E = get_csv_metadata_by_bone_type("mmd_english", target_columns)

	if FFXIV_BONE_METADATA_DICTIONARY_MMD_J is not None:

		bpy.ops.object.mode_set(mode='POSE')
		
		#run through the MMD Japanese bone dictionary
		for metadata_bone in FFXIV_BONE_METADATA_DICTIONARY_MMD_J:
			for pbone in armature.pose.bones:
				#if MMD Japanese bone name is empty, set it to the blender bone name
				if pbone.mmd_bone.name_j.strip() == '':
					pbone.mmd_bone.name_j = pbone.name
				
				#if it finds a match with any of the bones from the csv, set it to the MMD Japanese name
				if pbone.mmd_bone.name_j.strip() == metadata_bone[1]:
					pbone.mmd_bone.name_j = metadata_bone[0]

		#run through the MMD English bone dictionary
		for metadata_bone in FFXIV_BONE_METADATA_DICTIONARY_MMD_E:
			for pbone in armature.pose.bones:
				#if MMD English bone name is empty, set it to the blender bone name
				if pbone.mmd_bone.name_e.strip() == '':
					pbone.mmd_bone.name_e = pbone.name
				
				#if it finds a match with any of the bones from the csv, set it to the MMD English name
				if pbone.mmd_bone.name_e.strip() == metadata_bone[1]:
					pbone.mmd_bone.name_e = metadata_bone[0]
		
					
				

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

@register_wrap
class SortMMDBoneOrder(bpy.types.Operator):
	"""Auto Sorts the MMD Bone Order & Deformation Tiers"""
	bl_idname = "ffxiv_mmd_tools_helper.sort_mmd_bone_order"
	bl_label = "Sort MMD Bone Order/Deformation Tiers"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		root = mmd_model.Model.findRoot(obj)
		return obj is not None and obj.type == 'ARMATURE' and root is not None

	def execute(self, context):
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		set_mmd_bone_order(armature)
		return {'FINISHED'}

@register_wrap
class HideSpecial_Bones(bpy.types.Operator):
	"""Hides Bones for Export to MMD"""
	bl_idname = "ffxiv_mmd_tools_helper.hide_special_bones"
	bl_label = "Hides Special/Physics Bones for Export to MMD"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		hide_special_bones(armature)
		return {'FINISHED'}

@register_wrap
class LockPositionRotation_Bones(bpy.types.Operator):
	"""Locks Position & Rotation of Bones for Export to MMD"""
	bl_idname = "ffxiv_mmd_tools_helper.lock_position_rotation_bones"
	bl_label = "Hides Special/Physics Bones for Export to MMD"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		lock_position_rotation_bones(armature)
		return {'FINISHED'}

@register_wrap
class SetFixedAxisLocalAxis_Bones(bpy.types.Operator):
	"""Sets Fixed Axis/Local Axis for Export to MMD"""
	bl_idname = "ffxiv_mmd_tools_helper.set_fixed_axis_local_axis_bones"
	bl_label = "Hides Special/Physics Bones for Export to MMD"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		set_fixed_axis_local_axis_bones(armature)
		return {'FINISHED'}


@register_wrap
class AutoFixMMDBoneNames(bpy.types.Operator):
	"""If MMD bone name is empty, sets to Blender Bone name, then check if MMD bone matches a bone on metadata dictionary, sets it to the MMD Japanese/English equivalent"""
	bl_idname = "ffxiv_mmd_tools_helper.auto_fix_mmd_bone_names"
	bl_label = "If MMD bone name is empty, sets to Blender Bone name, then if it matches a bone on metadata dictionary, sets it to the MMD Japanese/English equivalent"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		auto_fix_mmd_bone_names(armature)
		return {'FINISHED'}
