import bpy
from . import register_wrap
from . import import_csv
import json



def parse_chara_file(file_path):


	#CHARAFILE_DICTIONARY = import_csv.use_csv_charafile_dictionary()

	print(file_path)

	
	# Open and read the JSON file
	with open(file_path, 'r') as file:
		# Store the results in a dictionary
		charafile_data = json.load(file)

	
	#charafile_data = data

	"""
	# Extract the value associated with the 'Eyebrows' key
	if 'Eyebrows' in my_dict:
		eyebrows_value = my_dict['Eyebrows']
		print("Value for 'Eyebrows':", eyebrows_value)
	else:
		print("Key 'Eyebrows' not found in the JSON data.")

		print(my_dict)
	"""
	# Define CHARAFILE_DICTIONARY containing the list of keys to check
	CHARAFILE_KEYS = {
		'Eyes',
		'Eyebrows',
		'Mouth',
		'Nose',
		'Jaw',
		'Race',
		'Tribe',
		'Gender',
		'SkinGloss',
		'BustScale',
		'FacialFeatures'
	}

	# Create a dictionary to store the results
	result_dict = {}

	# Loop through charafile_data to find only matching data from CHARAFILE_KEYS
	for charafile_key in CHARAFILE_KEYS:
		for key in charafile_data:
			if charafile_key == key:
				if key == 'Eyes' and int(charafile_data[key]) >=128:
					result_dict[key] = int(charafile_data[key]) - 128
				elif key == 'Mouth' and int(charafile_data[key]) >=128:
					result_dict[key] = int(charafile_data[key]) - 128	
				else:
					result_dict[key] = charafile_data[key]

	# Print the results
	#print("Results for CHARAFILE_DICTIONARY keys:")
	#for key, value in result_dict.items():
	#	print(f"{key}: {value}")


	CHARAFILE_DICTIONARY = import_csv.use_csv_charafile_dictionary()
	#for row in CHARAFILE_DICTIONARY:
	#	print (f"{row[0]}:{row[1]}:{row[2]}")


	#loop thorough CHARAFILE_DICTIONARY to find values that match charafile_data
	for key, value in result_dict.items():
		for row in CHARAFILE_DICTIONARY:
			if key == row[0] and str(value) == (row[1]):
				#print (f"{row[0]}:{row[1]}:{row[2]}")
				if row[2] != '':
					#turn on all shape keys that match the results
					enable_shape_keys(row[2])
					#print (row[2])

	#shapekeys that need to be enabled
	#for 

	#return my_dict


	
def enable_shape_keys(shape_key_name):
	print (shape_key_name + " is going to be modified!")

	# Get the currently selected armature
	selected_armature = bpy.context.active_object

	if selected_armature and selected_armature.type == 'ARMATURE':
		# Create a list to store the meshes that are children of the armature
		child_meshes = []

		# Iterate through all objects in the scene
		for obj in bpy.context.scene.objects:
			if obj.type == 'MESH' and obj.parent and obj.parent.type == 'ARMATURE' and obj.parent.name == selected_armature.name:
				child_meshes.append(obj)


		# Check for 'shp_nse_c' shape key and set its value to 1 if found
		for mesh in child_meshes:
			if hasattr(mesh.data.shape_keys, 'key_blocks'):
				shape_key_block = mesh.data.shape_keys.key_blocks.get(shape_key_name)
				if shape_key_block:
					# Set the shape key's value to 1
					shape_key_block.value = 1.0
					print(f"{shape_key_block.name} is going to be modified!")
				#elif shape_key_block.value:
					#shape_key_block.value = 0
	"""
	# Get the currently selected armature
	selected_armature = bpy.context.active_object

	if selected_armature and selected_armature.type == 'ARMATURE':
		# Loop through all the materials applied to the armature
		for material in selected_armature.data.materials:
			if material:
				# Check if the material has shape keys
				if hasattr(material, 'shape_keys') and material.shape_keys:
					shape_key_block = material.shape_keys.key_blocks.get('shp_nse_c')
					if shape_key_block:
						# Set the shape key's value to 1
						shape_key_block.value = 1.0

	"""


def main(context):
	print ('im in main()')

from bpy_extras.io_utils import ImportHelper
@register_wrap
class FFXIV_CharaFileBrowserImportOperator(bpy.types.Operator, ImportHelper):
	"""Operator that opens the file browser dialog for .chara files from Anamnesis"""
	bl_idname = "ffxiv_mmd.ffxiv_chara_file_browser_operator"
	bl_label = "Chara File Browser Operator"
	bl_options = {'REGISTER', 'UNDO'}

	filename_ext = ".chara"
	filter_glob: bpy.props.StringProperty(
		default="*.chara",
		options={'HIDDEN'},
	)

	def execute(self, context):
		filepath = self.filepath
		# Add code here to process the selected file
		print (filepath)
		parse_chara_file(filepath)

		return {'FINISHED'}



@register_wrap
class ImportFFXIVModel(bpy.types.Operator):
	"""Import FFXIV Test Model"""
	bl_idname = "ffxiv_mmd.import_ffxiv_model2"
	bl_label = "Import FFXIV Test Model"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.selected_ffxiv_test_model2 = bpy.props.EnumProperty(items = \
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
	
	], name = "Sample", default = 'none')
	
	"""
	@classmethod
	def poll(cls, context):
		return context.active_object is not None
	"""
	def execute(self, context):
		main(context)
		return {'FINISHED'}