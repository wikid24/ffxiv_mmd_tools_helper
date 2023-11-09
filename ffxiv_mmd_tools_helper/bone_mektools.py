import bpy
import addon_utils
from . import register_wrap
from . import model



	
def auto_create_mektools_armature_from_race(target_armature):

	existing_mektools_arm = None

	#check if target_armature already has a mektools rig, if it does, don't create a new one
	for obj in target_armature.children:
		if obj.type == 'MESH':
			for mod in obj.modifiers:
				if mod.type == 'ARMATURE' and mod.name=='mektools_armature_deform' and mod.object:
					existing_mektools_arm = mod.object
					break
		if existing_mektools_arm:
			break

			
	#print(target_armature.data['ModelRaceType'])

	armature_race = target_armature.data['ModelRaceType']

	modelracetype_mektools_operator_dict = {
		'Hyur_Mid_F' 	: 'sna.import_mf_36952' ,
		'Hyur_Hig_F' 	: 'sna.import_hf_e2d09' ,
		'Elez_F' 	  	: 'sna.import_ef_8e849' ,
		'Miqo_F' 	  	: 'sna.import_miqf_e13b1' ,
		'Miqo_F_NPC' 	: 'sna.import_miqf_e13b1' ,
		'Roeg_F' 		: 'sna.import_rf_c1dc0' ,
		'Lala_F' 		: 'sna.import_lala_adb84' ,
		'Aura_F' 		: 'sna.import_af_b4751' ,
		'Vier_F' 		: 'sna.import_vf_6301c' ,
		'Hyur_Mid_M'	: 'sna.import_mm_02dc3' ,
		'Hyur_Mid_M_NPC': 'sna.import_mm_02dc3' ,
		'Hyur_Hig_M'	: 'sna.import_hm_52444' ,
		'Elez_M' 		: 'sna.import_em_b2121' ,
		'Miqo_M'		: 'sna.import_miqm_0929d' ,
		'Roeg_M'		: 'sna.import_rm_39a5f' ,
		'Lala_M'		: 'sna.import_lala_adb84' ,
		'Aura_M'		: 'sna.import_am_c728c' ,
		'Hrot_M'		: 'sna.import_hrm_c1590' ,
		'Vier_M' 		: 'sna.import_vm_4aaf7' ,
	}

	if armature_race in modelracetype_mektools_operator_dict.keys():
		#import_operator = modelracetype_mektools_operator_dict[armature_race]
		import_operator = 'bpy.ops.' + modelracetype_mektools_operator_dict[armature_race] + '()'
		#print(f"race: {armature_race} : {modelracetype_mektools_operator_dict[armature_race]}")


		try:
			#if there is an existing mektools armature, do not create a new one
			if existing_mektools_arm is None:
				eval(import_operator)
				print(f"Executed operator for race: {armature_race}")
			else:
				print(f"Existing mektools armature exists: {existing_mektools_arm}")
		except Exception as e:
			print(f"Failed to execute operator for race: {armature_race}")
			print(f"Error: {str(e)}")
		else:
			#get the newly added mektools collection
			collections = bpy.context.scene.collection.children
			root_collection = None
			if collections:
				root_collection = bpy.context.scene.collection.children[0]

			mektools_collection = None
			mektools_armature = None

			for obj in bpy.data.objects:
				#if not obj.name.startswith('mektooks_'):
				if obj.type =='ARMATURE' and not (obj.name.startswith('mektools_')):
					if 'PROPERTIES' in obj.data.bones.keys():
						mektools_collection = obj.users_collection[0]
						mektools_armature = obj
						break
			
			if mektools_collection: 
				mektools_collection.name = 'mektools_' + target_armature.parent.name
				mektools_armature.name = 'mektools_' + mektools_armature.name

				# Unlink the mektools_collection from its current parent collection
				if mektools_collection.name in bpy.context.scene.collection.children.keys():
					bpy.context.scene.collection.children.unlink(mektools_collection)

				if mektools_collection.name not in root_collection.children.keys():
					root_collection.children.link(mektools_collection)
				
			
			if mektools_collection:

				bpy.ops.object.mode_set(mode='OBJECT')

				for obj in target_armature.children:
					if obj.type=='MESH':
						obj.select = True
				apply_mektools_armature_deform_to_selected_meshes(mektools_armature)
				apply_copy_location_for_mektools_armature_from_meshes(mektools_armature)

				
	else:
		print(f"No operator found for race: {armature_race}")

def apply_mektools_armature_deform_to_selected_meshes(armature_obj):
	# Loop through all selected objects
	for obj in bpy.context.selected_objects:
		if obj.type == 'MESH':
			# Check if the object is a mesh
			# Check if there's already an Armature Deform modifier linked to the target armature
			armature_mod = None
			for mod in obj.modifiers:
				if mod.type == 'ARMATURE' and mod.name=='mektools_armature_deform':
					armature_mod = mod
					armature_mod.object = armature_obj
					break
			if armature_mod is None:
				# If there's no Armature Deform modifier, create a new one
				armature_mod = obj.modifiers.new(name="mektools_armature_deform", type='ARMATURE')
				armature_mod.object = armature_obj

	# Make sure to update the scene after adding modifiers
	bpy.context.view_layer.update()	


def apply_copy_location_for_mektools_armature_from_meshes(target_armature):
	# Get the currently selected mesh object
	selected_objects = bpy.context.selected_objects
	armature_object = None

	if selected_objects:
		selected_mesh = None
		for obj in selected_objects:
			if obj.type == 'MESH':
				selected_mesh = obj
				break

		if selected_mesh:
			# Find the Armature Deform modifier linked to the mesh
			for modifier in selected_mesh.modifiers:
				if modifier.type == 'ARMATURE':
					if modifier.object != target_armature:
						armature_object = modifier.object
						print(f"Armature associated with the selected mesh: {armature_object.name}")
		else:
			print("No selected mesh object.")
	else:
		print("No objects are selected.")


	if armature_object and target_armature:
		if armature_object != target_armature:
			# Check if a Copy Location constraint already exists on the target armature
			copy_loc_constraint = None
			for constraint in target_armature.constraints:
				if constraint.type == 'COPY_LOCATION' and constraint.target == armature_object:
					copy_loc_constraint = constraint
					print("Copy Location constraint already exists.")
					break
			
			if copy_loc_constraint is None:
				# Create a new Copy Location constraint for the destination armature
				copy_loc_constraint = target_armature.constraints.new(type='COPY_LOCATION')
			
				# Set the target armature (source) for the Copy Location constraint
				copy_loc_constraint.target = armature_object

	


	

@register_wrap
class ApplyMekToolsRig(bpy.types.Operator):
	"""Adds a MekTools rig based on the current FFXIV Race"""
	bl_idname = "ffxiv_mmd.apply_mektools_rig"
	bl_label = "Adds a MekTools rig based on the current FFXIV Race"
	bl_options = {'REGISTER', 'UNDO'}

	#bpy.types.Scene.armature_deform_pin = bpy.props.PointerProperty(
		#type=bpy.types.Object
		#,poll=lambda self, obj: obj.type == 'ARMATURE',
		#)

	@classmethod
	def poll(cls, context):
		
		if context.active_object:
			if context.active_object.type == 'ARMATURE':
					return True
			
		return False #obj is not None and obj.type == 'ARMATURE'

	def execute(self, context):
		
		addon_name = 'mek_tools'
		addon_required_version = '0.35'
		addon_module = [m for m in addon_utils.modules() if m.__name__ == addon_name][0] # get module
		if addon_module:
			installed_version = addon_module.bl_info.get('version',(-1,-1,-1))
			installed_version = float(str(installed_version[0])+'.'+str(installed_version[1])+str(installed_version[2]))

		# Check if the addon is enabled
		if addon_name not in bpy.context.preferences.addons.keys():
			raise Exception(f"The addon '{addon_name}' is not installed or is not enabled. Please install and enable it.")
		elif  installed_version < float(addon_required_version):
			raise Exception(f"Addon '{addon_name}' version is {installed_version} please install {addon_required_version} or higher.")
		else:
			#print(f"The addon '{addon_name}' is installed and enabled.")

			active_armature = None

			if bpy.context.active_object.type == 'ARMATURE':
				active_armature = bpy.context.active_object

			if active_armature:
				auto_create_mektools_armature_from_race(active_armature)

		return {'FINISHED'}
