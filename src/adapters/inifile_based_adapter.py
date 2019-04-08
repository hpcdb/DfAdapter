from __future__ import print_function
import ConfigParser
import sys
import os
import json
from StringIO import StringIO
from iniparse import INIConfig
import time
import sys

INI_SECTION_HEADER = "parameters"
TIMES_FILE_NAME = "times.json"
RESET_FILE_NAME = "reset.run"

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def read_ini_file(in_filepath):
    with open(in_filepath, "r") as ini_file:
        ini_file_content = ini_file.read()
    vfile = StringIO(u'[%s]\n%s'  % (INI_SECTION_HEADER, ini_file_content))
    in_parameters = INIConfig(vfile)
    return in_parameters

def write_new_ini_file(in_parameters):
    new_ini_content = in_parameters.__str__().replace("[%s]\n"%INI_SECTION_HEADER,"")
    with open(in_filepath, "w") as new_file:
        new_file.write(new_ini_content)

def steer_parameters(in_parameters, steered_parameters):
    steering_provenance = {}
    for p in steered_parameters:
        if p not in in_parameters[INI_SECTION_HEADER]:
            eprint("There is no such parameter: %s " % p)
            sys.exit(-1)

        old_v = in_parameters[INI_SECTION_HEADER][p]
        new_v = steered_parameters[p]
        in_parameters[INI_SECTION_HEADER][p] = new_v
        steering_provenance[p] = {
            "old": old_v,
            "new": new_v
        }
    return steering_provenance

def write_reset_file(execution_dir):
    reset_file_path = execution_dir+"/"+RESET_FILE_NAME
    with open(execution_dir+"/"+RESET_FILE_NAME, "w") as run_sh:
        run_sh.write("")


def wait_to_get_time_dict(execution_dir):
    time_path = execution_dir+"/"+TIMES_FILE_NAME

    while not os.path.isfile(time_path):
        eprint("times.json not ready yet. Waiting...")
        time.sleep(3)

    try:
        with open(time_path) as time_file:
            time_dict = json.load(time_file)
            os.remove(time_path)
            return time_dict
    except:
        eprint("Invalid JSON in %s " % time_path)
        sys.exit(-1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        eprint("You need to pass the parameters to be tuned as a valid JSON format")
        sys.exit(0)

    in_filepath = os.getenv("INFILE", None)
    if not in_filepath:
        eprint("You need define INFILE environment var with the ini file to be modified")
        sys.exit(0)

    steered_parameters = json.loads(sys.argv[1])
    execution_dir = os.getcwd()

    in_parameters = read_ini_file(in_filepath)
    parameter_provenance = steer_parameters(in_parameters,steered_parameters)
    write_new_ini_file(in_parameters)
    write_reset_file(execution_dir)
    time_dict = wait_to_get_time_dict(execution_dir)

    return_dict = {
        "parameter-provenance": parameter_provenance,
        "extra-domain-data": time_dict
    }
    print(json.dumps(return_dict))
