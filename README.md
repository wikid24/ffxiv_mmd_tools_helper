# this is a fork of Hogarth-MMD's [mmd_tools_helper](https://github.com/Hogarth-MMD/mmd_tools_helper), updated to be compatible with FFXIV Models and Blender 2.8+. It's a work in progress.

Purpose of this tool is for EVERYONE in FFXIV to start exporting their favorite FFXIV characters to MMD so we can all make memes of dancing and music videos with as little effort as possible. Once I get this tool out of alpha, detailed tutorials on how to export FFXIV characters to MMD will come. For now, just check the simple [60 second conversion](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/README.md#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow) tutorial below

------------

# New Features:
  - Auto generate Bone Morphs (Facial Expressions)
      - working for Hyur so far (but can be used on other races)
  - Auto generate Rigid Bodies (Physics blocks)
      - working but only partially completed (so far)
  - Auto generate Joints
      - working but only partially completed (so far)
  - Auto generate Bone Groups
  - Auto generate Shape Keys from csv
      - Working for Hyur, partially completed (so far)
  - Skirt rig generator
      - Add new skirt bones + weight paint existing skirt meshes with a few clicks.
  - Auto generate MMD Display Panel groups
  - Auto Sort the MMD Bone Order and Deformation Tiers
  - Auto-fix MMD Bone Names
  - Bulk Update Rigid Bodies and set starting/ending values in a rigid body chain (with new powerful search features!)
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
- Add presets for skirt/hair for bulk-update to Rigid Bodies (skirts heaviest on the bottom, hair heaviest on the top?)
- Create 'bulk-add joints' with min/max values:
    - Add presets for skirt/hair (skirts heaviest on the bottom, hair heaviest on the top?)
- Automate MMD Tools material sorter
- Automate the fix for materials/shaders - ([ffxiv material shader fix plugin](https://drive.google.com/drive/folders/10ashyJJ4HhJqFxDVnGU6s9lyJ0aFHRwa) )
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
- A bunch of MMD effects: (will list them later)
- [MikuMikuEffects](https://learnmmd.com/downloads/) - [Install Tutorial](https://www.youtube.com/watch?v=qPOX1eLg3nY)
- [Ray MMD](https://github.com/ray-cast/ray-mmd/releases) - [Install Tutorial/Beginner's Guide](https://learnmmd.com/http:/learnmmd.com/using-ray-mmd-ver-1-5-0-beginners-guide/)
- [Alpha Textures Fix](https://www.deviantart.com/dendewa/art/RayMMD-Alpha-Fix-DOWNLOAD-848877809)

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

# How to rig a character and get it dancing less than 60 seconds (my new workflow):

On the **FFXIV MMD** tab
1) On the **Import an FFXIV Model** panel, click on  **Import your model FBX File**
2) On the **Language and Translation** panel, click on "**Mass Rename Bones**" (from FFXIV to MMD English)
3) On the **Bones and IK** panel, run all of these functions IN ORDER from top to bottom (Start w/ **Correct MMD Root & Center Bones**, end with **Add Shoulder Control Bones**)

![image](https://user-images.githubusercontent.com/19479648/217979381-7c6f51bb-7688-4efd-8625-8ef111ce23c6.png)

4) On the **Bones and IK** panel, click on **Add leg/foot IK**

![image](https://user-images.githubusercontent.com/19479648/217979835-044061eb-ef14-4266-b33c-ea048a38b016.png)


5) Go the **MMD** tab
6) click on **Convert Model**

![image](https://user-images.githubusercontent.com/19479648/217980088-a3cbad2d-f35a-4bf2-b76d-8b384e34deb5.png)

7) Back on **FFXIV MMD** tab, with your model selected, go to "**Rigid Bodies and Joints**" -> "**Add Rigid Bodies**"
8) With your model selected, go to "**Rigid Bodies and Joints**" -> "**Add Joints**"
9) On the **Shape Keys / Bone Morphs** tab, select your model's race and click on **Import Bone Morphs from File**

![image](https://user-images.githubusercontent.com/19479648/217980615-5c8b0469-63e9-4c70-9c11-4dc1f8b14dd1.png)

10) On the Scene Outliner View, click on **New MMD Model**
11) Go to **MMD** tab
12) Under Assembly section click on **All**

![image](https://user-images.githubusercontent.com/19479648/217982914-77067a23-a2ea-47da-99da-ed408d90477b.png)

13) Click on **FFXIV MMD** tab
14)  On the **Language and Translation** panel, change **To:** to **MMD Japanese w/.L.R suffix**
15) Click on **Mass Rename Bones** again

![image](https://user-images.githubusercontent.com/19479648/217983389-f0c07ebf-c535-4968-82a5-543e47dd870e.png)

16) On the Scene Outliner View, click on **n_root**
17) Click on **MMD** tab
18) On the **Scene Setup tab, click on **Motion Import**

![image](https://user-images.githubusercontent.com/19479648/217983858-47f90e84-74ea-47a2-bbef-5f33b055d9f0.png)

19) Use MMD Tools to import a motion dance VMD file:
    - Bone Mapper: set to 'Renamed bones'
    - 'Rename Bones - L/R Suffix' should be checked
    - 'Treat Current Pose as Rest Pose' should be checked
    - select your VMD file
    - import VMD file

![image](https://user-images.githubusercontent.com/19479648/217984754-27ce81b7-7c5a-4c2c-a9b4-31fd00b1be83.png)

20) On the Scene Outliner View, click on **.placeholder**, and click on **Motion Import** again

![image](https://user-images.githubusercontent.com/19479648/217985991-70de46c7-1fef-4804-b80b-38089e3aff4d.png)



21) Use MMD Tools to import a motion dance VMD file:
    - Bone Mapper: set to 'Renamed bones'
    - 'Rename Bones - L/R Suffix' should be checked
    - 'Treat Current Pose as Rest Pose' should be checked
    - select your VMD file
    - import VMD file
   ![image](https://user-images.githubusercontent.com/19479648/217985065-779437ea-8c2a-4013-a781-50edcd759789.png)

22) Press play to watch your character dance. All done!! :D
