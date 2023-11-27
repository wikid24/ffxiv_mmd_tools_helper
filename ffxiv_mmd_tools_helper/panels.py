import bpy
from . import register_wrap
from . import model
from . import addon_preferences


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
		# Add a help button
		row = layout.row()
		row.operator("wm.url_open", text="Help / User Guide", icon='QUESTION').url = "https://github.com/wikid24/ffxiv_mmd_tools_helper/tree/master/documentation"
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
		row.label(text="TexTools 'Saved' Folder:")
		row = layout.row(align=True)
		row.prop(context.scene,"textools_saved_folder", text = "")
		row.operator("ffxiv_mmd.select_textools_saved_folder", text='', icon='FILE_FOLDER')
		#row.operator("ffxiv_mmd.textools_saved_folder", text="Select TexTools 'Saved' Folder")

		row = layout.row()
		row.label(text="Anamnesis .chara File:")
		row = layout.row()
		col = layout.column(align=True)
		grid = col.grid_flow(row_major=True, align=True)
		split = row.split(factor=0.5)
		grid.row(align=True).operator("ffxiv_mmd.read_ffxiv_chara_file_browser_operator", text="Read", icon='VIEWZOOM')
		grid.row(align=True).operator("ffxiv_mmd.apply_ffxiv_chara_file_browser_operator", text="Apply to Model", icon='IMPORT')
		row = layout.row()
		row.prop(context.scene,"color_skin", text='',icon_only=True,icon='OUTLINER_DATA_MESH')
		row.prop(context.scene,"color_hair", text='',icon_only=True,icon='OUTLINER_DATA_MESH')
		row.prop(context.scene,"color_hair_highlights", text='',icon_only=True,icon='OUTLINER_DATA_MESH')
		row.prop(context.scene,"color_tattoo_limbal", text='',icon_only=True,icon='OUTLINER_DATA_MESH')
		row.prop(context.scene,"color_eyes", text='',icon_only=True,icon='OUTLINER_DATA_MESH')
		row.prop(context.scene,"color_odd_eye", text='',icon_only=True,icon='OUTLINER_DATA_MESH')
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
		row.operator("ffxiv_mmd.merge_bones_and_meshes_to_ffxiv_model", text = "Merge Skirt Bones & Meshes To Armature",icon='AUTOMERGE_ON')
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

"""
@register_wrap
class ShadingAndToonsPanel_MTH(bpy.types.Panel):
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
		if context.active_object:
			row.prop(context.active_object, "active_material",text="Material")
		row = layout.row()
		
		row = layout.row()
		grid = row.grid_flow(columns=1,align=True)
		
		
		row = layout.row()
		if context.active_object and context.active_object.type == 'MESH':
			active_object = bpy.context.active_object
			active_material = active_object.active_material if active_object else None


			if active_material and active_material.use_nodes:
				node_tree = active_material.node_tree
				glossy_bsdf_node = None
				mektools_skin_node = None
				mektools_eye_node = None
				colorsetter_gear_node = None
				colorsetter_eye_node = None
				colorsetter_hair_node = None
				colorsetter_face_node = None
				colorsetter_faceacc_node = None
				colorsetter_tail_node = None
				colorsetter_skin_node = None
				eye_catchlight_node = None
				eye_catchlight_mix_node = None

				mat_replace_shader_added = False

				
				for node in node_tree.nodes:
					
					if node.type == 'GROUP' and node.node_tree.name.startswith('FFXIV_Colorset Shader'):
						colorsetter_gear_node = node

					# Find the Glossy BSDF node
					if node.type == 'BSDF_GLOSSY' and node.name=='ffxiv_mmd_glossy':
						glossy_bsdf_node = node

					# Find the Colorsetter Eye Group node
					if node.type == 'GROUP' and node.name.startswith('colorsetter_eye_node_instance'):
						colorsetter_eye_node = node

					# Find the Colorsetter Hair Group node
					if node.type == 'GROUP' and node.name.startswith('colorsetter_hair_node_instance'):
						colorsetter_hair_node = node

					# Find the Colorsetter Face Group node
					if node.type == 'GROUP' and node.name.startswith('colorsetter_face_node_instance'):
						colorsetter_face_node = node

					# Find the Colorsetter Face Accent Group node
					if node.type == 'GROUP' and node.name.startswith('colorsetter_faceacc_node_instance'):
						colorsetter_faceacc_node = node

					# Find the Colorsetter Tail Group node
					if node.type == 'GROUP' and node.name.startswith('colorsetter_tail_node_instance'):
						colorsetter_tail_node = node

					# Find the Colorsetter Skin Group node
					if node.type == 'GROUP' and node.name.startswith('colorsetter_skin_node_instance'):
						colorsetter_skin_node = node



					# Find the MekTools Skin Shader group node
					if node.type =='GROUP' and node.node_tree.name == 'FFXIV Skin Shader':
						#mektools_skin_node = context.active_object.active_material.node_tree.nodes['Group']
						mektools_skin_node = node 
						
					# Find the MekTools Eye Shader group node
					if node.type =='GROUP' and node.name.startswith('mektools_eye_node_group_instance'):
						#mektools_skin_node = context.active_object.active_material.node_tree.nodes['Group']
						mektools_eye_node = node 

					#find the Eye Catchlight nodes
					if node.type =='GROUP' and node.node_tree.name.startswith('ffxiv_mmd_eye_catchlight'):
						eye_catchlight_node = node
					if node.type == 'MIX_SHADER' and node.name == 'ffxiv_mmd_eye_catchlight_mix_shader':
						eye_catchlight_mix_node = node

						

				#Glossy BSDF panel
				if glossy_bsdf_node:
					row = layout.row()
					grid = row.grid_flow(columns=2,align=True)
					grid.prop(glossy_bsdf_node.inputs[1], "default_value", text="Glossy Roughness")
					grid.operator("ffxiv_mmd.remove_glossy_shader", text="", icon='X')
				else:
					row = layout.row()
					row.operator("ffxiv_mmd.apply_glossy_shader", text="Add Glossy Shader")

				#Eye Catchlight panel
				if eye_catchlight_node:
					row = layout.row()
					grid.label(text="Eye Catchlight Settings")
					grid = row.grid_flow(columns=2,align=True)
					grid.prop(eye_catchlight_mix_node.inputs['Fac'], "default_value", text="Eye Catchlight Mix")
					grid.operator("ffxiv_mmd.remove_catchlight_shader", text="", icon='X')
				else:
					row = layout.row()
					row.operator("ffxiv_mmd.apply_catchlight_shader", text="Add Eye Catchlight Shader")

				
				#Colorsetter Gear panel
				if colorsetter_gear_node:
					colorsetter_gear_multi_node = colorsetter_gear_node.inputs['Multi Texture'].links[0].from_node
					colorsetter_gear_normal_node = colorsetter_gear_node.inputs['Normal Map'].links[0].from_node
					colorsetter_gear_normal_nearest_node = colorsetter_gear_node.inputs['Colorset Position Ramp'].links[0].from_node.inputs[0].links[0].from_node.inputs[0].links[0].from_node.inputs[0].links[0].from_node.inputs['Fac'].links[0].from_node
					colorsetter_gear_diffuse_node = colorsetter_gear_node.inputs['Diffuse Texture'].links[0].from_node
					colorsetter_gear_specular_node = colorsetter_gear_node.inputs['Specular Texture'].links[0].from_node
					colorsetter_gear_specular_mask_node = colorsetter_gear_node.inputs['Specular Mask Texture'].links[0].from_node

					if colorsetter_gear_multi_node:
						box = layout.box()
						grid = box.grid_flow(columns=2,align=True)
						grid.label(text="Colorsetter Gear Settings")
						grid.label(text="For MaterialType 'e' or 'a'")
						#grid.operator("ffxiv_mmd.remove_colorsetter_gear_shader", text="", icon='X')
						grid.operator("ffxiv_mmd.remove_colorsetter_shader", text="", icon='X').shader_type = 'gear'

						grid = box.grid_flow(columns=2,align=True)
						grid.prop(colorsetter_gear_multi_node,"image",text='Multi (_m,_d,_s)')
						grid.prop(colorsetter_gear_normal_node,"image",text='Normal (_n)')
						grid.prop(colorsetter_gear_normal_nearest_node,"image",text='Normal (Nearest)(_n)')
						grid.prop(colorsetter_gear_diffuse_node,"image",text='Diffuse (_d)')
						grid.prop(colorsetter_gear_specular_node,"image",text='Specular (_s)')
						grid.prop(colorsetter_gear_specular_mask_node,"image",text='Specular Mask')
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_gear_multi_node.name
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_gear_normal_node.name
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_gear_normal_nearest_node.name
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_gear_diffuse_node.name
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_gear_specular_node.name
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_gear_specular_mask_node.name
						grid = box.grid_flow(columns=1,align=True)
						grid.label(text="Replace Textures Folder")
						grid = box.grid_flow(columns=2,align=True)
						grid.prop(context.scene,"shaders_replacement_texture_folder",text='')
						grid.operator("ffxiv_mmd.replace_colorsetter_textures",text='',icon='CHECKMARK')


				#MekTools skin panel
				if mektools_skin_node:
					box = layout.box()
					grid = box.grid_flow(columns=2,align=True)
					grid.label(text="MekTools Skin Settings")
					grid.operator("ffxiv_mmd.remove_mektools_skin_shader", text="", icon='X')
					grid = box.grid_flow(columns=1,align=True)

					if 'SSS' in mektools_skin_node.node_tree.nodes:
						grid.prop(context.scene, "mektools_skin_prop_sss", text="Subsurface Scattering", slider=True)

					if 'Specular' in mektools_skin_node.node_tree.nodes:
						grid.prop(context.scene, "mektools_skin_prop_specular", text="Specular", slider=True)

					if 'Wet' in mektools_skin_node.node_tree.nodes:
						grid.prop(context.scene, "mektools_skin_prop_wet", text="Wet", slider=True)

					if 'Roughness' in mektools_skin_node.node_tree.nodes:
						grid.prop(context.scene, "mektools_skin_prop_roughness", text="Roughness", slider=True)	


				#MekTools Eye panel
				if mektools_eye_node:
					box = layout.box()
					grid = box.grid_flow(columns=2,align=True)
					grid.label(text="MekTools Eye Settings")
					grid.operator("ffxiv_mmd.remove_mektools_eye_shader", text="", icon='X')
					grid = box.grid_flow(columns=1,align=True)
					grid.prop(context.scene, "eye_shader_ffxiv_model_list")
					#grid.prop(mektools_eye_node.inputs["Eye Index"], "default_value", text="Eye Index")
					grid.prop(mektools_eye_node.inputs["Brightness"], "default_value", text="Brightness", slider=True)
					eye_index = mektools_eye_node.inputs["Eye Index"].default_value
					grid.prop(mektools_eye_node.inputs["Eye Color"], "default_value", text="Eye Color")
					if eye_index >= 11:
						grid.prop(mektools_eye_node.inputs["Custom Eye Image"], "default_value", text="Custom Eye Color")
					
					mektools_eye_specular_file = None
					mektools_eye_diffuse_file = None
					#print(eye_index)
					if eye_index >= 1 and eye_index < 2: #lalafell 1
						mektools_eye_diffuse_file = mektools_eye_node.node_tree.nodes["Image Texture.001"]
					elif eye_index >= 2 and eye_index <= 3: #lalafell 2
						mektools_eye_diffuse_file = mektools_eye_node.node_tree.nodes["Image Texture.002"]
					elif eye_index >= 3 and eye_index <= 4: #miqote 1
						mektools_eye_diffuse_file = mektools_eye_node.node_tree.nodes["Image Texture.005"]
					elif eye_index >= 4 and eye_index < 5: #miqote 2
						mektools_eye_diffuse_file = mektools_eye_node.node_tree.nodes["Image Texture.004"]
					elif eye_index >= 5 and eye_index < 6: #au ra
						mektools_eye_diffuse_file = mektools_eye_node.node_tree.nodes["Image Texture.006"]
					elif eye_index >= 6 and eye_index < 7: #viera
						mektools_eye_diffuse_file = mektools_eye_node.node_tree.nodes["Image Texture.008"]
					elif eye_index >= 7 and eye_index < 8: #hyur midlander
						mektools_eye_diffuse_file = mektools_eye_node.node_tree.nodes["Image Texture.019"]
					elif eye_index >= 8 and eye_index < 9: #hyur highlander
						mektools_eye_diffuse_file = mektools_eye_node.node_tree.nodes["Image Texture.020"]
					elif eye_index >= 9 and eye_index < 10: #elezen
						mektools_eye_diffuse_file = mektools_eye_node.node_tree.nodes["Image Texture"]
					elif eye_index >= 10 and eye_index < 11: #roegadyn
						mektools_eye_diffuse_file = mektools_eye_node.node_tree.nodes["Image Texture.003"]
					elif eye_index >= 11 and eye_index < 12: #hrothgar
						mektools_eye_diffuse_file = mektools_eye_node.node_tree.nodes["Image Texture.007"]
					if mektools_eye_specular_file:
						grid.prop(mektools_eye_specular_file,"image",text="Specular File")
					if mektools_eye_diffuse_file:
						grid.prop(mektools_eye_diffuse_file,"image",text="Diffuse File")
					grid.prop(mektools_eye_node.node_tree.nodes["Image Texture.011"],"image",text="Catchlight File")


				#Colorsetter Eye panel
				if colorsetter_eye_node:
					colorsetter_eye_color = colorsetter_eye_node.inputs['Eye Color']
					colorsetter_eye_odd_enabled = colorsetter_eye_node.inputs['Odd Eyes Enabled']
					colorsetter_eye_odd_color = colorsetter_eye_node.inputs['Odd Eye Color']
					colorsetter_eye_specular_decay = colorsetter_eye_node.inputs['Specular Decay']
					colorsetter_eye_multi_node = colorsetter_eye_node.inputs['Multi Texture'].links[0].from_node
					colorsetter_eye_normal_node = colorsetter_eye_node.inputs['Normal Texture'].links[0].from_node

					box = layout.box()
					grid = box.grid_flow(columns=2,align=True)
					grid.label(text="Colorsetter Eye Settings")
					grid.label(text="For materials that end with '_iri_a'")
					#grid.operator("ffxiv_mmd.remove_colorsetter_eye_shader", text="", icon='X')
					grid.operator("ffxiv_mmd.remove_colorsetter_shader", text="", icon='X').shader_type = 'eye'

					if colorsetter_eye_color:
						grid = box.grid_flow(columns=3,align=True)
						grid.prop(colorsetter_eye_color,"default_value",text='Eye Color')
						grid.prop(colorsetter_eye_odd_enabled,"default_value",text='Mix', slider=True)
						grid.prop(colorsetter_eye_odd_color,"default_value",text='Odd Eye Color')
						grid = box.grid_flow(columns=1,align=True)
						grid.prop(colorsetter_eye_specular_decay,"default_value",text='Specular Decay',slider=True)


						grid = box.grid_flow(columns=2,align=True)
						grid.prop(colorsetter_eye_multi_node,"image",text='Multi (iri_s)')
						grid.prop(colorsetter_eye_normal_node,"image",text='Normal (iri_n)')
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_eye_multi_node.name
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_eye_normal_node.name
						grid = box.grid_flow(columns=1,align=True)
						grid.prop(colorsetter_eye_node.node_tree.nodes['Normal Map'].inputs['Strength'],"default_value",text='Normal Strength',slider=True)



				#Colorsetter Hair panel
				if colorsetter_hair_node:
					colorsetter_hair_color = colorsetter_hair_node.inputs['Hair Color']
					colorsetter_hair_highlights_color = colorsetter_hair_node.inputs['Highlights Color']
					colorsetter_hair_highlights_enabled = colorsetter_hair_node.inputs['Enable Highlights']
					colorsetter_hair_anisotropy = colorsetter_hair_node.inputs['Disable Hair Anisotropy']
					colorsetter_hair_multi_node = colorsetter_hair_node.inputs['Multi Texture'].links[0].from_node
					colorsetter_hair_normal_node = colorsetter_hair_node.inputs['Normal Texture'].links[0].from_node

					box = layout.box()
					grid = box.grid_flow(columns=2,align=True)
					grid.label(text="Colorsetter Hair Settings")
					grid.label(text="For MaterialType 'h'")
					#grid.operator("ffxiv_mmd.remove_colorsetter_hair_shader", text="", icon='X')
					grid.operator("ffxiv_mmd.remove_colorsetter_shader", text="", icon='X').shader_type = 'hair'
					
					
					if colorsetter_hair_color:
						grid = box.grid_flow(columns=3,align=True)
						grid.prop(colorsetter_hair_color,"default_value",text='Hair Color')
						grid.prop(colorsetter_hair_highlights_enabled,"default_value",text='Mix', slider=True)
						grid.prop(colorsetter_hair_highlights_color,"default_value",text='Highlights Color')
						grid = box.grid_flow(columns=1,align=True)
						grid.prop(colorsetter_hair_anisotropy,"default_value",text='Anisotropy',slider=True)
					
						
						
						grid = box.grid_flow(columns=2,align=True)
						grid.prop(colorsetter_hair_multi_node,"image",text='Multi (hir_s)')
						grid.prop(colorsetter_hair_normal_node,"image",text='Normal (hir_n)')
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_hair_multi_node.name
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_hair_normal_node.name
							#grid.prop(colorsetter_eye_node.node_tree.nodes['Normal Map'].inputs['Strength'],"default_value",text='Normal Strength',slider=True)


				#Colorsetter Face panel
				if colorsetter_face_node:
					colorsetter_face_skin_color = colorsetter_face_node.inputs['Skin Color']
					colorsetter_face_sss = colorsetter_face_node.inputs['Enable SSS']
					colorsetter_face_lip_color_mix = colorsetter_face_node.inputs['Lip Color Enabled']
					colorsetter_face_lip_color = colorsetter_face_node.inputs['Lip Color']
					colorsetter_face_lip_lightdark = colorsetter_face_node.inputs['Light/Dark Lips']
					colorsetter_face_lip_brightness = colorsetter_face_node.inputs['Lip Brightness/Opacity']
					colorsetter_face_facepaint_mix = colorsetter_face_node.inputs['Face Paint Enabled']
					colorsetter_face_facepaint_color = colorsetter_face_node.inputs['Face Paint Color']
					colorsetter_face_facepaint_lightdark = colorsetter_face_node.inputs['Face Paint Light/Dark']
					colorsetter_face_facepaint_brightness = colorsetter_face_node.inputs['Face Paint Brightness/Opacity']
					
					colorsetter_face_diffuse_node = colorsetter_face_node.inputs['Diffuse Texture'].links[0].from_node
					colorsetter_face_facepaint_node = colorsetter_face_node.inputs['Face Paint Texture'].links[0].from_node
					colorsetter_face_multi_node = colorsetter_face_node.inputs['Multi Texture'].links[0].from_node
					colorsetter_face_normal_node = colorsetter_face_node.inputs['Normal Texture'].links[0].from_node

					box = layout.box()
					grid = box.grid_flow(columns=2,align=True)
					grid.label(text="Colorsetter Face Settings")
					grid.label(text="For materials that end with '_fac_a'")
					#grid.operator("ffxiv_mmd.remove_colorsetter_face_shader", text="", icon='X')
					grid.operator("ffxiv_mmd.remove_colorsetter_shader", text="", icon='X').shader_type='face'
					
					
					if colorsetter_face_skin_color:
						grid = box.grid_flow(columns=1,align=True)
						grid.prop(colorsetter_face_skin_color,"default_value",text='Skin Color')
						grid.prop(colorsetter_face_sss,"default_value",text='Subsurface Scattering', slider=True)
						grid.prop(colorsetter_face_lip_color,"default_value",text='Lip Color')
						grid.prop(colorsetter_face_lip_color_mix,"default_value",text='Lip Color Mix',slider=True)
						grid.prop(colorsetter_face_lip_lightdark,"default_value",text='Lip Light/Dark',slider=True)
						grid.prop(colorsetter_face_lip_brightness,"default_value",text='Lip Brightness/Opacity',slider=True)
						#grid.prop(colorsetter_face_facepaint_mix,"default_value",text='Facepaint Mix',slider=True)
						#grid.prop(colorsetter_face_facepaint_color,"default_value",text='Facepaint Color')
						#grid.prop(colorsetter_face_facepaint_lightdark,"default_value",text='Facepaint Light/Dark')
						#grid.prop(colorsetter_face_facepaint_brightness,"default_value",text='Facepaint Brightness/Opacity')
												
						
						grid = box.grid_flow(columns=2,align=True)
						grid.prop(colorsetter_face_diffuse_node,"image",text='Diffuse (fac_d)')
						grid.prop(colorsetter_face_multi_node,"image",text='Multi (fac_s)')
						grid.prop(colorsetter_face_normal_node,"image",text='Normal (fac_n)')
						#grid.prop(colorsetter_face_facepaint_node,"image",text='Facepaint')
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_face_diffuse_node.name
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_face_multi_node.name
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_face_normal_node.name
						#grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_face_facepaint_node.name
						

				#Colorsetter Face Accent panel
				if colorsetter_faceacc_node:
					colorsetter_faceacc_hair_color = colorsetter_faceacc_node.inputs['Hair Color']
					colorsetter_faceacc_hair_color_brighten = colorsetter_faceacc_node.inputs['Hair Color Brighten']
					colorsetter_faceacc_tattoo_color = colorsetter_faceacc_node.inputs['Tattoo Color']
					colorsetter_faceacc_limbal_color = colorsetter_faceacc_node.inputs['Limbal Ring Color']
					colorsetter_faceacc_limbal_mix = colorsetter_faceacc_node.inputs['Limbal Ring Enabled']
					colorsetter_faceacc_limbal_intensity = colorsetter_faceacc_node.inputs['Limbal Ring Intensity']
					colorsetter_faceacc_multi_node = colorsetter_faceacc_node.inputs['Multi Texture'].links[0].from_node
					colorsetter_faceacc_normal_node = colorsetter_faceacc_node.inputs['Normal Texture'].links[0].from_node

					box = layout.box()
					grid = box.grid_flow(columns=2,align=True)
					grid.label(text="Colorsetter Face Accent Settings")
					grid.label(text="For materials that end with '_etc_a'")
					#grid.operator("ffxiv_mmd.remove_colorsetter_faceacc_shader", text="", icon='X')
					grid.operator("ffxiv_mmd.remove_colorsetter_shader", text="", icon='X').shader_type = 'faceacc'
					
					
					if colorsetter_faceacc_hair_color:
						grid = box.grid_flow(columns=1,align=True)
						grid.prop(colorsetter_faceacc_hair_color,"default_value",text='Hair Color')
						grid.prop(colorsetter_faceacc_hair_color_brighten,"default_value",text='Mix', slider=True)
						grid.prop(colorsetter_faceacc_tattoo_color,"default_value",text='Tattoo Color')
						grid.prop(colorsetter_faceacc_limbal_color,"default_value",text='Limbal Ring Color')
						grid.prop(colorsetter_faceacc_limbal_mix,"default_value",text='Limbal Mix')
						grid.prop(colorsetter_faceacc_limbal_intensity,"default_value",text='Limbal Intensity')
						
						grid = box.grid_flow(columns=2,align=True)
						grid.prop(colorsetter_faceacc_multi_node,"image",text='Multi (_s)')
						grid.prop(colorsetter_faceacc_normal_node,"image",text='Normal (_n)')
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_faceacc_multi_node.name
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_faceacc_normal_node.name
							#grid.prop(colorsetter_eye_node.node_tree.nodes['Normal Map'].inputs['Strength'],"default_value",text='Normal Strength',slider=True)

				#Colorsetter Tail panel
				if colorsetter_tail_node:
					colorsetter_tail_hair_color = colorsetter_tail_node.inputs['Hair Color']
					colorsetter_tail_highlights_mix = colorsetter_tail_node.inputs['Enable Highlights']
					colorsetter_tail_highlights_color = colorsetter_tail_node.inputs['Highlight Color']
					colorsetter_tail_multi_node = colorsetter_tail_node.inputs['Multi Texture'].links[0].from_node
					colorsetter_tail_normal_node = colorsetter_tail_node.inputs['Normal Texture'].links[0].from_node
					

					box = layout.box()
					grid = box.grid_flow(columns=2,align=True)
					grid.label(text="Colorsetter Tail Settings")
					#grid.operator("ffxiv_mmd.remove_colorsetter_tail_shader", text="", icon='X')
					grid.operator("ffxiv_mmd.remove_colorsetter_shader", text="", icon='X').shader_type='tail'
					
					
					if colorsetter_tail_hair_color:
						grid = box.grid_flow(columns=1,align=True)
						grid.prop(colorsetter_tail_hair_color,"default_value",text='Hair Color')
						grid.prop(colorsetter_tail_highlights_color,"default_value",text='Highlight Color')
						grid.prop(colorsetter_tail_highlights_mix,"default_value",text='Highlight Mix')
						
						grid = box.grid_flow(columns=2,align=True)
						grid.prop(colorsetter_tail_multi_node,"image",text='Multi')
						grid.prop(colorsetter_tail_normal_node,"image",text='Normal')
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_tail_multi_node.name
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_tail_normal_node.name
							#grid.prop(colorsetter_eye_node.node_tree.nodes['Normal Map'].inputs['Strength'],"default_value",text='Normal Strength',slider=True)

				#Colorsetter Skin panel
				if colorsetter_skin_node:
					colorsetter_skin_color = colorsetter_skin_node.node_tree.nodes['Skin Tone'].inputs[6] #inputs['Skin Color']
					colorsetter_skin_sss = colorsetter_skin_node.inputs['Enable SSS']
					colorsetter_skin_diffuse_node = colorsetter_skin_node.node_tree.nodes['Diffuse Skin Texture'] #inputs['Diffuse Texture'].links[0].from_node
					colorsetter_skin_multi_node = colorsetter_skin_node.node_tree.nodes['Multi Skin Texture'] #inputs['Multi Texture'].links[0].from_node
					colorsetter_skin_normal_node = colorsetter_skin_node.node_tree.nodes['Normal Skin Texture'] #inputs['Normal Texture'].links[0].from_node
					

					box = layout.box()
					grid = box.grid_flow(columns=2,align=True)
					grid.label(text="Colorsetter Skin Settings")
					grid.label(text="For MaterialType 'b'")
					#grid.operator("ffxiv_mmd.remove_colorsetter_skin_shader", text="", icon='X')
					grid.operator("ffxiv_mmd.remove_colorsetter_shader", text="", icon='X').shader_type='skin'
					
					
					if colorsetter_skin_color:
						grid = box.grid_flow(columns=1,align=True)
						grid.prop(colorsetter_skin_color,"default_value",text='Skin Color')
						grid.prop(colorsetter_skin_sss,"default_value",text='Subsurface Scattering', slider=True)
						
						grid = box.grid_flow(columns=2,align=True)
						grid.prop(colorsetter_skin_diffuse_node,"image",text='Diffuse')
						grid.prop(colorsetter_skin_multi_node,"image",text='Multi')
						grid.prop(colorsetter_skin_normal_node,"image",text='Normal')
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_skin_diffuse_node.name
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_skin_multi_node.name
						grid.operator("ffxiv_mmd.update_colorsetter_image_node",text='',icon='FILEBROWSER').image_node_name = colorsetter_skin_normal_node.name
							#grid.prop(colorsetter_eye_node.node_tree.nodes['Normal Map'].inputs['Strength'],"default_value",text='Normal Strength',slider=True)


				
				if mektools_skin_node or mektools_eye_node or colorsetter_eye_node or colorsetter_hair_node or colorsetter_face_node or colorsetter_faceacc_node or colorsetter_tail_node or colorsetter_skin_node or colorsetter_gear_node:
						mat_replace_shader_added =True


				if 	mat_replace_shader_added == False:
				
					row = layout.row()
					row.label(text = 'Apply MekTools Shader')
					row = layout.row()
					grid = row.grid_flow(columns=2,align=True)
					grid.operator("ffxiv_mmd.apply_mektools_skin_shader", text="Skin")
					grid.operator("ffxiv_mmd.apply_mektools_eye_shader", text="Eyes")
					row = layout.row()
					row.label(text = 'Apply Colorsetter Shader')
					row = layout.row()
					grid = row.grid_flow(columns=2, align=True)
					grid.operator("ffxiv_mmd.apply_colorsetter_shader", text="Skin").shader_type = 'skin'
					grid.operator("ffxiv_mmd.apply_colorsetter_shader", text="Face").shader_type = 'face'
					grid.operator("ffxiv_mmd.apply_colorsetter_shader", text="Hair").shader_type = 'hair'
					grid.operator("ffxiv_mmd.apply_colorsetter_shader", text="Eyes").shader_type = 'eye'
					grid.operator("ffxiv_mmd.apply_colorsetter_shader", text="Face Accent").shader_type = 'faceacc'
					grid.operator("ffxiv_mmd.apply_colorsetter_shader", text="Hrothgar/Miqote Tail").shader_type = 'tail'
					# Colorsetter Addon Gear Stuff
					row = layout.row()
					row.label(text="Apply Colorsetter Gear Texture Folder:")
					row = layout.row()
					grid = row.grid_flow(columns=2,align=True)
					grid.prop(context.scene,"shaders_texture_folder", text = "")
					grid.operator("ffxiv_mmd.select_colorsetter_gear_materials_folder", text="", icon='CHECKMARK')
					


		# Background Color changer Stuff 
		row = layout.row()
		world_material = bpy.context.scene.world
		world_background_node = world_material.node_tree.nodes.get('ffxiv_mmd_background')
		if world_background_node:
			grid = row.grid_flow(columns=2,align=True)
			grid.prop(world_background_node.inputs[0],"default_value", text="Background Color")
			grid.operator("ffxiv_mmd.remove_world_background_color", text="", icon='X')
		else:
			row.operator("ffxiv_mmd.apply_world_background_color", text="Add Background Color")

		
		

@register_wrap
class FacePaint_MTH(bpy.types.Panel):
	bl_idname = "OBJECT_PT_FacePaintMMD_MTH"
	bl_label = "Decals / Face Paint"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_options = {'DEFAULT_CLOSED'}
	bl_order = 9

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		if context.active_object and context.active_object.type == 'MESH':
			active_object = bpy.context.active_object
			active_material = active_object.active_material if active_object else None

			if active_material and active_material.use_nodes:

				# Call the function for each decal
				for i in range(1, 5):  # Change 5 to the number of decals you want
					create_decal_controls(layout, i, active_material)		
		else:
			row.label(text='Select a Mesh')

def create_decal_controls(layout, decal_index, active_material):
	decal_node_instance = active_material.node_tree.nodes.get(f'ffxiv_mmd_decal_{decal_index}')
	
	if decal_node_instance:
		decal_group = bpy.data.node_groups.get(f'ffxiv_mmd_decal_{decal_index}')
		image_node = decal_group.nodes.get(f'ffxiv_mmd_decal_img_{decal_index}')
		
		box = layout.box()
		grid = box.grid_flow(columns=2, align=True)
		grid.label(text=f"Decal {decal_index}")
		grid.operator("ffxiv_mmd.remove_decal_layout", text="", icon='X').decal_slot_id = decal_index
		
		if image_node:
			grid = box.grid_flow(columns=2, align=True)
			grid.prop_search(image_node, "image", bpy.data, "images", text="Image")
			grid.operator('ffxiv_mmd.insert_image_decal', text='', icon='FILE_FOLDER').decal_slot_id = decal_index
			
			grid = box.grid_flow(columns=2, align=True)
			grid.prop(decal_node_instance.inputs["Base Color"], "default_value", text="Color")
			grid.prop(decal_node_instance.inputs["Alpha"], "default_value", text="Alpha")
			#grid.prop(decal_node_instance.inputs['Subsurface'], "default_value", text="Mix", slider=True)
			#grid.prop(decal_node_instance.inputs["Subsurface Color"], "default_value", text="Subsurface")
			
			grid = box.grid_flow(columns=2, align=True)
			grid.prop(decal_node_instance.inputs["Roughness"], "default_value", text="Roughness")
			grid.prop(decal_node_instance.inputs["Specular"], "default_value", text="Specular")
	else:
		row = layout.row()
		row.operator("ffxiv_mmd.create_decal_layout", text=f"Add Decal {decal_index}").decal_slot_id = decal_index

		

		


@register_wrap
class MiscellaneousToolsPanel_MTH(bpy.types.Panel):
	#Miscellaneous Tools panel
	bl_label = "Miscellaneous Tools"
	bl_idname = "OBJECT_PT_MiscellaneousToolsPanel_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_options = {'DEFAULT_CLOSED'}
	bl_order = 10

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="Misc Tools", icon='WORLD_DATA')
		row = layout.row()
		split = layout.split(factor=0.80,align=True)
		split.prop(context.scene, "selected_miscellaneous_tools")	
		split.operator("ffxiv_mmd.miscellaneous_tools", text = "Run", icon='ORIENTATION_NORMAL')
		row = layout.row(align=True)
		row.prop(context.scene,"bust_slider",text='FFXIV Bust Scale',slider=True)
		row.operator("ffxiv_mmd.bust_slider",text='',icon='CHECKMARK' )
		row = layout.row()
			
		#Rigify Metarig
		row = layout.row(align=True)
		col = row.column(align=True)
		col.label(text="Rigify", icon="OUTLINER_OB_ARMATURE")
		col = row.column(align=True)
		col.operator("ffxiv_mmd.add_rigify_metarig", text = "Add")
		col = row.column(align=True)
		col.operator("ffxiv_mmd.adjust_metarig_bones", text = "Fix Bones")
		col = row.column(align=True)
		col.operator("ffxiv_mmd.apply_metarig", text = "Apply")
		#Mektools Rig
		row = layout.row(align=True)
		col = row.column(align=True)
		col.label(text="MekTools Rig", icon="OUTLINER_OB_ARMATURE")
		col = row.column(align=True)
		col.operator("ffxiv_mmd.apply_mektools_rig", text = "Add MekTools Rig")


		# Bone Compare
		box = layout.box()
		box.label(text="Bone Compare", icon="CONSTRAINT_BONE")

		row = box.row()
		col = row.column(align=True)
		col.prop(context.scene, "bone_compare_source_armature", text="Source")
		col.prop(context.scene, "bone_compare_target_armature", text="Target")
		if context.scene.bone_compare_target_armature:
			col.prop_search(context.scene, "bone_compare_comparison_bone", context.scene.bone_compare_target_armature.id_data.pose, "bones", text="Bone")
		col = row.column(align=False)
		col.operator("ffxiv_mmd.bone_scale_comparison", text="", icon="UV_SYNC_SELECT")
		col.operator("ffxiv_mmd.bone_scale_comparison_select_target_bone",text="", icon="RESTRICT_SELECT_OFF")

		row = box.row(align=True)
		col = row.column(align=True)
		col.label(text="Copy Rotation")
		col = row.column(align=True)
		col.operator("ffxiv_mmd.rotate_target_pose_bone_to_source_bone", text='Source Bone').bone_rotate_search_by_mmd_english_name = True
		col = row.column(align=True)
		col.operator("ffxiv_mmd.rotate_target_armature_bones_to_source_armature", text='All Arm Bones').armature_rotate_search_by_mmd_english_name = True ##TESTING##

		# Bone Scale Comparison
		row = box.row(align=True)
		col = row.column(align=True)
		col.label(text='Scale')
		col = row.column(align=True)
		col.prop(context.scene, "bone_compare_scale_x", text="X")
		col = row.column(align=True)
		col.prop(context.scene, "bone_compare_scale_y", text="Y")
		col = row.column(align=True)
		col.prop(context.scene, "bone_compare_scale_z", text="Z")





@register_wrap
class ExportMMD_MTH(bpy.types.Panel):
	bl_idname = "OBJECT_PT_ExportMMD_MTH"
	bl_label = "Export MMD Preparation"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_options = {'DEFAULT_CLOSED'}
	bl_order = 11

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
		
		"""
		row = layout.row(align=True)
		col = row.column(align=True)
		col.operator("ffxiv_mmd.armature_diagnostic", text = "Diagnose Armature (broken)",icon='ORPHAN_DATA')
		col = row.column(align=True)
		col.prop(context.scene, "selected_armature_to_diagnose")
		row = layout.row()
		"""

@register_wrap
class TexToDDS_MTH(bpy.types.Panel):
	bl_idname = "OBJECT_PT_TexToDDS_MTH"
	bl_label = "Tex to DDS Converter"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "FFXIV MMD"
	bl_options = {'DEFAULT_CLOSED'}
	bl_order = 12

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text='Input Folder')
		row = layout.row()
		grid = row.grid_flow(columns=2, align=True)
		grid.prop(context.scene,"convert_input_file_folder",text='')
		grid.operator("ffxiv_mmd.select_convert_input_folder", icon='FILE_FOLDER', text='')
		row = layout.row()
		row.label(text='Output Folder')
		row = layout.row()
		grid = row.grid_flow(columns=2, align=True)
		grid.prop(context.scene,"convert_output_file_folder",text='')
		grid.operator("ffxiv_mmd.convert_open_output_folder", icon='FILE_FOLDER', text='')
		row = layout.row()
		grid = row.grid_flow(columns=1, align=True)
		row.operator("ffxiv_mmd.convert_tex_to_dds", text='Convert .tex to .dds')
		row.operator("ffxiv_mmd.convert_dds_to_tex", text='Convert .dds to .tex')
		row = layout.row()
		row.label(text='WARNING: This converts ALL subfolders as well')
		row = layout.row()
		row.label(text='THIS MAY TAKE A WHILE IF LOTS OF FILES/SUBFOLDERS')

