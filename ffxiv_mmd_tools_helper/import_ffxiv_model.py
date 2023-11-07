import bpy
import os
from . import register_wrap
from . import miscellaneous_tools
from . import bones_renamer
from . import add_foot_leg_ik
from bpy.props import StringProperty



def get_test_model_file_path(ffxiv_model):

	file_path = (__file__ + "\\ffxiv models\\" + ffxiv_model + "\\" + ffxiv_model + ".fbx").replace("import_ffxiv_model.py" , "")

	return file_path

def import_ffxiv_model(context,file_path):

	if bpy.context.mode != 'OBJECT':
		bpy.ops.object.mode_set(mode='OBJECT')

	#file_path = (__file__ + "\\ffxiv models\\" + ffxiv_model + "\\" + ffxiv_model + ".fbx").replace("import_ffxiv_model.py" , "")
	#print(file_path)
	#deselect all objects

	#sets the active collection to collection[0]
	# Make sure you have at least one collection in your scene before running this code
	collections = bpy.context.scene.collection.children

	if collections:
		bpy.context.window.view_layer.active_layer_collection = bpy.context.window.view_layer.layer_collection.children[collections[0].name]
	else:
		print("No collections found in the scene.")

	bpy.ops.object.select_all(action='DESELECT')
	
	bpy.ops.import_scene.fbx( \
		filepath = file_path \
		, global_scale = 1
		, primary_bone_axis='X' \
		, secondary_bone_axis='Y' \
		, use_manual_orientation=True \
		, axis_forward='Y' \
		, axis_up='Z'
	)
	
	
	armature = None
	
	if bpy.context.selected_objects:
		for i in bpy.context.selected_objects:
			if i.type =='ARMATURE':
				armature = i

	if armature:
		print (f"{armature.name}:{armature.type}")


		#####move all 'Group' objects to an empty object called 'FFXIV Junk'####
		# Get the selected object
		selected_obj = bpy.context.selected_objects[0] #should be n_root
		#print(f"{selected_obj}:{selected_obj.type}")
		selected_obj_parent = selected_obj.parent #should be imported object name (Nala V3)
		#print(f"{selected_obj_parent}:{selected_obj_parent.type}")

		bpy.context.view_layer.objects.active = selected_obj_parent

		#rotate the model 90 degrees on the x axis
		miscellaneous_tools.fix_object_axis()

		
		# Create a new empty object to store all the junk that comes from FFXIV
		bpy.ops.object.add(type='EMPTY', location=(0, 0, 0))
		new_empty = bpy.context.object
		new_empty.name = 'FFXIV Empty Groups'
		#print (new_empty)

		# Parent the new empty object to the selected object
		new_empty.parent = selected_obj_parent

		# Iterate through all children of the selected object
		for child in selected_obj_parent.children:
			# Check if the child object contains the substring 'Group' in its name
			if 'Group' in child.name:
				if len(child.children) == 0:
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

		###### Fix the alpha blend mode so that all the textures can be viewed properly, and set backface culling to True ######
		mats = bpy.data.materials
		for mat in mats:
			mat.blend_method = 'HASHED'
			mat.use_backface_culling = True
		
		##### add the" mmd_bone_order_override" armature modifier to the FIRST mesh on n_root (as per the MMD Tools instructions)####
		# Get the first mesh object that is a child of the armature
		mesh = [child for child in armature.children if child.type == 'MESH'][0]

		mmd_bone_order_override_modifier = None

		for modifier in mesh.modifiers:
			if modifier.type == 'ARMATURE' and modifier.object.name in (armature.name,'mmd_bone_order_override'):
				mmd_bone_order_override_modifier = modifier
				mmd_bone_order_override_modifier.name = 'mmd_bone_order_override'
				break

		if mmd_bone_order_override_modifier == None:
			# Add the armature modifier to the mesh
			mmd_bone_order_override_modifier = mesh.modifiers.new(name="mmd_bone_order_override", type='ARMATURE')
			# Set the armature as the object to which the modifier applies
			mmd_bone_order_override_modifier.object = armature
		
		#set the last selected armature as the active object
		x = bpy.data.objects[armature.name]
		x.select_set(True)

		print(x.name + ' ' +x.type)

		#get name of the root object and add it as a custom property to the armature (needed becuase MMD moves the armature to a new root)
		if x.type=='ARMATURE':
			root = x.parent
			add_custom_property(x,'original_root_name',root.name)
	

		mesh_list = {}
		
		#loop through all the meshes and rename them to something human-readable
		if x.type =='ARMATURE':
			for obj in x.parent.children_recursive:
				if obj.type == 'MESH':
					add_custom_property(obj,'original_mesh_name',obj.name) 
					#print("renaming!" + obj.name)
					rename_ffxiv_mesh(obj)

					original_material_name = obj.data['original_material_name']
					model_type = obj.data['ModelType']
					material_type = obj.data['MaterialType']
					material_folder=''
					immediate_folder_name=''
					#if mesh doesn't exist on the mesh_list add to the mesh_list
					if original_material_name not in mesh_list:
						mesh_list[original_material_name] = (model_type,material_type,immediate_folder_name,material_folder,)

					#add the ModelRaceType to the root armature properties
					if obj.data['ModelType'] == 'Face':
						# Copy the custom property 'ModelRaceType' to the armature data
						add_custom_property(x,'ModelRaceType',obj.data['ModelRaceType'])


					

		textools_folder = None

		addon_prefs = bpy.context.preferences.addons[__package__].preferences
		textools_saved_folder = addon_prefs.textools_saved_folder

		# Check if textools_saved_folder is not None
		if context.scene.textools_model_folder:
			if os.path.exists(os.path.abspath(context.scene.textools_model_folder)):
				textools_folder = os.path.abspath(context.scene.textools_model_folder)

		elif textools_saved_folder:
			if os.path.exists(os.path.abspath(textools_saved_folder)):
				textools_folder = os.path.abspath(textools_saved_folder)
			
		print(f"textools folder: {textools_folder}")
		
		#loop through the mesh_list and search for the target files
		for i in mesh_list:
			material_folder = find_TexTools_material_texture_folder(textools_folder,mesh_list[i][0],mesh_list[i][1],i)
			#print(f"{i}: {mesh_list[i][0]}, {mesh_list[i][1]}:{material_folder}")
			
			#if material folder is found, update mesh_list with the details
			if material_folder:
				immediate_folder_name = material_folder.split(os.path.sep)[-1]
				mesh_list[i] = (mesh_list[i][0],mesh_list[i][1],immediate_folder_name,material_folder)
			else:
				mesh_list[i] = (mesh_list[i][0],mesh_list[i][1],'','')
			
			#print(f"{i}: {mesh_list[i][0]}, {mesh_list[i][1]},{mesh_list[i][2]}")
		
		#loop through the armature and if there's any meshes that match the mesh_list, update custom properties and name
		if x.type =='ARMATURE':
			for obj in x.parent.children_recursive:
				if obj.type == 'MESH':
					
					if obj.data['original_material_name'] in mesh_list:
						matname= obj.data['original_material_name']
						if mesh_list[matname][3] != '':
							print(f"{obj.name}: {mesh_list[matname][0]},{mesh_list[matname][1]},{mesh_list[matname][2]},{mesh_list[matname][3]}")
		
							
							add_custom_property(obj,'ModelName',mesh_list[matname][2])
							add_custom_property(obj,'material_filepath', mesh_list[matname][3])
		

					
def add_custom_property(obj,prop_name,prop_value):
	
	obj.data[prop_name] = prop_value



def find_TexTools_material_texture_folder(root_folder_path,ModelType,MaterialType,original_material_name):

	#root_folder_path = r'C:\Users\wikid\OneDrive\Documents\TexTools\Saved'
	#ModelType = 'Body'
	#original_material_name = 'mt_c0501e9152_top_a'
	#target_filename = 'mt_c0501e9152_top_a.dat'
	target_filename = original_material_name+'.dat'
	target_folder_path = None
	ModelType_subfolder = None

	textools_subfolder_gear_dict = {    
			"Wrists":"Wrists",
			"Earrings":"Earring",
			"Neck":"Neck",
			"RingL":"Rings",
			"RingR":"Rings",
			"Legs":"Legs",
			"Head":"Head",
			"Feet":"Feet",
			"Hands":"Hands",
			"Body":"Body",
		}
	
	prop_textools_subfolder_char_dict ={
			"Body":"Character\Body",
			"Face":"Character\Face",
			"Hair":"Character\Hair",
			"Tail":"Character\Tail",
			"Ears":"Character\Ear",
			"EquipmentDecal":"Character\Equipment Decals",
			"FacePaint":"Character\Face Paint",
		}
	
	#if MaterialType in ['b','f','h','t','z']
		#then point to the Chracter folder
	
	#if MaterialType in ['e','a']
		#then point to the equipment folder
	
	
	if root_folder_path and os.path.exists(root_folder_path):
		if ModelType in textools_subfolder_gear_dict and MaterialType in ['e','a']:
			ModelType_subfolder = textools_subfolder_gear_dict[ModelType]

		elif ModelType in prop_textools_subfolder_char_dict and MaterialType in ['b','f','h','t','z']:
			ModelType_subfolder = prop_textools_subfolder_char_dict[ModelType]

		else:
			ModelType_subfolder = ""  # Set it to an empty string if not found

		def find_target_file(folder_path, target_filename):
			for root, dirs, files in os.walk(folder_path):
				if target_filename in files:
					return os.path.abspath(root)
			return None


		# Ensure ModelType_subfolder is a string before using it in os.path.join
		if not isinstance(ModelType_subfolder, str):
			ModelType_subfolder = str(ModelType_subfolder)

		#print(f"({root_folder_path}, {ModelType_subfolder})")
		subfolder_path = os.path.join(root_folder_path, ModelType_subfolder)

		#print(subfolder_path)
		if os.path.exists(subfolder_path):
			target_folder_path = find_target_file(subfolder_path, target_filename)
		

		#if target_folder_path:
		#	print("Target Folder:", target_folder_path)
		#else:
		#	print(f"Filename {target_filename} not found in folder {subfolder_path}.")

	return target_folder_path







def rename_ffxiv_mesh(obj):
	# Input string
	input_string = obj.name
	#input_string = "c0801h0105_hir Part 1.80"
	if obj.type =='MESH' and (input_string.startswith("c1") or input_string.startswith("c0")):
		# Define the lengths for each part
		part_lengths = [5, 1, 4, 1, 3, 1, 4,1,4]

		# Initialize variables to store the parsed parts
		parsed_parts = []

		# Loop through the parts and extract them
		start_index = 0
		for length in part_lengths:
			part = input_string[start_index:start_index + length]
			parsed_parts.append(part)
			start_index += length

		# Print the parsed parts
		#for i, part in enumerate(parsed_parts):
			#print(f"Part {i + 1}: {part}")
		
		#add mesh details as a custom property
		Model_ID = parsed_parts[0]+parsed_parts[1]+parsed_parts[2]+parsed_parts[3]+parsed_parts[4]
		add_custom_property(obj,'ModelID',Model_ID)
		add_custom_property(obj,'ModelRaceID',int(parsed_parts[0].lstrip('c')))
		add_custom_property(obj,'ModelNumberID',int(parsed_parts[2]))
		add_custom_property(obj,'ModelTypeID',parsed_parts[4])
		add_custom_property(obj,'MeshPartNumber',parsed_parts[8])
		add_custom_property(obj,'original_material_name',obj.active_material.name.split('.')[0])
		add_custom_property(obj,'MaterialType',obj.data['original_material_name'][8])
		add_custom_property(obj,'ModelName','')
		add_custom_property(obj,'material_filepath','')
			

		# Define the replacement dictionary
		race_dict = {
			"c0101": "Hyur_Mid_M",
			"c0104": "Hyur_Mid_M_NPC",
			"c0201": "Hyur_Mid_F",
			"c0301": "Hyur_Hig_M",
			"c0401": "Hyur_Hig_F",
			"c0501": "Elez_M",
			"c0601": "Elez_F",
			"c0701": "Miqo_M",
			"c0801": "Miqo_F",
			"c0804": "Miqo_F_NPC",
			"c0901": "Roeg_M",
			"c1001": "Roeg_F",
			"c1101": "Lala_M",
			"c1201": "Lala_F",
			"c1301": "Aura_M",
			"c1401": "Aura_F",
			"c1501": "Hrot_M",
			"c1601": "Hrot_F",
			"c1701": "Vier_M",
			"c1801": "Vier_F",
		}

		

		# Replace part 1 using the dictionary
		if parsed_parts[0] in race_dict:
			parsed_parts[0] = race_dict[parsed_parts[0]]

		add_custom_property(obj,'ModelRaceType',parsed_parts[0])
			
		part_dict = {    
			"wrs":"Wrists",
			"ear":"Earrings",
			"nek":"Neck",
			"rir":"RingL",
			"ril":"RingR",
			"dwn":"Legs",
			"met":"Head",
			"sho":"Feet",
			"glv":"Hands",
			"top":"Body",
			"fac":"Face",
			"hir":"Hair",
			"til":"Tail",
			"zer":"Ears",
		}

		# Replace part 5 using the dictionary
		if parsed_parts[4] in part_dict:
			parsed_parts[4] = part_dict[parsed_parts[4]]

		add_custom_property(obj,'ModelType',parsed_parts[4])

		# Print the parsed parts
		#for i, part in enumerate(parsed_parts):
			#print(f"Part {i + 1}: {part}")
		
		new_mesh_name = parsed_parts[4]+"-"+parsed_parts[1]+parsed_parts[2]+"-"+parsed_parts[8]+"-"+parsed_parts[0]

		obj.name = new_mesh_name


def main(context):



	if bpy.context.scene.selected_ffxiv_test_model == "import_nala":
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		filepath='C:\\Users\\wikid\\OneDrive\\Documents\\TexTools\\Saved\\FullModel\\Nala V3\\Nala V3.fbx'
		import_ffxiv_model(context,filepath)

	elif bpy.context.scene.selected_ffxiv_test_model == "import_nala_deluxe":
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		filepath='C:\\Users\\wikid\\OneDrive\\Documents\\TexTools\\Saved\\FullModel\\Nala V3\\Nala V3.fbx'
		import_ffxiv_model(context,filepath)
		miscellaneous_tools.fix_object_axis()
		bones_renamer.main(context)
		miscellaneous_tools.correct_root_center()
		miscellaneous_tools.correct_groove()
		miscellaneous_tools.correct_waist()
		miscellaneous_tools.correct_waist_cancel()
		add_foot_leg_ik.main(context)
	else:
		import_ffxiv_model(context,get_test_model_file_path(bpy.context.scene.selected_ffxiv_test_model))


from bpy_extras.io_utils import ImportHelper
@register_wrap
class FFXIV_FileBrowserImportOperator(bpy.types.Operator, ImportHelper):
	"""Operator that opens the file browser dialog"""
	bl_idname = "ffxiv_mmd.ffxiv_file_browser_operator"
	bl_label = "Import FFXIV .fbx File"
	bl_options = {'REGISTER', 'UNDO'}

	filename_ext = ".fbx"
	filter_glob: bpy.props.StringProperty(
		default="*.fbx",
		options={'HIDDEN'},
	)

	def execute(self, context):
		file = self.filepath
		# Add code here to process the selected file
		print (file)
		import_ffxiv_model(context,file)

		return {'FINISHED'}



@register_wrap
class ImportFFXIVModel(bpy.types.Operator):
	"""Import FFXIV Test Model"""
	bl_idname = "ffxiv_mmd.import_ffxiv_model"
	bl_label = "Import FFXIV Test Model"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.selected_ffxiv_test_model = bpy.props.EnumProperty(items = \
	[('none', 'none', 'none')\
	#, ("import_nala", "import_nala","import_nala") \
	#, ("import_nala_deluxe", "import_nala_deluxe","import_nala_deluxe") \
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
	
	
	@classmethod
	def poll(cls, context):

		if context.scene.selected_ffxiv_test_model != 'none':	
			return True#context.active_object is not None
	
	def execute(self, context):
		main(context)
		return {'FINISHED'}
	


@register_wrap
class SelectTexToolsModelFolder(bpy.types.Operator):
	"""User can select the folder for materials"""
	bl_idname = "ffxiv_mmd.select_textools_model_folder"
	bl_label = "Select TexTools Model Folder"
	bl_options = {'REGISTER', 'UNDO'}

	


	bpy.types.Scene.textools_model_folder = bpy.props.StringProperty(
		name="TexTools Model Folder"
		, description="Folder for where TexTools stores FFXIV gear files"
		, default=''
		, maxlen=0, options={'ANIMATABLE'}, subtype='DIR_PATH', update=None, get=None, set=None)
	
	#@classmethod
	#def poll(cls, context):
	#	return context.active_object is not None and context.active_object.type == 'MESH'

	def execute(self, context):
		#self.textools_model_folder = context.preferences.addons['ffxiv_mmd_tools_helper'].preferences.textools_saved_folder.title()

		context.scene.textools_model_folder = bpy.path.abspath(context.scene.textools_model_folder)
		folder_path = context.scene.textools_model_folder
		print(folder_path)
		return {'FINISHED'}
	