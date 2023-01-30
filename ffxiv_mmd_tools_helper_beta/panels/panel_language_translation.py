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

		row.label(text="Mass Rename Bones", icon="ARMATURE_DATA")
		row = layout.row()
		row = layout.row()
		layout.prop(context.scene, "Origin_Armature_Type")
		row = layout.row()
		layout.prop(context.scene, "Destination_Armature_Type")
		row = layout.row()
		row.operator("object.bones_renamer", text = "Mass Rename Bones")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.blender_to_japanese_bone_names", text = "Blender to MMD Japanese Bone Name")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.reverse_japanese_english", text = "Swap MMD Japanese/English Bone Names")
		row = layout.row()
		row.label(text="Find this string in bone names:")
		row = layout.row()
		row.prop(context.scene,"find_bone_string")
		row = layout.row()
		row.label(text="Replace it with this string:")
		row = layout.row()
		row.prop(context.scene,"replace_bone_string")
		row = layout.row()
		row.prop(context.scene, "bones_all_or_selected")
		row = layout.row()
		row.label(text="Selected bones only")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.replace_bones_renaming", text = "Find and replace a string in bone names")


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