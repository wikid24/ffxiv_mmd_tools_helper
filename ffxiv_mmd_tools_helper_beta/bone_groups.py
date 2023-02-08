import bpy

from . import register_wrap
from . import model
from . import import_csv



def __items(display_item_frame):
	return getattr(display_item_frame, 'data', display_item_frame.items)

"""
@register_wrap
class MmdToolsBoneGroupsPanel(bpy.types.Panel):
	#Mass add bone groups
	bl_idname = "OBJECT_PT_mmd_add_bone_groups"
	bl_label = "Create Bone Groups"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="Add Bone Groups", icon="ARMATURE_DATA")
		row = layout.row()
		layout.prop (context.scene, "bone_panel_bone_type_options")
		row = layout.row()
		row.operator("object.add_bone_groups", text = "Add Blender bone groups")
		row = layout.row()
"""

def read_bones_metadata_file():
	BONES_METADATA_FFXIV_DICTIONARY = import_csv.use_csv_bone_metadata_ffxiv_dictionary()
	return BONES_METADATA_FFXIV_DICTIONARY

def get_csv_bone_groups(BONES_METADATA_FFXIV):
	# Create an empty set to store the unique values
	bone_groups = set()

	# Get the index of "blender_bone_group" column
	header = BONES_METADATA_FFXIV[0]
	blender_bone_group_index = header.index("blender_bone_group")

	# Iterate over the list, starting from the second row
	for row in BONES_METADATA_FFXIV[1:]:
		# Get the value of the "blender_bone_group" column
		bone_group = row[blender_bone_group_index]
		# Add the value to the set
		bone_groups.add(bone_group)

	# Assign the set to a variable
	bone_groups = list(bone_groups)
	return bone_groups



def get_csv_bones_by_bone_group(BONES_METADATA_FFXIV,target_column):
	
	header = BONES_METADATA_FFXIV[0]
	blender_bone_group_index = header.index("blender_bone_group")
	column_data = header.index(target_column)
	
	# Use a lambda function to filter out the rows where the target_column column is None
	filtered_rows = filter(lambda row: row[column_data] != None, BONES_METADATA_FFXIV[1:])

	

	# Use a dictionary comprehension to group the rows by "blender_bone_group" and extract the target_column's data
	#bones_in_bone_group = {row[blender_bone_group_index]: [row[column_data]] for row in filtered_rows}
	bones_in_bone_group = [(row[blender_bone_group_index],row[column_data]) for row in filtered_rows]
	return bones_in_bone_group

def add_bone_to_group (bone_name,bone_group):
	if bone_group not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name=bone_group)
		print(f"Bone group '{bone_group}' created")
	if bone_name in bpy.context.active_object.pose.bones:
		bone = bpy.context.active_object.pose.bones[bone_name]
		bone.bone_group = bpy.context.active_object.pose.bone_groups[bone_group]
	else:
		print("bone: " +  bone_name + " does not exist in currently selected object")

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



#MOVE VERTEX GROUP / BONE ORDER TO A SPECIFIC POSITION
def vgmove(delta):
    direction = 'UP' if delta > 0 else 'DOWN'
    for i in range(abs(delta)):
        bpy.ops.object.vertex_group_move(direction=direction)

def move_vg_to_pos(mesh, vg_name, target_pos):
    #search for vg_name in mesh
    for vg in mesh.vertex_groups:
        if vg.name == vg_name:
            #set the active index to the matching criteria
            mesh.vertex_groups.active_index = vg.index
            #get delta from the current index position to the target position
            delta = vg.index - min(target_pos, len(mesh.vertex_groups) - 1)
            #call vgmove to set the vg to that specific position
            vgmove(delta)        

#mesh = bpy.data.objects['c1801b0002_top Part 9.0']        
#vg_name = 'waist'
#target_pos = 10

#move_vg_to_pos(mesh,vg_name,target_pos)    



def main(context):
	"""
	armature_object = model.findArmature(bpy.context.active_object)
	bpy.context.view_layer.objects.active = armature_object
	if model.findRoot(bpy.context.active_object) is None:
		bpy.ops.mmd_tools.convert_to_mmd_model()
	#root = model.findRoot(bpy.context.active_object)
	#mesh_objects_list = model.findMeshesList(bpy.context.active_object)
	"""

	BONES_METADATA_DICTIONARY = read_bones_metadata_file()
	sorted_bones = get_csv_bones_by_bone_group(BONES_METADATA_DICTIONARY,bpy.context.scene.bone_panel_bone_type_options)

	for row in sorted_bones:
		#print (row[1],":",row[0]) # bone_group, bone
		add_bone_to_group(row[1], row[0])



		
@register_wrap
class BoneGroups(bpy.types.Operator):
	"""Mass add bone names and shape key names to display panel groups"""
	bl_idname = "object.add_bone_groups"
	bl_label = "Create Display Panel Groups and Add Items"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.bone_panel_bone_type_options = bpy.props.EnumProperty(items = \
		[('mmd_english', 'MMD English', 'MMD English')\
		, ('mmd_japanese', 'MMD Japanese', 'MMD Japanese')\
		, ('mmd_japaneseLR', 'MMD Japanese LR', 'MMD Japanese LR')\
		, ('ffxiv', 'FFXIV', 'FFXIV')\
		], name = "MMD Bone Type Groups :", default = 'ffxiv')


	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		main(context)
		return {'FINISHED'}