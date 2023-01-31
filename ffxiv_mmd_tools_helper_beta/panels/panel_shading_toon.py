import bpy
from .. import register_wrap


@register_wrap
class ShadingAndToonsPanel_MTH(bpy.types.Panel):
	#User can modify the rendering of toon texture color
	bl_idname = "OBJECT_PT_ShadingAndToonsPanel_MTH"
	bl_label = "Shading and Toons"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="MMD Render toon textures", icon="MATERIAL")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.mmd_toon_render_node_editor", text = "MMD Create Toon Material Nodes",icon='MATERIAL')
		row = layout.row()

		row.label(text="MMD Toon modifier", icon='NODE_MATERIAL')
		layout.prop(context.scene, "ToonModifierBlendType")
		row = layout.row()
		layout.prop(context.scene, "ToonModifierColor")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.toon_modifier", text = "Modify Toon",icon='NODE_MATERIAL')

"""

@register_wrap
class MMDToonModifierPanel(bpy.types.Panel):
	#User can modify the rendering of toon texture color
	bl_idname = "OBJECT_PT_mmd_toon_modifier"
	bl_label = "MMD toon modifier"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="MMD Toon modifier", icon="MATERIAL")
		layout.prop(context.scene, "ToonModifierBlendType")
		row = layout.row()
		layout.prop(context.scene, "ToonModifierColor")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.toon_modifier", text = "Modify Toon")

@register_wrap
class MMDToonTexturesToNodeEditorShaderPanel(bpy.types.Panel):
	#Sets up nodes in Blender node editor for rendering toon textures
	bl_idname = "OBJECT_PT_mmd_toon_render_node_editor"
	bl_label = "MMD toon textures render using node editor "
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="MMD Render toon textures", icon="MATERIAL")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.mmd_toon_render_node_editor", text = "MMD Create Toon Material Nodes")
		row = layout.row()
"""