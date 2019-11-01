from os import listdir
from os.path import isfile, join, abspath

import ast
import stegtest.utils.filesystem as fs
import stegtest.utils.lookup as lookup

import configparser

def is_config_file(file):
	return fs.get_extension(file) == '.ini'

def validate_native():
	return True

def validate_docker(config):
	#TODO assert facts about the image and the command
	assert(config[lookup.DOCKER_IMAGE])
	assert(config[lookup.COMMAND])

def validate_native(config):
	assert(config[lookup.COMMAND])

def validate_rest(config):
	raise NotImplementedError

def validate_class(config):
	raise NotImplementedError

def validate_config(config):
	compatible_types = config[lookup.compatible_descriptor]
	allowed_types = lookup.all_supported_types()
	for img_type in compatible_types:
		assert(img_type in allowed_types)

	validate_function = {
		lookup.DOCKER: validate_docker,
		lookup.NATIVE: validate_native,
		lookup.REST: validate_rest,
		lookup.CLASS: validate_class
	}[config[lookup.COMMAND_TYPE]]

	validate_function(config)

def process_embeddor(embeddors_dict, config_file_path):
	embeddor_file = lookup.get_all_files()[lookup.embeddors_file]
	data_to_write = []
	for name in embeddors_dict.keys():
		embeddor_data = embeddors_dict[name]
		data = [fs.get_uuid(), name, config_file_path]

		data_to_write.append(data)

	fs.write_to_csv_file(embeddor_file, data_to_write)

def process_detector(detectors_dict, config_file_path):
	detector_file = lookup.get_all_files()[lookup.detectors_file]
	data_to_write = []
	for name in detectors_dict.keys():
		detector_data = detectors_dict[name]
		data = [fs.get_uuid(), name, detector_data[lookup.COMPATIBLE_TYPES], config_file_path]

		data_to_write.append(data)

	fs.write_to_csv_file(detector_file, data_to_write)

def get_config_from_file(config_file_path):
	config_dict = fs.read_config_file(config_file_path)
	for config_name in config_dict:
		config = config_dict[config_name]
		config[lookup.compatible_descriptor] = ast.literal_eval(config[lookup.compatible_descriptor])
		config[lookup.embedding_descriptor] = float(config[lookup.embedding_descriptor])

		validate_config(config)

	return config_dict

def process_configs(config_dict, config_file_path):
	config_embeddors = {k:v for (k,v) in config_dict.items() if config_dict[k][lookup.ALGORITHM_TYPE] == lookup.embeddor}
	config_detectors = {k:v for (k,v) in config_dict.items() if config_dict[k][lookup.ALGORITHM_TYPE] == lookup.detector}

	process_embeddor(config_embeddors, config_file_path)
	process_detector(config_detectors, config_file_path)

def get_config_files(config_directory): #TODO push this to filesystem
	assert(fs.dir_exists(config_directory))
	config_files = [abspath(join(config_directory, f)) for f in listdir(config_directory) if is_config_file(f)]
	return config_files

def process_config_file(config_file_path):
	config_file_path = abspath(config_file_path)
	config_dict = get_config_from_file(config_file_path)

	print('starting processing of config file: ' + config_file_path)
	process_configs(config_dict, config_file_path)
	print('processing of file complete')

def process_config_directory(config_directory):
	config_files = get_config_files(config_directory)
	print('processing config directory: ' + config_directory)
	for config_file_path in config_files:
		process_config_file(config_file_path)

	print('processing of directory complete')

def build_configs(configs):
	for config in configs:
		build_config_file(config[INSTALL][0])

def check_config_docker(config_details):
	raise NotImplementedError

def check_config_native(config_details):
	raise NotImplementedError

def check_config_class(config_details):
	raise NotImplementedError

def check_config_rest(config_details):
	raise NotImplementedError

def check_config_info(config_details):
	return True