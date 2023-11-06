import bpy
#import mathutils
from . import register_wrap
from . import model
from . import import_csv
#from mmd_tools.core.bone import FnBone
#import mmd_tools.core.model as mmd_model
#from . import miscellaneous_tools
from . import bone_tools
#from . import add_foot_leg_ik
#from . import add_hand_arm_ik


def adjust_metarig_scale(mmd_armature,metarig_armature):



		if mmd_armature and metarig_armature:    
			# Clear the selection (optional)
			bpy.ops.object.select_all(action='DESELECT')

			# Select the armature (optional)
			metarig_armature.select_set(True)
			mmd_armature.select_set(True)
			bpy.context.view_layer.objects.active = metarig_armature
			
			#go to edit mode
			bpy.ops.object.mode_set(mode='EDIT')
			bpy.context.view_layer.objects.active = mmd_armature
			metarig_height = metarig_armature.data.edit_bones['spine.004'].head[2]
			neck_bone_name = bone_tools.get_armature_bone_name_by_mmd_english_bone_name(mmd_armature,'neck')
			armature_height = mmd_armature.data.edit_bones[neck_bone_name].head[2]
			
			#metarig_neck.select = True
			#armature_neck.select = True
			
			print (f"metarig_height: {metarig_height}")           
			print (f"armature_height: {armature_height}")

			scale = armature_height / metarig_height
			print (f"scale: {scale}") 
			metarig_armature.scale = (scale,scale,scale)

			bpy.ops.object.mode_set(mode='OBJECT')
			bpy.ops.object.transform_apply(scale=True)


			
def adjust_metarig_bone_positions(mmd_armature,metarig_armature):
	
	bpy.ops.object.mode_set(mode='EDIT')

	metarig_to_mmd_bone_mapping = {}

	#for each bone in metarig_armature, check for mmd_english name
	for metarig_bone in metarig_armature.data.edit_bones:
		rigify_bone_name_mmd_english = None

		#get the metarig bone name in mmd_english
		rigify_bone_name_mmd_english =  bone_tools.get_mmd_english_equivalent_bone_name(metarig_bone.name)
		if rigify_bone_name_mmd_english:

			metarig_to_mmd_bone_mapping[rigify_bone_name_mmd_english] = (metarig_bone,None)
			#print(metarig_to_mmd_bone_mapping[metarig_bone.name])
			#print (f"metarig bone name: {metarig_bone.name}, mmd_english: {rigify_bone_name_mmd_english}")
	
	############

	#for each bone in metarig_armature, check for mmd_english name
	for mmd_armature_bone in mmd_armature.data.edit_bones:
		mmd_armature_bone_mmd_english = None
		#get the mmd_armature bone name in mmd_english
		mmd_armature_bone_mmd_english =  bone_tools.get_mmd_english_equivalent_bone_name(mmd_armature_bone.name)
		if mmd_armature_bone_mmd_english and mmd_armature_bone_mmd_english in metarig_to_mmd_bone_mapping:
			metarig_to_mmd_bone_mapping[mmd_armature_bone_mmd_english] = (metarig_to_mmd_bone_mapping[mmd_armature_bone_mmd_english][0],mmd_armature_bone)

	############
	#for each bone in metarig_to_mmd_bone_mapping, check if exists on mmd_armature
	for x in metarig_to_mmd_bone_mapping:
		#if bone both found on mmd_armature AND rigify armature
		if metarig_to_mmd_bone_mapping[x][0] and metarig_to_mmd_bone_mapping[x][1]:
			move_target_bone_to_source_bone (mmd_armature,metarig_to_mmd_bone_mapping[x][1],metarig_armature,metarig_to_mmd_bone_mapping[x][0])
			#print (metarig_to_mmd_bone_mapping[x])

	########## next is bone cleanup
	target_bone = metarig_armature.data.edit_bones['thumb.01.L']
	source_bone = mmd_armature.data.edit_bones['thumb1_L']

	target_bone.head = source_bone.head
	target_bone.tail = source_bone.tail
	target_bone.length = target_bone.length * 0.4


	target_bone = metarig_armature.data.edit_bones['thumb.01.R']
	source_bone = mmd_armature.data.edit_bones['thumb1_R']

	target_bone.head = source_bone.head
	target_bone.tail = source_bone.tail
	target_bone.length = target_bone.length * 0.4

	
	adjust_extra_finger_bone(metarig_armature,mmd_armature,'fore2_L','fore3_L')
	adjust_extra_finger_bone(metarig_armature,mmd_armature,'middle2_L','middle3_L')
	adjust_extra_finger_bone(metarig_armature,mmd_armature,'third2_L','third3_L')
	adjust_extra_finger_bone(metarig_armature,mmd_armature,'little2_L','little3_L')
	adjust_extra_finger_bone(metarig_armature,mmd_armature,'fore2_R','fore3_R')
	adjust_extra_finger_bone(metarig_armature,mmd_armature,'middle2_R','middle3_R')
	adjust_extra_finger_bone(metarig_armature,mmd_armature,'third2_R','third3_R')
	adjust_extra_finger_bone(metarig_armature,mmd_armature,'little2_R','little3_R')	

	adjust_palm_bone(metarig_armature,mmd_armature,'fore1_L','palm.01.L')
	adjust_palm_bone(metarig_armature,mmd_armature,'middle1_L','palm.02.L')	
	adjust_palm_bone(metarig_armature,mmd_armature,'third1_L','palm.03.L')	
	adjust_palm_bone(metarig_armature,mmd_armature,'little1_L','palm.04.L')	
	adjust_palm_bone(metarig_armature,mmd_armature,'fore1_R','palm.01.R')
	adjust_palm_bone(metarig_armature,mmd_armature,'middle1_R','palm.02.R')	
	adjust_palm_bone(metarig_armature,mmd_armature,'third1_R','palm.03.R')	
	adjust_palm_bone(metarig_armature,mmd_armature,'little1_R','palm.04.R')	

	#fix the spine on the rig
	metarig_armature.data.edit_bones['spine'].head = mmd_armature.data.edit_bones['lower body'].tail

	metarig_armature.data.edit_bones['spine.003'].tail = metarig_armature.data.edit_bones['spine.004'].head
	#metarig_armature.data.edit_bones['spine.003'].use_connect = True
	metarig_armature.data.edit_bones['spine.004'].tail = metarig_armature.data.edit_bones['spine.005'].head
	#metarig_armature.data.edit_bones['spine.004'].use_connect = True


	#if match found, move metarig_armatue bone position to mmd_armature bone position

def adjust_extra_finger_bone(metarig_armature,mmd_armature,mmd_e_source_bone_name,mmd_e_extra_finger_bone_name):
	mmd_source_bone_name =  bone_tools.get_armature_bone_name_by_mmd_english_bone_name(mmd_armature,mmd_e_source_bone_name)
	mmd_extra_finger_bone_name =  bone_tools.get_armature_bone_name_by_mmd_english_bone_name(mmd_armature,mmd_e_extra_finger_bone_name)
	rigify_source_bone_name = bone_tools.get_bone_name_by_mmd_english_bone_name(mmd_e_source_bone_name,'blender_rigify')
	rigify_extra_finger_bone_name = bone_tools.get_bone_name_by_mmd_english_bone_name(mmd_e_extra_finger_bone_name,'blender_rigify')

	#print(mmd_source_bone_name, ' ' , mmd_extra_finger_bone_name, ' ',rigify_source_bone_name, ' ', rigify_extra_finger_bone_name)

	if mmd_extra_finger_bone_name is None:

		mmd_source_bone = mmd_armature.data.edit_bones[mmd_source_bone_name]
		rigify_source_bone = metarig_armature.data.edit_bones[rigify_source_bone_name]
		rigify_extra_finger_bone = metarig_armature.data.edit_bones[rigify_extra_finger_bone_name]

		rigify_source_bone.head = mmd_source_bone.head
		rigify_source_bone.tail = mmd_source_bone.tail
		rigify_source_bone.length = rigify_source_bone.length/2
		rigify_extra_finger_bone.head = rigify_source_bone.tail
		rigify_extra_finger_bone.tail = mmd_source_bone.tail
		rigify_extra_finger_bone.roll = mmd_source_bone.roll

def adjust_palm_bone(metarig_armature,mmd_armature,mmd_e_source_bone_name,metarig_bone_name):
	mmd_source_bone_name =  bone_tools.get_armature_bone_name_by_mmd_english_bone_name(mmd_armature,mmd_e_source_bone_name)
	mmd_source_bone = mmd_armature.data.edit_bones[mmd_source_bone_name]
	metarig_bone = metarig_armature.data.edit_bones[metarig_bone_name]

	metarig_bone.head = mmd_source_bone.head
	metarig_bone.tail = mmd_source_bone.tail
	metarig_bone.length = metarig_bone.length * -1
	new_head = metarig_bone.tail.copy()
	new_tail = metarig_bone.head.copy()
	metarig_bone.head = new_head
	metarig_bone.tail = new_tail
	metarig_bone.roll = mmd_source_bone.roll
	


def move_target_bone_to_source_bone (source_armature,source_bone,target_armature,target_bone):
	#print(f"source_armature: {source_armature.name},source_bone: {source_bone.name}, target_armature: {target_armature.name}, target_bone: {target_bone.name}")
	target_bone.head = source_bone.head
	target_bone.tail = source_bone.tail
	target_bone.roll = source_bone.roll


def adjust_metarig_bones(context):
	armature = bpy.context.view_layer.objects.active

	mmd_armature = None
	metarig_armature = None
	
	if bpy.context.active_object.mode == 'OBJECT':
	
		obj = bpy.context.active_object
		
		if obj and obj.type =='ARMATURE' and obj.name != 'metarig':
			mmd_armature = obj    
			

		# Iterate through all objects in the scene
		for obj in bpy.context.scene.objects:
			if obj.type == 'ARMATURE' and obj.name == 'metarig':
				# Armature with the name 'metarig' found
				metarig_armature = obj

				break  # Stop searching once you've found the armature

	if mmd_armature and metarig_armature:    
		adjust_metarig_scale(mmd_armature,metarig_armature)
		adjust_metarig_bone_positions(mmd_armature,metarig_armature)
		
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.context.view_layer.objects.active = metarig_armature
		


def apply_metarig (mmd_armature, metarig_armature):
		
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.context.view_layer.objects.active = metarig_armature

	#generates the rig
	bpy.ops.pose.rigify_generate()

	#select all meshes from mmd armature and sets the parent to the rig
	
	bpy.ops.object.select_all(action='DESELECT')
	#bpy.context.view_layer.objects.active = mmd_armature
	for obj in mmd_armature.parent.children_recursive:
		if obj.type == 'MESH':
			obj.select = True


	# Iterate through all objects in the current scene
	for obj in bpy.context.scene.objects:
		if obj.type == 'ARMATURE' and obj.name == 'rig':
			# Armature with the name 'rig' found
			rigify_armature = obj
			rigify_armature.select = True
			bpy.context.view_layer.objects.active = rigify_armature
			break  # Stop searching once you've found the armature

		
	bpy.ops.object.parent_set(type='ARMATURE_AUTO')

	#delete the metarig armature
	if metarig_armature:
		
		bpy.ops.object.mode_set(mode='OBJECT')
		# Ensure the armature is in object mode (not in pose or edit mode)
		bpy.ops.object.select_all(action='DESELECT')
		bpy.context.view_layer.objects.active = metarig_armature

		# Select the armature object
		metarig_armature.select_set(True)

		# Delete the selected object(s)
		bpy.ops.object.delete()



	


@register_wrap
class AddRigify_Metarig(bpy.types.Operator):
	"""Adds a Rigify Metarig to the Scene"""
	bl_idname = "ffxiv_mmd.add_rigify_metarig"
	bl_label = "Add Rigify Metarig"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE' and obj.name not in ('metarig','rig')

	def execute(self, context):
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		armature = bpy.context.view_layer.objects.active
		bpy.ops.object.armature_human_metarig_add()

		#lock_position_rotation_bones(armature)
		return {'FINISHED'}
	
@register_wrap
class Adjust_Metarig(bpy.types.Operator):
	"""Adjusts a Rigify Metarig to the Model"""
	bl_idname = "ffxiv_mmd.adjust_metarig_bones"
	bl_label = "Adjust Metarig Bones"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE' and obj.name not in ('metarig','rig')

	def execute(self, context):
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		
		adjust_metarig_bones(context)
		

		#lock_position_rotation_bones(armature)
		return {'FINISHED'}
	
@register_wrap
class Apply_Metarig(bpy.types.Operator):
	"""Adjusts a Rigify Metarig to the Model"""
	bl_idname = "ffxiv_mmd.apply_metarig"
	bl_label = "Apply Rigify Metarig"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.type == 'ARMATURE' and obj.name not in ('metarig','rig')

	def execute(self, context):
		#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)
		obj = context.active_object

		target_armature = None
		metarig_armature = None

		if obj.type == 'ARMATURE':
			target_armature = obj


		# Iterate through all objects in the current scene
		for obj in bpy.context.scene.objects:
			if obj.type == 'ARMATURE' and obj.name == 'metarig':
				metarig_armature = obj
				break  # Stop searching once you've found the 'metarig' armature

		if target_armature and metarig_armature:
			apply_metarig(target_armature,metarig_armature)
		

		#lock_position_rotation_bones(armature)
		return {'FINISHED'}