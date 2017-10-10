# Generic Dataflow Example in Apache Spark

## Dependencies

- Apache Spark
  - [Download](https://spark.apache.org/downloads.html)
  - It was tested on v2.2.0, Pre-built for Apache Hadoop 2.7 and later
- Redis
  - [Download](https://redis.io/topics/quickstart)
- Python 2.7
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

## Functioning

In this example, we implement the [Sequence Diagram](../README.md#sequence-diagram) as follows.
First, in message `1`, the user calls DfAdapter using `DfAdapter.sh` script.

DfAdapter and the running workflow in Spark uses Redis to store the adaptable dataset. That is, when DfAdapter adapts the adaptable dataset in Redis (message `2` in the diagram), the running workflow in Spark reloads the dataset with the new adjusted data (message `4` in the diagram).

Also, Redis is used as a data-oriented communication between DfAdapter and the running workflow in Spark. To implement the message `3` in the diagram, DfAdapter modifies a flag to notify the running workflow about the adaptation. The workflow checks this flag at each iteration in the main loop to see if an adaptation occurred. When the adaptation finishes (message `5` in the diagram), the workflow modifies the same flag. DfAdapter keeps checking this flag periodically to acknowledge message `5`. Extra data are also written in Redis by the running workflow in Spark to be read by DfAdapter. Finally, DfAdapter gets these data, organizes them, and store in the DBMS for provenance (message `6`). DfAdapter prints a sucess message for the user.

