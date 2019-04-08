# Diagrams

### Provenance Database Relational Schema
![Complete ER-Diagram](https://raw.githubusercontent.com/hpcdb/DfAdapter/master/diagrams/DfAnalyzer%26Adapter.png)

### DfAdapter tables
![DfAdapter tables](https://raw.githubusercontent.com/hpcdb/DfAdapter/master/diagrams/DB-Schema-ParameterTuning.png)

### PROV-DfA extended with Steering Action
![PROV-Df extended with Parameter Tuning Entities Entities](https://raw.githubusercontent.com/hpcdb/DfAdapter/master/diagrams/PROV-Df-ParameterTuning.png)

### Sequence Diagram

![Sequence Diagram](https://raw.githubusercontent.com/hpcdb/DfAdapter/master/diagrams/seq-diagram.png)

The sequence of steps that occur when a user steers using DfAdapter are as follows.

- `0`. Monitoring data specified in monitoring points are sent to the Provenance Server
- `1`. Provenance Server stores monitoring provenance in the Provenance Database, managed by MonetDB.
- `2`. User runs DfAdapter Command Line Interface (e.g., by calling [DfAdapter-example.sh](DfAdapter-example.sh)).
- `3`. The CLI calls [DfAdapter client](../src/DfAdapter.py). 
- `4`. DfAdapter client calls Provenance Server
- `5`. Provenance Server registers the beginning of a steering intention.
- `6`. DfAdapter client calls the adapter.
- `7`. The adapter (see [implemented adapters](https://github.com/hpcdb/DfAdapter/tree/master/src/adapters)) effectuates the adaptation that can be perceived by the running workflow.
- `8`. The running workflow perceives an adaptation (e.g., it verifies that a file -- see [libMesh-sedimentation example](../examples/libMesh-sedimentation) -- or an in-memory data structure -- see [Spark example](../examples/simple_spark_dataflow) -- has been modified).
- `9`. In the steering points specified by the user in the workflow code, the workflow generates steering action data and calls Provenance Server.
- `10`. Provenance Server receives the callings and stores user steering data in the Provenance Database.
- `11`. The user can run user steering action analysis. 


