import bpy
import os
from . import register_wrap

from os.path import isfile


def add_decal_node_group_to_material(active_material,decal_slot_id):

	material_output_node = None
	original_input_node = None
	node_group = None

	# Ensure the material output node exists
	for node in active_material.node_tree.nodes:
		if node.type == 'OUTPUT_MATERIAL':
			material_output_node = node
			break
				
	# Ensure the original input node exists
	if material_output_node:
		original_input_node = material_output_node.inputs[0].links[0].from_node

		if original_input_node.name == 'ffxiv_mmd_decal_'+str(decal_slot_id):
			original_input_node = original_input_node.inputs[1].links[0].from_node
		
		
	if material_output_node and original_input_node:


		# Check if the node group doesn't exist and create it
		if bpy.data.node_groups.get('ffxiv_mmd_decal_'+str(decal_slot_id)):
			node_group = bpy.data.node_groups.get('ffxiv_mmd_decal_'+str(decal_slot_id))
		else:
			node_group = create_decal_node_group(active_material,decal_slot_id)


		node_location_cursor_x = material_output_node.location[0]
		node_location_cursor_y = material_output_node.location[1]
		node_location_cursor_x += 200

		if node_group:
			
			# Add a Node Group instance and set its group name
			node_group_instance = active_material.node_tree.nodes.new(type='ShaderNodeGroup')
			node_group_instance.node_tree = node_group
			node_group_instance.location = material_output_node.location
			node_group_instance.label = 'FFXIV Decal '+ str(decal_slot_id)
			node_group_instance.name = 'ffxiv_mmd_decal_'+ str(decal_slot_id)
			material_output_node.location = (node_location_cursor_x,node_location_cursor_y)

			# Connect Original Input to Node Group
			active_material.node_tree.links.new(original_input_node.outputs[0], node_group_instance.inputs[0])
	
		
			# Connect Node Group to Material Output
			active_material.node_tree.links.new(node_group_instance.outputs[0], material_output_node.inputs[0])

def create_decal_node_group(active_material,decal_slot_id):

	node_group = None

	# Check if the node group doesn't exist and create it
	if bpy.data.node_groups.get('ffxiv_mmd_decal_'+str(decal_slot_id)):
		node_group = bpy.data.node_groups.get('ffxiv_mmd_decal_'+str(decal_slot_id))

	else:
		node_group = bpy.data.node_groups.new(type='ShaderNodeTree', name='ffxiv_mmd_decal_'+str(decal_slot_id))

	# Create the group input and output nodes as needed
	input_node = None
	if 'ffxiv_mmd_decal_input_'+str(decal_slot_id) not in node_group.nodes:
	
		input_node = node_group.nodes.new(type='NodeGroupInput')
		input_node.name = 'ffxiv_mmd_decal_input_'+str(decal_slot_id)
		node_group.inputs.new("NodeSocketShader", "Shader")
		node_group.inputs.new("NodeSocketColor", "Base Color")
		node_group.inputs["Base Color"].default_value = (1.0, 1.0, 1.0, 1.0)  # (R, G, B, A)
		#node_group.inputs.new("NodeSocketFloatFactor", "Subsurface")
		#node_group.inputs['Subsurface'].min_value = 0
		#node_group.inputs['Subsurface'].max_value = 1
		#node_group.inputs['Subsurface'].default_value = 0
		#node_group.inputs.new("NodeSocketColor", "Subsurface Color")
		#node_group.inputs["Subsurface Color"].default_value = (0, 0, 0, 1.0)  # (R, G, B, A)
		node_group.inputs.new("NodeSocketFloatFactor", "Specular")
		node_group.inputs['Specular'].min_value = 0
		node_group.inputs['Specular'].max_value = 1
		node_group.inputs['Specular'].default_value = 0
		node_group.inputs.new("NodeSocketFloatFactor", "Roughness")
		node_group.inputs['Roughness'].min_value = 0
		node_group.inputs['Roughness'].max_value = 1
		node_group.inputs['Roughness'].default_value = 0
		node_group.inputs.new("NodeSocketFloatFactor", "Alpha")
		node_group.inputs['Alpha'].min_value = 0
		node_group.inputs['Alpha'].max_value = 1
		node_group.inputs['Alpha'].default_value = 1
	else:
		input_node = node_group.nodes.get('ffxiv_mmd_decal_input_'+str(decal_slot_id))

	output_node = None
	if 'ffxiv_mmd_decal_output_'+str(decal_slot_id) not in node_group.nodes:
		output_node = node_group.nodes.new(type='NodeGroupOutput')
		output_node.name = 'ffxiv_mmd_decal_output_'+str(decal_slot_id)
		node_group.outputs.new("NodeSocketShader", "Shader")
		output_node.location = (input_node.location[0]+200,input_node.location[1] )
	else:
		output_node = node_group.nodes.get('ffxiv_mmd_decal_output_'+str(decal_slot_id))

	node_location_cursor_x = output_node.location[0]
	node_location_cursor_y = output_node.location[1]
	node_location_cursor_x += 100

	"""
		# Create a new node group called 'ffxiv_mmd_decal_x' on the active material
	node_group_instance = active_material.node_tree.nodes.new(type='ShaderNodeGroup')
	node_group_instance.location = (0, 300)
	node_group_instance.node_tree = bpy.data.node_groups.get('ffxiv_mmd_decal_'+str(decal_slot_id))
	#decal_group = active_material.node_tree.layouts.new(name="ffxiv_mmd_decal_"+str(decal_slot_id))

	"""

	# Create UV Map Node
	if 'ffxiv_mmd_decal_uv_'+str(decal_slot_id) not in node_group.nodes:
		uv_node = node_group.nodes.new(type='ShaderNodeUVMap')
		uv_node.name='ffxiv_mmd_decal_uv_'+str(decal_slot_id)
		uv_node.location = (node_location_cursor_x, node_location_cursor_y +200)
		node_location_cursor_x += 200
		
		
		output_node.location = (node_location_cursor_x, node_location_cursor_y)
	else: 
		uv_node = node_group.nodes.get('ffxiv_mmd_decal_uv_'+str(decal_slot_id))
	# Set the UV property to 'uv2'
	uv_node.uv_map = 'uv2'

	# Create Decal Image Node
	if 'ffxiv_mmd_decal_img_'+str(decal_slot_id) not in node_group.nodes:
		image_node = node_group.nodes.new(type='ShaderNodeTexImage')
		image_node.name = 'ffxiv_mmd_decal_img_'+str(decal_slot_id)
		image_node.location = (node_location_cursor_x, node_location_cursor_y +200)
		node_location_cursor_x += 300
		output_node.location = (node_location_cursor_x, node_location_cursor_y)
		#image_node.image.colorspace_settings.name = 'Non-Color'
	else: 
		image_node = node_group.nodes.get('ffxiv_mmd_decal_img_'+str(decal_slot_id))

	# Connect UV Node to Decal Image Node
	node_group.links.new(uv_node.outputs[0], image_node.inputs[0])

	# Create Decal Alpha Mix Node
	if 'ffxiv_mmd_decal_alpha_'+str(decal_slot_id) not in node_group.nodes:
		alpha_node = node_group.nodes.new(type='ShaderNodeMix')
		alpha_node.name = 'ffxiv_mmd_decal_alpha_'+str(decal_slot_id)
		alpha_node.location = (node_location_cursor_x, node_location_cursor_y +200)
		node_location_cursor_x += 300
		output_node.location = (node_location_cursor_x, node_location_cursor_y)
		#image_node.image.colorspace_settings.name = 'Non-Color'
	else: 
		image_node = node_group.nodes.get('ffxiv_mmd_decal_img_'+str(decal_slot_id))

	# Connect Image Node to Alpha Mix Node
	node_group.links.new(image_node.outputs[0], alpha_node.inputs[3])


	# Create Principled BSDF Node
	if 'ffxiv_mmd_decal_bsdf_'+str(decal_slot_id) not in node_group.nodes:
		bsdf_node = node_group.nodes.new(type='ShaderNodeBsdfPrincipled')
		bsdf_node.name = 'ffxiv_mmd_decal_bsdf_'+str(decal_slot_id)
		bsdf_node.location = image_node.location
		bsdf_node.location = (bsdf_node.location[0],image_node.location[1]-300)
		#node_location_cursor_x += 300
		
	else: 
		bsdf_node = node_group.nodes.get('ffxiv_mmd_decal_bsdf_'+str(decal_slot_id))
	
	#link all nodes to Group Input node
	node_group.links.new(input_node.outputs["Base Color"], bsdf_node.inputs["Base Color"])
	#node_group.links.new(input_node.outputs["Subsurface"], bsdf_node.inputs["Subsurface"])
	#node_group.links.new(input_node.outputs["Subsurface Color"], bsdf_node.inputs["Subsurface Color"])
	node_group.links.new(input_node.outputs["Specular"], bsdf_node.inputs["Specular"])
	node_group.links.new(input_node.outputs["Roughness"], bsdf_node.inputs["Roughness"])
	node_group.links.new(input_node.outputs["Alpha"], alpha_node.inputs["Factor"])


	# Create Mix Shader Node
	if 'ffxiv_mmd_decal_mix_'+str(decal_slot_id) not in node_group.nodes:
		mix_node = node_group.nodes.new(type='ShaderNodeMixShader')
		mix_node.name = 'ffxiv_mmd_decal_mix_'+str(decal_slot_id)
		mix_node.location = (node_location_cursor_x, node_location_cursor_y)
		node_location_cursor_x += 300
		output_node.location = (node_location_cursor_x, node_location_cursor_y)
	else:
		mix_node = node_group.nodes.get('ffxiv_mmd_decal_mix_'+str(decal_slot_id))

	# Connect Alpha to Mix Shader Fac
	node_group.links.new(alpha_node.outputs[0], mix_node.inputs[0])

	# Connect Original Input to Mix Shader Shader 1
	node_group.links.new(input_node.outputs["Shader"], mix_node.inputs[1])

	# Connect Principled BSDF to Mix Shader Shader 2
	node_group.links.new(bsdf_node.outputs[0], mix_node.inputs[2])
	
	# Connect Mix Shader to Material Output
	node_group.links.new(mix_node.outputs[0], output_node.inputs[0])

	
	return node_group

	

	
				
def remove_decal_node_group_from_material(active_material,decal_slot_id):

	original_input_node = None
	original_output_node = None
	node_group_instance = None
	

	if active_material.node_tree:
		if active_material.node_tree.nodes.get('ffxiv_mmd_decal_'+str(decal_slot_id)):
			node_group_instance = active_material.node_tree.nodes.get('ffxiv_mmd_decal_'+str(decal_slot_id))


		if node_group_instance:
			original_input_node = node_group_instance.inputs['Shader'].links[0].from_node 
			original_output_node = node_group_instance.outputs[0].links[0].to_node

		if 	original_input_node and original_output_node:
			#connect mix shader input to material_output's output
			active_material.node_tree.links.new(original_input_node.outputs[0],  original_output_node.inputs[0]) 

			active_material.node_tree.nodes.remove(node_group_instance)

			original_output_node.location = (original_output_node.location[0]-200, original_output_node.location[1])



def insert_image_to_decal_nodegroup(context, filepath, decal_slot_id):

	active_material = None

	if context.active_object:
		if context.active_object.active_material:
			active_material = context.active_object.active_material

	if active_material:
		node_group = None
		image_node = None
		if bpy.data.node_groups.get('ffxiv_mmd_decal_'+str(decal_slot_id)):
			node_group = bpy.data.node_groups.get('ffxiv_mmd_decal_'+str(decal_slot_id))
		if node_group:
			image_node = node_group.nodes.get('ffxiv_mmd_decal_img_'+str(decal_slot_id))
		if image_node:
			image = None
			#check if this image exists, if it does, reuse it
			for img in bpy.data.images:
				if img.source == 'FILE' and img.filepath == filepath:
					image = img
					break

			# Open the image file
			if image is None:
				image = bpy.data.images.load(filepath)  # Load the image from the selected file path
			image_node.image = image 
			image_node.image.colorspace_settings.name = 'Non-Color'
			


@register_wrap
class CreateDecalNodeGroup(bpy.types.Operator):
	"""Adds a decal node group to the selected mesh's active material"""
	bl_idname = "ffxiv_mmd.create_decal_layout"
	bl_label = "Adds a decal to the selected mesh's active material"
	bl_options = {'REGISTER', 'UNDO'}

	decal_slot_id = bpy.props.IntProperty(name="decal_slot_id")

	def execute(self, context):

		active_material = None

		if context.active_object:
			if context.active_object.active_material:
				active_material = context.active_object.active_material

		if active_material:
			add_decal_node_group_to_material(active_material,self.decal_slot_id)


		return {'FINISHED'}
	


from bpy_extras.io_utils import ImportHelper
@register_wrap
class InsertImageDecal(bpy.types.Operator, ImportHelper):

	bl_idname = "ffxiv_mmd.insert_image_decal"
	bl_label = "Adds a decal to the selected mesh's active material"
	bl_options = {'REGISTER', 'UNDO'}

	filename_ext = ".png"
	filter_glob: bpy.props.StringProperty(
		default="*.png",
		options={'HIDDEN'},
	)

	decal_slot_id = bpy.props.IntProperty(name="decal_slot_id")
	

	@classmethod
	def poll(cls, context):
		if context.active_object:
			return context.active_object.type == 'MESH'

	def execute(self, context):
		filepath = self.filepath
		insert_image_to_decal_nodegroup(context,filepath,self.decal_slot_id)
		return {'FINISHED'}
	
	def invoke(self, context, event):
		# Set the default folder for the file browser to the addon's decal folder
		file_path = (__file__ + r"assets\ffxiv_face_paint").replace("facepaint.py" , "")
		file_path = bpy.path.abspath(file_path + '\\')
		self.filepath = file_path
		context.window_manager.fileselect_add(self)
		#print(f"filepath: {self.filepath}")
		return {'RUNNING_MODAL'}

	
@register_wrap
class RemoveDecalNodeGroup(bpy.types.Operator):
	"""Removes a decal to the selected mesh's active material"""
	bl_idname = "ffxiv_mmd.remove_decal_layout"
	bl_label = "Removes a decal to the selected mesh's active material"
	bl_options = {'REGISTER', 'UNDO'}

	decal_slot_id = bpy.props.IntProperty(name="decal_slot_id")

	def execute(self, context):

		active_material = None

		if context.active_object:
			if context.active_object.active_material:
				active_material = context.active_object.active_material

		if active_material:
			remove_decal_node_group_from_material(active_material,self.decal_slot_id)


		return {'FINISHED'}
