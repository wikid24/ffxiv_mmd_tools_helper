import bpy
from . import register_wrap
from . import model
from . import bone_retargeting_addon
from . import bone_tools



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

				art_mapping_controls = bpy.context.active_object.retargeting_context
				row = layout.row()
				if art_mapping_controls:
					if art_mapping_controls.ui_editing_mappings is None or art_mapping_controls.ui_editing_mappings == False:
						row.label(text = 'Edit the bone mapping to see options')
					else:
						#to-do: check if in pose mode first
						box = layout.box()
						#row = box.row()
						#grid = row.grid_flow(columns=2,align=True)
						
						
						if art_mapping_controls.active_mapping is None:
							row.label(text = 'Pick body part for mapping')
						else:
							#row = box.row()
							#row.label(text='Index: ' + str(art_mapping_controls.active_mapping))
							index = art_mapping_controls.active_mapping
							mapping_data = bpy.context.active_object.get('retargeting_context').get('mappings')
							source_arm = art_mapping_controls.get('source')
							target_arm = art_mapping_controls.get('target')
							source_bone = None
							target_bone = None
							source_bone_name = ''
							target_bone_name = ''
							source_bone_description = ''							
							target_bone_description = ''
							if str(art_mapping_controls.active_mapping):
								if int(index) >= 0 and int(index)<=(len(mapping_data)):
									source_bone_name = mapping_data[index].get('source')
									if source_bone_name:
										source_bone = source_arm.pose.bones.get(source_bone_name)
									target_bone_name = mapping_data[index].get('target')
									if target_bone_name:
										target_bone = target_arm.pose.bones.get(target_bone_name)

									if source_bone:
										source_bone_description = bone_tools.get_metadata_by_bone_name(source_bone_name,'description')
									if target_bone:
										print(target_bone.name)
										target_bone_description = bone_tools.get_metadata_by_bone_name(target_bone_name,'description')
							#else:
							row = box.row()
							grid = row.grid_flow(columns=2,align=True)
							active_bone_description = None
							active_bone_text = ''
							if context.active_pose_bone:
								active_bone_text = context.active_pose_bone.name
								active_bone_description = bone_tools.get_metadata_by_bone_name(active_bone_text,'description')
							if active_bone_description:
								active_bone_text += ' : ' + active_bone_description
							grid.label(text = active_bone_text)	
							#grid.operator("ffxiv_mmd.art_set_bone_in_mapping",text='Find Source',icon='ZOOM_PREVIOUS').armature_type = 'source'
							grid.operator("ffxiv_mmd.art_set_bone_in_mapping",text='Set as Target',icon='TRIA_DOWN').armature_type = 'target'
							#if context.active_object:
								#if context.active_pose_bone:
							
									
								#else:
									#grid.label(text='Select a bone')
							row = box.row()
							grid = row.grid_flow(columns=2,align=True)
							grid.label(text = 'Source: ')
							grid2 = grid.grid_flow(columns=2,align=True)
							grid2.operator("ffxiv_mmd.art_select_bone_in_mapping",text=source_bone_name).armature_type = 'source'
							grid2.operator("ffxiv_mmd.art_set_bone_in_mapping",text='',icon='ZOOM_PREVIOUS').armature_type = 'source'
							grid.label(text = source_bone_description)
							grid.label(text = 'Target: ')
							grid.operator("ffxiv_mmd.art_select_bone_in_mapping",text=target_bone_name).armature_type = 'target'
							grid.label(text = target_bone_description)
								
							#row.prop
					
					row = layout.row()
					grid = row.grid_flow(columns=2,align=True)
					row.operator("ffxiv_mmd.art_autofix_bone_mapping", text="Autofix the Mapping List").bone_group='clear_mapping'
					row.operator("ffxiv_mmd.art_add_bone_mapping", text="CLEAR THE MAPPING LIST").bone_group='clear_mapping'
			
					row = layout.row()
					row.label(text = 'Add Mapping by Bone Type')
					row = layout.row()
					grid = row.grid_flow(columns=3,align=True)
					grid.operator("ffxiv_mmd.art_add_bone_mapping", text="ALL!").bone_group='all_verbatim'
					grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Body").bone_group='body'
					grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Tail").bone_group='tail'
					grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Breasts").bone_group='breast'
					grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Skirt").bone_group='skirt'
					row = layout.row()
					grid = row.grid_flow(columns=3,align=True)
					grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Mouth").bone_group='mouth'
					grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Eyes").bone_group='eye'
					grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Eyelids").bone_group='eyelid'
					grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Eyebrows").bone_group='eyebrow'
					grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Nose").bone_group='nose'
					grid.operator("ffxiv_mmd.art_add_bone_mapping", text="Ears").bone_group='ear'
					row = layout.row()
					row.label(text = 'Should work on MMD(Kaito w/Skirt),FFXIV(converted),FFXIV')
				
		
			
			


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

				row = layout.row()
				row.label(text = 'EXPERIMENTAL:')
				grid = row.grid_flow(columns=1,align=True)
				grid.operator("ffxiv_mmd.adjust_kaito_bone_angle", text="Fix Kaito Wrists/Hands")