# Generic Dataflow Example in Apache Spark

## Dependencies

- Apache Spark
  - [Download](https://spark.apache.org/downloads.html)
  - It was tested on v2.2.0, Pre-built for Apache Hadoop 2.7 and later
- [Redis]
  - [Download](https://redis.io/topics/quickstart)
- [Python 2.7]
  - [Download](https://www.python.org/downloads/)

## Main source files

#### Main Dataflow

- `run-main-dataflow.sh` calls Spark to run the dataflow in localhost
- `src/Main_Spark_Dataflow.py` defines the main dataflow. For a longer demo, you can add more elements to X or increase the sleep time in `act3`.

#### DfAdapter

- `DfAdapter.sh` predefines some parameters that can be tuned with new values. If you want to modify different parameters or with different values, you can edit the JSON in this file.
- `src/DfAdapter.py` calls the Dataset Adapter.
- `src/Dataset_2_Adapter.py` contains application-specific code that runs the adaptation.

## Running

1. Run the main dataflow
```
$> bash run-main-dataflow.sh
```

2. Adapt the dataflow
```
$> bash DfAdapter.sh
```
