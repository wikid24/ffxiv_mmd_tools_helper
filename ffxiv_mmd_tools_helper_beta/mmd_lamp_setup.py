import bpy

from . import register_wrap

@register_wrap
class MMDlightSetupPanel(bpy.types.Panel):
	"""One-click light Setup for mmd_tools"""
	bl_idname = "OBJECT_PT_mmd_light_setup"
	bl_label = "MMD light Setup"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="MMD light", icon="light" if bpy.app.version < (2,80,0) else "LIGHT")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.mmd_light_setup", text = "MMD light")
		row = layout.row()
		row = layout.row()

def light_setup(o):
	o.rotation_mode = 'XYZ'
	o.rotation_euler[0] = 0.785398 #45 degrees in radians
	o.rotation_euler[1] = 0
	o.rotation_euler[2] = 0.785398 #45 degrees in radians
	o.location = (30, -30, 30)
	o.scale = (2,2,2)

	o.data.type = 'SUN'
	o.data.color = (0.6, 0.6, 0.6)
	o.data.shadow_ray_samples = 4
	o.data.shadow_soft_size = 2.0
	o.data.shadow_color = (0.4, 0.4, 0.4)

def main(context):
	bpy.context.space_data.shading.type = 'RENDERED'
	#bpy.context.scene.tool_settings.material_mode = 'GLSL'
	#bpy.context.space_data.shading.type = 'TEXTURED'
	#bpy.context.scene.world.light_settings.use_environment_light = True

	#Set color management to None
	bpy.context.scene.display_settings.display_device = 'None'

	light_objects = [ob for ob in bpy.context.scene.objects if ob.type == 'LIGHT']

	print (len(light_objects))

	if len(light_objects) == 0:
		light_data = bpy.data.lights.new("sunlight", "SUN")
		light_object = bpy.data.objects.new("sunlight", light_data)
		bpy.context.scene.objects.link(light_object)
		bpy.context.scene.update()

	if bpy.context.active_object is not None:
		active_object = bpy.context.active_object
	else:
		active_object = bpy.context.scene.objects[-1]


	if bpy.context.active_object is not None:
		if bpy.context.active_object.type == 'light':
			o = bpy.context.active_object
			light_setup(o)
		else:
			light_objects = [ob for ob in bpy.context.scene.objects if ob.type == 'LIGHT']
			o = light_objects[0]
			bpy.context.view_layer.objects.active = o
			light_setup(o)


	bpy.context.view_layer.objects.active = active_object

				# bpy.context.scene.world.ambient_color = (0.6, 0.6, 0.6)

				# o.data.type = 'SPOT'
				# o.data.shadow_method = 'BUFFER_SHADOW'
				# o.data.distance = 45
				# o.data.spot_size = 1.309 #radians = 75 degress
				# o.data.use_auto_clip_start = True
				# o.data.use_auto_clip_end = True
				# o.data.shadow_color = (0, 0, 0)

@register_wrap
class MMDlightSetup(bpy.types.Operator):
	"""One-click light Setup for mmd_tools"""
	bl_idname = "ffxiv_mmd_tools_helper.mmd_light_setup"
	bl_label = "MMD light Setup"

	# @classmethod
	# def poll(cls, context):
		# return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}