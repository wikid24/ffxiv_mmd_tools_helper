import bpy
from . import register_wrap


	
@register_wrap
class ApplyEyeCatchlightShader(bpy.types.Operator):
	"""Adds the painted-on FFXIV catchlight to the eyes, same as in-game"""
	bl_idname = "ffxiv_mmd.apply_catchlight_shader"
	bl_label = "Adds the painted-on FFXIV catchlight to the eyes, same as in-game"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.active_object is not None and context.active_object.type == 'MESH'

	def execute(self, context):
		add_catchlight_node_group_to_material()
		return {'FINISHED'}
	
@register_wrap
class RemoveEyeCatchlightShader(bpy.types.Operator):
	"""Removes the painted-on FFXIV catchlight from the eyes"""
	bl_idname = "ffxiv_mmd.remove_catchlight_shader"
	bl_label = "Removes the painted-on FFXIV catchlight from the eyes"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.active_object is not None and context.active_object.type == 'MESH'

	def execute(self, context):
		remove_catchlight_node_group_from_material()
		return {'FINISHED'}



def create_eye_catchlight_node_group():

	node_group = None

	# Check if the node group doesn't exist and create it
	if bpy.data.node_groups.get('ffxiv_mmd_eye_catchlight'):
		node_group = bpy.data.node_groups.get('ffxiv_mmd_eye_catchlight')

	else:
		node_group = bpy.data.node_groups.new(type='ShaderNodeTree', name='ffxiv_mmd_eye_catchlight')

	if node_group:

		# Create the group input and output nodes as needed
		nodes = node_group.nodes
		links = node_group.links


		# Create nodes

		# Camera Data Node
		if 'catchlight_camera_data' not in node_group.nodes:
			camera_data_node = nodes.new(type='ShaderNodeCameraData')
			camera_data_node.name = 'catchlight_camera_data'
		else: 
			camera_data_node = node_group.nodes.get('catchlight_camera_data')

		node_location_cursor_x = camera_data_node.location[0]
		node_location_cursor_y = camera_data_node.location[1]
		node_location_cursor_x += 200

		# Vector Transform Node
		if 'catchlight_vector_transform' not in node_group.nodes:
			vector_transform_node = nodes.new(type='ShaderNodeVectorTransform')
			vector_transform_node.name = 'catchlight_vector_transform'
		else: 
			vector_transform_node = node_group.nodes.get('catchlight_vector_transform')

		vector_transform_node.vector_type = 'VECTOR'
		vector_transform_node.convert_from = 'CAMERA'
		vector_transform_node.convert_to = 'OBJECT'
		vector_transform_node.location = (node_location_cursor_x, node_location_cursor_y)
		node_location_cursor_x += 200

		# Map Range Node
		if 'catchlight_map_range' not in node_group.nodes:
			map_range_node = nodes.new(type='ShaderNodeMapRange')
			map_range_node.name = 'catchlight_map_range'
		else: 
			map_range_node = node_group.nodes.get('catchlight_map_range')	

		map_range_node.data_type = 'FLOAT_VECTOR'
		map_range_node.inputs[9].default_value[0] = 0
		map_range_node.inputs[9].default_value[1] = 0.9
		map_range_node.inputs[10].default_value[0] = 0.4
		map_range_node.inputs[10].default_value[1] = 0.9
		map_range_node.location = (node_location_cursor_x, node_location_cursor_y)
		node_location_cursor_x += 200

		# UV Map Node
		if 'catchlight_uv_map' not in node_group.nodes:
			uv_map_node = nodes.new(type='ShaderNodeUVMap')
			uv_map_node.name = 'catchlight_uv_map'
		else: 
			uv_map_node = node_group.nodes.get('catchlight_uv_map')	
		uv_map_node.uv_map = 'uv1'
		uv_map_node.location = (node_location_cursor_x, node_location_cursor_y)
		node_location_cursor_x += 200

		# Vector Math Node
		if 'catchlight_vector_math' not in node_group.nodes:
			vector_math_node = nodes.new(type='ShaderNodeVectorMath')
			vector_math_node.name = 'vector_math_node'
		else:
			vector_math_node = node_group.nodes.get('catchlight_vector_math')

		vector_math_node.operation = 'ADD'
		vector_math_node.location = (node_location_cursor_x, node_location_cursor_y)
		node_location_cursor_x += 200

	
		# Image Node
		file_path = (__file__ + r"assets\ffxiv_iris\catchlight_1.png").replace("shaders.py" , "")
		if 'catchlight_tex_image' not in node_group.nodes:
			image_node = nodes.new(type='ShaderNodeTexImage')
			image_node.name = 'catchlight_tex_image'
		else:
			image_node = node_group.nodes.get('catchlight_tex_image')

		image_node.image = bpy.data.images.load(file_path)
		image_node.location = (node_location_cursor_x, node_location_cursor_y)
		node_location_cursor_x += 300

		# Specular BSDF Node
		if 'catchlight_specular' not in node_group.nodes:
			specular_bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
			specular_bsdf_node.name = 'catchlight_specular'
		else:
			specular_bsdf_node = node_group.nodes.get('catchlight_specular')
		specular_bsdf_node.location = (node_location_cursor_x, node_location_cursor_y)
		node_location_cursor_x += 300

		# Output Node
		output_node = None
		if 'ffxiv_mmd_eye_catchlight_output' not in node_group.nodes:
			output_node = node_group.nodes.new(type='NodeGroupOutput')
			output_node.name = 'ffxiv_mmd_eye_catchlight_output'
			node_group.outputs.new("NodeSocketShader", "Shader")
			output_node.location = (node_location_cursor_x, node_location_cursor_y)
			node_location_cursor_x += 200
		else:
			output_node = node_group.nodes.get('ffxiv_mmd_eye_catchlight_output')

		# Connect nodes
		links.new(camera_data_node.outputs["View Vector"], vector_transform_node.inputs["Vector"])
		links.new(vector_transform_node.outputs["Vector"], map_range_node.inputs["Vector"])
		links.new(map_range_node.outputs["Vector"], vector_math_node.inputs[0])
		links.new(uv_map_node.outputs["UV"], vector_math_node.inputs[1])
		links.new(vector_math_node.outputs[0], image_node.inputs["Vector"])
		links.new(image_node.outputs["Color"], specular_bsdf_node.inputs["Base Color"])
		links.new(image_node.outputs["Color"], specular_bsdf_node.inputs["Specular"])
		# Connect BSDF to Material Output
		node_group.links.new(specular_bsdf_node.outputs[0], output_node.inputs[0])

		return node_group



def add_catchlight_node_group_to_material():
	active_object = bpy.context.active_object
	if active_object and active_object.active_material:
		active_material = active_object.active_material
		if active_material.node_tree:
			for node in active_material.node_tree.nodes:
				if node.name == 'Material Output':
					material_output_node = active_material.node_tree.nodes['Material Output']

	original_input_node = None

	if material_output_node:
		#get the original thing that it's connected to
		original_input_node = material_output_node.inputs[0].links[0].from_node

		if original_input_node.name == 'ffxiv_mmd_eye_catchlight_mix_shader':
			original_input_node = original_input_node.inputs[1].links[0].from_node

	
	if material_output_node and original_input_node:

		# Check if the node group doesn't exist and create it
		if bpy.data.node_groups.get('ffxiv_mmd_eye_catchlight'):
			node_group = bpy.data.node_groups.get('ffxiv_mmd_eye_catchlight')
		else:
			node_group = create_eye_catchlight_node_group()
		
		
		if node_group:
			
			# Add a Node Group instance and set its group name
			if active_material.node_tree.nodes.get('ffxiv_mmd_eye_catchlight_instance'):
				node_group_instance = active_material.node_tree.nodes.get('ffxiv_mmd_eye_catchlight_instance')
			else:
				node_group_instance = active_material.node_tree.nodes.new(type='ShaderNodeGroup')
				node_group_instance.node_tree = node_group
				
				node_group_instance.location = material_output_node.location
				node_group_instance.location[0] += 200
				node_group_instance.label = 'FFXIV Eye Catchlight'
				node_group_instance.name = 'ffxiv_mmd_eye_catchlight_instance'	
				

			#Create Mix Shader
			if active_material.node_tree.nodes.get('ffxiv_mmd_eye_catchlight_mix_shader'):
				mix_shader_node = active_material.node_tree.nodes.get('ffxiv_mmd_eye_catchlight_mix_shader')
			else:
				mix_shader_node = active_material.node_tree.nodes.new(type='ShaderNodeMixShader')
				mix_shader_node.name = 'ffxiv_mmd_eye_catchlight_mix_shader'
				mix_shader_node.location =  (node_group_instance.location[0]+200,node_group_instance.location[1])
				
				
			

			# Connect Original Input to Mix Shader
			active_material.node_tree.links.new(original_input_node.outputs[0], mix_shader_node.inputs[1])
			# Connect Catchlight Group Node  to Mix Shader
			active_material.node_tree.links.new(node_group_instance.outputs[0], mix_shader_node.inputs[2])
		
			# Connect Mix Shader to Material Output
			active_material.node_tree.links.new(mix_shader_node.outputs[0], material_output_node.inputs[0])

			material_output_node.location =  (mix_shader_node.location[0]+200,mix_shader_node.location[1])
		

def remove_catchlight_node_group_from_material():
	active_object = bpy.context.active_object
	if active_object and active_object.active_material:
		active_material = active_object.active_material
		if active_material.node_tree:
			for node in active_material.node_tree.nodes:
				if node.name == 'Material Output':
					material_output_node = node
				if node.name == 'ffxiv_mmd_eye_catchlight_instance':
					node_group_instance = node
				if node.name == 'ffxiv_mmd_eye_catchlight_mix_shader':
					mix_shader_node = node
				
	
	if material_output_node and node_group_instance and mix_shader_node:
		original_input_node = mix_shader_node.inputs[1].links[0].from_node

	if original_input_node:

		if mix_shader_node:
			active_material.node_tree.nodes.remove(mix_shader_node)
		if node_group_instance:
			material_output_node.location = node_group_instance.location
			active_material.node_tree.nodes.remove(node_group_instance)
		
		# Connect Mix Shader to Material Output
		active_material.node_tree.links.new(original_input_node.outputs[0], material_output_node.inputs[0])




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
		#add_catchlight_node_group_to_material()
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