# this is a fork of Hogarth-MMD's [mmd_tools_helper](https://github.com/Hogarth-MMD/mmd_tools_helper), updated to be compatible with FFXIV Models and Blender 2.8+. It's a work in progress.

Purpose of this tool is for EVERYONE in FFXIV to start exporting their favorite FFXIV characters to MMD so we can all make memes of dancing and music videos with as little effort as possible. Once I get this tool working, tutorials on how to export FFXIV characters to MMD will come. 

------------

# New Features (completed):
  - 'Insert Bone Morphs from csv'. Working for Hyur in the CSVs now.
  - 'Insert Rigid Bodies from csv'. Working but only partially completed.
  - 'Insert Joints from csv'. Working but only partially completed.
  - 'Insert Bone Groups from csv'. Working but it doesn't add ALL the various bones for hair/hats/accessories/earrings etc... Just the essentials.
  - 'Insert Shape Keys from csv'. Working for Hyur, partially completed. 
  - Auto skirt rig generator. Add new skirt bones + weight paint existing skirt meshes with a few clicks.
  - A bunch of important useful stuff. Will list them later.

# Conversion/upgrade to Blender 2.8+ (to do):
  - mmd_lamp_setup.py
  - mmd_view.py
  - toon_textures_to_node_editor_shader.py (it works, sort of... I need to understand shaders more)

# To do:
- FFXIV Bone Morphs (facial animation sliders):
  - Populate the csv files with data. 
  - Allow for user to upload their OWN csv file (instead of using the template in this addon)
- Add 'Transform Rigify armature to match ffxiv armature'
- display_panel_groups.py - Updated to Match the ffxiv bone structure
- Automate Bone Order for PMX export
- Create 'bulk-add Rigid Bodies' with min/max values ([example plugin](https://github.com/12funkeys/rigid_bodys_gen) - [Video Tutorial](https://www.youtube.com/watch?v=0haYapQ7l_U) )
    - Add presets for skirt/hair (skirts heaviest on the bottom, hair heaviest on the top?)
- Create 'bulk-add joints' with min/max values:
    - Add presets for skirt/hair (skirts heaviest on the bottom, hair heaviest on the top?)
- Automate MMD Tools material sorter
- Automate the fix for materials/shaders - ([ffxiv material shader fix plugin](https://drive.google.com/drive/folders/10ashyJJ4HhJqFxDVnGU6s9lyJ0aFHRwa) )
- Add skirt physics module (the default skirt from FFXIV sucks for physics)
------------

# In order to use this tool, you need:
- A FFXIV Model exported into FBX file format - [FFXIV TexTools](https://www.ffxiv-textools.net/) - [Video Tutorial](https://www.youtube.com/watch?v=JbkNt51PRyM) - watch the first 7 minutes
- [Blender](https://www.blender.org/) (2.80+) or higher installed
- [MMD Tools addon](https://github.com/UuuNyaa/blender_mmd_tools) for Blender
- VMD files (MMD character/camera animation/dance files) - [Deviant Art](https://www.deviantart.com/mmd-dance-comunnity/gallery/36305808/motion-dl), [bowlroll](https://bowlroll.net/),[Reddit](https://www.reddit.com/r/mikumikudance/) or UuuNyaa's Helper addon (listed below)

# Not really needed but recommended:
- [UuuNyaa's Helper addon](https://github.com/UuuNyaa/blender_mmd_uuunyaa_tools) to MMD Tools for Blender
- [XIV Tools Discord](https://discord.com/invite/KvGJCCnG8t) - Where to find help on FFXIV Rigging
- [Miku Miku Dance](https://learnmmd.com/downloads/) (duh)
- PMX files (MMD model files) - [Deviant Art](https://www.deviantart.com/mmd-downloads-galore/gallery/39472353/models), [bowlroll](https://bowlroll.net/),[Reddit](https://www.reddit.com/r/mikumikudance/) or UuuNyaa's Helper addon (listed above)
- [PMXE](https://www.deviantart.com/inochi-pm/art/PmxEditor-vr-0254f-English-Version-v2-0-766313588) - MMD's Model Editor for PMX files
- [MekTools addon](https://www.xivmodarchive.com/modid/22780) for Blender to fix inside-out alpha (if you're not using this tool to import)
- A bunch of MMD effects (will list them later)

------------
# Useful Guides:
- [MMD Facial Expression Reference guide](https://www.deviantart.com/xoriu/art/MMD-Facial-Expressions-Chart-341504917)
- [FIX FFXIV Materials/Textures - Blender Addon](https://drive.google.com/drive/folders/10ashyJJ4HhJqFxDVnGU6s9lyJ0aFHRwa) - [Video Tutorial](https://user-images.githubusercontent.com/19479648/215879548-67bd503e-70b4-4255-abe4-bc1bbcb06618.mp4)
- [XIV Mod Archive - Useful guides to exporting](https://www.xivmodarchive.com/modid/9408) 
- [MMD Skirt Rigging Tutorial: Video Tutorial](https://www.youtube.com/watch?v=cGcBfhYyjC8)
- [UuuNyaa's Physics Adjuster: Video Tutorial](https://www.youtube.com/watch?v=pRJNJDFSYfk)
- [MMD Tools wiki](https://mmd-blender.fandom.com/wiki/MMD_Tools/Manual)
- [Animation Retargeting Video Tutorial](https://docs.google.com/document/d/1siUjAAJjUk7-Nlq11wE-Sldr8UyCeu7SkFJzUsxZpTU/edit) - An alternative approach to animating MMD using FFXIV characters

------------

# How to Install

 - Download the latest release package.zip
 - Go to Edit -> Preferences -> Add-ons -> Install and select the zip file you downloaded
  ![image](https://user-images.githubusercontent.com/19479648/215303847-8a5b34de-b8be-4070-9ab7-dc51ada3fc10.png)
  
 - In the search box, type in 'ffxiv' until the addon 'Object: FFXIV MMD Tools Helper' shows up and check the checkbox
  ![image](https://user-images.githubusercontent.com/19479648/215303990-62fca28b-79b3-4648-b620-d9c6b0f5aa3c.png)

 - Once you see "FFXIV MMD", you'll know it is installed correctly. All of the tools are located here.
  ![image](https://user-images.githubusercontent.com/19479648/216140678-1b14644f-8639-472d-99dd-23136001bcc7.png)

--------------

# How to use (my new workflow:)

On the **FFXIV MMD** tab
1) On the **Import an FFXIV Model** panel, click on  **Import your model FBX File**
2) On the **Language and Translation** panel, click on "**Mass Rename Bones**" (from FFXIV to MMD English)
3) On the **Misc/Testing/Diagnostics** panel, run all of these functions IN ORDER from top to bottom (Start w/ **Correct MMD Root & Center Bones**, end with **Correct Arm Wrist Twist**)

![image](https://user-images.githubusercontent.com/19479648/216136708-c97f8000-03e1-4c4b-86be-1e9c5d36da8f.png)

4) Go the **MMD** tab, click on **Convert Model**

![image](https://user-images.githubusercontent.com/19479648/216136857-5a0f9c28-d825-42dc-87c0-ca76d66d1a21.png)

5) Back on the **FFXIV MMD** tab on the **Bones and IK** panel, click on "**Add Leg and foot IK**"
6) On the "**Rigid Bodies and Joints**" panel, click on "**Add Rigid Bodies to converted MMD armature**"
7) 7) Click on **Add Joints to converted MMD armature**

![image](https://user-images.githubusercontent.com/19479648/216137068-a52465b3-09ad-4b74-8127-5b435cb5968a.png)

8) On the **Language and Translation** panel, change **To:** to **MMD Japanese w/.L.R suffix**
9) Click on **Mass Rename Bones** again

![image](https://user-images.githubusercontent.com/19479648/216137344-4d051b88-309a-488f-b83a-4323c38eb5fc.png)

10) Back on the **MMD** tab,click on the "**Physics**" button

11) Import an MMD Motion file.

![image](https://user-images.githubusercontent.com/19479648/216139143-d9f58160-0a74-4ad2-81d9-75f5ec1c6eb7.png)

12) Use MMD Tools to import a motion dance VMD file:
   When using MMD Tools' 'Import Motion' functionality to import a VMD motion file:

    - Scale should be set to '0.08' (if you imported the FBX file with a scale of 1.00 this is the correct setting to use)
    - Bone Mapper: set to 'Renamed bones'
    - 'Rename Bones - L/R Suffix' should be checked
    - 'Treat Current Pose as Rest Pose' should be checked

  ![image](https://user-images.githubusercontent.com/19479648/214442288-e62fa637-f605-4ba8-b806-6b5ee935d8d5.png)

13) Back on the **FFXIV MMD** tab on the **Shape Keys / Bone Morphs** panel, pick your model's race and select **Add Bone Morphs to FFXIV Model**

  ![image](https://user-images.githubusercontent.com/19479648/216657347-3c600aa5-3c2a-4970-ac34-32d231080795.png)


14) Use MMD Tools to import Facial Animations:
    - Under 'Assembly' click on the Morph tab. 
    - It will create a mesh called .placeholder. Click on it.
    - Then go to 'import motion', and select the same motion VMD dance file
   ![image](https://user-images.githubusercontent.com/19479648/216222723-f1f3bcc1-e17b-4b9d-9385-c447ffead7f3.png)

14) Press play. All done!! :D

--------------------------


# My old workflow:

1) Import FBX file with these parameters:
    
    Set manual orientation: Y forward, Z up
    Set primary bone: X Axis
    Set seconrd bone: Y Axis


      ![image](https://user-images.githubusercontent.com/19479648/213100063-fc5a4607-d850-44ee-9869-ea9f90389000.png)
      
2) Object will come in looking like it's on it's back.

    Set rotation X to 90
    
    ![image](https://user-images.githubusercontent.com/19479648/213100223-cf9ede44-81e1-44f5-917b-2666ec718943.png)

3) while in object mode, press CTRL+A, then apply 'Rotation', which then applied the appropriate transformations so that it treated the object's rotation as 0,0,0 to meet the global axis.

  ![image](https://user-images.githubusercontent.com/19479648/213100326-968e15ab-96f1-4188-9f80-e5801a5fa26c.png)
  
4) Use MekTools to make the textures visible so your character doesn't look like an inside-out void:

  ![image](https://user-images.githubusercontent.com/19479648/214442955-a2cdfa2a-4444-4e5c-97e9-3889c35e1685.png)

5) delete all the facial tattoo's / face paint / horrible reaper eyes from the model

6) go to the FIRST mesh's modifier properties and rename the modifier from 'n_root' to 'mmd_bone_order_override'
   ![image](https://user-images.githubusercontent.com/19479648/215369054-2f793d0f-7be8-439d-8c91-5c554bf205d8.png)


7) If you wanna use the default shape keys (for facial expressions):
    - In Object mode, select all meshes and press Ctrl+J to join them all into one mesh
    - USE FFXIV MMD Helper tool to select your FFXIV model's race and click the button to add the shape keys

8) Use FFXIV MMD Helper tool to rename bones from 'ffxiv bones' to 'MMD English'
9) Use FFXIV MMD Helper tool to add Center/Root/Goove/Waist/Waist Cancel bones
10) USE FFXIV MMD Helper tool to add IK legs bones
11) Use MMD Tools to 'Convert Model'
  ![image](https://user-images.githubusercontent.com/19479648/215303255-96e633fa-00dd-4261-9e97-89dc275e5c4c.png)
  
12) USE FFXIV MMD Helper tool to add rigid bodies

13) USE FFXIV MMD Helper tool to add joints

14)  USE FFXIV MMD Helper tool to rename the bones to 'MMD Japanese LR'


15) Use MMD Tools to import a motion dance VMD file:
   When using MMD Tools' 'Import Motion' functionality to import a VMD motion file:

    - Scale should be set to '0.08' (if you imported the FBX file with a scale of 1.00 this is the correct setting to use)
    - Bone Mapper: set to 'Renamed bones'
    - 'Rename Bones - L/R Suffix' should be checked
    - 'Treat Current Pose as Rest Pose' should be checked

  ![image](https://user-images.githubusercontent.com/19479648/214442288-e62fa637-f605-4ba8-b806-6b5ee935d8d5.png)


16) Profit!


