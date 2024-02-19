# FFXIV MMD Tools Helper (Blender Addon)
## EVERYONE in FFXIV can make their FFXIV characters move to MMD (Miku Miku Dance) animation files with as _little effort_ as possible. 

This is a Blender Addon to convert FFXIV Models to Miku Miku Dance (MMD) models. It's geared for _speed_, so you can cut down on the time it takes to:

- Export models out of FFXIV TexTools (using .chara files from [Anamnesis](https://github.com/imchillin/Anamnesis)) - [Video](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/ef673466-007f-473f-93c7-9320205ba3c9)
- Update the standard textures to the detailed ones (using the [Colorsetter Addon Shaders](https://drive.google.com/drive/folders/10ashyJJ4HhJqFxDVnGU6s9lyJ0aFHRwa)) - [Video](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/0159a68a-b682-49dc-a768-3122d81ae479)
- Convert FFXIV's .tex files to .dds files (using [ffxiv-tex-converter](https://github.com/emarron/ffxiv-tex-converter))
- Map bones from MMD models to FFXIV models (using [Animation Retargeting Addon](https://github.com/Mwni/blender-animation-retargeting))
- Apply Mektools Rig & Mektools Skin/Eye Shaders (using [MekTools Addon](https://www.xivmodarchive.com/modid/22780))
- Convert the model to MMD Format (using [MMD Tools Addon](https://github.com/UuuNyaa/blender_mmd_tools))
- Add MMD-style physics in Blender
- Animate it it in Blender (Including MMD _Facial_ Animation!)
- Export to .PMX Format (if you want to use it in the Miku Miku Dance program)

All can be done in **minutes**.

- [Download Blender Addon](https://github.com/wikid24/ffxiv_mmd_tools_helper/releases)
- [Install guide](https://github.com/wikid24/ffxiv_mmd_tools_helper/wiki/Install-Guide)
- [60 second FFXIV to MMD Conversion & Animation tutorial](https://github.com/wikid24/ffxiv_mmd_tools_helper/wiki/Quickstart-Guide)
- [Frequently Asked Questions](https://github.com/wikid24/ffxiv_mmd_tools_helper/wiki/FAQ) below.
- [User Guide / Manual Documentation](https://github.com/wikid24/ffxiv_mmd_tools_helper/wiki/Manual) for everything in the plugin, including images & videos. **Updated!**: 2023-12-02


What this tool will NOT do is allow you to import these motions back into the FFXIV game, as this is a **full model conversion** to the MMD model structure (which is not compatible _within_ the FFXIV game). 

If you want to do that, please use [XAT (FFXIV Animation Toolkit)](https://github.com/AsgardXIV/XAT) and follow this [guide](https://docs.google.com/document/d/1siUjAAJjUk7-Nlq11wE-Sldr8UyCeu7SkFJzUsxZpTU/edit). FFXIV models converted to MMD with this addon must be treated as your **source MMD model**, NOT your destination/target FFXIV model. Instead of this, **I recommend using ['Kaito' MMD Model modified with Skirt Physics](https://github.com/wikid24/ffxiv_mmd_tools_helper/raw/master/sample_files/KAITOwPhy-RexZ.zip)** as it has been tested and proven to work easier with ffxiv skirt physics. Once you have experience with doing this successfully, you can move on to intermediate-level face/lip animations using Haine's [Working With Custom Lip Animations](https://docs.google.com/document/d/1y0hLaO6WA7C6ayT7udr0puNAa7PY5qDvcRC9RDanTDg/edit) guide.

While this tool is geared towards FFXIV model conversion to MMD, the majority of it's features can be used on any models that leverage the [MMD Tools](https://github.com/UuuNyaa/blender_mmd_tools) addon for Blender.

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
  
------------

# In order to use this tool, you need:
   - [Blender](https://www.blender.org/) (2.80+) or higher installed. Only [Blender 3.6 LTS](https://www.blender.org/download/lts/) is _officially_ supported, **BLENDER 4.0 DOES NOT WORK YET**([issue](https://github.com/wikid24/ffxiv_mmd_tools_helper/issues/5)).
   - [MMD Tools addon](https://github.com/UuuNyaa/blender_mmd_tools) for Blender
   - A FFXIV Model exported into .FBX file format
   - .VMD animation files (MMD animation files) - [Deviant Art](https://www.deviantart.com/mmd-dance-comunnity/gallery/36305808/motion-dl), [bowlroll](https://bowlroll.net/),[Reddit](https://www.reddit.com/r/mikumikudance/) or UuuNyaa's Helper addon (listed below)

# Not really needed but recommended:
### FFXIV Export to Blender Stuff:
   - [Anamnesis](https://github.com/imchillin/Anamnesis) - Used for finding out the character data in FFXIV leveraging the .chara file. _This_ addon is now integrated with it to make it faster and easier to use!
   - [FFXIV TexTools](https://www.ffxiv-textools.net/) Used for exporting the character data into .FBX format - [Video Tutorial](https://www.youtube.com/watch?v=JbkNt51PRyM) - watch the first 7 minutes
   - [XIV Tools Discord](https://discord.com/invite/KvGJCCnG8t) - Where to find help on FFXIV Rigging

### Blender to FFXIV Import Stuff:
   - [XAT](https://github.com/AsgardXIV/XAT) FFXIV Animation Toolkit - Standalone tool for manipulating animations and skeletons in Final Fantasy XIV. Needed to play any custom animation .pap files created & exported out of blender
   

### Blender Addon Stuff:
   - [FFXIV Colorsetter Blender Addon](https://drive.google.com/drive/folders/10ashyJJ4HhJqFxDVnGU6s9lyJ0aFHRwa) - Blender Addon for better FFXIV Materials/Textures/Shaders. _This_ addon is now integrated with it to make it faster and easier to use! - [Video Tutorial #1](https://user-images.githubusercontent.com/19479648/215879548-67bd503e-70b4-4255-abe4-bc1bbcb06618.mp4) [Video Tutorial #2](https://www.youtube.com/watch?v=AhVzU_BK6zk)
   - [FFXIV MekTools Blender Addon](https://www.xivmodarchive.com/modid/22780) for Blender to fix inside-out alpha (if you're not using this tool to import). Also, it has a pretty good skin shader, but I haven't gotten all the controls to work properly to be honest. _This_ addon is now integrated with it to make it faster and easier to use!
   - [UuuNyaa's MMD Tools Helper Blender Addon](https://github.com/UuuNyaa/blender_mmd_uuunyaa_tools) addon for MMD Tools for Blender, a bunch of useful tools for animating MMD Models (including lighting presets, material presets, physics tools etc...)
   - [Animation Retargeting Addon](https://github.com/Mwni/blender-animation-retargeting) for Blender - Needed to copy animations from one model to another model (such as a MMD model to a FFXIV Model) since they have different bone names and bone structures. Used in conjunction with the [XAT](https://github.com/AsgardXIV/XAT) addon to play MMD Animations in FFXIV. _This_ addon is now integrated with it to make it faster and easier to use!
   - [Auto-Rig Pro](https://blendermarket.com/products/auto-rig-pro) - A paid application that does what [Animation Retargeting Addon](https://github.com/Mwni/blender-animation-retargeting) does, but apparently is faster and easier to use. I don't know, I never tried it, but the more experienced FFXIV XAT animators swear by it.
   - [Gravity Collider Bone Physics Addon](https://github.com/MiniEval/Bone-Physics) - I haven't tried it, but its a free and easy way to add skirt and hair physics (if you're sticking simply in Blender)

### MMD Animation in Blender Stuff:
   - The original MMD model (.pmx file) that the VMD animation files were based on (useful for animation scaling reasons)
   - PMX files (MMD model files) - [Deviant Art](https://www.deviantart.com/mmd-downloads-galore/gallery/39472353/models), [bowlroll](https://bowlroll.net/),[Reddit](https://www.reddit.com/r/mikumikudance/) or UuuNyaa's Helper addon (listed above)
   
   
### MMD (application) Rendering Stuff:
   - [Miku Miku Dance (application)](https://learnmmd.com/downloads/) (duh)
   - [PMX Editor](https://www.deviantart.com/inochi-pm/art/PmxEditor-vr-0254f-English-Version-v2-0-766313588) - MMD's Model Editor for PMX files
   - A bunch of MMD effects: (will list them later)
   - [MikuMikuEffects](https://learnmmd.com/downloads/) - [Install Tutorial](https://www.youtube.com/watch?v=qPOX1eLg3nY)
   - [Ray MMD](https://github.com/ray-cast/ray-mmd/releases) - [Install Tutorial/Beginner's Guide](https://learnmmd.com/http:/learnmmd.com/using-ray-mmd-ver-1-5-0-beginners-guide/)
   - [Alpha Textures Fix](https://www.deviantart.com/dendewa/art/RayMMD-Alpha-Fix-DOWNLOAD-848877809)

------------
# Useful Guides:
- [FFXIV TexTools Hex Color Reference List](https://docs.google.com/spreadsheets/d/18Z1ph1Xa-rFvC8FtB7X6IgSbjwPAom5XuDuCtVeNRvo)
- [MMD Facial Expression Reference guide](https://www.deviantart.com/xoriu/art/MMD-Facial-Expressions-Chart-341504917)
- [XIV Mod Archive - Useful guides to exporting](https://www.xivmodarchive.com/modid/9408) 
- [MMD Skirt Rigging Tutorial: Video Tutorial](https://www.youtube.com/watch?v=cGcBfhYyjC8)
- [UuuNyaa's Physics Adjuster: Video Tutorial](https://www.youtube.com/watch?v=pRJNJDFSYfk)
- [MMD Tools wiki](https://mmd-blender.fandom.com/wiki/MMD_Tools/Manual)
- [XAT Animation - Body Retargeting Guide](https://docs.google.com/document/d/1siUjAAJjUk7-Nlq11wE-Sldr8UyCeu7SkFJzUsxZpTU/edit) - An alternative approach to animating FFXIV characters using MMD motion files
- [XAT Animation - Working With Custom Lip Animations](https://docs.google.com/document/d/1y0hLaO6WA7C6ayT7udr0puNAa7PY5qDvcRC9RDanTDg/edit)
- [FFXIV TexTools Reference Data](https://docs.google.com/spreadsheets/d/1kIKvVsW3fOnVeTi9iZlBDqJo6GWVn6K6BCUIRldEjhw/edit#gid=296196266)

