import bpy
from . import register_wrap
from . import model
from . import import_csv
from mmd_tools.core import model as mmd_model


def unhide_all_armatures():
	for o in bpy.context.scene.objects:
		if o.type == 'ARMATURE':
			o.hide = False

def print_missing_bone_names():
	missing_bone_names = []
	BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_dictionary()
	FINGER_BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_fingers_dictionary()
	SelectedBoneMap = bpy.context.scene.Destination_Armature_Type
	BoneMapIndex = BONE_NAMES_DICTIONARY[0].index(SelectedBoneMap)
	FingerBoneMapIndex = FINGER_BONE_NAMES_DICTIONARY[0].index(SelectedBoneMap)
	bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
	for b in BONE_NAMES_DICTIONARY:
		if BONE_NAMES_DICTIONARY.index(b) != 0:
			if b[BoneMapIndex] != '':
				if b[BoneMapIndex] not in ["upper body 2", "上半身2"]:
					if b[BoneMapIndex] not in bpy.context.active_object.data.bones.keys():
						missing_bone_names.append(b[BoneMapIndex])
	for b in FINGER_BONE_NAMES_DICTIONARY:
		if FINGER_BONE_NAMES_DICTIONARY.index(b) != 0:
			if b[FingerBoneMapIndex] != '':
				if b[FingerBoneMapIndex] not in ["thumb0_L", "thumb0_R", "左親指0", "親指0.L", "右親指0", "親指0.R"]:
					if b[FingerBoneMapIndex] not in bpy.context.active_object.data.bones.keys():
						missing_bone_names.append(b[FingerBoneMapIndex])
	print("\nBones renaming destination bone map was:")
	print(SelectedBoneMap)
	print("These bone names of" , SelectedBoneMap, "are missing from the active armature:" )
	print(missing_bone_names)



def rename_bones(boneMap1, boneMap2, BONE_NAMES_DICTIONARY): 
	boneMaps = BONE_NAMES_DICTIONARY[0]
	boneMap1_index = boneMaps.index(boneMap1)
	boneMap2_index = boneMaps.index(boneMap2)
	bpy.ops.object.mode_set(mode='OBJECT')

	for k in BONE_NAMES_DICTIONARY[1:]:
		if k[boneMap1_index] in bpy.context.active_object.data.bones.keys():
			if k[boneMap2_index] != '':
				bpy.context.active_object.data.bones[k[boneMap1_index]].name = k[boneMap2_index]
				if boneMap2 == 'mmd_japanese' or boneMap2 == 'mmd_japaneseLR':
					bpy.ops.object.mode_set(mode='POSE')
					if hasattr(bpy.context.active_object.pose.bones[k[boneMap2_index]] , "mmd_bone"):
						bpy.context.active_object.pose.bones[k[boneMap2_index]].mmd_bone.name_e = k[0]
					bpy.ops.object.mode_set(mode='OBJECT')



def rename_finger_bones(boneMap1, boneMap2, FINGER_BONE_NAMES_DICTIONARY):
	boneMaps = FINGER_BONE_NAMES_DICTIONARY[0]
	boneMap1_index = boneMaps.index(boneMap1)
	boneMap2_index = boneMaps.index(boneMap2)
	bpy.ops.object.mode_set(mode='OBJECT')

	for k in FINGER_BONE_NAMES_DICTIONARY[1:]:
		if k[boneMap1_index] in bpy.context.active_object.data.bones.keys():
			if k[boneMap2_index] != '':
				bpy.context.active_object.data.bones[k[boneMap1_index]].name = k[boneMap2_index]
				if boneMap2 == 'mmd_japanese' or boneMap2 == 'mmd_japaneseLR':
					bpy.ops.object.mode_set(mode='POSE')
					if hasattr(bpy.context.active_object.pose.bones[k[boneMap2_index]] , "mmd_bone"):
						bpy.context.active_object.pose.bones[k[boneMap2_index]].mmd_bone.name_e = k[0]
					bpy.ops.object.mode_set(mode='OBJECT')

	bpy.context.scene.Origin_Armature_Type = boneMap2
	print_missing_bone_names()


def mass_bones_renamer(context):
	bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)

	#show the bone names
	bpy.context.object.data.show_names = True
	unhide_all_armatures()
	BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_dictionary()
	FINGER_BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_fingers_dictionary()
	rename_bones(bpy.context.scene.Origin_Armature_Type, bpy.context.scene.Destination_Armature_Type, BONE_NAMES_DICTIONARY)
	rename_finger_bones(bpy.context.scene.Origin_Armature_Type, bpy.context.scene.Destination_Armature_Type, FINGER_BONE_NAMES_DICTIONARY)
	bpy.ops.object.mode_set(mode='POSE')
	bpy.ops.pose.select_all(action='SELECT')
	bpy.ops.object.mode_set(mode='OBJECT')


@register_wrap
class MassBonesRenamer(bpy.types.Operator):
	"""Mass bones renamer for armature conversion"""
	bl_idname = "ffxiv_mmd_tools_helper.bones_renamer"
	bl_label = "Bones Renamer"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.Origin_Armature_Type = bpy.props.EnumProperty(items = [\
	('mmd_english', 'MMD English', 'MikuMikuDance English bone names')\
	, ('mmd_japanese', 'MMD Japanese', 'MikuMikuDamce Japanese bone names')\
	, ('mmd_japaneseLR', 'MMD Japanese w/.L.R suffix', 'MikuMikuDamce Japanese bones names with .L.R suffixes')\
	, ('xna_lara', 'XNALara', 'XNALara bone names')\
	, ('daz_poser', 'DAZ/Poser', 'DAZ/Poser/Second Life bone names')\
	, ('blender_rigify', 'Blender rigify', 'Blender rigify bone names before generating the complete rig')\
	, ('sims_2', 'Sims 2', 'Sims 2 bone names')\
	, ('motion_builder', 'Motion Builder', 'Motion Builder bone names')\
	, ('3ds_max', '3ds Max', '3ds Max bone names')\
	, ('bepu', 'Bepu full body IK', 'Bepu full body IK bone names')\
	, ('project_mirai', 'Project Mirai', 'Project Mirai bone names')\
	, ('manuel_bastioni_lab', 'Manuel Bastioni Lab', 'Manuel Bastioni Lab bone names')\
	, ('makehuman_mhx', 'Makehuman MHX', 'Makehuman MHX bone names')\
	, ('sims_3', 'Sims 3', 'Sims 3 bone names')\
	, ('doa5lr', 'DOA5LR', 'Dead on Arrival 5 Last Round bone names')\
	, ('Bip_001', 'Bip001', 'Bip001 bone names')\
	, ('biped_3ds_max', 'Biped 3DS Max', 'Biped 3DS Max bone names')\
	, ('biped_sfm', 'Biped Source Film Maker', 'Biped Source Film Maker bone names')\
	, ('valvebiped', 'ValveBiped', 'ValveBiped bone names')\
	, ('iClone7', 'iClone7', 'iClone7 bone names')\
	,('ffxiv', 'FFXIV', 'FFXIV bone names')\
	], name = "From", default = 'ffxiv')
	

	bpy.types.Scene.Destination_Armature_Type = bpy.props.EnumProperty(items = [ \
	('mmd_english', 'MMD English', 'MikuMikuDance English bone names')\
	, ('mmd_japanese', 'MMD Japanese', 'MikuMikuDamce Japanese bone names')\
	, ('mmd_japaneseLR', 'MMD Japanese w/.L.R suffix', 'MikuMikuDamce Japanese bones names with .L.R suffixes')\
	, ('xna_lara', 'XNALara', 'XNALara bone names')\
	, ('daz_poser', 'DAZ/Poser', 'DAZ/Poser/Second Life bone names')\
	, ('blender_rigify', 'Blender rigify', 'Blender rigify bone names before generating the complete rig')\
	, ('sims_2', 'Sims 2', 'Sims 2 bone names')\
	, ('motion_builder', 'Motion Builder', 'Motion Builder bone names')\
	, ('3ds_max', '3ds Max', '3ds Max bone names')\
	, ('bepu', 'Bepu full body IK', 'Bepu full body IK bone names')\
	, ('project_mirai', 'Project Mirai', 'Project Mirai bone names')\
	, ('manuel_bastioni_lab', 'Manuel Bastioni Lab', 'Manuel Bastioni Lab bone names')\
	, ('makehuman_mhx', 'Makehuman MHX', 'Makehuman MHX bone names')\
	, ('sims_3', 'Sims 3', 'Sims 3 bone names')\
	, ('doa5lr', 'DOA5LR', 'Dead on Arrival 5 Last Round bone names')\
	, ('Bip_001', 'Bip001', 'Bip001 bone names')\
	, ('biped_3ds_max', 'Biped 3DS Max', 'Biped 3DS Max bone names')\
	, ('biped_sfm', 'Biped Source Film Maker', 'Biped Source Film Maker bone names')\
	, ('valvebiped', 'ValveBiped', 'ValveBiped bone names')\
	, ('iClone7', 'iClone7', 'iClone7 bone names')\
	,('ffxiv', 'FFXIV', 'FFXIV bone names')\
	], name = "To", default = 'mmd_english')


	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		mass_bones_renamer(context)
		return {'FINISHED'}


def find_and_replace_bone_names(context):
	
	bpy.context.view_layer.objects.active = model.findArmature(bpy.context.active_object)
	if bpy.context.scene.bones_all_or_selected == True:
		for b in bpy.context.active_object.data.bones:
			if b.select == True:
				if '_dummy' not in b.name and '_shadow' not in b.name:
					b.name = b.name.replace(bpy.context.scene.find_bone_string, bpy.context.scene.replace_bone_string)
	if bpy.context.scene.bones_all_or_selected == False:
		for b in bpy.context.active_object.data.bones:
			if '_dummy' not in b.name and '_shadow' not in b.name:
				b.name = b.name.replace(bpy.context.scene.find_bone_string, bpy.context.scene.replace_bone_string)

def find_bone_names(search_string):
	bpy.context.view_layer.objects.active = model.findArmature(bpy.context.active_object)
	armature = bpy.context.view_layer.objects.active

	if bpy.context.mode == 'OBJECT':
		bpy.ops.object.mode_set(mode='EDIT')

	if bpy.context.mode == 'EDIT_ARMATURE':
		#deselect all bones
		bpy.ops.armature.select_all(action='DESELECT')
		
		for b in bpy.data.objects[armature.name].data.edit_bones:
			print (b)
			if search_string in b.name:
				if '_dummy' not in b.name and '_shadow' not in b.name:
					b.select = True

	if bpy.context.mode == 'POSE':
		#deselect all bones
		for b in bpy.context.active_object.pose.bones:
			b.bone.select = False
		
		for b in bpy.context.active_object.pose.bones:
			if search_string in b.name:
				if '_dummy' not in b.name and '_shadow' not in b.name:
					b.bone.select = True
                
	

@register_wrap
class FindAndReplaceBoneNames(bpy.types.Operator):
	"""Find and replace mass renaming of bones"""
	bl_idname = "ffxiv_mmd_tools_helper.replace_bones_renaming"
	bl_label = "Replace bones renaming"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.find_bone_string = bpy.props.StringProperty(name="", description="", default="", maxlen=0, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)
	
	bpy.types.Scene.replace_bone_string = bpy.props.StringProperty(name="", description="", default="", maxlen=0, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)

	bpy.types.Scene.bones_all_or_selected = bpy.props.BoolProperty(name="Selected bones only", description="", default=False, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		find_and_replace_bone_names(context)
		return {'FINISHED'}

@register_wrap
class FindBoneNames(bpy.types.Operator):
	"""Find bones that match earch string"""
	bl_idname = "ffxiv_mmd_tools_helper.find_bones"
	bl_label = "Find bones that match search string"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		find_bone_names(bpy.context.scene.find_bone_string)
		return {'FINISHED'}


def blender_to_japanese_bone_names(context):
	armature = model.findArmature(bpy.context.active_object)
	for b in armature.data.bones:
		if hasattr(armature.pose.bones[b.name], "mmd_bone"):
			armature.pose.bones[b.name].mmd_bone.name_j = b.name


@register_wrap
class BlenderToJapaneseBoneNames(bpy.types.Operator):
	"""Copy Blender bone names to Japanese bone names"""
	bl_idname = "ffxiv_mmd_tools_helper.blender_to_japanese_bone_names"
	bl_label = "Copy Blender bone names to Japanese bone names"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		root = mmd_model.Model.findRoot(obj)
		return obj is not None and obj.type == 'ARMATURE' and root is not None

	def execute(self, context):
		blender_to_japanese_bone_names(context)
		return {'FINISHED'}

