import bpy
from . import register_wrap
from . import model
from . import bone_retargeting_addon



@register_wrap
class ART_BoneMapping_MTH(bpy.types.Panel):
	bl_idname = "OBJECT_PT_ART_BoneMapping_MTH"
	bl_label = "FFXIV MMD - Add Bone Mapping"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "Retargeting"
	bl_options = {'DEFAULT_CLOSED'}
	bl_order = 2

	def draw(self, context):
		active_obj = context.active_object

		layout = self.layout
		
		if bone_retargeting_addon.is_addon_installed() == False:
			row = layout.row()
			row.label(text = 'Animation Regargeting v2.1.0 or higher required')
		else:
			if bone_retargeting_addon.is_source_and_target_mapped(active_obj) == False:
				row = layout.row()
				row.label(text = 'Select source & target armature')
			else:
				row = layout.row()
				row.operator("ffxiv_mmd.art_add_bone_mapping", text="CLEAR THE MAPPING LIST").bone_group='clear_mapping'
				"""
				row = layout.row()
				row.label(text = 'Generic TDA MMD Model')
				row = layout.row()
				grid = row.grid_flow(columns=4,align=True)
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Body").bone_group='body'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Eyes").bone_group='eye'

				row = layout.row()
				row.label(text = 'Kaito MMD Model')
				row = layout.row()
				grid = row.grid_flow(columns=5,align=True)
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Body").bone_group='body'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Eyes").bone_group='eye'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Skirt").bone_group='skirt'

				row = layout.row()
				row.label(text = 'FFXIV (converted) MMD Model')
				row = layout.row()
				grid = row.grid_flow(columns=3,align=True)
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="ALL!").bone_group='all_verbatim'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Body").bone_group='body'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Breasts").bone_group='breast'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Mouth").bone_group='mouth'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Eyes").bone_group='eye'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Eyelids").bone_group='eyelid'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Eyebrows").bone_group='eyebrow'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Skirt").bone_group='skirt'
				"""
				row = layout.row()
				row.label(text = 'Pick body part for mapping')
				row = layout.row()
				row.label(text = 'Should work on MMD(Kaito w/Skirt),FFXIV(converted),FFXIV')
				row = layout.row()
				grid = row.grid_flow(columns=3,align=True)
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="ALL!").bone_group='all_verbatim'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Body").bone_group='body'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Breasts").bone_group='breast'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Mouth").bone_group='mouth'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Eyes").bone_group='eye'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Eyelids").bone_group='eyelid'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Eyebrows").bone_group='eyebrow'
				grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Skirt").bone_group='skirt'
		
			
			


@register_wrap
class ART_RestPosition_MTH(bpy.types.Panel):
	bl_idname = "OBJECT_PT_ART_BoneMapping__MTH"
	bl_label = "FFXIV MMD - Rest Position Adjustments"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "Retargeting"
	bl_options = {'DEFAULT_CLOSED'}
	bl_order = 3

	def draw(self, context):
		active_obj = context.active_object

		layout = self.layout

		if bone_retargeting_addon.is_addon_installed() == False:
			row = layout.row()
			row.label(text = 'Animation Regargeting v2.1.0 or higher required')
		else:
			if bone_retargeting_addon.is_source_and_target_mapped(active_obj) == False:
				row = layout.row()
				row.label(text = 'Select source & target armature')
			else:
				layout = self.layout
				row = layout.row()
				row.label(text = 'Reset Armature Pose (location & rotation)')
				row = layout.row()
				grid = row.grid_flow(columns=2,align=True)
				grid.operator("ffxiv_mmd.art_apply_bone_rotation_to_target", text="Target Armature").bone_group='clear_mapping_target'
				grid.operator("ffxiv_mmd.art_apply_bone_rotation_to_target", text="Source Armature").bone_group='clear_mapping_source'
				

				row = layout.row()
				row.label(text = 'Apply Rotation To Target')
				row = layout.row()
				grid = row.grid_flow(columns=4,align=True)
				grid.operator("ffxiv_mmd.art_apply_bone_rotation_to_target", text="Upper Arms").bone_group='upperarm'
				grid.operator("ffxiv_mmd.art_apply_bone_rotation_to_target", text="Forearms").bone_group='forearm'
				grid.operator("ffxiv_mmd.art_apply_bone_rotation_to_target", text="Wrists").bone_group='wrist'
				grid.operator("ffxiv_mmd.art_apply_bone_rotation_to_target", text="Hands").bone_group='hand'
				row = layout.row()
				grid = row.grid_flow(columns=4,align=True)
				grid.operator("ffxiv_mmd.art_apply_bone_rotation_to_target", text="Upper Legs").bone_group='upperleg'
				grid.operator("ffxiv_mmd.art_apply_bone_rotation_to_target", text="Lower Legs").bone_group='lowerleg'
				grid.operator("ffxiv_mmd.art_apply_bone_rotation_to_target", text="Feet").bone_group='feet'
				grid.operator("ffxiv_mmd.art_apply_bone_rotation_to_target", text="Toes").bone_group='toe'
				row = layout.row()
				row.prop(context.scene,"art_reset_rot_if_no_match",text='Reset Rotation On Target Bone if Source Bone Not Found')
