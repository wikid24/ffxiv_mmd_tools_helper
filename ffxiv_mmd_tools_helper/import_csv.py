import csv
import os


def csv_cleanup (csv_data,keep_header,convert_str_to_float,convert_null_to_0, convert_null_to_none):

	if keep_header == False:
		# remove the first element of the list (column header)
		csv_data = csv_data[1:]

	# remove leading/trailing whitespaces and replace empty string with None
	csv_data = [[x.strip() if isinstance(x, str) else x for x in row] for row in csv_data]
	csv_data = [[None if x == '' and i == 0 else x for i,x in enumerate(row)] for row in csv_data]

	if convert_str_to_float == True:
		# convert numeric strings to floats 
		csv_data = [[float(x) if isinstance(x, str) and x.replace('.','').replace('-','').isnumeric() else x for x in row] for row in csv_data]
	
	if convert_null_to_0 == True:
		# replace empty string with 0
		csv_data = [[0 if x == '' and i != 0 else x for i,x in enumerate(row)] for row in csv_data]
		
	if convert_null_to_none == True:
		# replace empty string with None
		csv_data = [[None if x == '' and i != 0 else x for i,x in enumerate(row)] for row in csv_data]
		"""
		#convert the str '' values to None;
		for row in csv_data:
			for key, value in row.items():
				if value == '':
					row[key] = None
		"""
	return csv_data

	
	
def try_read_file (file_path):

	#error handling to make sure that the file actually exists before attempting to open it
	if os.path.exists(file_path):
		try:
			with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
				CSVdata = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
				dictionary = [tuple(x) for x in CSVdata]
				return dictionary
		except:
			print(f"File found but can't be opened: {file_path}")
			return None
	else:
		print(f"File not found: {file_path}")
		return None

# Each row read from the csv file is returned as a list of strings.

def use_csv_bones_dictionary():
	file_path = (__file__ + r"data\bones_dictionary.csv").replace("import_csv.py" , "")
	print(file_path)
	BONES_DICTIONARY = try_read_file(file_path)
	BONES_DICTIONARY = csv_cleanup(BONES_DICTIONARY,True,False,False,False)
	return BONES_DICTIONARY



def use_csv_bones_fingers_dictionary():
	file_path = (__file__ + r"data\bones_fingers_dictionary.csv").replace("import_csv.py" , "")
	print(file_path)
	FINGER_BONES_DICTIONARY = try_read_file(file_path)
	FINGER_BONES_DICTIONARY = csv_cleanup(FINGER_BONES_DICTIONARY,True,False,False,False)
	return FINGER_BONES_DICTIONARY

def use_csv_translations_dictionary():
	file_path = (__file__ + r"data\translations.csv").replace("import_csv.py" , "")
	print(file_path)
	TRANSLATIONS_DICTIONARY = try_read_file(file_path)
	TRANSLATIONS_DICTIONARY = csv_cleanup(TRANSLATIONS_DICTIONARY,True,False,False,False)
	return TRANSLATIONS_DICTIONARY

def use_csv_bone_metadata_ffxiv_dictionary():
	file_path = (__file__ + r"data\bones_metadata_ffxiv_dictionary.csv").replace("import_csv.py" , "")
	#print(file_path)
	BONES_METADATA_FFXIV_DICTIONARY = try_read_file(file_path)
	BONES_METADATA_FFXIV_DICTIONARY = csv_cleanup(BONES_METADATA_FFXIV_DICTIONARY,True,False,False,True)
	return BONES_METADATA_FFXIV_DICTIONARY
	
def use_csv_shape_keys_dictionary(ffxiv_race):

	#path = r"D:\MMD\ffxiv_mmd_tools_helper\ffxiv_mmd_tools_helper_beta"
	#file_path= (path + r"\data\shape_keys_" + ffxiv_race +".csv").replace("import_csv.py" , "")
	file_path = (__file__ + r"data\shape_keys_" + ffxiv_race +".csv").replace("import_csv.py" , "")
	print(file_path)

	SHAPE_KEYS_DICTIONARY = try_read_file(file_path)
	SHAPE_KEYS_DICTIONARY = csv_cleanup(SHAPE_KEYS_DICTIONARY,False,True,True,False)
	return SHAPE_KEYS_DICTIONARY


def use_csv_bone_morphs_list():

	#path = r"D:\MMD\ffxiv_mmd_tools_helper\ffxiv_mmd_tools_helper_beta"
	#file_path= (path + r"\data\bone_morph_list.csv").replace("import_csv.py" , "")
	file_path = (__file__ + r"data\bone_morph_list.csv").replace("import_csv.py" , "")
	#print(file_path)

	BONE_MORPHS_LIST = try_read_file(file_path)
	BONE_MORPHS_LIST = csv_cleanup(BONE_MORPHS_LIST,False,False,False,False)

	BONE_MORPHS_LIST = [element for element in BONE_MORPHS_LIST]
	return BONE_MORPHS_LIST


def use_csv_bone_morphs_dictionary(ffxiv_race):

	#path = r"D:\MMD\ffxiv_mmd_tools_helper\ffxiv_mmd_tools_helper_beta"
	#file_path= (path + r"\data\bone_morphs_" + ffxiv_race +".csv").replace("import_csv.py" , "")
	file_path = (__file__ + r"data\bone_morphs_" + ffxiv_race +".csv").replace("import_csv.py" , "")
	#print(file_path)
	
	BONE_MORPHS_DICTIONARY = try_read_file(file_path)
	BONE_MORPHS_DICTIONARY = csv_cleanup(BONE_MORPHS_DICTIONARY,False,True,True,False)
	
	return BONE_MORPHS_DICTIONARY



def use_csv_rigid_body_dictionary():

    #path = r"D:\MMD\ffxiv_mmd_tools_helper\ffxiv_mmd_tools_helper_beta"
    #file_path= (path + r"\data\rigid_body_dictionary.csv").replace("import_csv.py" , "")
    file_path = (__file__ + r"data\rigid_body_dictionary.csv").replace("import_csv.py" , "")
    print(file_path)

    RIGID_BODY_DICTIONARY = try_read_file(file_path)
    RIGID_BODY_DICTIONARY = csv_cleanup(RIGID_BODY_DICTIONARY,True,True,True,False)
    return RIGID_BODY_DICTIONARY

def use_csv_joints_dictionary():

	#path = r"D:\MMD\ffxiv_mmd_tools_helper\ffxiv_mmd_tools_helper_beta"
	#file_path= (path + r"\data\joints_dictionary.csv").replace("import_csv.py" , "")
	file_path = (__file__ + r"data\joints_dictionary.csv").replace("import_csv.py" , "")
	print(file_path)

	JOINTS_DICTIONARY = try_read_file(file_path)
	JOINTS_DICTIONARY = csv_cleanup(JOINTS_DICTIONARY,True,True,True,False)
	return JOINTS_DICTIONARY

def use_csv_charafile_dictionary():
	file_path = (__file__ + r"data\chara_file_dictionary.csv").replace("import_csv.py" , "")
	print(file_path)
	CHARAFILE_DICTIONARY = try_read_file(file_path)
	CHARAFILE_DICTIONARY = csv_cleanup(CHARAFILE_DICTIONARY,True,False,False,False)
	return CHARAFILE_DICTIONARY

def use_csv_color_eye_dictionary():
	file_path = (__file__ + r"data\color_eye_dictionary.csv").replace("import_csv.py" , "")
	print(file_path)
	COLOR_EYE_DICTIONARY = try_read_file(file_path)
	COLOR_EYE_DICTIONARY = csv_cleanup(COLOR_EYE_DICTIONARY,True,False,False,False)
	return COLOR_EYE_DICTIONARY

def use_csv_color_facepaint_dictionary():
	file_path = (__file__ + r"data\color_facepaint_dictionary.csv").replace("import_csv.py" , "")
	print(file_path)
	COLOR_FACEPAINT_DICTIONARY = try_read_file(file_path)
	COLOR_FACEPAINT_DICTIONARY = csv_cleanup(COLOR_FACEPAINT_DICTIONARY,True,False,False,False)
	return COLOR_FACEPAINT_DICTIONARY

def use_csv_color_hair_dictionary():
	file_path = (__file__ + r"data\color_hair_dictionary.csv").replace("import_csv.py" , "")
	print(file_path)
	COLOR_HAIR_DICTIONARY = try_read_file(file_path)
	COLOR_HAIR_DICTIONARY = csv_cleanup(COLOR_HAIR_DICTIONARY,True,False,False,False)
	return COLOR_HAIR_DICTIONARY

def use_csv_color_hairhighlights_dictionary():
	file_path = (__file__ + r"data\color_hairhighlights_dictionary.csv").replace("import_csv.py" , "")
	print(file_path)
	COLOR_HAIRHIGHLIGHTS_DICTIONARY = try_read_file(file_path)
	COLOR_HAIRHIGHLIGHTS_DICTIONARY = csv_cleanup(COLOR_HAIRHIGHLIGHTS_DICTIONARY,True,False,False,False)
	return COLOR_HAIRHIGHLIGHTS_DICTIONARY

def use_csv_color_lips_dictionary():
	file_path = (__file__ + r"data\color_lips_dictionary.csv").replace("import_csv.py" , "")
	print(file_path)
	COLOR_LIPS_DICTIONARY = try_read_file(file_path)
	COLOR_LIPS_DICTIONARY = csv_cleanup(COLOR_LIPS_DICTIONARY,True,False,False,False)
	return COLOR_LIPS_DICTIONARY

def use_csv_color_skin_dictionary():
	file_path = (__file__ + r"data\color_skin_dictionary.csv").replace("import_csv.py" , "")
	print(file_path)
	COLOR_SKIN_DICTIONARY = try_read_file(file_path)
	COLOR_SKIN_DICTIONARY = csv_cleanup(COLOR_SKIN_DICTIONARY,True,False,False,False)
	return COLOR_SKIN_DICTIONARY

def use_csv_color_tattoo_limbalring_dictionary():
	file_path = (__file__ + r"data\color_tattoo_limbalring_dictionary.csv").replace("import_csv.py" , "")
	print(file_path)
	COLOR_TATTOO_LIMBALRING_DICTIONARY = try_read_file(file_path)
	COLOR_TATTOO_LIMBALRING_DICTIONARY = csv_cleanup(COLOR_TATTOO_LIMBALRING_DICTIONARY,True,False,False,False)
	return COLOR_TATTOO_LIMBALRING_DICTIONARY


def open_csv(file_path):
    #subprocess.Popen(["start", file_path], shell=True)
	os.startfile(file_path)



def open_bone_morphs_dictionary(ffxiv_race):

	#path = r"D:\MMD\ffxiv_mmd_tools_helper\ffxiv_mmd_tools_helper_beta"
	#file_path= (path + r"\data\bone_morphs_" + ffxiv_race +".csv").replace("import_csv.py" , "")
	file_path = (__file__ + r"data\bone_morphs_" + ffxiv_race +".csv").replace("import_csv.py" , "")
	print(file_path)
	BONE_MORPHS_DICTIONARY = try_read_file(file_path)

	if BONE_MORPHS_DICTIONARY is not None:
		open_csv(file_path)
	else:
		print('could not find the file', file_path)

def open_shape_keys_dictionary(ffxiv_race):

	#path = r"D:\MMD\ffxiv_mmd_tools_helper\ffxiv_mmd_tools_helper_beta"
	#file_path= (path + r"\data\bone_morphs_" + ffxiv_race +".csv").replace("import_csv.py" , "")
	file_path = (__file__ + r"data\shape_keys_" + ffxiv_race +".csv").replace("import_csv.py" , "")
	print(file_path)
	BONE_MORPHS_DICTIONARY = try_read_file(file_path)

	if BONE_MORPHS_DICTIONARY is not None:
		open_csv(file_path)
	else:
		print('could not find the file', file_path)
