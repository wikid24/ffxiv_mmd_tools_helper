# this is a fork of Hogarth-MMD's mmd_tools_helper (https://github.com/Hogarth-MMD/mmd_tools_helper), updated to be compatible with ffxiv and Blender 2.8+. It's a work in progress.

Purpose of this tool is for EVERYONE in FFXIV to start exporting their favorite FFXIV characters to MMD so we can all make memes of dancing and music videos with as little effort as possible. Once I get this tool working, tutorials on how to export FFXIV characters to MMD will come. 




Todo stuff:

New Features (to do):
- ffxiv shape keys:
  - Populate the shape keys files (facial animation sliders) -- 55 shape keys for each of the 8 races...  440 in all! :S. Reference guide: https://www.deviantart.com/xoriu/art/MMD-Facial-Expressions-Chart-341504917
  - Allow for a user to upload their OWN custom shape key csv file (instead of relying on the ones that come as part of this addon)
  - Find a way to export shape key data to CSV file (in a similar format as the IMPORT shape keys CSV)
- Automate the rigify armature bones to match ffxiv armature bones (should be mostly easy, the majority of it is a 1:1 'transform rigify bone to match the ffxiv bone's position/rotation data)
- fix IK to match double jointed knees (move the bone constraints to j_asi_c_l instead of j_asi_b_l, set the chain=3 instead of 2)
- display_panel_groups.py - needs to be updated to match the ffxiv bone structure
- automate the bone order export for PMX export (should be easy since ffxiv bones are mostly standard across the board)
- find a way to auto-generate rigid bodies (https://github.com/12funkeys/rigid_bodys_gen - https://www.youtube.com/watch?v=0haYapQ7l_U )

New Features (completed):
- added 'Automate FFXIV rig Shape Keys' feature. Working but it doesn't have any raw data to work with yet.
- A bunch of important useful stuff. Will list them later.

Conversion/upgrade to Blender 2.8+ (to do):
  - add_hand_arm_ik.py
  - mmd_lamp_setup.py
  - mmd_view.py
  - toon_textures_to_node_editor_shader.py (it works, sort of... I need to understand shaders more)

In order to use this tool, you need:
- To have your character exported into FBX file format (using FFXIV TexTools) - https://www.ffxiv-textools.net/
- Blender (2.80+) or higher installed - https://www.blender.org/
- 'MMD Tools' addon for Blender - https://github.com/UuuNyaa/blender_mmd_tools
- uuunyaa's Helper addon to  MMD Tools for Blender - https://github.com/UuuNyaa/blender_mmd_uuunyaa_tools
- MekTools addon for Blender - https://www.xivmodarchive.com/modid/22780

Not really needed but recommended:
- MMD (duh) - https://learnmmd.com/downloads/
- PMXE (MMD 3d modeling editor for PMX files) - https://www.deviantart.com/inochi-pm/art/PmxEditor-vr-0254f-English-Version-v2-0-766313588
- PMX files (MMD model files) - https://www.deviantart.com/mmd-downloads-galore/gallery/39472353/models (or you can find the majority of them on asian websites that I can't understand without google translate), alternatively you can use uuunyaa's Helper addon to download some models from within Blender
- VMD files (MMD character/camera animation/dance files) - https://www.deviantart.com/mmd-dance-comunnity/gallery/36305808/motion-dl or check reddit or again, asian websites. Alternatively you can use uuunyaa's Helper addon to download some VMD files from within Blender
- A bunch of MMD effects (will list them later)

------------

My current workflow:

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

5) Important if you wanna use the default shape keys (for facial expressions):
    - In Object mode, select all meshes and press Ctrl+J to join them all into one mesh
    - USE FFXIV MMD Helper tool to select your FFXIV model's race and click the button to add the shape keys

6) Use FFXIV MMD Helper tool to rename bones from 'ffxiv bones' to 'MMD English'
7) Use FFXIV MMD Helper tool to add Center/Root/Goove/Waist/Waist Cancel
8) USE FFXIV MMD Helper tool to add IK legs bones

9)  USE FFXIV MMD Helper tool to rename the bones to 'MMD Japanese LR'

10) Use MMD Tools to import a motion dance VMD file:
   When using MMD Tools' 'Import Motion' functionality to import a VMD motion file:

    - Scale should be set to '0.08' (it should match the same scale you imported the FBX model with)
    - Bone Mapper: set to 'Renamed bones'
    - 'Rename Bones - L/R Suffix' should be checked
    - 'Treat Current Pose as Rest Pose' should be checked

  ![image](https://user-images.githubusercontent.com/19479648/214442288-e62fa637-f605-4ba8-b806-6b5ee935d8d5.png)


11) Profit!
12) USE MMD Tools to 'Convert' to a MMD Armature

