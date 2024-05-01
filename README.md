# FFXIV MMD Tools Helper (Blender Addon)
## Convert FFXIV Models to MMD Models with as _little effort_ as possible.

> Update: 2024-04-19 - Updates are on hold until Dawntrail comes out (I might to have to rewrite the entire plugin)

This is a Blender Addon to convert FFXIV Models to Miku Miku Dance (MMD) models. It's geared for _speed_, so you can cut down on the time it takes to:

- Export models out of FFXIV TexTools (using .chara files from [Anamnesis](https://github.com/imchillin/Anamnesis)) - [Guide](https://github.com/wikid24/ffxiv_mmd_tools_helper/wiki/Export-.fbx-from-Textools-using-Anamnesis)
- Update the standard textures to the detailed ones (using the [Colorsetter Addon Shaders](https://drive.google.com/drive/folders/10ashyJJ4HhJqFxDVnGU6s9lyJ0aFHRwa)) - [Guide(Equipment)](https://github.com/wikid24/ffxiv_mmd_tools_helper/wiki/Apply-Colorsetter-Shaders-to-Equipment) / [Guide(body parts)](https://github.com/wikid24/ffxiv_mmd_tools_helper/wiki/Apply-Colorsetter-Shaders-to-Body-Parts)
- Convert FFXIV's .tex files to .dds files (using [ffxiv-tex-converter](https://github.com/emarron/ffxiv-tex-converter)) - [Guide](https://github.com/wikid24/ffxiv_mmd_tools_helper/wiki/Batch-convert-between-.tex-&-.dds)
- Map bones from MMD models to FFXIV models (using [Animation Retargeting Addon](https://github.com/Mwni/blender-animation-retargeting))
- Apply Mektools Rig & Mektools Skin/Eye Shaders (using [MekTools Addon](https://www.xivmodarchive.com/modid/22780)) - [Guide](https://github.com/wikid24/ffxiv_mmd_tools_helper/wiki/Apply-Mektools-Shaders-to-Body-Parts)
- Convert the model to MMD Format (using [MMD Tools Addon](https://github.com/UuuNyaa/blender_mmd_tools))
- Add MMD-style physics in Blender
- Animate it it in Blender (Including MMD _Facial_ Animation!)
- Export to .PMX Format (if you want to use it in the Miku Miku Dance program)

All can be done in **minutes**.

### - [Download Blender Addon](https://github.com/wikid24/ffxiv_mmd_tools_helper/releases)
### - [Install guide](https://github.com/wikid24/ffxiv_mmd_tools_helper/wiki/Install-Guide)
### - [60 second FFXIV to MMD Conversion & Animation tutorial](https://github.com/wikid24/ffxiv_mmd_tools_helper/wiki/Import-and-Animate-an-FFXIV-character)
### - [Frequently Asked Questions](https://github.com/wikid24/ffxiv_mmd_tools_helper/wiki/FAQ)
### - [User Guide / Manual Documentation](https://github.com/wikid24/ffxiv_mmd_tools_helper/wiki/Manual)


#### DISCLAIMER
This is designed a **full model conversion** to the MMD structure to be used in **Blender or MMD only** (which is not compatible _within_ FFXIV).  

Anything this plugin creates must be treated your **source MMD model**, NOT your destination/target in-game FFXIV model.

If you want to convert MMD animations that can be used _within FFXIV_, instead of using this addon:
 - Use [XAT](https://github.com/AsgardXIV/XAT) and follow this [guide](https://docs.google.com/document/d/1siUjAAJjUk7-Nlq11wE-Sldr8UyCeu7SkFJzUsxZpTU/edit).
 - For source MMD Model, **I recommend using ['Kaito' MMD Model modified with Skirt Physics](https://github.com/wikid24/ffxiv_mmd_tools_helper/raw/master/sample_files/KAITOwPhy-RexZ.zip)**
 - Once you have experience with doing this successfully, you can move on to intermediate-level face/lip animations using Haine's [Working With Custom Lip Animations](https://docs.google.com/document/d/1y0hLaO6WA7C6ayT7udr0puNAa7PY5qDvcRC9RDanTDg/edit) guide (which does leverage this addon as part of the workflow).

While this tool is geared towards FFXIV model conversion to MMD, the majority of it's features can be used on _any MMD models_ that leverage the [MMD Tools](https://github.com/UuuNyaa/blender_mmd_tools).

If you have questions you can find me (wikid24) in Discord on [XIV Tools](https://discord.gg/xivtools) mostly active in  #xat-discussion channel.

I need your help to improve this plugin! Please leave suggestions / comments [here](https://github.com/wikid24/ffxiv_mmd_tools_helper/issues)

------------

#### Sample Video 1: Thancred & Sadu - skirt physics testing

https://user-images.githubusercontent.com/19479648/225201036-c3c85e70-ea17-4100-89c9-f22462ae71b9.mp4

Credits: 
- Video/model conversion by me (wikid24)
- Model by Square Enix
- MMD Body Motion by sn - https://www.nicovideo.jp/watch/sm36532472
- MMD Facial/Camera Motion by Marshmallow Machine - https://bowlroll.net/file/221190
- Song - Honeymoon Un Deux Trois (cover) by dongdang - https://www.youtube.com/watch?v=z8i6JnznAi8

#### Sample Video 2: Hythlodaeus, Gauis and Erenville - testing rigging/conversion/rendering in less than 30 minutes (no physics on the hair)

https://user-images.githubusercontent.com/19479648/225201333-e3e72554-bf2a-4cea-9fe5-b503e51946b8.mp4

Credits: 
- Video/model conversion by me (wikid24)
- Model by Square Enix
- MMD Body/Facial/Camera Motion by Temporal7Lizardo - http://www.mediafire.com/file/935qedyecesu9t5/Everybody.7z/file
- Song - Everybody by Backstreet Boys


#### Sample Video 3: Random WOL - Manually-created hair physics testing

https://user-images.githubusercontent.com/19479648/225201368-46c79f71-307e-4130-91c6-0342e539fbc6.mp4

Credits:
- Video/model conversion by me (wikid24)
- Model by Square Enix
- MMD Facial/Body Motion by かりんとう - https://www.nicovideo.jp/watch/sm33513391
- Song - Elephant (Ignite) by Funkin Matt - 


#### Sample Video 4: Random WOL vs Aura WOL - Importing Kugane



https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/97924ad0-c5bf-42f3-be2b-0d3a800dcbea


Credits:
- Video/model conversion by me (wikid24)
- Model by Square Enix
- Background by Square Enix - https://www.nexusmods.com/finalfantasy14/mods/1709
- MMD Facial/Body Motion by mahlazer - https://www.youtube.com/watch?v=HuzxtZj-AYI
- Song - U Got That - Halogen (Little V cover) - https://www.youtube.com/watch?v=j8xoV-v1Yl0&t=0s

------------

# New Features:
  - Auto-convert the FFXIV bone structure to match MMD Models
  - Auto generate Bone Morphs (Facial Expressions)
      - working for all races, Hrothgar needs a bit more fine-tuning but it works fine
  - Auto generate Rigid Bodies (Physics blocks)
  - Auto generate Joints
  - Auto generate Bone Groups
  - Skirt rig bone + weight painting generator (for physics)
      - Add new skirt bones + weight paint existing skirt meshes with a few clicks.
  - Auto generate MMD Display Panel groups
  - Auto Sort the MMD Bone Order and Deformation Tiers
  - Auto-fix/Translate MMD Bone Names
  - Bulk Update Rigid Bodies and set starting/ending values in a rigid body chain (with new powerful search features!)
  - Automating the application of the [ColorSetter Addon](https://drive.google.com/drive/folders/10ashyJJ4HhJqFxDVnGU6s9lyJ0aFHRwa) to materials (to make using it [faster](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/fc155d0b-4367-4324-be24-424f19bf63d4))
  - Automating the application of the [MekTools Addon](https://www.xivmodarchive.com/modid/22780): Integrated the FFXIV Rigs as well as the skin shader!
  - Auto-import of .chara files from [Anamnesis](https://github.com/imchillin/Anamnesis): Will apply the face deformations, as well as read back all the skin/hair/face paint color info to the Blender logs, to be able to select and export the EXACT files & needed to export out of TexTools
  - Auto convert .tex to .dds leveraging the [FFXIV Tex Converter](https://github.com/emarron/ffxiv-tex-converter) library from emarron. Pull files _directly_ from FFXIV and import them to your model immediately!
  - Automation of the bone mapping leveraging the [Animation Retargeting](https://github.com/Mwni/blender-animation-retargeting) addon! Will automatically map bones as well as apply bone rotation from any source MMD/FFXIV model (including FFXIV converted to MMD with this addon) with one click of a button!
  - Apply FFXIV Face Paint images with all the included color shader settings
  - Calculate the VMD import scale by comparing a MMD Armature against your target armature with included Bone Scale Compare tool
  - A bunch of other important useful stuff... Will list them all later!

# To do:
-  FFXIV Bone Morphs (facial animation sliders):
   - Allow for user to upload their OWN csv file (instead of using the template in this addon)
- Add 'Transform Rigify armature to match ffxiv armature'
- Add presets for skirt/hair for bulk-update to Rigid Bodies (skirts heaviest on the bottom, hair heaviest on the top?)
- Create 'bulk-add joints' with min/max values:
    - Add presets for skirt/hair (skirts heaviest on the bottom, hair heaviest on the top?)
  
