# 3D Viewport -> Sidebar

## FFXIV MMD -> Import FFXIV Model

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/80e3a3ba-cd96-4897-a73e-b82bfe8b11eb)


### Import FFXIV .fbx File

- Imports a FFXIV Model into Blender
    - primary_bone_axis='X'
    - secondary_bone_axis='Y'
    - use_manual_orientation=True
    - axis_forward='Y'
    - axis_up='Z'

- Moves all 'Group' objects to an empty object called 'FFXIV Empty Groups'
- Fixes the alpha blend mode so that all the textures can be viewed properly (blend_method = 'HASHED')
- Adds the"mmd_bone_order_override" armature modifier to the FIRST mesh on n_root (as per the MMD Tools instructions)
- Adds custom object/data properties:
    - Armature object:
        - original_root_name (needed because MMD Tools moves the armature to a new object called 'New MMD Model')    
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
        
 - Renames the meshes objects to something that is more human-readable
 
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
 
2) Applies the Facial Deformation Shape Keys (shp_brw_a, etc) to the selected armature by setting them to 1.0
 
3) Adds the FFXIV Race's MMD Facial Expression Bone Morphs (eye blink, smile, etc.) to the model (only works if the model has been converted to MMD Format)

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

Used to rename bones according to the Bone Dictionary table. If bone name in 'From' match found on the selected armature, bone will be renamed to the 'To' target bone name

## Blender to MMD Jap

Will push the Blender Bone name to the MMD Tool's PMX Japanese Bone name (found in the Bone Properties -> **MMD Bone Tools** panel), assuming the MMD Tools application is installed in Blender.

![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/af6885ba-63cd-4e0e-9e31-bf15e0c6455c)
 
## Swap Jap / Eng

Swaps the MMD (PMX) Japanese and MMD (PMX) English bone names, shape key names, and material names. Useful if you're in the MMD-only workflow


# Bones and IK
![image](https://github.com/wikid24/ffxiv_mmd_tools_helper/assets/19479648/1fcd5396-ca1b-40bd-9056-7a144297acf3)

## Visibility Shortcuts

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

## MMD Conversion

Various steps to add/remove certain bones to MMD Format

- Run Steps 1 to 12 - Shortcut to running steps 1 to 12 in order
- 

