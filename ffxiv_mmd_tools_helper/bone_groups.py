import bpy
from . import register_wrap
from . import model
from . import bone_tools


def __items(display_item_frame):
	return getattr(display_item_frame, 'data', display_item_frame.items)


def add_bone_to_group (bone_name,bone_group):
	#create bone group if it doesn't exist
	if bone_group not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name=bone_group)
		print(f"Bone group '{bone_group}' created")
	#add bone to bone group
	if bone_name in bpy.context.active_object.pose.bones:
		bone = bpy.context.active_object.pose.bones[bone_name]
		bone.bone_group = bpy.context.active_object.pose.bone_groups[bone_group]

def delete_bone_groups():
	# Get the currently selected armature
	armature = model.find_MMD_Armature(bpy.context.object)

	# Check if the selected object is an armature
	if armature.type != 'ARMATURE':
		print("Error: Please select an armature.")
		return
	
	# Delete all bone groups
	for group in armature.pose.bone_groups:
		armature.pose.bone_groups.remove(group)
	print("All bone groups deleted.")



def main(context):
	"""
	armature_object = model.findArmature(bpy.context.active_object)
	bpy.context.view_layer.objects.active = armature_object
	if model.findRoot(bpy.context.active_object) is None:
		bpy.ops.mmd_tools.convert_to_mmd_model()
	#root = model.findRoot(bpy.context.active_object)
	#mesh_objects_list = model.findMeshesList(bpy.context.active_object)
	"""

	target_columns = ['mmd_english', 'mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv']
	bone_groups_dictionary = bone_tools.get_csv_metadata_by_bone_type("blender_bone_group", target_columns)


	for row in bone_groups_dictionary:
		#print (row[1],":",row[0]) # bone_name, bone_group
		add_bone_to_group(row[1], row[0])
	
	#additional cleanup
	for bone in bpy.context.active_object.pose.bones:
		#if bone name starts with 'j_ex_h', then it belongs in the hair category
		if bone.name.startswith('j_ex_h'):
			add_bone_to_group(bone.name,'hair')
		#if bone name starts with 'skirt_' then it belongs in the skirt category
		elif bone.name.startswith('skirt_'):
			add_bone_to_group(bone.name,'skirt')
		elif bone.bone_group is None:
			add_bone_to_group(bone.name,'other')
	
		
@register_wrap
class BoneGroups(bpy.types.Operator):
	"""Mass add bone names to blender bone groups"""
	bl_idname = "ffxiv_mmd.add_bone_groups"
	bl_label = "Create Display Panel Groups and Add Items"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		main(context)
		return {'FINISHED'}