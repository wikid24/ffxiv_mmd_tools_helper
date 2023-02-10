import bpy

from . import register_wrap
from . import model

 # blend_type
	# Type:	enum in ["MIX", "ADD", "MULTIPLY", "SUBTRACT", "SCREEN", "DIVIDE", "DIFFERENCE", "DARKEN", "LIGHTEN", "OVERLAY", "DODGE", "BURN", "HUE", "SATURATION", "VALUE", "COLOR", "SOFT_LIGHT", "LINEAR_LIGHT"], default ‘MIX’

def main(context):
	mesh_objects_list = model.find_MMD_MeshesList(bpy.context.active_object)
	# print("mesh_objects_list = ", mesh_objects_list)
	assert(mesh_objects_list is not None), "The active object is not an MMD model."
	for o in mesh_objects_list:
		bpy.context.view_layer.objects.active = o
		for m in bpy.context.active_object.data.materials:
			for n in m.node_tree.nodes:
				if n.label == "toon_modifier":
					n.inputs['Color2'].default_value[0] = bpy.context.scene.ToonModifierColor[0]
					n.inputs['Color2'].default_value[1] = bpy.context.scene.ToonModifierColor[1]
					n.inputs['Color2'].default_value[2] = bpy.context.scene.ToonModifierColor[2]
					n.blend_type = bpy.context.scene.ToonModifierBlendType


@register_wrap
class MMDToonModifier(bpy.types.Operator):
	"""User can modify the rendering of toon texture color"""
	bl_idname = "ffxiv_mmd_tools_helper.toon_modifier"
	bl_label = "MMD toon modifier"
	bl_options = {'REGISTER', 'UNDO'}

	bpy.types.Scene.ToonModifierColor = bpy.props.FloatVectorProperty( \
		name="Toon Modifer Color" \
		, description="toon modifer color" \
		, default=(1.0, 1.0, 1.0) \
		, min=0.0 \
		, max=1.0 \
		, soft_min=0.0 \
		, soft_max=1.0 \
		, step=3 \
		, precision=2 \
		, options={'ANIMATABLE'} \
		, subtype='COLOR' \
		, unit='NONE' \
		, size=3 \
		, update=None \
		, get=None \
		, set=None)

	bpy.types.Scene.ToonModifierBlendType = bpy.props.EnumProperty( \
			items = [ \
			('MIX', 'MIX', 'MIX') \
			, ('ADD', 'ADD', 'ADD') \
			, ('MULTIPLY', 'MULTIPLY', 'MULTIPLY') \
			, ('SUBTRACT', 'SUBTRACT', 'SUBTRACT') \
			, ('SCREEN', 'SCREEN', 'SCREEN') \
			, ('DIVIDE', 'DIVIDE', 'DIVIDE') \
			, ('DIFFERENCE', 'DIFFERENCE', 'DIFFERENCE') \
			, ('DARKEN', 'DARKEN', 'DARKEN') \
			, ('LIGHTEN', 'LIGHTEN', 'LIGHTEN') \
			, ('OVERLAY', 'OVERLAY', 'OVERLAY') \
			, ('DODGE', 'DODGE', 'DODGE') \
			, ('BURN', 'BURN', 'BURN') \
			, ('HUE', 'HUE', 'HUE') \
			, ('SATURATION', 'SATURATION', 'SATURATION') \
			, ('VALUE', 'VALUE', 'VALUE') \
			, ('COLOR', 'COLOR', 'COLOR') \
			, ('SOFT_LIGHT', 'SOFT_LIGHT', 'SOFT_LIGHT') \
			, ('LINEAR_LIGHT', 'LINEAR_LIGHT', 'LINEAR_LIGHT')] \
			, name = "Toon Modifier Blend Type", default = 'MULTIPLY' \
			)

	# @classmethod
	# def poll(cls, context):
		# return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}