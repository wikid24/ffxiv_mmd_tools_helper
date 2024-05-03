import bpy
import csv
import os
import math
from . import register_wrap

import mmd_tools.core.model as mmd_model
from mmd_tools.core import model as mmd_model

from mathutils import Quaternion, Vector
from mmd_tools.bpyutils import matmul

from bpy_extras.io_utils import ExportHelper

# Function to round the values to the nearest 4th decimal and display blank instead of 0 or 1 for scale values
def format_value(value, is_scale=False):
	rounded_value = round(value, 3)
	
	if is_scale:
		if rounded_value == 1:
			return ""
	else:
		if rounded_value == 0:
			return ""
	if rounded_value.is_integer():
		return str(int(rounded_value))
	else:
		return str(rounded_value)
	
# Function to export pose bone names, bone groups, and transformation data to CSV
def export_bone_morph_data(filepath):
	# Get active object
	obj = bpy.context.active_object
	
	# Find the root of the MMD model
	root = mmd_model.Model.findRoot(obj)
	mmd_root = root.mmd_root
	morph_type = 'bone_morphs' #mmd_root.active_morph_type
	morphs = getattr(mmd_root, morph_type)

	# Create a CSV file and write headers
	with open(filepath, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["bone_morph", "bone_name", "locationX", "locationY", "locationZ", 
						"rotateX", "rotateY", "rotateZ", 
						"scaleX", "scaleY", "scaleZ"])

		# Iterate over all bone morphs
		for morph in morphs:
			for bones in morph.data:
				p_bone = obj.pose.bones.get(bones.bone, None)
				if p_bone:
					bone_name = p_bone.name
					morph_name = morph.name
					morph_name_e = morph.name_e
					p_bone.bone.select = True
					
					old_matrix_basis = p_bone.matrix_basis

					mtx = matmul(p_bone.matrix_basis.to_3x3(), Quaternion(*bones.rotation.to_axis_angle()).to_matrix()).to_4x4()
					mtx.translation = p_bone.location + bones.location
					p_bone.matrix_basis = mtx

					# Get local space transformations of the pose bone
					bone_location = [format_value(v) for v in p_bone.location]
					
					
					# Check if rotation is in quaternion or euler mode
					if p_bone.rotation_mode == 'QUATERNION':
						p_bone.rotation_mode = 'XYZ'
						# Convert quaternion rotation to euler
						bone_rotation = [format_value(math.degrees(v)) for v in p_bone.rotation_euler]
						p_bone.rotation_mode = 'QUATERNION'
						#bone_rotation = [format_value(v) for v in p_bone.rotation_quaternion.to_euler()]
					else:
						bone_rotation = [format_value(math.degrees(v)) for v in p_bone.rotation_euler]
					bone_scale = [format_value(v, is_scale=True) for v in p_bone.scale]

					# Write bone data to CSV
					writer.writerow([morph_name_e, bone_name,
									*bone_location,
									*bone_rotation,
									*bone_scale])
					
					p_bone.matrix_basis = old_matrix_basis
					bpy.ops.mmd_tools.clear_bone_morph_view()


	print("Bone morph data exported successfully to", filepath)

@register_wrap
# Operator to handle file selection using ExportHelper
class ExportPoseBoneFileHelper(bpy.types.Operator, ExportHelper):
	bl_idname = "ffxiv_mmd.export_bone_morphs_file"
	bl_label = "Export to CSV"

	filename_ext = ".csv"

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		root = mmd_model.Model.findRoot(obj)
		return obj is not None and obj.type == 'ARMATURE' and root is not None

	def execute(self, context):
		filepath = self.filepath
		if not filepath.lower().endswith(".csv"):
			filepath += ".csv"
		export_bone_morph_data(filepath)
		return {'FINISHED'}
