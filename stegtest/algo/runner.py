import subprocess 
import docker

import stegtest.utils.lookup as lookup
import stegtest.utils.filesystem as fs
from pathos.multiprocessing import ProcessingPool as Pool

client = docker.from_env()

def start_docker(image_name, volumes):
	container = client.containers.run(image_name, volumes=volumes, tty=True, detach=True)

	return container.id

def get_container(container_id):
	container = None
	while container is None:
		try:
			container = client.containers.get(container_id)
		except:
			print('lock contention for docker container')
			pass

	print(container.logs())
	return container

def stop_docker(container_id):
	container = get_container(container_id)
	container.stop()

def run_native(cmd, print_cmd=False):
	if print_cmd:
		print(cmd)
	subprocess.run(cmd, shell=True)

def run_docker(container_id, cmd, wdir=None):
	container = get_container(container_id)
	if wdir:
		container.run_exec(cmd, workdir=wdir)
	else:
		container.exec_run(cmd)

def run_class(cmd):
	raise NotImplementedError

def run_rest(cmd):
	raise NotImplementedError

def run(cmd_info):
	cmd_type = cmd_info[lookup.COMMAND_TYPE]
	run_function = {
		lookup.DOCKER: run_docker,
		lookup.NATIVE: run_native,
		lookup.REST: run_rest,
		lookup.CLASS: run_class,
		lookup.END_DOCKER: stop_docker,
	}[cmd_type]

	run_info = cmd_info[lookup.COMMAND]
	run_function(*run_info)

def run_pool(cmd_list, threads=None):
	if threads:
		pool = Pool(threads)
	else:
		pool = Pool()

	pool.map(run, cmd_list)