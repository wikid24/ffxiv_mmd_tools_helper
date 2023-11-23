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


def apply_texture_file_to_colorset_node(node_label,texture_file):
	for obj in bpy.context.selected_objects:
		if obj.type =='MESH' and obj.active_material.is_colorset:
			for slot in obj.material_slots:
					mat = slot.material

					for node in mat.node_tree.nodes:
						if node.label == node_label:
							node.image = texture_file



def fix_normalmap ():
	for obj in bpy.context.selected_objects:
		if obj.type =='MESH' and obj.active_material.is_colorset:    
			for slot in obj.material_slots:
				mat = slot.material
				
				#print (f"The material in slot {slot.name} of object {obj.name} is {mat.name}")
				
				normal_texture_node = None
				
				
				#set the 'Normal Texture' node's Colorspace to Non-Colour
				for node in mat.node_tree.nodes:
					#print (f"Name: {node.name}, Label: {node.label}")
					if node.label =='Normal Texture':
						normal_texture_node = node
						if node.image:
							node.image.colorspace_settings.name = 'Non-Color'
				#set the 'Normal Texture (Closest)' node's to the same image as 'Normal Texture'
				if normal_texture_node:
					for node in mat.node_tree.nodes:
						#print (f"Name: {node.name}, Label: {node.label}")
						if node.label =='Normal Texture (Closest)':
							node.image = normal_texture_node.image

def fix_material_output_node():
	#if "Principled BSDF" node output BSDF is not connected to "Material Output" node Surface input, then connect them
	if bpy.context.active_object:
		obj = bpy.context.active_object
		if obj.type =='MESH' and obj.active_material.is_colorset:
			
			mat = obj.active_material

			principled_bsdf = None
			material_output = None
			
			for node in mat.node_tree.nodes:
				if node.name =='Principled BSDF':
					principled_bsdf = node
					#print (principled_bsdf)

				if node.name =='Material Output':
					material_output = node
					#print (material_output)

				#mat.node_tree.links.new(material_output.inputs['Surface'], principled_bsdf.outputs['BSDF'])
				#bpy.context.selected_objects[0].active_material.node_tree.links.new(material_output.inputs['Surface'],principled_bsdf.outputs['BSDF'])
				if principled_bsdf and material_output:
					mat.node_tree.links.new(material_output.inputs['Surface'],principled_bsdf.outputs['BSDF'])
				#if principled_bsdf.output

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

					old_material.use_fake_user = True #stores material in blend file even if not used after save


					return old_material
				

def apply_textures_to_colorset_material(context,folder_path):
	if bpy.context.active_object:
			obj = bpy.context.active_object

			if obj.type =='MESH' and obj.active_material.is_colorset :

				#model_id = obj.data['ModelID']
				#new_material = obj.active_material

				colorset_files = [f for f in os.listdir(context.scene.shaders_texture_folder) if f.endswith('_a.dds') ]
				multimap_files = [f for f in os.listdir(context.scene.shaders_texture_folder) if f.endswith('_m.bmp') or f.endswith('_d.png') or f.endswith('_d.bmp') or f.endswith('_s.png')]
				normalmap_files = [f for f in os.listdir(context.scene.shaders_texture_folder) if f.endswith('_n.bmp') or f.endswith('_n.png')]
				specular_files = [f for f in os.listdir(context.scene.shaders_texture_folder) if f.endswith('_s.bmp') or f.endswith('_s.png')]
				diffuse_files = [f for f in os.listdir(context.scene.shaders_texture_folder) if f.endswith('_d.bmp') or f.endswith('_d.png')]
				colorset_filename = None
				multimap_filename = None
				normalmap_filename = None
				specular_filename = None


				if colorset_files:
					colorset_filename = folder_path+colorset_files[0]
					#print(f"Colorset file found: {colorset_filename}")
					try:
						apply_colorset_file(colorset_filename)
					except:
						#display_error_message=  "ERROR: could not apply ",colorset_filename
						print("ERROR: could not apply ",colorset_filename)
						#bpy.context.window_manager.popup_menu(display_error_message, title="Error Message", icon='ERROR')
						return obj.active_material

				else:
					print("No colorset file ending with '_a' found in the folder.")
										
						
				if multimap_files:
					multimap_filename = folder_path+multimap_files[0]
					# Specify the name of the image you want to check
					if multimap_files[0] not in bpy.data.images:
						multimap = bpy.data.images.load(multimap_filename)
						
					else:
						multimap = bpy.data.images[multimap_files[0]]
						print(f"Multimap file found: {multimap_filename}")
						print(f"Multimap: {multimap}")
					#apply_multimap_file(multimap)
					apply_texture_file_to_colorset_node('MultiTexture',multimap)
				else:
					print("No multimap file ending with '_m' or '_s' found in the folder.")
					
						
				if normalmap_files:
					normalmap_filename = folder_path+normalmap_files[0]
					if normalmap_files[0] not in bpy.data.images:
						normalmap = bpy.data.images.load(normalmap_filename)
					
					else:
						normalmap = bpy.data.images[normalmap_files[0]]
					#print(f"Normalmap file found: {normalmap_filename}")
					#apply_normalmap_file(normalmap)
					apply_texture_file_to_colorset_node('Normal Texture',normalmap)
					fix_normalmap()
				else:
					print("No normalmap file ending with '_n' found in the folder.")

				if specular_files:
					specular_filename = folder_path+specular_files[0]
					if specular_files[0] not in bpy.data.images:
						specular = bpy.data.images.load(specular_filename)
						#apply_normalmap_file(normalmap)
					else:
						specular = bpy.data.images[specular_files[0]]
					#print(f"Specular file found: {normalmap_filename}")
					#apply_specular_file(specular)
					apply_texture_file_to_colorset_node('Specular Texture',specular)
				else:
					print("No specular file ending with '_s' found in the folder.")


				if diffuse_files:
					diffuse_filename = folder_path+diffuse_files[0]
					if diffuse_files[0] not in bpy.data.images:
						diffuse = bpy.data.images.load(diffuse_filename)
						#apply_normalmap_file(normalmap)
					else:
						diffuse = bpy.data.images[diffuse_files[0]]
					#print(f"Diffuse file found: {normalmap_filename}")
					#apply_diffuse_file(diffuse)
					apply_texture_file_to_colorset_node('Diffuse Texture',diffuse)
				else:
					print("No diffuse file ending with '_d' found in the folder.")						
										

				fix_material_output_node()
			
				return obj.active_material


def undo_if_colorset_plugin_error(obj,old_material,new_material):

	if new_material.is_colorset:


		diffuse_node = None
		specular_node = None
		multitexture_node = None
		normaltexture_node = None
		normaltexture_closest_node = None
		specularmask_node = None

		#for slot in obj.material_slots:
		#	mat = slot.material
		for node in new_material.node_tree.nodes:
			if node.label =='Diffuse Texture':
				diffuse_node = node
			if node.label =='Specular Texture':
				specular_node = node
			if node.label == 'MultiTexture':
				multitexture_node = node
			if node.label == 'Normal Texture':
				normaltexture_node = node
			if node.label == 'Normal Texture (Closest)':
				normaltexture_closest_node = node
			if node.label == 'Specular Mask Texture (SET TO NON-COLOR)':

				specularmask_node = node

		#for i in [diffuse_node.image,specular_node.image,multitexture_node.image,normaltexture_node.image,normaltexture_closest_node.image,specularmask_node.image]:
			#print (i)

		if (diffuse_node.image or specular_node.image or multitexture_node.image or normaltexture_node.image or normaltexture_closest_node.image or specularmask_node.image):
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

		#if not(diffuse_node,specular_node,multitexture_node,normaltexture_node,normaltexture_closest_node, specularmask_node):

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
	




@register_wrap
class SelectMaterialsFolder(bpy.types.Operator):
	"""Apply the Colorsetter addon to the selected mesh using DDS/PNG/BMP textures from the selected folder"""
	bl_idname = "ffxiv_mmd.select_materials_folder"
	bl_label = "Select Materials Folder"
	bl_options = {'REGISTER', 'UNDO'}

	#folder_path = "yoooooo"
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
		if addon_name not in bpy.context.preferences.addons.keys():

			raise Exception(f"The addon '{addon_name}' is not installed or is not enabled. Please install and enable it.")
		else:
			#print(f"The addon '{addon_name}' is installed and enabled.")

			context.scene.shaders_texture_folder = bpy.path.abspath(context.scene.shaders_texture_folder)
			folder_path = context.scene.shaders_texture_folder
			print (folder_path)
			#context.scene.ffxiv_mmd.select_materials_folder.folder_path
			
			old_material = None
			new_material = None
			
			if bpy.context.active_object:

				obj = bpy.context.active_object

				if obj.type == 'MESH':
					old_material = apply_colorset_plugin()
					new_material = apply_textures_to_colorset_material(context,folder_path).id_data

					if undo_if_colorset_plugin_error(bpy.context.active_object,old_material, new_material):
						#if no errors, apply to all materials 
						print ("no errors ya'll!")
						apply_material_to_all_matching_ffxiv_meshes (obj)
					else:
						print ("ERROR: COULD NOT APPLY THE COLORSETTER PLUGIN (probably a 'Import DDS' error in Colorsetter addon)")					
				
			# return {"CANCELLED"}

			return {'FINISHED'}
	



	

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
			try:
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

						#set the default color values to the ones from the .chara file that were stored as custom properties on the armature
						if active_armature:
							if shader_type == 'skin':
								node_group_instance.inputs['Skin Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_skin'))
						
							if shader_type == 'eye':
								set_colorsetter_eye_textures(active_object)
								node_group_instance.inputs['Eye Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_eyes'))
								node_group_instance.inputs['Odd Eye Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_odd_eye'))

							if shader_type == 'face':
								node_group_instance.inputs['Skin Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_skin'))
								node_group_instance.inputs['Lip Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_lips'))
								node_group_instance.inputs['Face Paint Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_facepaint'))
	

							if shader_type == 'hair':
								node_group_instance.inputs['Hair Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_hair'))
								node_group_instance.inputs['Highlights Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_hair_highlights'))

								
							if shader_type == 'faceacc':
								node_group_instance.inputs['Hair Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_hair'))
								node_group_instance.inputs['Tattoo Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_tattoo_limbal'))
								node_group_instance.inputs['Limbal Ring Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_tattoo_limbal'))
								
							if shader_type == 'tail':
								node_group_instance.inputs['Hair Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_hair'))
								node_group_instance.inputs['Highlight Color'].default_value = import_ffxiv_charafile.hex_to_rgba(active_armature.data.get('color_hex_hair_highlights'))
	
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

	shader_type_list = ['eye','face','hair','faceacc','tail','skin']

	if shader_type in shader_type_list:

		active_material = context.active_object.active_material
		shader_node_instance = None
		shader_node_group = None
		if active_material.name.startswith(f"colorsetter_{shader_type}_"):
			for instance_node in active_material.node_tree.nodes:
				if instance_node.type =='GROUP' and instance_node.name.startswith(f"colorsetter_{shader_type}_node_instance"):
					shader_node_instance = instance_node
					shader_node_group = shader_node_instance.node_tree
					break
			selected_material_name = active_material.name[len(f"colorsetter_{shader_type}_"):]
		backup_material = bpy.data.materials.get('backup_' + selected_material_name) 
		active_object = bpy.context.active_object

		#if active material, active object, and eye_shader_node_instance found
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
		active_mat = context.active_object.active_material
		image_node = active_mat.node_tree.nodes.get(self.image_node_name)
		
		filepath = self.filepath

		if image_node:
			update_image_node_file(image_node,filepath)
		return {'FINISHED'}
	

@register_wrap
class ApplyColorsetterEyeShader(bpy.types.Operator):
	"""Apply Colorsetter Eye Shader"""
	bl_idname = "ffxiv_mmd.apply_colorsetter_eye_shader"
	bl_label = "Apply Colorsetter Eye Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		add_colorsetter_shader(context,"eye")
		return {'FINISHED'}
	
	
@register_wrap
class RemoveColorsetterEyeShader(bpy.types.Operator):
	"""Remove Colorsetter Eye Shader"""
	bl_idname = "ffxiv_mmd.remove_colorsetter_eye_shader"
	bl_label = "Remove Colorsetter Eye Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		remove_colorsetter_shader(context,'eye')
		return {'FINISHED'}

@register_wrap
class ApplyColorsetterHairShader(bpy.types.Operator):
	"""Apply Colorsetter Hair Shader"""
	bl_idname = "ffxiv_mmd.apply_colorsetter_hair_shader"
	bl_label = "Apply Colorsetter Hair Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		add_colorsetter_shader(context,"hair")
		return {'FINISHED'}
	
@register_wrap
class RemoveColorsetterHairShader(bpy.types.Operator):
	"""Remove Colorsetter Hair Shader"""
	bl_idname = "ffxiv_mmd.remove_colorsetter_hair_shader"
	bl_label = "Remove Colorsetter Hair Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		remove_colorsetter_shader(context,'hair')
		return {'FINISHED'}
	
@register_wrap
class ApplyColorsetterFaceShader(bpy.types.Operator):
	"""Apply Colorsetter Face Shader"""
	bl_idname = "ffxiv_mmd.apply_colorsetter_face_shader"
	bl_label = "Apply Colorsetter Face Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		add_colorsetter_shader(context,"face")
		return {'FINISHED'}
	
@register_wrap
class RemoveColorsetterFaceShader(bpy.types.Operator):
	"""Remove Colorsetter Face Shader"""
	bl_idname = "ffxiv_mmd.remove_colorsetter_face_shader"
	bl_label = "Remove Colorsetter Face Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		remove_colorsetter_shader(context,'face')
		return {'FINISHED'}
	

@register_wrap
class ApplyColorsetterFaceAccShader(bpy.types.Operator):
	"""Apply Colorsetter Face Accent Shader"""
	bl_idname = "ffxiv_mmd.apply_colorsetter_faceacc_shader"
	bl_label = "Apply Colorsetter Face Accent Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		add_colorsetter_shader(context,"faceacc")
		return {'FINISHED'}
	
@register_wrap
class RemoveColorsetterFaceAccShader(bpy.types.Operator):
	"""Remove Colorsetter Face Accent Shader"""
	bl_idname = "ffxiv_mmd.remove_colorsetter_faceacc_shader"
	bl_label = "Remove Colorsetter Face Accent Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		remove_colorsetter_shader(context,'faceacc')
		return {'FINISHED'}
	
@register_wrap
class ApplyColorsetterTailShader(bpy.types.Operator):
	"""Apply Colorsetter Tail Shader"""
	bl_idname = "ffxiv_mmd.apply_colorsetter_tail_shader"
	bl_label = "Apply Colorsetter Tail Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		add_colorsetter_shader(context,"tail")
		return {'FINISHED'}
	
@register_wrap
class RemoveColorsetterTailShader(bpy.types.Operator):
	"""Remove Colorsetter Tail Shader"""
	bl_idname = "ffxiv_mmd.remove_colorsetter_tail_shader"
	bl_label = "Remove Colorsetter Tail Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		remove_colorsetter_shader(context,'tail')
		return {'FINISHED'}
	
@register_wrap
class ApplyColorsetterSkinShader(bpy.types.Operator):
	"""Apply Colorsetter Skin Shader"""
	bl_idname = "ffxiv_mmd.apply_colorsetter_skin_shader"
	bl_label = "Apply Colorsetter Skin Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		add_colorsetter_shader(context,"skin")
		return {'FINISHED'}
	
@register_wrap
class RemoveColorsetterSkinShader(bpy.types.Operator):
	"""Remove Colorsetter Skin Shader"""
	bl_idname = "ffxiv_mmd.remove_colorsetter_skin_shader"
	bl_label = "Remove Colorsetter Skin Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		remove_colorsetter_shader(context,'skin')
		return {'FINISHED'}
	




