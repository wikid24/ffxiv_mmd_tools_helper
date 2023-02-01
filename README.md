# this is a fork of Hogarth-MMD's mmd_tools_helper (https://github.com/Hogarth-MMD/mmd_tools_helper), updated to be compatible with FFXIV Models and Blender 2.8+. It's a work in progress.

Purpose of this tool is for EVERYONE in FFXIV to start exporting their favorite FFXIV characters to MMD so we can all make memes of dancing and music videos with as little effort as possible. Once I get this tool working, tutorials on how to export FFXIV characters to MMD will come. 

------------

# New Features (completed):
- added 'Automate FFXIV rig Shape Keys from csv' feature. Working but there's no raw data in the CSVs yet.
- added 'Automate FFXIV rig Bone Morphs from csv' feature. Working but there's no raw data in the CSVs yet.
- added 'Automate FFXIV rig Rigid Bodies from csv' feature. Working but there's no raw data in the CSVs yet.
- added 'Automate FFXIV rig Joints from csv' feature. Working but it doesn't have any raw data in the CSVs yet.

- A bunch of important useful stuff. Will list them later.

# Conversion/upgrade to Blender 2.8+ (to do):
  - mmd_lamp_setup.py
  - mmd_view.py
  - toon_textures_to_node_editor_shader.py (it works, sort of... I need to understand shaders more)

# To do:
- ffxiv shape keys:
  - Populate the shape keys files (facial animation sliders) -- 55 shape keys for each of the 8 races...  440 in all! :S. Reference guide: https://www.deviantart.com/xoriu/art/MMD-Facial-Expressions-Chart-341504917
  - Allow for a user to upload their OWN custom shape key csv file (instead of relying on the ones that come as part of this addon)
- Automate the rigify armature bones to match ffxiv armature bones (should be mostly easy, the majority of it is a 1:1 'transform rigify bone to match the ffxiv bone's position/rotation data)
- display_panel_groups.py - needs to be updated to match the ffxiv bone structure
- automate the bone order export for PMX export (should be easy since ffxiv bones are mostly standard across the board)
- auto-generate rigid bodies instead of using csv (https://github.com/12funkeys/rigid_bodys_gen - https://www.youtube.com/watch?v=0haYapQ7l_U )
    - Add presets for skirts (set min max settings, will generate for the entire chain, heaviest on the bottom)
    - Add presets for hair (set min max settings, will generate for the entire chain, heaviest on the top)
- auto-generate joints instead of using csv:
    - Add presets for boobs (figure out the proper boobs parameters)
    - Add presets for skirts (set min max settings, will generate for the entire chain, heaviest on the bottom)
    - Add presets for hair (set min max settings, will generate for the entire chain, heaviest on the top)
- automate the MMD material sorter population:
    - not sure which way to go with this-- should I take the original mesh parts and automate them as their own single material the MMD tools panel? 
    - or should I create a new hierarchy based on hair/skirt/etc...?
    - or should I do it based on individual textures?
    - or should create an option to pick/choose one vs the other?
------------

# In order to use this tool, you need:
- To have your character exported into FBX file format (using FFXIV TexTools) - https://www.ffxiv-textools.net/
- Blender (2.80+) or higher installed - https://www.blender.org/
- 'MMD Tools' addon for Blender - https://github.com/UuuNyaa/blender_mmd_tools
- uuunyaa's Helper addon to  MMD Tools for Blender - https://github.com/UuuNyaa/blender_mmd_uuunyaa_tools

# Not really needed but recommended:
- Miku Miku Dance (duh) - https://learnmmd.com/downloads/
- PMXE (MMD 3d modeling editor for PMX files) - https://www.deviantart.com/inochi-pm/art/PmxEditor-vr-0254f-English-Version-v2-0-766313588
- PMX files (MMD model files) - https://www.deviantart.com/mmd-downloads-galore/gallery/39472353/models (or you can find the majority of them on asian websites that I can't understand without google translate), alternatively you can use uuunyaa's Helper addon to download some models from within Blender
- VMD files (MMD character/camera animation/dance files) - https://www.deviantart.com/mmd-dance-comunnity/gallery/36305808/motion-dl or check reddit or again, asian websites. Alternatively you can use uuunyaa's Helper addon to download some VMD files from within Blender
- A bunch of MMD effects (will list them later)
- MekTools addon for Blender - https://www.xivmodarchive.com/modid/22780


------------
# Useful Guides:
- Useful guides to exporting: https://www.xivmodarchive.com/modid/9408
- FIX FFXIV Textures in blender addon: https://drive.google.com/drive/folders/10ashyJJ4HhJqFxDVnGU6s9lyJ0aFHRwa
- Quick tutorial how to use the FFXIV Shader plugin above: https://user-images.githubusercontent.com/19479648/215879548-67bd503e-70b4-4255-abe4-bc1bbcb06618.mp4
- XAT guide to animation retargeting (an alternative approach to animating MMD using FFXIV characters) https://docs.google.com/document/d/1siUjAAJjUk7-Nlq11wE-Sldr8UyCeu7SkFJzUsxZpTU/edit

------------

# How to Install

 - Download the latest release package.zip
 - Go to Edit -> Preferences -> Add-ons -> Install and select the zip file you downloaded
  ![image](https://user-images.githubusercontent.com/19479648/215303847-8a5b34de-b8be-4070-9ab7-dc51ada3fc10.png)
  
 - In the search box, type in 'ffxiv' until the addon 'Object: FFXIV MMD Tools Helper' shows up and check the checkbox
  ![image](https://user-images.githubusercontent.com/19479648/215303990-62fca28b-79b3-4648-b620-d9c6b0f5aa3c.png)

 - Once you see "ffxiv_mmd_tools_helper", you'll know it is installed correctly. All of the tools are located here.
  ![image](https://user-images.githubusercontent.com/19479648/215304046-309d996e-939e-458c-9d0f-1dc626972931.png)


# My new workflow:

On the **FFXIV MMD** tab
1) On the **Import an FFXIV Model** panel, click on  **Import your model FBX File**
2) On the **Language and Translation** panel, click on "**Mass Rename Bones**" (from FFXIV to MMD English)
3) On the **Misc/Testing/Diagnostics** panel, run all of these functions IN ORDER from top to bottom (Start w/ **Correct MMD Root & Center Bones**, end with **Correct Arm Wrist Twist**)

![image](https://user-images.githubusercontent.com/19479648/216136708-c97f8000-03e1-4c4b-86be-1e9c5d36da8f.png)

4) Go the **MMD** tab, click on **Convert Model**

![image](https://user-images.githubusercontent.com/19479648/216136857-5a0f9c28-d825-42dc-87c0-ca76d66d1a21.png)

5)Back on the **FFXIV MMD** tab on the "**Bones and IK**" panel, click on **Add Leg and foot IK**
6) On the "**Rigid Bodies and Joints**" panel, click on **Add Rigid Bodies to converted MMD armature**
7) Click on **Add Joints to converted MMD armature**
![image](https://user-images.githubusercontent.com/19479648/216137068-a52465b3-09ad-4b74-8127-5b435cb5968a.png)

8) On the **Language and Translation** panel, change **To: ** to **MMD Japanese w/.L.R suffix**
9) Mass Rename Bones again

![image](https://user-images.githubusercontent.com/19479648/216137344-4d051b88-309a-488f-b83a-4323c38eb5fc.png)

10) Back on the **MMD** tab,click on the "**Physics**" button
11) Import an MMD Motion file.
12) Press Play. You're done!

![image](https://user-images.githubusercontent.com/19479648/216139143-d9f58160-0a74-4ad2-81d9-75f5ec1c6eb7.png)


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


