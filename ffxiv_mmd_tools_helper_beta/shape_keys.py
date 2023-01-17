import bpy
import math
import mathutils

from . import register_wrap
from . import model
from . import import_csv


@register_wrap
class ShapeKeysPanel(bpy.types.Panel):
	"""Add foot and leg IK bones and constraints to MMD model"""
	bl_idname = "OBJECT_PT_mmd_add_shape_keys"
	bl_label = "Add shape keys to FFXIV model"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="Add shape keys to FFXIV model", icon="ARMATURE_DATA")
		row = layout.row()
		layout.prop (context.scene, "ffxiv_model_list")
		row = layout.row()
		row.operator("object.add_shape_keys_btn", text = "Add shape keys to FFXIV model")
		row = layout.row()


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
			
		#set the selected objects as the active object
		#bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
		#obj = bpy.context.active_object
	return bpy.context.selected_objects



def save_rest_position(armature):

	# Create a dictionary to store the original pose bone data
	original_pose_data = {}

	# Set the pose mode
	bpy.context.view_layer.objects.active = armature
	bpy.ops.object.mode_set(mode='POSE')

	# Store the original positional data of the bones
	for pbone in bpy.context.object.pose.bones:
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

	# Set the pose mode
	bpy.ops.object.mode_set(mode='POSE')

	# Iterate over the stored pose data and apply it back to the bones
	for pbone_name, data in original_pose_data.items():
		pbone = bpy.context.object.pose.bones[pbone_name]
		pbone.location = data['location']
		pbone.rotation_mode = data['rotation_mode']
		if data['rotation_mode'] == 'XYZ':
			pbone.rotation_euler = data['rotation_euler']
		else:
			pbone.rotation_quaternion = data['rotation_quaternion']
		pbone.scale = data['scale']

def transform_pose_bone (armature,pbone_name,delta_coords):

	delta = delta_coords
	#if the value on delta is None or '', set the value to 0
	delta = [None if x == '' else x for x in delta]
	delta = [val if val is not None else 0 for val in delta]
	#convert all strings to float
	delta = [float(x) for x in delta]

	bpy.ops.object.mode_set(mode='POSE')
	pbone = armature.pose.bones[pbone_name]
	#if pose bone is quaternion, convert to XYZ euler first (not sure if I should use this yet)
	quaternion_flag = False
	if pbone.rotation_mode == 'QUATERNION' :
		quaternion_flag = True
		#Change the rotation mode to XYZ Euler
		pbone.rotation_mode = 'XYZ'
		"""
		# Get the current quaternion rotation value
		quat_rot = pbone.rotation_quaternion
		
		# Convert the quaternion rotation value to euler
		euler_rot = quat_rot.to_euler()
		
		# Set the euler rotation value to the bone
		pbone.rotation_euler = euler_rot
		"""


# pbone.location[0] location x
# pbone.location[1] location y
# pbone.location[2] location z
# pbone.rotation_euler[0] rotation x
# pbone.rotation_euler[1] rotation y
# pbone.rotation_euler[2] rotation z

	curr_coords = [pbone.location[0] \
					,pbone.location[1] \
					,pbone.location[2] \
					,pbone.rotation_euler[0] \
					,pbone.rotation_euler[1] \
					,pbone.rotation_euler[2] \
					] 

	new_coords = [curr_coords[0] + delta[0] \
					,curr_coords[1] + delta[1] \
					,curr_coords[2] + delta[2] \
					,curr_coords[3] + math.radians(delta[3]) \
					,curr_coords[4] + math.radians(delta[4]) \
					,curr_coords[5] + math.radians(delta[5]) \
					]
	pbone.location = [new_coords[0],new_coords[1],new_coords[2]]
	pbone.rotation_euler = [new_coords[3],new_coords[4],new_coords[5]]

	if quaternion_flag == True:
		pbone.rotation_mode = 'QUATERNION'

def get_armature():
	bpy.ops.object.mode_set(mode='OBJECT')

	armature = None

	# Get the selected object
	selected_object = bpy.context.object

	# Check if the selected object is a mesh object
	if selected_object.type == 'MESH':
		# Check if the selected object's parent is an armature object
		if selected_object.parent and selected_object.parent.type == 'ARMATURE':
			# Get the armature object
			armature = selected_object.parent      
			
		# Check if the selected object's grandparent is an armature object
		if selected_object.parent.parent and selected_object.parent.parent.type == 'ARMATURE':
			# Get the armature object
			armature = selected_object.parent.parent

	if selected_object.type == 'ARMATURE':
		armature = selected_object

	bpy.context.view_layer.objects.active = armature
	  
	return armature

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
			delta_coords = [bone[1],bone[2],bone[3],bone[4],bone[5],bone[6]]
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
				ob.select_set(True)
			else:
				ob.select_set(False)

		#set the selected objects as the active object
		bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
		obj = bpy.context.active_object

		# Create a new Armature modifier
		mod = obj.modifiers.new(name=shape_key_name, type='ARMATURE')

		# Assign the armature object
		mod.object = armature

		# Apply the modifier as a shape key
		bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=False, modifier=mod.name, report=False)
		
		print( "shape_key: '" + shape_key_name + "' created" )

	else:
		print( "shape_key: '" + shape_key_name + "' was not applied at all" )

	#restore the rest position back to it's original shape
	load_rest_position(rest_position, armature)
	bpy.ops.object.mode_set(mode='OBJECT')


def parse_shape_key_data_from_csv (csv_data):
	
	# Create an empty dictionary
	shape_key_dictionary = {}

	# Iterate through each row and 
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
			
	#for shape_key in shape_key_dictionary
	#create_shape_key(armature,shape_key,shape_key_dictionary[shape_key])
			
	return shape_key_dictionary



def read_shape_keys_file(ffxiv_race):
	#if test_is_mmd_english_armature() == True:
	#	bpy.ops.object.mode_set(mode='EDIT')
	SHAPE_KEYS_DICTIONARY = None
	#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
	SHAPE_KEYS_DICTIONARY = import_csv.use_csv_shape_keys_dictionary(ffxiv_race)


	#if test_is_mmd_english_armature() == False:
	#	print("This operator will only work on an armature with mmd_english bone names. First rename bones to mmd_english and then try running this operator again.")

	return SHAPE_KEYS_DICTIONARY

#applies the shape keys





"""

def apply_shape_keys(SHAPE_KEYS_DICTIONARY_DATA, armature_name):
	bpy.ops.object.mode_set(mode='POSE')
	# Get the armature object
	bpy.context.view_layer.objects.active = model.findArmature(bpy.context.active_object)
	armature = bpy.context.view_layer.objects.active
	

	SHAPE_KEYS_DICTIONARY = {}
	for row in SHAPE_KEYS_DICTIONARY_DATA:
		SHAPE_KEYS_DICTIONARY[(row[0], row[1])] = \
		{'locationX': row[2] \
		, 'locationY': row[3] \
		, 'locationZ': row[4] \
		, 'rotateX': row[5] \
		, 'rotateY': row[6] \
		, 'rotateZ': row[7]}

	keys = ['shape_key', 'bone_name']
	values = ['locationX', 'locationY', 'locationZ', 'rotateX', 'rotateY', 'rotateZ']
	SHAPE_KEYS_DICTIONARY_DATA = [dict(zip(keys, row)) for row in reader]
	
	for shape_key_bone_name, location_rotation in SHAPE_KEYS_DICTIONARY_DATA:
		shape_key, bone_name = shape_key_bone_name
		locationX, locationY, locationZ, rotateX, rotateY, rotateZ = location_rotation
		
		try:
			if shape_key in armature.shape_keys:
				 raise ValueError (f"{shape_key} exists already in armature")
				
			if bone_name not in armature.pose.bones:
				raise ValueError (f"{bone_name} does not exist in the armature.")
			bone = armature.pose.bones[bone_name]
			bone.shape_key_add(name=shape_key)
			bone.location = (locationX, locationY, locationZ)
			bone.rotation_euler = (rotateX, rotateY, rotateZ)
		except ValueError as e:
			print(e)


	
	#armature = bpy.data.objects[armature_name]
	if not armature:
		print(f"Armature with name '{armature_name}' not found.")
		return

	# Loop through all the bones
	for bone_name in unique_bone_names:
		# Get the bone you want to edit
		bone = armature.pose.bones.get(bone_name)
		if not bone:
			print(f"Bone with name '{bone_name}' not found in armature.")
			continue

		# Loop through all the shape keys
		for shape_key_name in unique_shape_keys:
			# Get the shape key you want to apply
			shape_key = armature.data.shape_keys.key_blocks.get(shape_key_name)
			if not shape_key:
				print(f"Shape key with name '{shape_key_name}' not found in armature.")
				continue

			# Apply the shape key to the bone
			bone.shape_key_add(shape_key, from_mix=True)
			
			locationX = SHAPE_KEYS_DICTIONARY[shape_key_name, bone_name]['locationX']
			locationY = SHAPE_KEYS_DICTIONARY[shape_key_name, bone_name]['locationY']
			locationZ = SHAPE_KEYS_DICTIONARY[shape_key_name, bone_name]['locationZ']
			rotateX = SHAPE_KEYS_DICTIONARY[shape_key_name, bone_name]['rotateX']
			rotateY = SHAPE_KEYS_DICTIONARY[shape_key_name, bone_name]['rotateY']
			rotateZ = SHAPE_KEYS_DICTIONARY[shape_key_name, bone_name]['rotateZ']

			# Set the location and rotation values
			bone.location = (float(locationX) , float(locationY) , float(locationZ))
			bone.rotation_quaternion = (float(rotateX) , float(rotateY) , float(rotateZ))
"""


def main(context):
	# print(bpy.context.scene.selected_ffxiv_model_type)
	armature_object = model.findArmature(bpy.context.active_object)
	bpy.context.view_layer.objects.active = armature_object


	if bpy.context.scene.ffxiv_model_list == 'none':
		pass
	if bpy.context.scene.ffxiv_model_list == "hyur":
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		SHAPE_KEYS_DICTIONARY = read_shape_keys_file("hyur")
	if bpy.context.scene.ffxiv_model_list == "miquote":
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		SHAPE_KEYS_DICTIONARY = read_shape_keys_file("miquote")
	if bpy.context.scene.ffxiv_model_list == "viera":
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		SHAPE_KEYS_DICTIONARY =read_shape_keys_file("viera")
	if bpy.context.scene.ffxiv_model_list == "aura":
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		SHAPE_KEYS_DICTIONARY = read_shape_keys_file("aura")
	if bpy.context.scene.ffxiv_model_list == "hrothgar":
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		SHAPE_KEYS_DICTIONARY = read_shape_keys_file("hrothgar")
	if bpy.context.scene.ffxiv_model_list == "elezen":
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		SHAPE_KEYS_DICTIONARY = read_shape_keys_file("elezen")
	if bpy.context.scene.ffxiv_model_list == "roegadyn":
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		SHAPE_KEYS_DICTIONARY = read_shape_keys_file("roegadyn")
	if bpy.context.scene.ffxiv_model_list == "lalafell":
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		SHAPE_KEYS_DICTIONARY = read_shape_keys_file("lalafell")

	shape_keys = parse_shape_key_data_from_csv(SHAPE_KEYS_DICTIONARY)

	for shape_key in shape_keys:
		create_shape_key(get_armature(),shape_key,shape_keys[shape_key])
		#print (key + ": \t")
		#print (shape_keys[shape_key])
		#print ('\n')

	

	#apply_shape_keys(SHAPE_KEYS_DICTIONARY, armature_object)

@register_wrap
class Shape_Keys(bpy.types.Operator):
	"""Shape Keys"""
	bl_idname = "object.add_shape_keys_btn"
	bl_label = "Import Shape Keys"

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
	], name = "Select Race:", default = 'hyur')

#	@classmethod
#	def poll(cls, context):
#		return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}