bl_info = {
	"name": "FFXIV MMD Tools Helper",
	"author": "wikid24",
	"version": (0, 835),
	"blender": (2, 80, 0),
	"location": "View3D > Sidebar > FFXIV MMD Tools Helper",
	"description": "Fork of MMDToolsHelper for FFXIV Models & updated Blender to be compatible with 2.8+",
	"warning": "",
	"wiki_url": "https://github.com/wikid24/ffxiv_mmd_tools_helper",
	"tracker_url": "https://github.com/wikid24/ffxiv_mmd_tools_helper/issues",
	"category": "Object",
	}

__bl_classes = []
def register_wrap(cls):
	#print('%3d'%len(__bl_classes), cls)
	#assert(cls not in __bl_classes)
	if __make_annotations:
		bl_props = {k:v for k, v in cls.__dict__.items() if isinstance(v, __bpy_property)}
		if bl_props:
			if '__annotations__' not in cls.__dict__:
				setattr(cls, '__annotations__', {})
			annotations = cls.__dict__['__annotations__']
			for k, v in bl_props.items():
				#print('   -', k, v)
				#assert(v.__class__.__name__ == '_PropertyDeferred' or getattr(v[0], '__module__', None) == 'bpy.props' and isinstance(v[1], dict))
				annotations[k] = v
				delattr(cls, k)
	if hasattr(cls, 'bl_rna'):
		__bl_classes.append(cls)
	return cls

if "bpy" in locals():
	if bpy.app.version < (2, 71, 0):
		import imp as importlib
	else:
		import importlib
	importlib.reload(model)
	importlib.reload(import_csv)
	importlib.reload(add_foot_leg_ik)
	importlib.reload(add_hand_arm_ik)
	importlib.reload(armature_diagnostic)
	importlib.reload(background_color_picker)
	importlib.reload(bone_conversion)
	importlib.reload(bone_groups)
	importlib.reload(bone_morphs)
	importlib.reload(bone_tools)
	importlib.reload(bones_renamer)
	importlib.reload(convert_to_blender_camera)
	importlib.reload(display_panel_groups)
	importlib.reload(import_ffxiv_model)
	importlib.reload(joints)
	importlib.reload(miscellaneous_tools)
	importlib.reload(mmd_lamp_setup)
	#importlib.reload(mmd_view)
	importlib.reload(reverse_japanese_english)
	importlib.reload(rigid_body)
	importlib.reload(shape_keys)
	importlib.reload(skirt)
	importlib.reload(toon_textures_to_node_editor_shader)
	importlib.reload(toon_modifier)
	importlib.reload(panels)
	
else:
	import bpy
	import logging

	__make_annotations = (bpy.app.version >= (2, 80, 0))
	__bpy_property = (bpy.props._PropertyDeferred if hasattr(bpy.props, '_PropertyDeferred') else tuple)
	from . import model
	from . import import_csv
	from . import add_foot_leg_ik
	from . import add_hand_arm_ik
	from . import armature_diagnostic
	from . import background_color_picker
	from . import bone_conversion
	from . import bone_groups
	from . import bone_morphs
	from . import bone_tools
	from . import bones_renamer
	from . import convert_to_blender_camera
	from . import display_panel_groups
	from . import import_ffxiv_model
	from . import joints
	from . import miscellaneous_tools
	from . import mmd_lamp_setup
	#from . import mmd_view
	from . import reverse_japanese_english
	from . import rigid_body
	from . import shape_keys
	from . import skirt
	from . import toon_textures_to_node_editor_shader
	from . import toon_modifier
	from . import panels

if bpy.app.version < (2, 80, 0):
	bl_info['blender'] = (2, 70, 0)

logging.basicConfig(format='%(message)s', level=logging.DEBUG)


def register():
	for cls in __bl_classes:
		bpy.utils.register_class(cls)
	print(__name__, 'registed %d classes'%len(__bl_classes))

def unregister():
	for cls in reversed(__bl_classes):
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register()
