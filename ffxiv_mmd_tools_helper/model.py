import bpy
from . import bone_tools

#this function is mostly useless without MMD Tools
def findRoot(obj):
	if obj is not None:
		if obj.mmd_type == 'ROOT':
			return obj
		else:
			return findRoot(obj.parent)
	else:
		return None
	

def find_MMD_Armature(obj):
	root = findRoot(obj)
	if root is None:
		return None
		#print('No MMD model is selected')
	else:
		return armature(root)

#i dont use this, dont know wtf it does
def armature(root):
	armatures = []
	for c in root.children:
		if c.type == 'ARMATURE':
			#c.hide = False
			armatures.append(c)
	if len(armatures) == 1:
		return armatures[0]
	if len(armatures) == 0:
		return None
	if len(armatures) > 1:
		print("Error. More than 1 armature found", armatures)

#i dont use this, dont know wtf it does
def __allObjects(obj):
	r = []
	for i in obj.children:
		r.append(i)
		r += __allObjects(i)
	return r

#i dont use this, dont know wtf it does
def allObjects(obj, root):
	if obj is None:
		obj = root
	return [obj] + __allObjects(obj)

#I think it gets all meshes from the root directory
def meshes(root):
	arm = armature(root)
	if arm is None:
		return []
	else:
		return filter(lambda x: x.type == 'MESH' and x.mmd_type == 'NONE', allObjects(arm, root))



def findArmature(obj):

	arm = None

	if bpy.context.mode == 'OBJECT':
		if obj.hide == True:
			obj.hide = False	
	
	if obj.type == 'ARMATURE':
		arm = obj
		return arm
	if obj.parent:
		if obj.parent.type == 'ARMATURE':
			#obj.mmd_root.show_armature = True	
			arm = obj.parent
			if arm.hide == True:
				arm.hide = False
			return arm
		else:
			for child in obj.parent.children:
				if child.type == 'ARMATURE':					
					#child.mmd_root.show_armature = True	
					arm = child
					if arm.hide == True:
						arm.hide = False
					return arm
	try:
		if obj.parent.parent:
			if obj.parent.parent.type == 'ARMATURE':
				#obj.parent.parent.hide = False
				#child.mmd_root.show_armature = True	
				arm = obj.parent.parent
				#arm.hide = False
				return arm
			else:
				for child in obj.parent.parent.children:
					if child.type == 'ARMATURE':
						arm = child
						if arm.hide == True:
							arm.hide = False
						#child.mmd_root.show_armature = True	
						return arm
	finally:
		if hasattr(obj, "mmd_type"):
			if obj.mmd_type == 'ROOT':
				return armature(obj)
		if obj.type == 'EMPTY':
			return armature(obj)


def find_MMD_MeshesList(obj):
	root = findRoot(obj)
	if root is None:
		print('No MMD model is selected')
	else:
		return list(meshes(root))

def findMeshesList(obj):
	mesheslist = []
	if obj.type == 'ARMATURE':
		for c in obj.children:
			if c.type == 'MESH':
				mesheslist.append(c)
		return mesheslist
	if obj.type == 'MESH':
		if obj.parent is not None:
			if obj.parent.type == 'ARMATURE':
				for c in obj.parent.children:
					if c.type == 'MESH':
						mesheslist.append(c)
				return mesheslist
		if obj.parent is None or obj.parent.type != 'ARMATURE':
			return [obj]
	if hasattr(obj, "mmd_type"):
		if obj.mmd_type == 'ROOT':
			return list(meshes(obj))
	if obj.type == 'EMPTY':
		return list(meshes(obj))

def find_mmd_rigid_bodies_list(root):
	rigidbodies = None
	rigid_bodies_list = []
	for c in root.children:
		if c.type == 'EMPTY':
			if c.name.startswith("rigidbodies"):
				rigidbodies = c
	if rigidbodies is not None:
		rigid_bodies_list = list(rigidbodies.children)
	return rigid_bodies_list

def find_mmd_joints_list(root):
	joints = None
	joints_list = []
	for c in root.children:
		if c.type == 'EMPTY':
			if c.name.startswith("joints"):
				joints = c
	if joints is not None:
		joints_list = list(joints.children)
	return joints_list

def is_mmd_english():
	mmd_english = True
	bpy.context.view_layer.objects.active  = findArmature(bpy.context.active_object)
	mmd_english_test_bone_names = ['upper body', 'neck', 'head', 'shoulder_L', 'arm_L', 'elbow_L', 'wrist_L', 'leg_L', 'knee_L', 'ankle_L', 'shoulder_R', 'arm_R', 'elbow_R', 'wrist_R', 'leg_R', 'knee_R', 'ankle_R']
	missing_mmd_english_test_bone_names = []
	for b in mmd_english_test_bone_names:
		if b not in bpy.context.active_object.data.bones.keys():
			missing_mmd_english_test_bone_names.append(b)
	if len(missing_mmd_english_test_bone_names) > 0:
		print("Missing mmd_english test bone names = ", missing_mmd_english_test_bone_names)
		print('\n')
		print("This armature appears not to be an mmd_english armature")
		mmd_english = False
	return mmd_english

#gets the equivalent primary bones from armature and returns the primary bonename type (mmd_english,mmd_english_alt, mmd_japanese, mmd_japaneseLR etc...)
def get_primary_bonetype (armature):
	bone_list = {'root','neck','head','center','center_2','upper body','upper body 2','upper body 3','lower body','shoulder_L','arm_L','elbow_L','wrist_L'
			,'thumb0_L','thumb1_L','thumb2_L','fore1_L','fore2_L','fore3_L','middle1_L','middle2_L','middle3_L','third1_L','third2_L','third3_L','little1_L','little2_L','little3_L'
			,'shoulder_R','arm_R','elbow_R','wrist_R',
			'thumb0_R','thumb1_R','thumb2_R','fore1_R','fore2_R','fore3_R','middle1_R','middle2_R','middle3_R','third1_R','third2_R','third3_R','little1_R','little2_R','little3_R'
			,'leg_L','knee_L','ankle_L','toe_L','leg_R','knee_R','ankle_R','toe_R','eye_L','eye_R','waist'}
	
	bone_finds = []
		
	for bone in bone_list:
		if bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,bone):
			armature_bone_name = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(armature,bone)
			bone_finds.append(armature_bone_name)

	bone_types = ['mmd_english', 'mmd_english_alt','mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv','mmd_kaito']

	max_counter = 0
	max_bone_type = None

	for bone_type in bone_types:
		counter = sum(1 for bone in bone_finds if bone_tools.is_bone_bone_type(armature, bone, bone_type))
		if counter > max_counter:
			max_counter = counter
			max_bone_type = bone_type

	return max_bone_type

def test():
	if hasattr(bpy.context, "active_object"):
		if bpy.context.active_object is not None:
			print("Active Object Type = ", bpy.context.active_object.type)
			Root = findRoot(bpy.context.active_object)
			print("root = ", Root)
			Meshes = find_MMD_MeshesList(bpy.context.active_object)
			print("mmd_meshes = ", Meshes)
			Armature = find_MMD_Armature(bpy.context.active_object)
			print("mmd_armature = ", Armature, '\n')
			Meshes = findMeshesList(bpy.context.active_object)
			print("meshes = ", Meshes)
			Armature = findArmature(bpy.context.active_object)
			print("armature = ", Armature)
			print('\n')
			Rigid_Bodies = find_mmd_rigid_bodies_list(Root)
			print("rigid bodies = ", Rigid_Bodies)
			print('\n')
			Joints = find_mmd_joints_list(Root)
			print("joints = ", Joints)
			print('\n')
			print()

# test()


