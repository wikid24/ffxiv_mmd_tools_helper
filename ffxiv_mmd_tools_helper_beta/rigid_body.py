import bpy
from . import register_wrap
from . import model
from mmd_tools.operators.rigid_body import AddRigidBody
from . import import_csv


@register_wrap
class RigidBodyPanel(bpy.types.Panel):
	"""Rigid Body panel"""
	bl_label = "Rigid Body panel"
	bl_idname = "OBJECT_PT_rigid_body_panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "ffxiv_mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="Find this string in bone names:")
		row = layout.row()
		row.prop(context.scene,"find_bone_to_add")
		row = layout.row()
		row.label(text="Replace it with this string:")
		row = layout.row()
		row.prop(context.scene,"rigid_body_name")
		row = layout.row()
		row.prop(context.scene, "rigid_bodies_all")
		row = layout.row()
		row.label(text="Selected rigid_bodies only")
		row = layout.row()
		row.operator("ffxiv_mmd_tools_helper.add_rigid_body", text = "Add Rigid Bodies to armature")
		row = layout.row()


def read_rigid_body_file():
	#if test_is_mmd_english_armature() == True:
	#	bpy.ops.object.mode_set(mode='EDIT')
	
	RIGID_BODY_DICTIONARY = None
	#bpy.context.view_layer.objects.active  = model.findArmature(bpy.context.active_object)

	RIGID_BODY_DICTIONARY = import_csv.use_csv_rigid_body_dictionary()

	#convert the rigid_body_data list into a dictionary with a header
	RIGID_BODY_DICTIONARY = [dict(zip(RIGID_BODY_DICTIONARY[0],row)) for row in RIGID_BODY_DICTIONARY[1:]]

	#convert the values in 'collision_group_mask' into a boolean list
	for row in RIGID_BODY_DICTIONARY:
		if (row['collision_group_mask'] == 0.0):
			row['collision_group_mask'] = str('')
		index_values = str(row['collision_group_mask']).split('/')
		bool_list = [str(i) in index_values for i in range(16)]
		row['collision_group_mask'] = bool_list



	#if test_is_mmd_english_armature() == False:
	#	print("This operator will only work on an armature with mmd_english bone names. First rename bones to mmd_english and then try running this operator again.")

	return RIGID_BODY_DICTIONARY


def apply_all_rigid_bodies(armature,rigid_body_data):


	
	if rigid_body_data: 
		for rigid_body in rigid_body_data:
			rigid_body_name = rigid_body['rigid_body_name']
			bone = rigid_body['bone_name']
			offset_loc = [rigid_body['offset_x'],rigid_body['offset_y'],rigid_body['offset_z']]
			name_j = rigid_body['name_j']
			name_e = rigid_body['name_e']
			collision_group_number = int(rigid_body['collision_group'])
			collision_group_mask = rigid_body['collision_group_mask']
            #collision_group_mask = [True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False] 

			rigid_type = str(int(rigid_body['rigid_type'])) #'0'= Bone, '1' = Physics, '2' = Physics+Bone
			rigid_shape = rigid_body['rigid_shape']  #SPHERE, BOX, CAPSULE        
			size = [rigid_body['x'], rigid_body['y'],rigid_body['z']]  #size[0] = X, size[1] = Y, size[2] = Z
			mass = rigid_body['mass']
			friction = rigid_body['friction'] 
			bounce = rigid_body['bounce']  #restitution
			linear_damping = rigid_body['linear_damping']
			angular_damping = rigid_body['angular_damping']
			
			bpy.context.view_layer.objects.active = armature         
			create_rigid_body(armature,rigid_body_name,bone,offset_loc,name_j,name_e,collision_group_number,collision_group_mask, rigid_type,rigid_shape,size,mass,friction,bounce,linear_damping,angular_damping)
	

def create_rigid_body(armature,rigid_body_name,bone,offset_loc,name_j,name_e,collision_group_number,collision_group_mask, rigid_type,rigid_shape,size,mass,friction,bounce,linear_damping,angular_damping):

	#check if bone exists
	if bone in armature.data.bones:

		#if rigid body exists, delete it
		for obj in armature.parent.children_recursive:
			if obj.mmd_type == 'RIGID_BODY' and obj.name == rigid_body_name:
				# Delete the object
				bpy.data.objects.remove(obj, do_unlink=True)
		
		"""
		name_j = '$name_j'
		name_e = '$name_e'
		collision_group_number = 0
		collision_group_mask = [True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False] 
		rigid_type = '0' #'0'= Bone, '1' = Physics, '2' = Physics+Bone
		rigid_shape = 'SPHERE' #SPHERE, BOX, CAPSULE
		size = [0.6, 0.6, 0.6]  #size[0] = X, size[1] = Y, size[2] = Z
		mass = 1 
		friction = 0.5
		bounce = 0 #restitution
		linear_damping = 0.04
		angular_damping = 0.1
		"""
		# Set mode as edit mode
		bpy.ops.object.mode_set(mode='EDIT')

		# Set active bone
		#armature = bpy.context.object
		#bpy.context.view_layer.objects.active = armature
		bpy.ops.object.mode_set(mode='EDIT')

		# Select the bone
		bpy.ops.armature.select_all(action='DESELECT')
		armature.data.edit_bones[bone].select = True
		armature.data.bones.active = armature.data.bones[bone]
			
		bpy.ops.mmd_tools.rigid_body_add(
			name_j= name_j
			,name_e= name_e
			,collision_group_number=collision_group_number
			,collision_group_mask=collision_group_mask
			,rigid_type=rigid_type
			,rigid_shape=rigid_shape
			,size=size
			,mass=mass
			,friction=friction
			,bounce=bounce
			,linear_damping=linear_damping
			,angular_damping=angular_damping
		)
		
		rigid_body = bpy.context.view_layer.objects.active

		#set rigid_body_name
		rigid_body.name = rigid_body_name

			
		#set the size to match what the MMD Rigid Body Panel displays as the size
		if rigid_shape == 'SPHERE':
			rigid_body.mmd_rigid.size = (max(size[0], 1e-3)\
											,0\
											,0 )
		elif rigid_shape == 'BOX':
			rigid_body.mmd_rigid.size = (max(size[0], 1e-3)\
										,max(size[1] , 1e-3)\
										,max(size[2] , 1e-3))
			
			
			#rigid_body.mmd_rigid.size[0] = max(size[0] , 1e-3)
			#rigid_body.mmd_rigid.size[1] = max(size[1] , 1e-3)
			#rigid_body.mmd_rigid.size[2] = max(size[2] , 1e-3)
			
		elif rigid_shape == 'CAPSULE':
			rigid_body.mmd_rigid.size = (max(size[0], 1e-3) \
										,max(size[1], 1e-3) \
										,0)
			
			#rigid_body.mmd_rigid.size[0] = (max(size[0], 1e-3)
			#rigid_body.mmd_rigid.size[1] = max(size[1], 1e-3)
			
		#set the offset
		#rigid_body.delta_location.x = offset_loc[0]
		#rigid_body.delta_location.y = offset_loc[1]
		#rigid_body.delta_location.z = offset_loc[2]
		rigid_body.location.x = rigid_body.location.x + offset_loc[0]
		rigid_body.location.y = rigid_body.location.y + offset_loc[1]
		rigid_body.location.z = rigid_body.location.z + offset_loc[2]
		
		
		return rigid_body
	else:
		print ('bone ',bone,' does not exist')
 
 


def main(context):
	bpy.context.view_layer.objects.active = model.findArmature(bpy.context.active_object)
	armature = bpy.context.view_layer.objects.active
	"""
	if bpy.context.scene.bones_all_or_selected == True:
		for b in bpy.context.active_object.data.bones:
			if b.select == True:
				if 'dummy' not in b.name and 'shadow' not in b.name:
					b.name = b.name.replace(bpy.context.scene.find_bone_string, bpy.context.scene.replace_bone_string)
	if bpy.context.scene.bones_all_or_selected == False:
		for b in bpy.context.active_object.data.bones:
			if 'dummy' not in b.name and 'shadow' not in b.name:
				b.name = b.name.replace(bpy.context.scene.find_bone_string, bpy.context.scene.replace_bone_string)
	"""

	RIGID_BODY_DICTIONARY = read_rigid_body_file ()
	
	apply_all_rigid_bodies(armature, RIGID_BODY_DICTIONARY)
	#apply_all_rigid_bodies(armature)





@register_wrap
class AddRigidBody(bpy.types.Operator):
	"""Add Rigid Body properties to a MMD Model"""
	bl_idname = "ffxiv_mmd_tools_helper.add_rigid_body"
	bl_label = "Replace bones renaming"

	bpy.types.Scene.find_bone_to_add = bpy.props.StringProperty(name="", description="", default="", maxlen=0, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)
	
	bpy.types.Scene.rigid_body_name = bpy.props.StringProperty(name="", description="", default="", maxlen=0, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)

	bpy.types.Scene.rigid_bodies_all = bpy.props.BoolProperty(name="Selected bones only", description="", default=False, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}