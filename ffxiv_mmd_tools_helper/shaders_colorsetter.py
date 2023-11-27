import bpy
import os
from . import register_wrap
from . import model
from struct import unpack, pack
from os.path import isfile

def read_i(file, i):
	return [unpack('e', file.read(2))[0] for x in range(i)]


def apply_colorset_file(file_name):
	for obj in bpy.context.selected_objects:
		if obj.type =='MESH' and obj.active_material.is_colorset:
			colorsetdat = False
			if isfile(file_name[:-3]+'dat'):
				colorsetdat = open(file_name[:-3]+'dat', 'rb')
			with open(file_name, 'rb') as colorset:
				colorset.seek(128)
				for i in range(16):
					bpy.context.object.active_material.cs_rows[i].diff = read_i(colorset, 4)
					# these properties have to be 4 long to update properly, 4th is dummy,
					# won't append directly to the read_i call for some reason...
					spec = read_i(colorset, 3)
					spec.append(1.0)
					bpy.context.object.active_material.cs_rows[i].spec = spec
					bpy.context.object.active_material.cs_rows[i].gloss = read_i(colorset, 1)[0]
					glow = read_i(colorset, 3)
					glow.append(1.0)
					bpy.context.object.active_material.cs_rows[i].glow = glow
					bpy.context.object.active_material.cs_rows[i].tile_id = int(read_i(colorset, 1)[0] * 64)
					bpy.context.object.active_material.cs_rows[i].tile_transform = [x for x in read_i(colorset, 4)]
					if colorsetdat:
						#unpacked_hex_value = hex(unpack('>H', colorsetdat.read(2))[0])[2:]
						#if len(unpacked_hex_value) < 4:
							
						bpy.context.object.active_material.cs_rows[i].dye = hex(unpack('>H', colorsetdat.read(2))[0])[2:]

				colorset.close()
			if colorsetdat:
				colorsetdat.close()





def apply_colorset_plugin():
	if bpy.context.active_object:
			obj = bpy.context.active_object

			if obj.type =='MESH':
				if not obj.active_material.is_colorset:
					#get model_id and material name
					model_id = obj.data['ModelID']
	
					# Duplicate the material
					old_material = obj.active_material.copy()
					old_material.name = "backup_" + obj.active_material.name  # Rename the duplicated material if needed
					# Add the duplicated material to the material slots of the active object
					#bpy.context.object.data.materials.append(old_material)


					bpy.ops.object.add_cs_material()
					if obj.active_material.is_colorset:
						new_material = obj.active_material
						new_material.name = "colorsetter_gear_" + old_material.name.lstrip("backup_" )

						for node in new_material.node_tree.nodes:
							if node.type == 'GROUP' and node.node_tree.name.startswith('FFXIV_Colorset Shader'):
								node.name = 'colorsetter_gear_node_instance'
								break

					old_material.use_fake_user = True #stores material in blend file even if not used after save


					return old_material
				

def apply_textures_to_colorset_material(context,folder_path):
	if bpy.context.active_object:
			obj = bpy.context.active_object

			if obj.type =='MESH' and obj.active_material.is_colorset :

				colorsetter_gear_node = None

				for node in obj.active_material.node_tree.nodes:
					if node.type == 'GROUP' and node.node_tree.name.startswith('FFXIV_Colorset Shader'):
						colorsetter_gear_node = node
						break

				if colorsetter_gear_node:
					multi_node = colorsetter_gear_node.inputs['Multi Texture'].links[0].from_node
					normal_node = colorsetter_gear_node.inputs['Normal Map'].links[0].from_node
					normal_nearest_node = colorsetter_gear_node.inputs['Colorset Position Ramp'].links[0].from_node.inputs[0].links[0].from_node.inputs[0].links[0].from_node.inputs[0].links[0].from_node.inputs['Fac'].links[0].from_node
					diffuse_node = colorsetter_gear_node.inputs['Diffuse Texture'].links[0].from_node
					specular_node = colorsetter_gear_node.inputs['Specular Texture'].links[0].from_node
					specular_mask_node = colorsetter_gear_node.inputs['Specular Mask Texture'].links[0].from_node



					#model_id = obj.data['ModelID']
					#new_material = obj.active_material

					colorset_files = [f for f in os.listdir(context.scene.shaders_texture_folder) if f.endswith('_a.dds') ]
					multimap_files = [f for f in os.listdir(context.scene.shaders_texture_folder) if f.endswith('_m.bmp') or f.endswith('_d.png') or f.endswith('_d.bmp') or f.endswith('_s.png')]
					normalmap_files = [f for f in os.listdir(context.scene.shaders_texture_folder) if f.endswith('_n.bmp') or f.endswith('_n.png')]
					specular_files = [f for f in os.listdir(context.scene.shaders_texture_folder) if f.endswith('_s.bmp') or f.endswith('_s.png')]
					diffuse_files = [f for f in os.listdir(context.scene.shaders_texture_folder) if f.endswith('_d.bmp') or f.endswith('_d.png')]


					if colorset_files:
						filename = folder_path+colorset_files[0]
						#print(f"Colorset file found: {colorset_filename}")
						try:
							apply_colorset_file(filename)
						except:
							#display_error_message=  "ERROR: could not apply ",colorset_filename
							print("ERROR: could not apply ",filename)
							#bpy.context.window_manager.popup_menu(display_error_message, title="Error Message", icon='ERROR')
							return obj.active_material

					else:
						print("No colorset file ending with '_a' found in the folder.")
											
							
					if multimap_files:
						filename = folder_path+multimap_files[0]
						update_image_node_file(multi_node,filename)
						multi_node.image.colorspace_settings.name = 'sRGB'
					else:
						print("No multimap file ending with '_m' or '_s' found in the folder.")
						
							
					if normalmap_files:
						filename = folder_path+normalmap_files[0]
						update_image_node_file(normal_node,filename)
						update_image_node_file(normal_nearest_node,filename)
						normal_node.image.colorspace_settings.name = 'Non-Color'
						normal_nearest_node.image.colorspace_settings.name = 'Non-Color'
					else:
						print("No normalmap file ending with '_n' found in the folder.")

					if specular_files:
						specular_filename = folder_path+specular_files[0]
						update_image_node_file(specular_node,specular_filename)
					else:
						print("No specular file ending with '_s' found in the folder.")


					if diffuse_files:
						diffuse_filename = folder_path+diffuse_files[0]
						update_image_node_file(diffuse_node,diffuse_filename)
						diffuse_node.image.colorspace_settings.name = 'sRGB'
					else:
						print("No diffuse file ending with '_d' found in the folder.")						
															
					return obj.active_material


def undo_if_colorset_plugin_error(obj,old_material,new_material):

	if new_material.is_colorset:


		colorsetter_gear_node = None

		for node in obj.active_material.node_tree.nodes:
			if node.type == 'GROUP' and node.node_tree.name.startswith('FFXIV_Colorset Shader'):
				colorsetter_gear_node = node
				break

		if colorsetter_gear_node:
			multi_node = colorsetter_gear_node.inputs['Multi Texture'].links[0].from_node
			normal_node = colorsetter_gear_node.inputs['Normal Map'].links[0].from_node
			normal_nearest_node = colorsetter_gear_node.inputs['Colorset Position Ramp'].links[0].from_node.inputs[0].links[0].from_node.inputs[0].links[0].from_node.inputs[0].links[0].from_node.inputs['Fac'].links[0].from_node
			diffuse_node = colorsetter_gear_node.inputs['Diffuse Texture'].links[0].from_node
			specular_node = colorsetter_gear_node.inputs['Specular Texture'].links[0].from_node
			colorsetter_gear_specular_mask_node = colorsetter_gear_node.inputs['Specular Mask Texture'].links[0].from_node

		if (diffuse_node.image or specular_node.image or multi_node.image or normal_node.image or normal_nearest_node.image or specular_node.image):
			return True
		else:
			#if error detected, delete the material node and reset the material to it's original material
			if old_material == new_material:
				print("")
			else:
				print ("old_material:",old_material)
				print ("new_material:",new_material)
				
				obj.active_material = old_material

				# Remove the material
				bpy.data.materials.remove(new_material)
				old_material.name = old_material.name.lstrip('backup_')
			return False


def apply_material_to_all_matching_ffxiv_meshes (source_object):
	
	#model_id = None
	armature = model.findArmature(source_object)

	if source_object.data["original_material_name"]:
		model_id = source_object.data["original_material_name"]

	print(source_object)
	print (source_object.data["original_material_name"])
	print (model_id)

	if source_object.data["original_material_name"]:
		for obj in armature.children_recursive:
			if obj.type == 'MESH' and obj.data["original_material_name"]:
				if obj.data["original_material_name"] == source_object.data["original_material_name"]:
					obj.active_material = source_object.active_material
	

import fnmatch
import re
def find_replacement_texture(image_node, replacement_folderpath,re_search_string=None):

	filename_no_extension = None
		
	if image_node.image and image_node.image.filepath:
		filename = os.path.basename(image_node.image.filepath)
		filename_no_extension, extension = os.path.splitext(filename)

	# List of valid extensions to check for
	valid_extensions = ['.dds', '.png', '.bmp']

	# Get the list of files in the replacement folder and its subfolders
	replacement_files = set()
	for root, dirs, files in os.walk(replacement_folderpath):

		if re_search_string is not None:
			pattern = re.compile(f".*{re_search_string}.*", re.IGNORECASE)
			for file in files:
				if pattern.match(file) and any(file.lower().endswith(ext) for ext in valid_extensions):
					replacement_files.add(os.path.join(root, file))
		else:
			for file in fnmatch.filter(files, f"{filename_no_extension}*"):
				if any(file.lower().endswith(ext) for ext in valid_extensions):
					replacement_files.add(os.path.join(root, file))	

	# Check if any replacement file with a valid extension exists
	if replacement_files:
		# Choose the first match
		new_filepath = sorted(replacement_files)[0]
		if image_node.image and image_node.image.filepath:
			if new_filepath != image_node.image.filepath:

				update_image_node_file(image_node,new_filepath)
		else:
			update_image_node_file(image_node,new_filepath)
				
				
		print(f"Node:{image_node.name} updated with replacement image: {os.path.basename(new_filepath)}")
		
	else:
		print(f"No matching replacement image found for node:{image_node.name}")



	
@register_wrap
class ReplaceColorsetterTextures(bpy.types.Operator):
	"""Replace textures using .dds/.png/.bmp files with the exact same filename from the selected folder"""
	bl_idname = "ffxiv_mmd.replace_colorsetter_textures"
	bl_label = "Replace Materials Textures"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.shaders_replacement_texture_folder = bpy.props.StringProperty(name="Texture Folder", description="Folder where the gear for _a, _m, and _n files are located", default="", maxlen=0, options={'ANIMATABLE'}, subtype='DIR_PATH', update=None, get=None, set=None)
	
	shader_type_list = ['eye','face','hair','faceacc','tail','skin','gear']
	shader_type = bpy.props.StringProperty(name="shader_type", update=None, get=None, set=None)

	def execute(self, context):
		active_object = context.active_object
		active_material = active_object.active_material

		for node in active_material.node_tree.nodes:
			if node.type == 'TEX_IMAGE': 
				find_replacement_texture(node,context.scene.shaders_replacement_texture_folder)
		
		return {'FINISHED'}
	

def search_texture(mesh_obj,image_node, replacement_folderpath,shader_type):
	original_material_name = mesh_obj.data.get('original_material_name')
	material_prefix = original_material_name.lstrip('mt_')
	# Strip everything up to and including the last underscore
	parts = material_prefix.rsplit('_', 1)
	stripped_prefix = parts[0] if len(parts) > 1 else material_prefix
	#print (f'material_prefix:{material_prefix},stripped_prefix:{stripped_prefix}')

	if image_node.image and image_node.image.filepath:
		return
	else:
		re_search_string = None

		if shader_type == 'skin':
			if image_node.label == 'Diffuse Skin Texture': 
				re_search_string = stripped_prefix+'_d'
			if image_node.label == 'Multi Skin Texture': 
				re_search_string = stripped_prefix+'_s'
			if image_node.label == 'Normal Skin Texture': 
				re_search_string = stripped_prefix+'_n'

		if shader_type == 'eye':
			if image_node.label == 'Multi Texture': 
				re_search_string = 'iri_s'
			if image_node.label == 'Normal Texture': 
				re_search_string = 'iri_n'
			
		if shader_type == 'face':
			if image_node.label == 'Diffuse Face Texture':
				re_search_string = stripped_prefix+'_d'
			if image_node.label == 'Multi Face Texture':
				re_search_string = stripped_prefix+'_s'
			if image_node.label == 'Normal Face Texture':
				re_search_string = stripped_prefix+'_n'

		if shader_type == 'faceacc':
			if image_node.label == 'Multi Texture':
				re_search_string = stripped_prefix+'_s'
			if image_node.label == 'Normal Texture':
				re_search_string = stripped_prefix+'_n'

		if shader_type == 'hair':
			if image_node.label == 'Hair Multi Texture':
				re_search_string = stripped_prefix+'_s'
			if image_node.label == 'Hair Normal Map':
				re_search_string = stripped_prefix+'_n'

		if shader_type == 'tail':
			if image_node.label == 'Multi Texture':
				re_search_string = stripped_prefix+'_etc_s'
			if image_node.label == 'Normal Texture':
				re_search_string = stripped_prefix+'_etc_n'

		if re_search_string:
			#print(suffix)
			find_replacement_texture(image_node,replacement_folderpath,re_search_string=re_search_string)


	
@register_wrap
class SearchColorsetterTextures(bpy.types.Operator):
	"""Search for missing textures with .bmp/.dds/.png files from the selected folder"""
	bl_idname = "ffxiv_mmd.search_colorsetter_textures"
	bl_label = "Search For Textures Folder"
	bl_options = {'REGISTER', 'UNDO'}

	shader_type_list = ['eye','face','hair','faceacc','tail','skin','gear']

	shader_type = bpy.props.StringProperty(name="shader_type", update=None, get=None, set=None)

	def execute(self, context):
		active_object = context.active_object
		active_material = active_object.active_material
		node_tree = active_material.node_tree

		if self.shader_type == 'skin':
			node_tree = active_material.node_tree.nodes.get('colorsetter_skin_node_instance').node_tree
			

		for node in node_tree.nodes:
			if node.type == 'TEX_IMAGE': 
				search_texture(active_object,node,context.scene.shaders_replacement_texture_folder,self.shader_type)
		
		return {'FINISHED'}




@register_wrap
class SelectColorsetterGearMaterialsFolder(bpy.types.Operator):
	"""Apply the Colorsetter addon to the selected mesh using DDS/PNG/BMP textures from the selected folder"""
	bl_idname = "ffxiv_mmd.select_colorsetter_gear_materials_folder"
	bl_label = "Select Materials Folder"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.shaders_texture_folder = bpy.props.StringProperty(name="Texture Folder", description="Folder where the gear for _a, _m, and _n files are located", default="", maxlen=0, options={'ANIMATABLE'}, subtype='DIR_PATH', update=None, get=None, set=None)

	@classmethod
	def poll(cls, context):

		if 	context.active_object is not None \
			and context.active_object.type == 'MESH' \
			and os.path.exists(context.scene.shaders_texture_folder):
			return True


	def execute(self, context):

		addon_name = 'Colorsetter'

		# Check if the addon is enabled
		if addon_name not in context.preferences.addons.keys():
			raise Exception(f"The addon '{addon_name}' is not installed or is not enabled. Please install and enable it.")
		else:
			#print(f"The addon '{addon_name}' is installed and enabled.")

			context.scene.shaders_texture_folder = bpy.path.abspath(context.scene.shaders_texture_folder)
			folder_path = context.scene.shaders_texture_folder
			print (folder_path)
			
			old_material = None
			new_material = None
			
			if context.active_object:

				obj = context.active_object

				if obj.type == 'MESH':
					old_material = apply_colorset_plugin()
					new_material = apply_textures_to_colorset_material(context,folder_path).id_data

					if undo_if_colorset_plugin_error(context.active_object,old_material, new_material):
						#if no errors, apply to all materials 
						apply_material_to_all_matching_ffxiv_meshes (obj)
					else:
						print ("ERROR: COULD NOT APPLY THE COLORSETTER PLUGIN (probably a 'Import DDS' error in Colorsetter addon)")					
				
			return {'FINISHED'}
		



def get_ffxiv_skin_file(active_object,texture_type):

	skin_dictionary = [
	['Hyur','Midlander','Masculine','hyur_midl_m','c0101b0001_d','c0101b0001_n','skin_m']
	,['Hyur','Midlander','Feminine','hyur_midl_f','c0201b0001_d','c0201b0001_n','skin_m']
	,['Hyur','Highlander','Masculine','hyur_high_m','c0301b0001_d','c0301b0001_n','skin_m']
	,['Hyur','Highlander','Feminine','hyur_high_f','c0401b0001_d','c0401b0001_n','skin_m']
	,['Elezen','Duskwight','Masculine','elez_dusk_m','c0101b0001_d','c0101b0001_n','skin_m']
	,['Elezen','Wildwood','Masculine','elez_wild_m','c0101b0001_d','c0101b0001_n','skin_m']
	,['Elezen','Duskwight','Feminine','elez_dusk_f','c0201b0001_d','c0201b0001_n','skin_m']
	,['Elezen','Wildwood','Feminine','elez_wild_f','c0201b0001_d','c0201b0001_n','skin_m']
	,['Miqote','KeeperOfTheMoon','Masculine','miqo_keep_m','c0101b0001_d','c0101b0001_n','skin_m']
	,['Miqote','SeekerOfTheSun','Masculine','miqo_seek_m','c0101b0001_d','c0101b0001_n','skin_m']
	,['Miqote','KeeperOfTheMoon','Feminine','miqo_keep_f','c0201b0001_d','c0201b0001_n','skin_m']
	,['Miqote','SeekerOfTheSun','Feminine','miqo_seek_f','c0201b0001_d','c0201b0001_n','skin_m']
	,['Roegadyn','Hellsguard','Masculine','roeg_hell_m','c0901b0001_d','c0901b0001_n','skin_m']
	,['Roegadyn','SeaWolf','Masculine','roeg_seaw_m','c0901b0001_d','c0901b0001_n','skin_m']
	,['Roegadyn','Hellsguard','Feminine','roeg_hell_f','c0401b0001_d','c0401b0001_n','skin_m']
	,['Roegadyn','SeaWolf','Feminine','roeg_seaw_f','c0401b0001_d','c0401b0001_n','skin_m']
	,['Lalafel','Dunesfolk','Masculine','lala_dune_m','c1101b0001_d','c1101b0001_n','skin_m']
	,['Lalafel','Plainsfolk','Masculine','lala_plai_m','c1101b0001_d','c1101b0001_n','skin_m']
	,['Lalafel','Dunesfolk','Feminine','lala_dune_f','c1101b0001_d','c1101b0001_n','skin_m']
	,['Lalafel','Plainsfolk','Feminine','lala_plai_f','c1101b0001_d','c1101b0001_n','skin_m']
	,['AuRa','Raen','Masculine','aura_raen_m','c1301b0001_d','c1301b0001_n','c1301b0001_s']
	,['AuRa','Xaela','Masculine','aura_xael_m','c1301b0101_d','c1301b0001_n','c1301b0001_s']
	,['AuRa','Raen','Feminine','aura_raen_f','c1401b0001_d','c1401b0001_n','c1401b0001_s']
	,['AuRa','Xaela','Feminine','aura_xael_f','c1401b0101_d','c1401b0001_n','c1401b0001_s']
	,['Hrothgar','Helions','Masculine','hrot_heli_m','c1501b0001_d','c1501b0001_n','v01_c1501b0001_s']
	,['Hrothgar','TheLost','Masculine','hrot_lost_m','c1501b0001_d','c1501b0001_n','v01_c1501b0001_s']
	,['Hrothgar','Helions','Feminine','hrot_heli_f','c1601b0001_d','c1601b0001_n','v01_c1501b0001_s']
	,['Hrothgar','TheLost','Feminine','hrot_lost_f','c1601b0001_d','c1601b0001_n','v01_c1501b0001_s']
	,['Viera','Rava','Masculine','vier_rava_m','c1701b0001_d','c1701b0001_n','skin_m']
	,['Viera','Veena','Masculine','vier_veen_m','c1701b0001_d','c1701b0001_n','skin_m']
	,['Viera','Rava','Feminine','vier_rava_f','c1801b0001_d','c1801b0001_n','skin_m']
	,['Viera','Veena','Feminine','vier_veen_f','c1801b0001_d','c1801b0001_n','skin_m']
	]

	folder_path = (__file__ + r"assets\ffxiv_skin").replace("shaders_colorsetter.py" , "")
	print (folder_path)

	if active_object:
		if active_object.type == 'MESH':
			armature = model.findArmature(active_object) 

			if armature:
				race = armature.data.get('Race')
				tribe = armature.data.get('Tribe')
				gender = armature.data.get('Gender')

				texture_file = None

				#if there is no tribe (but there is a race and gender), default to the first tribe that matches
				if tribe == None and race and gender:
					for skin_type in skin_dictionary:
						if race == skin_type[0] and gender == skin_type[2]:
							tribe = skin_type[1]
							break

				

				if race and tribe and gender:
					for skin_type in skin_dictionary:
						if race == skin_type[0] and tribe == skin_type[1] and gender == skin_type[2]:
							if texture_type == 'diffuse':
								texture_file = skin_type[4]
							if texture_type == 'normal':
								texture_file = skin_type[5]
							if texture_type == 'multi':
								texture_file = skin_type[6]



					# Get a list of files in the folder
					files = os.listdir(folder_path)

					# Find the first file with the specified prefix
					matching_files = [file for file in files if file.startswith(texture_file)]

					if matching_files:
						first_matching_file = matching_files[0]
						full_path = os.path.join(folder_path, first_matching_file)
						#print("Found matching file:", full_path)
						return full_path
					

def find_existing_shader_type_in_armature(active_armature, shader_type):
	node_group_instance = None
	
	for obj in active_armature.children_recursive:
		#find all materials with nodes that have a skin node group instance
		if obj.type == 'MESH' and obj.active_material:
			for node in obj.active_material.node_tree.nodes:
				if node.type == 'GROUP' and node.name.startswith(f'colorsetter_{shader_type}_node_instance'):
					node_group_instance = node
					return node_group_instance
				
				
		




def set_colorsetter_skin_textures(active_object):

	colorsetter_material = active_object.active_material
	diffuse_node = None
	multi_node = None
	normal_node = None

	# Find the Colorsetter Skin Group node
	for node in colorsetter_material.node_tree.nodes:
		if node.type == 'GROUP' and node.name.startswith('colorsetter_skin_node_instance'):
			colorsetter_node = node

	if colorsetter_node:
		diffuse_node = colorsetter_node.node_tree.nodes['Diffuse Skin Texture'] #inputs['Diffuse Texture'].links[0].from_node
		multi_node = colorsetter_node.node_tree.nodes['Multi Skin Texture'] #inputs['Multi Texture'].links[0].from_node
		normal_node = colorsetter_node.node_tree.nodes['Normal Skin Texture'] #inputs['Normal Texture'].links[0].from_node

	diffuse_file_path = get_ffxiv_skin_file(active_object,"diffuse")
	multi_file_path = get_ffxiv_skin_file(active_object,"multi")
	normal_file_path = get_ffxiv_skin_file(active_object,"normal")
	

	update_image_node_file(diffuse_node,diffuse_file_path)
	update_image_node_file(multi_node,multi_file_path)
	update_image_node_file(normal_node,normal_file_path)

	return
	

def get_ffxiv_eye_multimap_file(active_object):

	folder_path = (__file__ + r"assets\ffxiv_iris").replace("shaders_colorsetter.py" , "")
	print (folder_path)

	if active_object:
		if active_object.type == 'MESH':
			model_race_id = active_object.data['ModelRaceID']
			original_material_name = active_object.data['original_material_name']
			model_number_id = str(active_object.data['ModelNumberID']).zfill(4)
			print(f"model_number_id: {model_number_id}")
			iris_multimap_prefix = 'c'+str(model_race_id).zfill(4)+'f'+model_number_id[0]+model_number_id[1]
			#print(iris_multimap_prefix)
			#print (f"iris_multimap_prefix: {iris_multimap_prefix}")

			# Get a list of files in the folder
			files = os.listdir(folder_path)

			# Find the first file with the specified prefix
			matching_files = [file for file in files if file.startswith(iris_multimap_prefix)]

			if matching_files:
				first_matching_file = matching_files[0]
				full_path = os.path.join(folder_path, first_matching_file)
				#print("Found matching file:", full_path)
				return full_path
			else:
				#strip the last character of the string and try again 
				iris_multimap_prefix = iris_multimap_prefix[:-1]
				matching_files = [file for file in files if file.startswith(iris_multimap_prefix)]

				if matching_files:
					first_matching_file = matching_files[0]
					full_path = os.path.join(folder_path, first_matching_file)
					#print("Found matching file:", full_path)
					return full_path
				
				else:
					#print("No matching file found.")
					return None


def get_ffxiv_eye_normalmap_file(active_object):

	folder_path = (__file__ + r"assets\ffxiv_iris").replace("shaders_colorsetter.py" , "")
	print (folder_path)

	if active_object:
		if active_object.type == 'MESH':
			iris_normalmap_prefix = '_iri_n'
			
			# Get a list of files in the folder
			files = os.listdir(folder_path)

			# Find the first file with the specified prefix
			matching_files = [file for file in files if file.startswith(iris_normalmap_prefix)]

			if matching_files:
				first_matching_file = matching_files[0]
				full_path = os.path.join(folder_path, first_matching_file)
				#print("Found matching file:", full_path)
				return full_path
			else:
				#print("No matching file found: ")
				return None

			
def set_colorsetter_eye_textures(active_object):

	colorsetter_material = active_object.active_material
	colorsetter_eye_node = None
	colorsetter_eye_multi_node = None
	colorsetter_eye_normal_node = None

	# Find the Colorsetter Eye Group node
	for node in colorsetter_material.node_tree.nodes:
		if node.type == 'GROUP' and node.name.startswith('colorsetter_eye_node_instance'):
			colorsetter_eye_node = node

	if colorsetter_eye_node:
		colorsetter_eye_multi_node = colorsetter_eye_node.inputs['Multi Texture'].links[0].from_node
		colorsetter_eye_normal_node = colorsetter_eye_node.inputs['Normal Texture'].links[0].from_node

	multimap_file_path = get_ffxiv_eye_multimap_file(active_object)
	normalmap_file_path = get_ffxiv_eye_normalmap_file(active_object)

	update_image_node_file(colorsetter_eye_multi_node,multimap_file_path)
	update_image_node_file(colorsetter_eye_normal_node,normalmap_file_path)
	

def update_image_node_file(image_node,file_path):

	image = None
	#check if this image exists, if it does, reuse it
	for img in bpy.data.images:
		if img.source == 'FILE' and img.filepath == file_path:
			image = img
			break

	# Open the image file
	if image is None:
		image = bpy.data.images.load(file_path)  # Load the image from the selected file path
	image_node.image = image 

	if file_path.endswith(("_d.png", "_d.bmp", "_d.dds")):
		return
	else:
		image_node.image.colorspace_settings.name = 'Non-Color'
		return
	
from . import import_ffxiv_charafile
def set_shader_defaults(active_armature,active_object,node_group_instance,shader_type):
	if shader_type == 'skin':
		node_group_instance.node_tree.nodes['Skin Tone'].inputs[6].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_skin'))
		node_group_instance.inputs['Enable SSS'].default_value = 0.025
		set_colorsetter_skin_textures(active_object)

	if shader_type == 'eye':
		set_colorsetter_eye_textures(active_object)
		node_group_instance.inputs['Eye Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_eyes'))
		node_group_instance.inputs['Odd Eye Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_odd_eye'))
		node_group_instance.inputs['Odd Eyes Enabled'].default_value = 1


	if shader_type == 'face':
		node_group_instance.inputs['Skin Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_skin'))
		node_group_instance.inputs['Lip Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_lips'))
		node_group_instance.inputs['Face Paint Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_facepaint'))
		node_group_instance.inputs['Enable SSS'].default_value = 0.025
		node_group_instance.inputs['Lip Color Enabled'].default_value = 1
		node_group_instance.inputs['Light/Dark Lips'].default_value = 0.5
		node_group_instance.inputs['Lip Brightness/Opacity'].default_value = 0.5


	if shader_type == 'hair':
		node_group_instance.inputs['Hair Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_hair'))
		node_group_instance.inputs['Highlights Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_hair_highlights'))
		node_group_instance.inputs['Enable Highlights'].default_value = 1

		
	if shader_type == 'faceacc':
		node_group_instance.inputs['Hair Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_hair'))
		node_group_instance.inputs['Tattoo Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_tattoo_limbal'))
		node_group_instance.inputs['Limbal Ring Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_tattoo_limbal'))
		node_group_instance.inputs['Hair Color Brighten'].default_value = 0.2
		node_group_instance.inputs['Limbal Ring Enabled'].default_value = 0.05
		node_group_instance.inputs['Limbal Ring Intensity'].default_value = 0

		
	if shader_type == 'tail':
		node_group_instance.inputs['Hair Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_hair'))
		node_group_instance.inputs['Highlight Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_hair_highlights'))
		node_group_instance.inputs['Enable Highlights'].default_value = 1



def replace_with_colorsetter_material(active_object,existing_shader_node,shader_type):

	existing_shader_node.node_tree

	if active_object.active_material:
		old_material = active_object.active_material

		colorsetter_material = bpy.data.materials.new(name=f"colorsetter_{shader_type}_"+ old_material.name.lstrip("backup_"))
		colorsetter_material.use_fake_user = False

		active_object.active_material = colorsetter_material
		colorsetter_material.use_nodes = True

		#delete the principled bsdf
		principled_bsdf = colorsetter_material.node_tree.nodes.get('Principled BSDF')
		colorsetter_material.node_tree.nodes.remove(principled_bsdf)

		material_output_node = colorsetter_material.node_tree.nodes.get('Material Output')

		#add new node group instance
		new_node_group_instance = colorsetter_material.node_tree.nodes.new(type='ShaderNodeGroup')
		new_node_group_instance.node_tree = existing_shader_node.node_tree
		new_node_group_instance.name = existing_shader_node.name
		

		##add a material output node
		material_output_node.location = (new_node_group_instance.location[0]+200,new_node_group_instance.location[1])

		
		#connect new node group instance to material output
		colorsetter_material.node_tree.links.new(new_node_group_instance.outputs[0], material_output_node.inputs[0])

		return colorsetter_material
		

	return


def add_colorsetter_shader(context,shader_type):

	shader_type_list = ['eye','face','hair','faceacc','tail','skin']

	shader_type_mat_dict = {'eye':'Eyes'
						,'face':'Face'
					 	,'hair':'Hair'
						,'faceacc':'Face_Acc'
						,'tail' : 'Hrothgar/Miqote Tail'
						,'skin' : 'Skin'
						}
		
	shader_type_node_group_dict = {'eye':'FFXIV Eye Shader'
									,'face':'FFXIV Face Shader'
					 				,'hair':'FFXIV Hair Shader'
									,'faceacc':'FFXIV Face Acc Shader'
									,'tail':'FFXIV Tail Shader'
									,'skin':'FFXIV Skin Shader'}

	if shader_type in shader_type_list:

		print (shader_type_mat_dict[shader_type])
		print (shader_type_node_group_dict[shader_type])

		active_material = context.active_object.active_material
		active_object = context.active_object
		active_armature = model.findArmature(active_object)

		#check if material is a colorsetter node material
		if active_material.name.startswith(f"colorsetter_{shader_type}_"):
			raise Exception(f"Cannot add colorsetter material as this is already a colorsetter material")
			
		else:
			old_material = active_material
			old_material.name = "backup_" + active_material.name  # Rename the old material
			old_material.use_fake_user=True #stores material in blend file even if not used after save
			colorsetter_material = None
			try:
				existing_shader_node = None

				if shader_type=='skin':
					existing_shader_node = find_existing_shader_type_in_armature(active_armature,shader_type)

				if existing_shader_node:
					colorsetter_material = replace_with_colorsetter_material(active_object,existing_shader_node,shader_type)
				else: 

					# Find the file path for WoL_Shader_V6.blend file
					file_path = (__file__ + r"assets\colorset_shaders\WoL_Shader_V6.blend").replace("shaders_colorsetter.py" , "")
									
					# Append the colorsetter material from WoL_Shader_V6.blend file to the blender project
					with bpy.data.libraries.load(file_path, link=False) as (data_from, data_to):

						# Append the material
						data_to.materials = [mat for mat in data_from.materials if mat == shader_type_mat_dict[shader_type]]

					# Check if the material was successfully appended
					if shader_type_mat_dict[shader_type] in bpy.data.materials:

						colorsetter_material = bpy.data.materials.get(shader_type_mat_dict[shader_type])
						colorsetter_material.name = f"colorsetter_{shader_type}_"+ active_material.name.lstrip("backup_")
						colorsetter_material.use_fake_user = False
						bpy.context.active_object.active_material = colorsetter_material
						
						#name the node group "colorsetter_{shader_type}_node_group"
						if colorsetter_material.node_tree.nodes['Group'].node_tree.name.startswith (shader_type_node_group_dict[shader_type]):
							colorsetter_material.node_tree.nodes['Group'].node_tree.name = f"colorsetter_{shader_type}_node_group"

						#name the instance of the node group within the material to colorsetter_{shader_type}_node_instance
						if colorsetter_material.node_tree.nodes['Group'].node_tree.name.startswith(f"colorsetter_{shader_type}_node_group"):
							colorsetter_material.node_tree.nodes['Group'].name = f"colorsetter_{shader_type}_node_instance"
							node_group_instance = colorsetter_material.node_tree.nodes.get(f"colorsetter_{shader_type}_node_instance")

							#set the default values to the ones from the .chara file that were stored as custom properties on the armature
							if active_armature:
								set_shader_defaults(active_armature,active_object,node_group_instance,shader_type)

	
					else:
						print(f"Material '{shader_type_mat_dict[shader_type]}' not found in the source file.")
				
			except:
				bpy.context.active_object.active_material = old_material
				old_material.name = old_material.name.lstrip('backup_')

				if colorsetter_material:
					bpy.data.materials.remove(colorsetter_material)

				raise Exception(f"Failed to add Colorsetter {shader_type} shader")
			
			finally:
				#loop through all the meshes that use the old material and set them to use the colorsetter material
				if colorsetter_material and old_material:
					for obj in bpy.data.objects:
						if obj.type == 'MESH':
							if obj.active_material == old_material:
								obj.active_material = colorsetter_material

	
	return
			
def remove_colorsetter_shader (context,shader_type):

	shader_type_list = ['eye','face','hair','faceacc','tail','skin','gear']

	if shader_type in shader_type_list:

		active_material = context.active_object.active_material
		shader_node_instance = None
		shader_node_group = None
		if active_material.name.startswith(f"colorsetter_{shader_type}_"):
			for instance_node in active_material.node_tree.nodes:
				if instance_node.type =='GROUP' and instance_node.name.startswith(f"colorsetter_{shader_type}_node_instance"):
					shader_node_instance = instance_node
					shader_node_group = shader_node_instance.node_tree

					if shader_type == 'gear':
						detail_texture_output_node = shader_node_group.nodes.get('Group').node_tree
						colorset_ramps_node = detail_texture_output_node.nodes.get('Group.017').node_tree
						detail_combine_node = detail_texture_output_node.nodes.get('Group.018').node_tree
						normal_details_combine_node = detail_texture_output_node.nodes.get('Group.022').node_tree
						normal_combine_node = normal_details_combine_node.nodes.get('Group').node_tree
						tilescale_skew_node = detail_texture_output_node.nodes.get('Group.021').node_tree

					break
			selected_material_name = active_material.name[len(f"colorsetter_{shader_type}_"):]
		backup_material = bpy.data.materials.get('backup_' + selected_material_name) 
		active_object = bpy.context.active_object

		#if active material, active object, and shader_node_instance found
		if active_material.name.startswith(f"colorsetter_{shader_type}_") and backup_material and active_object and shader_node_instance:
			for obj in bpy.data.objects:
				if obj.type =='MESH':
					#set the backup material as the active material, and restore it's original name
					if obj.active_material == active_material:
						obj.active_material = backup_material
			backup_material.name = backup_material.name.lstrip('backup_')
			#delete the active material
			bpy.data.materials.remove(active_material)
			#delete the shader node group
			if shader_node_group:

				if shader_type == 'gear':
					bpy.data.node_groups.remove(detail_texture_output_node)
					bpy.data.node_groups.remove(colorset_ramps_node)
					bpy.data.node_groups.remove(detail_combine_node)
					bpy.data.node_groups.remove(normal_details_combine_node)
					bpy.data.node_groups.remove(normal_combine_node)
					bpy.data.node_groups.remove(tilescale_skew_node)

				if shader_node_group.users == 0:
					bpy.data.node_groups.remove(shader_node_group)
	return

from bpy_extras.io_utils import ImportHelper
@register_wrap
class UpdateColorsetterImageNodeFile(bpy.types.Operator, ImportHelper):
	"""Open a File Browser to Select Image"""
	bl_idname = "ffxiv_mmd.update_colorsetter_image_node"
	bl_label = "Open a File Browser to Select Image"
	bl_options = {'REGISTER', 'UNDO'}

	image_node_name = bpy.props.StringProperty(name="image_node_name", update=None, get=None, set=None)

	filename_ext = ".png;.bmp;.dds"
	filter_glob: bpy.props.StringProperty(
		default="*.png;*.bmp;*.dds",
		options={'HIDDEN'},
	)
	
	def execute(self, context):
		filepath = self.filepath
		active_mat = context.active_object.active_material

		image_node = active_mat.node_tree.nodes.get(self.image_node_name)	

		if image_node:
			update_image_node_file(image_node,filepath)
		else:

			for node in active_mat.node_tree.nodes:
				if node.type == 'GROUP' and node.name.startswith('colorsetter_skin_node_instance'):
					colorsetter_skin_node = node
					break

			if colorsetter_skin_node:
				image_node = colorsetter_skin_node.node_tree.nodes.get(self.image_node_name)

			if image_node:
				update_image_node_file(image_node,filepath)
		
		return {'FINISHED'}
	
@register_wrap
class ApplyColorsetterShader(bpy.types.Operator):
	"""Apply Colorsetter Shader"""
	bl_idname = "ffxiv_mmd.apply_colorsetter_shader"
	bl_label = "Apply Colorsetter Shader"
	bl_options = {'REGISTER', 'UNDO'}

	shader_type_list = ['eye','face','hair','faceacc','tail','skin']
	shader_type = bpy.props.StringProperty(name="shader_type", update=None, get=None, set=None)

	def execute(self, context):
		if self.shader_type in self.shader_type_list:
			add_colorsetter_shader(context,self.shader_type)
		return {'FINISHED'}
	
@register_wrap
class RemoveColorsetterShader(bpy.types.Operator):
	"""Remove Colorsetter Shader"""
	bl_idname = "ffxiv_mmd.remove_colorsetter_shader"
	bl_label = "Remove Colorsetter Shader"
	bl_options = {'REGISTER', 'UNDO'}

	shader_type_list = ['eye','face','hair','faceacc','tail','skin','gear']
	shader_type = bpy.props.StringProperty(name="shader_type", update=None, get=None, set=None)

	def execute(self, context):
		if self.shader_type in self.shader_type_list:
			remove_colorsetter_shader(context,self.shader_type)
		return {'FINISHED'}




