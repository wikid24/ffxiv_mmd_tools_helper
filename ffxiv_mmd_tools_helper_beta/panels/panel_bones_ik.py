import bpy
from .. import register_wrap


@register_wrap
class BonesAndIKPanel_MTH(bpy.types.Panel):
	#Mass add bone groups
	bl_idname = "OBJECT_PT_BonesAndIKPanel_MTH"
	bl_label = "Bones and IK"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row = layout.row()
		row.label(text="Add IK to MMD model", icon="CONSTRAINT_BONE")
		row = layout.row()
		row.operator("object.add_foot_leg_ik", text = "Add leg and foot IK", icon="CONSTRAINT_BONE" )
		row = layout.row()
		row.operator("object.add_hand_arm_ik", text = "Add hand and arm IK", icon="CONSTRAINT_BONE")
		row = layout.row()
		row.label(text="Add Bone Groups", icon="GROUP_BONE")
		row = layout.row()
		layout.prop (context.scene, "bone_panel_bone_type_options")
		row = layout.row()
		row.operator("object.add_bone_groups", text = "Add Blender bone groups", icon="GROUP_BONE")
		row = layout.row()

"""

@register_wrap
class MmdToolsBoneGroupsPanel(bpy.types.Panel):
	#Mass add bone groups
	bl_idname = "OBJECT_PT_mmd_add_bone_groups"
	bl_label = "Create Bone Groups"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="Add Bone Groups", icon="ARMATURE_DATA")
		row = layout.row()
		layout.prop (context.scene, "bone_panel_bone_type_options")
		row = layout.row()
		row.operator("object.add_bone_groups", text = "Add Blender bone groups")
		row = layout.row()



@register_wrap
class ReplaceBonesRenamingPanel(bpy.types.Panel):
	#Replace Bones Renaming panel
	bl_label = "Replace bones renaming panel"
	bl_idname = "OBJECT_PT_replace_bones_renaming"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
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
		row = layout.row()




@register_wrap
class Add_MMD_IK_Panel(bpy.types.Panel):
	bl_idname = "OBJECT_PT_mmd_add_ik"
	bl_label = "Add IK to MMD model"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="Add IK to MMD model", icon="ARMATURE_DATA")
		row = layout.row()
		row.operator("object.add_foot_leg_ik", text = "Add leg and foot IK to MMD model")
		row = layout.row()
		row.operator("object.add_hand_arm_ik", text = "Add hand and arm IK to MMD model")
		row = layout.row()

"""