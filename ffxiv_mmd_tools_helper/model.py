import bpy

def findRoot(obj):
	if obj is not None:
		if obj.mmd_type == 'ROOT':
			return obj
		else:
			return findRoot(obj.parent)
	else:
		return None

def armature(root):
	armatures = []
	for c in root.children:
		if c.type == 'ARMATURE':
			c.hide = False
			armatures.append(c)
	if len(armatures) == 1:
		return armatures[0]
	if len(armatures) == 0:
		return None
	if len(armatures) > 1:
		print("Error. More than 1 armature found", armatures)

def __allObjects(obj):
	r = []
	for i in obj.children:
		r.append(i)
		r += __allObjects(i)
	return r

def allObjects(obj, root):
	if obj is None:
		obj = root
	return [obj] + __allObjects(obj)

def meshes(root):
	arm = armature(root)
	if arm is None:
		return []
	else:
		return filter(lambda x: x.type == 'MESH' and x.mmd_type == 'NONE', allObjects(arm, root))


def find_MMD_Armature(obj):
	root = findRoot(obj)
	if root is None:
		print('No MMD model is selected')
	else:
		return armature(root)

def findArmature(obj):
	
	if obj.type == 'ARMATURE':
		#obj.hide = False
		return obj
	if obj.parent is not None:
		if obj.parent.type == 'ARMATURE':
			#obj.parent.hide = False
			#obj.mmd_root.show_armature = True	
			return obj.parent
		else:
			for child in obj.parent.children:
				if child.type == 'ARMATURE':
					#child.hide = False
					#child.mmd_root.show_armature = True	
					return child
	if obj.parent.parent is not None:
		if obj.parent.parent.type == 'ARMATURE':
			#obj.parent.parent.hide = False
			#child.mmd_root.show_armature = True	
			return obj.parent.parent
		for child in obj.parent.parent.children:
			if child.type == 'ARMATURE':
				#child.hide = False
				#child.mmd_root.show_armature = True	
				return child
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


