from pyspark import SparkContext, SparkConf
import time
import sys
import numpy as np
from src.adapters.redis_based_adapter import *

conf = SparkConf().setAppName("dataflow")
sc = SparkContext(conf=conf)

def act1(de):
    return [de[0]*de[0], de[1]*de[1], de[2]*de[2]]

def act2(de):
    lst = []
    for i in range(0,5):
        lst.append([i*de[0]+de[1], i*de[1]+de[2], i*de[0]+de[2]])
    return lst

def act3(de,dataset_2_lst,error):
    time.sleep(1)
    return (1,np.sqrt(dataset_2_lst[0][0]*de[0]+
             dataset_2_lst[0][1]*de[1]+
             dataset_2_lst[0][0]*de[2])/error)

def act4(accum, n):
    return accum+n

## Initializations
X = [[1.0e-4,2.45e-4,3.2e-3]]
error = 1.0e-1
i = 0
max_iterations = 100
dataset_1 = sc.parallelize(X,8)
ds2_adapter = Redis_DataSet_Adapter()
##################

dataset_2 = dataset_1.map(lambda de: act1(de))
dataset_2_lst = dataset_2.collect()

while i < max_iterations:
    if ds2_adapter.has_adaptation():
        dataset_2_lst = ds2_adapter.update_values(dataset_2_lst,i)
        dataset_2 = sc.parallelize(dataset_2_lst,8)

    dataset_3 = dataset_2.flatMap(lambda de: act2(de))
    dataset_4 = dataset_3.map(lambda de: act3(de,dataset_2_lst,error))
    dataset_5 = dataset_4.reduceByKey(lambda accum, n: act4(accum, n))
    error *= dataset_5.collect()[0][1]
    print "Printing error", error
    i += 1
