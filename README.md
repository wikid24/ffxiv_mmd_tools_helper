# FFXIV MMD Tools Helper
## EVERYONE in FFXIV can make their FFXIV characters move to MMD (Miku Miku Dance) animation files with as _little effort_ as possible. 

Once I get this tool out of alpha, detailed tutorials on how to export FFXIV characters to MMD will come. 

- [download here](https://github.com/wikid24/ffxiv_mmd_tools_helper/releases)
- [install guide](https://github.com/wikid24/ffxiv_mmd_tools_helper#how-to-install)
- [60 second conversion & animation process](https://github.com/wikid24/ffxiv_mmd_tools_helper#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow) tutorial
- [frequently asked questions](https://github.com/wikid24/ffxiv_mmd_tools_helper#frequently-asked-questions) below. 


What this tool will NOT do is allow you to import these motions back into the FFXIV game, as this is a full model conversion to the MMD model structure (which is not compatible _within_ the FFXIV game). If you want to do that, please use XAT Tools and follow this [guide](https://docs.google.com/document/d/1siUjAAJjUk7-Nlq11wE-Sldr8UyCeu7SkFJzUsxZpTU/edit)


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
      - working for all races except for Hrothgar (still need to figure out those unique mouth shapes)
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
  - A bunch of important useful stuff. Will list them later.

# To do:
- Better skin/hair/clothing shaders so that the textures don't look so flat in Blender
-  FFXIV Bone Morphs (facial animation sliders):
  - Allow for user to upload their OWN csv file (instead of using the template in this addon)
- Add 'Transform Rigify armature to match ffxiv armature'
- Add presets for skirt/hair for bulk-update to Rigid Bodies (skirts heaviest on the bottom, hair heaviest on the top?)
- Create 'bulk-add joints' with min/max values:
    - Add presets for skirt/hair (skirts heaviest on the bottom, hair heaviest on the top?)
  
------------

# In order to use this tool, you need:
- A FFXIV Model exported into FBX file format - [FFXIV TexTools](https://www.ffxiv-textools.net/) - [Video Tutorial](https://www.youtube.com/watch?v=JbkNt51PRyM) - watch the first 7 minutes
- [Blender](https://www.blender.org/) (2.80+) or higher installed. Only [Blender 3.6 LTS](https://www.blender.org/download/lts/) is _officially_ supported, but it may work on later versions.
- [MMD Tools addon](https://github.com/UuuNyaa/blender_mmd_tools) for Blender
- VMD files (MMD character/camera animation/dance files) - [Deviant Art](https://www.deviantart.com/mmd-dance-comunnity/gallery/36305808/motion-dl), [bowlroll](https://bowlroll.net/),[Reddit](https://www.reddit.com/r/mikumikudance/) or UuuNyaa's Helper addon (listed below)

# Not really needed but recommended:
- The original MMD model that the VMD animation files were based on (useful for animation scaling reasons)
- [UuuNyaa's Helper addon](https://github.com/UuuNyaa/blender_mmd_uuunyaa_tools) to MMD Tools for Blender
- [FIX FFXIV Materials/Textures - Blender Addon](https://drive.google.com/drive/folders/10ashyJJ4HhJqFxDVnGU6s9lyJ0aFHRwa) - [Video Tutorial](https://user-images.githubusercontent.com/19479648/215879548-67bd503e-70b4-4255-abe4-bc1bbcb06618.mp4)
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
- [FFXIV TexTools Hex Color Reference List](https://docs.google.com/spreadsheets/d/18Z1ph1Xa-rFvC8FtB7X6IgSbjwPAom5XuDuCtVeNRvo)
- [MMD Facial Expression Reference guide](https://www.deviantart.com/xoriu/art/MMD-Facial-Expressions-Chart-341504917)
- [XIV Mod Archive - Useful guides to exporting](https://www.xivmodarchive.com/modid/9408) 
- [MMD Skirt Rigging Tutorial: Video Tutorial](https://www.youtube.com/watch?v=cGcBfhYyjC8)
- [UuuNyaa's Physics Adjuster: Video Tutorial](https://www.youtube.com/watch?v=pRJNJDFSYfk)
- [MMD Tools wiki](https://mmd-blender.fandom.com/wiki/MMD_Tools/Manual)
- [XAT Animation Retargeting Guide](https://docs.google.com/document/d/1siUjAAJjUk7-Nlq11wE-Sldr8UyCeu7SkFJzUsxZpTU/edit) - An alternative approach to animating FFXIV characters using MMD motion files
- [FFXIV TexTools Reference Data](https://docs.google.com/spreadsheets/d/1kIKvVsW3fOnVeTi9iZlBDqJo6GWVn6K6BCUIRldEjhw/edit#gid=296196266)

------------

# How to Install

 - Before you install, make sure you have all the [prerequisites installed first](https://github.com/wikid24/ffxiv_mmd_tools_helper#in-order-to-use-this-tool-you-need)
 - Download the [latest release package](https://github.com/wikid24/ffxiv_mmd_tools_helper/releases).zip
 - Go to Edit -> Preferences -> Add-ons -> Install and select the zip file you downloaded

  ![image](https://user-images.githubusercontent.com/19479648/215303847-8a5b34de-b8be-4070-9ab7-dc51ada3fc10.png)
  
 - In the search box, type in 'ffxiv' until the addon 'Object: FFXIV MMD Tools Helper' shows up and check the checkbox

  ![image](https://user-images.githubusercontent.com/19479648/215303990-62fca28b-79b3-4648-b620-d9c6b0f5aa3c.png)

 - Once you see "FFXIV MMD", you'll know it is installed correctly. All of the tools are located here.
  
  ![image](https://user-images.githubusercontent.com/19479648/216140678-1b14644f-8639-472d-99dd-23136001bcc7.png)

--------------

# How to rig a character and get it dancing less than 60 seconds (my new workflow):

## Part 1: Rigging your FFXIV Character using this plugin

On the **FFXIV MMD** tab
1) On the **Import an FFXIV Model** panel, click on  **Import your model FBX File**
2) Click on **Initialize MMD Structure**
3) With your model's bones (read: armature) selected, on the **Language and Translation** panel, click on "**Mass Rename Bones**" (from FFXIV to MMD English)
4) On the **Bones and IK** panel, select "Run steps 1 to 9" -> **Run**

![image](https://user-images.githubusercontent.com/19479648/225116978-fc9d2dbd-c3b4-4d27-b2a2-97929b9d785c.png)

5) On the **Bones and IK** panel, click on **Leg/foot IK**

![image](https://user-images.githubusercontent.com/19479648/225117950-33924dbb-8d9d-4198-8053-fbd744618704.png)


6) Go to **Rigid Bodies** Panel -> Click on **From FFXIV Skeleton (CSV)**
7) Go to **Joints** Panel -> Click on **From FFXIV Skeleton (CSV)**

![image](https://user-images.githubusercontent.com/19479648/225118718-6baf26b6-6b6f-497d-9b08-50c7cfe56458.png)


8) On the **Bone Morphs (Facial Expressions)** Panel, select your model's race and click on **Generate**

![image](https://user-images.githubusercontent.com/19479648/225119028-099a122f-b3aa-4c36-b400-86c108d210c9.png)

9) On the **Export MMD Preparation** Panel -> Click on **Auto-Fix MMD Japanese/English Bone Names**

![image](https://user-images.githubusercontent.com/19479648/225119958-7208b241-9cdc-4753-9aec-9997c717e633.png)


Your character is now rigged and ready for animating using MMD Tools! 

I may suggest saving your Blender file at this point so you can easily switch between different motion files in Part 2 below.

--------------

## Part 2: Animating your FFXIV Character using MMD Tools
 
10) On the Scene Outliner View, click on **New MMD Model**
11) Go to **MMD** tab
12) Under Assembly section click on **All**

![image](https://user-images.githubusercontent.com/19479648/217982914-77067a23-a2ea-47da-99da-ed408d90477b.png)

13) On the Scene Outliner View, click on **n_root**
14) Click on **MMD** tab
15) On the **Scene Setup tab, click on **Motion** -> **Import**

![image](https://user-images.githubusercontent.com/19479648/225124664-93fae3b8-333d-42fc-a6f2-9d236a7643c1.png)

16) Use MMD Tools to import a motion dance VMD file:
    - 'Treat Current Pose as Rest Pose' should be checked

![image](https://user-images.githubusercontent.com/19479648/225125072-ac90a801-1f93-459e-88ce-27d00b4ff651.png)

Your character's **body** will now be animated.

17) On the Scene Outliner View, click on **.placeholder**, and click on **Motion Import** again

![image](https://user-images.githubusercontent.com/19479648/225125745-20c15e22-1201-4f90-b8a1-3af098f26804.png)

18) Use MMD Tools to import a motion dance VMD file:
    - 'Treat Current Pose as Rest Pose' should be checked

![image](https://user-images.githubusercontent.com/19479648/225126409-bc91e8d1-c1da-4632-a6cb-bfb8aa809706.png)

Your character's **face** will now be animated.

19) In the **Scene Setup** panel -> Click on **Rigid Body Physics:** -> **Update World**

![image](https://user-images.githubusercontent.com/19479648/227049123-5c62d250-ece8-4c7f-b11b-de4beb3153f7.png)


20) Press play to watch your character dance. All done!! :D

--------------
# Frequently Asked Questions:

- Animation:
    - [When I play an animation, the arms don't line up __exactly__ to the animation or clip/collide into the head/body/other hand at certain parts. How do I fix this?](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-when-i-play-an-animation-the-arms-dont-line-up-exactly-to-the-animation-or-clipcollide-into-the-headbodyother-hand-at-certain-parts-how-do-i-fix-this)
    - [Why are the leg meshes not following the leg bones? What kind of witchcraft is this??](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-why-are-the-leg-meshes-not-following-the-leg-bones-what-kind-of-witchcraft-is-this)

- Physics:
    - [How do I get better physics working on the skirt? The default one sucks.](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-how-do-i-get-better-physics-working-on-the-skirt-the-default-one-sucks)
    - [My character's skirt isn't complete all around, there are cuts in-between. How do I fix?](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-my-characters-skirt-isnt-complete-all-around-there-are-cuts-in-between-how-do-i-fix)
    - [I am using the new skirt method but I still get clipping on the legs with the skirt. What gives?](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-i-am-using-the-new-skirt-method-but-i-still-get-clipping-on-the-legs-with-the-skirt-what-gives)
    - [Physics is turned on -- Why is my character's skirt/tail going through the floor?](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-physics-is-turned-on----why-is-my-characters-skirttail-going-through-the-floor)
    - [There are other parts of my model that I want to apply physics to. How do I do it?](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-there-are-other-parts-of-my-model-that-i-want-to-apply-physics-to-how-do-i-do-it)
    - [When I start an animation, the model quickly transports to a location and messes up all the physics causing my character's boobs/skirt/hair/tail to warp in weird ways! How to fix?](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-when-i-start-an-animation-the-model-quickly-transports-to-a-location-and-messes-up-all-the-physics-causing-my-characters-boobsskirthairtail-to-warp-in-weird-ways-how-to-fix)

- Other/Miscellaneous:

    - [Can I get rid all these extra bones (other viera ear bones,miquote ears on a non-miqote character, equipment attachment points that are not used, etc.) that my character does not use?](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-can-i-get-rid-all-these-extra-bones-other-viera-ear-bonesmiquote-ears-on-a-non-miqote-character-equipment-attachment-points-that-are-not-used-etc-that-my-character-does-not-use)
    - [Why are the textures all weird and black? They don't look like this in game.](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-why-are-the-textures-all-weird-and-black-they-dont-look-like-this-in-game)
    - [I want to export my model to PMX Format. How do I do that?](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-i-want-to-export-my-model-to-pmx-format-how-do-i-do-that)
    - [My FFXIV chracter's clothing is overlapping! It doesn't look like that in game.](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-my-ffxiv-chracters-clothing-is-overlapping-it-doesnt-look-like-that-in-game)
    - [I want to add new facial expressions or change the existing facial expressions. How?](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-i-want-to-add-new-facial-expressions-or-change-the-existing-facial-expressions-how)
    - [Why does my character's hair have bald patches? HALP!](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-why-does-my-characters-hair-have-bald-patches-halp)


--------------

#### Q: How do I get better physics working on the skirt? The default one sucks.

A: I agree! Physics is hard to get right and implement (and time-consuming). Good news is that this plugin does a lot of the hard work for you (but it can be still time consuming). The first thing I'd recommend is reading the [theory behind how MMD's rigid bodies & joints work in Blender](https://github.com/wikid24/ffxiv_mmd_tools_helper/tree/master/research/physics) so that it doesn't seem so overly confusing.

In the [conversion guide](https://github.com/wikid24/ffxiv_mmd_tools_helper#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow) you'll need to insert some steps _after step 7_. 

Note: Blender tends to crash when there is anything related to physics involved. SAVE OFTEN, especially before you press 'Play' to animate a model.

Using the **Rigid Body** panel, find the all the rigid bodies that start with "j_sk" and delete them.
![image](https://user-images.githubusercontent.com/19479648/225160597-6c1439c0-7cea-4215-8e44-9d0b3d0d4eda.png)

Then'll need to use the **Skirt** panel to generate a new skirt, but there are quite a few steps involved and it's probably the longest part about rigging a FFXIV Model in Blender. 

![image](https://user-images.githubusercontent.com/19479648/225154261-df9eb081-0c3d-4cce-b79e-4281623ebcda.png)

Guide coming soon! In the meantime, here's:
 - [low-quality video to shape the skirt mesh](https://user-images.githubusercontent.com/19479648/225138838-68859c43-a703-40ad-a0f1-c130793d239a.mp4) 
 - [low-quality video to add the rigid bodies and joints](https://user-images.githubusercontent.com/19479648/225158880-eb61221d-6e27-4d5e-a01d-d9cac7253f97.mp4)

I did these a long time ago (the UI looks different and the steps have changed a bit but hopefully it will suffice for now until a _proper_ guide is created). 

Try to line the bones up close to the mesh when generating the skirt (after generating the skirt, you can manually move a bone's location if it's not close enough to the mesh). The skirt bones don't need to __exactly__ be lined up with the mesh but they do need to be __close__ otherwise you risk having clipping issues with the legs going through the skirt unintentionally. Generally speaking, the closer the bones are to the skirt's mesh, the better your rigid bodies will line up with the mesh when they are created, therefore the physics will look better.

Note: When playing an animation, if you are running into issues with legs literally going through the mesh (not the same as small 'clipping') and assuming you lined up the bones to the mesh closely, I find that usually the easiest solution is to _add more bone parents_: 

![image](https://user-images.githubusercontent.com/19479648/225157902-02e4cb80-310f-4fc9-b023-62149c334a72.png)

I've found that adding 20 to 26 bone parents usually fixes the legs going through the skirt.

That being said, try to limit the amount of bones/rigid bodies that are needed for physics, as the more skirt bones that you add, the more physics calculations Blender has to do in order to animate the rigid bodies, so it will slow down your PC when trying to animate the physics in real-time.

After you're finished with tweaking the physics settings, you can bake the physics into the animation (using MMD Tools) so that Blender does not need to calculate the physics any more. Since baking the physics into an animation is a time-comsuming process, I generally only bake my physics in once I'm happy with the results of my tweaking and I'm close to the rendering an output file out of Blender.


--------------
#### Q: My character's skirt isn't complete all around, there are cuts in-between. How do I fix?

![image](https://user-images.githubusercontent.com/19479648/225166631-1f0c6b8d-d39a-4c33-8200-ae7da07fd0ee.png)

A: You may run into skirts like this that are not perfectly round, or are split into many pieces. 

There are a few ways to fix:
- Delete skirt bones (before generating the rigid bodies)
- Delete the rigid bodies (before generating the joints)
- Delete the horizontal joints

Or you can use a combination of all three.

In this example we delete the **horizontal joints** that are connecting the rigid bodies together. 

Note: Whenever you need to change __anything__ related to adding or removing bones/rigid bodies/joints, **make sure Physics is turned OFF** in MMD Tools (or use this shortcut), otherwise you risk breaking your model:

![image](https://user-images.githubusercontent.com/19479648/225162913-e236ad64-3375-486b-8853-9dec7c2b8569.png)


Using the **Rigid Body** panel shift+select (or control+select) the rigid bodies that you need to remove the joints from. These tools will help you make it easy to select what you need to:

![image](https://user-images.githubusercontent.com/19479648/225162948-3a4a2d60-7a28-4ce4-8d79-65d0b5bff4fc.png)

Then go to the **Joints** panel and click on 'Get Joints from Rigid Bodies', then click on 'Horizontal' to filter ONLY horizontal joints.

![image](https://user-images.githubusercontent.com/19479648/225163385-7eda5e1a-2f67-4a6f-b22b-7d61a2b59b97.png)

With the joints you want selected, you should now be able to delete them.

After you're finished making your modifications, SAVE your .blend file(just incase Blender crashes), turn physics ON again, and press play to see if it made a difference. If not, UNDO you steps, or turn Physics off again and play with the model until you get your desired results. 

--------------
#### Q: I am using the new skirt method but I still get clipping on the legs with the skirt. What gives?

A: Assuming you did all the steps correctly and the rigid bodies are lined up correctly with their respective meshes, the last available option is to increase the width/length on the skirt's rigid bodies OR increase the width of the leg rigid bodies. Or both. This can be done using the rigid body transform 'Bulk Apply', 'Bone Chain', or 'All Bone Chains' tools.


- **Bulk Apply** will apply the the rigid body's settings you change EXACTLY the same for all selected rigids.

- **Bone Chain** and **All Bone Chains** will apply a 'gradient' so of the selected rigid bodies, the highest bone parent's rigid body  will get that (starting) value, and lowest bone child's rigid body will get that (ending) value.

Perhaps maybe a visual explanation is better for the differences between each tool:

https://user-images.githubusercontent.com/19479648/225210461-c10581d3-ff3d-4fb8-92d8-1bed41de3dac.mp4


You can see on [Sample Video 1](https://github.com/wikid24/ffxiv_mmd_tools_helper#sample-video-1-thancred--sadu---skirt-physics-testing) that there is clipping on Thancred's legs through the skirt (I did leave this in the video intentionally). This is because the Rigid bodies with the skirt are colliding with the rigid bodies on the legs, unfortunately because the leg's rigid bodies are smaller than the leg's mesh, it is causing clipping to occurr.

In this example below, increase the rigid body width/radius/size until it is __slightly__ larger than mesh using these tools (I'd use the 'Bulk Apply' tool in this specific example):
![image](https://user-images.githubusercontent.com/19479648/225213419-a2e040ad-0db0-415f-bf95-663411398a9d.png)


--------------

#### Q: Can I get rid all these extra bones (other viera ear bones,miquote ears on a non-miqote character, equipment attachment points that are not used, etc.) that my character does not use?

A: Yes you can get rid of them! In the **Miscellaneous Tools** panel, run these two commands:
- Flag unused bones as '_unused_'
- Delete 'unused' bones

![image](https://user-images.githubusercontent.com/19479648/225139856-80f9efc0-5ec6-455a-8be0-aef79c5da27a.png)

In general it is safer to run this step immediately after Step 1 in the [conversion guide](https://github.com/wikid24/ffxiv_mmd_tools_helper#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow) (before starting to manipulate all the bones on the model).

--------------

#### Q: When I play an animation, the arms don't line up __exactly__ to the animation or clip/collide into the head/body/other hand at certain parts. How do I fix this?

A: The FFXIV bone structure isn't _exactly_ lined up with a standard MMD model's A-Pose (the 'rest pose'). In general, FFXIV shoulders / arms / forearms / wrists are longer than a regular MMD model and it requires changes to the FFXIV bone structure. I've implemented an 'experimental' feature that adjusts the shoulder / arm / forearm / wrists positions. You'd need to run this step immediately after step 4 in the [conversion guide](https://github.com/wikid24/ffxiv_mmd_tools_helper#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow): 

![image](https://user-images.githubusercontent.com/19479648/225142650-e640c4f8-96a3-48fc-bda8-10f5d1bac701.png)

Note: This is an **experimental** feature so it's not guaranteed to work exactly, as I haven't found a proper solution yet, but it does seem to work better in some cases then others. For example, on one MMD animation it ended up twisting the bone arm in a weird way, but on another animation it fixed all my hand/arm clipping issues, so your mileage may vary.

--------------

#### Q: Why are the textures all weird and black? They don't look like this in game.

![image](https://user-images.githubusercontent.com/19479648/225144053-a6132eb8-7dd1-4aa5-b2a1-1fd0eb1cb6ef.png)

A: Textools unfortunately doesn't export ALL of the texture files needed to render some textures properly for some gear (like dyed gear or metallic gear).

Using Textools, you'd need to individually export each affected body part's normal/multi/colorset texture(read: DDS files) and use this [Blender Plugin ](https://drive.google.com/drive/folders/10ashyJJ4HhJqFxDVnGU6s9lyJ0aFHRwa) & [video guide](https://user-images.githubusercontent.com/19479648/215879548-67bd503e-70b4-4255-abe4-bc1bbcb06618.mp4) to fix it. 

You'll need to perform this immediately after step 1 in the [conversion guide](https://github.com/wikid24/ffxiv_mmd_tools_helper#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow). On step 2, __uncheck__ this box: ![image](https://user-images.githubusercontent.com/19479648/225148216-89bd0dbc-dc54-47b8-b074-47a24ec352ce.png)
 
 --------------
 
#### Q: I want to export my model to PMX Format. How do I do that?

A: Everything that is needed to export to PMX format is included in this plugin. 

Immediately after step 4 on the [conversion guide](https://github.com/wikid24/ffxiv_mmd_tools_helper#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow), run this command:

![image](https://user-images.githubusercontent.com/19479648/225155767-6f97c683-edb0-44e3-b17a-9cb35eba3293.png)

Next, after step 9 in the [conversion guide](https://github.com/wikid24/ffxiv_mmd_tools_helper#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow), follow these steps:

1) On the **Export MMD Preparation** Panel -> Click on **Add Display Panels** 

![image](https://user-images.githubusercontent.com/19479648/225148500-8c5ea5dd-f838-4366-a0f1-1da9d626016d.png)

2) On the MMD Tools Plugin -> **Bone Order** Panel -> Click on that weird square shape on the bottom
3) Click on the arrow to expand the menu
4) Click on **Add Missing Vertex Groups from Bones**

![image](https://user-images.githubusercontent.com/19479648/225152213-4dffae74-5e2e-4de6-b992-a9baec4066af.png)

5) Back in FFXIV MMD Tools Plugin, click on all of these buttons

![image](https://user-images.githubusercontent.com/19479648/225152849-f2339f03-ca85-477b-803d-f2144f880f19.png)

6) On the MMD Tools Plugin -> click on **Model** -> **Export**

![image](https://user-images.githubusercontent.com/19479648/225153368-5a104ea7-58f5-47de-b95a-c70e34b69648.png)

The character should now be fully rigged and exported into PMX Format. From here you can treat this file exactly as a normal MMD Model and import it directly into MMD program OR edit it using PMX Editor.

 --------------
 
#### Q: My FFXIV chracter's clothing is overlapping! It doesn't look like that in game.

![image](https://user-images.githubusercontent.com/19479648/225433632-36181fc9-38a3-4062-b17b-c4ed376b3cdd.png)

A: This is because FFXIV uses a system of cutting clothes into smaller pieces, then it uses special shape keys to adjust the size for the remaining pieces. 

For example a glove may go all the way up to the biceps, while the chest gear may go all the way up to the wrist. This can be fixed by deleting the extra chest clothing pieces, then leveraging the built-in shape keys to adjust the remaining clothes' size.

To fix this, we need to go into **MMD Tools** -> **Morph Tools** -> **Vertex** tab, and play with the shape key sliders that show up in this section setting the values from 0 to 1. 

I play with these sliders and set the values to 1 until I find a slider that fixes my clothing issue.

To fix any FFXIV clothing, the value should either be 0 or 1 (nothing in-between).

![image](https://user-images.githubusercontent.com/19479648/225436534-171ea31a-a913-41ea-96ce-fd56559678c3.png)


In this example, setting this particular slider to 1 (shp_kat) fixed my issue. 

Please note you may have MULTIPLE sliders under this section that need to be set to 1. 

![image](https://user-images.githubusercontent.com/19479648/225436383-ca1699a1-e277-4cbb-b6db-3b14ea5a9f88.png)

An alternate way is by going into each individual mesh and using Blender's Shape Key panel, but personally I find it easier to do this using MMD Tools since MMD Tools groups all the meshes for your model's shape keys together under one easy-to-use panel:

![image](https://user-images.githubusercontent.com/19479648/225437354-02209e0b-1afd-40c5-8ef2-441b6b59950c.png)

 --------------
 
#### Q: There are other parts of my model that I want to apply physics to. How do I do it?

A: There are a few ways to do it, and depending on the method some are easier than others. 

For breast physics, I would recommend using [UuuNyaa's Plugin](https://www.youtube.com/watch?v=f9LA6_XnFIg) as it is very easy to use. But only if you are staying in Blender as this will not work if you want to export to PMX format.

I will go over an example of how to manually add physics using the MMD method using Bones,Rigid Bodies and Joints, as this method will work if you want to export to PMX format. The first thing I'd recommend is reading the [theory behind how MMD's rigid bodies & joints work in Blender](https://github.com/wikid24/ffxiv_mmd_tools_helper/tree/master/research/physics) so that it doesn't seem so overly confusing.

In general these are the high-level steps required:
1) Create the Bones you would like to apply physics to
2) Weight paint the bones for the mesh
3) Create the rigid bodies and configure the rigid body parameters
4) Create the joints between the rigid bodies and configure the joint parameters
5) Create a joint to attach the rigid body stem to a 'collision-based' rigid body so it stays attached to your model's skeleton

You would want to do this _after step 7_ on the [Conversion Guide](https://github.com/wikid24/ffxiv_mmd_tools_helper#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow)

In this example we will go over creating physics for a FFXIV model's hair pony tails, we will use this Au Ra model found in [Sample Video 3](https://github.com/wikid24/ffxiv_mmd_tools_helper#sample-video-3-random-wol---manually-created-hair-physics-testing).

First thing I will say is make sure **Physics is turned OFF** whenever you are changing/adding bones/rigid bodies/joints on anything related to physics. Once you are done making changes, SAVE OFTEN (as Blender likes to crash a lot whenever Physics are involved) and then you can turn Physics ON again.

#### Part 1: Create the Bones you would like to apply physics to

With the Au Ra model, find the hair mesh you would like to change. There should already be some bones attached that are weight painted on it. If your model does not have an existing bone to use on the place you would like add physics, create one from where you would like the physics to **start** on the mesh.

![image](https://user-images.githubusercontent.com/19479648/225772659-c7486053-88e2-4660-9e15-02591a0bb2d3.png)

Next, we will extrude some bones from the existing bone that will match the shape of the mesh. Go to 'edit' mode for the bones. If you are lucky and there are bones on both side of your model (left and right, the bone names should end with 'l' and 'r'), you can use the 'X Axis Mirror' to cut the amount of work in half. Select the **tail**  of the bone (ONLY the tail, not the entire bone) and press 'E' to extrude. You can manipulate the bone tail position by selecting it and pressing 'G' on the tail.  

![image](https://user-images.githubusercontent.com/19479648/225773313-860dc1f3-038d-4af7-88ab-10c4149e1d8a.png)

Repeat this process for however many bones you would like the hair physics to have, until you are finished. The more bones you add, the more detailed the physics will look. But I am lazy, so I only add a few bones :)

![image](https://user-images.githubusercontent.com/19479648/225773672-34ff8d19-5276-43e2-85f3-f39ec7234eb7.png)

#### Part 2: Weight paint the bones for the mesh

Next we will apply weight painting to all the bones. Go to 'object' mode and select the armature, then control+click on the mesh. Then go to 'weight-painting' mode. 

![image](https://user-images.githubusercontent.com/19479648/225773985-8ad42e64-1bf9-4e45-8347-637a30f095b0.png)

Shift + Click on all the bones that need weight painting, then go to the menu option that says Weights -> Assign Automatic from Bones

![image](https://user-images.githubusercontent.com/19479648/225774216-61f38aa6-3b5c-4354-a4d1-ff037948e3f3.png)

The hair should now be weight painted. You can check if they are weight painted correctly by control+clicking on a bone and seeing if the weight paint is applied properly in all the correct areas. If not, you will have to manually fix the weight paint (Don't ask me how, there are lots of videos on the internet and it is a tedious process). 

#### Part 3: Create the rigid bodies and configure the rigid body parameters

Now that we have weight painted the bones, we will create the rigid bodies. Go back to 'object' mode, then select the armature and go to 'edit' mode. Control+click on all of the hair bones so they are all selected that you would like to apply physics to. In the FFXIV MMD Tools -> Rigid Bodies panel, select Create: **From Selected Bones**.

![image](https://user-images.githubusercontent.com/19479648/225774808-187ea52d-2bf1-4036-a653-f60b03cb2849.png)

Configure the shape of the rigid bodies, as well as the parameters.

For this particular example I selected:
- Rigid Body Shape: Capsule
- Make sure the collision group is a different from than the skeletion (I used '9' because I know it's currently not used by any other rigid body groups)
- Make sure the collision group mask is selected to **ignore itself** (I set the collision group mask to ignore all rigid bodies from group 9)
- Make sure the rigid body type is 'Physics'

Here is the menu options that I used:

![image](https://user-images.githubusercontent.com/19479648/225783387-d7f527b9-41a8-4387-bae2-73733136c99d.png)

![image](https://user-images.githubusercontent.com/19479648/225775248-c6968387-75cd-4da1-b66b-f8c190cc667e.png)

Your rigid bodies should now be configured. You can always change the settings later using the 'Bulk Apply'/'Bone Chain'/'All Bone Chain' options in the FFXIV MMD Tools Rigid Bodies panel.

#### Part 4: Create the joints between the rigid bodies and configure the joint parameters

Next we will create joints between the rigid bodies. With the rigid bodies selected, go to the Joints panel and select Create: **From Selected Rigid Bodies**. 

![image](https://user-images.githubusercontent.com/19479648/225775565-c70af677-97b7-4d00-921c-98ddae89b0e4.png)

You can configure always the settings later using 'Get Joints from Rigid Bodies' and 'Bulk Apply' on the Joints panel.

![image](https://user-images.githubusercontent.com/19479648/225776232-8848acd5-877b-4e59-9266-dcd647516ad1.png)


#### Part 5: Create a joint to attach the rigid body stem to a 'collision-based' rigid body so it stays attached to your model's skeleton

Last thing to do is attach the hair stem rigid bodies to the head rigid body. Control + Click on the hair stem and the 'head' rigid body. Then click on Create: ** From Selected Rigid Bodies **

![image](https://user-images.githubusercontent.com/19479648/225776867-8598f660-e5ab-4c73-804e-7a876f1aebee.png)

You're all done! Turn Physics ON and Press Play to see if everything is working as expected. If not, Turn Physics OFF, make your changes and then turn it on again.


 --------------
 
#### Q: I want to add new facial expressions or change the existing facial expressions. How?

A: First thing I would recommend doing is looking at this [MMD Facial Expression Reference guide](https://www.deviantart.com/xoriu/art/MMD-Facial-Expressions-Chart-341504917) as these are the reference charts I used when creating MMD facial expressions. 

The facial expressions I created for FFXIV characters were fine-tuned manually (it doesn't use any data from Square Enix) so there is always room for improvement!

Ok, so before getting into the how to change facial expressions, I need to go into some theory discussion on how Facial Expressions work in Blender's MMD Tools.

Vertex Morphs (shape keys) vs Bone Morphs:
- **Shape keys** are a Blender concept are used for controlling a **mesh's verticies**
- MMD Facial animations are animated using shape keys (or 'Vertex Morphs' as MMD Tools calls them) under the **.placeholder** object in Blender
- When you animate facial expressions in Blender, those shape keys have special names in Japanese that are used by VMD/MMD motion files for animation.
- 'Vertex Morphs' manipulate a mesh's verticies, while 'Bone Morphs' manipulate multiple pose bone's transform data.
- **Bone Morphs** is an __intermediary__ step to creating shape keys. It allows someone in Blender to manipulate a pose bone's location & rotation data. When you press this 'Morph' button in MMD Tools, those Bone Morphs are then copied and converted into shape keys that are stored in the **.placeholder** object:

![image](https://user-images.githubusercontent.com/19479648/225810013-18549aab-72e8-4ca4-b21b-ace79b3f79de.png)

- A bone morph is simply a way of storing multiple pose bone location/rotation data in a collection.
- For example, the 'left wink' bone morph-- It is a collection of two pose bones, the 'left upper eyelid' and 'left lower eyelid' being rotated on the Z axis from the rest position. 
- Bone Morphs can always be converted into shape keys, but it is impossible to convert a shape key back into a bone morph... Meaning, if you want to modify a shape key, you're stuck manually modifying the verticies of a mesh at that point.
- I heavily leverage the Bone Morphs. It only works because I have an assumption that _all models within the same races_ have similar face shapes. For example, I assume that all lalafell have all the same massive eye sockets, and all roegadyn have tiny eye sockets. As a general rule it seems to work well enough.

The bone morph data for each race is stored in a CSV File that contains a few columns of data:
- Bone Morph Name
- Pose bone Name
- Location/rotation changes for each pose bone in XYZ Euler format ( *not* in 'Quaternion' because 'Quaternion' sucks :) )

It is easy enough to read and access the data if you have Excel by pressing on this button:

![image](https://user-images.githubusercontent.com/19479648/225806409-b93c9b43-925a-41ef-8ebd-c161952c4f31.png)

You can also see these exact same numbers used in MMD Tools if you:
1) Change the pose bone facial data to XYZ Euler using this button:

![image](https://user-images.githubusercontent.com/19479648/225806550-ded22bc0-1739-42a0-a568-d776f53e5a12.png)

2) Go into MMD Tools, and check the Bone Morphs section:

![image](https://user-images.githubusercontent.com/19479648/225807185-9bea83a0-a69a-40ec-b825-0b6968081aec.png)


That being said, if you wanted to add or change the bone morph data, There are a few ways to do it:
1) You can always modify these files, save it, and then press the 'Generate' button
2) Manually do it via MMD Tools using the tools they provide:

![image](https://user-images.githubusercontent.com/19479648/225808326-f5603e0c-aba6-4af5-a37f-e7d72065cd82.png)

![image](https://user-images.githubusercontent.com/19479648/225808828-b92bd39a-738e-4e10-9da4-8684b06bffbe.png)


 --------------
 
#### Q: When I start an animation, the model quickly transports to a location and messes up all the physics causing my character's boobs/skirt/hair/tail to warp in weird ways! How to fix?

A: When physics are applied to any animations in blender, the time that it takes to move from one frame to the next frame is important. A lot of VMD motion animation files start by transporting a charater to a specified spot _very quickly_. This is controlled by the 'margin' setting when importing an animation. 

![image](https://user-images.githubusercontent.com/19479648/227057740-437cae34-eef4-48c9-8307-65142d0cd10d.png)

By default the margin will be set to '5'. Margin is the starting MMD animation frame offset from frame 0. Meaning, if frame 0 is the 'rest' position for your model, and 5 is the MMD animation 'start' frame, this gives Blender exactly 5 frames to move a model, and transport the physics along with it... Which causes physics to warp your model in weird ways.

To fix this, upon importing a VMD motion file, set the margin to '30' or higher. Using multiples of **30** are ideal, as all VMD animations (well, all the keyframes anyway) are animated at 30 fps. What this will do is give Blender more time to 'safely' move a model with physics on so that they can settle easily before the VMD animation starts on frame 30. 

And if you're using a multiple of 30 it is easy to tell that the MMD animation starts on a specific second. For example if I set the margin to 120, and I render out a video at 30 fps, I can easily tell that I need to sync the music to the video on the 4 second mark.

--------------
 
#### Q: Why are the leg meshes not following the leg bones? What kind of witchcraft is this??

![image](https://user-images.githubusercontent.com/19479648/227060435-01edd03b-e899-4b10-a80c-dbacea463786.png)


A: There are certain 'special' bones that were invented due to how Inverse Kinematics work in MMD. Inverse Kinematics are great as they allow you to animate a whole leg by using a single 'controller' IK bone, but once you apply them, it means you can no longer physically move the 'controlled' bones (and therefore the mesh) _directly_ anymore. 

Someone in the MMD world invented these 'special' bones that allows you to move a mesh _even after_ IK was applied to the bones. This is so that if IK is not achieving the desired leg movement, you can always apply a slight nudge here or there in the right direction by adjusting these special bones.

These bones (at least, in this plugin) are called:
- waist_cancel_l
- waist_cancel_r
- leg_l_D
- leg_r_D
- knee_l_D
- knee_r_D
- knee_2_l_D
- knee_2_r_D
- toe_l_EX
- toe_r_EX

The problem is that sometimes these special bones tend to cause more issues on some VMD motion files than others. I've found (in at least two VMD motion files) that the culprit was **waist_cancel_l** and **waist_cancel_r**. To adjust these, you can turn down the 'influence' of these special bones to the mesh or turn it off completely. 

To do this, Select the Armature, go to 'pose' mode, then find the bones special bones you want to adjust (for this example we are using **waist_cancel_l** and **waist_cancel_r**) bones. Select the bone, go to 'bone constraints' and turn the 'Influence' down to 0.

![image](https://user-images.githubusercontent.com/19479648/227062268-e26b18f3-49bd-4fd9-8342-63ded2d51df8.png)

All fixed :)


--------------
 
#### Q: Physics is turned on -- Why is my character's skirt/tail going through the floor?

![image](https://user-images.githubusercontent.com/19479648/227067679-e5f976fb-c78b-4faa-98a5-717759900b46.png)


A: The first thing I'd recommend is reading the [theory behind how MMD's rigid bodies & joints work in Blender](https://github.com/wikid24/ffxiv_mmd_tools_helper/tree/master/research/physics) so that it doesn't seem so overly confusing. 

Done reading? Ok. So you have 'collision-based' rigid bodies, and 'physics-based' rigid bodies. All of the skirt/tail rigid bodies are 'physics-based'. The issue is that they have nothing to collide _into_. Right now, the tail rigids pass right through our imaginary floor. 

To fix this, we need to create a 'collision-based' rigid body that simulates an actual floor for the 'physics-based' rigid bodies to interact with. 

The best bone to use to simulate a floor is the 'root' bone, since it naturally should be directly below your model at all times, and also it's already on the xyz 0,0,0 point so we don't need to move it around anywhere. 

Anyway, the steps:
1) Turn Physics OFF.
2) Go to 'edit' mode, then select the 'root' bone. 
3) Click on **Rigid Body Create** -> **From Selected Bones**

![image](https://user-images.githubusercontent.com/19479648/227069077-8e0e5af3-56e5-41bb-ac61-9ca2c8684319.png)

4) On the rigid body settings, change the Shape to 'Box'

![image](https://user-images.githubusercontent.com/19479648/227069556-4c3eb09b-2e78-4356-b84d-c6dba9b9998c.png)

5) With the Rigid Body selected, Under **Rigid Body Transform** -> Select **Bulk Apply**
6) Change the following settings and press 'OK':
  - Location Z to 0
  - Size Z to 0
  - Size Y and X to anything you want, as long as it's below your model at all times

![image](https://user-images.githubusercontent.com/19479648/227070532-354f0073-583c-407c-ae8b-da74bbe39836.png)


If done properly, should now have something that looks like this:

![image](https://user-images.githubusercontent.com/19479648/227070606-6c3501ff-9fd3-4785-a741-530fca1ed728.png)


You're all done. Now Turn Physics ON again and observe that your physics-based rigid bodies will no longer pass through the imaginary floor (as it has a real collision-based rigid body to interact with now).

![image](https://user-images.githubusercontent.com/19479648/227070959-1899e16c-0f1f-4476-84b1-9cbc94415eec.png)

If you notice any weird issues such as the floor being too 'sticky' when the tail or skirt collide with it, you can try setting the 'friction' parameter to 0 on the floor rigid body to see if that changes anything.

![image](https://user-images.githubusercontent.com/19479648/227071122-a991e50d-8867-4985-91a9-35c5003c573e.png)

--------------

#### Q: Why does my characters hair have bald patches! HALP!

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/df35e420-2163-47cf-ab30-a2a4c45e38ce)

A: This is because Blender is using the wrong UV Map. To fix:

1) Go the the "Shading" tab in blender
2) While in "Object" mode, select the hair material with the bald patches in the viewport
3) Add a "UV Map" node

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/d2cb3643-7268-445b-8eb0-4f8dc6a0ed20)

4) You should see a node with the name "Diffuse" on it. Connect the UV Map node's "UV" output to the Diffuse node's "Vector" input
5) Set the UV Map node's dropdown to "uv2"

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/f4ff66a8-b091-4d66-8e0a-31afe6b589f3)


All fixed!

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/6b3fa76b-338f-443c-a3f3-16b7cbaa81c8)

