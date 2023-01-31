import bpy
from .. import register_wrap


@register_wrap
class ImportModelPanel_MTH(bpy.types.Panel):
	#Import Model panel
	bl_label = "Import FFXIV Model"
	bl_idname = "OBJECT_PT_ImportModelPanel_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.operator("object.ffxiv_file_browser_operator", text="Import FFXIV Model from .fbx File", icon='IMPORT')
		row = layout.row()
		layout.prop(context.scene, "selected_ffxiv_test_model")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.import_ffxiv_model", text = "Import from list", icon='IMPORT')

