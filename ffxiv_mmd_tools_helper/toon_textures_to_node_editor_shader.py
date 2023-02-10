import bpy

from . import register_wrap
from . import model


# Each image is a list of numbers(floats): R,G,B,A,R,G,B,A etc.
# So the length of the list of pixels is 4 X number of pixels
# pixels are in left-to-right rows from bottom left to top right of image


def toon_image_to_color_ramp(toon_texture_color_ramp, toon_image):
	pixels_width = toon_image.size[0]
	pixels_height = toon_image.size[1]
	toon_image_pixels = []
	toon_image_gradient = []

	for f in range(0, len(toon_image.pixels), 4):
		pixel_rgba = toon_image.pixels[f:f+4]
		toon_image_pixels.append(pixel_rgba)

	for p in range(0, len(toon_image_pixels), int(len(toon_image_pixels)/32)):
		toon_image_gradient.append(toon_image_pixels[p])

	toon_texture_color_ramp.color_ramp.elements[0].color = toon_image_gradient[0]
	toon_texture_color_ramp.color_ramp.elements[-1].color = toon_image_gradient[-1]

	for i in range(1, len(toon_image_gradient)-2, 1):
		toon_texture_color_ramp.color_ramp.elements.new(i/(len(toon_image_gradient)-1))
		toon_texture_color_ramp.color_ramp.elements[i].color = toon_image_gradient[i]
		if i > len(toon_image_gradient)/2:
			toon_texture_color_ramp.color_ramp.elements[i].color[3] = 0.0 #alpha of non-shadow colors set to 0.0

	return


def clear_material_nodes(context):
	for m in bpy.context.active_object.data.materials:
		if m.node_tree is not None:
			for n in range(len(m.node_tree.nodes)-1, 1, -1):
				m.node_tree.nodes.remove(m.node_tree.nodes[n])


def main_OLD(context):
	o = bpy.context.active_object
	if o.type == 'MESH':

		if len(bpy.data.lights) == 0:
			bpy.data.lights.new("Lamp", "SUN")

		for object in bpy.context.scene.objects:
			if object.data == bpy.data.lights[0]:
				LAMP = object

		if o.data.materials is not None:
			for m in o.data.materials:
				m.use_nodes = True
				# m.node_tree.nodes.new('OUTPUT')
				# m.node_tree.nodes.new('MATERIAL')
				output_node = m.node_tree.nodes[0]
				output_node.location = (1450, 800)
				material_node = m.node_tree.nodes[1]
				material_node = m.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
				material_node.material = m
				material_node.location = (-800, 800)

				lamp_node = m.node_tree.nodes.new('ShaderNodeLampData')
				lamp_node.lamp_object = LAMP
				lamp_node.location = (-530, -50)

				rgb_to_bw = m.node_tree.nodes.new('ShaderNodeRGBToBW')
				rgb_to_bw.location = (-90, -50) #(120, 470) (-530, -50)

				vector_math_node = m.node_tree.nodes.new('ShaderNodeVectorMath')
				vector_math_node.operation = 'DOT_PRODUCT'
				vector_math_node.location = (-520, 470)

				math_node_1 = m.node_tree.nodes.new('ShaderNodeMath')
				math_node_1.operation = 'ADD'
				math_node_1.inputs[1].default_value = 1.0
				math_node_1.location = (-325, 470)

				math_node_2 = m.node_tree.nodes.new('ShaderNodeMath')
				math_node_2.operation = 'MULTIPLY'
				math_node_2.inputs[1].default_value = 0.5 #1.0
				# math_node_2.use_clamp = True
				math_node_2.location = (-90, 470)

				math_node_3 = m.node_tree.nodes.new('ShaderNodeMath')
				math_node_3.operation = 'MULTIPLY'
				math_node_3.location = (120, 470)

				toon_texture_color_ramp = m.node_tree.nodes.new('ShaderNodeValToRGB')
				toon_texture_color_ramp.location = (340, 470)

				mix_rgb_node_ramp_overlay = m.node_tree.nodes.new('ShaderNodeMixRGB')
				mix_rgb_node_ramp_overlay.blend_type = 'MULTIPLY' #was 'OVERLAY'
				mix_rgb_node_ramp_overlay.inputs[0].default_value = 1.0
				mix_rgb_node_ramp_overlay.inputs['Color2'].default_value = (1.0, 1.0, 1.0, 1.0)
				mix_rgb_node_ramp_overlay.location = (690, 470)
				mix_rgb_node_ramp_overlay.label = "toon_modifier"

				mix_rgb_node = m.node_tree.nodes.new('ShaderNodeMixRGB')
				mix_rgb_node.blend_type = 'MULTIPLY'
				mix_rgb_node.inputs[0].default_value = 1.0
				# mix_rgb_node.use_clamp = True
				mix_rgb_node.location = (1000, 470)
				mix_rgb_node.inputs['Color2'].default_value = (m.diffuse_color[0], m.diffuse_color[1], m.diffuse_color[2], 1.0)

				mix_rgb_node_add_sphere = m.node_tree.nodes.new('ShaderNodeMixRGB')
				mix_rgb_node_add_sphere.blend_type = 'ADD'
				mix_rgb_node_add_sphere.inputs[0].default_value = 1.0
				mix_rgb_node_add_sphere.location = (1240, 470)

				diffuse_texture_geomety_uv_node = m.node_tree.nodes.new('ShaderNodeGeometry')
				diffuse_texture_geomety_uv_node.location = (620, 250)

				diffuse_texture_node = m.node_tree.nodes.new('ShaderNodeTexture')
				diffuse_texture_node.location = (820, 250)

				sphere_texture_geometry_normal_node = m.node_tree.nodes.new('ShaderNodeGeometry')
				sphere_texture_geometry_normal_node.location = (620, -50)

				sphere_texture_node = m.node_tree.nodes.new('ShaderNodeTexture')
				sphere_texture_node.location = (820, -50)


				print(len(m.node_tree.links))
				m.node_tree.links.new(output_node.inputs['Alpha'], material_node.outputs['Alpha'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(vector_math_node.inputs[0], material_node.outputs['Normal']) #vector_math_node.inputs['Vector']
				print(len(m.node_tree.links))
				m.node_tree.links.new(vector_math_node.inputs[1], lamp_node.outputs['Light Vector']) #vector_math_node.inputs['Vector']
				print(len(m.node_tree.links))
				m.node_tree.links.new(rgb_to_bw.inputs['Color'], lamp_node.outputs['Shadow']) #math_node_3.inputs['Value']
				print(len(m.node_tree.links))
				m.node_tree.links.new(math_node_3.inputs[1], rgb_to_bw.outputs['Val'])

				print(len(m.node_tree.links))
				m.node_tree.links.new(math_node_1.inputs[0], vector_math_node.outputs['Value']) #math_node_1.inputs['Value']
				print(len(m.node_tree.links))
				m.node_tree.links.new(math_node_2.inputs['Value'], math_node_1.outputs['Value'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(math_node_3.inputs[0], math_node_2.outputs['Value']) #math_node_3.inputs['Value']
				print(len(m.node_tree.links))
				m.node_tree.links.new(toon_texture_color_ramp.inputs['Fac'], math_node_3.outputs['Value'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(mix_rgb_node_ramp_overlay.inputs['Color1'], toon_texture_color_ramp.outputs['Color'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(mix_rgb_node_ramp_overlay.inputs['Fac'], toon_texture_color_ramp.outputs['Alpha'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(mix_rgb_node.inputs['Color1'], mix_rgb_node_ramp_overlay.outputs['Color'])

				print(len(m.node_tree.links))
				m.node_tree.links.new(mix_rgb_node_add_sphere.inputs['Color1'], mix_rgb_node.outputs['Color'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(output_node.inputs['Color'], mix_rgb_node_add_sphere.outputs['Color'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(diffuse_texture_node.inputs['Vector'], diffuse_texture_geomety_uv_node.outputs['UV'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(mix_rgb_node.inputs['Color2'], diffuse_texture_node.outputs['Color'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(sphere_texture_node.inputs['Vector'], sphere_texture_geometry_normal_node.outputs['Normal'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(mix_rgb_node_add_sphere.inputs['Color2'],sphere_texture_node.outputs['Color'])

				if m.texture_slots is not None:
					for t in range(len(m.texture_slots)):
						if m.texture_slots[t] is not None:
							texture_name = m.texture_slots[t].texture.name
							if t == 0:
								diffuse_texture_node.texture = bpy.data.textures[texture_name]
								diffuse_exists = True
								# bpy.data.textures[texture_name]["mmd_texture_type"] = "DIFFUSE"
							if t == 1:
								if m.texture_slots[t].texture.type == 'IMAGE':
									if m.texture_slots[t].texture.image is not None:
										#toon_image_bottom_half_to_color_ramp(toon_texture_color_ramp, m.texture_slots[t].texture.image)
										toon_image_to_color_ramp(toon_texture_color_ramp, m.texture_slots[t].texture.image)
									# bpy.data.textures[texture_name]["mmd_texture_type"] = "TOON"
									# bpy.context.active_object.data.materials[0].texture_slots[1].texture.image.name
							if t == 2:
								mix_rgb_node_add_sphere.blend_type = m.texture_slots[t].blend_type
								sphere_texture_node.texture = bpy.data.textures[texture_name]
								sphere_exists = True
								# bpy.data.textures[texture_name]["mmd_texture_type"] = "SPHERE"

				if diffuse_texture_node.texture == None:
					# m.node_tree.links.new(mix_rgb_node.inputs['Color2'], material_node.outputs['Color'])
					# m.use_shadeless = True
					m.node_tree.links.remove(mix_rgb_node.inputs['Color2'].links[0])
					print("This mesh object has no diffuse texture.")



def main (context):
	o = bpy.context.active_object
	if o.type == 'MESH':

		if len(bpy.data.lights) == 0:
			bpy.data.lights.new("Lamp", "SUN")

		for object in bpy.context.scene.objects:
			if object.data == bpy.data.lights[0]:
				LAMP = object

		#toonify_material(o)

	# Iterate over the selected objects
	for obj in bpy.context.selected_objects:
		# Check if the object is a mesh object
		if obj.type == 'MESH':
			# Iterate over the object's material slots
			for slot in obj.material_slots:
				mat = slot.material
				#bpy.context.object.active_material = mat
				toonify_material(mat)
				print(f"The material in slot {slot.name} of object {obj.name} is {mat.name}")
		#else:
			#print(f'{obj.name} is not a mesh object')

	



def toonify_material(mat):

	# Get the active material
	#mat = bpy.context.object.active_material

	# Find the principled BSDF node
	principled = None
	for node in mat.node_tree.nodes:
		if node.type == 'BSDF_PRINCIPLED':
			principled = node
			break

	if principled is None:
		print("Principled BSDF node not found.")
		principled = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
		principled.location = (0,0)
	else:
		# Create 'shader to RGB' node if it doesnt exist
		shader_to_rgb = None
		for node in mat.node_tree.nodes:
			if node.name == 'MMDH_shader_to_rgb':
				shader_to_rgb = node
				break
		if shader_to_rgb == None:      
			shader_to_rgb = mat.node_tree.nodes.new(type='ShaderNodeShaderToRGB')
			shader_to_rgb.name = 'MMDH_shader_to_rgb'
			shader_to_rgb.label = shader_to_rgb.name
			shader_to_rgb.location.x = principled.location.x + 300
			shader_to_rgb.location.y = principled.location.y
			
		# Create 'color ramp' node if it doesn't exist
		color_ramp = None
		for node in mat.node_tree.nodes:
			if node.name == 'MMDH_color_ramp':
				color_ramp = node
				break
		if color_ramp == None:    
			color_ramp = mat.node_tree.nodes.new(type='ShaderNodeValToRGB')
			color_ramp.name = 'MMDH_color_ramp'
			color_ramp.label = color_ramp.name
			color_ramp.location.x = shader_to_rgb.location.x + 300
			color_ramp.location.y = shader_to_rgb.location.y
		
		# Create mix_rgb node if it doesn't exist
		mix_rgb = None
		for node in mat.node_tree.nodes:
			if node.name == 'MMDH_mix_rgb':
				mix_rgb = node
				break
		if mix_rgb == None:      
			mix_rgb = mat.node_tree.nodes.new(type='ShaderNodeMixRGB')
			mix_rgb.name = 'MMDH_mix_rgb'
			mix_rgb.label = mix_rgb.name
			mix_rgb.location.x = color_ramp.location.x + 300
			mix_rgb.location.y = color_ramp.location.y
		
		# Create hue & saturation node if it doesn't exist
		hue_sat = None
		for node in mat.node_tree.nodes:
			if node.name == 'MMDH_hue_sat':
				hue_sat = node
				break
		if hue_sat == None:
			hue_sat = mat.node_tree.nodes.new(type='ShaderNodeHueSaturation')
			hue_sat.name = 'MMDH_hue_sat'
			hue_sat.label = hue_sat.name
			hue_sat.location.x = mix_rgb.location.x + 300
			hue_sat.location.y = mix_rgb.location.y

		# Create the transparent BSDF node if it doesn't exist
		transparent_bsdf = None
		for node in mat.node_tree.nodes:
			if node.name == 'MMDH_transparent_bsdf':
				transparent_bsdf = node
				break
		if transparent_bsdf == None:
			transparent_bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfTransparent')
			transparent_bsdf.name = 'MMDH_transparent_bsdf'
			transparent_bsdf.label = transparent_bsdf.name
			transparent_bsdf.location.x = hue_sat.location.x
			transparent_bsdf.location.y = hue_sat.location.y + 300

		# Create the mix shader node if it doesnt exist
		mix_shader = None
		for node in mat.node_tree.nodes:
			if node.name == 'MMDH_mix_shader':
				mix_shader = node
				break
		if mix_shader == None:
			mix_shader = mat.node_tree.nodes.new(type='ShaderNodeMixShader')
			mix_shader.name = 'MMDH_mix_shader'
			mix_shader.label = mix_shader.name
			mix_shader.location.x = transparent_bsdf.location.x + 300
			mix_shader.location.y = transparent_bsdf.location.y
		
		# Find the material output node
		material_output = None
		for node in mat.node_tree.nodes:
			if node.type == 'OUTPUT_MATERIAL':
				material_output = node
				material_output.location.x = hue_sat.location.x + 300
				material_output.location.y = hue_sat.location.y
				break

		if material_output is None:
			print("Material Output node not found.")
		else:
			# Connect the principled BSDF node to the shader to RGB node
			mat.node_tree.links.new(principled.outputs[0], shader_to_rgb.inputs[0])

			# Connect the shader to RGB node to the color ramp node
			mat.node_tree.links.new(shader_to_rgb.outputs[0], color_ramp.inputs[0])
			
			# Connect the color ramp node to the mix node
			mat.node_tree.links.new(color_ramp.outputs[0], mix_rgb.inputs[1])

			# Connect the mix node to the hue&saturation output node
			mat.node_tree.links.new(mix_rgb.outputs[0], hue_sat.inputs[4])
			
			# Connect shader_to_rgb alpha channel to mix_shader node
			mat.node_tree.links.new(shader_to_rgb.outputs[1], mix_shader.inputs[0])
			
			# Connect transparent_BSDF  to mix_shader node
			mat.node_tree.links.new(transparent_bsdf.outputs[0], mix_shader.inputs[1])    
			
			#Connect the hue saturation node to the mix_shader node
			mat.node_tree.links.new(hue_sat.outputs[0], mix_shader.inputs[2])
			
			
			#Connect mix_shader to material_outputs node
			mat.node_tree.links.new(mix_shader.outputs[0], material_output.inputs[0])
			
		
		# check for a base color input on the principled BSDF node
			
			
		if 'Base Color' in principled.inputs:
		
			# Get the node connected to the base color input
			base_color_input = None
			for link in mat.node_tree.links:
				if link.to_node == principled and link.to_socket == principled.inputs[0]:
					base_color_input = link.from_node
					break
				
			if base_color_input is not None:
			
				base_color_input.location.x = shader_to_rgb.location.x
				base_color_input.location.y = shader_to_rgb.location.y - 300
				
				
				# create toon modifier node if it doesn't exist
				toon_modifier = None
				for node in mat.node_tree.nodes:
					if node.name == 'MMDH_toon_modifier':
						toon_modifier = node
						break
				if toon_modifier == None:
					toon_modifier = mat.node_tree.nodes.new(type='ShaderNodeMath')
					toon_modifier.name = 'MMDH_toon_modifier'
					toon_modifier.label = toon_modifier.name
					toon_modifier.operation = 'MULTIPLY'
					toon_modifier.location.y = mix_rgb.location.y - 300
					toon_modifier.location.x = mix_rgb.location.x
				
				#connect base color input to mix_rgb input 1
				mat.node_tree.links.new(base_color_input.outputs[0], mix_rgb.inputs[1])
				# connect base color input to toon_modifier
				mat.node_tree.links.new(base_color_input.outputs[0], toon_modifier.inputs[0])
				# connect toon_modifier to mix_rgb node input 2
				mat.node_tree.links.new(toon_modifier.outputs[0], mix_rgb.inputs[2])

				# Find the material output node
				material_output = None
				for node in mat.node_tree.nodes:
					if node.type == 'OUTPUT_MATERIAL':
						material_output = node
						break

				if material_output is None:
					print("Material Output node not found.")
				else:
					# Connect the shader to RGB node to the color ramp node
					mat.node_tree.links.new(shader_to_rgb.outputs[0], color_ramp.inputs[0])
					
					# Connect the color ramp node to the mix_rgb node
					mat.node_tree.links.new(color_ramp.outputs[0], mix_rgb.inputs[0])

				# Connect the mix node to the hue_sat input node
					#mat.node_tree.links.new(mix.outputs[0], hue_sat.inputs[0])
					
			else:
				print("No node connected to the base color input of the principled BSDF node")

@register_wrap
class MMDToonTexturesToNodeEditorShader(bpy.types.Operator):
	"""Sets up nodes in Blender node editor for rendering toon textures"""
	bl_idname = "ffxiv_mmd_tools_helper.mmd_toon_render_node_editor"
	bl_label = "MMD toon textures render using node editor "
	bl_options = {'REGISTER', 'UNDO'}

	# @classmethod
	# def poll(cls, context):
		# return context.active_object is not None

	def execute(self, context):

		"""
		mesh_objects_list = model.find_MMD_MeshesList(bpy.context.active_object)
		assert(mesh_objects_list is not None), "The active object is not an MMD model."
		for o in mesh_objects_list:
			bpy.context.view_layer.objects.active = o
			clear_material_nodes(context)
			# create_default_material_nodes(context)
			main(context)
		"""			
		main(context)

		return {'FINISHED'}