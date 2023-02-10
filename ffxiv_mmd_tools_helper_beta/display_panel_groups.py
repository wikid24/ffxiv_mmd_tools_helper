import bpy
from . import register_wrap
from . import model
from mmd_tools.core import model as mmd_model
from . import bone_tools
from . import import_csv


def __items(display_item_frame):
	return getattr(display_item_frame, 'data', display_item_frame.items)


def delete_empty_display_panel_groups(root):
	bpy.context.view_layer.objects.active  = root
	for d in range(len(bpy.context.active_object.mmd_root.display_item_frames)-1, 1, -1):
		#if bpy.context.active_object.mmd_root.display_item_frames[d].name != "Root" and bpy.context.active_object.mmd_root.display_item_frames[d].name != "表情":
		if len(__items(bpy.context.active_object.mmd_root.display_item_frames[d])) == 0:
			bpy.context.active_object.mmd_root.display_item_frames.remove(d)

def clear_display_panel_groups(root):
	bpy.context.view_layer.objects.active  = root
	bpy.context.active_object.mmd_root.display_item_frames.clear()

def display_panel_groups_from_bone_groups(root, armature_object):
	bpy.context.view_layer.objects.active  = armature_object
	bpy.ops.object.mode_set(mode='POSE')
	bone_groups = armature_object.pose.bone_groups.keys() + ["Other"]
	bone_groups_of_bones = []
	for b in armature_object.pose.bones:
		if b.bone_group is not None:
			if "dummy" not in b.name and "shadow" not in b.name:
				if b.name not in ["root", "全ての親", "center", "センター"]:
					bone_groups_of_bones.append((b.name, b.bone_group.name))
				if b.name in ["root", "全ての親", "center", "センター"]:
					bone_groups_of_bones.append((b.name, "Root"))
		else:
			if "dummy" not in b.name and "shadow" not in b.name:
				if b.name not in ["root", "全ての親", "center", "センター"]:
					bone_groups_of_bones.append((b.name, "Other"))
				if b.name in ["root", "全ての親", "center", "センター"]:
					bone_groups_of_bones.append((b.name, "Root"))
	# bpy.context.view_layer.objects.active  = armature_object.parent
	bpy.context.view_layer.objects.active  = model.findRoot(armature_object)
	group = bpy.context.active_object.mmd_root.display_item_frames.add()
	group.name = "Root"
	group.name_e = "Root"
	group.is_special = True
	group = bpy.context.active_object.mmd_root.display_item_frames.add()
	group.name = "表情"
	group.name_e = "Expressions"
	group.is_special = True
	for bg in bone_groups:
		if bg != "Root" and bg != "表情":
			group = bpy.context.active_object.mmd_root.display_item_frames.add()
			group.name = bg
			group.name_e = bg
	for bgb in bone_groups_of_bones:
		item = __items(bpy.context.active_object.mmd_root.display_item_frames[bgb[1]]).add()
		item.name = bgb[0]
		item.name_e = bgb[0]

def display_panel_groups_from_shape_keys(mesh_objects_list):
	shape_key_names = []
	for m in mesh_objects_list:
		if m.data.shape_keys is not None:
			for s in m.data.shape_keys.key_blocks:
				if 'sdef' not in s.name and s.name != 'Basis':
					if s.name not in shape_key_names:
						shape_key_names.append(s.name)
		root = model.findRoot(m)
	for skn in shape_key_names:
		if skn not in __items(root.mmd_root.display_item_frames["表情"]).keys():
			item = __items(root.mmd_root.display_item_frames["表情"]).add()
			item.type = 'MORPH'
			item.morph_type = 'vertex_morphs'
			item.name = skn

def display_panel_groups_non_vertex_morphs(root):
	bpy.context.view_layer.objects.active  = root
	for m in root.mmd_root.bone_morphs:
		if m.name not in __items(root.mmd_root.display_item_frames["表情"]).keys():
			item = __items(root.mmd_root.display_item_frames["表情"]).add()
			item.type = 'MORPH'
			item.morph_type = "bone_morphs"
			item.name = m.name
	for m in root.mmd_root.material_morphs:
		if m.name not in __items(root.mmd_root.display_item_frames["表情"]).keys():
			item = __items(root.mmd_root.display_item_frames["表情"]).add()
			item.type = 'MORPH'
			item.morph_type = "material_morphs"
			item.name = m.name
	for m in root.mmd_root.uv_morphs:
		if m.name not in __items(root.mmd_root.display_item_frames["表情"]).keys():
			item = __items(root.mmd_root.display_item_frames["表情"]).add()
			item.type = 'MORPH'
			item.morph_type = "uv_morphs"
			item.name = m.name
	for m in root.mmd_root.group_morphs:
		if m.name not in __items(root.mmd_root.display_item_frames["表情"]).keys():
			item = __items(root.mmd_root.display_item_frames["表情"]).add()
			item.type = 'MORPH'
			item.morph_type = "group_morphs"
			item.name = m.name

#from pymeshio's englishmap.py
MMD_Standard_Display_Panel_Groups=[
("Root", "Root"),
("Exp", "表情"),
("IK", "ＩＫ"),
("Body[u]", "体(上)"),
("Hair", "髪"),
("Arms", "腕"),
("Fingers", "指"),
("Body[l]", "体(下)"),
("Legs", "足"),
]

Hogarth_Display_Panel_Groups =[
("Root", "Root"),
("Expressions", "表情"),
("IK", "ＩＫ"),
("Head", "頭"),
("Fingers", "指"),
("Hair", "髪"),
("Skirt", "ｽｶｰﾄ"),
("Body", "体(上)"), #I changed it from body to Upper Body to prevent errors
("Other", "その他"),
]

#https://learnmmd.com/http:/learnmmd.com/mmd-bone-reference-charts/
LearnMMD_Display_Panel_Groups =[
('Root', 'Root'),
("Expressions", "表情"),
("IK", "ＩＫ"),
("Head", "頭"),
('Upper Body', '体(上)'),
('Arms', '腕'),
("Fingers", "指"),
('Center', 'センター'),
('Lower Body', '体(下)'),
('Legs', '足'),
('Hair', '髪'),
('Skirt', 'ｽｶｰﾄ'),
("Other", "その他")
]



def display_panel_groups_create(root, armature_object):

	bpy.context.view_layer.objects.active  = armature_object

	#Get bones from the metadata dictionary
	target_columns = ['mmd_english', 'mmd_japanese', 'mmd_japaneseLR', 'blender_rigify', 'ffxiv']
	FFXIV_BONE_METADATA_DICTIONARY = bone_tools.get_csv_bones_by_bone_group("mmd_bone_group_eng", target_columns)


	items_added = []
	
	#If the Groups from LearnMMD_Display_Panel_Groups does not exist, create it
	bpy.context.view_layer.objects.active  = root
	for group in LearnMMD_Display_Panel_Groups:
		if group[1] not in bpy.context.active_object.mmd_root.display_item_frames.keys():
			group_data = bpy.context.active_object.mmd_root.display_item_frames.add()
			group_data.name = group[1]
			group_data.name_e = group[0]
	
	
	for bone in armature_object.data.bones.keys():
		#get all the mmd bone groups
		for mmd_group in LearnMMD_Display_Panel_Groups: 
			#get all the data from FFXIV_BONE_METADATA_DICTIONARY
			for bone_list in FFXIV_BONE_METADATA_DICTIONARY: 
				#if the bone group and bone matches
				if bone_list[0] == mmd_group[0] and bone_list[1]== bone:
					#if the bone hasn't already been added
					if bone not in __items(root.mmd_root.display_item_frames[mmd_group[1]]).keys():
						item = __items(root.mmd_root.display_item_frames[mmd_group[1]]).add()
						item.name = bone
						items_added.append(bone)


	########################START HOGARTH CODE#############################

	bpy.context.view_layer.objects.active  = armature_object

	BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_dictionary()
	FINGER_BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_fingers_dictionary()

	root_names = BONE_NAMES_DICTIONARY[1] # + ["center", "Center", "センター"]
	ik_names = [] # ["IK", "ik", ＩＫ"]
	head_names = ["Head", "head", "頭", "eye", "nose", "tongue", "lip", "jaw", "brow", "cheek", "mouth", "nostril"]
	finger_names = []
	# finger_names = ["finger", "Finger", "指", "thumb", "Thumb", "index", "Index", "mid", "Mid", "middle", "Middle", "Ring", "ring", "Pinky", "pinky", "Fore", "fore", "little", "Little", "Third", "third", "親指", "人指", "中指", "薬指", "小指", "palm"] #not forearm

	hair_names = ["Hair", "hair",'j_ex_h' ,"髪"]
	skirt_names = ["Skirt", "skirt", "スカト", "スカート"]
	body_names = []
	

	#Get all bones from the bone_dictionary.csv and store them in a list
	for b in BONE_NAMES_DICTIONARY:
		if BONE_NAMES_DICTIONARY.index(b) not in [0,1,3]:
			# not in [0,1,3] , not a bonemap ID, not a root bone, not a head bone
			body_names = body_names + list(b)

	#Get all bones from the bones_fingers_dictionary.csv and store them in a list
	for f in FINGER_BONE_NAMES_DICTIONARY:
		finger_names = finger_names + list(f)

	#get all IK pose bones and store them in ik_names
	bpy.ops.object.mode_set(mode='POSE')
	for pb in bpy.context.active_object.pose.bones:
		for c in pb.constraints:
			if c.type == "IK":
				if c.subtarget != '':
					if c.subtarget not in ik_names:
						ik_names.append(c.subtarget)

	#this is used because it is fuzzy logic based on a partial string match
	groups_names_1 = [("ＩＫ", ik_names), ("髪", hair_names), ("頭", head_names),  ("ｽｶｰﾄ", skirt_names)]
	#this is used because it is based on the dictionary files
	groups_names_2 = [("Root", root_names), ("指", finger_names),  ("体(上)", body_names)]

	
	#If the Groups from Hogarth_Display_Panel_Groups does not exist, create it
	bpy.context.view_layer.objects.active  = root
	for g in Hogarth_Display_Panel_Groups:
		if g[1] not in bpy.context.active_object.mmd_root.display_item_frames.keys():
			group = bpy.context.active_object.mmd_root.display_item_frames.add()
			group.name = g[1]
			group.name_e = g[0]
	
	#fuzzy string match based on names
	for b in armature_object.data.bones.keys(): #get all the bones in the armature
		for g in groups_names_1: #IK, hair, head, skirt
			for n in g[1]: #list of ik_names, hair_names, head_names, skirt_names
				#if fuzzy string match
				if n in b:
					#if bone is not already in a display group
					if b not in __items(root.mmd_root.display_item_frames[g[0]]).keys():
						#if bone has not already been added
						if b not in items_added:
							item = __items(root.mmd_root.display_item_frames[g[0]]).add()
							item.name = b
							items_added.append(b)

	#hard-coded dictionary search
	for b in armature_object.data.bones.keys():
		if b not in items_added:
			for g in groups_names_2: 
				for n in g[1]: #list of root_names, finger_names, body_names
					if n == b:
						if b not in __items(root.mmd_root.display_item_frames[g[0]]).keys():
							item = __items(root.mmd_root.display_item_frames[g[0]]).add()
							item.name = b
							items_added.append(b)

	#add all other bones to the 'Other' display group
	for b in armature_object.data.bones.keys():
		if b not in items_added:
			if "shadow" not in b and "dummy" not in b:
				if b not in __items(root.mmd_root.display_item_frames[g[0]]).keys():
					item = __items(root.mmd_root.display_item_frames["Other"]).add()
					item.name = b
					items_added.append(b)
	

	########################END HOGARTH CODE#############################

def main(context):
	armature_object = model.findArmature(bpy.context.active_object)
	bpy.context.view_layer.objects.active = armature_object
	if model.findRoot(bpy.context.active_object) is None:
		bpy.ops.mmd_tools.convert_to_mmd_model()
	root = model.findRoot(bpy.context.active_object)
	mesh_objects_list = model.findMeshesList(bpy.context.active_object)

	if bpy.context.scene.mmd_display_panel_options == 'no_change':
		pass
	if bpy.context.scene.mmd_display_panel_options == 'display_panel_groups_from_bone_groups':
		clear_display_panel_groups(root)
		display_panel_groups_from_bone_groups(root, armature_object)
		display_panel_groups_from_shape_keys(mesh_objects_list)
		display_panel_groups_non_vertex_morphs(root)
		delete_empty_display_panel_groups(root)
	if bpy.context.scene.mmd_display_panel_options == 'add_display_panel_groups':
		clear_display_panel_groups(root)
		display_panel_groups_create(root, armature_object)
		display_panel_groups_from_shape_keys(mesh_objects_list)
		display_panel_groups_non_vertex_morphs(root)
		#delete_empty_display_panel_groups(root)
		#print ("calling 6")

@register_wrap
class MmdToolsDisplayPanelGroups(bpy.types.Operator):
	"""Mass add bone names and shape key names to display panel groups"""
	bl_idname = "ffxiv_mmd_tools_helper.add_display_panel_groups"
	bl_label = "Create Display Panel Groups"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.mmd_display_panel_options = bpy.props.EnumProperty(items = [\
				('add_display_panel_groups', 'Auto-Generate', 'Automatically Create All MMD Display Panel Groups')\
				, ('display_panel_groups_from_bone_groups', 'Copy from Blender Bone Groups', 'Copy Display Panel Groups from Blender Bone Groups')\
				], name = "", default = 'add_display_panel_groups')

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		root = mmd_model.Model.findRoot(obj)
		return obj is not None and obj.type == 'ARMATURE' and root is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}