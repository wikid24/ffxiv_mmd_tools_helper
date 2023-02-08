import bpy
from .. import register_wrap


@register_wrap
class ShapeKeysBoneMorphsPanel_MTH(bpy.types.Panel):
	bl_idname = "OBJECT_PT_ShapeKeysBoneMorphsPanel_MTH"
	bl_label = "Shape Keys / Bone Morphs"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="Add Bone Morphs (Converted to MMD Model Only)", icon="SHAPEKEY_DATA")
		row = layout.row()
		col = layout.column(align=True)
		grid = col.grid_flow(row_major=True, align=True)
		grid.column(align=True).prop(context.scene, "bone_morph_ffxiv_model_list")
		grid.column(align=True).operator("object.add_bone_morphs", text = "Add",icon='SHAPEKEY_DATA')
		grid.column(align=True).operator("object.open_bone_morphs_file", text = "Open",icon='FILE')
		row = layout.row()
		layout.prop(context.scene, "alternate_folder_cbx", text="Use Alternate Folder for CSVs (broken)")

		"""
		row.label(text="Add shape keys to FFXIV model", icon="SHAPEKEY_DATA")
		row = layout.row()
		layout.prop (context.scene, "ffxiv_model_list")
		row = layout.row()
		row.operator("object.add_shape_keys_btn", text = "Add shape keys to FFXIV model",icon='SHAPEKEY_DATA')
		row = layout.row()
		layout.prop(context.scene, "alternate_folder_cbx", text="Use Alternate Folder for CSVs (broken)")
		"""