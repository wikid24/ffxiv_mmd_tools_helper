import bpy
from . import register_wrap

def main(context):
	for o in bpy.context.scene.objects:
		if o.type == 'CAMERA':
			camera = o
			camera.lock_location[0] = False
			camera.lock_location[1] = False
			camera.lock_location[2] = False
			camera.lock_rotation[0] = False
			camera.lock_rotation[1] = False
			camera.lock_rotation[2] = False
			camera.lock_scale[0] = False
			camera.lock_scale[1] = False
			camera.lock_scale[2] = False

			if o.animation_data is not None:
				for d in o.animation_data.drivers:
					d.mute = True

	if camera.parent is not None:
		if camera.parent.mmd_type == 'CAMERA':
			#bpy.context.scene.objects.unlink(camera.parent)
			
			camera_track = camera.parent
			bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
			#camera_track.name = 'Camera_Tracking_Target'
			
			# Create the constraint
			constraint = camera.constraints.new(type='CHILD_OF')
			constraint.target = camera_track

			# Apply the constraint
			constraint.influence = 1.0
			


@register_wrap
class MMDCameraToBlenderCamera(bpy.types.Operator):
	"""Convert MMD cameras back to Blender cameras"""
	bl_idname = "ffxiv_mmd.mmd_camera_to_blender_camera"
	bl_label = "Convert MMD Cameras to Blender cameras"
	bl_options = {'REGISTER', 'UNDO'}

	# @classmethod
	# def poll(cls, context):
		# return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}