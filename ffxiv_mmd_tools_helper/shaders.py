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
	


def apply_glossy_shader():
	active_object = bpy.context.active_object
	if active_object and active_object.active_material:
		active_material = active_object.active_material
		if active_material.node_tree:
			for node in active_material.node_tree.nodes:
				if node.name == 'Material Output':
					material_output = active_material.node_tree.nodes['Material Output']
					
					#get main shader from Material Output
					if not material_output.inputs[0].links[0].from_node.name=='Mix Shader':
						main_shader = material_output.inputs[0].links[0].from_node
					else:
						mix_shader = active_material.node_tree.nodes['Mix Shader']
						main_shader = mix_shader.inputs[1].links[0].from_node
					
					
					# Add a Mix Shader node
					mix_shader = None
					if 'Mix Shader' in active_material.node_tree.nodes:
						mix_shader = active_material.node_tree.nodes['Mix Shader']
					else:
						mix_shader = active_material.node_tree.nodes.new(type='ShaderNodeMixShader')
						mix_shader.name = 'ffxiv_mmd_glossy_mix_shader'
						mix_shader.location = material_output.location
						mix_shader.location.x = mix_shader.location.x - 200
					
					#connect Mix Shader to Material Output    
					active_material.node_tree.links.new(mix_shader.outputs[0], material_output.inputs[0])

					# Connect Main Shader to Mix Shader
					active_material.node_tree.links.new(main_shader.outputs[0], mix_shader.inputs[1])
					
					
					# Add a Glossy BSDF node
					glossy_bsdf = None
					if 'Glossy BSDF' in active_material.node_tree.nodes:
						glossy_bsdf = active_material.node_tree.nodes['Glossy BSDF']
					else:
						glossy_bsdf = active_material.node_tree.nodes.new(type='ShaderNodeBsdfGlossy')
						glossy_bsdf.name = 'ffxiv_mmd_glossy'
						glossy_bsdf.location = mix_shader.location
						glossy_bsdf.location.y = glossy_bsdf.location.y - 400
						
					#connect glossy bsdf to mix shader node
					active_material.node_tree.links.new(glossy_bsdf.outputs[0], mix_shader.inputs[2])
					
					#get node connected from main_shader 'Base Color'
					if main_shader.name == 'Principled BSDF':
						diffuse_node = main_shader.inputs[0].links[0].from_node
					if main_shader.name == 'mmd_shader':
						diffuse_node = main_shader.inputs['Base Tex'].links[0].from_node
							
					# Connect diffuse_node to Glossy BSDF
					active_material.node_tree.links.new(diffuse_node.outputs['Color'], glossy_bsdf.inputs[0]) 
					
					#get node connected from Principled BSDF 'Normal'
					if main_shader.name == 'Principled BSDF':
						normalmap_node = main_shader.inputs['Normal'].links[0].from_node
					else:
						normalmap_node = active_material.node_tree.nodes['Normal Map']
					
					#connect normalmap_node to Glossy BSDF
					active_material.node_tree.links.new(normalmap_node.outputs[0], glossy_bsdf.inputs[2]) 
				
def remove_glossy_shader():
	active_object = bpy.context.active_object
	if active_object and active_object.active_material:
		active_material = active_object.active_material
		if active_material.node_tree:
			glossy_bsdf = active_material.node_tree.nodes.get('ffxiv_mmd_glossy')
			ffxiv_mmd_glossy_mix_shader = active_material.node_tree.nodes.get('ffxiv_mmd_glossy_mix_shader')
			material_output = active_material.node_tree.nodes['Material Output']
			main_shader = ffxiv_mmd_glossy_mix_shader.inputs[1].links[0].from_node

			#connect mix shader input to material_output's output
			active_material.node_tree.links.new(main_shader.outputs[0],  material_output.inputs[0]) 

			if glossy_bsdf:
				active_material.node_tree.nodes.remove(glossy_bsdf)

			if ffxiv_mmd_glossy_mix_shader:
				active_material.node_tree.nodes.remove(ffxiv_mmd_glossy_mix_shader)




@register_wrap
class ApplyGlossyShader(bpy.types.Operator):
	"""Can make skin / hair / iris look shiny"""
	bl_idname = "ffxiv_mmd.apply_glossy_shader"
	bl_label = "Add Glossy Shader to Material"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.active_object is not None and context.active_object.type == 'MESH'

	def execute(self, context):
		apply_glossy_shader()
		return {'FINISHED'}
	
@register_wrap
class RemoveGlossyShader(bpy.types.Operator):
	"""Remove the glossy shader"""
	bl_idname = "ffxiv_mmd.remove_glossy_shader"
	bl_label = "Remove the glossy shader"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.active_object is not None and context.active_object.type == 'MESH'

	def execute(self, context):
		remove_glossy_shader()
		return {'FINISHED'}



@register_wrap
class SelectMaterialsFolder(bpy.types.Operator):
	"""User can select the folder for materials"""
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
	



def _update_mektools_skin_props(self,context):

	mektools_skin_node = None

	for instance_node in context.active_object.active_material.node_tree.nodes:
		if instance_node.type =='GROUP' and instance_node.node_tree.name == 'FFXIV Skin Shader':
			#mektools_skin_node = context.active_object.active_material.node_tree.nodes['Group']
			mektools_skin_node = instance_node 
			break
	if mektools_skin_node:
		mektools_skin_node.node_tree.nodes['SSS'].outputs[0].default_value = self.mektools_skin_prop_sss
		mektools_skin_node.node_tree.nodes['Specular'].outputs[0].default_value = self.mektools_skin_prop_specular
		mektools_skin_node.node_tree.nodes['Wet'].outputs[0].default_value = self.mektools_skin_prop_wet
		mektools_skin_node.node_tree.nodes['Roughness'].outputs[0].default_value = self.mektools_skin_prop_roughness

	return

def _get_mektools_skin_props(self,context):

	mektools_skin_node = None

	for instance_node in context.active_object.active_material.node_tree.nodes:
		if instance_node.type =='GROUP' and instance_node.node_tree.name == 'FFXIV Skin Shader':
			#mektools_skin_node = context.active_object.active_material.node_tree.nodes['Group']
			mektools_skin_node = instance_node 
			break
	if mektools_skin_node:
		context.scene.mektools_skin_prop_sss = mektools_skin_node.node_tree.nodes['SSS'].outputs[0].default_value 
		context.scene.mektools_skin_prop_specular = mektools_skin_node.node_tree.nodes['Specular'].outputs[0].default_value
		context.scene.mektools_skin_prop_wet = mektools_skin_node.node_tree.nodes['Wet'].outputs[0].default_value
		context.scene.mektools_skin_prop_roughness = mektools_skin_node.node_tree.nodes['Roughness'].outputs[0].default_value

	return

import mek_tools
import addon_utils

@register_wrap
class ApplyMekToolsSkinShader(bpy.types.Operator):
	"""Apply MekTools Skin Shader"""
	bl_idname = "ffxiv_mmd.apply_mektools_skin_shader"
	bl_label = "Apply MekTools Skin Shader"
	bl_options = {'REGISTER', 'UNDO'}

	

	bpy.types.Scene.mektools_skin_prop_sss = bpy.props.FloatProperty(name='Subsurface', min= 0,max=0.3,default=0.025, update = _update_mektools_skin_props)
	bpy.types.Scene.mektools_skin_prop_specular = bpy.props.FloatProperty(name='Specular', min= 0,max=1,default=0.03, update = _update_mektools_skin_props) 
	bpy.types.Scene.mektools_skin_prop_wet = bpy.props.FloatProperty(name='Wet', min= 0,max=5,default=0, update = _update_mektools_skin_props) 
	bpy.types.Scene.mektools_skin_prop_roughness = bpy.props.FloatProperty(name='Roughness', min= 0,max=1,default=0.015, update = _update_mektools_skin_props) 

	def execute(self, context):

		addon_name = 'mek_tools'
		addon_required_version = '0.35'
		addon_module = [m for m in addon_utils.modules() if m.__name__ == addon_name][0] # get module
		if addon_module:
			installed_version = addon_module.bl_info.get('version',(-1,-1,-1))
			installed_version = float(str(installed_version[0])+'.'+str(installed_version[1])+str(installed_version[2]))

		# Check if the addon is enabled
		if addon_name not in bpy.context.preferences.addons.keys():
			raise Exception(f"The addon '{addon_name}' is not installed or is not enabled. Please install and enable it.")
		elif  installed_version < float(addon_required_version):
			raise Exception(f"Addon '{addon_name}' version is {installed_version} please install {addon_required_version} or higher.")
		else:

			mek_tools.check_for_nodes()
			active_material = bpy.context.active_object.active_material
			active_object = bpy.context.active_object

			#check if mektools skin node is already added
			for instance_node in active_material.node_tree.nodes:
				if instance_node.type =='GROUP' and instance_node.node_tree.name in ('FFXIV Skin Shader','FFXIV Eye Shader'):
					break
			else:
				# Duplicate the material
				old_material = active_material.copy()
				old_material.name = "backup_" + active_material.name  # Rename the duplicated material if needed
				try:
					mek_tools.change_material(active_material)
					active_material.name = "mektools_"+ active_material.name
				except:
					bpy.context.active_object.active_material = old_material
					old_material.name = old_material.name.lstrip('backup_')
					bpy.data.materials.remove(active_material)
					raise Exception(f"Failed to apply MekTools skin shader, probably because it was already using an MMD skin shader. I'll fix it eventually")

		return {'FINISHED'}
	
@register_wrap
class RemoveMekToolsSkinShader(bpy.types.Operator):
	"""Remove MekTools Skin Shader"""
	bl_idname = "ffxiv_mmd.remove_mektools_skin_shader"
	bl_label = "Remove MekTools Skin Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		
		active_material = bpy.context.active_object.active_material
		skin_shader_node = None
		if active_material.name.startswith('mektools_'):
			for instance_node in active_material.node_tree.nodes:
				if instance_node.type =='GROUP' and instance_node.node_tree.name == ('FFXIV Skin Shader'):
					skin_shader_node = instance_node
					break
			selected_material_name = active_material.name[len('mektools_'):]
		backup_material = bpy.data.materials.get('backup_' + selected_material_name) 
		selected_objects = bpy.context.active_object

	
		if active_material.name.startswith('mektools_') and backup_material and selected_objects and skin_shader_node:
			for obj in bpy.data.objects:
				if obj.type =='MESH':
					if obj.active_material == active_material:
						obj.active_material = backup_material
			backup_material.name = backup_material.name.lstrip('backup_')
			bpy.data.materials.remove(active_material)
		return {'FINISHED'}
	

def _update_mektools_eye_props(self,context):

	mektools_eye_node = None

	for instance_node in context.active_object.active_material.node_tree.nodes:
		if instance_node.type =='GROUP' and instance_node.node_tree.name == 'FFXIV Eye Shader':
			#mektools_skin_node = context.active_object.active_material.node_tree.nodes['Group']
			mektools_eye_node = instance_node 
			break
	if mektools_eye_node:
		mektools_eye_node.inputs["Eye Index"].default_value = float(self.eye_shader_ffxiv_model_list)
		#mektools_eye_node.node_tree.nodes['SSS'].outputs[0].default_value = self.mektools_skin_prop_sss

	return
	
@register_wrap
class ApplyMekToolsEyeShader(bpy.types.Operator):
	"""Apply MekTools Eye Shader"""
	bl_idname = "ffxiv_mmd.apply_mektools_eye_shader"
	bl_label = "Apply MekTools Eye Shader"
	bl_options = {'REGISTER', 'UNDO'}

	#bpy.types.Scene.mektools_eye_prop_color = bpy.props.FloatProperty(name='Subsurface', min= 0,max=0.3,default=0.025, update = _update_mektools_skin_props)

	bpy.types.Scene.eye_shader_ffxiv_model_list = bpy.props.EnumProperty(items = \
	[("1", "Lalafell Type 1","Lalafell Type 1") \
	, ("2", "Lalafell Type 2","Lalafell Type 2") \
	, ("3", "Miqo'te Type 1","Miqo'te Type 1") \
	, ("4", "Miqo'te Type 2","Miqo'te Type 2") \
	, ("5", "Au Ra","Au Ra") \
	, ("6", "Viera","Viera") \
	, ("7", "Hyur Midlander","Hyur Midlander") \
	, ("8", "Hyur Highlander","Hyur Highlander") \
	, ("9", "Elezen","Elezen") \
	, ("10", "Roegadyn","Roegadyn") \
	, ("11", "Hrothgar","Hrothgar") \
	, ("12", "Custom","Custom") \
	], name = "Eye Type", default = "4", update = _update_mektools_eye_props)

	def execute(self, context):

		addon_name = 'mek_tools'
		addon_required_version = '0.35'
		addon_module = [m for m in addon_utils.modules() if m.__name__ == addon_name][0] # get module
		if addon_module:
			installed_version = addon_module.bl_info.get('version',(-1,-1,-1))
			installed_version = float(str(installed_version[0])+'.'+str(installed_version[1])+str(installed_version[2]))

		# Check if the addon is enabled
		if addon_name not in bpy.context.preferences.addons.keys():
			raise Exception(f"The addon '{addon_name}' is not installed or is not enabled. Please install and enable it.")
		elif  installed_version < float(addon_required_version):
			raise Exception(f"Addon '{addon_name}' version is {installed_version} please install {addon_required_version} or higher.")
		else:

			#mek_tools.check_for_nodes()
			active_material = bpy.context.active_object.active_material
			active_object = bpy.context.active_object
			eye_shader_node = None
			eye_shader_node_instance = None

			#check if mektools eye node is already added
			for instance_node in active_material.node_tree.nodes:
				if instance_node.type =='GROUP' and instance_node.node_tree.name.startswith ('FFXIV Eye Shader'):
					eye_shader_node = active_material.node_tree
					eye_shader_node_instance = instance_node
					break

			if eye_shader_node is None and eye_shader_node_instance is None:
				# Duplicate the material
				old_material = active_material.copy()
				old_material.name = "backup_" + active_material.name  # Rename the duplicated material if needed
				try:
					mek_tools.add_eyes(active_material)
					active_material.name = "mektools_"+ active_material.name
					for instance_node in active_material.node_tree.nodes:
						if instance_node.type =='GROUP' and instance_node.node_tree.name.startswith('FFXIV Eye Shader'):
							eye_shader_node_instance = instance_node
							eye_shader_node_instance.name = 'mektools_eye_node_group_instance'
				except:
					bpy.context.active_object.active_material = old_material
					old_material.name = old_material.name.lstrip('backup_')
					bpy.data.materials.remove(active_material)
					raise Exception(f"Failed to apply MekTools eye shader, probably because it was already using an MMD eye shader. I'll fix it eventually")
				finally:
					context.scene.eye_shader_ffxiv_model_list = "4"
		return {'FINISHED'}
	
@register_wrap
class RemoveMekToolsEyeShader(bpy.types.Operator):
	"""Remove MekTools Eye Shader"""
	bl_idname = "ffxiv_mmd.remove_mektools_eye_shader"
	bl_label = "Remove MekTools Eye Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		
		active_material = bpy.context.active_object.active_material
		eye_shader_node = None
		eye_shader_node_instance = None
		if active_material.name.startswith('mektools_'):
			for instance_node in active_material.node_tree.nodes:
				if instance_node.type =='GROUP' and instance_node.name.startswith ('mektools_eye_node_group_instance'):
					eye_shader_node_instance = instance_node
					break
			active_material_name = active_material.name[len('mektools_'):]
		backup_material = bpy.data.materials.get('backup_' + active_material_name) 
		selected_objects = bpy.context.active_object

	
		if active_material.name.startswith('mektools_') and backup_material and selected_objects and eye_shader_node_instance:
			for obj in bpy.data.objects:
				if obj.type =='MESH':
					if obj.active_material == active_material:
						obj.active_material = backup_material
			backup_material.name = backup_material.name.lstrip('backup_')
			bpy.data.materials.remove(active_material)
	
		return {'FINISHED'}
	

def get_ffxiv_eye_multimap_file(active_object):

	folder_path = (__file__ + r"assets\ffxiv_iris").replace("shaders.py" , "")
	print (folder_path)

	if active_object:
		if active_object.type == 'MESH':
			model_race_id = active_object.data['ModelRaceID']
			original_material_name = active_object.data['original_material_name']
			iris_multimap_prefix = 'c'+str(model_race_id).zfill(4)
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
				#print("No matching file found.")
				return None


def get_ffxiv_eye_normalmap_file(active_object):

	folder_path = (__file__ + r"assets\ffxiv_iris").replace("shaders.py" , "")
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

	#MULTIMAP FILE
	image = None
	#check if this image exists, if it does, reuse it
	for img in bpy.data.images:
		if img.source == 'FILE' and img.filepath == multimap_file_path:
			image = img
			break

	# Open the image file
	if image is None:
		image = bpy.data.images.load(multimap_file_path)  # Load the image from the selected file path
	colorsetter_eye_multi_node.image = image 
	colorsetter_eye_multi_node.image.colorspace_settings.name = 'Non-Color'


	#NORMALMAP FILE
	image = None
	#check if this image exists, if it does, reuse it
	for img in bpy.data.images:
		if img.source == 'FILE' and img.filepath == normalmap_file_path:
			image = img
			break

	# Open the image file
	if image is None:
		image = bpy.data.images.load(normalmap_file_path)  # Load the image from the selected file path
	colorsetter_eye_normal_node.image = image 
	colorsetter_eye_normal_node.image.colorspace_settings.name = 'Non-Color'





@register_wrap
class ApplyColorsetterEyeShader(bpy.types.Operator):
	"""Apply Colorsetter Eye Shader"""
	bl_idname = "ffxiv_mmd.apply_colorsetter_eye_shader"
	bl_label = "Apply Colorsetter Eye Shader"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):

		active_material = bpy.context.active_object.active_material
		active_object = bpy.context.active_object

		#check if material is a colorsetter eyes node material
		if active_material.name.startswith('colorsetter_eye_'):
			raise Exception(f"Cannot add colorsetter material as this is already a colorsetter material")
			
		else:
			old_material = active_material
			old_material.name = "backup_" + active_material.name  # Rename the old material
			try:
				# Find the file path for WoL_Shader_V6.blend file
				file_path = (__file__ + r"assets\colorset_shaders\WoL_Shader_V6.blend").replace("shaders.py" , "")
								
				# Append the 'Eyes' material from WoL_Shader_V6.blend file
				with bpy.data.libraries.load(file_path, link=False) as (data_from, data_to):
					# Append the material called 'Face'
					data_to.materials = [mat for mat in data_from.materials if mat == 'Eyes']

				# Check if the material was successfully appended
				if 'Eyes' in bpy.data.materials:
					

					colorsetter_material = bpy.data.materials.get("Eyes")
					colorsetter_material.name = "colorsetter_eye_"+ active_material.name.lstrip("backup_")
					bpy.context.active_object.active_material = colorsetter_material
					
					#name the node group "colorsetter_eye_node_group"
					if colorsetter_material.node_tree.nodes['Group'].node_tree.name.startswith ('FFXIV Eye Shader'):
						colorsetter_material.node_tree.nodes['Group'].node_tree.name = 'colorsetter_eye_node_group'


					if colorsetter_material.node_tree.nodes['Group'].node_tree.name.startswith('colorsetter_eye_node_group'):
						colorsetter_material.node_tree.nodes['Group'].name = 'colorsetter_eye_node_instance'
						#print("Material 'Eyes' appended successfully.")
						set_colorsetter_eye_textures(active_object)
						#get_ffxiv_eye_multimap_file(active_object)
				else:
					print("Material 'Eyes' not found in the source file.")
				
			except:
				bpy.context.active_object.active_material = old_material
				old_material.name = old_material.name.lstrip('backup_')
				bpy.data.materials.remove(active_material)
				raise Exception(f"Failed to add Colorsetter eye shader")
			
		return {'FINISHED'}
	
@register_wrap
class RemoveColorsetterEyeShader(bpy.types.Operator):
	"""Remove Colorsetter Eye Shader"""
	bl_idname = "ffxiv_mmd.remove_colorsetter_eye_shader"
	bl_label = "Remove Colorsetter Eye Shader"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		
		active_material = bpy.context.active_object.active_material
		eye_shader_node_instance = None
		eye_shader_node_group = None
		if active_material.name.startswith('colorsetter_eye_'):
			for instance_node in active_material.node_tree.nodes:
				if instance_node.type =='GROUP' and instance_node.name.startswith('colorsetter_eye_node_instance'):
					eye_shader_node_instance = instance_node
					eye_shader_node_group = eye_shader_node_instance.node_tree
					break
			selected_material_name = active_material.name[len('colorsetter_eye_'):]
		backup_material = bpy.data.materials.get('backup_' + selected_material_name) 
		active_object = bpy.context.active_object

	
		#if active material, active object, and eye_shader_node_instance found
		if active_material.name.startswith('colorsetter_eye_') and backup_material and active_object and eye_shader_node_instance:
			for obj in bpy.data.objects:
				if obj.type =='MESH':
					#set the backup material as the active material, and restore it's original name
					if obj.active_material == active_material:
						obj.active_material = backup_material
			backup_material.name = backup_material.name.lstrip('backup_')
			#delete the active material
			bpy.data.materials.remove(active_material)
			#delete the shader node group
			if eye_shader_node_group:
				bpy.data.node_groups.remove(eye_shader_node_group)
		return {'FINISHED'}


@register_wrap
class ApplyBackgroundColorShader(bpy.types.Operator):
	"""Adds a Color Shader to the Background"""
	bl_idname = "ffxiv_mmd.apply_world_background_color"
	bl_label = "Adds a Color Shader to the Background"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		add_background_color_shaders()
		bpy.context.space_data.shading.type = 'RENDERED'


		return {'FINISHED'}
	
@register_wrap
class RemoveBackgroundColorShader(bpy.types.Operator):
	"""Removes Color Shader from the Background"""
	bl_idname = "ffxiv_mmd.remove_world_background_color"
	bl_label = "Removes Color Shader from the Background"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		remove_background_color_shaders()
		bpy.context.space_data.shading.type = 'RENDERED'


		return {'FINISHED'}

def add_background_color_shaders():

	world_material = bpy.context.scene.world

	light_path_node = world_material.node_tree.nodes.get('ffxiv_mmd_light_path')
	greenscreen_background_node = world_material.node_tree.nodes.get('ffxiv_mmd_background')
	mix_shader_node = world_material.node_tree.nodes.get('ffxiv_mmd_mix_shader')
	og_background_node = world_material.node_tree.nodes.get('Background')
	world_output = world_material.node_tree.nodes.get('World Output')

	if light_path_node is None:
		light_path_node = world_material.node_tree.nodes.new(type='ShaderNodeLightPath')
		light_path_node.name = 'ffxiv_mmd_light_path'

	# Create a new Background node and add it to the world shader
	if greenscreen_background_node is None:
		greenscreen_background_node = world_material.node_tree.nodes.new(type='ShaderNodeBackground')
		greenscreen_background_node.name = 'ffxiv_mmd_background'

	# Create a new Mix Shader node and add it to the world shader
	if mix_shader_node is None:
		mix_shader_node = world_material.node_tree.nodes.new(type='ShaderNodeMixShader')
		mix_shader_node.name = 'ffxiv_mmd_mix_shader'

	
	# Connect the output of the Light Path node to your shader setup
	world_material.node_tree.links.new(light_path_node.outputs['Is Camera Ray'], mix_shader_node.inputs[0])  
	world_material.node_tree.links.new(og_background_node.outputs[0], mix_shader_node.inputs[1])  
	world_material.node_tree.links.new(greenscreen_background_node.outputs[0], mix_shader_node.inputs[2])  

	world_material.node_tree.links.new(mix_shader_node.outputs[0], world_output.inputs[0])  

def remove_background_color_shaders():
	world_material = bpy.context.scene.world

	light_path_node = world_material.node_tree.nodes.get('ffxiv_mmd_light_path')
	greenscreen_background_node = world_material.node_tree.nodes.get('ffxiv_mmd_background')
	mix_shader_node = world_material.node_tree.nodes.get('ffxiv_mmd_mix_shader')
	og_background_node = world_material.node_tree.nodes.get('Background')
	world_output = world_material.node_tree.nodes.get('World Output')

	if light_path_node:
		world_material.node_tree.nodes.remove(light_path_node)

	# Create a new Background node and add it to the world shader
	if greenscreen_background_node:
		world_material.node_tree.nodes.remove(greenscreen_background_node)

	# Create a new Mix Shader node and add it to the world shader
	if mix_shader_node:
		world_material.node_tree.nodes.remove(mix_shader_node)

	world_material.node_tree.links.new(og_background_node.outputs[0], world_output.inputs[0]) 