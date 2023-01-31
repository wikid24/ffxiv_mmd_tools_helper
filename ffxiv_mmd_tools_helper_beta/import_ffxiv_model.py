import bpy
import math

from . import register_wrap
from . import model
from . import miscellaneous_tools
from . import boneMaps_renamer
from . import add_foot_leg_ik

"""
@register_wrap
class ImportFFXIVTestModelPanel(bpy.types.Panel):
	#Import FFXIV Test Model panel
	bl_label = "Import FFXIV Test Model Panel"
	bl_idname = "OBJECT_PT_import_ffxiv_model"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout

		row = layout.row()
		layout.prop(context.scene, "selected_ffxiv_test_model")
		row = layout.row()
		row.label(text="Import FFXIV Model", icon='WORLD_DATA')
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.import_ffxiv_model", text = "Execute Function")
"""

def import_nala():


	bpy.ops.import_scene.fbx( \
	filepath=r'C:\Users\wikid\OneDrive\Documents\TexTools\Saved\FullModel\Nala V3\Nala V3.fbx'\
	, primary_bone_axis='X' \
	, secondary_bone_axis='Y' \
	, use_manual_orientation=True \
	, axis_forward='Y' \
	, axis_up='Z'
	)

	#####move all 'Group' objects to an empty object called 'FFXIV Junk'####
	# Get the selected object
	selected_obj = bpy.context.object #should be n_root
	selected_obj_parent = selected_obj.parent #should be imported object name (Nala V3)

	bpy.context.view_layer.objects.active = selected_obj_parent

	# Create a new empty object to store all the junk that comes from FFXIV
	bpy.ops.object.add(type='EMPTY', location=(0, 0, 0))
	new_empty = bpy.context.object
	new_empty.name = 'FFXIV Junk'
	print (new_empty)

	# Parent the new empty object to the selected object
	new_empty.parent = selected_obj_parent

	# Iterate through all children of the selected object
	for child in selected_obj_parent.children:
		# Check if the child object contains the substring 'Group' in its name
		if 'Group' in child.name:
			# Parent the child object to the new empty object
			child.parent = new_empty
			
	#####move all 'Mesh-type' objects to an empty object called 'Mesh'####
	bpy.context.view_layer.objects.active = selected_obj
		
	"""
	# Create a new empty object to store all the Mesh Objects
	bpy.ops.object.add(type='EMPTY', location=(0, 0, 0))
	new_empty = bpy.context.object
	new_empty.name = 'FFXIV Mesh'
	new_empty.parent = selected_obj

	# Iterate through all children of the selected object
	for child in selected_obj.children:
		# Check if the child object contains the substring 'Group' in its name
		if 'Part' in child.name:
			# Parent the child object to the new empty object
			child.parent = new_empty
	"""
	
	###### Fix the alpha blend mode so that all the textures can be viewed properly ######
	mats = bpy.data.materials
	for mat in mats:
		mat.blend_method = 'HASHED'

	##### add the" mmd_bone_order_override" armature modifier to the FIRST mesh on n_root (as per the MMD Tools instructions)####
	# Get the armature object
	armature = bpy.data.objects.get("n_root")
	# Get the first mesh object that is a child of the armature
	mesh = [child for child in armature.children if child.type == 'MESH'][0]
	
	mmd_bone_order_override_modifier = None

	for modifier in mesh.modifiers:
		if modifier.type == 'ARMATURE' and modifier.object.name in ('n_root','mmd_bone_order_override'):
			mmd_bone_order_override_modifier = modifier
			mmd_bone_order_override_modifier.name = 'mmd_bone_order_override'
			break

	if mmd_bone_order_override_modifier == None:
		# Add the armature modifier to the mesh
		mmd_bone_order_override_modifier = mesh.modifiers.new(name="mmd_bone_order_override", type='ARMATURE')
		# Set the armature as the object to which the modifier applies
		mmd_bone_order_override_modifier.object = armature
		mmd_bone_order_override_modifier.object = bpy.data.objects["n_root"]




def import_ffxiv_model(ffxiv_model):

	file_path = (__file__ + "\\ffxiv models\\" + ffxiv_model + "\\" + ffxiv_model + ".fbx").replace("import_ffxiv_model.py" , "")
	print(file_path)
	
	bpy.ops.import_scene.fbx( \
	filepath = file_path \
	, primary_bone_axis='X' \
	, secondary_bone_axis='Y' \
	, use_manual_orientation=True \
	, axis_forward='Y' \
	, axis_up='Z'
	)


	#####move all 'Group' objects to an empty object called 'FFXIV Junk'####
	# Get the selected object
	selected_obj = bpy.context.object #should be n_root
	selected_obj_parent = selected_obj.parent #should be imported object name (Nala V3)

	bpy.context.view_layer.objects.active = selected_obj_parent

	# Create a new empty object to store all the junk that comes from FFXIV
	bpy.ops.object.add(type='EMPTY', location=(0, 0, 0))
	new_empty = bpy.context.object
	new_empty.name = 'FFXIV Junk'
	print (new_empty)

	# Parent the new empty object to the selected object
	new_empty.parent = selected_obj_parent

	# Iterate through all children of the selected object
	for child in selected_obj_parent.children:
		# Check if the child object contains the substring 'Group' in its name
		if 'Group' in child.name:
			# Parent the child object to the new empty object
			child.parent = new_empty
			
	#####move all 'Mesh-type' objects to an empty object called 'Mesh'####
	bpy.context.view_layer.objects.active = selected_obj
		
			
	# Create a new empty object to store all the Mesh Objects
	bpy.ops.object.add(type='EMPTY', location=(0, 0, 0))
	new_empty = bpy.context.object
	new_empty.name = 'FFXIV Mesh'
	new_empty.parent = selected_obj

	# Iterate through all children of the selected object
	for child in selected_obj.children:
		# Check if the child object contains the substring 'Group' in its name
		if 'Part' in child.name:
			# Parent the child object to the new empty object
			child.parent = new_empty

	###### Fix the alpha blend mode so that all the textures can be viewed properly ######
	mats = bpy.data.materials
	for mat in mats:
		mat.blend_method = 'HASHED'

	##### add the" mmd_bone_order_override" armature modifier to the FIRST mesh on n_root (as per the MMD Tools instructions)####
	# Get the armature object
	armature = bpy.data.objects.get("n_root")
	# Get the first mesh object that is a child of the armature
	mesh = [child for child in armature.children if child.type == 'MESH'][0]
	
	mmd_bone_order_override_modifier = None

	for modifier in mesh.modifiers:
		if modifier.type == 'ARMATURE' and modifier.object.name in ('n_root','mmd_bone_order_override'):
			mmd_bone_order_override_modifier = modifier
			mmd_bone_order_override_modifier.name = 'mmd_bone_order_override'
			break

	if mmd_bone_order_override_modifier == None:
		# Add the armature modifier to the mesh
		mmd_bone_order_override_modifier = mesh.modifiers.new(name="mmd_bone_order_override", type='ARMATURE')
		# Set the armature as the object to which the modifier applies
		mmd_bone_order_override_modifier.object = armature
		mmd_bone_order_override_modifier.object = bpy.data.objects["n_root"]

	

def main(context):

	if bpy.context.scene.selected_ffxiv_test_model == "import_nala":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		import_nala()
	elif bpy.context.scene.selected_ffxiv_test_model == "import_nala_deluxe":
		bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		import_nala()
		miscellaneous_tools.fix_object_axis()
		boneMaps_renamer.main(context)
		miscellaneous_tools.correct_root_center()
		miscellaneous_tools.correct_groove()
		miscellaneous_tools.correct_waist()
		miscellaneous_tools.correct_waist_cancel()
		add_foot_leg_ik.main(context)
	else:
		import_ffxiv_model(bpy.context.scene.selected_ffxiv_test_model)


@register_wrap
class ImportFFXIVModel(bpy.types.Operator):
	"""Import FFXIV Test Model"""
	bl_idname = "ffxiv_mmd_tools_helper.import_ffxiv_model"
	bl_label = "Import FFXIV Test Model"

	bpy.types.Scene.selected_ffxiv_test_model = bpy.props.EnumProperty(items = \
	[('none', 'none', 'none')\
	, ("import_nala", "import_nala","import_nala") \
	, ("import_nala_deluxe", "import_nala_deluxe","import_nala_deluxe") \
	, ("AuRa female", "AuRa female","AuRa female") \
	, ("Elezen Female", "Elezen Female","Elezen Female") \
	, ("Hrothgar Male", "Hrothgar Male","Hrothgar Male") \
	, ("Hyur Highlander Female", "Hyur Highlander Female","Hyur Highlander Female") \
	, ("Hyur Midlander Female", "Hyur Midlander Female","Hyur Midlander Female") \
	, ("Lalafell Female", "Lalafell Female","Lalafell Female") \
	, ("Miqote Female", "Miqote Female","Miqote Female") \
	, ("Roegadyn Female", "Roegadyn Female","Roegadyn Female") \
	, ("Viera Female", "Viera Female","Viera Female") \
	
	], name = "Select Model to Import:", default = 'none')
	

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}