import bpy
import struct
from . import register_wrap
from bpy_extras.io_utils import ImportHelper
from . import model
#import mmd_tools.core.model as mmd_model
from . import translate


def _toShiftJisString(byteString):
	return byteString.split(b'\x00')[0].decode('shift_jis', errors='replace')

def read_vmd_file(file_path):
	
	VMD_SIGN = b'Vocaloid Motion Data 0002'
	signature = None
	model_name = ''
	bone_keyframes = []
	face_keyframes = []
	camera_keyframes = []
		
	with open(file_path, 'rb') as fin:
		
		try: 
			signature, = struct.unpack('<30s', fin.read(30))
			if signature[:len(VMD_SIGN)] != VMD_SIGN:
				raise InvalidFileError('File signature "%s" is invalid.'%signature)
			model_name = _toShiftJisString(struct.unpack('<20s', fin.read(20))[0])
			
			# Read the bone keyframes
			num_bone_keyframes, = struct.unpack('<I', fin.read(4))
			for _ in range(num_bone_keyframes):
				bone_name = _toShiftJisString(struct.unpack('<15s', fin.read(15))[0])
				frame_number, = struct.unpack('<I', fin.read(4))
				bone_pos = struct.unpack('<3f', fin.read(12))
				bone_rot = struct.unpack('<4f', fin.read(16))
				interpolation_data = fin.read(64)
				
				keyframe = {
					'bone_name': bone_name,
					'frame_number': frame_number,
					'bone_pos': bone_pos,
					'bone_rot': bone_rot,
					'interpolation_data': interpolation_data
				}
				bone_keyframes.append(keyframe)
			
			# Read the face keyframes
			num_face_keyframes, = struct.unpack('<I', fin.read(4))
			for _ in range(num_face_keyframes):
				face_name = _toShiftJisString(struct.unpack('<15s', fin.read(15))[0])
				frame_index, = struct.unpack('<I', fin.read(4))
				weight, = struct.unpack('<f', fin.read(4))
				
				keyframe = {
					'face_name': face_name,
					'frame_index': frame_index,
					'weight': weight
				}
				face_keyframes.append(keyframe)
				
			# Read the camera keyframes
			num_camera_keyframes, = struct.unpack('<I', fin.read(4))
			for _ in range(num_camera_keyframes):
				frame_index, = struct.unpack('<I', fin.read(4))
				distance_to_target, target_pos_x, target_pos_y, target_pos_z = struct.unpack('<4f', fin.read(16))
				camera_rot_x, camera_rot_y, camera_rot_z = struct.unpack('<3f', fin.read(12))
				interpolation_data = fin.read(24)
				fov_angle, = struct.unpack('<f', fin.read(4))
				perspective, = struct.unpack('<B', fin.read(1))
				
				keyframe = {
					'frame_index': frame_index,
					'distance_to_target': distance_to_target,
					'target_pos': (target_pos_x, target_pos_y, target_pos_z),
					'camera_rot': (camera_rot_x, camera_rot_y, camera_rot_z),
					'interpolation_data': interpolation_data,
					'fov_angle': fov_angle,
					'perspective': perspective
				}
				camera_keyframes.append(keyframe)
		
		except struct.error:
			pass 
	
	return model_name, bone_keyframes, face_keyframes, camera_keyframes
		
def output_vmdfile_results(model_name,bone_keyframes,face_keyframes,camera_keyframes):

	
	# Print model name
	print("\nModel Name from the VMD file:", model_name)

	# Sorting and printing unique bone names alphabetically
	unique_bone_names = sorted(set(keyframe['bone_name'] for keyframe in bone_keyframes))
	print("\nBone Names in the VMD file:")
	for bone_name in unique_bone_names:
			if translate.is_translated(bone_name):
				print (bone_name)
			else:
				print (bone_name, f' ({translate.toEng(bone_name)})')
			
	num_bones = len(unique_bone_names)
	print("\nTotal num bones:",num_bones)
	print("\n-------")
	
	# Printing unique face names
	unique_face_names = set(keyframe['face_name'] for keyframe in face_keyframes)
	print("\nMorphs/Shape Keys in the VMD File:")
	for face_name in unique_face_names:
		if translate.is_translated(face_name):
			print (face_name)
		else:
			print (face_name, f' ({translate.toEng(face_name)})')

	num_face_names = len(unique_face_names)
	print("\nTotal num morphs:",num_face_names)
	print("\n-------")

	# Print the number of camera keyframes
	num_camera_keyframes = len(camera_keyframes)
	print("Number of Camera Keyframes:", num_camera_keyframes)


def compare_vmd_to_armature(vmd_bone_name_mode,arm,model_name,bone_keyframes,face_keyframes,camera_keyframes):

	print("\nModel Name from the VMD file:", model_name)

	# Sorting and printing unique bone names alphabetically
	unique_vmd_bone_names = sorted(set(keyframe['bone_name'] for keyframe in bone_keyframes))
	num_vmd_bones = len(unique_vmd_bone_names)

	#armature_bone_names = [bone.name for bone in arm.data.bones]
	#get all the PMX bones name from currently selected aramture
 
	
	armature_bonenames = []
	for b in arm.data.bones:
		if vmd_bone_name_mode == 'mmd_bone_name_j' and hasattr(arm.pose.bones[b.name], "mmd_bone"):
			armature_bonenames.append(translate.parseJp(arm.pose.bones[b.name].mmd_bone.name_j))
		elif vmd_bone_name_mode == 'mmd_bone_name_e' and hasattr(arm.pose.bones[b.name], "mmd_bone"):
			armature_bonenames.append(translate.parseJp(arm.pose.bones[b.name].mmd_bone.name_e))
		elif vmd_bone_name_mode == 'blender_bone_name':
			armature_bonenames.append(translate.parseJp(b.name))

	print("\nTotal num bones in VMD:",num_vmd_bones)
	print("Bones in VMD but not on selected Armature:")

	nomatch_counter = 0

	for vmd_bone in unique_vmd_bone_names:
		
		#if hasattr(arm.pose.bones[b.name], "mmd_bone"):
			#arm.pose.bones[b.name].mmd_bone.name_j = b.name

		if translate.parseJp(vmd_bone) not in armature_bonenames:
			nomatch_counter += 1
			if translate.is_translated(vmd_bone):
				print (vmd_bone)
			else:
				print (vmd_bone, f' ({translate.toEng(vmd_bone)})')
	

	print(f"\nTotal nomatches: {nomatch_counter}")
	#get the PMX bones on the currently selected armature

	print("\n-------")
	
	# Printing unique face names
	unique_vmd_face_names = set(keyframe['face_name'] for keyframe in face_keyframes)
	num_vmd_face_names = len(unique_vmd_face_names)
	print("\nTotal num morphs in VMD:",num_vmd_face_names)
	print("Morphs in VMD but not on selected Armature:")
	print("\n-------")


@register_wrap
class FFXIV_VMDInspectFileBrowserImportOperator(bpy.types.Operator, ImportHelper):
	"""Read .vmd files in Blender Console Window"""
	bl_idname = "ffxiv_mmd.read_vmd_file_browser_operator"
	bl_label = "Read .vmd File"
	bl_options = {'REGISTER', 'UNDO'}

	filename_ext = ".vmd"
	filter_glob: bpy.props.StringProperty(
		default="*.vmd",
		options={'HIDDEN'},
	)

	def execute(self, context):
		filepath = self.filepath
			# Example usage

		model_name, bone_keyframes, face_keyframes,camera_keyframes  = read_vmd_file(filepath)

		print("\n-------")
		print("\nVMD File Inspector:")
		print(filepath)

		output_vmdfile_results(model_name, bone_keyframes, face_keyframes,camera_keyframes)


		return {'FINISHED'}
	
@register_wrap
class FFXIV_VMDCompareFileBrowserImportOperator(bpy.types.Operator, ImportHelper):
	"""Read VMD to compare the bones & shape keys on currently selected armature in Blender Console Window"""
	bl_idname = "ffxiv_mmd.compare_vmd_file_browser_operator"
	bl_label = "Compare .vmd File to Armature"
	bl_options = {'REGISTER', 'UNDO'}

	filename_ext = ".vmd"
	filter_glob: bpy.props.StringProperty(
		default="*.vmd",
		options={'HIDDEN'},
	)

	bpy.types.Scene.vmd_bone_name_mode = bpy.props.EnumProperty(items = \
	[("blender_bone_name", "Compare VMD vs Blender Bone","Compare VMD against Blender Bone Names") \
	, ("mmd_bone_name_j", "Compare VMD vs MMD Japanese Bone", "Compare VMD against MMD Japanese Bone Names")\
	, ("mmd_bone_name_e", "Compare VMD vs MMD English Bone", "Compare VMD against MMD English Bone Names")\
	], name = "", default = 'blender_bone_name')

	@classmethod
	def poll(cls, context):		

			return context.active_object


	def execute(self, context):
		filepath = self.filepath

		arm=None


		if bpy.context.scene.vmd_bone_name_mode in ('mmd_bone_name_j','mmd_bone_name_e'):
			arm = model.find_MMD_Armature(context.active_object)
		else:
			arm = model.findArmature(context.active_object)

		if not arm:
			raise TypeError("Only works on armatures that have been converted to MMD.")
		else:

			model_name, bone_keyframes, face_keyframes,camera_keyframes  = read_vmd_file(filepath)

			print("\n-------")
			print("\nVMD File Comparison:")
			print(filepath)

			compare_vmd_to_armature(bpy.context.scene.vmd_bone_name_mode,arm,model_name, bone_keyframes, face_keyframes,camera_keyframes)
			
	

			
		return {'FINISHED'}
	
	
