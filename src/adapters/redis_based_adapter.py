import redis
import json
import sys
import time
import ast
from time import gmtime, strftime

class Redis_DataSet_Adapter(object):
    def __init__(self):
        self.redis_client = redis.from_url('redis://localhost:6379')

    def has_adaptation(self):
        return self.redis_client.get("adapted") == "t"

    def get_new_values(self):
        attr1 = float(self.redis_client.get("attr1"))
        attr2 = float(self.redis_client.get("attr2"))
        attr3 = float(self.redis_client.get("attr3"))
        return [attr1, attr2, attr3]

    def update_values(self,dataset_lst,iteration):
        new_values = self.get_new_values()
        self.redis_client.set("iteration", iteration)
        self.redis_client.set("old_values", dataset_lst[0])
        self.redis_client.set("adapted", "f")
        return [[new_values[0], new_values[1], new_values[2]]]


class DataSet_Adapter_ProcCall(object):
    def __init__(self):
        self.redis_client = redis.from_url('redis://localhost:6379')

    def has_adaptation(self):
        return self.redis_client.get("adapted") == "t"

    def adapt(self, dict_new_values):
        self.redis_client.set("adapted", "t")
        for param in dict_new_values:
            self.redis_client.set(param, dict_new_values[param])

        #wait for the other process to conclude the adaptation
        while self.has_adaptation():
            time.sleep(1)

        lst_old_values = ast.literal_eval(self.redis_client.get("old_values"))
        iteration = self.redis_client.get("iteration")

        self.save_prov(dict_new_values,lst_old_values,iteration)

    def save_prov(self,dict_new_values,lst_old_values, iteration):
        prov = dict()
        prov["parameter-provenance"] = {
            "attr1": {"new":dict_new_values["attr1"],"old":lst_old_values[0]},
            "attr2": {"new":dict_new_values["attr2"],"old":lst_old_values[1]},
            "attr3": {"new":dict_new_values["attr3"],"old":lst_old_values[2]}
        }
        prov["extra-domain-data"] = {"iteration":iteration}
        print json.dumps(prov)

if __name__ == '__main__':
    dict_new_values = json.loads(sys.argv[1])
    ds2Adpt = DataSet_Adapter_ProcCall()
    ds2Adpt.adapt(dict_new_values)
