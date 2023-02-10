import bpy
from . import register_wrap


@register_wrap
class ImportModelPanel_MTH(bpy.types.Panel):
	#Import Model panel
	bl_label = "Import FFXIV Model"
	bl_idname = "OBJECT_PT_ImportModelPanel_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_options = {'DEFAULT_CLOSED'}
	bl_order = 1

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.ffxiv_file_browser_operator", text="Import FFXIV Model from .fbx File", icon='IMPORT')
		row = layout.row()
		col = layout.column(align=True)
		grid = col.grid_flow(row_major=True, align=True)
		#split = row.split(factor=0.66)
		grid.row(align=True).prop(context.scene, "selected_ffxiv_test_model")
		grid.row(align=True).operator("ffxiv_mmd_tools_helper.import_ffxiv_model", text = "Import", icon='IMPORT')


@register_wrap
class LanguageTranslationPanel_MTH(bpy.types.Panel):
	#Creates the Bones Renamer Panel in a VIEW_3D TOOLS tab
	bl_label = "Language and Translation"
	bl_idname = "OBJECT_PT_LanguageTranslationPanel_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_order = 2

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="Mass Rename Bones", icon="GROUP_BONE")
		row = layout.row()
		#split = row.split(factor=0.5)
		col = layout.column(align=True)
		grid = col.grid_flow(row_major=True, align=True)
		grid.column(align=True).prop(context.scene, "Origin_Armature_Type")
		grid.column(align=True).prop(context.scene, "Destination_Armature_Type")
		grid = col.grid_flow(row_major=True, align=True)
		grid.column(align=True).operator("ffxiv_mmd_tools_helper.bones_renamer", text = "Mass Rename Bones",icon='IMPORT')
		grid.column(align=True).operator("ffxiv_mmd_tools_helper.bone_names_showhide", text = "Show/Hide",icon='HIDE_ON')
		row = layout.row()
		col = layout.column(align=True)
		grid = col.grid_flow(row_major=True, align=True)
		grid.column(align=True).operator("ffxiv_mmd_tools_helper.blender_to_japanese_bone_names", text = "Blender to MMD Jap",icon='TRACKING_REFINE_FORWARDS')
		grid.column(align=True).operator("ffxiv_mmd_tools_helper.reverse_japanese_english", text = "Swap Jap/Eng",icon='UV_SYNC_SELECT')
		


@register_wrap
class BonesAndIKPanel_MTH(bpy.types.Panel):
	#Mass add bone groups
	bl_idname = "OBJECT_PT_BonesAndIKPanel_MTH"
	bl_label = "Bones and IK"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_order = 3

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="MMD Bone Conversion", icon="CONSTRAINT_BONE")
		split = layout.split( factor=0.80, align=True)
		split.prop(context.scene, "selected_bone_tool")	
		split.operator("ffxiv_mmd_tools_helper.bone_tools", text = "Run", icon='ORIENTATION_NORMAL')
		row = layout.row()
		col = row.column(align=True)
		col.label(text="Find in name:")
		col.prop(context.scene,"find_bone_string")
		col.prop(context.scene, "bones_all_or_selected")
		col = row.column(align=True)
		col.label(text="Replace with:")
		col.prop(context.scene,"replace_bone_string")
		col.operator("ffxiv_mmd_tools_helper.replace_bones_renaming", text = "Replace", icon='VIEWZOOM')
		row = layout.row()
		col = layout.column(align=True)
		grid = col.grid_flow(row_major=True)
		row = grid.row(align=True)
		row.label(text="IK", icon="CONSTRAINT_BONE")
		row.operator("ffxiv_mmd_tools_helper.add_foot_leg_ik", text = "Add Leg/Foot IK")
		row.operator("ffxiv_mmd_tools_helper.add_hand_arm_ik", text = "Add Hand/Arm IK")
		row = layout.row(align=True)
		col = row.column(align=True)
		col.label(text="Bone Groups", icon="GROUP_BONE")
		col = row.column(align=True)
		col.operator("ffxiv_mmd_tools_helper.add_bone_groups", text = "Auto-Generate")

@register_wrap
class RigidBodiesJointsPanel_MTH(bpy.types.Panel):
	#Rigid Body panel#
	bl_label = "Rigid Bodies and Joints"
	bl_idname = "OBJECT_PT_RigidBodiesJointsPanel_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_order = 4

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="Converted to MMD Model(English bones only)")
		row = layout.row()
		col = row.column()
		col.operator("ffxiv_mmd_tools_helper.add_rigid_body", text = "Add Rigid Bodies", icon="RIGID_BODY")
		col = row.column()
		row.operator("ffxiv_mmd_tools_helper.add_joints", text = "Add Joints", icon = "RIGID_BODY_CONSTRAINT")


@register_wrap
class ShapeKeysBoneMorphsPanel_MTH(bpy.types.Panel):
	bl_idname = "OBJECT_PT_ShapeKeysBoneMorphsPanel_MTH"
	bl_label = "Bone Morphs (Facial Expressions)"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_order = 5

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="Add Bone Morphs (MMD Model Only)", icon="SHAPEKEY_DATA")
		"""
		row = layout.row()
		col = row.column(align=True)
		split = col.split(factor = 0.55,align=True)
		split.prop(context.scene, "bone_morph_ffxiv_model_list")
		split.operator("ffxiv_mmd_tools_helper.add_bone_morphs", text = "Create",icon='SHAPEKEY_DATA')
		split.operator("ffxiv_mmd_tools_helper.open_bone_morphs_file", text="File",icon='FILE')
		"""
		row = layout.row()
		col = layout.column(align=True)
		grid = col.grid_flow(row_major=True)
		row = grid.row(align=True)
		row.prop(context.scene, "bone_morph_ffxiv_model_list")
		row.operator("ffxiv_mmd_tools_helper.add_bone_morphs", text = "Generate",icon='SHAPEKEY_DATA')
		row.operator("ffxiv_mmd_tools_helper.open_bone_morphs_file", text="",icon='CURRENT_FILE')
		#row = layout.row()
		#layout.prop(context.scene, "alternate_folder_cbx", text="Use Alternate Folder for CSVs (broken)")
		row = layout.row(align=True)
		col = row.column(align=True)
		col.column(align=True).prop(context.scene,'bone_morph_rotation_mode_list')
		col = row.column(align=True)
		col.column(align=True).operator("ffxiv_mmd_tools_helper.change_face_rotation_mode",text='Change Rotation Mode')
		

@register_wrap
class SkirtPanel_MTH(bpy.types.Panel):
	bl_idname = "OBJECT_PT_SkirtPanel_MTH"
	bl_label = "Skirt"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_options = {'DEFAULT_CLOSED'}
	bl_order = 6

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.generate_skirt_modal", text = "Generate A New Skirt Object",icon='SHADERFX')
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.move_mesh_to_new_skirt_btn", text = "Move Mesh To New Skirt Object",icon='PASTEDOWN')
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.weight_paint_transfer_to_mesh_btn", text = "Weight Paint Transfer To Mesh",icon='MOD_VERTEX_WEIGHT')
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.delete_ffxiv_skirt_vertex_groups", text = "Delete FFXIV Skirt Vertex Groups",icon='GPBRUSH_ERASE_HARD')
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.merge_bones_and_meshes_to_ffxiv_model", text = "Merge Bones And Meshes To Model",icon='AUTOMERGE_ON')
		
@register_wrap
class CameraLightingPanel_MTH(bpy.types.Panel):
	bl_label = "Camera and Lighting"
	bl_idname = "OBJECT_PT_CameraLightingPanel_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_options = {'DEFAULT_CLOSED'}
	bl_order = 7

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.mmd_light_setup", text = "Add MMD light (broken)", icon="LIGHT")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.mmd_camera_to_blender_camera", text = "Convert MMD cameras to Blender cameras", icon="CAMERA_DATA")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.background_color_picker", text = "MMD background color picker", icon="COLOR")
		layout.prop(context.scene, "BackgroundColor")
		row = layout.row()

@register_wrap
class ShadingAndToonsPanel_MTH(bpy.types.Panel):
	#User can modify the rendering of toon texture color
	bl_idname = "OBJECT_PT_ShadingAndToonsPanel_MTH"
	bl_label = "Shading and Toons"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_options = {'DEFAULT_CLOSED'}
	bl_order = 8

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="MMD Render toon textures (broken)", icon="MATERIAL")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.mmd_toon_render_node_editor", text = "MMD Create Toon Material Nodes (broken)",icon='MATERIAL')
		row = layout.row()

		row.label(text="MMD Toon modifier (broken)", icon='NODE_MATERIAL')
		layout.prop(context.scene, "ToonModifierBlendType")
		row = layout.row()
		layout.prop(context.scene, "ToonModifierColor")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.toon_modifier", text = "Modify Toon (broken)",icon='NODE_MATERIAL')

@register_wrap
class MiscellaneousToolsPanel_MTH(bpy.types.Panel):
	#Miscellaneous Tools panel
	bl_label = "Miscellaneous Tools"
	bl_idname = "OBJECT_PT_MiscellaneousToolsPanel_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_options = {'DEFAULT_CLOSED'}
	bl_order = 9

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="Misc Tools", icon='WORLD_DATA')
		row = layout.row()
		split = layout.split(factor=0.80,align=True)
		split.prop(context.scene, "selected_miscellaneous_tools")	
		split.operator("ffxiv_mmd_tools_helper.miscellaneous_tools", text = "Run", icon='ORIENTATION_NORMAL')

@register_wrap
class ExportMMD_MTH(bpy.types.Panel):
	#Mass add bone groups
	bl_idname = "OBJECT_PT_ExportMMD_MTH"
	bl_label = "Export MMD Preparation"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_options = {'DEFAULT_CLOSED'}
	bl_order = 10

	def draw(self, context):
		layout = self.layout
		row = layout.row(align=True)
		col = row.column(align=True)
		col.operator("ffxiv_mmd_tools_helper.add_display_panel_groups", text = "Create Display Panels", icon="LONGDISPLAY")
		col = row.column(align=True)
		col.prop (context.scene, "mmd_display_panel_options")
		row.separator()
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.sort_mmd_bone_order", text = "Sort MMD Bone Order/Deformation Tiers", icon="MOD_ARRAY") #Set bone order & deformation tiers
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.hide_special_bones", text = "Hide Special & Physics Bones", icon="HIDE_ON") #FFXIV stock face deformation shape keys (anything that starts with 'shp'), Physics Bones (Hair/Skirt/Armor/etc), Leg bones (after physics has been applied since the control bones should be used instead)

		row = layout.row()
		row.label(text="**TODO** Populate MMD Bone Names", icon="GROUP_BONE") #so that they don't show up as "NULL" in MMD
		row = layout.row()
		row.label(text="**TODO** Lock position / Rotation", icon="LOCKED") 
		row = layout.row()
		row.label(text="**TODO** Set Fixed Axis/Local Axis", icon="EMPTY_AXIS") 
		row = layout.row()
		row.label(text="**TODO** Edit Config File", icon="CURRENT_FILE") 
		row = layout.row()
		row.label(text="**TODO** Restore Config Defaults", icon="FILE_TICK") 
		
		"""
		row = layout.row(align=True)
		col = row.column(align=True)
		col.operator("ffxiv_mmd_tools_helper.armature_diagnostic", text = "Diagnose Armature (broken)",icon='ORPHAN_DATA')
		col = row.column(align=True)
		col.prop(context.scene, "selected_armature_to_diagnose")
		row = layout.row()
		"""

