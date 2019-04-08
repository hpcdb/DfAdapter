cd ../../
INFILE=/shared/workflow-sedimentation/libmesh-sedimentation/input/lock2d/alock_meiburg2D_cte.in
python src/DfAdapter.py Bob OSimulationSetup '{"flow_initial_linear_solver_tolerance": 1.0e-2}'
