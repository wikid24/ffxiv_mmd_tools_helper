import bpy
from . import register_wrap
from . import model
from mmd_tools.operators.rigid_body import AddRigidBody
from . import import_csv
from mmd_tools.core import model as mmd_model

def read_rigid_body_file():
	
	RIGID_BODY_DICTIONARY = None
	RIGID_BODY_DICTIONARY = import_csv.use_csv_rigid_body_dictionary()

	#convert the list into a dictionary with a header
	RIGID_BODY_DICTIONARY = [dict(zip(RIGID_BODY_DICTIONARY[0],row)) for row in RIGID_BODY_DICTIONARY[1:]]

	#convert the values in 'collision_group_mask' into a boolean list
	for row in RIGID_BODY_DICTIONARY:
		#print(row['collision_group_mask'])
		#if (row['collision_group_mask']) == 0.0:
			#row['collision_group_mask'] = str('0')
		if isinstance(row['collision_group_mask'], float):
			row['collision_group_mask'] = str(int(row['collision_group_mask']))
		index_values = str(row['collision_group_mask']).split('\\')
		bool_list = [str(i) in index_values for i in range(16)]
		row['collision_group_mask'] = bool_list
		#print('converted to',row['collision_group_mask'])

	return RIGID_BODY_DICTIONARY

def get_armature():
	
	if bpy.context.active_object.type == 'ARMATURE':
		return model.findArmature(bpy.context.active_object)
	if model.findArmature(bpy.context.selected_objects[0]) is not None:
		return model.findArmature(bpy.context.selected_objects[0])
	for child in  bpy.context.selected_objects[0].parent.children:
		if child.type == 'ARMATURE':
			return child
	for child in  bpy.context.selected_objects[0].parent.parent.children:
		if child.type == 'ARMATURE':
			return child
	else:
		print ('could not find armature for selected object:', bpy.context.selected_objects[0].name)

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

	
	
	#if rigid body exists, delete it
	for obj in armature.parent.children_recursive:
		if obj.mmd_type == 'RIGID_BODY' and obj.name == rigid_body_name:
			print ('deleting existing rigid_body:', obj.name)
			bpy.data.objects.remove(obj, do_unlink=True)

	
	#check if bone exists
	bpy.ops.object.mode_set(mode='EDIT')
	if bone in bpy.context.active_object.data.edit_bones:

		
		"""
		name_j = '$name_j'
		name_e = '$name_e'
		collision_group_number = 0
		collision_group_mask = [True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False] 
		rigid_type = '0' #'0'= Bone, '1' = Physics, '2' = Physics+Bone
		rigid_shape = 'SPHERE' #SPHERE, BOX, CAPSULE
		size = [0.6, 0.6, 0.6]  #X, Y, Z
		mass = 1 
		friction = 0.5
		bounce = 0 #restitution
		linear_damping = 0.04
		angular_damping = 0.1
		"""
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
			rigid_body.mmd_rigid.size = [max(size[0], 1e-3),0,0] #radius,y,z
		elif rigid_shape == 'BOX':
			rigid_body.mmd_rigid.size = [max(size[0], 1e-3),max(size[1] , 1e-3),max(size[2] , 1e-3)] #x,y,z
		elif rigid_shape == 'CAPSULE':
			rigid_body.mmd_rigid.size = [max(size[0], 1e-3),max(size[1], 1e-3),0] #radius,diameter,z
			
		#set the offset
		#rigid_body.delta_location.x = offset_loc[0]
		#rigid_body.delta_location.y = offset_loc[1]
		#rigid_body.delta_location.z = offset_loc[2]
		rigid_body.location.x = rigid_body.location.x + offset_loc[0]
		rigid_body.location.y = rigid_body.location.y + offset_loc[1]
		rigid_body.location.z = rigid_body.location.z + offset_loc[2]
		
		print ('created rigid body: ',rigid_body.name)
		return rigid_body
	else:
		print ('bone ',bone,' does not exist')
 

import bpy
import re
import math

#string = "skirt_8_12"


def get_skirt_rigid_vertical_objects(obj):
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    if obj.mmd_type == 'RIGID_BODY' and obj.name.startswith('skirt_'):

        #get the skirt chain number (first number after skirt_)
        result = re.search("^skirt_(\d+)_(\d+)$", obj.name)
        if result:
            chain_number = int(result.group(1))
            print("Captured value:", chain_number )
        else:
            print("No match found.")
            
        rb_obj_chain = []
                
        armature = bpy.context.active_object.constraints['mmd_tools_rigid_parent'].target
        bone_name = bpy.context.active_object.constraints['mmd_tools_rigid_parent'].subtarget
        rigid_bodies = None

        #get the 'rigidbodies' object
        for object in armature.parent.children:
            if object.name == 'rigidbodies':
                rigid_bodies = object
        
        if rigid_bodies is not None:
            #get all rigid bodies that have the same chain number as object that was passed
            for rigid_body in rigid_bodies.children:
                
                #if it finds it, add it to the rb_obj_chain list
                if rigid_body.name.startswith('skirt_'+str(chain_number)+'_') and rigid_body.mmd_type == 'RIGID_BODY':
                    rb_obj_chain.append(rigid_body)
        
        if rb_obj_chain is not None:
            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')
            #select all in chain    
            for rb_obj in rb_obj_chain:
                rb_obj.select_set(True)
                
            return rb_obj_chain
                
def get_skirt_rigid_horizontal_objects(obj):
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    if obj.mmd_type == 'RIGID_BODY' and obj.name.startswith('skirt_'):
        #get the skirt chain number (last number after skirt_)
        result = re.search("^skirt_(\d+)_(\d+)$", obj.name)
        if result:
            chain_number = int(result.group(2))
            print("Captured value:", chain_number )
        else:
            print("No match found.")
            
        rb_obj_chain = []
        
        armature = bpy.context.active_object.constraints['mmd_tools_rigid_parent'].target
        bone_name = bpy.context.active_object.constraints['mmd_tools_rigid_parent'].subtarget
        rigid_bodies = None

        #get the 'rigidbodies' object
        for object in armature.parent.children:
            if object.name == 'rigidbodies':
                rigid_bodies = object
        
        if rigid_bodies is not None:
            #get all rigid bodies that have the same chain number as object that was passed
            for rigid_body in rigid_bodies.children:
                
                #if it finds it, add it to the rb_obj_chain list
                if rigid_body.name.endswith('_'+str(chain_number)) and rigid_body.mmd_type == 'RIGID_BODY':
                    rb_obj_chain.append(rigid_body)        
                
        if rb_obj_chain is not None:
            
            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')
        
            #select all in chain    
            for rb_obj in rb_obj_chain:
                rb_obj.select_set(True)
        
            return rb_obj_chain

def transform_rigid_body(obj=None
						,rotation_x = None,rotation_y=None,rotation_z=None
						,size_x=None,size_y=None,size_z=None
						,rigid_body_type=None, rigid_body_shape=None,mass=None,restitution=None
						,collision_group_number=None, collision_group_mask=None, friction=None
						,linear_damping=None,angular_damping=None):

	
	if obj is None:
		if bpy.context.active_object.mmd_type == 'RIGID_BODY':
			obj=bpy.context.active_object
	#obj.rotation_mode


	if rotation_x is not None:
		obj.rotation_euler.x = rotation_x
	if rotation_y is not None:
		obj.rotation_euler.y = rotation_y
	if rotation_z is not None:
		obj.rotation_euler.z = rotation_z
	if rigid_body_shape is not None:
		#BOX
		#SPHERE
		#CAPSULE
		obj.mmd_rigid.shape = rigid_body_shape
	if (size_x or size_y or size_z):
		if size_x is None:
			size_x = obj.mmd_rigid.size[0]    
		if size_y is None:
			size_y = obj.mmd_rigid.size[1]    
		if size_z is None:
			size_z = obj.mmd_rigid.size[2] 
		obj.mmd_rigid.size = [max(size_x, 1e-3),max(size_y , 1e-3),max(size_z, 1e-3)]
	if rigid_body_type is not None:
		obj.mmd_rigid.type = rigid_body_type
		#'0' = bone
		#'1' = physics
		#'2' = physics+bone

	if mass is not None:
		obj.rigid_body.mass = mass
	if restitution is not None:
		obj.rigid_body.restitution = restitution 
	if collision_group_number is not None:
		obj.mmd_rigid.collision_group_number = collision_group_number
	if collision_group_mask is not None:
		obj.mmd_rigid.collision_group_mask = collision_group_mask
		#collision_group_mask = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
	if friction is not None:
		obj.rigid_body.friction = friction
	if linear_damping is not None:
		obj.rigid_body.linear_damping = linear_damping
	if angular_damping is not None:
		obj.rigid_body.angular_damping 



def transform_selected_rigid_bodies(rotation_x = None,rotation_y=None,rotation_z=None
									,size_x=None,size_y=None,size_z=None
									,rigid_body_type=None, rigid_body_shape=None,mass=None,restitution=None
									,collision_group_number=None, collision_group_mask=None, friction=None
									,linear_damping=None,angular_damping=None):
	
	selected_objects = bpy.context.selected_objects
	
	is_all_rigid_bodies = True
	
	for sel_objs in selected_objects:
		if sel_objs.mmd_type != 'RIGID_BODY':
			is_all_rigid_bodies = False
			
	if is_all_rigid_bodies:        
		for obj in selected_objects:

			transform_rigid_body(obj
								,rotation_x,rotation_y,rotation_z
								,size_x,size_y,size_z
								,rigid_body_type, rigid_body_shape,mass,restitution
								,collision_group_number, collision_group_mask, friction
								,linear_damping,angular_damping)

	else: 
		print('Not all selected objects are rigid bodies. Select only rigid bodies')
    


def create_rigid_bodies_from_csv(context):
	bpy.context.view_layer.objects.active = get_armature()
	armature = get_armature()

	RIGID_BODY_DICTIONARY = read_rigid_body_file ()
	
	apply_all_rigid_bodies(armature, RIGID_BODY_DICTIONARY)
	#apply_all_rigid_bodies(armature)

@register_wrap
class AddRigidBody(bpy.types.Operator):
	"""Add Rigid Bodies to a FFXIV Model (Converted to an MMD Model)"""
	bl_idname = "ffxiv_mmd_tools_helper.add_rigid_body"
	bl_label = "Add Rigid Bodies from CSV"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		root = mmd_model.Model.findRoot(obj)
		return obj is not None and obj.type == 'ARMATURE' and root is not None

	def execute(self, context):
		create_rigid_bodies_from_csv(context)
		return {'FINISHED'}


@register_wrap
class SelectVerticalSkirtRigidBodies(bpy.types.Operator):
	"""Select All Rigid Bodies in the vertical rigid body skirt chain"""
	bl_idname = "ffxiv_mmd_tools_helper.get_vertical_skirt_rigid_bodies"
	bl_label = "Replace bones renaming"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.mmd_type == 'RIGID_BODY' and obj.name.startswith('skirt_')

	def execute(self, context):
		get_skirt_rigid_vertical_objects(context.active_object)
		return {'FINISHED'}

@register_wrap
class SelectHorizontalSkirtRigidBodies(bpy.types.Operator):
	"""Select All Rigid Bodies in the horizontal rigid body skirt chain with the same number"""
	bl_idname = "ffxiv_mmd_tools_helper.get_horizontal_skirt_rigid_bodies"
	bl_label = "Replace bones renaming"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		return obj is not None and obj.mmd_type == 'RIGID_BODY' and obj.name.startswith('skirt_')

	def execute(self, context):
		get_skirt_rigid_horizontal_objects(context.active_object)
		return {'FINISHED'}

def _transform_rigid_body(self,context):

	obj = context.active_object

	transform_rigid_body(
				obj=obj,
				rotation_x=self.rotation_x if self.rotation_x is not None else None,
				rotation_y=self.rotation_y if self.rotation_y is not None else None,
				rotation_z=self.rotation_z if self.rotation_z is not None else None,
				size_x=self.size_x if self.size_x is not None else None,
				size_y=self.size_y if self.size_y is not None else None,
				size_z=self.size_z if self.size_z is not None else None,
				rigid_body_type=self.rigid_body_type if self.rigid_body_type is not None else None,
				rigid_body_shape=self.rigid_body_shape if self.rigid_body_shape is not None else None,
				mass=self.mass if self.mass is not None else None,
				restitution=self.restitution if self.restitution is not None else None,
				collision_group_number=self.collision_group_number if self.collision_group_number is not None else None,
				collision_group_mask=self.collision_group_mask if self.collision_group_mask is not None else None,
				friction=self.friction if self.friction is not None else None,
				linear_damping=self.linear_damping if self.linear_damping is not None else None,
				angular_damping=self.angular_damping if self.angular_damping is not None else None,
			)


@register_wrap
class BatchUpdateRigidBodies(bpy.types.Operator):
	bl_idname = "ffxiv_mmd_tools_helper.batch_update_rigid_bodies"
	bl_label = "Batch Update Rigid Bodies"
	bl_options = {'REGISTER', 'BLOCKING','UNDO','PRESET'}

	rotation_x: bpy.props.FloatProperty(min =0,unit='ROTATION',update=_transform_rigid_body)
	rotation_y: bpy.props.FloatProperty(min=0,unit='ROTATION',update=_transform_rigid_body)
	rotation_z: bpy.props.FloatProperty(min =0,unit='ROTATION',update=_transform_rigid_body)
	size_x: bpy.props.FloatProperty(min=0,update=_transform_rigid_body)
	size_y: bpy.props.FloatProperty(min=0,update=_transform_rigid_body)
	size_z: bpy.props.FloatProperty(min=0,update=_transform_rigid_body)
	rigid_body_type: bpy.props.EnumProperty(items=[\
			('0','Bone','Bone')\
			,('1','Physics','Physics')\
			,('2','Physics + Bone','Physics + Bone')\
			],update=_transform_rigid_body)
	rigid_body_shape: bpy.props.EnumProperty(items=[\
			('SPHERE','Sphere','Sphere')\
			,('BOX','Box','Box')\
			,('CAPSULE','Capsule','Capsule')\
			],update=_transform_rigid_body)
	mass: bpy.props.FloatProperty(min=0.001, unit='MASS',update=_transform_rigid_body)
	restitution: bpy.props.FloatProperty(min=0,max=1,update=_transform_rigid_body)
	collision_group_number: bpy.props.IntProperty(min=0, max=15,update=_transform_rigid_body)
	collision_group_mask: bpy.props.BoolVectorProperty(size=16,update=_transform_rigid_body)
	friction: bpy.props.FloatProperty(min=0,max=1,update=_transform_rigid_body)
	linear_damping: bpy.props.FloatProperty(min=0, max=1,update=_transform_rigid_body)
	angular_damping: bpy.props.FloatProperty(min=0,max = 1,update=_transform_rigid_body)

	def draw(self, context):
		layout = self.layout

		armature_name = context.active_object.constraints['mmd_tools_rigid_parent'].target
		bone_name = context.active_object.constraints['mmd_tools_rigid_parent'].subtarget
		

		row = layout.row()
		row.label(text='Active Object:'+ context.active_object.name)
		
		row.label(text='Bone:'+ bone_name)

		c = layout.column(align=True)
		row = c.row(align=True)
		row.prop(self, 'rotation_x')
		row.prop(self, 'rotation_y')
		row.prop(self, 'rotation_z')

		c = layout.column(align=True)
		row = c.row(align=True)
		row.prop(self, 'rigid_body_type', expand=True)

		c = layout.column(align=True)
		c.row(align=True).prop(self, 'rigid_body_shape', expand=True)

		col = c.column(align=True)
		if self.rigid_body_shape == 'BOX':
			c.prop(self,'size_x',text = 'Size X')
			c.prop(self,'size_y',text = 'Size Y')
			c.prop(self,'size_z',text = 'Size Z')
		elif self.rigid_body_shape == 'CAPSULE':
			c.prop(self,'size_x',text='Radius')
			c.prop(self,'size_y',text='Height')
		elif self.rigid_body_shape == 'SPHERE':
			c.prop(self,'size_x',text='Radius')
				
		row = layout.row()
		c = row.column()
		c.prop(self, 'mass')
		c.prop(self, 'restitution')

		c = row.column()
		c.prop(self, 'friction')
		c.prop(self, 'linear_damping')
		c.prop(self, 'angular_damping')
		
		c = layout.column(align=True)
		row = c.row(align=True)
		row.prop(self, 'collision_group_number')
		
		c = layout.column()
        #c.prop(obj.mmd_rigid, 'collision_group_mask')
		c.label(text='Collision Group Mask:')
		row = c.row(align=True)
		for i in range(0, 8):
			row.prop(self, 'collision_group_mask', index=i, text=str(i), toggle=True)
		row = c.row(align=True)
		for i in range(8, 16):
			row.prop(self, 'collision_group_mask', index=i, text=str(i), toggle=True)

	@classmethod
	def poll(cls, context):
		obj = context.active_object 
		return obj is not None and obj.mmd_type == 'RIGID_BODY'


	def execute(self, context):

		bpy.ops.object.mode_set(mode='OBJECT')
		

		# Call the function and only pass the non-None parameters
		transform_selected_rigid_bodies(
					rotation_x=self.rotation_x if self.rotation_x is not None else None,
					rotation_y=self.rotation_y if self.rotation_y is not None else None,
					rotation_z=self.rotation_z if self.rotation_z is not None else None,
					size_x=self.size_x if self.size_x is not None else None,
					size_y=self.size_y if self.size_y is not None else None,
					size_z=self.size_z if self.size_z is not None else None,
					rigid_body_type=self.rigid_body_type if self.rigid_body_type is not None else None,
					rigid_body_shape=self.rigid_body_shape if self.rigid_body_shape is not None else None,
					mass=self.mass if self.mass is not None else None,
					restitution=self.restitution if self.restitution is not None else None,
					collision_group_number=self.collision_group_number if self.collision_group_number is not None else None,
					collision_group_mask=self.collision_group_mask if self.collision_group_mask is not None else None,
					friction=self.friction if self.friction is not None else None,
					linear_damping=self.linear_damping if self.linear_damping is not None else None,
					angular_damping=self.angular_damping if self.angular_damping is not None else None,
				)
		
		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager

		obj = context.active_object

		#self.edit_rotation_x: bpy.props.BoolProperty(name='Rotation X')
		self.rotation_x= obj.rotation_euler.x
		self.rotation_y= obj.rotation_euler.y
		self.rotation_z= obj.rotation_euler.z
		self.size_x = obj.mmd_rigid.size[0]
		self.size_y = obj.mmd_rigid.size[1]
		self.size_z = obj.mmd_rigid.size[2]
		self.rigid_body_type = obj.mmd_rigid.type
		self.rigid_body_shape =  obj.mmd_rigid.shape
		self.mass = obj.rigid_body.mass
		self.restitution = obj.rigid_body.restitution
		self.collision_group_number = obj.mmd_rigid.collision_group_number
		self.collision_group_mask = obj.mmd_rigid.collision_group_mask
		self.friction =obj.rigid_body.friction
		self.linear_damping = obj.rigid_body.linear_damping
		self.angular_damping = obj.rigid_body.angular_damping

		return wm.invoke_props_dialog(self, width=400)