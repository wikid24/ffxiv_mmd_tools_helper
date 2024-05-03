import bpy
import struct
from . import register_wrap
from bpy_extras.io_utils import ImportHelper
from . import model
import mmd_tools.core.model as mmd_model

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
		# Print model name
		print("\nModel Name from the VMD file:", model_name)

		# Sorting and printing unique bone names alphabetically
		unique_bone_names = sorted(set(keyframe['bone_name'] for keyframe in bone_keyframes))
		print("\nBone Names in the VMD file:")
		for bone_name in unique_bone_names:
			print(bone_name)
				
		num_bones = len(unique_bone_names)
		print("\nTotal num bones:",num_bones)
		print("\n-------")
		
		# Printing unique face names
		unique_face_names = set(keyframe['face_name'] for keyframe in face_keyframes)
		print("\nMorphs/Shape Keys in the VMD File:")
		for face_name in unique_face_names:
			print(face_name)

		num_face_names = len(unique_face_names)
		print("\nTotal num morphs:",num_face_names)
		print("\n-------")

		# Print the number of camera keyframes
		num_camera_keyframes = len(camera_keyframes)
		print("Number of Camera Keyframes:", num_camera_keyframes)


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

	@classmethod
	def poll(cls, context):		

			return context.active_object


	def execute(self, context):
		filepath = self.filepath

		arm = model.find_MMD_Armature(context.active_object)

		model_name, bone_keyframes, face_keyframes,camera_keyframes  = read_vmd_file(filepath)

		print("\n-------")
		print("\nVMD File Comparison:")
		print(filepath)
		# Print model name
		print("\nModel Name from the VMD file:", model_name)

		# Sorting and printing unique bone names alphabetically
		unique_vmd_bone_names = sorted(set(keyframe['bone_name'] for keyframe in bone_keyframes))
		num_vmd_bones = len(unique_vmd_bone_names)

		#armature_bone_names = [bone.name for bone in arm.data.bones]
  		#get all the PMX bones name from currently selected aramture
		pmx_bonenames = []
		for b in arm.data.bones:
			if hasattr(arm.pose.bones[b.name], "mmd_bone"):
				pmx_bonenames.append(arm.pose.bones[b.name].mmd_bone.name_j)

		print("\nTotal num bones in VMD:",num_vmd_bones)
		print("Bones in VMD but not on selected Armature:")

		for vmd_bone in unique_vmd_bone_names:
			
			if hasattr(arm.pose.bones[b.name], "mmd_bone"):
				arm.pose.bones[b.name].mmd_bone.name_j = b.name

			if vmd_bone not in pmx_bonenames:
				print (vmd_bone)
		
		#get the PMX bones on the currently selected armature

		print("\n-------")
		
		# Printing unique face names
		unique_vmd_face_names = set(keyframe['face_name'] for keyframe in face_keyframes)
		num_vmd_face_names = len(unique_vmd_face_names)
		print("\nTotal num morphs in VMD:",num_vmd_face_names)
		print("Morphs in VMD but not on selected Armature:")
		print("\n-------")
		return {'FINISHED'}
	
	
