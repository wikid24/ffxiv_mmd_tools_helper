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
- A bunch of important useful still. Will list them later.

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
- To have your character exported into FBX file format (using FFXIV TexTools)
- Blender (2.80+) or higher installed
- 'MMD Tools' addon for Blender
- uuuunaya's Helper addon to  MMD Tools for Blender
- MekTools addon for Blender

Not really needed but recommended:
- MMD (duh)
- PXE (MMD character file editor for PMX files)
- PMX files (MMD character files)
- VMD files (MMD character/camera animation/dance files)
- A bunch of MMD effects (will list them later)


