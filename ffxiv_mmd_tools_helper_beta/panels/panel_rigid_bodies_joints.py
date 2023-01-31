import bpy
from .. import register_wrap

@register_wrap
class RigidBodiesJointsPanel_MTH(bpy.types.Panel):
	#Rigid Body panel#
	bl_label = "Rigid Bodies and Joints"
	bl_idname = "OBJECT_PT_RigidBodiesJointsPanel_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.add_rigid_body", text = "Add Rigid Bodies to armature", icon="RIGID_BODY")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.add_joints", text = "Add Joints to Rigid Bodies", icon = "RIGID_BODY_CONSTRAINT")


"""
@register_wrap
class RigidBodyPanel(bpy.types.Panel):
	#Rigid Body panel#
	bl_label = "Rigid Body panel"
	bl_idname = "OBJECT_PT_rigid_body_panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.add_rigid_body", text = "Add Rigid Bodies to armature")
		row = layout.row()

@register_wrap
class JointsPanel(bpy.types.Panel):
	#Joints panel#
	bl_label = "Joints panel"
	bl_idname = "OBJECT_PT_joints_panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.add_joints", text = "Add Joints to Rigid Bodies")
		row = layout.row()
"""