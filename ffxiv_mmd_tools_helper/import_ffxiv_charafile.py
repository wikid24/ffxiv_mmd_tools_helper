import bpy
from . import register_wrap
from . import import_csv
import mmd_tools.core.model as mmd_model
import json



def parse_chara_file(file_path):
	
	# Open and read the JSON file
	with open(file_path, 'r') as file:
		# Store the results in a dictionary
		charafile_data = json.load(file)

	
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

				#if value for these keys >= 128, then subtract 128 
				#values higher than 128 is a modifier for some checkboxes in Anamnesis
				#for example if Eyes=128, then Eyes is actually '0' and the 'Small Iris' checkbox is checked in Anamnesis
				#don't ask me why it's coded this way, it's just weird AF
				if key in ['Eyes', 'Eyebrows', 'Mouth', 'Nose', 'Jaw']and int(charafile_data[key]) >=128:
					result_dict[key] = int(charafile_data[key]) - 128
					if key == 'Eyes':
						result_dict['SmallIris'] = 1
						print ("SmallIris:" + str(result_dict['SmallIris']))
				else:
					result_dict[key] = charafile_data[key]


	return result_dict

def apply_face_shape_keys(result_dict):

	CHARAFILE_DICTIONARY = import_csv.use_csv_charafile_dictionary()

	#loop thorough CHARAFILE_DICTIONARY to find values that match charafile_data
	reset_all_shape_keys()
	for key, value in result_dict.items():
		for row in CHARAFILE_DICTIONARY:
			if key == row[0] and str(value) == (row[1]):
				#print (f"{row[0]}:{row[1]}:{row[2]}")
				if row[2] != '':
					#turn on all shape keys that match the results
					enable_shape_keys(row[2])
					print ('shape_key:' + row[2] + " set to 1")


def apply_face_bone_morphs(result_dict):
	
	
	if result_dict['Race'] == 'Hyur':
		bpy.context.scene.bone_morph_ffxiv_model_list = "hyur"
	elif result_dict['Race'] == 'Elezen':
		bpy.context.scene.bone_morph_ffxiv_model_list = "elezen"
	elif result_dict['Race'] == 'Lalafel':
		bpy.context.scene.bone_morph_ffxiv_model_list = "lalafell"
	elif result_dict['Race'] == 'Miqote':
		bpy.context.scene.bone_morph_ffxiv_model_list = "miqote"
	elif result_dict['Race'] == 'Roegadyn':
		bpy.context.scene.bone_morph_ffxiv_model_list = "roegadyn"
	elif result_dict['Race'] == 'Hrothgar':
		bpy.context.scene.bone_morph_ffxiv_model_list = "hrothgar"
	elif result_dict['Race'] == 'AuRa':
		bpy.context.scene.bone_morph_ffxiv_model_list = "aura"
	elif result_dict['Race'] == 'Viera':
		bpy.context.scene.bone_morph_ffxiv_model_list = "viera"
	else:
		bpy.context.scene.bone_morph_ffxiv_model_list = "none"

	
	obj = bpy.context.active_object
	root = mmd_model.Model.findRoot(obj)

	if obj and obj.type == 'ARMATURE' and root:
		if bpy.context.scene.bone_morph_ffxiv_model_list != "none" :
			bpy.ops.ffxiv_mmd.add_bone_morphs()
		else:
			print("Bone Morphs not applied since we couldn't determine the character's FFXIV Race")
	else:
		print("Bone Morphs not applied since this has not been converted into an MMD Model")
	



def reset_all_shape_keys():
	# Get the currently selected armature
	selected_armature = bpy.context.active_object

	if selected_armature and selected_armature.type == 'ARMATURE':
		# Create a list to store the meshes that are children of the armature
		child_meshes = []

		# Iterate through all objects in the scene
		for obj in bpy.context.scene.objects:
			if obj.type == 'MESH' and obj.parent and obj.parent.type == 'ARMATURE' and obj.parent.name == selected_armature.name:
				child_meshes.append(obj)


		for mesh in child_meshes:
			if hasattr(mesh.data.shape_keys, 'key_blocks'):
				for shape_key_block in mesh.data.shape_keys.key_blocks:
					if shape_key_block.value != 0:
						shape_key_block.value = 0
						print('shape_key:' + shape_key_block.name + ' Mesh: ' + mesh.name + ' Set to 0')

	
def enable_shape_keys(shape_key_name):
	#print (shape_key_name + " is going to be modified!")

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
				for shape_key_block in mesh.data.shape_keys.key_blocks:
					if shape_key_block.name == shape_key_name:
						# Set the shape key's value to 1
						shape_key_block.value = 1.0
						#print(f"{shape_key_block.name} is going to be modified!")




def main(context,filepath):
	#print (filepath)
	RESULTS_DICT=parse_chara_file(filepath)
	apply_face_shape_keys(RESULTS_DICT)
	apply_face_bone_morphs(RESULTS_DICT)


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

	@classmethod
	def poll(cls, context):
			if context.active_object:
				return context.active_object.type == 'ARMATURE'

	def execute(self, context):
		filepath = self.filepath
		# Add code here to process the selected file
		main(context,filepath)


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