import bpy
from .. import register_wrap


@register_wrap
class MiscellaneousToolsPanel_MTH(bpy.types.Panel):
	#Miscellaneous Tools panel
	bl_label = "Miscellaneous Tools"
	bl_idname = "OBJECT_PT_MiscellaneousToolsPanel_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"

	def draw(self, context):
		layout = self.layout
		
		row = layout.row()
		row.label(text="Misc Tools (MMD English bones only)", icon='WORLD_DATA')
		row = layout.row()
		split = layout.split(factor=0.66)
		split.prop(context.scene, "selected_miscellaneous_tools")	
		split.operator("ffxiv_mmd_tools_helper.miscellaneous_tools", text = "Execute", icon='ORIENTATION_NORMAL')

		

"""
@register_wrap
class ImportFFXIVTestModelPanel(bpy.types.Panel):
	#Import FFXIV Test Model panel
	bl_label = "Import FFXIV Test Model Panel"
	bl_idname = "OBJECT_PT_import_ffxiv_model"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout

		row = layout.row()
		layout.prop(context.scene, "selected_ffxiv_test_model")
		row = layout.row()
		row.label(text="Import FFXIV Model", icon='WORLD_DATA')
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.import_ffxiv_model", text = "Execute Function")


@register_wrap
class MiscellaneousToolsPanel(bpy.types.Panel):
	#Miscellaneous Tools panel
	bl_label = "Miscellaneous Tools Panel"
	bl_idname = "OBJECT_PT_miscellaneous_tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout

		row = layout.row()
		layout.prop(context.scene, "selected_miscellaneous_tools")
		row = layout.row()
		row.label(text="Miscellaneous Tools", icon='WORLD_DATA')
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.miscellaneous_tools", text = "Execute Function")

@register_wrap
class ArmatureDiagnosticPanel(bpy.types.Panel):
	#Armature Diagnostic panel
	bl_label = "Armature Diagnostic Panel"
	bl_idname = "OBJECT_PT_armature_diagnostic"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		layout.prop(context.scene, "selected_armature_to_diagnose")
		row = layout.row()
		row.label(text="Armature Diagnostic", icon='ARMATURE_DATA')
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.armature_diagnostic", text = "Diagnose Armature")
		row = layout.row()
		row = layout.row()

@register_wrap
class MmdToolsDisplayPanelGroupsPanel(bpy.types.Panel):
	#Mass add bone names and shape key names to display panel groups#
	bl_idname = "OBJECT_PT_mmd_add_display_panel_groups"
	bl_label = "Create Display Panel Groups and Add Items"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="Add MMD Display Panel Groups", icon="ARMATURE_DATA")
		row = layout.row()
		layout.prop (context.scene, "display_panel_options")
		row = layout.row()
		row.operator("object.add_display_panel_groups", text = "Add MMD display panel items")
		row = layout.row()
"""