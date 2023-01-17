import bpy
import csv

# Each row read from the csv file is returned as a list of strings.

def use_csv_bones_dictionary():
	bones_dictionary = (__file__ + "bones_dictionary.csv").replace("import_csv.py" , "")
	with open(bones_dictionary, newline='', encoding='utf-8') as csvfile:
		CSVreader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
		BONES_DICTIONARY = [tuple(x) for x in CSVreader]

	# print('\n')
	# print("BONES_DICTIONARY = ")
	# for t in BONES_DICTIONARY:
		# print(t , ",")

	return BONES_DICTIONARY


def use_csv_bones_fingers_dictionary():
	finger_bones_dictionary = (__file__ + "bones_fingers_dictionary.csv").replace("import_csv.py" , "")
	with open(finger_bones_dictionary, newline='', encoding='utf-8') as csvfile:
		CSVreader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
		FINGER_BONES_DICTIONARY = [tuple(x) for x in CSVreader]

	# print('\n')
	# print("FINGER_BONES_DICTIONARY = ")
	# for t in FINGER_BONES_DICTIONARY:
		# print(t , ",")

	return FINGER_BONES_DICTIONARY

def use_csv_translations_dictionary():
	translations_dictionary = (__file__ + "translations.csv").replace("import_csv.py" , "")
	with open(translations_dictionary, newline='', encoding='utf-8') as csvfile:
		CSVreader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
		TRANSLATIONS_DICTIONARY = [tuple(x[:2]) for x in CSVreader]

	# print('\n')
	# print("TRANSLATIONS_DICTIONARY = ")
	# for t in TRANSLATIONS_DICTIONARY:
		# print(t , ",")

	return TRANSLATIONS_DICTIONARY
	
	
def use_csv_shape_keys_dictionary(ffxiv_race):
	CSVreader = None

	shape_keys_dictionary = (__file__ + "shape_keys_" + ffxiv_race +".csv").replace("import_csv.py" , "")

	with open(shape_keys_dictionary, newline='', encoding='utf-8') as csvfile:
		CSVreader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
		SHAPE_KEYS_DICTIONARY = [tuple(x[:8]) for x in CSVreader]
	# delete the first element (header record)
	SHAPE_KEYS_DICTIONARY.pop(0)
	#trim leading and trailing white space
	for i in range(len(SHAPE_KEYS_DICTIONARY)):
		SHAPE_KEYS_DICTIONARY[i] = tuple(x.strip() for x in SHAPE_KEYS_DICTIONARY[i])
	return SHAPE_KEYS_DICTIONARY