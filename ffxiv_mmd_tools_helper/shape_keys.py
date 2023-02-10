import bpy
import math
from . import register_wrap
from . import import_csv

def get_meshes_of_armature (armature):
	bpy.ops.object.mode_set(mode='OBJECT')
	#Loop through all the objects, if it is a mesh, select it
	armature_parent = armature.parent
	# Deselect all objects
	bpy.ops.object.select_all(action='DESELECT')
	for ob in armature_parent.children_recursive:
		if ob.type=='MESH':
			ob.select_set(True)
		else:
			ob.select_set(False)

	return bpy.context.selected_objects


def save_rest_position(armature):

	# Create a dictionary to store the original pose bone data
	original_pose_data = {}

	# Set the pose mode
	bpy.context.view_layer.objects.active = armature
	bpy.ops.object.mode_set(mode='POSE')

	# Store the original positional data of the bones
	for pbone in armature.pose.bones:
		original_pose_data[pbone.name] = { \
			'location': pbone.location.copy(), \
			'rotation_mode': pbone.rotation_mode, \
			'rotation_euler': pbone.rotation_euler.copy() if pbone.rotation_mode=='XYZ' else None, \
			'rotation_quaternion': pbone.rotation_quaternion.copy() if pbone.rotation_mode!='XYZ' else None, \
			'scale': pbone.scale.copy() \
		}
	return original_pose_data


def load_rest_position(original_pose_data, armature):

	# Set the pose mode
	bpy.context.view_layer.objects.active = armature
	bpy.ops.object.mode_set(mode='POSE')

	# Iterate over the stored pose data and apply it back to the bones
	for pbone_name, data in original_pose_data.items():
		pbone = armature.pose.bones[pbone_name]
		pbone.location = data['location']
		pbone.rotation_mode = data['rotation_mode']
		if data['rotation_mode'] == 'QUATERNION':
			pbone.rotation_quaternion = data['rotation_quaternion']
		else:
			pbone.rotation_euler = data['rotation_euler']
		pbone.scale = data['scale']

def transform_pose_bone (armature,pbone_name,delta_coords):
	
	# Set the pose mode
	bpy.context.view_layer.objects.active = armature
	bpy.ops.object.mode_set(mode='POSE')
	pbone = armature.pose.bones[pbone_name]
	#if pose bone is quaternion, convert to XYZ euler first (not sure if I should use this yet)
	quaternion_flag = False
	if pbone.rotation_mode == 'QUATERNION' :
		quaternion_flag = True
		#Change the rotation mode to XYZ Euler
		pbone.rotation_mode = 'XYZ'

	# pbone.location[[0],[1],[2]] = location x,y,z
	# pbone.rotation_euler[[0],[1],[2] = rotation x, y, z (in euler)
	curr_coords = \
		[pbone.location[0] 
		,pbone.location[1] 
		,pbone.location[2] 
		,pbone.rotation_euler[0] 
		,pbone.rotation_euler[1] 
		,pbone.rotation_euler[2] 
		,pbone.scale[0] 
		,pbone.scale[1] 
		,pbone.scale[2] 
		] 
		
	#Data-cleanup and conversion
	#if the value on delta is None or '', set the value to 0
	delta_coords = [None if x == '' else x for x in delta_coords]
	delta_coords = [val if val is not None else 0 for val in delta_coords]
	#convert all strings to float
	delta_coords = [float(x) for x in delta_coords]

	new_coords = \
		[curr_coords[0] + delta_coords[0] 
		,curr_coords[1] + delta_coords[1] 
		,curr_coords[2] + delta_coords[2] 
		,curr_coords[3] + math.radians(delta_coords[3]) 
		,curr_coords[4] + math.radians(delta_coords[4]) 
		,curr_coords[5] + math.radians(delta_coords[5]) 
		,curr_coords[6] + delta_coords[6] 
		,curr_coords[7] + delta_coords[7] 
		,curr_coords[8] + delta_coords[8] 
		]
	pbone.location = [new_coords[0],new_coords[1],new_coords[2]]
	pbone.rotation_euler = [new_coords[3],new_coords[4],new_coords[5]]
	pbone.scale = [new_coords[6],new_coords[7],new_coords[8]]

	if quaternion_flag == True:
		pbone.rotation_mode = 'QUATERNION'


def create_shape_key (armature,shape_key_name,shape_key_bones_data):
	
	bpy.ops.object.mode_set(mode='POSE')

	#save the rest position before making any changes
	rest_position = save_rest_position(armature)

	#if a shape key exists with the same name, delete it first
	for mesh in get_meshes_of_armature(armature):
		bpy.ops.object.mode_set(mode='POSE')
		if mesh.data.shape_keys:
			if shape_key_name in mesh.data.shape_keys.key_blocks:
				existing_shape_key = mesh.data.shape_keys.key_blocks[shape_key_name]
				mesh.shape_key_remove(existing_shape_key)
				print(f"Shape key {shape_key_name} removed from {mesh.name}")

	i = 0
	
	#transform the bones according to the data provided
	for bone in shape_key_bones_data:
		#check if bone from shape_key_bones_data exists on the armature.
		exists = armature.pose.bones.get(bone[0]) is not None
		if exists :
			delta_coords = [bone[1],bone[2],bone[3],bone[4],bone[5],bone[6],bone[7],bone[8],bone[9]]
			transform_pose_bone(armature,bone[0],delta_coords)
			i += 1
		else:
			print( "shape_key: '" + shape_key_name + "', armature: '" + armature.name + "', bone: '" + bone[0] + "' doesn't exist" )
	
	bpy.ops.object.mode_set(mode='OBJECT')

	if i != 0:
		#Loop through all the objects, if it is a mesh, select it
		armature_parent = armature.parent
		# Deselect all objects
		bpy.ops.object.select_all(action='DESELECT')
		for ob in armature_parent.children_recursive:
			if ob.type=='MESH':
				vertex_group_names = [group.name for group in ob.vertex_groups]
				#loop through all the vertex groups on the mesh
				for vg in vertex_group_names:
					#loop through all the bones
					#if a vertex group name matches a bone name, shape key will be applied to this mesh
					#this is to prevent the shape key being applied to a mesh that has nothing to do with any of the bones that were just transformed
					for bone in shape_key_bones_data:
						if bone[0] == vg:
							#print ("\n\n\nhuzzah we have a match!")
							ob.select_set(True)
			else:
				ob.select_set(False)

		if (bpy.context.selected_objects):
			bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
			obj = bpy.context.active_object

			# Create a new Armature modifier
			mod = obj.modifiers.new(name=shape_key_name, type='ARMATURE')

			# Assign the armature object
			mod.object = armature

			# Apply the modifier as a shape key
			bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=False, modifier=mod.name, report=False)
			
			print( "shape_key: '" + shape_key_name + "' created on " + obj.name )
		else:
			print( "shape_key: '" + shape_key_name + "' was not applied at all" )	

	else:
		print( "shape_key: '" + shape_key_name + "' was not applied at all" )

	#restore the rest position back to it's original shape
	load_rest_position(rest_position, armature)
	bpy.ops.object.mode_set(mode='OBJECT')


def parse_shape_key_data_from_csv (csv_data):
	shape_key_dictionary = None
	
	# Create an empty dictionary
	shape_key_dictionary = {}

	for shape_key_bone_data in csv_data:
		
		#group the data based on the first row(shape key name)
		shape_key = shape_key_bone_data[0]
		
		#if the shape_key does not exist in the dictionary yet, create a new list for it
		if shape_key not in shape_key_dictionary:
			shape_key_dictionary[shape_key] = []
			
		#add the row to the dictionary
		shape_key_dictionary[shape_key].append(shape_key_bone_data)

	# Iterate through the values of each row and parse out the first column (shape_key) 
	# because we don't want to pass that as part of the bone data in the following step
	for shape_key in shape_key_dictionary:
		bone_data = shape_key_dictionary[shape_key]
		for i, j in enumerate(bone_data):
			bone_data[i] = j[1:]
			
	return shape_key_dictionary

def read_shape_keys_file(ffxiv_race):

	SHAPE_KEYS_DICTIONARY = None
	SHAPE_KEYS_DICTIONARY = import_csv.use_csv_shape_keys_dictionary(ffxiv_race)

	return SHAPE_KEYS_DICTIONARY

def clear_all_transformations(armature):
	
	# Get the active object
	obj = bpy.context.object

	if bpy.context.object.mode == 'POSE':

		# Select all pose bones
		for bone in armature.pose.bones:
			bone.bone.select = True

		# Clear all transformations of the selected bones
		for bone in armature.pose.bones:
			bone.location = [0, 0, 0]
			bone.rotation_euler = [0, 0, 0]
			bone.scale = [1, 1, 1]
	else:
		print(f"{obj.name} is not in pose mode, please switch to pose mode")

	#Reset all shape keys to 0
	for shape_key in bpy.data.shape_keys:
		for key_block in shape_key.key_blocks:
			key_block.value = 0
	

def switch_to_data_properties_menu():

	# Select the active object's mesh
	obj = bpy.context.object
	bpy.ops.object.mode_set(mode='OBJECT')
	obj.select_set(True)
	bpy.context.view_layer.objects.active = obj

	# Switch to the 'properties' menu
	bpy.context.area.type = 'PROPERTIES'
	# set the active context to 'DATA'
	bpy.context.area.spaces.active.context = 'DATA'

def main(context):
	armature = bpy.context.active_object #model.find_MMD_Armature(bpy.context.object)
	bpy.context.view_layer.objects.active = armature

	clear_all_transformations(armature)

	if bpy.context.scene.ffxiv_model_list == 'none':
		pass
	else:
		SHAPE_KEYS_DICTIONARY = read_shape_keys_file(bpy.context.scene.ffxiv_model_list)	
		shape_keys = parse_shape_key_data_from_csv(SHAPE_KEYS_DICTIONARY)
		for shape_key in shape_keys:
			create_shape_key(armature,shape_key,shape_keys[shape_key])



@register_wrap
class Shape_Keys(bpy.types.Operator):
	"""Shape Keys"""
	bl_idname = "ffxiv_mmd_tools_helper.add_shape_keys_btn"
	bl_label = "Import Shape Keys"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.ffxiv_model_list = bpy.props.EnumProperty(items = \
	[('none', 'none', 'none')\
	, ("hyur", "Import Hyur (Human) Shape Keys","Import Hyur Shape Keys") \
	, ("miquote", "Import Miquote Shape Keys","Import Miquote Shape Keys") \
	, ("viera", "Import Viera Shape Keys","Import Viera Shape Keys") \
	, ("aura", "Import Au Ra Shape Keys","Import Au Ra Shape Keys") \
	, ("hrothgar", "Import Hrothgar Shape Keys","Import Hrothgar Shape Keys") \
	, ("elezen", "Import Elezen Shape Keys","Import Elezen Shape Keys") \
	, ("roegadyn", "Import Roegadyn Shape Keys","Import Roegadyn Shape Keys") \
	, ("lalafell", "Import Lalafell Shape Keys","Import Lalafell Shape Keys") \
	], name = "FFXIV Race", default = 'hyur')
	
	bpy.types.Scene.alternate_folder_cbx = bpy.props.BoolProperty(name="Use Alternate Folder for CSVs", default=False)

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None #and obj.type == 'ARMATURE'

	def execute(self, context):
		main(context)
		return {'FINISHED'}