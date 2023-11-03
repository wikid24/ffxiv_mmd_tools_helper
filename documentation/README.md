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

- Update all material properties:
    - Fixes the alpha blend mode so that all the textures can be viewed properly (blend_method = 'HASHED')
    - Turns on backface culling (use_backface_culling = True)

- Update meshes:
    - Adds the"mmd_bone_order_override" armature modifier to the FIRST mesh on n_root (as per the [MMD Tools instructions](https://mmd-blender.fandom.com/wiki/MMD_Tools/Manual#mmd_bone_order_override))
    - Renames the meshes objects to something that is more human-readable

- Adds custom object/data properties:
    - Armature **object**:
        - original_root_name (MMD Tools moves the armature to a new object called 'New MMD Model' upon converting it, so it's useful to know the original name sometimes)    
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
     
    ![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/81be8212-ce57-4a19-ad65-c2119be822a1)

 
3) Applies the Facial Deformation Shape Keys (shp_brw_a, etc) to the _all_ the meshes attached to the selected armature with a matching shape key name by setting the values to 1.0. Values are mapped in the [Chara File Dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/chara_file_dictionary.csv)

   ![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/7c260f02-acba-4571-ba7b-f2e5cd4c7000)

 
5) Adds the FFXIV Race's MMD [Facial Expression Bone Morphs ](https://github.com/wikid24/ffxiv_mmd_tools_helper/tree/master/documentation#bone-morphs-facial-expressions) (eye blink, smile, etc.) to the model (only works if the model has been converted to MMD Format). 

   ![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/7146a3b1-a699-40c1-a9f3-d96dd49b806b)



#### Color Swatches

Various colors displayed for the colors from the .chara file. Color Swatches are based on the [FFXIV Color Hex Reference Guide](https://docs.google.com/spreadsheets/d/18Z1ph1Xa-rFvC8FtB7X6IgSbjwPAom5XuDuCtVeNRvo). 

Displays for:
- [Skin](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_skin_dictionary.csv) - Colors vary depending on the Race, Tribe and Gender of the what is in the .Chara file 
- [Hair](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_hair_dictionary.csv) - Colors vary depending on the Race, Tribe and Gender of the what is in the .Chara file 
- [Hair Highlights](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_hairhighlights_dictionary.csv)
- [Eyes](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_eye_dictionary.csv)
- [Tattoo / Limbal Ring](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_tattoo_limbalring_dictionary.csv) (colored circle around the Iris for Au Ra characters) 
- [Lips / Fur (for Hrothgar chracters)](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_lips_dictionary.csv)
- [Facepaint](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/color_facepaint_dictionary.csv)

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

And also adds the 'special' MMD Control bones (used to move the meshes in certain direction _after_ IK is applied, since once IK is applied, you can no longer directly move the pose bone like you would with a non-IK bone):
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

Shortcut to the button in 'Export

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

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/c07eeed1-8a29-41e8-a027-8faf496404ba)


## Rigid Bodies

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/c739e6f2-d242-4135-ae82-e810b802a4fc)

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

### Active Rigid Body / Bone

Show the actively selected Rigid body's name, as well as it's connected bone's name. Clicking on the bone name will select the bone in edit mode

### Rigid Body Search

Searches for rigid body name(s) based on the parameters provided (starts /w, contains, ends/w)

- 'Find' will deselect all selected objects first before showing the results
- 'Find + Add' is the same as 'Find' but will append the results to the currently selected objects
- 'Trashcan' will clear the 'starts w/', 'contains', and 'ends w/' textboxes

### Bone Chain Select

#### Up
Based on the 'active' rigid body selected's **bone**, will append the bone's parent's rigid bodies recursively. Useful if you want to apply change in bulk to all the rigid bodies attached to the bones

#### Down
Same as 'Up', but looks for the bone's children recusively.

#### All
It does both 'Up' and 'Down' at the same time

### Skirt Select

#### Vertical Skirt Selection

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/0fa35b5e-cc6e-4d1b-a8aa-8a0620ba4e1e)

When the [skirt module](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation/README.md#skirt) is leveraged to create rigid bodies, will select all vertical skirt rigid bodies from the active selection (based on the rigid body object name 'skirt_x_y', it will select any rigid bodies that match the currently active x)

#### Horizontal Skirt Selection

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/a420790d-c875-4c2e-acaa-b089696a2af3)


When the [skirt module](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation/README.md#skirt) is leveraged to create rigid bodies, will select all horizontal skirt rigid bodies from the active selection (based on the rigid body object name 'skirt_x_y', it will select any rigid bodies that match the currently active y)

#### All Skirt Selection

When the [skirt module](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation/README.md#skirt) is leveraged to create rigid bodies, will select all rigid bodies (based on the rigid body object name 'skirt_x_y', it will select any rigid bodies that match the the name 'skirt_')


### Rigid Body Transform

https://user-images.githubusercontent.com/19479648/225210461-c10581d3-ff3d-4fb8-92d8-1bed41de3dac.mp4

#### Bulk Apply Rigid Bodies
Used to apply changes to ALL selected rigid bodies. 

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/dc4f98da-7e11-41e4-8be7-62895cbdb552)

By default it will show the values on the ACTIVE rigid body.

Selecting a checkbox will apply that specific parameter to all selected rigid bodies.

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

#### All Rigid Body Bone Chains
![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/e0800c28-922b-4b8c-a64a-396ed7bde7c5)

Same as above but applies the values to ALL selected rigid body bone chains. Since each rigid body bone chain has it's own unique start and end value, this doesn't use the 'absolute' values, but rather applies a delta value based on the inputs.

### Rigid Body Create

#### From Selected Bones
Shortcut to the MMD Tools' Rigid Body Create button:
![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/9ed7ece8-3eb2-4ae8-b7cc-ece5b16bedca)

#### From FFXIV Template
Creates a Rigid Body skeletion based on the FFXIV general bone body structure, with all these presets created.
To see the preset values applied to each bone and the values, check out the [Rigid Body Dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/rigid_body_dictionary.csv)

## Joints

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/2be9f179-7797-4f8e-b235-f6a626a6bd21)

TBD

### Visibility Shortcuts

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/a7982deb-ef97-46e5-ac36-3bb376518b09)

Shortcuts to the MMD Tools show/hide joint, and show/hide joint name respectively.

#### Active Joint / Rigid 1 / Rigid 2

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/69dd9c14-c279-4a79-95ac-9922db8cdc6b)

When a joint is selected, will show the joint name, as well as its two associated rigid bodies. Clicking on the rigid body name will select it.

#### Get Joints from Rigid Bodies

When there are **multiple** rigid bodies selected, will scan the armature for **all** the associated joints that are connecting them and select the joints.

#### Vertical Select

When there are **multiple** joints selected, will scan for any rigid bodies that are connected in a **rigid body bone chain** ([see explanation](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation/README.md#rigid-body-bone-chain)) (meaning they are vertically connected) and filter the selection to ONLY these joints.

#### Horizontal Select

When there are **multiple** joints selected, will scan for any rigid bodies that are NOT connected in a **rigid body bone chain** ([see explanation](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation/README.md#rigid-body-bone-chain)) (meaning they are horizontally connected) and filter the selection to ONLY these joints.



### Joint Transform

Used to apply bulk changes to multiple selected joints. By default, all of the fields will be populated with the currently **active** joint.

To apply changes, input a value to one of the properties, select the checkbox next to it and press 'OK'

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/402f9c24-7238-469d-af5e-6583fbf78cb9)


### Joint Create

#### From Selected Rigid Bodies

Will create joints in bulk when there are 2 or more selected rigid bodies selected. **BUG: Currently only creates multiple joints when they are connected in a rigid body bone chain (meaning, it is a vertical joint). ** This is a MMD Tools bug.

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/70c0013d-5efe-4613-b0ba-c4cdca2405fe)


#### Create Vertical Joints

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/a7236bfa-bb3a-4f97-a275-2df7e36da535)


Create joints in bulk where there are **multiple** **rigid body bone chains** ([see explanation](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/documentation/README.md#rigid-body-bone-chain) selected, with only joints being created between rigid bodies that have a bone parent & child relationship, with  the option to create a joint for each bone chain's highest parent to a common rigid body that is shared between tham  (such as selecting all the hair rigid bodies and pinning the highest rigid body in each bone chain to the "head" rigid body)

Please be aware that this means that ONLY joints will be created between a rigid body bone's parents and children, meaning that there will be NO joints created between two separate bone chains. To create joints in bulk where there is no bone parent/child relationship refer to the Create Horizontal Joints section below.

Sample video:

https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/649d0ff4-9024-4e59-8fc1-6d05f855fe16

#### Create Horizontal Joints

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/73a80223-0233-46e6-af55-0ab3d05d3f3e)


Create joints in bulk where there are **multiple** **rigid body bone chains** selected, however there is no hierarchal parent/child relationship between the bones. To do this, all rigid bodies need to share a 1) a common name AND and two numbers in the same position.

**Example rigid body name:** skirt_0_1
- **common name pattern shared on all rigid bodies:** skirt_
- **first number**: 0
- **second number** 1

The search criteria (starts w/, contains, ends w/) will specify the **scope** of rigid bodies that need horizontal joints, will need to use the common name pattern to do so upon pressing 'find'.

Upon pressing 'Find', the search results will:
1) Show ALL rigid bodies that contain that common name pattern-- this becomes the scope of rigid bodies that will create  horizontal joints for
2) Show (at minimum) **two** numbers that will indicate if eveything that shares that same number is a 'horizontal' rigid body chain. The two numbers provided will be based on a rigid body within the search scope at random

Upon selecting one of the two (or more) numbers, a box will be displayed with a **<--previous ** and **next -->** button on it

These two arrows will be used to iterate through **all** the  rigid bodies in the search scope that share that same number's position in the rigid body name. This is for **testing** if the correct number position is selected (either the first number or second number in this example.

'Connect ending and starting rigid body' checkbox is to determine if the **starting** rigid body is supposed to have a joint to the **ending** rigid body. If unchecked, no joint will be created between them. This is useful if the selected rigid bodies are supposed to form a **full** circle horizontally, or not.

Upon pressing 'OK' the horizontal joints will be created.

Sample video:


https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/bf936ddc-c184-42f4-8665-4cf670857cbd





# Bone Morphs (Facial Expressions)

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/168df871-2fa1-4e3f-9e5b-fdd808369f44)


Bone Morphs defines how much each posebone should move in order to make a facial expression.

In Blender's MMD Tools, these bone morphs are made by manually adjusting a model's pose bone's rotation on the X/Y/Z axis, or offsetting their location on the X/Y/Z axis. For example, how many degrees an eyelid bone should rotate down on the Z axis in order for a model to wink. These location/rotation offsets are then stored in a 'Bone Morph', with the value of 1 meaning that the pose bones are 100% applied, and 0 meaning 0% of it is applied (the bone is at it's original rest position).

Typically these pose bones are grouped together to make a Bone Morph. For example a 'blink' bone morph is a combination of both the left _and_ right eyelid bones together.

The facial expressions that are commonly used by MMD animation files are referenced on this [MMD Facial Expression Reference Chart](https://www.deviantart.com/xoriu/art/MMD-Facial-Expressions-Chart-341504917). We cannot reproduce everything on the reference chart since this plugin doesn't add any 'new' data into the FFXIV model (such as adding the 'heart' eyes or the 'star' eyes, as those special shapes doesn't exist on the standard model.

- [Bone Morph Master List](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bone_morph_list.csv) - Defines the overall 'list' of Bone Morphs that are useable by each FFXIV race, as well as the japanese / english names that are used by VMD motion files for animation:

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

#### Change Rotation Mode

Change the rotation mode of the facial pose bones. By default, all pose bones are rotated in quaternion (XYZ+W), which is very difficult to work with. 
By changing rotation mode to 'XYZ Euler', it becomes much easier to manually adjust the pose bones, in order to make your own bone morphs / facial expressions, or when adjusting the ones that come built into this plugin.

## Skirt

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/3d688d98-760b-4585-9c5c-3a64ea6bad4c)

### Generate a New Skirt Object

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/4a467464-f863-4893-956a-2710bda954d5)

This will create a skirt object called 'skirt_obj' with it's own cone-shaped mesh called 'new_skirt_shape', and cone-shaped armature with all the included bones under 'new_skirt_arm'.

- The cone-shaped bones are intended to be your new skirt's bones for using leveraging MMD-style physics with rigid bodies & joints. These skirt bones will be transferred to your model once this whole skirt transfer process is complete.
- The cone-shaped mesh will have **weight painted pre-applied** to the bones from the cone-shaped armature. This cone-shaped mesh needed in order to perform a 'weight paint transfer' from this cone to your model's current skirt mesh to use it's weight painting. This skirt will be **deleted** once this whole skirt transfer process is complete as it is only needed for the weight paint transfer to your model.

The paramaters are as follows:

- Bone Chains: Specifies the number of bone chains that will encircle the circumference of your model. For example specifying '4' will have a bone chain starting on your model's left side, back, right side, and front.
- Bone Chain Children: Specifies how many bones will be added for each bone chain from the top of the skirt to the bottom of the skirt.
- Mesh Segments: Specifies how 'round' the circumference of your skirt mesh will be. Specifying a higher number will add more verticies to the circumference your skirt. Lower numbers will make your skirt object look like it was made in Quake
- Mesh Subdivisions: Specifies how many face subdivisions should be on the cone-shaped mesh. The higher the number, more faces will be on your mesh, and the more accurate/detailed the weight painting will be.
- Top Height: Specifies the XYZ's coordinate height of the **top** of the skirt from 0. Ideally this should be placed where you expect the new skirt's weight painting to be transferred onto your model
- Top Radius: Specifies how large/small the **top** of your skirt is
- Bottom Height: Specifies the XYZ's coordinate height of the **bottom** of the skirt from 0.
- Bottom Radius: Specifies how large/small the **bottom** of your skirt is

Upon pressing 'OK', it will create the skirt_obj and **remember** the parameters upon the next time you press the 'OK' button. **IT IS PERFECTLY FINE TO PRESS 'OK' EVEN IF YOU STILL WANT TO MAKE CHANGES** because every single time you press the OK button, it will **replace** the current skirt_obj with a **new** skirt object




### Move Mesh To New Skirt Object

TBD

### Weight Paint Transfer to Mesh

TBD

### Delete FFXIV & Unused Skirt Vertex Groups

TBD

### Move Bones and Meshes to Armature

TBD

### Generate Skirt Rigid Bodies

TBD

### Generate Skirt Joints

TBD

### Vertex Group List

TBD


TBD

## Shaders

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/b8d83fe0-48e1-45a9-962a-a8da9f082cf9)

TBD

### Texture Folder

TBD

### Apply Colorset

TBD

### Active Material

TBD

### Apply Glossy Shader

TBD

### Glossy Roughness Slider

TBD

## Miscellaneous Tools

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/9d8b80fa-e774-4a16-b748-1382483f5bed)

### Dropdown List

TBD

### Bust Slider

TBD

## Export MMD Preparation

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/54d3a8a5-861d-4bf7-b411-46ffe8cdde9f)

TBD

### Auto-Fix MMD Japanese / English Bone Names

Fixes the MMD Japanes & English PMX Bone names (while not changing the Blender Bone Name) to their MMD Japanese equivalent. Useful so that you can import a VMD animation file using the MMD Japanese (PMX) bone name without needing to read Japanese in Blender :P.

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/af6885ba-63cd-4e0e-9e31-bf15e0c6455c)

Leverages the [metadata bone group dictionary](https://github.com/wikid24/ffxiv_mmd_tools_helper/blob/master/ffxiv_mmd_tools_helper/data/bones_metadata_ffxiv_dictionary.csv) to do the PMX Bone group mapping. If Blender bone name is found matched in the 'mmd_english',	'mmd_japanese',	'mmd_japaneseLR', 'blender_rigify', or 'ffxiv' columns, will add the 'mmd_english',	'mmd_japanese' bone name MMD Tool's PMX Japanese/English Bone name fields respectively (found in the Bone Properties -> **MMD Bone Tools** panel). If no match is found, and the PMX field is empty, it puts the Blender bone name verbatim so at least the MMD field is not empty and has a name.

### Add Display Panels

TBD

### Sort Bone Order / Deform Tools

TBD

### Lock Position & Rotation

TBD

### Set Fixed Axis / Local Axis

TBD

### High Special & Physics Bones

TBD
