# libMesh-sedimentation Example

DfAdapter was mainly used coupled with a sedimentation simulation solver used in the O&G industry, called [**libMesh-sedimentation**](https://github.com/hpcdb/workflow-sedimentation), implemented in C++.
Please visit its own GitHub repository for more details and source code.

## Functioning of DfAdapter within libMesh-sedimentation

The main loop that can be adapted by the user is a time-loop whose simulation parameters can be steered by the user at each new iteration. The figure below shows a didatic illustration. The source code of the loop below is found [here](https://github.com/hpcdb/workflow-sedimentation/blob/master/libmesh-sedimentation/sedimentation.C#L725).

![libMesh-sedimentation](https://github.com/hpcdb/DfAdapter/raw/master/diagrams/libmesh-sed.pdf)

The loop reloads the predefined parameters whenever there is a change in a specified [INI](https://en.wikipedia.org/wiki/INI_file) file. This file path must be specified in the environment variable `INFILE`.
When the user uses DfAdapter by, e.g., calling the script [DfAdapter-example.sh](DfAdapter-example.sh), the specified file is modified by DfAdapter and the provenance of the steering actions are tracked and releated in the provenance database, managed by MonetDB.
    
  
