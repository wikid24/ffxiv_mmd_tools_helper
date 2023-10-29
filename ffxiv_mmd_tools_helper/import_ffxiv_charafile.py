import bpy
from . import register_wrap
from . import import_csv
from . import bone_conversion
import mmd_tools.core.model as mmd_model
import json
import math


def add_custom_property(obj,prop_name,prop_value):
	obj.data[prop_name] = prop_value

def parse_chara_file(file_path):
	
	# Open and read the JSON file
	with open(file_path, 'r') as file:
		# Store the results in a dictionary
		charafile_data = json.load(file)

	
	# Define CHARAFILE_DICTIONARY containing the list of keys to check
	CHARAFILE_KEYS = {
		#faceshape shapekey stuff
		'Eyes',
		'Eyebrows',
		'Mouth',
		'Nose',
		'Jaw',
		#body type stuff
		'ObjectKind',
		'Race',
		'Tribe',
		'Gender',
		'Head',
		'Hair',
		'TailEarsType',
		'Bust',
		'EnableHighlights',
		#gear
		'HeadGear',
		'Body',
		'Hands',
		'Legs',
		'Feet',
		#accessories
		'Ears',
		'Neck',
		'Wrists',
		'LeftRing',
		'RightRing',
		#Colors
		'Skintone',
		'HairTone',
		'Highlights',
		'LimbalEyes',
		'REyeColor',
		'LipsToneFurPattern',
		'FacePaintColor',
		#random stuff
		'SkinGloss',
		'BustScale',
		'FacialFeatures'
	}

	# Create a dictionary to store the results
	result_dict = {}

	# Loop through charafile_data to find only matching data from CHARAFILE_KEYS
	for charafile_key in CHARAFILE_KEYS:
		for key in charafile_data:
			if charafile_key == key:

				#if value for some of these keys >= 128, then subtract 128 
				#values higher than 128 is a modifier for some checkboxes in Anamnesis
				#for example if Eyes=128, then Eyes is actually '0' and the 'Small Iris' checkbox is checked in Anamnesis
				#don't ask me why it's coded this way, it's just weird AF
				if key in ['Eyes', 'Eyebrows', 'Mouth', 'Nose', 'Jaw']and int(charafile_data[key]) >=128:
					result_dict[key] = int(charafile_data[key]) - 128
					if key == 'Eyes':
						result_dict['SmallIris'] = 1
						print ("SmallIris:" + str(result_dict['SmallIris']))
				if key in ['HeadGear','Body','Hands','Legs','Feet','Ears','Neck','Wrists','LeftRing','RightRing']:
					result_dict[key] = int(charafile_data[key]['ModelBase'])
				else:
					result_dict[key] = charafile_data[key]


	return result_dict

def apply_face_shape_keys(result_dict):

	CHARAFILE_DICTIONARY = import_csv.use_csv_charafile_dictionary()

	#loop thorough CHARAFILE_DICTIONARY to find values that match charafile_data
	reset_all_shape_keys()
	for key, value in result_dict.items():
		for row in CHARAFILE_DICTIONARY:
			if key == row[0] and str(value) == (row[1]):
				#print (f"{row[0]}:{row[1]}:{row[2]}")
				if row[2] != '':
					#turn on all shape keys that match the results
					enable_shape_keys(row[2])
					print ('shape_key:' + row[2] + " set to 1")


def apply_face_bone_morphs(result_dict):
	
	
	if result_dict['Race'] == 'Hyur':
		bpy.context.scene.bone_morph_ffxiv_model_list = "hyur"
	elif result_dict['Race'] == 'Elezen':
		bpy.context.scene.bone_morph_ffxiv_model_list = "elezen"
	elif result_dict['Race'] == 'Lalafel':
		bpy.context.scene.bone_morph_ffxiv_model_list = "lalafell"
	elif result_dict['Race'] == 'Miqote':
		bpy.context.scene.bone_morph_ffxiv_model_list = "miqote"
	elif result_dict['Race'] == 'Roegadyn':
		bpy.context.scene.bone_morph_ffxiv_model_list = "roegadyn"
	elif result_dict['Race'] == 'Hrothgar':
		bpy.context.scene.bone_morph_ffxiv_model_list = "hrothgar"
	elif result_dict['Race'] == 'AuRa':
		bpy.context.scene.bone_morph_ffxiv_model_list = "aura"
	elif result_dict['Race'] == 'Viera':
		bpy.context.scene.bone_morph_ffxiv_model_list = "viera"
	else:
		bpy.context.scene.bone_morph_ffxiv_model_list = "none"

	
	obj = bpy.context.active_object
	root = mmd_model.Model.findRoot(obj)

	if obj and obj.type == 'ARMATURE' and root:
		if bpy.context.scene.bone_morph_ffxiv_model_list != "none" :
			bpy.ops.ffxiv_mmd.add_bone_morphs()
		else:
			print("Bone Morphs not applied since we couldn't determine the character's FFXIV Race")
	else:
		print("Bone Morphs not applied since this has not been converted into an MMD Model")
	
def diagnose_meshes_against_charafile(CHARAFILE,armature=None):

	if armature:
		results = True

		chara_prop_mapping = [
			["Head","e","met","HeadGear",],
			["Body","e","top","Body",],
			["Hands","e","glv","Hands",],
			["Legs","e","dwn","Legs",],
			["Feet","e","sho","Feet",],
			["Earrings","a","ear","Ears",],
			["Neck","a","nek","Neck",],
			["RingL","a","ril","LeftRing",],
			["RingR","a","rir","RightRing",],
			["Wrists","a","wrs","Wrists",],
			["Face","f","fac","Head",],
			["Hair","h","hir","Hair",],
			["Tail","t","til","TailEarsType",],
			["Ears","z","zer","TailEarsType",],

			]

		meshlist = {}

		#loop through all meshes in armature, check the custom properties and add to the meshlist
		for obj in armature.parent.children_recursive:
			if obj.type == 'MESH':
				#check if the custom properties were added
				if 'ModelID' in obj.data and 'ModelType' in obj.data:
					model_type = obj.data['ModelType']
					model_number_id = obj.data['ModelNumberID']
					model_id = obj.data['ModelID']
					#meshlist[model_type] = model_number_id
					meshlist[model_type] = (model_number_id, model_id)
					
		print('----------------')
		print('DIAGNOSIS:')
		for i in meshlist:
			#print(i,":",meshlist[i][0])
			
			for prop in chara_prop_mapping:

				#check if i is on the chara_prop_mapping table        
				if i == prop[0]:        

					chara_prop = prop[3]
					#check if prop[3] is in the CHARAFILE
					if chara_prop in CHARAFILE:
						chara_prop_value = CHARAFILE[chara_prop]		
						if meshlist[i][0] == chara_prop_value:
							#print(f"{i} : {meshlist[i][1]} mesh matches the chara file")
							break
						else:
							print(f"{i} : {meshlist[i][1]} mesh DOES NOT MATCH the chara file {prop[3]}: {CHARAFILE[chara_prop]}")
							results = False
							break
					else:
						print(f"{i} : {meshlist[i][1]} does not exist in the chara file")

		
		if results == True:
			print("ALL meshes from armature match the chara file!")

		print('----------------')
		

		return results
	else:
		print("DIAGNOSIS: To check if armature matches chara file, select an armature first")


def reset_all_shape_keys():
	# Get the currently selected armature
	selected_armature = bpy.context.active_object

	if selected_armature and selected_armature.type == 'ARMATURE':
		# Create a list to store the meshes that are children of the armature
		child_meshes = []

		# Iterate through all objects in the scene
		for obj in bpy.context.scene.objects:
			if obj.type == 'MESH' and obj.parent and obj.parent.type == 'ARMATURE' and obj.parent.name == selected_armature.name:
				child_meshes.append(obj)


		for mesh in child_meshes:
			if hasattr(mesh.data.shape_keys, 'key_blocks'):
				for shape_key_block in mesh.data.shape_keys.key_blocks:
					if shape_key_block.value != 0:
						shape_key_block.value = 0
						print('shape_key:' + shape_key_block.name + ' Mesh: ' + mesh.name + ' Set to 0')

	
def enable_shape_keys(shape_key_name):
	#print (shape_key_name + " is going to be modified!")

	# Get the currently selected armature
	selected_armature = bpy.context.active_object

	if selected_armature and selected_armature.type == 'ARMATURE':
		# Create a list to store the meshes that are children of the armature
		child_meshes = []

		# Iterate through all objects in the scene
		for obj in bpy.context.scene.objects:
			if obj.type == 'MESH' and obj.parent and obj.parent.type == 'ARMATURE' and obj.parent.name == selected_armature.name:
				child_meshes.append(obj)


		# Check for 'shp_nse_c' shape key and set its value to 1 if found
		for mesh in child_meshes:
			if hasattr(mesh.data.shape_keys, 'key_blocks'):
				for shape_key_block in mesh.data.shape_keys.key_blocks:
					if shape_key_block.name == shape_key_name:
						# Set the shape key's value to 1
						shape_key_block.value = 1.0
						#print(f"{shape_key_block.name} is going to be modified!")


def get_color_key(race,tribe,gender):
	
	color_key = None

	color_dictionary = [
		["AuRa","Raen","Masculine","aura_raen_m"],
		["AuRa","Raen","Feminine","aura_raen_f"],
		["AuRa","Xaela","Masculine","aura_xael_m"],
		["AuRa","Xaela","Feminine","aura_xael_f"],
		["Elezen","Duskwight","Masculine","elez_dusk_m"],
		["Elezen","Duskwight","Feminine","elez_dusk_f"],
		["Elezen","Wildwood","Masculine","elez_wild_m"],
		["Elezen","Wildwood","Feminine","elez_wild_f"],
		["Hrothgar","Helions","Masculine","hrot_heli_m"],
		#["Hrothgar","Helions","Feminine","hrot_heli_f"],
		["Hrothgar","TheLost","Masculine","hrot_lost_m"],
		#["Hrothgar","TheLost","Feminine","hrot_lost_f"],
		["Hyur","Highlander","Masculine","hyur_high_m"],
		["Hyur","Highlander","Feminine","hyur_high_f"],
		["Hyur","Midlander","Masculine","hyur_midl_m"],
		["Hyur","Midlander","Feminine","hyur_midl_f"],
		["Lalafel","Dunesfolk","Masculine","lala_dune_m"],
		["Lalafel","Dunesfolk","Feminine","lala_dune_f"],
		["Lalafel","Plainsfolk","Masculine","lala_plai_m"],
		["Lalafel","Plainsfolk","Feminine","lala_plai_f"],
		["Miqote","KeeperOfTheMoon","Masculine","miqo_keep_m"],
		["Miqote","KeeperOfTheMoon","Feminine","miqo_keep_f"],
		["Miqote","SeekerOfTheSun","Masculine","miqo_seek_m"],
		["Miqote","SeekerOfTheSun","Feminine","miqo_seek_f"],
		["Roegadyn","Hellsguard","Masculine","roeg_hell_m"],
		["Roegadyn","Hellsguard","Feminine","roeg_hell_f"],
		["Roegadyn","SeaWolf","Masculine","roeg_seaw_m"],
		["Roegadyn","SeaWolf","Feminine","roeg_seaw_f"],
		["Viera","Rava","Masculine","vier_rava_m"],
		["Viera","Rava","Feminine","vier_rava_f"],
		["Viera","Veena","Masculine","vier_veen_m"],
		["Viera","Veena","Feminine","vier_veen_f"],

	]

	#print(race + ' ' + tribe + ' ' + gender)

	for i in color_dictionary:
		#print (i[0] + i[1]+i[2]+i[3])
		if race==i[0] and tribe == i[1] and gender == i[2]:
			color_key = i[3]
			break
		
	#print (f"color_key={color_key}")

	return color_key


def get_model_race_key(race,tribe,gender):

	race_key = None

	race_dictionary = [
		["AuRa","Raen","Masculine","aura_raen_m","c1301"],
		["AuRa","Raen","Feminine","aura_raen_f","c1401"],
		["AuRa","Xaela","Masculine","aura_xael_m","c1301"],
		["AuRa","Xaela","Feminine","aura_xael_f","c1401"],
		["Elezen","Duskwight","Masculine","elez_dusk_m","c0501"],
		["Elezen","Duskwight","Feminine","elez_dusk_f","c0601"],
		["Elezen","Wildwood","Masculine","elez_wild_m","c0501"],
		["Elezen","Wildwood","Feminine","elez_wild_f","c0601"],
		["Hrothgar","Helions","Masculine","hrot_heli_m","c1501"],
		#["Hrothgar","Helions","Feminine","hrot_heli_f","c1601"],
		["Hrothgar","TheLost","Masculine","hrot_lost_m","c1501"],
		#["Hrothgar","TheLost","Feminine","hrot_lost_f","c1601"],
		["Hyur","Highlander","Masculine","hyur_high_m","c0301"],
		["Hyur","Highlander","Feminine","hyur_high_f","c0401"],
		["Hyur","Midlander","Masculine","hyur_midl_m","c0101"],
		["Hyur","Midlander","Feminine","hyur_midl_f","c0201"],
		["Lalafel","Dunesfolk","Masculine","lala_dune_m","c1101"],
		["Lalafel","Dunesfolk","Feminine","lala_dune_f","c1201"],
		["Lalafel","Plainsfolk","Masculine","lala_plai_m","c1101"],
		["Lalafel","Plainsfolk","Feminine","lala_plai_f","c1201"],
		["Miqote","KeeperOfTheMoon","Masculine","miqo_keep_m","c0701"],
		["Miqote","KeeperOfTheMoon","Feminine","miqo_keep_f","c0801"],
		["Miqote","SeekerOfTheSun","Masculine","miqo_seek_m","c0701"],
		["Miqote","SeekerOfTheSun","Feminine","miqo_seek_f","c0801"],
		["Roegadyn","Hellsguard","Masculine","roeg_hell_m","c0901"],
		["Roegadyn","Hellsguard","Feminine","roeg_hell_f","c1001"],
		["Roegadyn","SeaWolf","Masculine","roeg_seaw_m","c0901"],
		["Roegadyn","SeaWolf","Feminine","roeg_seaw_f","c1001"],
		["Viera","Rava","Masculine","vier_rava_m","c1701"],
		["Viera","Rava","Feminine","vier_rava_f","c1801"],
		["Viera","Veena","Masculine","vier_veen_m","c1701"],
		["Viera","Veena","Feminine","vier_veen_f","c1801"],

	]

	for i in race_dictionary:
		#print (i[0] + i[1]+i[2]+i[3])
		if race==i[0] and tribe == i[1] and gender == i[2]:
			race_key = i[4]
			break
		
	#print (f"race_key={race_key}")

	return race_key



def get_all_color_data(color_key,RESULTS_DICT):

	color_skin_dictionary=import_csv.use_csv_color_skin_dictionary()
	color_hair_dictionary=import_csv.use_csv_color_hair_dictionary()
	color_hairhighlights_dictionary=import_csv.use_csv_color_hairhighlights_dictionary()
	color_tattoo_limbalring_dictionary=import_csv.use_csv_color_tattoo_limbalring_dictionary()
	color_eye_dictionary=import_csv.use_csv_color_eye_dictionary()
	color_lips_dictionary=import_csv.use_csv_color_lips_dictionary()
	color_facepaint_dictionary=import_csv.use_csv_color_facepaint_dictionary()
	
	#print(f"{color_key}, {RESULTS_DICT['Skintone']}")

	color_hex_data = {}

	color_hex_data['skin'] = get_color_from_dictionary(color_key, RESULTS_DICT['Skintone'], color_skin_dictionary)
	color_hex_data['hair'] = get_color_from_dictionary(color_key, RESULTS_DICT['HairTone'], color_hair_dictionary)
	color_hex_data['hair_highlights'] = get_color_from_dictionary("hair_highlights", RESULTS_DICT['Highlights'], color_hairhighlights_dictionary)
	color_hex_data['tattoo_limbal'] = get_color_from_dictionary("tattoo_limbal", RESULTS_DICT['LimbalEyes'], color_tattoo_limbalring_dictionary)
	color_hex_data['eyes'] = get_color_from_dictionary("eye", RESULTS_DICT['REyeColor'], color_eye_dictionary)
	color_hex_data['lips'] = get_color_from_dictionary("lips", RESULTS_DICT['LipsToneFurPattern'], color_lips_dictionary)
	color_hex_data['facepaint'] = get_color_from_dictionary("face_paint", RESULTS_DICT['FacePaintColor'], color_facepaint_dictionary)

	return color_hex_data
	
	
def get_color_from_dictionary(color_key, color_index, dictionary):

	header_row = dictionary[0]
	color_index_column=None
	color_key_column=None
	color_hex_value=None

	#search the header row for column numbers for the color_key & color_index
	for i,cell_value in enumerate(header_row):
		if cell_value=='index':
			color_index_column=i
		if cell_value==color_key:
			color_key_column=i

	

	#print(f"color_key:{color_key}")
	#print(f"color_index:{color_index}")
	#print(f"color_index_column:{color_index_column}")
	#print(f"color_key_column:{color_key_column}")

	#search the entire dictionary for a row that has these two matching values
	for i in dictionary[1:]:
		if int(i[color_index_column]) == int(color_index):
			color_hex_value=i[color_key_column]

	#print(f"color_hex_value={color_hex_value}")
	return color_hex_value

# Function to convert Hex to RGB + A
def hex_to_rgba(hex_color):
	
	if hex_color is not None:

		hex_color = hex_color.lstrip('#')
		r_srgb = int(hex_color[:2], base=16) / 255
		r_linear = convert_srgb_to_linear_rgb(r_srgb)
		g_srgb = int(hex_color[2:4], base=16) / 255
		g_linear = convert_srgb_to_linear_rgb(g_srgb)
		b_srgb = int(hex_color[4:6], base=16) / 255
		b_linear = convert_srgb_to_linear_rgb(b_srgb)
		a = 1.0  # Set alpha to 1.0 (fully opaque) or adjust as needed
		
		#return (r_srgb, g_srgb, b_srgb, a)
		return (r_linear, g_linear, b_linear, a)
	
	else:
        # Handle the case when the color is None, for example:
        # You can set a default color or return (0.0, 0.0, 0.0, 1.0) for black
		return (0.0, 0.0, 0.0, 1.0)

def convert_srgb_to_linear_rgb(srgb_color_component):
		if srgb_color_component <=0.04045:
			linear_color_component= srgb_color_component  / 12.92
		else:
			linear_color_component= math.pow((srgb_color_component + 0.055) / 1.055, 2.4)

		return linear_color_component

def add_custom_properties_to_armature (selected_armature,RESULTS_DICT):
	selected_armature = bpy.context.active_object

	if selected_armature and selected_armature.type == 'ARMATURE':
		for key in RESULTS_DICT:
			if key in ('BustScale','SkinGloss'):
				x = [float(x) for x in RESULTS_DICT[key].split(',')]
				add_custom_property(selected_armature,key,x)
			#if key in ('EnableHighlights'):
				#add_custom_property(selected_armature,key,bool(RESULTS_DICT[key]))
			else:
				add_custom_property(selected_armature,key,RESULTS_DICT[key])

def print_textools_data(RESULTS_DICT,color_hex_data):

	#print the export .FBX cheatsheet for textools
	print('TEXTOOLS DATA:')
	print('----------------')
	print(f"Skin Color: {color_hex_data['skin']}")
	print(f"Hair Color: {color_hex_data['hair']}")
	if RESULTS_DICT['EnableHighlights'] == True:
		print(f"Hair Highlights Color: {color_hex_data['hair_highlights']}")
	else:
		print(f"Hair Highlights Color: {color_hex_data['hair']}")
	print(f"Iris Color: {color_hex_data['eyes']}")
	print(f"Lip/Fur Color: {color_hex_data['lips']}")
	print(f"Tattoo/Limbal Color: {color_hex_data['tattoo_limbal']}")
	print('----------------')
	print(f"Race: {RESULTS_DICT['Race']} | Tribe: {RESULTS_DICT['Tribe']} | Gender: {RESULTS_DICT['Gender']}")
	model_race_key = get_model_race_key(RESULTS_DICT['Race'],RESULTS_DICT['Tribe'],RESULTS_DICT['Gender'])
	#print(f"Model Race: {model_race_key}")
	#print(f"Head: {int(RESULTS_DICT['Head']):04}")
	print('----------------')
	

	#body
	
	if int(RESULTS_DICT['Head']) >= 200:
		#only 'special' NPC faces will use the +200s, I think normal NPC's use the regular 0s and 100s, its on a case by case basis tbh
		print(f"Face Model: {model_race_key}f{int(RESULTS_DICT['Head']):04}_fac")
	else:
		if RESULTS_DICT['Tribe'] in ["Midlander","Wildwood","Plainsfolk","SeekerOfTheSun","SeaWolf","Xaela","Raen","Veena","Rava","Helions","TheLost"]:
			print(f"Face Model: {model_race_key}f{int(RESULTS_DICT['Head']):04}_fac")

		elif RESULTS_DICT['Tribe'] in ["Highlander","Duskwight","Dunesfolk","KeeperOfTheMoon","Hellsguard"]:
			print(f"Face Model: {model_race_key}f{int(RESULTS_DICT['Head']+100):04}_fac")


		
	
	print(f"Hair Model: {model_race_key}h{int(RESULTS_DICT['Hair']):04}_hir")
	
	if RESULTS_DICT['Race'] in ['Miqote','Hrothgar','AuRa']:
		print(f"Tail Model: {model_race_key}t{int(RESULTS_DICT['TailEarsType']):04}_til")
	if RESULTS_DICT['Race'] in ['Viera']:
		print(f"Ears Model: {model_race_key}z{int(RESULTS_DICT['TailEarsType']):04}_zer")
	#gear
	print('----------------')
	print(f"Body Gear: e{int(RESULTS_DICT['Body']):04}")
	print(f"Legs Gear: e{int(RESULTS_DICT['Legs']):04}")
	print(f"Head Gear: e{int(RESULTS_DICT['HeadGear']):04}")
	print(f"Hand Gear: e{int(RESULTS_DICT['Hands']):04}")
	print(f"Feet Gear: e{int(RESULTS_DICT['Feet']):04}")
	print('----------------')
	#accessories
	print(f"Earring Gear: a{int(RESULTS_DICT['Ears']):04}")
	print(f"Necklace Gear: a{int(RESULTS_DICT['Neck']):04}")
	print(f"Wrists Gear: a{int(RESULTS_DICT['Wrists']):04}")	
	print(f"Ring Left Gear: a{int(RESULTS_DICT['LeftRing']):04}")
	print(f"Ring Right Gear: a{int(RESULTS_DICT['RightRing']):04}")
	
	# hyur mid m
	# hyur high
	# wild, dusk
	# plains, dunes
	# seek, keep
	# seaw, hells
	# raen, xael
	# heli, lost
	# rava, veena


def main(context,filepath,apply_charafile_to_selected=None):
	print('----------------')
	print (f".chara file: {filepath}")

	obj = bpy.context.active_object
	selected_armature = None

	if obj and obj.type == 'ARMATURE':
		selected_armature = obj

	RESULTS_DICT=parse_chara_file(filepath)

	color_key = get_color_key(RESULTS_DICT['Race'],RESULTS_DICT['Tribe'],RESULTS_DICT['Gender'])
	color_hex_data = get_all_color_data(color_key,RESULTS_DICT)
	context.scene.color_skin = hex_to_rgba(color_hex_data['skin'])
	context.scene.color_hair = hex_to_rgba(color_hex_data['hair'])
	context.scene.color_hair_highlights = hex_to_rgba(color_hex_data['hair_highlights'])
	context.scene.color_tattoo_limbal = hex_to_rgba(color_hex_data['tattoo_limbal'])
	context.scene.color_eyes = hex_to_rgba(color_hex_data['eyes'])
	context.scene.color_lips = hex_to_rgba(color_hex_data['lips'])
	context.scene.color_facepaint = hex_to_rgba(color_hex_data['facepaint'])

	
	diagnose_meshes_against_charafile(RESULTS_DICT,selected_armature)

	print_textools_data(RESULTS_DICT,color_hex_data)
	

	
	if apply_charafile_to_selected == True:
		add_custom_properties_to_armature(selected_armature,RESULTS_DICT)
		apply_face_shape_keys(RESULTS_DICT)
		apply_face_bone_morphs(RESULTS_DICT)
		#add the hex properties to the armature
		add_custom_property(selected_armature,'color_hex_skin',color_hex_data['skin'])
		add_custom_property(selected_armature,'color_hex_hair',color_hex_data['hair'])
		add_custom_property(selected_armature,'color_hex_hair_highlights',color_hex_data['hair_highlights'])
		add_custom_property(selected_armature,'color_hex_tattoo_limbal',color_hex_data['tattoo_limbal'])
		add_custom_property(selected_armature,'color_hex_eyes',color_hex_data['eyes'])
		add_custom_property(selected_armature,'color_hex_lips',color_hex_data['lips'])
		add_custom_property(selected_armature,'color_hex_facepaint',color_hex_data['facepaint'])

		
		bone_conversion.set_bust_size(bust_xyz=[float(x) for x in RESULTS_DICT['BustScale'].split(',')])

		
	




from bpy_extras.io_utils import ImportHelper
@register_wrap
class FFXIV_CharaFileBrowserImportOperator(bpy.types.Operator, ImportHelper):
	"""Operator that opens the file browser dialog for .chara files from Anamnesis and applies it to currently selected armature"""
	bl_idname = "ffxiv_mmd.apply_ffxiv_chara_file_browser_operator"
	bl_label = "Chara File Browser Operator"
	bl_options = {'REGISTER', 'UNDO'}

	filename_ext = ".chara"
	filter_glob: bpy.props.StringProperty(
		default="*.chara",
		options={'HIDDEN'},
	)

	#apply_charafile_to_selected = bpy.props.BoolProperty(name="Apply To Selected", default=False)

	@classmethod
	def poll(cls, context):
		if context.active_object:
			return context.active_object.type == 'ARMATURE'


	def execute(self, context):
		filepath = self.filepath
		main(context,filepath,apply_charafile_to_selected=True)



		return {'FINISHED'}
	
@register_wrap
class FFXIV_CharaFileBrowserImportOperator(bpy.types.Operator, ImportHelper):
	"""Operator that opens the file browser dialog for .chara files from Anamnesis"""
	bl_idname = "ffxiv_mmd.read_ffxiv_chara_file_browser_operator"
	bl_label = "Chara File Browser Operator"
	bl_options = {'REGISTER', 'UNDO'}

	filename_ext = ".chara"
	filter_glob: bpy.props.StringProperty(
		default="*.chara",
		options={'HIDDEN'},
	)

	def execute(self, context):
		filepath = self.filepath
		main(context,filepath,apply_charafile_to_selected=False)


		return {'FINISHED'}




@register_wrap
class ImportFFXIVModel(bpy.types.Operator):
	"""Store Relevant Chara information"""
	bl_idname = "ffxiv_mmd.chara_data_box"
	bl_label = "Chara Data Box"
	bl_options = {'REGISTER', 'UNDO'}


	bpy.types.Scene.color_skin= bpy.props.FloatVectorProperty(name="Skin", subtype='COLOR', size=4, default=(1.0, 1.0, 1.0, 1.0))
	bpy.types.Scene.color_hair= bpy.props.FloatVectorProperty(name="Hair", subtype='COLOR', size=4, default=(1.0, 1.0, 1.0, 1.0))
	bpy.types.Scene.color_hair_highlights= bpy.props.FloatVectorProperty(name="Hair Highlights",  subtype='COLOR', size=4, default=(1.0, 1.0, 1.0, 1.0))
	bpy.types.Scene.color_tattoo_limbal= bpy.props.FloatVectorProperty(name="Tattoo/Limbal", subtype='COLOR', size=4, default=(1.0, 1.0, 1.0, 1.0))
	bpy.types.Scene.color_eyes= bpy.props.FloatVectorProperty(name="Eyes", subtype='COLOR', size=4, default=(1.0, 1.0, 1.0, 1.0))
	bpy.types.Scene.color_lips= bpy.props.FloatVectorProperty(name="Lips", subtype='COLOR', size=4, default=(1.0, 1.0, 1.0, 1.0))
	bpy.types.Scene.color_facepaint= bpy.props.FloatVectorProperty(name="Facepaint", subtype='COLOR', size=4, default=(1.0, 1.0, 1.0, 1.0))
	
	"""
	@classmethod
	def poll(cls, context):
		return context.active_object is not None
	
	def execute(self, context):
		main(context)
		return {'FINISHED'}
	"""



