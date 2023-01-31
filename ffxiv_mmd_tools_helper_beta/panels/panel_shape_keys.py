import bpy
from .. import register_wrap


@register_wrap
class ShapeKeysPanel_MTH(bpy.types.Panel):
	bl_idname = "OBJECT_PT_ShapeKeysPanel_MTH"
	bl_label = "Shape Keys"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="Add shape keys to FFXIV model", icon="SHAPEKEY_DATA")
		row = layout.row()
		layout.prop (context.scene, "ffxiv_model_list")
		row = layout.row()
		row.operator("object.add_shape_keys_btn", text = "Add shape keys to FFXIV model",icon='SHAPEKEY_DATA')
		row = layout.row()
		layout.prop(context.scene, "alternate_folder_cbx", text="Use Alternate Folder for CSVs (broken)")