import bpy
from .. import register_wrap

@register_wrap
class CameraLightingPanel_MTH(bpy.types.Panel):
	#Creates the Bones Renamer Panel in a VIEW_3D TOOLS tab
	bl_label = "Camera and Lighting"
	bl_idname = "OBJECT_PT_CameraLightingPanel_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.mmd_light_setup", text = "Add MMD light (broken)", icon="LIGHT")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.mmd_camera_to_blender_camera", text = "Convert MMD cameras to Blender cameras", icon="CAMERA_DATA")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.background_color_picker", text = "MMD background color picker", icon="COLOR")
		layout.prop(context.scene, "BackgroundColor")
		row = layout.row()
	

"""

@register_wrap
class MMDlightSetupPanel(bpy.types.Panel):
	#One-click light Setup for mmd_tools#
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

@register_wrap
class MMDCameraToBlenderCameraPanel(bpy.types.Panel):
	#Convert MMD cameras back to Blender cameras
	bl_idname = "OBJECT_PT_mmd_camera_to_blender_camera"
	bl_label = "Convert MMD Cameras to Blender cameras"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.mmd_camera_to_blender_camera", text = "Convert MMD cameras to Blender cameras")
		row = layout.row()

@register_wrap
class MMDBackgroundColorPicker_Panel(bpy.types.Panel):
	#Selects world background color and a contrasting text color#
	bl_idname = "OBJECT_PT_mmd_background_color_picker"
	bl_label = "MMD background color picker"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row = layout.row()
		layout.prop(context.scene, "BackgroundColor")
		row.operator("ffxiv_mmd_tools_helper.background_color_picker", text = "MMD background color picker")
		row = layout.row()
"""