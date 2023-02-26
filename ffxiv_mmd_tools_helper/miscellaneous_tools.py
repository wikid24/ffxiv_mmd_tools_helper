import bpy
import math
from . import register_wrap
from . import model
from mmd_tools.core.bone import FnBone
from . import rigid_body
from . import bone_tools


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

	bpy.ops.object.mode_set(mode='POSE')

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

def flag_unused_bones():
	armature = model.findArmature(bpy.context.active_object)
	root = armature.parent


	#check if bone has any attached rigid bodies, or vertex groups. If it has neither, delete it.
	#ignore D bones, IK bones, and shoulder P & C bones.
	#need to add:ignore hidden bones or bones on another layer

	if armature is not None:
		bpy.ops.object.mode_set(mode='EDIT')

		#Get bones from the metadata dictionary
		target_columns = ['mmd_english', 'mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv']
		FFXIV_BONE_METADATA_DICTIONARY = bone_tools.get_csv_metadata_by_bone_type("is_special", target_columns)


		for b in bpy.context.active_object.pose.bones:
			has_rigid = False
			has_vg = False
			is_special = False

			#check if bone has any constraints
			if len(b.constraints.items()) > 0:
				is_special = True

			#check if bone is a special MMD Tools bone
			if b.name.startswith('_dummy') or b.name.startswith('_shadow'):
				is_special = True
			
			#check if bone is on the 'is_special' list
			for metadata_bone in FFXIV_BONE_METADATA_DICTIONARY:
				if b.name == metadata_bone[1]:
					is_special = True
					break

			if is_special == False:		
				for obj in root.children_recursive:
					#check for vertex groups
					if obj.type =='MESH':
						for vg in obj.vertex_groups:
							if vg.name == b.name:
								if vg.name == 'j_mune_r':
									print (vg.name,' found on ',obj.name)
								has_vg = True
								break
					#check for rigid bodies
					if obj.mmd_type == 'RIGID_BODY':
						if b == rigid_body.get_bone_from_rigid_body(obj):
							has_rigid = True
							break
				
				for b2 in bpy.context.active_object.pose.bones:
					#check if bone is used as a transform bone
					if b2.mmd_bone.additional_transform_bone == b.name:
						is_special = True
						break
					#check if bone is used as an IK bone
					if 'IK' in b2.constraints.keys():
						if b2.constraints['IK'].subtarget == b.name:
							is_special = True
							break

			if has_rigid == False and has_vg == False and is_special == False:
				if b.name.startswith('_unused_'):
					b.name = b.name
				else:
					b.name = '_unused_' + b.name
			"""
			#if it magically got used, remove the '_unused_' part of the name
			else:
				if b.name.startswith('_unused_'):
					b.name.replace('_unused_','')
			"""



	else:
		print('\n Cannot find an armature. Please select an armature first.'), 

def delete_unused_bones():
	armature = model.findArmature(bpy.context.active_object)
	#root = armature.parent


	if armature is not None:
		bpy.ops.object.mode_set(mode='EDIT')

		#Get bones from the metadata dictionary
		target_columns = ['mmd_english', 'mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv']
		FFXIV_BONE_METADATA_DICTIONARY = bone_tools.get_csv_metadata_by_bone_type("is_special", target_columns)


		for b in armature.data.edit_bones:
			if b.name.startswith('_unused_'):
				bpy.data.armatures[armature.name].edit_bones.remove(b)




def add_bone_to_group (bone_name,bone_group):
	if bone_name in bpy.context.active_object.pose.bones:
		bone = bpy.context.active_object.pose.bones[bone_name]
		bone.bone_group = bpy.context.active_object.pose.bone_groups[bone_group]
	else:
		print("bone: " +  bone_name + " does not exist in currently selected object")




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

	selected_miscellaneous_tools = bpy.context.scene.selected_miscellaneous_tools

	if selected_miscellaneous_tools == "combine_2_bones":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		parent_bone_name, child_bone_name = analyze_selected_parent_child_bone_pair()
		if parent_bone_name is not None:
			if child_bone_name is not None:
				combine_2_vg_1_vg(parent_bone_name, child_bone_name)
				combine_2_bones_1_bone(parent_bone_name, child_bone_name)
	if selected_miscellaneous_tools == "flag_unused_bones":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		flag_unused_bones()
		#delete_unused_vertex_groups()
	if selected_miscellaneous_tools == "delete_unused_bones":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		#flag_unused_bones()
		delete_unused_bones()
	if selected_miscellaneous_tools == "mmd_ambient_white":
		all_materials_mmd_ambient_white()
	if selected_miscellaneous_tools == "fix_object_axis":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		fix_object_axis()
	


@register_wrap
class MiscellaneousTools(bpy.types.Operator):
	"""Execute Function"""
	bl_idname = "ffxiv_mmd_tools_helper.miscellaneous_tools"
	bl_label = "Miscellaneous Tools"
	bl_options = {'REGISTER', 'UNDO'}
	

	bpy.types.Scene.selected_miscellaneous_tools = bpy.props.EnumProperty(items = \
	[('none', 'none', 'none')\
	, ("fix_object_axis", "Fix Object Axis (90 degrees)","Fix Object Axis (90 degrees)") \
	, ("combine_2_bones", "Combine 2 bones", "Combine a parent-child pair of bones and their vertex groups to 1 bone and 1 vertex group")\
	, ("flag_unused_bones", "Flag unused bones as '_unused_'", "Flag non-special bones with no vertex groups/constraints/rigid bodies as '_unused_'")\
	, ("delete_unused_bones", "Delete '_unused_' bones", "Delete all bones which start with '_unused_' in them")\
	#, ("mmd_ambient_white", "All materials MMD ambient color white", "Change the MMD ambient color of all materials to white")\
	], name = "", default = 'none')

	@classmethod
	def poll(cls, context):
		obj = context.active_object 
		return obj is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}