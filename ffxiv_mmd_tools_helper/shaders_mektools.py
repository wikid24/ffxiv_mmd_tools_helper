import bpy
import os
from . import register_wrap
	



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

import addon_utils
try:
	import mek_tools
except ImportError:
	raise Exception(f"The addon 'mek_tools' is not installed or is not enabled. Please install and enable it.")


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
		addon_module = None
		try:
			addon_module = [m for m in addon_utils.modules() if m.__name__ == addon_name][0] # get module
		except:
			raise Exception(f"The addon 'mek_tools' is not installed or is not enabled. Please install and enable it.")

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
		addon_module = None
		try:
			addon_module = [m for m in addon_utils.modules() if m.__name__ == addon_name][0] # get module
		except:
			raise Exception(f"The addon 'mek_tools' is not installed or is not enabled. Please install and enable it.")

		if addon_module:
			installed_version = addon_module.bl_info.get('version',(-1,-1,-1))
			installed_version = float(str(installed_version[0])+'.'+str(installed_vresion[1])+str(installed_version[2]))

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
	
