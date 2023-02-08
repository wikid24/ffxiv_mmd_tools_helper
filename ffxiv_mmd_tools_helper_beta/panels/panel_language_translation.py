import bpy
from .. import register_wrap


@register_wrap
class LanguageTranslationPanel_MTH(bpy.types.Panel):
	#Creates the Bones Renamer Panel in a VIEW_3D TOOLS tab
	bl_label = "Language and Translation"
	bl_idname = "OBJECT_PT_LanguageTranslationPanel_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="Mass Rename Bones", icon="GROUP_BONE")
		row = layout.row()
		#split = row.split(factor=0.5)
		col = layout.column(align=True)
		grid = col.grid_flow(row_major=True, align=True)
		grid.column(align=True).prop(context.scene, "Origin_Armature_Type")
		grid.column(align=True).prop(context.scene, "Destination_Armature_Type")
		grid = col.grid_flow(row_major=True, align=True)
		grid.column(align=True).operator("object.bones_renamer", text = "Mass Rename Bones",icon='IMPORT')
		grid.column(align=True).operator("object.bone_names_showhide", text = "Show/Hide",icon='HIDE_ON')
		row = layout.row()
		col = layout.column(align=True)
		grid = col.grid_flow(row_major=True, align=True)
		grid.column(align=True).operator("ffxiv_mmd_tools_helper.blender_to_japanese_bone_names", text = "Blender to MMD Jap",icon='TRACKING_REFINE_FORWARDS')
		grid.column(align=True).operator("ffxiv_mmd_tools_helper.reverse_japanese_english", text = "Swap Jap/Eng",icon='UV_SYNC_SELECT')
		row = layout.row()
		col = row.column(align=True)
		col.label(text="Find in bone names:")
		col.prop(context.scene,"find_bone_string")
		col.prop(context.scene, "bones_all_or_selected")
		col = row.column(align=True)
		col.label(text="Replace with:")
		col.prop(context.scene,"replace_bone_string")
		col.operator("ffxiv_mmd_tools_helper.replace_bones_renaming", text = "Find and Replace", icon='VIEWZOOM')



"""


@register_wrap
class BonesRenamerPanel_MTH(bpy.types.Panel):
	#Creates the Bones Renamer Panel in a VIEW_3D TOOLS tab
	bl_label = "Bones Renamer"
	bl_idname = "OBJECT_PT_bones_renamer_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="Mass Rename Bones", icon="ARMATURE_DATA")
		row = layout.row()
		row = layout.row()
		layout.prop(context.scene, "Origin_Armature_Type")
		row = layout.row()
		layout.prop(context.scene, "Destination_Armature_Type")
		row = layout.row()
		row.operator("object.bones_renamer", text = "Mass Rename Bones")
		row = layout.row()

@register_wrap
class BlenderToJapaneseBoneNamesPanel(bpy.types.Panel):
	#Creates a Panel
	bl_idname = "OBJECT_PT_blender_to_japanese_bone_names"
	bl_label = "Copy Blender bone names to Japanese bone names"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="Copy Blender bone names to Japanese bone names", icon="TEXT")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.blender_to_japanese_bone_names", text = "Copy Blender bone names to Japanese bone names")
		row = layout.row()


@register_wrap
class ReverseJapaneseEnglishPanel(bpy.types.Panel):
	#Sets up nodes in Blender node editor for rendering toon textures
	bl_idname = "OBJECT_PT_reverse_japanese_english"
	bl_label = "Reverse Japanese English names"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="Reverse Japanese English names", icon="TEXT")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.reverse_japanese_english", text = "Reverse Japanese English names")
		row = layout.row()
"""