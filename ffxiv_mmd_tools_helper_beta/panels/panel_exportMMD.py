import bpy
from .. import register_wrap


@register_wrap
class ExportMMD_MTH(bpy.types.Panel):
	#Mass add bone groups
	bl_idname = "OBJECT_PT_ExportMMD_MTH"
	bl_label = "Export MMD"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_options = {'DEFAULT_CLOSED'}

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="Add MMD Display Panel Groups (not fixed yet)", icon="LONGDISPLAY")
		row = layout.row()
		layout.prop (context.scene, "display_panel_options")
		row = layout.row()
		row.operator("object.add_display_panel_groups", text = "Add MMD display panel items (not fixed yet)", icon="LONGDISPLAY")
		row = layout.row()
		row.label(text="Hide Special & Physics Bones (TBD)", icon="LONGDISPLAY") #FFXIV stock face deformation shape keys (anything that starts with 'shp'), Physics Bones (Hair/Skirt/Armor/etc), Leg bones (after physics has been applied since the control bones should be used instead)
		row = layout.row()
		row.label(text="Populate MMD Bone Names (TBD)", icon="LONGDISPLAY") #so that they don't show up as "NULL" in MMD
		row = layout.row()
		row.label(text="Set Bone Export Order (TBD)", icon="LONGDISPLAY") #Set bone order & deformation tiers
		row = layout.row()
		row.label(text="Lock position / Rotation (TBD)", icon="LONGDISPLAY") 
		row = layout.row()
		row.label(text="Armature Diagnostic (broken)", icon='ARMATURE_DATA')
		row = layout.row()
		layout.prop(context.scene, "selected_armature_to_diagnose")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.armature_diagnostic", text = "Diagnose Armature",icon='ORPHAN_DATA')
		row = layout.row()


		
		