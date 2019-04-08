import sys
import os
import json
from time import gmtime, strftime
from subprocess import Popen, PIPE
import pymonetdb

from numpy import random

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

    if len(sys.argv) < 4:
        print "Arguments: user dataset parameters_json [optional path to adapter script]"
        sys.exit(0)

    connection = pymonetdb.connect(username="monetdb", password="monetdb", hostname="localhost", database="dataflow_analyzer", autocommit=True)
    cursor = connection.cursor()


    user = sys.argv[1]
    dataset = sys.argv[2]
    parameters_json = sys.argv[3]
    if len(sys.argv) > 4:
        adapter_implementation_script = sys.argv[4]
    else:
        adapter_implementation_script = "src/adapters/redis_based_adapter.py"

    parameters_str = get_steered_parameters_str(parameters_json)
    cmd = ["python", adapter_implementation_script, parameters_str]
    process = Popen(cmd, stdout=PIPE)
    (adapted_parameters_json, err) = process.communicate()

    #print err
    exit_code = process.wait()
    if (exit_code == 0):
        provenance = json.loads(adapted_parameters_json)
        provenance.update({"user":user, "dataset":dataset, "time_gmt":strftime("%Y-%m-%d %H:%M:%S", gmtime())})
        with open('data/adaptations.jsonl', 'a+') as outfile:
            outfile.write(json.dumps(provenance)+"\n")

        cursor.execute('set schema "public"')

        human_activity_id = int(random.random()*100)

        sql = ("INSERT INTO human_activity (id, ha_type, time, description) values \
        (" + str(human_activity_id) + ", 'TUNING','" + provenance['time_gmt'] +  "', '');")

        print(sql)

        cursor.execute(sql)



        cursor.execute("INSERT INTO attribute_tuned (human_activity_id, attribute_id, old_value, new_value)\
         VALUES ({}, {},{},{});".format(human_activity_id, 230, provenance['parameter-provenance']['attr1']['old'],provenance['parameter-provenance']['attr1']['new']))

        print provenance
        print "Steered successfully"
