import bpy
from . import register_wrap
from . import miscellaneous_tools
from . import bones_renamer
from . import add_foot_leg_ik
from bpy.props import StringProperty



def get_test_model_file_path(ffxiv_model):

	file_path = (__file__ + "\\ffxiv models\\" + ffxiv_model + "\\" + ffxiv_model + ".fbx").replace("import_ffxiv_model.py" , "")

	return file_path

def import_ffxiv_model(file_path):

	#file_path = (__file__ + "\\ffxiv models\\" + ffxiv_model + "\\" + ffxiv_model + ".fbx").replace("import_ffxiv_model.py" , "")
	#print(file_path)
	#deselect all objects
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

		###### Fix the alpha blend mode so that all the textures can be viewed properly ######
		mats = bpy.data.materials
		for mat in mats:
			mat.blend_method = 'HASHED'
		
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



		
		#loop through all the meshes and rename them to something human-readable
		if x.type =='ARMATURE':
			for obj in x.parent.children_recursive:
				if obj.type == 'MESH':
					add_custom_property(obj,'original_mesh_name',obj.name) 
					print("renaming!" + obj.name)
					rename_ffxiv_mesh(obj)
					
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
		for i, part in enumerate(parsed_parts):
			print(f"Part {i + 1}: {part}")
		
		#add mesh details as a custom property
		Model_ID = parsed_parts[0]+parsed_parts[1]+parsed_parts[2]+parsed_parts[3]+parsed_parts[4]
		add_custom_property(obj,'ModelID',Model_ID)
		add_custom_property(obj,'ModelRaceID',int(parsed_parts[0].lstrip('c')))
		add_custom_property(obj,'ModelNumberID',int(parsed_parts[2]))
		add_custom_property(obj,'ModelTypeID',parsed_parts[4])
		add_custom_property(obj,'MeshPartNumber',parsed_parts[8])
			
		# Define the replacement dictionary
		race_dict = {
			"c0101": "Hyur_Mid_M",
			"c0104": "Hyur_Mid_M_NPC",
			"c0201": "Hyur_Mid_F",
			"c0301": "Hyur_Hig_M",
			"c0401": "Hyur_Hig_F",
			"c0501": "Elez_M",
			"c0601": "Elez_F",
			"c0701": "Miqo_M",
			"c0801": "Miqo_F",
			"c0804": "Miqo_F_NPC",
			"c0901": "Roeg_M",
			"c1001": "Roeg_F",
			"c1101": "Lala_M",
			"c1201": "Lala_F",
			"c1301": "Aura_M",
			"c1401": "Aura_F",
			"c1501": "Hrot_M",
			"c1601": "Hrot_F",
			"c1701": "Vier_M",
			"c1801": "Vier_F",
		}

		

		# Replace part 1 using the dictionary
		if parsed_parts[0] in race_dict:
			parsed_parts[0] = race_dict[parsed_parts[0]]

		add_custom_property(obj,'ModelRaceType',parsed_parts[0])
			
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

		obj.name = new_mesh_name


def main(context):

	if bpy.context.scene.selected_ffxiv_test_model == "import_nala":
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		filepath='C:\\Users\\wikid\\OneDrive\\Documents\\TexTools\\Saved\\FullModel\\Nala V3\\Nala V3.fbx'
		import_ffxiv_model(filepath)

	elif bpy.context.scene.selected_ffxiv_test_model == "import_nala_deluxe":
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		filepath='C:\\Users\\wikid\\OneDrive\\Documents\\TexTools\\Saved\\FullModel\\Nala V3\\Nala V3.fbx'
		import_ffxiv_model(filepath)
		miscellaneous_tools.fix_object_axis()
		bones_renamer.main(context)
		miscellaneous_tools.correct_root_center()
		miscellaneous_tools.correct_groove()
		miscellaneous_tools.correct_waist()
		miscellaneous_tools.correct_waist_cancel()
		add_foot_leg_ik.main(context)
	else:
		import_ffxiv_model(get_test_model_file_path(bpy.context.scene.selected_ffxiv_test_model))


from bpy_extras.io_utils import ImportHelper
@register_wrap
class FFXIV_FileBrowserImportOperator(bpy.types.Operator, ImportHelper):
	"""Operator that opens the file browser dialog"""
	bl_idname = "ffxiv_mmd.ffxiv_file_browser_operator"
	bl_label = "File Browser Operator"
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
		import_ffxiv_model(file)

		return {'FINISHED'}



@register_wrap
class ImportFFXIVModel(bpy.types.Operator):
	"""Import FFXIV Test Model"""
	bl_idname = "ffxiv_mmd.import_ffxiv_model"
	bl_label = "Import FFXIV Test Model"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.selected_ffxiv_test_model = bpy.props.EnumProperty(items = \
	[('none', 'none', 'none')\
	, ("import_nala", "import_nala","import_nala") \
	, ("import_nala_deluxe", "import_nala_deluxe","import_nala_deluxe") \
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
	
	"""
	@classmethod
	def poll(cls, context):
		return context.active_object is not None
	"""
	def execute(self, context):
		main(context)
		return {'FINISHED'}