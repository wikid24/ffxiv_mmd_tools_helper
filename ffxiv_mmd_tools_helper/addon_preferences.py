import os
import bpy
from . import register_wrap
from bpy.types import AddonPreferences
from bpy.props import StringProperty

@register_wrap
class FFXIV_MMDAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # Property to store the folder path
    textools_saved_folder: bpy.props.StringProperty(
        name="TexTools 'Saved' Folder",
        description=("Directory path to TexTools 'Saved' Folder. This is normally where TexTools saves all model & texture files upon export"),
        subtype='DIR_PATH',
    )   

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "textools_saved_folder")

        """
        if not self.textools_saved_folder:
            # If the property is not set, set a default value here
            user_profile = os.environ.get('USERPROFILE')
            if user_profile:
                documents_folder = os.path.join(user_profile, 'Documents', 'TexTools', 'Saved')
                self.textools_saved_folder = documents_folder
        """

   # def update_textools_saved_folder(self, context):
        if not self.textools_saved_folder:
            # If the property is not set, set a default value here
            user_profile = os.environ.get('USERPROFILE')
            if user_profile:
                documents_folder = os.path.join(user_profile, 'OneDrive', 'Documents', 'TexTools', 'Saved')
                if os.path.exists(documents_folder):
                    self.textools_saved_folder = documents_folder
                else:
                    documents_folder = os.path.join(user_profile, 'Documents', 'TexTools', 'Saved')
                    if os.path.exists(documents_folder):
                        self.textools_saved_folder = documents_folder
                    else:
                        # Fallback to a different location if the folder doesn't exist
                        self.textools_saved_folder = ""  # Set your desired fallback path here
