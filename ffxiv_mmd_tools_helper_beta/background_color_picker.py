import bpy
import sys

from . import register_wrap

"""
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

def main(context):

	spaces3d = [a.spaces.active for a in bpy.context.screen.areas if a.type == 'VIEW_3D']
	for s in spaces3d: 
		s.shading.type = 'RENDERED'

	bpy.data.worlds[0].node_tree.nodes["Background"].inputs[0].default_value = \
		( round(bpy.context.scene.BackgroundColor[0])\
		, round(bpy.context.scene.BackgroundColor[1])\
		, round(bpy.context.scene.BackgroundColor[2])
		, 1 \
		)

	bpy.context.preferences.themes[0].view_3d.space.text_hi = \
		(round(1-bpy.context.scene.BackgroundColor[0])\
		, round(1-bpy.context.scene.BackgroundColor[1])\
		,round(1-bpy.context.scene.BackgroundColor[2]))
	
@register_wrap
class MMDBackgroundColorPicker(bpy.types.Operator):
	"""Selects world background color and a contrasting text color"""
	bl_idname = "ffxiv_mmd_tools_helper.background_color_picker"
	bl_label = "MMD background color picker"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.BackgroundColor = bpy.props.FloatVectorProperty( \
		name="Background Color" \
		, description="Set world background color" \
		, default=(1.0, 1.0, 1.0) \
		, min=0.0 \
		, max=1.0 \
		, soft_min=0.0 \
		, soft_max=1.0 \
		, step=3 \
		, precision=2 \
		, options={'ANIMATABLE'} \
		, subtype='COLOR' \
		, unit='NONE' \
		, size=3 \
		, update=None \
		, get=None \
		, set=None )

	def execute(self, context):
		main(context)
		return {'FINISHED'}