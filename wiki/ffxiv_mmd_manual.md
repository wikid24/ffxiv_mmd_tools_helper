# 3D Viewport -> Sidebar

## FFXIV MMD -> Import FFXIV Model

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
 
 3) Adds the MMD Facial Expression Bone Morphs (eye blink, smile, etc.)  to the model (only works if the model has been converted to MMD Format)
 
 
 
 
 