import bpy
import math
from . import register_wrap
from . import import_csv
from . import bone_tools

import mmd_tools.core.model as mmd_model
from mmd_tools.utils import ItemOp
from mmd_tools.core import model as mmd_model



def create_bone_morph(bone_morph_name,bone_morph_e_name,bone_morph_category):
	obj = bpy.context.active_object
	root = mmd_model.Model.findRoot(obj)
	mmd_root = root.mmd_root
	morph_type = 'bone_morphs' #mmd_root.active_morph_type
	morphs = getattr(mmd_root, morph_type)
	morph,mmd_root.active_morph = ItemOp.add_after(morphs, mmd_root.active_morph)
	morph.name = bone_morph_name
	morph.name_e = bone_morph_e_name
	morph.category = bone_morph_category
	
	#items=[
	#        ('SYSTEM', 'Hidden', '', 0),
	#        ('EYEBROW', 'Eye Brow', '', 1),
	#        ('EYE', 'Eye', '', 2),
	#        ('MOUTH', 'Mouth', '', 3),
	#        ('OTHER', 'Other', '', 4),
	#    ]
	
	return morph

def get_bone_morph(bone_morph_name):
	
	obj = bpy.context.active_object
	root = mmd_model.Model.findRoot(obj)
	mmd_root = root.mmd_root

	for morph in mmd_root.bone_morphs:
		if (morph.name == bone_morph_name) or (morph.name_e == bone_morph_name):
			return morph
			break
		
def remove_bone_morph(bone_morph_name):
	
	obj = bpy.context.active_object
	root = mmd_model.Model.findRoot(obj)
	mmd_root = root.mmd_root
	
	morphs = getattr(mmd_root, 'bone_morphs') 
	
	for index,morph in enumerate(mmd_root.bone_morphs):
		if (morph.name == bone_morph_name) or (morph.name_e == bone_morph_name):
			morphs.remove(index)
			mmd_root.active_morph = max(0, mmd_root.active_morph-1)
			print(f"bone morph {bone_morph_name} removed")
			break

def clear_bone_morph():
    
    obj = bpy.context.active_object
    root = mmd_model.Model.findRoot(obj)
    rig = mmd_model.Model(root)
    armature = rig.armature()
    for p_bone in armature.pose.bones:
        p_bone.matrix_basis.identity()

def apply_bone_morph(bone_morph_name):
	
	obj = bpy.context.active_object
	root = mmd_model.Model.findRoot(obj)
	rig = mmd_model.Model(root)
	armature = rig.armature()
	mmd_root = root.mmd_root
	morph = get_bone_morph(bone_morph_name) #mmd_root.bone_morphs[mmd_root.active_morph]
	morph.data.clear()
	morph.active_data = 0
	for p_bone in armature.pose.bones:
		if p_bone.location.length > 0 or p_bone.matrix_basis.decompose()[1].angle > 0:
			item = morph.data.add()
			item.bone = p_bone.name
			item.location = p_bone.location
			item.rotation = p_bone.rotation_quaternion if p_bone.rotation_mode == 'QUATERNION' else p_bone.matrix_basis.to_quaternion()
			p_bone.bone.select = True
		else:
			p_bone.bone.select = False

	clear_bone_morph()


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


def generate_bone_morph (armature,bone_morph_name,bone_morph_bones_data):

	bpy.ops.object.mode_set(mode='POSE')

	bm_name = bone_morph_name
	bm_name_e = bone_morph_name
	bm_category = 'OTHER'

	#pull data from mmd_bone_morphs_list to get the metadata
	mmd_bone_morphs_list = import_csv.use_csv_bone_morphs_list()
	for mmd_bone_morph in mmd_bone_morphs_list:
		if bone_morph_name in (mmd_bone_morph[1],mmd_bone_morph[2]):
			bm_name = mmd_bone_morph[0]
			bm_name_e = mmd_bone_morph[1]
			bm_category = mmd_bone_morph[2]
			break

	#if a bone_morph exists with the same name, delete it first
	remove_bone_morph(bone_morph_name)
	bone_morph_obj = create_bone_morph(bm_name,bm_name_e,bm_category)

	i = 0
	
	#transform the bones according to the data provided
	for bone in bone_morph_bones_data:
		#check if bone from bone_morph_bones_data exists on the armature.
		exists = armature.pose.bones.get(bone[0]) is not None
		if exists :
			delta_coords = [bone[1],bone[2],bone[3],bone[4],bone[5],bone[6],bone[7],bone[8],bone[9]]
			transform_pose_bone(armature,bone[0],delta_coords)
			i += 1
		else:
			print( "bone_morph: '" + bone_morph_name + "', armature: '" + armature.name + "', bone: '" + bone[0] + "' doesn't exist" )
	

	if i != 0:

			apply_bone_morph(bone_morph_obj.name)
			print( "bone_morph: '" + bone_morph_name + "' applied ")
	else:
		print( "bone_morph: '" + bone_morph_name + "' was not applied at all" )



def parse_bone_morphs_data_from_csv (csv_data):
	bone_morphs_dictionary = None
	
	# Create an empty dictionary
	bone_morphs_dictionary = {}

	for bone_morphs_bone_data in csv_data:
		
		#group the data based on the first row(bone_morph name)
		bone_morph = bone_morphs_bone_data[0]
		
		#if the bone_morph does not exist in the dictionary yet, create a new list for it
		if bone_morph not in bone_morphs_dictionary:
			bone_morphs_dictionary[bone_morph] = []
			
		#add the row to the dictionary
		bone_morphs_dictionary[bone_morph].append(bone_morphs_bone_data)

	# Iterate through the values of each row and parse out the first column (bone_morph) 
	# because we don't want to pass that as part of the bone data in the following step
	for bone_morph in bone_morphs_dictionary:
		bone_data = bone_morphs_dictionary[bone_morph]
		for i, j in enumerate(bone_data):
			bone_data[i] = j[1:]
			
	return bone_morphs_dictionary

def read_bone_morphs_list_file():

	BONE_MORPHS_LIST = None
	BONE_MORPHS_LIST = import_csv.use_csv_bone_morphs_list()

	return BONE_MORPHS_LIST

def change_face_rotation_mode(rotation_mode):
	armature = bpy.context.active_object

	bone_type = ['mmd_english', 'mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv']
	BONE_DICTIONARY = bone_tools.get_csv_metadata_by_bone_type('blender_bone_group',bone_type)

	for bone in armature.pose.bones:
		for _bone in BONE_DICTIONARY:
			if bone.name == _bone[1] and _bone[0] == 'face':
				bone.rotation_mode = rotation_mode


def main(context,file_path):

	print("the filepath for the selected file is:",file_path)

	armature = bpy.context.active_object #model.find_MMD_Armature(bpy.context.object)
	bpy.context.view_layer.objects.active = armature

	clear_bone_morph()

	BONE_MORPH_DICTIONARY = import_csv.use_csv_bone_morphs_dictionary(file_path)
	bone_morphs = parse_bone_morphs_data_from_csv(BONE_MORPH_DICTIONARY)
	for bone_morph in bone_morphs:
		generate_bone_morph(armature,bone_morph,bone_morphs[bone_morph])



@register_wrap
class AddBoneMorphs(bpy.types.Operator):
	"""Add Bone Morphs to an FFXIV Model (converted to an MMD Model)"""
	bl_idname = "ffxiv_mmd.add_bone_morphs"
	bl_label = "Import Bone Morphs"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.bone_morph_ffxiv_model_list = bpy.props.EnumProperty(items = \
	[('none', 'none', 'none')\
	, ("aura", "Au Ra","Import Au Ra Bone Morphs") \
	, ("elezen", "Elezen","Import Elezen Bone Morphs") \
	, ("hrothgar", "Hrothgar","Import Hrothgar Bone Morphs") \
	, ("hyur", "Hyur (Human)","Import Hyur Bone Morphs") \
	, ("lalafell", "Lalafell","Import Lalafell Bone Morphs") \
	, ("miqote", "Miqo'te","Import Miqo'te Bone Morphs") \
	, ("roegadyn", "Roegadyn","Import Roegadyn Bone Morphs") \
	, ("viera", "Viera","Import Viera Bone Morphs") \
	], name = "Race", default = 'hyur')
	
	bpy.types.Scene.alternate_folder_cbx = bpy.props.BoolProperty(name="Use Alternate Folder for CSVs", default=False)

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		root = mmd_model.Model.findRoot(obj)
		return obj is not None and obj.type == 'ARMATURE' and root is not None

	def execute(self, context):

		if bpy.context.scene.bone_morph_ffxiv_model_list == 'none':
			pass
		else:
			ffxiv_race = bpy.context.scene.bone_morph_ffxiv_model_list
			file_path = (__file__ + r"data\bone_morphs_" + ffxiv_race +".csv").replace("bone_morphs.py" , "")
			
			
			main(context,file_path)
		#context.scene.bone_morph_ffxiv_model_list = self.bone_morph_ffxiv_model_list
		return {'FINISHED'}
	

from bpy_extras.io_utils import ImportHelper
@register_wrap
class ImportCustomBoneMorphsFile(bpy.types.Operator, ImportHelper):
	"""Import a custom Bone Morphs CSV File"""
	bl_idname = "ffxiv_mmd.import_custom_bone_morphs_file"
	bl_label = "Import CSV"
	bl_options = {'REGISTER', 'UNDO'}

	filename_ext = ".csv"
	filter_glob: bpy.props.StringProperty(
		default="*.csv",
		options={'HIDDEN'},
	)

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		root = mmd_model.Model.findRoot(obj)
		return obj is not None and obj.type == 'ARMATURE' and root is not None

	def execute(self, context):
		filepath = self.filepath
		
		main (context,filepath)
		
		return {'FINISHED'}

@register_wrap
class OpenBoneMorphsFile(bpy.types.Operator):
	"""Open Bone Morphs CSV File for the selected race"""
	bl_idname = "ffxiv_mmd.open_bone_morphs_file"
	bl_label = "Open Bone Morphs CSV File"

	def execute(self, context):
		import_csv.open_bone_morphs_dictionary(context.scene.bone_morph_ffxiv_model_list)
		return {'FINISHED'}
	



		
@register_wrap
class ChangeFaceBoneRotationMode(bpy.types.Operator):
	"""Changes all Face Bones to the selected Rotation Mode"""
	bl_idname = "ffxiv_mmd.change_face_rotation_mode"
	bl_label = "Change Face Rotation Mode"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.bone_morph_rotation_mode_list = bpy.props.EnumProperty(items = [\
		  ("QUATERNION", "Quaternion (WXYZ)","Quaternion (WXYZ)") \
		, ("XYZ", "XYZ Euler","XYZ Euler") \
		], name = "", default = 'XYZ')

	def execute(self, context):
		change_face_rotation_mode(context.scene.bone_morph_rotation_mode_list)
		return {'FINISHED'}

"""
@register_wrap
class PopulateMMDBoneMorphsFile(bpy.types.Operator):
	bl_idname = "ffxiv_mmd.populate_mmd_bone_morphs_file"
	bl_label = "Open Bone Morphs CSV File"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bone_morphs = read_bone_morphs_list_file()
		for bone_morph in bone_morphs:
			create_bone_morph(bone_morph[0],bone_morph[1],bone_morph[2])
		return {'FINISHED'}
"""