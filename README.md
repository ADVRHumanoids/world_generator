# World Random Generator
This python script allows to randomly generate cluttered Gazebo worlds. In particular you can select the shapes you want to include and define: min and max dimensions, min and max area for the spawning, number of elements to consider.

# Dependencies
- Python3
- pyyaml

# How to run
In order to run it you simply have to execute the script: generator.py
The resulting .world file will be written inside "data" folder.

In order to launch the world from other locations you need the following export:
    export GAZEBO_RESOURCE_PATH=$GAZEBO_RESOURCE_PATH:{your_local_path}/world_generator/data

# Object Description
For now the following objects are available:
- _Random boxes_: boxes with random size, orientation (mass to be added).
- _Brick_: a brick with 3 holes. It has fixed dimension 0.50x0.15x0.194 and mass 15 Kg.
- _WoodenPlatform_: wooden rectangular platform with the following dimension: 1.25x0.50x0.15 with mass 10 Kg.
- _WoodenPallet_: wooden rectangular pallet with the following dimension: 1.20x0.805x0.165 with mass 1000 Kg.
- _WoodenCrate_: cubic crate with dimensions 0.4x0.4x0.4 and mass 10kg.
