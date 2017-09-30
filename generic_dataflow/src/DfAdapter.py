import sys
import os
import json
from time import gmtime, strftime
from subprocess import call
from subprocess import Popen, PIPE

def get_steered_parameters_str(parameters_json):
    if os.path.isfile(parameters_json):
        with open(parameters_json) as data_file:
            steered_parameters = json.load(data_file)
    else:
        try:
            steered_parameters = json.loads(parameters_json)
        except:
            print "This is not a valid JSON: %s \n" % parameters_json
            sys.exit(-1)
    return json.dumps(steered_parameters)

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print "Arguments: user dataset parameters_json"
        sys.exit(0)

    user = sys.argv[1]
    dataset = sys.argv[2]
    parameters_json = sys.argv[3]

    parameters_str = get_steered_parameters_str(parameters_json)
    cmd = ["python","src/Dataset_2_Adapter.py",parameters_str]
    process = Popen(cmd, stdout=PIPE)
    (output, err) = process.communicate()

    #print err
    exit_code = process.wait()
    if (exit_code == 0):
        provenance = json.loads(output)
        provenance.update({"user":user, "dataset":dataset, "time_gmt":strftime("%Y-%m-%d %H:%M:%S", gmtime())})
        with open('adaptations.jsonl', 'a+') as outfile:
            outfile.write(json.dumps(provenance)+"\n")
        print provenance
        print "Steered successfully"
