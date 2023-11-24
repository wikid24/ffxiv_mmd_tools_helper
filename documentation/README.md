# 3D Viewport -> Sidebar

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/51578364-bbaf-4ac3-84ad-679b9f87a4d5)

Sections:
- [Import FFXIV Model](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#import-ffxiv-model)
- [Language and Translation](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#language-and-translation)
- [Bones and IK](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#bones-and-ik)
- [Rigid Bodies](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#rigid-bodies)
- [Joints](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#joints)
- [Bone Morphs (Facial Expressions)](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#bone-morphs-facial-expressions)
- [Skirt](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#skirt)
- [Shaders](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#shaders)
- [Decals / Face Paint](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#decals--face-paint)
- [Miscellaneous Tools](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#miscellaneous-tools)
- [Export MMD Preparation](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#export-mmd-preparation)

------

## Import FFXIV Model

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/79655313-f5e6-4415-97b8-de19a6b7650d)

Sections:
- [Import FFXIV .fbx File](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#import-ffxiv-fbx-file)
- [Load Sample](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#load-sample)
- [Initialize MMD Struture](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#initialize-mmd-struture)
- [TexTools 'Saved' Folder](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#textools-saved-folder)
- [Anamnesis .chara File Read](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#anamnesis-chara-file-read)
- [Anamnesis .chara File Apply To Model](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#anamnesis-chara-file-apply-to-model)
- [Color Swatches](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#color-swatches)


### Import FFXIV .fbx File

- Imports a FFXIV Model's .fbx file into Blender, using these paramaters:
    - primary_bone_axis='X'
    - secondary_bone_axis='Y'
    - use_manual_orientation=True
    - axis_forward='Y'
    - axis_up='Z'
 
- Rotates the armature 90 degrees from the origin point, and presses 'Apply all transformations' so that Blender will treat this orientation as the 'rest' position.  It's _Important_ to **apply transforamtions** before importing VMD animation files, as it starts using this data for keyframes.

- Moves all 'Group' objects to an empty object called 'FFXIV Empty Groups'

- Update all material properties:
    - Fixes the alpha blend mode so that all the textures can be viewed properly (blend_method = 'HASHED')
    - Turns on backface culling (use_backface_culling = True)

- Update meshes:
    - Adds the"mmd_bone_order_override" armature modifier to the FIRST mesh on n_root (as per the [MMD Tools instructions](https://mmd-blender.fandom.com/wiki/MMD_Tools/Manual#mmd_bone_order_override))
    - Renames the meshes objects to something that is more human-readable

- Adds custom object/data properties:
    - Armature **object**:
        - original_root_name (MMD Tools moves the armature to a new object called 'New MMD Model' upon converting it, so it's useful to know the original name sometimes)
    - Edit bone **data**:
        - the head bone _local_ position 
        - the tail bone _local_ position
        - the matrix _local_ position
    - Mesh **data**:
        - ModelID - Parsed from original object name
        - ModelRaceID - Parsed from original object name
        - ModelNumberID - Parsed from original object name
        - ModelTypeID - Parsed from original object name
        - MeshPartNumber - Parsed from original object name
        - original_mesh_name - Parsed from original object name
        - original_material_name - Parsed from active material name
        - MaterialType - Parsed from active material name
        - ModelName - Parsed from FFXIV TexTools folder (if folder name found in TexTools 'Saved' Folder)
        - material_filepath - Parsed from FFXIV TexTools folder (if folder name found in TexTools 'Saved' Folder)
![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/0742b581-f962-4c7c-ad55-a653a2ce407e)


------
 
### Load Sample
 
 - Import an example .fbx model that is included with the plugin, and applies the same transformations that [**Import FFXIV .fbx File**](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#import-ffxiv-fbx-file) does:
    - AuRa Female
    - Elezen Female
    - Hrothgar Male
    - Hyur Highlander Female
    - Hyur Midlander Female
    - Lalafell Female
    - Miqote Female
    - Roegadyn Female
    - Viera Female
  
Useful if you need to quickly compare and diagnose your own .fbx file vs one I created for my testing, or you just need a test out each race really quickly.

------

### Initialize MMD Struture
Shortcut to the MMD Tools addon's Convert Model feature:

- Convert the model to an MMD Model's format adding all the properties and data needed to convert and use as a MMD Model.
- Moves your FFXIV Character's armature n_root from it's original object (your character's .fbx file name) to a new root object called 'New MMD Model'

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/3352b02f-6d40-4b65-92a7-3b2284a3e275)
![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/cc1040c1-bc5c-474b-8f34-2545917757dc)

------

### TexTools 'Saved' Folder
  
Saved' Folder where TexTools exports all textures and models by default. Used for pulling in extra custom properties details upon .FBX Import:
- Mesh data:  
    - ModelName - Parsed from FFXIV TexTools folder (if folder name found in TexTools 'Saved' Folder)
    - material_filepath - Parsed from FFXIV TexTools folder (if folder name found in TexTools 'Saved' Folder)

------
        
### Anamnesis .chara File Read:

Reads the .chara file and outputs to the results to Blender's System Console:

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/da942342-ed34-4b13-b7b2-3ed0a5e50212)


1) DIAGNOSIS: If an armature is selected, it compares the selected armature against the .chara file to see if it has all the correct equipment attached from TexTools. Useful if you made any mistakes exporting gear out of TexTools (such as the wrong equipment)

2) Outputs the following data used for TexTools .fbx export:
    - Skin Color ([hex value](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_skin_dictionary.csv)) - Colors vary depending on the Race, Tribe and Gender of the what is in the .Chara file 
    - Hair Color ([hex value](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_hair_dictionary.csv)) - Colors vary depending on the Race, Tribe and Gender of the what is in the .Chara file 
    - Hair Highlights Color ([hex value](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_hairhighlights_dictionary.csv)) - If hair highlights is disabled, will output the hair color
    - Iris Color ([hex value](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_hairhighlights_dictionary.csv))
    - Lip/Fur Color: ([hex value](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_lips_dictionary.csv))
    - Tattoo/Limbal Color: ([hex value](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_tattoo_limbalring_dictionary.csv))
    - Race, Tribe, Gender
    - Face Model: modelID (can be copy & pasted directly to TexTools search bar)
    - Hair Model: modelID (can be copy & pasted directly to TexTools search bar)
    - Tail Model: modelID (can be copy & pasted directly to TexTools search bar)
    - Body Gear: equipment ID (cannot parse the model variation if the model is shared in TexTools)
    - Legs Gear: equipment ID (cannot parse the model variation if the model is shared in TexTools)
    - Head Gear: equipment ID (cannot parse the model variation if the model is shared in TexTools)
    - Hand Gear: equipment ID (cannot parse the model variation if the model is shared in TexTools)
    - Feet Gear: equipment ID (cannot parse the model variation if the model is shared in TexTools)
    - Earring Gear: accessory ID (cannot parse the model variation if the model is shared in TexTools)
    - Necklace Gear: accessory ID (cannot parse the model variation if the model is shared in TexTools)
    - Wrists Gear: accessory ID (cannot parse the model variation if the model is shared in TexTools)
    - Ring Left Gear: accessory ID (cannot parse the model variation if the model is shared in TexTools)
    - Ring Right Gear: accessory ID (cannot parse the model variation if the model is shared in TexTools)

Sample Video: 

https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/ef673466-007f-473f-93c7-9320205ba3c9
    
------
    
### Anamnesis .chara File Apply To Model:

In addition to what [.chara File Read](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#anamnesis-chara-file-read) does, also:
 
1) Applies the Facial Deformation Shape Keys (shp_brw_a, etc) to the _all_ the meshes attached to the selected armature with a matching shape key name by setting the values to 1.0. Values are mapped in the [Chara File Dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/chara_file_dictionary.csv)

   ![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/7c260f02-acba-4571-ba7b-f2e5cd4c7000)

 
2) Adds the FFXIV Race's MMD [Facial Expression Bone Morphs ](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#bone-morphs-facial-expressions) (eye blink, smile, etc.) to the model (only works if the model has been converted to MMD Format). 

   ![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/7146a3b1-a699-40c1-a9f3-d96dd49b806b)

 
3) Adds .chara file custom properties to the armature object:
    

    - Facial Deformation ID (based on the FFXIV tribe & gender's face part selectors in-game)
        - Eyes
        - Eyebrows
        - Mouth
        - Nose
        - Jaw
    - Body Type IDs
        - ObjectKind
        - Race
        - Tribe
        - Gender
        - Head
        - Hair
        - TailEarsType
        - Bust
        - EnableHighlights (hair)
    - Equipment Gear IDs
        - HeadGear
        - Body
        - Hands
        - Legs
        - Feet
        - Ear (earrings)
        - Neck (necklace)
        - Wrists
        - LeftRing
        - RightRing
    - Colors (hex)
        - Skintone
        - HairTone
        - Highlights
        - LimbalEyes
        - REyeColor
        - LipsToneFurPattern
        - FacePaintColor
    - Random Stuff
        - SkinGloss (rgb)? I dunno.
        - BustScale (x,y,z)
        - FacialFeatures (Facial Checkbox flags)
     
    ![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/81be8212-ce57-4a19-ad65-c2119be822a1)

------

### Color Swatches

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/b420b0d7-93fd-4e19-855c-1559b14612a9)


Various colors displayed for the colors from the .chara file. Color Swatches are based on the [FFXIV Color Hex Reference Guide](https://docs.google.com/spreadsheets/d/18Z1ph1Xa-rFvC8FtB7X6IgSbjwPAom5XuDuCtVeNRvo). 

Displays for:
- [Skin](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_skin_dictionary.csv) - Colors vary depending on the Race, Tribe and Gender of the what is in the .Chara file 
- [Hair](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_hair_dictionary.csv) - Colors vary depending on the Race, Tribe and Gender of the what is in the .Chara file 
- [Hair Highlights](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_hairhighlights_dictionary.csv) - If hair highlights is disabled, will output the hair color
- [Eyes](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_eye_dictionary.csv)
- [Tattoo / Limbal Ring](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_tattoo_limbalring_dictionary.csv) (colored circle around the Iris for Au Ra characters) 
- [Lips / Fur (for Hrothgar chracters)](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_lips_dictionary.csv)
- [Facepaint](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_facepaint_dictionary.csv)

## Language and Translation

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/2705ac60-cca6-4ace-bd53-6db4a3c239b0)

Sections:
- [Mass Rename Bones](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#mass-rename-bones)
- [Blender to MMD Jap](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#blender-to-mmd-jap)
- [Swap Jap / Eng](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#swap-jap--eng)

------

### Mass Rename Bones

Used to rename bones according to the [Bone Dictionary table](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_dictionary.csv) and [Finger Bone Dictionary table](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_fingers_dictionary.csv) . If bone name in 'From' match found on the selected armature, bone will be renamed to the 'To' target bone name.

------

### Blender to MMD Jap

Will push the Blender Bone name to the MMD Tool's PMX Japanese Bone name (found in the Bone Properties -> **MMD Bone Tools** panel), assuming the MMD Tools application is installed in Blender.

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/af6885ba-63cd-4e0e-9e31-bf15e0c6455c)

------
 
### Swap Jap / Eng

Swaps the MMD (PMX) Japanese and MMD (PMX) English bone names, shape key names, and material names. Useful if you're in the MMD-only workflow


## Bones and IK
![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/1fcd5396-ca1b-40bd-9056-7a144297acf3)

Sections:
- [Visibility Shortcuts](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#visibility-shortcuts)
- [MMD Conversion Dropdown List](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#mmd-conversion-dropdown-list)
- [Find & Replace](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#find--replace)
- [Bone Groups](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#bone-groups)

------

### Visibility Shortcuts

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/3874acc0-c1c1-4813-80ff-e9afa8e057e2)

Shortcuts to the standard visibility options found on **Armature** -> **Viewport Display** panel:

- Hide/Show bones
- Hide/Show bone names
- Show bones in front of all other objects
- Display bones as:
    - Octahedral
    - Stick
    - Envelope
    - B-Bone
    - Wire
- Hide/Show armature (shortcut to the **MMD Tools** hide/show armature button, only displayed if model has been [converted to MMD Model](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#initialize-mmd-struture) format):

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/36507716-0f5b-4bad-b976-b4af4d34a73e)

------

### MMD Conversion Dropdown List

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/5262e25b-e78d-4b2d-be02-31f7f054699c)


Various steps to add/remove certain bones to MMD Format. _NOTE: Bones must be renamed from ['FFXIV' to 'MMD English' format](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#mass-rename-bones) for most of these to work._

#### Run Steps 1 to 12

Shortcut to running steps 1 to 12 in order

#### 1  -  Remove unused bones (no vertex groups)

Shortcut to [flag 'unused' bones](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#flag-unused-bones-as-unused) and [delete 'unused' bones](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#delete-unused-bones). 
Removes any bones without any meshes attached. Useful since the standard FFXIV bone struture that is imported includes bones including ones with no meshes attached. Removing them makes the armature cleaner / easier to see in Blender

#### 2  -  Correct MMD Root and Center bones

Adds the MMD 'root' and 'center' bones if they don't already exist on the model, and move the bones to the correct position while at rest pose

#### 3  -  Correct MMD Groove bone

Adds the MMD 'groove' bone if they don't already exist on the model, and move the bones to the correct position while at rest pose

#### 4  -  Correct MMD Waist bone

Moves the 'waist' bone to the correct position while at rest pose

#### 5  -  Correct Waist Cancel L/R bones

Adds the _special_ MMD 'waist_cancel_l' and 'waist_cancel_r' bones to the correct position, and sets the legs as their parent bones. These are modifiers that prevent the rest of the armature moving from the waist down. Useful for some certain MMD Models. Sometimes it's needed for VMD files, some times it is not. If there are issues with these bones, refer to the FAQ [question](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-why-are-the-leg-meshes-not-following-the-leg-bones-what-kind-of-witchcraft-is-this)  to fix

#### 6  -  Correct MMD 'view cnt' bone

Adds 'view_cnt' bone. Not really needed in Blender, but it's a placeholder bone useful sometimes for animating stuff in Miku Miku Dance, as some properties are keyframed to this bone.

#### 7  -  Correct Shoulder/Arm/Elbow Bone Lengths

Adjusts the standard FFXIV Bone lengths and positions to be closer to a standard MMD model. THIS IS NOT PERFECT, but it definitely helps. I still haven't figured out the exact position in order to get VMD files to animate the arms 100%. If there are issues upon importing a VMD file, refer to this [FAQ question](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master#q-when-i-play-an-animation-the-arms-dont-line-up-exactly-to-the-animation-or-clipcollide-into-the-headbodyother-hand-at-certain-parts-how-do-i-fix-this).

#### 8  -  Add Eyes Control Bone

Adds the special MMD 'Eyes' controller bone that is used to control 'eye_L' and 'eye_r' at the same time. Applies rotation to both bones

#### 9  -  Add Arm Twist Bones

Adds the special MMD 'arm_twist_1','arm_twist_2','arm_twist_3', 'wrist_twist_1', 'wrist_twist_2', 'wrist_twist_3' twist bones, for additional arm fine-tuneing for animations. Needed for some VMD animation files. 

#### 10 -  Add Shoulder Control Bones

Adds the special MMD 'should_C','shoulder_P' bones. Needed for some VMD animation files. 

#### 11 -  Add Leg/Foot IK
Adds the _standard_ MMD Leg/Foot IK Bones:
- leg IK_root_L
- leg IK_root_R
- leg IK_L
- leg IK_R
- toe IK_L
- toe IK_R

And also adds the _special_ MMD Control bones (used to move the meshes in certain direction _after_ IK is applied, since once IK is applied, you can no longer directly move the pose bone like you would with a non-IK bone):
- leg_L_D
- leg_R_D
- knee_L_D
- knee_R_D
- ankle_L_D
- ankle_R_D
- toe_L_EX
- toe_R_EX
- knee_2_L_D
- knee_2_R_D

#### 12 -  Auto-Fix MMD Japanese/English Bone Names

Shortcut to the [button with the same name](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#auto-fix-mmd-japanese--english-bone-names) in 'Export MMD Preparation' panel

#### 13 -  Add Hand/Arm IK

Adds some IK to hands/arms, similar to Leg/IK. Unlike Leg/Arm IK, this one is rarely if ever used in a VMD motion file, and is recommended that you don't use it unless it is actually called for. 

#### 14 - Add Extra Finger Bones (select finger mesh first)

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/7977812b-5c03-40fa-a3bb-6d30b22adfcd)


Adds a third finger bone (the last bone tip of a finger) to FFXIV models, since they only have 2 finger bones. Script will attempt to automatically weight paint the bones, but it is hit or miss. I'd avoid doing this unless you like weight painting manually. Ensure that the hand mesh is selected first _before_ running this command.

#### 15 - Add Extra Breast Tip Bones

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/4289c853-e186-4a68-9695-5dd7d336f230)


Will add an extra bone tip to the breasts bones (j_mune_l, j_mune_r) to match some other similar looking MMD Models, though it is not needed in Blender. Only useful if you're planning to [export to PMX format](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-i-want-to-export-my-model-to-pmx-format-how-do-i-do-that) and continue rigging using PMX Editor.

#### 16 - Merge Double-Jointed Knee (FFXIV PMX Export Only)

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/5a10f28c-39c6-443c-8ab8-bc2bb21f2af0)


Since most standard MMD Models don't have these 'double-jointed' knees, this will merge the FFXIV- 'j_asi_c_l' and 'j_asi_b_l'(or Knee_L if you've renamed the bone) bones into one, and attempt merging the weight painting into the newly merged bone.  Only useful if you're planning to [export to PMX format](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-i-want-to-export-my-model-to-pmx-format-how-do-i-do-that) and continue rigging using PMX Editor, otherwise if you're planning on staying in Blender, stick with the double-jointed knee to avoid extra headache.

#### EXPERIMENTAL - Adjust Arm Position for FFXIV Models

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/5f07fd05-b342-419f-81fd-4aa3ace99dad)

In the case of issues with the [arms not moving properly or going through the body/face using VMD animation files](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-when-i-play-an-animation-the-arms-dont-line-up-exactly-to-the-animation-or-clipcollide-into-the-headbodyother-hand-at-certain-parts-how-do-i-fix-this),  this attempts to adjust the should/arm/elbow bone postitions further to align with a stanard MMD Model. Sometimes it works and solves all the related arm motion problems, sometimes it doesn't. I can't seem to find a proper solution that will 100% work 100% of the time :S

#### Convert FFXIV Boobs to Genshin Boobs

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/c09f9db1-ef4f-417e-925c-9725c8d93519)

Leverages the bone structure for boobs found on Genshin Impact models and applies the same 'style' to FFXIV boobs:

- j_mune_l/r renamed to j_mune_l/r_mid
- mid bone is rotated 90 degrees and pointed downwards towards
- new j_mune_l/r_top (parent bone to j_mune_l/r_mid)
- new j_mune_l/r_bot
- new j_mune_core (parent bone to the _top and _bot bones)

When combined with [converting this to an MMD Model](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#initialize-mmd-struture) and applying [Rigid Bodies from FFXIV Template](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#from-ffxiv-template) + [Joints from FFXIV Template](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#joints), give the boobs a better looking bounce effect using MMD physics.

https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/f2aa4972-e705-4df5-858f-28f2be539918


------

### Find & Replace

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/3f2b77ad-7c98-4b20-b205-e89344daa5cd)


#### Find 
Will search for any bone of the selected armature (in edit mode or pose mode) containing the search text provided

#### Replace
Combined with the find textbox, will rename any found bones to the new name provided

#### Selected only checkbox
Will limit the 'replace' to only _selected_ bones

------

### Bone Groups

#### Auto Generate
Will add the armature's bones to the Blender's **Armature -> Bone Groups** panel, according to the [metadata bone group dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_metadata_ffxiv_dictionary.csv). If bone name is found matched in the 'mmd_english',	'mmd_japanese',	'mmd_japaneseLR', 'blender_rigify', or 'ffxiv' columns, will add the bone to the bone group specified in the 'blender_bone_group' column

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/c07eeed1-8a29-41e8-a027-8faf496404ba)


## Rigid Bodies

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/c739e6f2-d242-4135-ae82-e810b802a4fc)

Sections:
- [Visibility Shortcuts](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#visibility-shortcuts-1)
- [Active Rigid Body / Bone](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#active-rigid-body--bone)
- [Rigid Body Search](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#rigid-body-search)
- [Bone Chain Select](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#bone-chain-select)
- [Skirt Select](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#skirt-select)
- [Rigid Body Transform](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#rigid-body-transform)
- [Rigid Body Create](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#rigid-body-create)

------

### Visibility Shortcuts

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/15d1c5c8-6d9b-4b27-9d9d-22c3147f3ccb)


#### Hide/Show Rigid Body
Shortcut to the hide/show button on MMD Tools

#### Hide/Show Rigid Body Name
Shortcut to the hide/show button on MMD Tools

#### Hide/Show Mesh
Shortcut to the hide/show button on MMD Tools

#### Enable/Disable Physics
Shortcut to the enable/disable physics button on MMD Tools

------

### Active Rigid Body / Bone

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/5922bc1c-093c-495a-9432-a0b7bd29ada8)


Show the actively selected Rigid body's name, as well as it's connected bone's name. Clicking on the bone name will select the bone in edit mode

------

### Rigid Body Search

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/a84bb65c-3941-4c56-9348-1011821d1324)


Searches for rigid body name(s) based on the parameters provided (starts /w, contains, ends/w)

- 'Find' will deselect all selected objects first before showing the results
- 'Find + Add' is the same as 'Find' but will append the results to the currently selected objects
- 'Trashcan' will clear the 'starts w/', 'contains', and 'ends w/' textboxes

------

### Bone Chain Select

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/eafb1a00-a889-49c9-b8ba-d441bd243216)


#### Up
Based on the 'active' rigid body selected's **bone**, will append the bone's parent's rigid bodies recursively. Useful if you want to apply change in bulk to all the rigid bodies attached to the bones

#### Down
Same as 'Up', but looks for the bone's children recusively.

#### All
It does both 'Up' and 'Down' at the same time

------

### Skirt Select

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/8c5cec5e-dee8-413f-b52c-fa76cc0a66c0)


#### Vertical Skirt Selection

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/0fa35b5e-cc6e-4d1b-a8aa-8a0620ba4e1e)

When the [skirt module](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation/README.md#skirt) is leveraged to create rigid bodies, will select all vertical skirt rigid bodies from the active selection (based on the rigid body object name 'skirt_x_y', it will select any rigid bodies that match the currently active x)

#### Horizontal Skirt Selection

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/a420790d-c875-4c2e-acaa-b089696a2af3)


When the [skirt module](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation/README.md#skirt) is leveraged to create rigid bodies, will select all horizontal skirt rigid bodies from the active selection (based on the rigid body object name 'skirt_x_y', it will select any rigid bodies that match the currently active y)

#### All Skirt Selection

When the [skirt module](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation/README.md#skirt) is leveraged to create rigid bodies, will select all rigid bodies (based on the rigid body object name 'skirt_x_y', it will select any rigid bodies that match the the name 'skirt_')

------

### Rigid Body Transform

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/443629ec-b487-4d66-b9c5-726e5fe36992)


https://user-images.githubusercontent.com/19479648/225210461-c10581d3-ff3d-4fb8-92d8-1bed41de3dac.mp4

------

#### Bulk Apply Rigid Bodies
Used to apply changes to ALL selected rigid bodies. 

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/dc4f98da-7e11-41e4-8be7-62895cbdb552)

By default it will show the values on the ACTIVE rigid body.

Selecting a checkbox will apply that specific parameter to all selected rigid bodies.

------

#### Rigid Body Bone Chain

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/7b30110f-ba6c-497c-826f-8887240758a5)

Used to apply a 'gradient' change to MMD Tools' rigid bodies.

By default it will show the values on the highest parent rigid body (based on the bone structure) as the START value,with the lowest child bone's rigid body as the END value.

Selecting a checkbox will apply that specific parameter to all selected rigid bodies.

For example if there are 3 selected rigid bodies in a bone chain, with the starting value being 1, and the ending value being 2, the rigid bodies values will be:
- Rigid body 1: 1.0
- Rigid body 2: 1.5
- Rigid body 3: 2.0

Can be used when you need to edit multiple rigid bodies' shape at once, such as a skirt that is uniformly shaped at the top, but gradually gets larger and more angular at the bottom.

------

#### All Rigid Body Bone Chains
![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/e0800c28-922b-4b8c-a64a-396ed7bde7c5)

Same as above but applies the values to ALL selected rigid body bone chains. Since each rigid body bone chain has it's own unique start and end value, this doesn't use the 'absolute' values, but rather applies a delta value based on the inputs.

------

### Rigid Body Create

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/b0c1d3f6-93ff-4597-8de6-1735b02b7c8a)

------

#### From Selected Bones
Shortcut to the MMD Tools' Rigid Body Create button:

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/0d63493c-dc82-4b62-9ce6-9cf03d1a75ba)

------

#### From FFXIV Template
Creates a Rigid Body skeletion based on the FFXIV general bone body structure, with all these presets created.
To see the preset values applied to each bone and the values, check out the [Rigid Body Dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/rigid_body_dictionary.csv)

## Joints

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/2be9f179-7797-4f8e-b235-f6a626a6bd21)

Sections:
- [Visibility Shortcuts](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#visibility-shortcuts-2)
- [Joint Select Controls](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#joint-select-controls)
- [Joint Transform Controls](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#joint-transform-controls)
- [Joint Create](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#joint-create)

------

### Visibility Shortcuts

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/a7982deb-ef97-46e5-ac36-3bb376518b09)

Shortcuts to the MMD Tools show/hide joint, and show/hide joint name respectively.

#### Active Joint / Rigid 1 / Rigid 2

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/77775dca-32ac-426c-8268-7b592cb6c61d)

When a joint is selected, will show the joint name, as well as its two associated rigid bodies. Clicking on the rigid body name will select it.

------

### Joint Select Controls

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/4cfa0691-e87a-42a3-963c-f6230bdc457d)



https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/bc80d732-eb93-4c43-b451-28fc25afc97a



#### Get Joints from Rigid Bodies

When there are **multiple** rigid bodies selected, will scan the armature for **all** the associated joints that are connecting them and select the joints.

#### Vertical Select

When there are **multiple** joints selected, will scan for any rigid bodies that are connected in a **rigid body bone chain** ([see explanation](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation/README.md#rigid-body-bone-chain)) (meaning they are vertically connected) and filter the selection to ONLY these joints.

#### Horizontal Select

When there are **multiple** joints selected, will scan for any rigid bodies that are NOT connected in a **rigid body bone chain** ([see explanation](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation/README.md#rigid-body-bone-chain)) (meaning they are horizontally connected) and filter the selection to ONLY these joints.

------

### Joint Transform Controls

Used to apply bulk changes to multiple selected joints. By default, all of the fields will be populated with the currently **active** joint.

To apply changes, input a value to one of the properties, select the checkbox next to it and press 'OK'

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/402f9c24-7238-469d-af5e-6583fbf78cb9)

------

### Joint Create

#### From Selected Rigid Bodies

Will create joints in bulk when there are 2 or more selected rigid bodies selected. **BUG: Currently only creates multiple joints when they are connected in a rigid body bone chain (meaning, it is a vertical joint). ** This is a **MMD Tools bug**.

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/70c0013d-5efe-4613-b0ba-c4cdca2405fe)

------

#### Create Vertical Joints

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/a7236bfa-bb3a-4f97-a275-2df7e36da535)

Create joints in bulk where there are **multiple** **rigid body bone chains** ([see explanation](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation/README.md#rigid-body-bone-chain) selected, with only joints being created between rigid bodies that have a bone parent & child relationship, with  the option to create a joint for each bone chain's highest parent to a common rigid body that is shared between tham  (such as selecting all the hair rigid bodies and pinning the highest rigid body in each bone chain to the "head" rigid body)

Please be aware that this means that ONLY joints will be created between a rigid body bone's parents and children, meaning that there will be NO joints created between two separate bone chains. To create joints in bulk where there is no bone parent/child relationship refer to the Create Horizontal Joints section below.

Sample video:

https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/649d0ff4-9024-4e59-8fc1-6d05f855fe16

------

#### Create Horizontal Joints

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/73a80223-0233-46e6-af55-0ab3d05d3f3e)


Create joints in bulk where there are **multiple** **rigid body bone chains** selected, however there is no hierarchal parent/child relationship between the bones. To do this, all rigid bodies need to share a 1) a common name AND and two numbers in the same position.

**Example rigid body name:** skirt_0_1
- **common name pattern shared on all rigid bodies:** skirt_
- **first number**: 0
- **second number** 1

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/94434e2b-caed-4ee0-b59c-b761f57fd680)


The search criteria (starts w/, contains, ends w/) will specify the **scope** of rigid bodies that need horizontal joints, will need to use the common name pattern to do so upon pressing 'find'.

Upon pressing 'Find', the search results will:
1) Show ALL rigid bodies that contain that common name pattern-- this becomes the scope of rigid bodies that will create  horizontal joints for
2) Show (at minimum) **two** numbers that will indicate if eveything that shares that same number is a 'horizontal' rigid body chain. The two numbers provided will be based on a rigid body within the search scope at random

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/205a3700-0b02-4962-9b91-cf016d0dec53)


Upon selecting one of the two (or more) numbers, a box will be displayed with a **<--previous ** and **next -->** button on it:

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/69c3b9e0-a32e-4bad-9bc0-424408c70999)


These two arrows will be used to iterate through **all** the  rigid bodies in the search scope that share that same number's position in the rigid body name. This is for **testing** if the correct number position is selected (either the first number or second number in this example.

'Connect ending and starting rigid body' checkbox is to determine if the **starting** rigid body is supposed to have a joint to the **ending** rigid body. If unchecked, no joint will be created between them. This is useful if the selected rigid bodies are supposed to form a **full** circle horizontally, or not.

Upon pressing 'OK' the horizontal joints will be created.

Sample video:

https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/bf936ddc-c184-42f4-8665-4cf670857cbd


## Bone Morphs (Facial Expressions)

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/168df871-2fa1-4e3f-9e5b-fdd808369f44)

Bone Morphs defines how much each posebone should move in order to make a facial expression.

In Blender's MMD Tools, these bone morphs are made by manually adjusting a model's pose bone's rotation on the X/Y/Z axis, or offsetting their location on the X/Y/Z axis. For example, how many degrees an eyelid bone should rotate down on the Z axis in order for a model to wink. These location/rotation offsets are then stored in a 'Bone Morph', with the value of 1 meaning that the pose bones are 100% applied, and 0 meaning 0% of it is applied (the bone is at it's original rest position).

Typically these pose bones are grouped together to make a Bone Morph. For example a 'blink' bone morph is a combination of both the left _and_ right eyelid bones together.

The facial expressions that are commonly used by MMD animation files are referenced on this [MMD Facial Expression Reference Chart](https://www.deviantart.com/xoriu/art/MMD-Facial-Expressions-Chart-341504917). We cannot reproduce everything on the reference chart since this plugin doesn't add any 'new' data into the FFXIV model (such as adding the 'heart' eyes or the 'star' eyes, as those special shapes doesn't exist on the standard model.

[Bone Morph Master List](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bone_morph_list.csv) - Defines the overall list of Bone Morph 'Groups' s that are useable by each FFXIV race, as well as the japanese / english names that are used by VMD motion files for animation.

------

### Generate Bone Morphs

The list below contains each FFXIV Race's own list of preset pose bone offsets (from rest position) to either their location or rotation on the XYZ axis (in XYZ Euler mode):
- [Au Ra](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bone_morphs_aura.csv)
- [Elezen](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bone_morphs_elezen.csv)
- [Hrothgar](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bone_morphs_elezen.csv)
- [Hyur](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bone_morphs_hyur.csv)
- [Lalafell](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bone_morphs_lalafell.csv)
- [Miqo'te](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bone_morphs_miqote.csv)
- [Roegadyn](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bone_morphs_roegadyn.csv)
- [Viera](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bone_morphs_viera.csv)

It's worth noting that these were manually tuned by myself (it's not a conversion from FFXIV animation files, they are completely something new I created added), so there are no guarantees that they are '100% accurate' to any facial expressions that could be made in-game, there is always room for improvement here

------

### Change Rotation Mode

Change the rotation mode of the facial pose bones. By default, all pose bones are rotated in quaternion (XYZ+W), which is very difficult to work with. 
By changing rotation mode to 'XYZ Euler', it becomes much easier to manually adjust the pose bones, in order to make your own bone morphs / facial expressions, or when adjusting the ones that come built into this plugin.

## Skirt

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/3d688d98-760b-4585-9c5c-3a64ea6bad4c)

Sections:
- [Generate a New Skirt Object](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#generate-a-new-skirt-object)
- [Move Mesh To New Skirt Object](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#move-mesh-to-new-skirt-object)
- [Weight Paint Transfer to Mesh](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#weight-paint-transfer-to-mesh)
- [Delete FFXIV & Unused Skirt Vertex Groups](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#delete-ffxiv--unused-skirt-vertex-groups)
- [Move Skirt Bones and Meshes to Armature](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#move-skirt-bones-and-meshes-to-armature)
- [Generate Skirt Rigid Bodies](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#generate-skirt-rigid-bodies)
- [Generate Skirt Joints](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#generate-skirt-joints)
- [Vertex Group List](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#vertex-group-list)


------

### Generate a New Skirt Object

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/4a467464-f863-4893-956a-2710bda954d5)

This will create a skirt object called 'skirt_obj' with it's own cone-shaped mesh called 'new_skirt_shape', and cone-shaped armature with all the included bones under 'new_skirt_arm'.

- The cone-shaped bones are intended to be your new skirt's bones for using leveraging MMD-style physics with rigid bodies & joints. These skirt bones will be **transferred** to your model's armature once this whole process is complete.
- The cone-shaped mesh will have **weight painted pre-applied** to the bones. This cone-shaped mesh needed in order to perform a 'weight paint transfer' to your model's skirt mesh. This cone-shaped mesh will be **deleted** upon completing this whole process.

https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/b12906f1-55d1-4aae-8b59-b7e72eca9a5b

The paramaters are as follows:

- **Bone Chains** -  Specifies the number of bone chains that will encircle the circumference of your model. For example specifying '4' will have a bone chain starting on your model's left side, back, right side, and front.
- **Bone Chain Children** - Specifies how many bones will be added for each bone chain from the top of the skirt to the bottom of the skirt.
- **Mesh Segments** - Specifies how 'round' the circumference of your skirt mesh will be. Specifying a higher number will add more verticies to the circumference your skirt. Lower numbers will make your skirt object look like it was made in Quake
- **Mesh Subdivisions** - Specifies how many face subdivisions should be on the cone-shaped mesh. The higher the number, more faces will be on your mesh, and the more accurate/detailed the weight painting will be.
- **Top Height** - Specifies the XYZ's coordinate height of the **top** of the skirt from 0. Ideally this should be placed where you expect the new skirt's weight painting to be transferred onto your model
- **Top Radius** - Specifies how large/small the **top** of your skirt is
- **Bottom Height** - Specifies the XYZ's coordinate height of the **bottom** of the skirt from 0.
- **Bottom Radius** - Specifies how large/small the **bottom** of your skirt is

Upon pressing 'OK', it will create the skirt_obj and **remember** the parameters upon the next time you press the 'OK' button. **IT IS PERFECTLY FINE TO PRESS 'OK' EVEN IF YOU STILL WANT TO MAKE CHANGES** because every single time you press the OK button, it will **replace** the current skirt_obj with a **new** skirt object

------

### Move Mesh To New Skirt Object

Will move the currently selected active object to the 'skirt_obj' object. To prevent accidentally breaking things on the armature, all the weight paint transferring occurs only on meshes that exist within the 'skirt_obj' object.

https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/0959d3c8-2bec-4f95-bb6a-6630780eec51

------

### Weight Paint Transfer to Mesh

Will transfer the weight paint from 'new_skirt_shape' to the currently selected mesh, assuming it exists in the 'skirt_obj' object.

Please note: Weight paint transfer will ONLY work if the selected mesh is as as physically close as possible to the new_skirt_shape mesh. If they are physically too far apart, the weight paint won't transfer properly.

You can see if weight paint transferred properly by scrolling through the vertex group list:

https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/a529aa5c-cc10-4b92-8b11-e1859cd59388

Note: After running this, you may want to test if the weight paint was transferred properly by going into 'Pose' mode and applying some simple rotation & location bone testing. If there are any issues with weight paint transfer, you can always start over from '[Generate a New Skirt Object](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#generate-a-new-skirt-object)' 

------

### Delete FFXIV & Unused Skirt Vertex Groups

Deletes any of the FFXIV vertex groups that start with 'j_sk_', or any vertex groups that start with 'skirt_' where it's corresponding bone can't be found. This is to prevent any weight paint conflicts between the _new_ weight painting that was applied in the previous step and the old FFXIV skirt bones.

------

### Move Skirt Bones and Meshes to Armature

Will move the meshes and bones contained within 'skirt_obj' object to the currently selected armature, while 'new_skirt_shape' mesh will be deleted.

The parent for all the skirt bones will be either 'lower body' (MMD English bone name),'下半身' (MMD Japanese bone name)  or 'j_kosi' (FFXIV lower body bone).

https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/d4c9c1b9-6a56-445c-a08d-e2d9e8614730

------

### Generate Skirt Rigid Bodies

If you used all the above steps to create the skirt bones and successfully transferred them to your armature, this will create a rigid bodies with **all** with gravity/friction/size/collision group settings preapplied. By default, these settings are configured for a somewhat 'heavy' skirt.

https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/4ee99bab-c998-48fd-9e68-ea3b9b7ef1d4

------

### Generate Skirt Joints

If you used all the above steps to create the skirt bones generated the rigid bodies, this will create joints with all the joint linear & angular parameteres preapplied. By default, these settings are configured for a somewhat 'heavy' skirt.

Searches for a rigid body named 'lower body','下半身' or 'j_kosi' first. If it does not exist this will not work, as the skirt's rigid bodies needs to be physically pinned to this 'lower body'.


https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/a64e1020-649c-4b0e-9ab1-2992f278a753

------

### Vertex Group List

Lists all the vertex groups for the currently selected mesh. Useful when trying to see if weight painting was applied correctly while in weight painting mode.


## Shaders

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/7eab16f2-d992-4de5-b088-b6afe8cd643d)

Sections:
- [Active Material](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#active-material)
- [Colorsetter Gear Texture Folder](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#colorsetter-gear-texture-folder)
- [Apply Colorset](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#apply-colorset)
- [Glossy Shader](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#apply-glossy-shader)
- [Eye Catchlight Shader](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#apply-eye-catchlight-shader)
- [MekTools Skin Shader](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#apply-mektools-skin-shader)
- [MekTools Eye Shader](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#apply-mektools-eye-shader)
- [Colorsetter Shaders](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#apply-colorsetter-shaders)
- [Background Color](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#background-color)


------

### Active Material

Shortcut to selecting the active material for a mesh. 
![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/ea42a076-7b54-4a1d-9825-86335ec952fc)

------

### Colorsetter Gear Texture Folder

Location of the FFXIV Gear's textures that you would like to apply the colorset addon's textures to. This should be set to your TexTools' gear's foldername that you have exported. Typically this would be found in the Documents\TexTools\Saved\*gear type*\*gear name* folder

For example on my Windows 10 PC if I would like to apply the "Diados Jacket of Fending" textures, it would be: 
- C:\Users\ %userprofile%\OneDrive\Documents\TexTools\Saved\Body\Diadochos Jacket of Fending\
  or
- C:\Users\ %userprofile%\Documents\TexTools\Saved\Body\Diadochos Jacket of Fending\

------

### Apply Colorset

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/7349c9bb-87de-4cd1-8bcf-0694e4131dd4)


Will automatically apply the colorset addon's material to ALL meshes that share this material. The material will be called 'Colorsetter Base'. 

Unlike using the colorsetter addon on its own (that destroys the old material), THIS plugin will store a backup of the old material, it's original name will be prefixed with 'backup_'

In order for this to properly, you need:
1) The colorset addon installed in Blender([link](https://drive.google.com/drive/folders/10ashyJJ4HhJqFxDVnGU6s9lyJ0aFHRwa))
2) ALL the textures files that are available (diffuse, normal, specular, multimap, colorset, etc...) exported to JPG, BMP AND DDS from TexTools. Make sure Alpha textbox (A) is also checked before export as well. 
![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/20b3e6f7-3d72-423c-8a95-c108b33d92ad)


https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/76c763c8-210c-4f4e-8ae6-d9a71cd5fca0

Please note: there is BUGS with the colorset addon that may prevent some DDS colorset files to be applied. This plugin (FFXIV MMD) will roll back any changes to prevent losing your original material. 
To see the actual error message, attempt to use the color setter plugin manually and review the Blender Console Window.

------

### Apply Glossy Shader

Applies a 'Glossy BSDF' shader to a material. Once applied, the 'Roughness' skilder will be displayed, along with an 'X' button. The X button removes the shader from the active material


![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/2e497455-e761-484e-8c6f-dd023b8e012b)



#### Glossy Roughness Slider

Adjusts the Gossy shader's roughness


------

### Apply Eye Catchlight Shader

Adds a 'floating' eye catchlight to the currently selected mesh that:

- uses ffxiv's built-in "catchlight_1.png" texture
- moves/floats around the eye depending on your camera angle

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/31dc26d8-37c3-4970-9ae8-cf3956c20d2d)

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/870d519e-5157-4397-a7ea-d97e2efa48fa)


This works on its own, OR can be used in combination with the Mektools Eye Shader / Colorsetter Eye Shader.

------

### Apply MekTools Skin Shader

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/4aeb848a-75ee-4f62-b370-e0876a3c1060)

If you have the [MekTools Addon](https://www.xivmodarchive.com/modid/22780) installed, this will automatically apply the shader to the currently selected mesh, and add a few controls so that you don't need to go to the Shader Node Editor to adjust these settings. The X button removes the shader from the active material.

Upon applying this shader, a BACKUP of the original material is stored (it is the ORIGINAL name of the material prefixed with 'backup_'. This addon also adds a 'mektools_' prefix to the material as name as well. Pressing the 'X' button deletes the 'mektools_' material and restores the original 'backup_' to the active material for this mesh.

The following controls have been added (there's still more to add, like 'Lip Color' and 'Subsurface Color', but to be honest when I played with these settings, I didn't like the look, so it's not high on my priority list.

Anyway yeah embedded within the MekTools skin shader, the following controls has been exposed into this addon's panel:

- Subsurface Scattering
- Specular
- Wet
- Roughness

------

### Apply MekTools Eye Shader

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/ec9c8761-d369-4029-b637-a8d90e4f06d1)


If you have the [MekTools Addon](https://www.xivmodarchive.com/modid/22780) installed, this will automatically apply the eye shader to the currently selected mesh, and add a few controls so that you don't need to go to the Shader Node Editor to adjust these settings. The X button removes the shader from the active material.

Upon applying this shader, a BACKUP of the original material is stored (it is the ORIGINAL name of the material prefixed with 'backup_'. This addon also adds a 'mektools_' prefix to the material as name as well. Pressing the 'X' button deletes the 'mektools_' material and restores the original 'backup_' to the active material for this mesh.

- Eye Type (need to pick depending on the Character's Race/Tribe.
- Brightness
- Eye Color

Also allows user to select a different image diffuse file & catchlight image file. They're built into the MekTools addon, but you can change it if you want to.

------

### Apply Colorsetter Shaders

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/19f6e4e1-8fe9-4cd0-9698-3c31c1f66477)

Automatically adds the Colorsetter Shaders to the currently selected mesh, and add a few controls so that you don't need to go to the Shader Node Editor to adjust these settings. The X button removes the shader from the active material.

Upon applying this shader, a BACKUP of the original material is stored (it is the ORIGINAL name of the material prefixed with 'backup_'. This addon also adds a 'colorsetter_' prefix to the material as name as well. Pressing the 'X' button deletes the 'colorsetter_' material and restores the original 'backup_' to the active material for this mesh.

If [Apply .chara To Model](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#anamnesis-chara-file-apply-to-model) was used beforehand, it will automatically apply the .chara file's colors upon adding a Colorsetter Shader

Sample Video:
https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/20f4480a-9aec-425b-bb94-0122e42475e5


#### Skin

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/01f1354b-d72c-4aac-9d38-f12abb596ac0)

TBD

#### Eyes

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/e8382a90-003d-4829-ba9d-e94b2cdb4689)

TBD

#### Face

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/0b0dbd6b-4d80-4377-a0cc-da7ba7e1cad1)


TBD

#### Face Accent

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/894a2eed-d821-4e2e-bbf5-8acc4e9a5265)


TBD

#### Hair

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/b86b00d9-56da-41ec-81c9-593888c95fdb)


TBD

#### Hrothgat / Miqote Tail

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/d38e9353-d129-4b02-ba53-b47e91f21961)


TBD

------


#### Background Color


![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/b85271e2-ef7e-4815-9478-8d489c5041d0)

Adds a background color that can be seen in renders. This is perfect for green screening/keying, as it is a uniform color and there is no gradient or shadows,  and it does NOT bleed any light/color onto your scene. Pressing the 'X' button will remove the shaders.

------
## Decals / Face Paint

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/a4191cb1-a5b3-492d-93b2-4d45017b6558)


Adds up to 4 (or possibly more in the furture) facial decals to your FFXIV models.

To use:
1) You must know the decal # for the facepaint you want to apply from TexTools!
2) Select the face mesh
3) Push the 'Add Decal' button3
4) Pick the decal .png file from the addon's built in ones, or select a .png from your harddrive

Each Decal is a grouped shader node that is shared amongst ALL models that it is applied to. For example, if you have two FFXIV models, and they both have Decal 1 appled, they will BOTH share the same decal .png file. Although the parameters that are applied (such as Base Color/Subsurface/Mix/etc...) are NOT shared, so it is something to be aware of. If you want to apply two different decals to two difference models, apply Decal 1 to the first model. and Decal 2 to the second model.

The group decal node automatically applies 'UV2' to the materials so you don't need to add it manually. 

Pressing the 'X' button will remove the decal from the active material. 

Parameters:
- Base Color
- Mix (Subsurface Amount)
- Subsurface Color
- Roughness
- Specular



## Miscellaneous Tools

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/2e9399b8-1897-47dd-af46-279fad7c04e6)

Sections:
- [Dropdown List](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#dropdown-list)
- [Bust Slider](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#bust-slider)
- [Rigify Meta-Rig](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#rigify-meta-rig)
- [MekTools Rig](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#mektools-rig)
- [Bone Compare](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#bone-compare)

------

### Dropdown List

#### Fix object axis (90 degrees)

Rotates an object's axis by (you guessed it) 90 degrees, and then does a 'Apply All Transformations' so that this becomes the new XYZ 0,0,0

#### Combine 2 bones

Attempted to merge two bones into one one, as well as attempts to merge the weight painting from the two bones together, but the weight painting might not be perfect and will probably still need to be fixed for any/all bones that used to leverage it.

#### Flag Unused bones as 'unused'

Scans the armature for any bones that are not used by any meshes, and adds a prefix of 'unused_' to them. Please note: any bones that are identified as 'is_special' bones on the [metadata bone dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_metadata_ffxiv_dictionary.csv) are excluded from this

#### Delete 'unused' bones

Combined the the setting above, it does exactly that.

#### Remove Orphaned Rigid Bodies

Scans the armature for any rigid bodies that exist but it cannot find it's associated bone. This will delete these rigid bodies. 
Used for making sure MMD Tools doesn't crash or act weird when physics is turned on. Sometimes you delete a bone, and this happens.

#### Remove Orphaned Joints

Scans the armature for any joints that exist but it cannot find either of the two rigid bodies that it is supposed to be attached to. This will delete these joints. 
Used for making sure MMD Tools doesn't crash or act weird when physics is turned on. Sometimes you delete a rigid body, and this happens. I delete rigid bodies a lot, and this has been extremely useful to me.

------

### Bust Slider

Adjusts the boobie size of pose bones 'j_mune_l' and 'j_mune_r', and adds a keyframe to frame 0 so that it (hopefully) stays that size when you import a VMD motion file. I don't know why sometimes it works, and sometimes it doesn't... If anyone wants to do some boobie research and let me know what's up, I'll try to fix it.

The scale slider should match the same settings as the FFXIV game ([reference data link](https://docs.google.com/spreadsheets/d/1kIKvVsW3fOnVeTi9iZlBDqJo6GWVn6K6BCUIRldEjhw/edit#gid=296196266)).

Here's the boobie math:
- scale_x = 0.92 + (bust_scale_number * 0.16)
- scale_y = 0.816 + (bust_scale_number * 0.368)
- scale_z = 0.8 + (bust_scale_number * 0.4)


------

### Rigify Meta-Rig

Allows you to add a pre-rigged [Rigify Meta-Rig](https://docs.blender.org/manual/en/latest/addons/rigging/rigify/metarigs.html) to your FFXIV Model. To use, you must have the [Rigify Addon installed](https://www.pluralsight.com/blog/tutorials/rigging-minutes-blenders-rigify-addon) (it's in the Blender Addon Menu but it's disabled by default. These features currently in 'research' phase, so don't expect everything to work properly.

#### Add

Shortcut to adding a "Human (Meta-Rig)" from the standard menu

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/7ef977c4-c23f-421c-a697-3c718a1df56e)

#### Fix

Will adjust the Meta-Rig's bone structure to match that of your MMD Model. Leverages the [metadata dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_metadata_ffxiv_dictionary.csv) to match any MMD English, MMD Japanese, MMD Japanese.LR or FFXIV bone against it's corresponding Rigify Meta-Rig bone name. Only the body has been mapped, the face will take a lot longer to figure out.

#### Apply

Shortcut to pressing the 'Generate Rig' button in Rigify Addon.

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/6841c5e3-25db-4fc5-8546-f2c17629fb43)


Note: To make everything work 'properly', I will probably need to enable/disable a bunch of stuff in the 'Advanced' section of Rigify, but again for now it's on the backburner.



------ 

### MekTools Rig

#### Add MekTools Rig

If you have the [MekTools Addon](https://www.xivmodarchive.com/modid/22780) installed, will automatically add the MekTools rig to your selected FFXIV Model.

Tool automatically detects your character's race, tribe and gender so all you gotta do is press the button and it will automatically add the rig, as well as apply the 'armatuer deform' modifier to the MekTools rig for ALL your meshes. That's one less step for you and a lot of less rigging work

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/fba6cce1-cbce-4d94-bf79-10690a0bcd9b)

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/5cd79810-a665-4fdb-843c-d85b45dd437d)


------ 

### Bone Compare

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/05559671-8d9a-4f27-ae9a-e653a3000e42)

#### Source

Selects the source armature from which to find & compare a source bone

#### Target

Selects the target armature from which to select a target bone

#### Swap Source & Target Armature

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/20f5d469-d760-4cde-9ea0-281b6d72d977)


Swaps the source armature & target armature. Upon pressing it, if there is a matching source armature bone from whatever is filled out on the bone textbox, it will auto-fill the 'Bone' field with the source armature's bone. Leverages the [metadata dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_metadata_ffxiv_dictionary.csv) to match any MMD English, MMD Japanese, MMD Japanese.LR, FFXIV, or Rigify Meta-Rig bone.

#### Select the current active bone as the target bone

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/6b246eb0-d22b-469f-ac88-c16cea92eb17)

Sets the currently selected active bone in the viewport as your target bone.


#### Copy Rotation - Source Bone

Applies a 'Copy Rotation' modifier from the source bone (if there indeed is a match) to the selected target bone in the textbox. 

#### Copy Rotation - All Arm Bones

Applies a 'Copy Rotation' modifier to the following MMD English-equivalent bones on the target armature:

- arm_L/R
- elbow_L/R
- wrist_L/R
- thumb1_L/R
- thumb2_L/R
- fore1_L/R
- fore2_L/R
- fore3_L/R
- middle1_L/R
- middle2_L/R
- middle3_L/R
- third1_L/R
- third2_L/R
- third3_L/R
- little1_L/R
- little2_L/R
- little3_L/R

#### Scale X/Y/Z

Used to compare the target bone's scale against the source bone (if there indeed is a match). Useful when importing a VMD animation file and applying it to your FFXIV Model that has been converted to MMD. How to use:

1) Using MMD Tools, import a MMD Model that works well with the VMD Animation file with a scale of **1.0**:

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/7b12dffc-de9d-4b04-b871-f0da5922133b)

Upon import, the MMD Model will look like a giant. This is FINE. All we want from the MMD Model is to know the scale difference from one of it's bones to one of the FFXIV model's bones.

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/683aa67f-0cf8-4a8e-a422-b7e46709a734)

2) Using this addon, select the source armature (MMD Model), target armature (FFXIV Model), and target armature's bone ('neck' bone is usually a good one to use):

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/f633cc4b-5a38-4601-aa12-33b119f4e322)


In the above picture, 'Z' scale is 0.042. Now we have a good scale that can be used for VMD animation. You can test it's a good scale if you take the MMD model and apply 0.042 to the X,Y, and Z scale to the MMD Armature.

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/32748873-f222-477d-b096-3bc5490fc73c)

We're done with the MMD Model, we just needed it for the scale number, you can delete it now if you'd like.

3) Using MMD Tools, import a VMD Motion file to your FFXIV Model. **Use 0.042 for scale.**

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/09210619-85f4-418f-bafb-842377b63a0d)

All done. When you import the VMD Motion file, you should find that the animation now better closely aligns with your FFXIV Model file.

## Export MMD Preparation

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/54d3a8a5-861d-4bf7-b411-46ffe8cdde9f)

Sections:
- [Auto-Fix MMD Japanese / English Bone Names](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#auto-fix-mmd-japanese--english-bone-names)
- [Add Display Panels](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#add-display-panels)
- [Sort Bone Order / Deform Tiers](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#sort-bone-order--deform-tiers)
- [Lock Position & Rotation](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#lock-position--rotation)
- [Set Fixed Axis / Local Axis](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#set-fixed-axis--local-axis)
- [Hide Special & Physics Bones](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation#high-special--physics-bones)

------

### Auto-Fix MMD Japanese / English Bone Names

Fixes the MMD Japanes & English PMX Bone names (while not changing the Blender Bone Name) to their MMD Japanese equivalent. Useful so that you can import a VMD animation file using the MMD Japanese (PMX) bone name without needing to read Japanese in Blender :P.

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/af6885ba-63cd-4e0e-9e31-bf15e0c6455c)

Leverages the [metadata bone group dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_metadata_ffxiv_dictionary.csv) to do the PMX Bone group mapping. If Blender bone name is found matched in the 'mmd_english',	'mmd_japanese',	'mmd_japaneseLR', 'blender_rigify', or 'ffxiv' columns, will add the 'mmd_english',	'mmd_japanese' bone name MMD Tool's PMX Japanese/English Bone name fields respectively (found in the Bone Properties -> **MMD Bone Tools** panel). If no match is found, and the PMX field is empty, it puts the Blender bone name verbatim so at least the MMD field is not empty and has a name.

------

### Add Display Panels


 Adds add all the bones, and vertex morphs and bone morphs to the display groups sections that you would find in Miku Miku Dance program upon .pmx export.


-  **Auto Generate**:

    ![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/c54d5852-7664-4c11-9f40-ebb99a96c870)
   
    - Leverages the [metadata bone group dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_metadata_ffxiv_dictionary.csv) then sends this data to the populate display panels in MMD Tools. 

- **Copy from Blender Bone Groups**:

    ![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/7c364d81-eaa3-4008-9828-e1ce3a94142c)

    - It will add the Blender Bone Group names to MMD Tools' Display Panels section 



------

### Sort Bone Order / Deform Tiers

Leverages the [metadata bone group dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_metadata_ffxiv_dictionary.csv) to sort the bone order in MMD Tools. 

THIS IS VERY IMPORTANT FOR PMX EXPORT TO FOLLOW THESE STEPS IN ORDER (taken from the [FAQ guide for exporting to PMX Format](https://github.com/wikid24/ffxiv_mmd_tools_helper#q-i-want-to-export-my-model-to-pmx-format-how-do-i-do-that)):

2) On the MMD Tools Plugin -> **Bone Order** Panel -> Click on that weird square shape on the bottom
3) Click on the arrow to expand the menu
4) Click on **Add Missing Vertex Groups from Bones**

![image](https://user-images.githubusercontent.com/19479648/225152213-4dffae74-5e2e-4de6-b992-a9baec4066af.png)

5) Back in FFXIV MMD Tools Plugin, click on 'Sort Bone Order / Deform Tiers'

------

### Lock Position & Rotation

Leverages the [metadata bone group dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_metadata_ffxiv_dictionary.csv) to lock position and rotation of bones ( you can see these flags in PMX Editor). This isn't really 'required' for PMX Export, but it doesn't hurt either

------

### Set Fixed Axis / Local Axis

Leverages the [metadata bone group dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_metadata_ffxiv_dictionary.csv) to set bones to either 'fixed axis' or 'local axis'  ( you can see these flags in PMX Editor). This isn't really 'required' for PMX Export, but it doesn't hurt either

------

### Hide Special & Physics Bones

Leverages the [metadata bone group dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_metadata_ffxiv_dictionary.csv) to set bones to be hidden from the Miku Miku Dance viewport so they won't clutter your screen.  ( you can see these flags in PMX Editor)
