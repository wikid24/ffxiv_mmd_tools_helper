import bpy
import subprocess
import sys
import os

from . import register_wrap
from bpy_extras.io_utils import ImportHelper


def tex_to_dds(source_folder):
	file_path = (__file__ + r"ext\ffxiv-tex-converter.pyz").replace("tex_converter.py" , "")
	# Example usage
	#args = ["--directory", "/path/to/your/directory", "--command", "dds-to-tex", "--parallel", "--multiplier", "5"]
	#source_folder = r"D:\temp"
	target_folder = None

	run_pyz_script(file_path, ["--directory", source_folder, "--command", "tex-to-dds"])


def dds_to_tex(source_folder):
	file_path = (__file__ + r"ext\ffxiv-tex-converter.pyz").replace("tex_converter.py" , "")
	# Example usage
	#args = ["--directory", "/path/to/your/directory", "--command", "dds-to-tex", "--parallel", "--multiplier", "5"]
	#source_folder = r"D:\temp"
	target_folder = None

	run_pyz_script(file_path, ["--directory", source_folder, "--command", "dds-to-tex"])




def run_pyz_script(pyz_file_path, args):
    # Get the path to the Python executable running Blender
    blender_python_executable = sys.executable

    # Construct the command to run the pyz file
    command = [blender_python_executable, pyz_file_path] + args
    # Run the command
    subprocess.run(command)

@register_wrap
class SelectConvertInputFolder(bpy.types.Operator,ImportHelper):
	"""Select Input Folder for Conversion"""
	bl_idname = "ffxiv_mmd.select_convert_input_folder"
	bl_label = "Accept"
	bl_options = {'REGISTER', 'UNDO'}

	# Filter folders only
	filename_ext = ""
	filter_folder = True
	filter_file = False
	filter_glob: bpy.props.StringProperty(default="", options={'HIDDEN'})
	
	bpy.types.Scene.convert_input_file_folder = bpy.props.StringProperty(
		name="Input File Folder"
		, description="Folder where the input files are located"
		, default=''
		, maxlen=0, update=None, get=None, set=None)
	
	bpy.types.Scene.convert_output_file_folder = bpy.props.StringProperty(
		name="Output File Folder"
		, description="Folder where the output files are located"
		, default=''
		, maxlen=0, update=None, get=None, set=None)
	
	#def invoke(self, context, event):
		#self.filepath = context.scene.convert_input_file_folder
		#context.window_manager.fileselect_add(self)
		#return {'RUNNING_MODAL'}

	def execute(self, context):
		context.scene.convert_input_file_folder = bpy.path.abspath(self.filepath)
		context.scene.convert_output_file_folder = ''

		return {'FINISHED'}
	

@register_wrap
class ConvertTEXtoDDS(bpy.types.Operator):
	"""User can select the folder for materials"""
	bl_idname = "ffxiv_mmd.convert_tex_to_dds"
	bl_label = "Convert .tex to .dds"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		folder_path = bpy.path.abspath(context.scene.convert_input_file_folder)
		return os.path.exists(folder_path)

	def execute(self,context):
		input_folder_path = context.scene.convert_input_file_folder

		# Get the folder path
		folder_path = os.path.dirname(input_folder_path)

		# Append "_dds" to the folder path
		output_folder_path = os.path.join(folder_path, folder_path + "_dds")
		context.scene.convert_output_file_folder = bpy.path.abspath(output_folder_path)


		tex_to_dds(input_folder_path)

		return {'FINISHED'}
	

@register_wrap
class ConvertDDStoTEX(bpy.types.Operator):
	"""User can select the folder for materials"""
	bl_idname = "ffxiv_mmd.convert_dds_to_tex"
	bl_label = "Convert .dds to .tex"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		folder_path = bpy.path.abspath(context.scene.convert_input_file_folder)
		return os.path.exists(folder_path)

	def execute(self,context):
		input_folder_path = context.scene.convert_input_file_folder

		# Get the folder path
		folder_path = os.path.dirname(input_folder_path)

		# Append "_tex" to the folder path
		output_folder_path = os.path.join(folder_path, folder_path + "_tex")
		context.scene.convert_output_file_folder = bpy.path.abspath(output_folder_path)

		dds_to_tex(input_folder_path)

		return {'FINISHED'}
	

@register_wrap
class ConvertOpenOutputFolderInWindowsExplorer(bpy.types.Operator):
	"""Opens output folder in Windows Explorer"""
	bl_idname = "ffxiv_mmd.convert_open_output_folder"
	bl_label = "Open Output Folder in Windows Explorer"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		folder_path = bpy.path.abspath(context.scene.convert_output_file_folder)

		return os.path.exists(folder_path)


	def execute(self,context):
		folder_path = bpy.path.abspath(context.scene.convert_output_file_folder)

		if os.path.exists(folder_path):
			# Use subprocess to open the folder in Windows Explorer
			subprocess.Popen(['start', 'explorer', folder_path], shell=True)
		
		return {'FINISHED'}
