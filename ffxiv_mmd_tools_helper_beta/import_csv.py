import bpy
import csv
import os

def csv_cleanup (csv_data,keep_header,convert_numbers):

	if keep_header == False:
		# remove the first element of the list (column header)
		csv_data = csv_data[1:]

	# remove leading/trailing whitespaces and replace empty string with None
	csv_data = [[x.strip() if isinstance(x, str) else x for x in row] for row in csv_data]
	csv_data = [[None if x == '' and i == 0 else x for i,x in enumerate(row)] for row in csv_data]

	if convert_numbers == True:
		# convert numeric strings to floats and replace empty string with 0
		csv_data = [[float(x) if isinstance(x, str) and x.replace('.','').replace('-','').isnumeric() else x for x in row] for row in csv_data]
		csv_data = [[0 if x == '' and i != 0 else x for i,x in enumerate(row)] for row in csv_data]

	return csv_data
	
	
def try_open_file (file_path):

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
	file_path = (__file__ + "bones_dictionary.csv").replace("import_csv.py" , "")
	print(file_path)
	BONES_DICTIONARY = try_open_file(file_path)
	BONES_DICTIONARY = csv_cleanup(BONES_DICTIONARY,True,False)
	return BONES_DICTIONARY



def use_csv_bones_fingers_dictionary():
	file_path = (__file__ + "bones_fingers_dictionary.csv").replace("import_csv.py" , "")
	print(file_path)
	FINGER_BONES_DICTIONARY = try_open_file(file_path)
	FINGER_BONES_DICTIONARY = csv_cleanup(FINGER_BONES_DICTIONARY,True,False)
	return FINGER_BONES_DICTIONARY

def use_csv_translations_dictionary():
	file_path = (__file__ + "translations.csv").replace("import_csv.py" , "")
	print(file_path)
	TRANSLATIONS_DICTIONARY = try_open_file(file_path)
	TRANSLATIONS_DICTIONARY = csv_cleanup(TRANSLATIONS_DICTIONARY,True,False)
	return TRANSLATIONS_DICTIONARY

	
def use_csv_shape_keys_dictionary(ffxiv_race):

	path = r"D:\MMD\ffxiv_mmd_tools_helper_beta\ffxiv_mmd_tools_helper_beta"
	file_path= (path + r"\data\shape_keys_" + ffxiv_race +".csv").replace("import_csv.py" , "")
	print(file_path)
	#file_path = (__file__ + "shape_keys_" + ffxiv_race +".csv").replace("import_csv.py" , "")
	
	SHAPE_KEYS_DICTIONARY = try_open_file(file_path,False,True)
	SHAPE_KEYS_DICTIONARY = csv_cleanup(SHAPE_KEYS_DICTIONARY)
	return SHAPE_KEYS_DICTIONARY

