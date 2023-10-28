# 3D Viewport -> Sidebar

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/b009c050-95a0-45fc-908e-304c13ea8bf4)


## Import FFXIV Model

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/80e3a3ba-cd96-4897-a73e-b82bfe8b11eb)


### Import FFXIV .fbx File

- Imports a FFXIV Model into Blender and presses 'Apply all transformations' so that Blender will treat this orientation as the 'rest' position. _Important_ to apply transforamtions before importing MMD animation files as it starts using this data for keyframes.
    - primary_bone_axis='X'
    - secondary_bone_axis='Y'
    - use_manual_orientation=True
    - axis_forward='Y'
    - axis_up='Z'

- Moves all 'Group' objects to an empty object called 'FFXIV Empty Groups'
- Fixes the alpha blend mode so that all the textures can be viewed properly (blend_method = 'HASHED')
- Adds the"mmd_bone_order_override" armature modifier to the FIRST mesh on n_root (as per the [MMD Tools instructions](https://mmd-blender.fandom.com/wiki/MMD_Tools/Manual#mmd_bone_order_override))
- Renames the meshes objects to something that is more human-readable
- Adds custom object/data properties:
    - Armature object:
        - original_root_name (MMD Tools moves the armature to a new object called 'New MMD Model' upon converting it, so it's useful to know the original name sometimes)    
    - Mesh data:
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


 
#### Load Sample
 
 - Import an example .fbx model that is included with the plugin:
    - AuRa Female
    - Elezen Female
    - Hrothgar Male
    - Hyur Highlander Female
    - Hyur Midlander Female
    - Lalafell Female
    - Miqote Female
    - Roegadyn Female
    - Viera Female

#### Initialize MMD Struture
Shortcut to the MMD Tools addon's Convert Model feature. Will convert the model to an MMD Model's format adding all the properties and data needed to convert and use as a MMD Model. Will move your FFXIV Character from it's original root object (your character's .fbx file name) to a new root object called 'New MMD Model'

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/8171954b-d271-4a19-8806-cd68412eae7d)


#### TexTools 'Saved' Folder
  
Saved' Folder where TexTools exports all textures and models by default. Used for pulling in extra custom properties details upon .FBX Import:
- Mesh data:  
    - ModelName - Parsed from FFXIV TexTools folder (if folder name found in TexTools 'Saved' Folder)
    - material_filepath - Parsed from FFXIV TexTools folder (if folder name found in TexTools 'Saved' Folder)
        
#### Anamnesis .chara File Read:

Reads the .chara file and outputs to the results to Blender's System Console.

1) DIAGNOSIS: If an armature is selected, it compares the selected armature against the .chara file to see if it has all the correct equipment attached from TexTools. Useful if you made any mistakes exporting gear out of TexTools (such as the wrong equipment)

2) Outputs the following data used for TexTools .fbx export:
    - Skin Color (hex)
    - Hair Color (hex)
    - Hair Highlights Color (hex) If hair highlights is disabled, will output the hair color
    - Iris Color (hex)
    - Lip/Fur Color: (hex)
    - Tattoo/Limbal Color: (hex)
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
    
    
#### Anamnesis .chara File Apply To Model:
 
In addition to above, also:
 
1) Adds .chara file custom properties to the armature object:
    

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
 
3) Applies the Facial Deformation Shape Keys (shp_brw_a, etc) to the _all_ the meshes attached to the selected armature with a matching shape key name by setting the values to 1.0
 
4) Adds the FFXIV Race's MMD Facial Expression Bone Morphs (eye blink, smile, etc.) to the model (only works if the model has been converted to MMD Format)

#### Color Swatches

Various colors displayed for the colors from the .chara file. Color Swatches are based on the [FFXIV Color Hex Reference Guide](https://docs.google.com/spreadsheets/d/18Z1ph1Xa-rFvC8FtB7X6IgSbjwPAom5XuDuCtVeNRvo). 

Displays for:
- Skin - Colors vary depending on the Race, Tribe and Gender of the what is in the .Chara file 
- Hair - Colors vary depending on the Race, Tribe and Gender of the what is in the .Chara file 
- Hair Highlights
- Limbal Ring (colored circle around the Iris for Au Ra characters) 
- Lips / Fur (for Hrothgar chracters)
- Face Paint
 
# Language and Translation

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/2705ac60-cca6-4ace-bd53-6db4a3c239b0)


## Mass Rename Bones

Used to rename bones according to the [Bone Dictionary table](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_dictionary.csv) and [Finger Bone Dictionary table](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_fingers_dictionary.csv) . If bone name in 'From' match found on the selected armature, bone will be renamed to the 'To' target bone name.


## Blender to MMD Jap

Will push the Blender Bone name to the MMD Tool's PMX Japanese Bone name (found in the Bone Properties -> **MMD Bone Tools** panel), assuming the MMD Tools application is installed in Blender.

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/af6885ba-63cd-4e0e-9e31-bf15e0c6455c)
 
## Swap Jap / Eng

Swaps the MMD (PMX) Japanese and MMD (PMX) English bone names, shape key names, and material names. Useful if you're in the MMD-only workflow


## Bones and IK
![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/1fcd5396-ca1b-40bd-9056-7a144297acf3)

### Visibility Shortcuts

Shortcuts to the standard visibility options found on **Armature** -> **Viewport Display** panel:

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/793ed8c3-755c-4c2e-8308-1213454cdf3d)

- Hide/Show bones
- Hide/Show bone names
- Show bones in front of all other objects
- Display bones as:
    - Octahedral
    - Stick
    - Envelope
    - B-Bone
    - Wire
- Hide/Show armature (shortcut to the **MMD Tools** hide/show armature button, assuming the model has been converted to MMD Model format):

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/71e10b43-b181-46b9-bc40-5cdbb10ad650)

### MMD Conversion

Various steps to add/remove certain bones to MMD Format. _NOTE: Bones must be renamed from 'FFXIV' to 'MMD English' format for most of these to work._

#### Run Steps 1 to 12 - Shortcut to running steps 1 to 12 in order
#### 1  -  Remove unused bones (no vertex groups)
Removes any bones without any meshes attached. Useful since the stanard FFXIV bone struture the is imported includes bones even when there are no meshes attached to it. Removing them makes the armature cleaner / easier to see in Blender
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
Adjusts the standard FFXIV Bone lengths and positions to be closer to a standard MMD model. THIS IS NOT PERFECT, but it definitely helps. I still haven't figured out the exact position in order to get VMD files to animate the arms 100%. If there are issues upon importing a VMD file, refer to this [FAQ question](https://github.com/wikid24/ffxiv_mmd_tools_helper/tree/master#q-when-i-play-an-animation-the-arms-dont-line-up-exactly-to-the-animation-or-clipcollide-into-the-headbodyother-hand-at-certain-parts-how-do-i-fix-this).
#### 8  -  Add Eyes Control Bone
Adds the special MMD 'Eyes' controller bone that is used to control 'eye_L' and 'eye_r' at the same time. Applies rotation to both bones
#### 9  -  Add Arm Twist Bones
Adds the special MMD 'arm_twist_1','arm_twist_2','arm_twist_3', 'wrist_twist_1', 'wrist_twist_2', 'wrist_twist_3' twist bones, for additional arm fine-tuneing for animations. Needed for some VMD animation files. 
#### 10 -  Add Shoulder Control Bones
Adds the special MMD 'should_C','shoulder_P' bones. Needed for some VMD animation files. 
#### 11 -  Add Leg/Foot IK
Adds the 'stanard' MMD Leg/Foot IK Bones:
- leg IK_root_L
- leg IK_root_R
- leg IK_L
- leg IK_R
- toe IK_L
- toe IK_R
And also adds the 'special' MMD Control bones (used to move the meshes in certain direction _after_ IK is applied, since once IK is applied, you can no longer directly move the pose bone like you would with a non-IK bone)
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
Fixes the MMD Japanes & English PMX Bone names (while not changing the Blender Bone Name) to their MMD Japanese equivalent. Useful so that you can import a VMD animation file using the MMD Japanese (PMX) bone name without needed to read Japanese in Blender :P
#### 13 -  Add Hand/Arm IK
Adds some IK to hands/arms, similar to Leg/IK. Unlike Leg/Arm IK, this one is rarely if ever used in a VMD motion file, and is recommended that you don't use it unless it is actually called for. 
#### 14 - Add Extra Finger Bones (select finger mesh first)
Added a third finger bone (the last bone tip of a finger) to FFXIV models, since they only have 2 finger bones. Script will attempt to automatically weight paint the bones, but it is hit or miss. I'd avoid doing this unless you like weight painting manually. Ensure that the hand mesh is selected first _before_ running this command.
#### 15 - Add Extra Breast Tip Bones
Will add an extra bone tip to the breasts bones (j_mune_l, j_mune_r) to match some other similar looking MMD Models, though it is not needed in Blender. Only useful if you're planning to export to PMX format and continue rigging using PMX Editor.
#### 16 - Merge Double-Jointed Knee (FFXIV PMX Export Only)
Since most standard MMD Models don't have these 'double-jointed' knees, this will merge the FFXIV- 'j_asi_c_l' and 'j_asi_b_l'(or Knee_L if you've renamed the bone) bones into one, and attempt merging the weight painting into the newly merged bone.  Only useful if you're planning to export to PMX format and continue rigging using PMX Editor, otherwise if you're planning on staying in Blender, stick with the double-jointed knee to avoid extra headache.
#### EXPERIMENTAL - Adjust Arm Position for FFXIV Models
Attempt to adjust the should/arm/elbow bone postitions further to align with a stanard MMD Model. Sometimes it works and solves all the related arm motion problems, sometimes it doesn't. I can't seem to find a proper solution that will 100% work 100% of the time :S

### Find & Replace

#### Find 
Will search for any bone of the selected armature (in edit mode or pose mode) containing the search text provided

#### Replace
Combined with the find textbox, will rename any found bones to the new name provided

#### Selected only checkbox
Will limit the 'replace' to only _selected_ bone

### Bone Groups

#### Auto Generate
Will add the armature's bones to the Blender's **Armature -> Bone Groups** panel, according to the [metadata bone group dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_metadata_ffxiv_dictionary.csv). If bone name is found matched in the 'mmd_english',	'mmd_japanese',	'mmd_japaneseLR', 'blender_rigify', or 'ffxiv' columns, will add the bone to the bone group specified in the 'blender_bone_group' column
