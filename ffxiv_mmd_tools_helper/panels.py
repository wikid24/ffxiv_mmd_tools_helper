import bpy
from . import register_wrap
from . import model


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
		row.operator("ffxiv_mmd.ffxiv_file_browser_operator", text="Import FFXIV .fbx File", icon='IMPORT')
		row = layout.row()
		col = layout.column(align=True)
		grid = col.grid_flow(row_major=True, align=True)
		#split = row.split(factor=0.66)
		grid.row(align=True).prop(context.scene, "selected_ffxiv_test_model")
		grid.row(align=True).operator("ffxiv_mmd.import_ffxiv_model", text = "Load Sample", icon='IMPORT')
		row = layout.row()
		row.label(text="FFXIV Conversion:")
		row = layout.row()
		#row.operator_context = 'INVOKE_DEFAULT'
		row.operator('mmd_tools.convert_to_mmd_model', text='Initialize MMD Struture', icon='ARMATURE_DATA')
		row = layout.row()
		row.operator("ffxiv_mmd.ffxiv_chara_file_browser_operator", text="Import FFXIV .chara File", icon='IMPORT')
		row = layout.row()
		row.prop(context.scene,"color_skin", text='',icon_only=True,icon='OUTLINER_DATA_MESH')
		row.prop(context.scene,"color_hair", text='',icon_only=True,icon='OUTLINER_DATA_MESH')
		row.prop(context.scene,"color_hair_highlights", text='',icon_only=True,icon='OUTLINER_DATA_MESH')
		row.prop(context.scene,"color_tattoo_limbal", text='',icon_only=True,icon='OUTLINER_DATA_MESH')
		row.prop(context.scene,"color_eyes", text='',icon_only=True,icon='OUTLINER_DATA_MESH')
		row.prop(context.scene,"color_lips", text='',icon_only=True,icon='OUTLINER_DATA_MESH')
		row.prop(context.scene,"color_facepaint", text='',icon_only=True,icon='OUTLINER_DATA_MESH')
		#row = layout.row()
		#row.operator("ffxiv_mmd.create_joints_from_csv", text = "Add Base Joints", icon = "RIGID_BODY_CONSTRAINT")


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
		obj = None
		if context.object is not None:
			obj = context.object
		layout = self.layout
		row = layout.row()
		row.label(text="Mass Rename Bones", icon="GROUP_BONE")
		row = layout.row()
		col = layout.column(align=True)
		grid = col.grid_flow(row_major=True, align=True)
		grid.column(align=True).prop(context.scene, "Origin_Armature_Type")
		grid.column(align=True).prop(context.scene, "Destination_Armature_Type")
		grid = col.grid_flow(align=True)
		row = grid.row(align=True)
		row.operator("ffxiv_mmd.bones_renamer", text = "Mass Rename Bones",icon='IMPORT')
		if obj:
			if obj.type=='ARMATURE':
				row.prop(context.object.data,"show_names",toggle=True ,text = "",icon_only=True,icon='SORTALPHA')
		row = layout.row(align=True)
		col = layout.column(align=True)
		grid = col.grid_flow(align=True)
		grid.column(align=True).operator("ffxiv_mmd.blender_to_japanese_bone_names", text = "Blender to MMD Jap",icon='TRACKING_REFINE_FORWARDS')
		grid.column(align=True).operator("ffxiv_mmd.reverse_japanese_english", text = "Swap Jap/Eng",icon='UV_SYNC_SELECT')


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
		obj = None
		root = None
		
		if context.object is not None:
			obj = context.object
			if model.findRoot(obj):
				root = model.findRoot(obj)

		layout = self.layout
		row = layout.row(align=True)
		grid = row.grid_flow(columns=1,align=True)
		row = grid.row(align=True)
		row.prop(context.space_data.overlay, 'show_bones', toggle=True, text='',icon_only=True,icon='HIDE_OFF' if context.space_data.overlay.show_bones else 'HIDE_ON' )
		if obj:
			if obj.type == 'ARMATURE':
				row.prop(obj.data,"show_names",toggle=True ,text = "",icon_only=True,icon='SORTALPHA')
				row.prop(obj,"show_in_front",toggle=True ,text = "",icon_only=True,icon='COMMUNITY')
				row.prop(obj.data, 'display_type',text='')


			else:
				row.label(text=' Bone Visibility')
			if root:
				row.prop(root.mmd_root, 'show_armature', toggle=True, icon_only=True, icon='ARMATURE_DATA')
		row = layout.row()
		row.label(text="MMD Conversion")
		split = layout.split( factor=0.80, align=True)
		split.prop(context.scene, "selected_bone_tool")	
		split.operator("ffxiv_mmd.bone_tools", text = "Run", icon='ORIENTATION_NORMAL')
		row = layout.row(align=True)
		col = row.column(align=True)
		grid = col.grid_flow(columns=1,align=True)
		grid.label(text="Find in name:")
		grid.prop(context.scene,"find_bone_string",text='')
		grid.operator("ffxiv_mmd.find_bones", text = "Find", icon='VIEWZOOM').append_to_selected=False
		col = row.column(align=True)
		grid = col.grid_flow(columns=1,align=True)
		grid.label(text="Replace with:")
		grid.prop(context.scene,"replace_bone_string",text='')
		grid.operator("ffxiv_mmd.replace_bones_renaming", text = "Replace", icon='CON_ROTLIMIT')
		grid.prop(context.scene, "bones_all_or_selected",text='Selected Only')
		#row = layout.row(align=True)
		#col = row.column(align=True)
		#grid = col.grid_flow(row_major=True,align=True)
		#grid.label(text="IK", icon="CONSTRAINT_BONE")
		#grid.operator("ffxiv_mmd.add_foot_leg_ik", text = "Leg/Foot IK")
		#grid.operator("ffxiv_mmd.add_hand_arm_ik", text = "Hand/Arm IK")
		row = layout.row(align=True)
		col = row.column(align=True)
		col.label(text="Bone Groups", icon="GROUP_BONE")
		col = row.column(align=True)
		col.operator("ffxiv_mmd.add_bone_groups", text = "Auto-Generate")


@register_wrap
class RigidBodiesPanel_MTH(bpy.types.Panel):
	#Rigid Body panel#
	bl_label = "Rigid Bodies"
	bl_idname = "OBJECT_PT_RigidBodiesPanel_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_order = 4

	def draw(self, context):
		root = model.findRoot(context.object)

		layout = self.layout
		# Display the active object's name in a text box

		row = layout.row()
		col = row.column()
		grid = col.grid_flow(align=True,columns=5)
		if model.findRoot(bpy.context.object) is not None:
			grid.prop(root.mmd_root,"show_rigid_bodies", toggle=True, text='',icon_only=True,icon='HIDE_OFF' if root.mmd_root.show_rigid_bodies else 'HIDE_ON' )
			grid.prop(root.mmd_root,"show_names_of_rigid_bodies", toggle=True, text='',icon_only=True,icon='SORTALPHA')
			grid.label(text="Rigid Body Visibility")
			grid.prop(root.mmd_root,"show_meshes", toggle=True, text='',icon_only=True,icon='OUTLINER_DATA_MESH')
			if not root.mmd_root.is_built:
				row.operator('mmd_tools.build_rig',text='',icon='PHYSICS',depress=False)
			else:
				row.operator('mmd_tools.clean_rig',text='', icon='PHYSICS',depress=True)
		else:
			grid.label(text="Rigid Body Visibility")
		row = layout.row()
		col = row.column()
		grid = col.grid_flow(align=True,columns=2)
		grid.label(text="Active Rigid: ")
		grid.label(text='Bone: ')	
		grid = col.grid_flow(align=True,columns=2)
		if(context.active_object):
			if context.active_object.mmd_type == 'RIGID_BODY':
				grid.prop(context.active_object,"name",text="")	
				grid.operator("ffxiv_mmd.get_bone_from_rigid_body",text=str(context.active_object.mmd_rigid.bone))
			else:
				grid.label(text='Select a Rigid Body')
		row = layout.row()
		col = row.column(align=True)
		grid = col.grid_flow(align=True)
		row = grid.row(align=True)
		row.label(text='Starts w/')
		row.label(text='Contains')
		row.label(text='Ends w/')
		row = grid.row(align=True)
		row.prop(context.scene,"rigidbody_startswith", text = "")
		row.prop(context.scene,"rigidbody_contains", text = "")
		row.prop(context.scene,"rigidbody_endswith", text = "")
		row = grid.row(align=True)
		row.operator("ffxiv_mmd.find_rigid_bodies", text = 'Find', icon='VIEWZOOM').append_to_selected=False
		row.operator("ffxiv_mmd.find_rigid_bodies", text = 'Find + Add', icon='ZOOM_IN').append_to_selected=True
		row.operator("ffxiv_mmd.clear_find_rigid_bodies", text='',icon='TRASH')
		row = layout.row()
		col = row.column()
		grid = col.grid_flow(align=True)
		grid.label(text='Bone Chain',icon='LINK_BLEND')
		grid.operator("ffxiv_mmd.select_rigid_body_bone_chain", text = 'Up', icon='TRIA_UP').direction='UP'
		grid.operator("ffxiv_mmd.select_rigid_body_bone_chain", text = 'Down', icon='TRIA_DOWN').direction='DOWN'
		grid.operator("ffxiv_mmd.select_rigid_body_bone_chain", text = 'All', icon='UV_SYNC_SELECT').direction='ALL'
		col = row.column()
		grid = col.grid_flow(align=True)
		grid.label(text="Skirt", icon='MESH_CONE')
		#row.operator("ffxiv_mmd.get_vertical_skirt_rigid_bodies", text = "Vert", icon="SORT_DESC")
		#row.operator("ffxiv_mmd.get_horizontal_skirt_rigid_bodies", text = "Horiz", icon="CENTER_ONLY")
		grid.operator("ffxiv_mmd.select_skirt_rigid_bodies", text = "Vert", icon="SORT_DESC").direction='VERTICAL'
		grid.operator("ffxiv_mmd.select_skirt_rigid_bodies", text = "Horiz", icon="CENTER_ONLY").direction='HORIZONTAL'
		grid.operator("ffxiv_mmd.select_skirt_rigid_bodies", text = "All", icon="CONE").direction='ALL'
		row = layout.row()
		col = row.column()
		col.label(text="Rigid Body Transform:", icon='CON_CLAMPTO')
		row = layout.row()
		col = row.column()
		grid = col.grid_flow(align=True)
		grid.operator("ffxiv_mmd.batch_update_rigid_bodies", text = 'Bulk Apply')
		grid.operator("ffxiv_mmd.batch_update_rigid_body_bone_chain", text='Bone Chain')
		grid.operator("ffxiv_mmd.batch_update_rigid_body_bone_chains", text = 'All Bone Chains')
		row = layout.row()
		col = row.column(align=True)
		grid = col.grid_flow(align=True)
		row = grid.row(align=True)
		row.label(text='Rigid Body Create:',icon='RIGID_BODY')
		#row.operator('mmd_tools.rigid_body_add', text='From Selected Bones')
		row = grid.row(align=True)
		row.operator('ffxiv_mmd.create_rigid_bodies', text='From Selected Bones')
		row = grid.row(align=True)
		row.operator("ffxiv_mmd.create_rigid_bodies_from_csv", text = "From FFXIV Template")

		

		
		

@register_wrap
class JointsPanel_MTH(bpy.types.Panel):
	#Joints panel#
	bl_label = "Joints"
	bl_idname = "OBJECT_PT_JointsPanel_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_order = 4

	def draw(self, context):
		root = model.findRoot(context.object)

		layout = self.layout
			
		row = layout.row()
		col = row.column()
		grid = col.grid_flow(align=True,columns=3)
		if model.findRoot(bpy.context.object) is not None:
			grid.prop(root.mmd_root,"show_joints", toggle=True, text='',icon_only=True,icon='HIDE_OFF' if root.mmd_root.show_joints else 'HIDE_ON' )
			grid.prop(root.mmd_root,"show_names_of_joints", toggle=True, text='',icon_only=True,icon='SORTALPHA')
		grid.label(text="Joint Visibility")
		row = layout.row()
		col = row.column()
		grid = col.grid_flow(align=True,columns=3)
		grid.label(text="Active Joint: ")
		grid.label(text='Rigid 1: ')	
		grid.label(text='Rigid 2: ')	
		grid = col.grid_flow(align=True,columns=4)
		if(context.active_object):
			if context.active_object.mmd_type == 'JOINT':
				grid.prop(context.active_object,"name",text="")	
				grid.operator("ffxiv_mmd.select_rigid_body_from_joint",text=context.active_object.rigid_body_constraint.object1.name).rigid_number = '1'
				grid.operator("ffxiv_mmd.select_rigid_body_from_joint",text=context.active_object.rigid_body_constraint.object2.name).rigid_number = '2'
			else:
				grid.label(text='Select a Joint')
		row = layout.row()
		col = row.column()
		row = col.row(align=True)
		grid = row.grid_flow(align=True)
		grid.operator("ffxiv_mmd.select_joints_from_rigid_bodies", text = 'Get Joints from Rigid Bodies')
		row = col.row(align=True)
		grid = row.grid_flow(align=True,columns=2)
		grid.operator("ffxiv_mmd.select_vertical_horizontal_joints", text = 'Vertical', icon="SORT_DESC").direction='VERTICAL'
		grid.operator("ffxiv_mmd.select_vertical_horizontal_joints", text = 'Horizontal', icon="CENTER_ONLY").direction='HORIZONTAL'
		
		row = layout.row()
		row.label(text="Joint Transform:", icon='CON_CLAMPTO')
		row = layout.row()
		grid = row.grid_flow(align=True,columns=1)
		grid.operator("ffxiv_mmd.batch_update_joints", text = 'Bulk Apply')
		row = layout.row()
		col = layout.column()
		row.label(text='Joint Create:',icon='PIVOT_MEDIAN')
		#row.operator('mmd_tools.joint_add', text='From Selected Rigid Bodies')	
		row = layout.row()
		col = row.column(align=True)
		grid = col.grid_flow(align=True)
		row = grid.row(align=True)
		row.operator('ffxiv_mmd.create_joints', text='From Selected Rigid Bodies')	
		row = grid.row(align=True)
		row.operator("ffxiv_mmd.create_joints_from_csv", text = "From FFXIV Template")
		#row = layout.row()
		#col = layout.column()
		#grid = row.grid_flow(row_major=True,align=True,columns=1)
		row = grid.row(align=True)
		col = row.grid_flow(align=True,columns=2)
		#grid.label(text='Vertical',icon='EMPTY_SINGLE_ARROW')
		col.operator("ffxiv_mmd.batch_create_vertical_joints", text = "Bulk Vertical",icon='EMPTY_SINGLE_ARROW')
		col.prop(context.scene, "vertical_joint_pin", text="Pin",expand=True)
		#col = layout.column()
		#grid = row.grid_flow(row_major=True,align=True,columns=1)
		row = grid.row(align=True)
		#grid.label(text='Horizontal',icon='CENTER_ONLY')
		grid.operator("ffxiv_mmd.batch_create_horizontal_joints", text = "Bulk Horizontal",icon='CENTER_ONLY')
		#grid.prop(context.scene, "bones_all_or_selected",text='Wrap Around')

		
				

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
		#bone morphs ########################################
		row = layout.row()
		col = layout.column(align=True)
		grid = col.grid_flow(row_major=True)
		row = grid.row(align=True)
		row.prop(context.scene, "bone_morph_ffxiv_model_list")
		row.operator("ffxiv_mmd.add_bone_morphs", text = "Generate",icon='SHAPEKEY_DATA')
		row.operator("ffxiv_mmd.open_bone_morphs_file", text="",icon='CURRENT_FILE')
		#shape keys ########################################
		#row = layout.row()
		#col = layout.column(align=True)
		#grid = col.grid_flow(row_major=True)
		#row = grid.row(align=True)
		##row.prop(context.scene, "bone_morph_ffxiv_model_list")
		#row.operator("ffxiv_mmd.add_shape_keys_btn", text = "Generate",icon='SHAPEKEY_DATA')
		#row.operator("ffxiv_mmd.open_shape_keys_file", text="",icon='CURRENT_FILE')
		####################################################

		#row = layout.row()
		#layout.prop(context.scene, "alternate_folder_cbx", text="Use Alternate Folder for CSVs (broken)")
		row = layout.row(align=True)
		col = row.column(align=True)
		col.column(align=True).prop(context.scene,'bone_morph_rotation_mode_list')
		col = row.column(align=True)
		col.column(align=True).operator("ffxiv_mmd.change_face_rotation_mode",text='Change Rotation Mode')
		#row = layout.row()
		#row.label(text='**TODO** Open Dictionary File')
		#row = layout.row()
		#row.label(text='**TODO** Restore Defaults')
		

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
		row.operator("ffxiv_mmd.generate_skirt_modal", text = "Generate A New Skirt Object",icon='SHADERFX')
		row = layout.row()
		row.operator("ffxiv_mmd.move_mesh_to_new_skirt_btn", text = "Move Mesh To New Skirt Object",icon='PASTEDOWN')
		row = layout.row()
		row.operator("ffxiv_mmd.weight_paint_transfer_to_mesh_btn", text = "Weight Paint Transfer To Mesh",icon='MOD_VERTEX_WEIGHT')
		row = layout.row()
		row.operator("ffxiv_mmd.delete_ffxiv_skirt_vertex_groups", text = "Delete FFXIV & Unused Skirt Vertex Groups",icon='GPBRUSH_ERASE_HARD')
		row = layout.row()
		row.operator("ffxiv_mmd.merge_bones_and_meshes_to_ffxiv_model", text = "Merge Bones And Meshes To Armature",icon='AUTOMERGE_ON')
		row = layout.row()
		row.operator("ffxiv_mmd.generate_skirt_rigid_bodies", text = "Generate Skirt Rigid Bodies",icon='RIGID_BODY')
		row = layout.row()
		row.operator("ffxiv_mmd.generate_skirt_joints", text = "Generate Skirt Joints",icon='RIGID_BODY_CONSTRAINT')
		row = layout.row()
		row.template_list("MESH_UL_vgroups", "list", context.object, "vertex_groups", context.object.vertex_groups, "active_index")
		
		

		
"""		
@register_wrap
class CameraLightingPanel_MTH(bpy.types.Panel):
	bl_label = "Camera and Lighting"
	bl_idname = "OBJECT_PT_CameraLightingPanel_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"value
	bl_category = "FFXIV MMD"
	bl_options = {'DEFAULT_CLOSED'}
	bl_order = 7

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.operator("ffxiv_mmd.mmd_light_setup", text = "Add MMD light (broken)", icon="LIGHT")
		row = layout.row()
		row.operator("ffxiv_mmd.mmd_camera_to_blender_camera", text = "Convert MMD cameras to Blender cameras", icon="CAMERA_DATA")
		row = layout.row()
		row.operator("ffxiv_mmd.background_color_picker", text = "MMD background color picker", icon="COLOR")
		layout.prop(context.scene, "BackgroundColor")
		row = layout.row()
"""
@register_wrap
class ShadingAndToonsPanel_MTH(bpy.types.Panel):
	#User can modify the rendering of toon texture color
	bl_idname = "OBJECT_PT_ShadingAndToonsPanel_MTH"
	bl_label = "Shaders"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_options = {'DEFAULT_CLOSED'}
	bl_order = 8

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="Texture Folder:")
		row = layout.row()
		row.prop(context.scene,"shaders_texture_folder", text = "")
		row = layout.row()
		row.operator("ffxiv_mmd.select_materials_folder", text="Apply Colorset")
		row = layout.row()
		if context.active_object:
			row.prop(context.active_object, "active_material",text="Material")
		row = layout.row()
		row.operator("ffxiv_mmd.apply_glossy_shader", text="Apply Glossy Shader")
		row = layout.row()
		if context.active_object and context.active_object.type == 'MESH':
			active_object = bpy.context.active_object
			active_material = active_object.active_material if active_object else None

			if active_material and active_material.use_nodes:
				node_tree = active_material.node_tree
				glossy_bsdf_node = None

				# Find the Glossy BSDF node
				for node in node_tree.nodes:
					if node.type == 'BSDF_GLOSSY':
						glossy_bsdf_node = node

				if glossy_bsdf_node:
					row.prop(glossy_bsdf_node.inputs[1], "default_value", text="Glossiness")


		
		
		"""
		row = layout.row()
		row.operator("ffxiv_mmd.fix_normal_maps", text="Fix Normal Maps")
		
		row = layout.row()
		row.label(text="FFXIV Colorset Editor", icon="MATERIAL")
		row = layout.row()
		if(context.object.active_material):
			if(context.object.active_material.is_colorset):
				normal = context.object.active_material.node_tree.nodes['Normal']
				multi = context.object.active_material.node_tree.nodes['Multi']
				normal_closest = context.object.active_material.node_tree.nodes['Normal.001']
				
				row = layout.row()
				row.operator("import.colorsetdds")
				row.operator("export.colorsetdds")
				layout.label(text="Multi Map")
				row = layout.row()
				row.template_ID(multi, 'image', open="image.open")
				layout.label(text="Normal Map")
				row = layout.row()
				row.template_ID(normal, 'image', open="image.open")
				layout.label(text="Normal Map (Closest)")
				row = layout.row()
				row.template_ID(normal_closest, 'image', open="image.open")

			else:
				row = layout.row()
				row.operator("object.add_cs_material", text="Add")
		row = layout.row()
		"""

		"""
		row.label(text="MMD Render toon textures (broken)", icon="MATERIAL")
		row = layout.row()
		row.operator("ffxiv_mmd.mmd_toon_render_node_editor", text = "MMD Create Toon Material Nodes (broken)",icon='MATERIAL')
		row = layout.row()
		
		row.label(text="MMD Toon modifier (broken)", icon='NODE_MATERIAL')
		layout.prop(context.scene, "ToonModifierBlendType")
		row = layout.row()
		layout.prop(context.scene, "ToonModifierColor")
		row = layout.row()
		row.operator("ffxiv_mmd.toon_modifier", text = "Modify Toon (broken)",icon='NODE_MATERIAL')
		"""



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
		split.operator("ffxiv_mmd.miscellaneous_tools", text = "Run", icon='ORIENTATION_NORMAL')
		row = layout.row()
		row.prop(context.scene,"bust_slider",slider=True)
		row.operator("ffxiv_mmd.bust_slider",text='Run')

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
		row = layout.row()
		row.operator("ffxiv_mmd.auto_fix_mmd_bone_names",text="Auto-Fix MMD Japanese/English Bone Names", icon="GROUP_BONE") #so that they don't show up as "NULL" in MMD
		row = layout.row(align=True)
		col = row.column(align=True)
		col.operator("ffxiv_mmd.add_display_panel_groups", text = "Add Display Panels", icon="LONGDISPLAY")
		col = row.column(align=True)
		col.prop (context.scene, "mmd_display_panel_options")
		row.separator()
		row = layout.row()
		row.operator("ffxiv_mmd.sort_mmd_bone_order", text = "Sort Bone Order/Deform Tiers", icon="MOD_ARRAY") #Set bone order & deformation tiers
		row = layout.row()
		row.operator("ffxiv_mmd.lock_position_rotation_bones",text="Lock Position & Rotation", icon="LOCKED") 
		row = layout.row()
		row.operator("ffxiv_mmd.set_fixed_axis_local_axis_bones",text="Set Fixed Axis/Local Axis", icon="EMPTY_AXIS") 
		row = layout.row()
		row.operator("ffxiv_mmd.hide_special_bones", text = "Hide Special & Physics Bones", icon="HIDE_ON") #FFXIV stock face deformation shape keys (anything that starts with 'shp'), Physics Bones (Hair/Skirt/Armor/etc), Leg bones (after physics has been applied since the control bones should be used instead)		
		row = layout.row()
		row.label(text="**TODO** Edit Metadata Dictionary File", icon="CURRENT_FILE") 
		row = layout.row()
		row.label(text="**TODO** Restore Metadata Dictionary Defaults", icon="FILE_TICK") 
		
		"""
		row = layout.row(align=True)
		col = row.column(align=True)
		col.operator("ffxiv_mmd.armature_diagnostic", text = "Diagnose Armature (broken)",icon='ORPHAN_DATA')
		col = row.column(align=True)
		col.prop(context.scene, "selected_armature_to_diagnose")
		row = layout.row()
		"""

