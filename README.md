# DfAdapter

DfAdapter is a light-weight tool that collects provenance of human interaction data when users adapt a dataflow online (while it is in execution), relates with other data of interest and makes the provenance database available for online analytical queries.  Example of possible adaptations are: parameter tuning, dataset reduction, loop changes, etc.

# Contents

- [Data diagrams](diagrams)   
- [Adapting a Spark dataflow online](generic_dataflow)

# Sequence Diagram

The objective of this diagram is to clarify how human adaptation occurs in a running workflow.

![Sequence Diagram](https://raw.githubusercontent.com/hpcdb/DfAdapter/master/diagrams/seq-diagram.png)

0. The workflow runs normally. Meanwhile, provenance data are collected and stored in a DBMS for online queries. The adaptable dataset is stored in a shared space between DfAdapter and the dataflow itself. That is, DfAdapter needs to have access to the dataset being processed/that will be processed by the running workflow.
1. The user issues a command using DfAdapter Command Line Interface to adapt a dataset in the dataflow.
2. DfAdapter calls the DataSet Adapter (application specific) to adapt the dataset in the shared space.
3. DfAdapter notifies the running workflow that the user issued an adaptation.
4. The running workflow verifies that an adaptation occurred and reloads the dataset with the adapted data.
5. The running workflow communicates with DfAdapter to send data related to the workflow execution state, extra data that are relevant to identify the execution state. Also, the workflow sends a  message to DfAdapter to notify that the dataset has been reloaded.
6. DfAdapter stores human-adaptation data in the provenance database.
7. DfAdapter sends a feedback message to the user to notify that the adaptation action has finished successfully.

An example of implementation of this diagram is described along with the source code of a [generic workflow](generic_dataflow/README.md#functioning) implemented in Spark.
