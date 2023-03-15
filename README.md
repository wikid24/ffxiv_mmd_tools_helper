# FFXIV MMD Tools Helper
## This is a fork of Hogarth-MMD's [mmd_tools_helper](https://github.com/Hogarth-MMD/mmd_tools_helper), massively updated to be compatible with FFXIV Models and Blender 2.8+. It's a work in progress.

Purpose of this tool is for EVERYONE in FFXIV to start exporting their favorite FFXIV characters to MMD so we can all make memes of dancing and music videos with as little effort as possible. Once I get this tool out of alpha, detailed tutorials on how to export FFXIV characters to MMD will come. 

For now, [download here](https://github.com/wikid24/ffxiv_mmd_tools_helper/releases), check the [install guide](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/README.md#how-to-install), simple [60 second conversion](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/README.md#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow) tutorial, and the [frequently asked questions](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/README.md#frequently-asked-questions) below. 

If you have questions you can find me (wikid24) in Discord on [XIV Tools](https://discord.gg/xivtools) mostly active in  #xat-discussion channel.

------------
While this tool is geared towards FFXIV model conversion, the majority of it's features can be used for conversion for any MMD models.

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
  - A bunch of important useful stuff. Will list them later.

# To-Do Conversion/upgrade to Blender 2.8+ (from original Hogarth-MMD plugin):
  - mmd_lamp_setup.py
  - mmd_view.py
  - toon_textures_to_node_editor_shader.py (it works, sort of... I need to understand shaders more)

# To do:
- Auto generate Shape Keys (as opposed to using Bone Morphs) from csv
- FFXIV Bone Morphs (facial animation sliders):
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
- [Blender](https://www.blender.org/) (2.80+) or higher installed. Only [Blender 3.3 LTS](https://www.blender.org/download/lts/) is _officially_ supported, but it may work on later versions.
- [MMD Tools addon](https://github.com/UuuNyaa/blender_mmd_tools) for Blender
- VMD files (MMD character/camera animation/dance files) - [Deviant Art](https://www.deviantart.com/mmd-dance-comunnity/gallery/36305808/motion-dl), [bowlroll](https://bowlroll.net/),[Reddit](https://www.reddit.com/r/mikumikudance/) or UuuNyaa's Helper addon (listed below)

# Not really needed but recommended:
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
3) On the **Language and Translation** panel, click on "**Mass Rename Bones**" (from FFXIV to MMD English)
4) On the **Bones and IK** panel, select "Run steps 1 to 9" -> **Run**

![image](https://user-images.githubusercontent.com/19479648/225116978-fc9d2dbd-c3b4-4d27-b2a2-97929b9d785c.png)

5) On the **Bones and IK** panel, click on **Leg/foot IK**

![image](https://user-images.githubusercontent.com/19479648/225117950-33924dbb-8d9d-4198-8053-fbd744618704.png)


6) With your model selected, go to **Rigid Bodies** Panel -> Click on **From FFXIV Skeleton (CSV)**
7) With your model selected, go to **Joints** Panel -> Click on **From FFXIV Skeleton (CSV)**

![image](https://user-images.githubusercontent.com/19479648/225118718-6baf26b6-6b6f-497d-9b08-50c7cfe56458.png)


8) On the **Bone Morphs (Facial Expressions)** Panel, select your model's race and click on **Generate**

![image](https://user-images.githubusercontent.com/19479648/225119028-099a122f-b3aa-4c36-b400-86c108d210c9.png)

9) On the **Export MMD Preparation** Panel -> Click on **Auto-Fix MMD Japanese/English Bone Names**

![image](https://user-images.githubusercontent.com/19479648/225119958-7208b241-9cdc-4753-9aec-9997c717e633.png)


Your character is now rigged and ready for animating using MMD Tools!

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

19) Press play to watch your character dance. All done!! :D

--------------
# Frequently Asked Questions:
#### Q: How do I get better physics working on the skirt? The default one sucks.

A: I agree! Physics is hard to get right and implement (and time-consuming). Good news is that this plugin does a lot of the hard work for you (but it can be still time consuming). The first thing I'd recommend is reading the [theory behind how MMD's rigid bodies & joints work in Blender](https://github.com/wikid24/ffxiv_mmd_tools_helper/tree/master/research/physics) so that it doesn't seem so overly confusing.

In the [conversion guide](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/README.md#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow) you'll need to insert some steps _after step 7_. 

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

Note: When playing an animation, if you are running into issues with legs clipping (assuming you lined up the bones to the mesh closely), I find that usually the easiest solution is to _add more bone parents_: 

![image](https://user-images.githubusercontent.com/19479648/225157902-02e4cb80-310f-4fc9-b023-62149c334a72.png)

I've found the adding 20 to 26 bone parents usually fixes the legs going through the skirt.

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

In this example we will to delete the **horizontal joints** that are connecting the rigid bodies together. 

Note: Whenever you need to change __anything__ related to adding or removing bones/rigid bodies/joints, **make sure Physics is turn OFF** in MMD Tools (or use this shortcut), otherwise you risk breaking your model:

![image](https://user-images.githubusercontent.com/19479648/225162913-e236ad64-3375-486b-8853-9dec7c2b8569.png)


Using the **Rigid Body** panel shift+select (or control+select) the rigid bodies that you need to remove. These tools will help you make it easy to select what you need to:

![image](https://user-images.githubusercontent.com/19479648/225162948-3a4a2d60-7a28-4ce4-8d79-65d0b5bff4fc.png)

Then go to the **Joints** panel and click on 'Get Joints from Rigid Bodies', then click on 'Horizontal' to filter ONLY horizontal joints.

![image](https://user-images.githubusercontent.com/19479648/225163385-7eda5e1a-2f67-4a6f-b22b-7d61a2b59b97.png)

With the joints you want selected you should now be able to delete them.

After you're finished making your modifications, SAVE your .blend file(just incase Blender crashes), turn physics ON again, and press play to see if it made a difference. If not, UNDO you steps, or turn Physics off again and play with the model until you get your desired results. 

--------------

#### Q: Can I get rid all these extra bones (other viera ear bones,miquote ears on a non-miqote character, unused bones that are not used by your gear, etc) that my character does not use?

A: Yes you can get rid of them! In the **Miscellaneous Tools** panel, run these two commands:
- Flag unused bones as '_unused_'
- Delete 'unused' bones

![image](https://user-images.githubusercontent.com/19479648/225139856-80f9efc0-5ec6-455a-8be0-aef79c5da27a.png)

In general it is safer to run this step immediately after Step 1 in the [conversion guide](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/README.md#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow) (before starting to manipulate all the bones on the model).

--------------

#### Q: When I run the an animation, the arms don't line up __exactly__ to the animation or clip/collide into the head/body/other hand at certain parts. How do I fix this?

A: The FFXIV bone structure isn't _exactly_ lined up with a standard MMD model's A-Pose (the 'rest pose'). In general, FFXIV shoulders / arms / forearms / wrists are longer than a regular MMD model and it requires changes to the FFXIV bone structure. I've implemented an 'experimental' feature that adjusts the shoulder / arm / forearm / wrists positions. You'd need to run this step immediately after step 4 in the [conversion guide](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/README.md#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow): 

![image](https://user-images.githubusercontent.com/19479648/225142650-e640c4f8-96a3-48fc-bda8-10f5d1bac701.png)

Note: This is an **experimental** feature so it's not guaranteed to work exactly, as I haven't found a proper solution yet, but it does seem to work better in some cases then others.For example, on one MMD animation it ended up twisting the bone arm in a weird way, but on another animation it fixed all my hand/arm clipping issues, so your mileage may vary.

--------------

#### Q: Why are the textures all weird and black? They don't look like this in game.

![image](https://user-images.githubusercontent.com/19479648/225144053-a6132eb8-7dd1-4aa5-b2a1-1fd0eb1cb6ef.png)

A: Textools unfortunately doesn't export ALL of the texture files needed to render some textures properly for some gear (like dyed gear or metallic gear).

Using Textools you'd need to individually export each affected body part's normal/multi/colorset texture(read:DDS files) and use this [Blender Plugin ](https://drive.google.com/drive/folders/10ashyJJ4HhJqFxDVnGU6s9lyJ0aFHRwa) & [video guide](https://user-images.githubusercontent.com/19479648/215879548-67bd503e-70b4-4255-abe4-bc1bbcb06618.mp4) to fix it. 

You'll need to perform this immediately after step 1 in the [conversion guide](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/README.md#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow). On step 2, __uncheck__ this box: ![image](https://user-images.githubusercontent.com/19479648/225148216-89bd0dbc-dc54-47b8-b074-47a24ec352ce.png)
 
 --------------
 
#### Q: I want to export my model to PMX Format. How do I do that?

A: Everything that is needed to export to PMX format is included in this plugin. 

Immediately after step 4 on the [conversion guide](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/README.md#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow), run this command:

![image](https://user-images.githubusercontent.com/19479648/225155767-6f97c683-edb0-44e3-b17a-9cb35eba3293.png)

After step 9 in the [conversion guide](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/README.md#how-to-rig-a-character-and-get-it-dancing-less-than-60-seconds-my-new-workflow), then follow these steps:

1) On the **Export MMD Preparation** Panel -> Click on **Add Display Panels** 

![image](https://user-images.githubusercontent.com/19479648/225148500-8c5ea5dd-f838-4366-a0f1-1da9d626016d.png)

2) On the MMD Tools Plugin -> **Bone Order** Panel -> Click on that weird square shape on the bottom
3) Click on the arrow to expand the menu
4) Click on **Add Missing Vertex Groups from Bones**

![image](https://user-images.githubusercontent.com/19479648/225152213-4dffae74-5e2e-4de6-b992-a9baec4066af.png)

5) Back in FFXIV MMD Tools Plugin, Click on all of these buttons

![image](https://user-images.githubusercontent.com/19479648/225152849-f2339f03-ca85-477b-803d-f2144f880f19.png)

6) On the MMD Tools Plugin -> Click on **Model** -> **Export**

![image](https://user-images.githubusercontent.com/19479648/225153368-5a104ea7-58f5-47de-b95a-c70e34b69648.png)

The character should now be fully rigged and exported into PMX Format. From here you can treat this file exactly as a normal MMD Model and import it directly into MMD program OR edit it using PMX Editor.
