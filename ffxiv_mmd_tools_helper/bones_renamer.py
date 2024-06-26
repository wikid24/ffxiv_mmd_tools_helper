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



def rename_bones(source, target, BONE_NAMES_DICTIONARY): 
	boneMaps = BONE_NAMES_DICTIONARY[0]
	source_index = boneMaps.index(source)
	target_index = boneMaps.index(target)
	bpy.ops.object.mode_set(mode='OBJECT')

	for mapping in BONE_NAMES_DICTIONARY[1:]:
		#if source and target mappings are not blank
		if mapping[source_index] and mapping[source_index] != '' :
			#if target bone name exists on the armature
			if mapping[source_index] in bpy.context.active_object.data.bones.keys():
				#if target bonemap is not blank
				if mapping[target_index] and mapping[target_index] != '':
					#set the bone name
					bpy.context.active_object.data.bones[mapping[source_index]].name = mapping[target_index]
					#If target is MMD Japanese
					if target == 'mmd_japanese' or target == 'mmd_japaneseLR':
						bpy.ops.object.mode_set(mode='POSE')
						#If armature is converted to MMD armature
						if hasattr(bpy.context.active_object.pose.bones[mapping[target_index]] , "mmd_bone"):
							#set the MMD English Bone name as well to english equivalent
							bpy.context.active_object.pose.bones[mapping[target_index]].mmd_bone.name_e = mapping[0]
						bpy.ops.object.mode_set(mode='OBJECT')

	#after finished translating, set the source dropdown to the same as the target
	bpy.context.scene.Origin_Armature_Type = target


"""
def rename_finger_bones(boneMap1, boneMap2, FINGER_BONE_NAMES_DICTIONARY):
	boneMaps = FINGER_BONE_NAMES_DICTIONARY[0]
	boneMap1_index = boneMaps.index(boneMap1)
	boneMap2_index = boneMaps.index(boneMap2)
	bpy.ops.object.mode_set(mode='OBJECT')

	for k in FINGER_BONE_NAMES_DICTIONARY[1:]:
		if k[boneMap1_index] and k[boneMap1_index] != '':
			if k[boneMap1_index] in bpy.context.active_object.data.bones.keys():
				if k[boneMap2_index] and k[boneMap2_index] != '':
					bpy.context.active_object.data.bones[k[boneMap1_index]].name = k[boneMap2_index]
					if boneMap2 == 'mmd_japanese' or boneMap2 == 'mmd_japaneseLR':
						bpy.ops.object.mode_set(mode='POSE')
						if hasattr(bpy.context.active_object.pose.bones[k[boneMap2_index]] , "mmd_bone"):
							bpy.context.active_object.pose.bones[k[boneMap2_index]].mmd_bone.name_e = k[0]
						bpy.ops.object.mode_set(mode='OBJECT')

	bpy.context.scene.Origin_Armature_Type = boneMap2
	print_missing_bone_names()
"""

def mass_bones_renamer(context):
	bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)

	#show the bone names
	bpy.context.object.data.show_names = True
	unhide_all_armatures()
	BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_dictionary()
	#FINGER_BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_fingers_dictionary()
	rename_bones(bpy.context.scene.Origin_Armature_Type, bpy.context.scene.Destination_Armature_Type, BONE_NAMES_DICTIONARY)
	#rename_finger_bones(bpy.context.scene.Origin_Armature_Type, bpy.context.scene.Destination_Armature_Type, FINGER_BONE_NAMES_DICTIONARY)
	bpy.ops.object.mode_set(mode='POSE')
	bpy.ops.pose.select_all(action='SELECT')
	bpy.ops.object.mode_set(mode='OBJECT')


@register_wrap
class MassBonesRenamer(bpy.types.Operator):
	"""Mass bones renamer for armature conversion"""
	bl_idname = "ffxiv_mmd.bones_renamer"
	bl_label = "Bones Renamer"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.Origin_Armature_Type = bpy.props.EnumProperty(items = [\
	('mmd_english', 'MMD English', 'MikuMikuDance English bone names')\
	, ('mmd_english_alt', 'MMD English (Alternate TL)', 'MMD English (Alternate Translation used from MMD Tools Translator)')\
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
	,('yakuza', 'Yakuza', 'Yakuza Series bone names')\
	,('autorig_pro', 'AutoRig Pro', 'AutoRig Pro bone names')\
	,('mixamo', 'Adobe Mixamo', 'Adobe Mixamo bone names')\
	,('fortnite', 'Fortnite', 'Fortnite')\
	], name = "From", default = 'ffxiv')
	

	bpy.types.Scene.Destination_Armature_Type = bpy.props.EnumProperty(items = [ \
	('mmd_english', 'MMD English', 'MikuMikuDance English bone names')\
	, ('mmd_english_alt', 'MMD English (Alternate TL)', 'MMD English (Alternate Translation used from MMD Tools Translator)')\
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
	,('yakuza', 'Yakuza', 'Yakuza Series bone names')\
	,('autorig_pro', 'AutoRig Pro', 'AutoRig Pro bone names')\
	,('mixamo', 'Adobe Mixamo', 'Adobe Mixamo bone names')\
	,('fortnite', 'Fortnite', 'Fortnite')\
	], name = "To", default = 'mmd_english')


	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		mass_bones_renamer(context)
		return {'FINISHED'}


def find_and_replace_bone_names(context,bone_search_type):
	
	armature = model.findArmature(context.active_object)

	context.view_layer.objects.active = armature
	if context.scene.bones_all_or_selected == True:
		for b in context.active_object.data.bones:
			if b.select == True:

				if '_dummy' not in b.name and '_shadow' not in b.name:

					if bone_search_type=='blender_bone_name':
						b.name = b.name.replace(context.scene.find_bone_string, context.scene.replace_bone_string)
					elif bone_search_type=='mmd_bone_name_j':
						if hasattr(armature.pose.bones[b.name], "mmd_bone"):
							new_mmd_bone_name = armature.pose.bones[b.name].mmd_bone.name_j.replace(context.scene.find_bone_string, context.scene.replace_bone_string)
							armature.pose.bones[b.name].mmd_bone.name_j = new_mmd_bone_name
					elif bone_search_type=='mmd_bone_name_e':
						if hasattr(armature.pose.bones[b.name], "mmd_bone"):
							new_mmd_bone_name = armature.pose.bones[b.name].mmd_bone.name_e.replace(context.scene.find_bone_string, context.scene.replace_bone_string)
							armature.pose.bones[b.name].mmd_bone.name_e = new_mmd_bone_name

	if context.scene.bones_all_or_selected == False:
		for b in context.active_object.data.bones:
			if '_dummy' not in b.name and '_shadow' not in b.name:
				if bone_search_type=='blender_bone_name':
					b.name = b.name.replace(context.scene.find_bone_string, context.scene.replace_bone_string)
				elif bone_search_type=='mmd_bone_name_j':
					if hasattr(armature.pose.bones[b.name], "mmd_bone"):
						new_mmd_bone_name = armature.pose.bones[b.name].mmd_bone.name_j.replace(context.scene.find_bone_string, context.scene.replace_bone_string)
						armature.pose.bones[b.name].mmd_bone.name_j = new_mmd_bone_name
				elif bone_search_type=='mmd_bone_name_e':
					if hasattr(armature.pose.bones[b.name], "mmd_bone"):
						new_mmd_bone_name = armature.pose.bones[b.name].mmd_bone.name_e.replace(context.scene.find_bone_string, context.scene.replace_bone_string)
						armature.pose.bones[b.name].mmd_bone.name_e = new_mmd_bone_name

def find_bone_names(bone_search_type=None,contains=None,startswith=None,endswith=None,append_to_selected=None):

	

	armature = model.findArmature(bpy.context.active_object)
	if armature is not None:
		armature.mmd_root.show_armature = True
		armature.hide = False
		bpy.context.view_layer.objects.active = armature


	if bone_search_type is None:
		bone_search_type='blender_bone_name'
	if startswith is None:
		startswith = ''
	if endswith is None:
		endswith = ''
	if contains is None:
		contains = ''
	if append_to_selected is None:
		append_to_selected = False

	if bpy.context.mode == 'OBJECT':
		bpy.ops.object.mode_set(mode='EDIT')

	selected_objs = None

	if bpy.context.mode == 'EDIT_ARMATURE':

		if append_to_selected == False:
			#deselect all bones
			bpy.ops.armature.select_all(action='DESELECT')

		for b in bpy.data.objects[armature.name].data.edit_bones:

			mmd_j_bone_name = ''
			mmd_e_bone_name = ''

			if hasattr(armature.pose.bones[b.name], "mmd_bone"):
				mmd_j_bone_name = armature.pose.bones[b.name].mmd_bone.name_j
				mmd_e_bone_name = armature.pose.bones[b.name].mmd_bone.name_e

			if '_dummy' not in b.name and '_shadow' not in b.name:
				
				if bone_search_type=='blender_bone_name':
					if b.name.startswith(str(startswith)) and b.name.endswith(str(endswith)) and contains in b.name:
						b.hide=False
						b.select = True
				elif bone_search_type=='mmd_bone_name_j':
					if mmd_j_bone_name.startswith(str(startswith)) and mmd_j_bone_name.endswith(str(endswith)) and contains in mmd_j_bone_name:
						b.hide=False
						b.select = True

				elif bone_search_type=='mmd_bone_name_e':
					if mmd_e_bone_name.startswith(str(startswith)) and mmd_e_bone_name.endswith(str(endswith)) and contains in mmd_e_bone_name:
						b.hide=False
						b.select = True

		selected_bones = bpy.context.selected_bones
		return selected_bones

	if bpy.context.mode == 'POSE':
		if append_to_selected == False:
			#deselect all bones
			for b in bpy.context.active_object.pose.bones:
				b.bone.select = False
		
		for b in bpy.context.active_object.pose.bones:

			mmd_j_bone_name = ''
			mmd_e_bone_name = ''

			if hasattr(armature.pose.bones[b.name], "mmd_bone"):
				mmd_j_bone_name = armature.pose.bones[b.name].mmd_bone.name_j
				mmd_e_bone_name = armature.pose.bones[b.name].mmd_bone.name_e

			if '_dummy' not in b.name and '_shadow' not in b.name:
				if bone_search_type=='blender_bone_name':
					if b.name.startswith(str(startswith)) and b.name.endswith(str(endswith)) and contains in b.name:
						b.bone.hide = False
						b.bone.select = True
				elif bone_search_type=='mmd_bone_name_j':
					if mmd_j_bone_name.startswith(str(startswith)) and mmd_j_bone_name.endswith(str(endswith)) and contains in mmd_j_bone_name:
						b.bone.hide = False
						b.bone.select = True

				elif bone_search_type=='mmd_bone_name_e':
					if mmd_e_bone_name.startswith(str(startswith)) and mmd_e_bone_name.endswith(str(endswith)) and contains in mmd_e_bone_name:
						b.bone.hide = False
						b.bone.select = True
		
		selected_bones = bpy.context.selected_bones
		return selected_objs

		

	
                
	

@register_wrap
class FindAndReplaceBoneNames(bpy.types.Operator):
	"""Find and replace mass renaming of bones"""
	bl_idname = "ffxiv_mmd.replace_bones_renaming"
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
		find_and_replace_bone_names(context,bone_search_type=bpy.context.scene.find_bone_name_mode)
		return {'FINISHED'}

@register_wrap
class FindBoneNames(bpy.types.Operator):
	"""Find bones that match earch string"""
	bl_idname = "ffxiv_mmd.find_bones"
	bl_label = "Find bones that match search string"
	bl_options = {'REGISTER', 'UNDO'}

	append_to_selected = bpy.props.BoolProperty(name="Append", default=False)


	bpy.types.Scene.find_bone_name_mode = bpy.props.EnumProperty(items = \
	[("blender_bone_name", "Blender Bone Names","Search for Blender Bone Names") \
	, ("mmd_bone_name_j", "MMD Japanese Bone Names", "Search for MMD Japanese Bone Names")\
	, ("mmd_bone_name_e", "MMD English Bone Names", "Search for MMD English Bone Name")\
	], name = "", default = 'blender_bone_name')

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None #and obj.type == 'ARMATURE'

	def execute(self, context):
		find_bone_names(bone_search_type=bpy.context.scene.find_bone_name_mode,contains=bpy.context.scene.find_bone_string,append_to_selected=self.append_to_selected)
		return {'FINISHED'}


def blender_to_japanese_bone_names(context):
	armature = model.findArmature(bpy.context.active_object)
	for b in armature.data.bones:
		if hasattr(armature.pose.bones[b.name], "mmd_bone"):
			armature.pose.bones[b.name].mmd_bone.name_j = b.name


@register_wrap
class BlenderToJapaneseBoneNames(bpy.types.Operator):
	"""Copy Blender bone names to Japanese bone names"""
	bl_idname = "ffxiv_mmd.blender_to_japanese_bone_names"
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

