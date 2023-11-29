import bpy
import os
from . import register_wrap
from . import miscellaneous_tools
from . import bones_renamer
from . import add_foot_leg_ik
from bpy.props import StringProperty



def get_test_model_file_path(ffxiv_model):

	file_path = (__file__ + "\\assets\\ffxiv_models\\" + ffxiv_model + "\\" + ffxiv_model + ".fbx").replace("import_ffxiv_model.py" , "")

	return file_path

def import_ffxiv_model(context,file_path):

	if bpy.context.mode != 'OBJECT':
		bpy.ops.object.mode_set(mode='OBJECT')

	#file_path = (__file__ + "\\ffxiv models\\" + ffxiv_model + "\\" + ffxiv_model + ".fbx").replace("import_ffxiv_model.py" , "")
	#print(file_path)
	#deselect all objects

	#sets the active collection to collection[0]
	# Make sure you have at least one collection in your scene before running this code
	collections = bpy.context.scene.collection.children

	if collections:
		bpy.context.window.view_layer.active_layer_collection = bpy.context.window.view_layer.layer_collection.children[collections[0].name]
	else:
		print("No collections found in the scene.")

	bpy.ops.object.select_all(action='DESELECT')
	
	bpy.ops.import_scene.fbx( \
		filepath = file_path \
		, global_scale = 1
		, primary_bone_axis='X' \
		, secondary_bone_axis='Y' \
		, use_manual_orientation=True \
		, axis_forward='Y' \
		, axis_up='Z'
	)
	
	
	armature = None
	
	if bpy.context.selected_objects:
		for i in bpy.context.selected_objects:
			if i.type =='ARMATURE':
				armature = i

	if armature:
		print (f"{armature.name}:{armature.type}")


		#####move all 'Group' objects to an empty object called 'FFXIV Junk'####
		# Get the selected object
		selected_obj = bpy.context.selected_objects[0] #should be n_root
		#print(f"{selected_obj}:{selected_obj.type}")
		selected_obj_parent = selected_obj.parent #should be imported object name (Nala V3)
		#print(f"{selected_obj_parent}:{selected_obj_parent.type}")

		bpy.context.view_layer.objects.active = selected_obj_parent

		#rotate the model 90 degrees on the x axis
		miscellaneous_tools.fix_object_axis()

		
		# Create a new empty object to store all the junk that comes from FFXIV
		bpy.ops.object.add(type='EMPTY', location=(0, 0, 0))
		new_empty = bpy.context.object
		new_empty.name = 'FFXIV Empty Groups'
		#print (new_empty)

		# Parent the new empty object to the selected object
		new_empty.parent = selected_obj_parent

		# Iterate through all children of the selected object
		for child in selected_obj_parent.children:
			# Check if the child object contains the substring 'Group' in its name
			if 'Group' in child.name:
				if len(child.children) == 0:
					# Parent the child object to the new empty object
					child.parent = new_empty
				
		#####move all 'Mesh-type' objects to an empty object called 'Mesh'####
		bpy.context.view_layer.objects.active = selected_obj
			
		"""		
		# Create a new empty object to store all the Mesh Objects
		bpy.ops.object.add(type='EMPTY', location=(0, 0, 0))
		new_empty = bpy.context.object
		new_empty.name = 'FFXIV Mesh'
		new_empty.parent = selected_obj

		# Iterate through all children of the selected object
		for child in selected_obj.children:
			# Check if the child object contains the substring 'Group' in its name
			if 'Part' in child.name:
				# Parent the child object to the new empty object
				child.parent = new_empty
		"""

		###### Fix the alpha blend mode so that all the textures can be viewed properly, and set backface culling to True ######
		mats = bpy.data.materials
		for mat in mats:
			mat.blend_method = 'HASHED'
			mat.use_backface_culling = True
		
		##### add the" mmd_bone_order_override" armature modifier to the FIRST mesh on n_root (as per the MMD Tools instructions)####
		# Get the first mesh object that is a child of the armature
		mesh = [child for child in armature.children if child.type == 'MESH'][0]

		mmd_bone_order_override_modifier = None

		for modifier in mesh.modifiers:
			if modifier.type == 'ARMATURE' and modifier.object.name in (armature.name,'mmd_bone_order_override'):
				mmd_bone_order_override_modifier = modifier
				mmd_bone_order_override_modifier.name = 'mmd_bone_order_override'
				break

		if mmd_bone_order_override_modifier == None:
			# Add the armature modifier to the mesh
			mmd_bone_order_override_modifier = mesh.modifiers.new(name="mmd_bone_order_override", type='ARMATURE')
			# Set the armature as the object to which the modifier applies
			mmd_bone_order_override_modifier.object = armature
		
		#set the last selected armature as the active object
		x = bpy.data.objects[armature.name]
		x.select_set(True)

		print(x.name + ' ' +x.type)

		#get name of the root object and add it as a custom property to the armature (needed becuase MMD moves the armature to a new root)
		if x.type=='ARMATURE':
			root = x.parent
			add_custom_property(x,'original_root_name',root.name)
	

		mesh_list = {}
		
		#loop through all the meshes and rename them to something human-readable
		if x.type =='ARMATURE':
			for obj in x.parent.children_recursive:
				if obj.type == 'MESH':
					add_custom_property(obj,'original_mesh_name',obj.name) 
					#print("renaming!" + obj.name)
					rename_ffxiv_mesh(obj)

					original_material_name = obj.data['original_material_name']
					model_type = obj.data['ModelType']
					material_type = obj.data['MaterialType']
					material_folder=''
					immediate_folder_name=''
					#if mesh doesn't exist on the mesh_list add to the mesh_list
					if original_material_name not in mesh_list:
						mesh_list[original_material_name] = (model_type,material_type,immediate_folder_name,material_folder,)

					#add the ModelRaceType to the root armature properties
					if obj.data['ModelType'] == 'Face':
						# Copy the custom property 'ModelRaceType' to the armature data
						add_custom_property(x,'ModelRaceType',obj.data['ModelRaceType'])
						add_custom_property(x,'Race',obj.data['Race'])
						add_custom_property(x,'Gender',obj.data['Gender'])
						if obj.data.get('Tribe') is not None:
							add_custom_property(x,'Tribe',obj.data['Tribe'])

		#loop through all the meshes and hide the reaper eyes
		if x.type =='ARMATURE':
			for obj in x.parent.children_recursive:
				if obj.type == 'MESH':
					if obj.data['MaterialType'] == 'f' and obj.data['MaterialMeshType'] == 'etc_b':
						obj.hide = True
						#print (f"reaper eyes:{obj.data['original_material_name']}")


					

		
		#loop through the armature and if there's any meshes that match the mesh_list, update custom properties and name
		if x.type =='ARMATURE':
			for obj in x.parent.children_recursive:
				if obj.type == 'MESH':
					
					if obj.data['original_material_name'] in mesh_list:
						matname= obj.data['original_material_name']
						if mesh_list[matname][3] != '':
							print(f"{obj.name}: {mesh_list[matname][0]},{mesh_list[matname][1]},{mesh_list[matname][2]},{mesh_list[matname][3]}")
		
							
							add_custom_property(obj,'ModelName',mesh_list[matname][2])
							add_custom_property(obj,'material_filepath', mesh_list[matname][3])

		#loop through all the bones and add the original bone local data to it as a custom property
		if x.type =='ARMATURE':
			for bone in armature.data.bones:
				add_original_bone_local_data(x,bone.name)
		
def add_original_bone_local_data(armature,bone_name):
	
	bone = None
	
	bone = armature.data.bones.get(bone_name)
	
	if bone:
		bone['original_head_local'] = bone.head_local
		bone['original_tail_local'] = bone.tail_local
		bone['original_matrix_local_0'] = bone.matrix_local[0]
		bone['original_matrix_local_1'] = bone.matrix_local[1]
		bone['original_matrix_local_2'] = bone.matrix_local[2]
		bone['original_matrix_local_3'] = bone.matrix_local[3]
	
	return
					
def add_custom_property(obj,prop_name,prop_value):
	
	obj.data[prop_name] = prop_value








def rename_ffxiv_mesh(obj):
	# Input string
	input_string = obj.name
	#input_string = "c0801h0105_hir Part 1.80"
	if obj.type =='MESH' and (input_string.startswith("c1") or input_string.startswith("c0")):
		# Define the lengths for each part
		part_lengths = [5, 1, 4, 1, 3, 1, 4,1,4]

		# Initialize variables to store the parsed parts
		parsed_parts = []

		# Loop through the parts and extract them
		start_index = 0
		for length in part_lengths:
			part = input_string[start_index:start_index + length]
			parsed_parts.append(part)
			start_index += length

		# Print the parsed parts
		#for i, part in enumerate(parsed_parts):
			#print(f"Part {i + 1}: {part}")
		
		#add mesh details as a custom property
		Model_ID = parsed_parts[0]+parsed_parts[1]+parsed_parts[2]+parsed_parts[3]+parsed_parts[4]
		add_custom_property(obj,'ModelID',Model_ID)
		add_custom_property(obj,'ModelRaceID',int(parsed_parts[0].lstrip('c')))
		add_custom_property(obj,'ModelNumberID',int(parsed_parts[2]))
		add_custom_property(obj,'ModelTypeID',parsed_parts[4])
		add_custom_property(obj,'MeshPartNumber',parsed_parts[8])
		original_material_name = obj.active_material.name.split('.')[0]
		add_custom_property(obj,'original_material_name',original_material_name)
		add_custom_property(obj,'MaterialType',original_material_name[8])
		original_material_mesh_type = ''
		for i,part in enumerate(original_material_name.split('_')):
			if i >= 2:
				original_material_mesh_type += part + '_'
				#print(part)
		add_custom_property(obj,'MaterialMeshType',original_material_mesh_type.rstrip('_'))
		add_custom_property(obj,'ModelName','')
		add_custom_property(obj,'material_filepath','')
			

		# Define the replacement dictionary
		race_dict = {
			"c0101": ("Hyur_Mid_M","Hyur","Masculine","Midlander"),
			"c0104": ("Hyur_Mid_M_NPC","Hyur","Masculine","Midlander"),
			"c0201": ("Hyur_Mid_F","Hyur","Feminine","Midlander"),
			"c0301": ("Hyur_Hig_M","Hyur","Masculine","Highlander"),
			"c0401": ("Hyur_Hig_F","Hyur","Feminine","Highlander"),
			"c0501": ("Elez_M","Elezen","Masculine",None),
			"c0601": ("Elez_F","Elezen","Feminine",None),
			"c0701": ("Miqo_M","Miqote","Masculine",None),
			"c0801": ("Miqo_F","Miqote","Feminine",None),
			"c0804": ("Miqo_F_NPC","Miqote","Feminine",None),
			"c0901": ("Roeg_M","Roegadyn","Masculine",None),
			"c1001": ("Roeg_F","Roegadyn","Femanine",None),
			"c1101": ("Lala_M","Lalafel","Masculine",None),
			"c1201": ("Lala_F","Lalafel","Feminine",None),
			"c1301": ("Aura_M","AuRa","Masculine",None),
			"c1401": ("Aura_F","AuRa","Feminine",None),
			"c1501": ("Hrot_M","Hrothgar","Masculine",None),
			"c1601": ("Hrot_F","Hrothgar","Feminine",None),
			"c1701": ("Vier_M","Viera","Masculine",None),
			"c1801": ("Vier_F","Viera","Feminine",None),
		}

		

		# Replace part 1 using the dictionary
		if parsed_parts[0] in race_dict:
			add_custom_property(obj,'ModelRaceType', race_dict[parsed_parts[0]][0])
			add_custom_property(obj,'Race', race_dict[parsed_parts[0]][1])
			add_custom_property(obj,'Gender', race_dict[parsed_parts[0]][2])
			if race_dict[parsed_parts[0]][3] is not None:
				add_custom_property(obj,'Tribe', race_dict[parsed_parts[0]][3])
			parsed_parts[0] = race_dict[parsed_parts[0]][0]

		

			
		part_dict = {    
			"wrs":"Wrists",
			"ear":"Earrings",
			"nek":"Neck",
			"rir":"RingL",
			"ril":"RingR",
			"dwn":"Legs",
			"met":"Head",
			"sho":"Feet",
			"glv":"Hands",
			"top":"Body",
			"fac":"Face",
			"hir":"Hair",
			"til":"Tail",
			"zer":"Ears",
		}

		# Replace part 5 using the dictionary
		if parsed_parts[4] in part_dict:
			parsed_parts[4] = part_dict[parsed_parts[4]]

		add_custom_property(obj,'ModelType',parsed_parts[4])

		# Print the parsed parts
		#for i, part in enumerate(parsed_parts):
			#print(f"Part {i + 1}: {part}")
		
		new_mesh_name = parsed_parts[4]+"-"+parsed_parts[1]+parsed_parts[2]+"-"+parsed_parts[8]+"-"+parsed_parts[0]
		if original_material_mesh_type != '':
			new_mesh_name += '-' + obj.data['MaterialType']  + '-' + obj.data['MaterialMeshType'] 

		obj.name = new_mesh_name


def main(context):

	import_ffxiv_model(context,get_test_model_file_path(bpy.context.scene.selected_ffxiv_test_model))


from bpy_extras.io_utils import ImportHelper
@register_wrap
class FFXIV_FileBrowserImportOperator(bpy.types.Operator, ImportHelper):
	"""Import a FFXIV .fbx Model File from TexTools"""
	bl_idname = "ffxiv_mmd.ffxiv_file_browser_operator"
	bl_label = "Import FFXIV .fbx File"
	bl_options = {'REGISTER', 'UNDO'}

	filename_ext = ".fbx"
	filter_glob: bpy.props.StringProperty(
		default="*.fbx",
		options={'HIDDEN'},
	)

	def execute(self, context):
		file = self.filepath
		# Add code here to process the selected file
		print (file)
		import_ffxiv_model(context,file)

		return {'FINISHED'}



@register_wrap
class ImportFFXIVModel(bpy.types.Operator):
	"""Import a sample FFXIV .fbx Model File (created from TexTools)"""
	bl_idname = "ffxiv_mmd.import_ffxiv_model"
	bl_label = "Import FFXIV Test Model"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.selected_ffxiv_test_model = bpy.props.EnumProperty(items = \
	[('none', 'none', 'none')\
	#, ("import_nala", "import_nala","import_nala") \
	#, ("import_nala_deluxe", "import_nala_deluxe","import_nala_deluxe") \
	, ("AuRa female", "AuRa female","AuRa female") \
	, ("Elezen Female", "Elezen Female","Elezen Female") \
	, ("Hrothgar Male", "Hrothgar Male","Hrothgar Male") \
	, ("Hyur Highlander Female", "Hyur Highlander Female","Hyur Highlander Female") \
	, ("Hyur Midlander Female", "Hyur Midlander Female","Hyur Midlander Female") \
	, ("Lalafell Female", "Lalafell Female","Lalafell Female") \
	, ("Miqote Female", "Miqote Female","Miqote Female") \
	, ("Roegadyn Female", "Roegadyn Female","Roegadyn Female") \
	, ("Viera Female", "Viera Female","Viera Female") \
	
	], name = "Sample", default = 'none')
	
	
	@classmethod
	def poll(cls, context):

		if context.scene.selected_ffxiv_test_model != 'none':	
			return True#context.active_object is not None
	
	def execute(self, context):
		main(context)
		return {'FINISHED'}
	

