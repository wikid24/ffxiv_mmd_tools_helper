import bpy
import math

from . import register_wrap
from . import model

@register_wrap
class ImportFFXIVTestModelPanel(bpy.types.Panel):
	"""Import FFXIV Test Model panel"""
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


def import_ffxiv_model(ffxiv_model):

	file_path = (__file__ + "\\ffxiv models\\" + ffxiv_model + "\\" + ffxiv_model + ".fbx").replace("import_ffxiv_test_model.py" , "")
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
	

def main(context):

	import_ffxiv_model(bpy.context.scene.selected_ffxiv_test_model)
	

@register_wrap
class ImportFFXIVModel(bpy.types.Operator):
	"""Import FFXIV Test Model"""
	bl_idname = "ffxiv_mmd_tools_helper.import_ffxiv_model"
	bl_label = "Import FFXIV Test Model"

	bpy.types.Scene.selected_ffxiv_test_model = bpy.props.EnumProperty(items = \
	[('none', 'none', 'none')\
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