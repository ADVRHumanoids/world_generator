# World Random Generator
This python script allows to randomly generate cluttered Gazebo worlds. In particular you can select the shapes you want to include (for now only rectangular ones) and define: min and max dimensions, min and max area for the spawning, number of elements to consider.

# Dependencies
- Python3
- pyyaml

# How to run
In order to run it you simply have to execute the script: generator.py
The resulting .world file will be written inside "data" folder.

In order to launch the world from other nodes:
    export GAZEBO_RESOURCE_PATH=$GAZEBO_RESOURCE_PATH:{your_local_path}/world_generator/data
