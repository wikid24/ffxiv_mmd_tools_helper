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
- MMD Tools uses Shadow bone and D bones -- find a way to get MMD Tools to make them for me (or are they really necessary?)
- automate the bone order export for PMX export (should be easy since ffxiv bones are mostly standard across the board)
- get a list of all the mmd tools properties/ property names so I can can manipulate them directly from python

New Features (completed):
- added 'Automate FFXIV rig Shape Keys' feature. Working but it doesn't have any raw data to work with yet.
- A bunch of important useful stuff. Will list them later.

Conversion/upgrade to Blender 2.8+ (to do):
  - add_hand_arm_ik.py
  - armature_diagnostic.py
  - background_color_picker.py
  - delete_mmd_model_part.py
  - fix_bones_for_IK.py
  - mmd_lamp_setup.py
  - mmd_view.py
  - toon_modifier.py
  - toon_textures_to_node_editor_shader.py

In order to use this tool, you need:
- To have your character exported into FBX file format (using FFXIV TexTools) - https://www.ffxiv-textools.net/
- Blender (2.80+) or higher installed - https://www.blender.org/
- 'MMD Tools' addon for Blender - https://github.com/UuuNyaa/blender_mmd_tools
- uuunyaa's Helper addon to  MMD Tools for Blender - https://github.com/UuuNyaa/blender_mmd_uuunyaa_tools
- MekTools addon for Blender - https://www.xivmodarchive.com/modid/22780

Not really needed but recommended:
- MMD (duh) - https://learnmmd.com/downloads/
- PXE (MMD 3d modeling editor for PMX files) - https://www.deviantart.com/inochi-pm/art/PmxEditor-vr-0254f-English-Version-v2-0-766313588
- PMX files (MMD model files) - https://www.deviantart.com/mmd-downloads-galore/gallery/39472353/models (or you can find the majority of them on asian websites that I can't understand without google translate)
- VMD files (MMD character/camera animation/dance files) - https://www.deviantart.com/mmd-dance-comunnity/gallery/36305808/motion-dl or check reddit or again, asian websites
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
4) Go to Edit Mode, select all bones by pressing 'A', then select 'Clear Roll'
![image](https://user-images.githubusercontent.com/19479648/213671651-c2294687-66d0-4330-b276-8c80014619b5.png)

5) Use FFXIV MMD Helper tool to rename bones from 'ffxiv bones' to 'MMD English'
6) Use FFXIV MMD Helper tool to add Center/Root/Goove/Waist Bones
7) USE FFXIV MMD Helper tool to add shape keys
8) USE FFXIV MMD Helper tool to add IK legs bones
9) Move the bone constraints from KNEE L/R to j_asi_l_c and j_asi_r_c respectively. Set 'Chain' property from 2 to 3. Should fix the legs orientation
10) Import VMD file to check if motion is working
11) Profit!
12) USE MMD Tool to 'Convert' to a MMD Armature

