# World Random Generator
This python script allows to randomly generate cluttered Gazebo worlds. In particular you can select the shapes you want to include and define: min and max dimensions, min and max area for the spawning, number of elements to consider.

# Dependencies
- Python3
- pyyaml

# How to run
In order to run it you simply have to execute the script: generator.py
The resulting .world file will be written inside "data" folder.

In order to launch the world from other locations you need the following export:
```
export GAZEBO_RESOURCE_PATH=$GAZEBO_RESOURCE_PATH:{your_local_path}/world_generator/data
```
# Object Description
For now the following objects are available:
- _Random boxes_: boxes with random size, orientation (mass to be added).
- _Brick_: a brick with 3 holes. It has fixed dimension 0.50x0.15x0.194 and mass 15 Kg.
- _WoodenCrateLong_: a longer wooden crate with dimension 1.0x0.50x0.50 and mass 50 kg.
- _WoodenPlatform_: wooden rectangular platform with the following dimension: 1.25x0.50x0.15 with mass 10 Kg.
- _WoodenPallet_: wooden rectangular pallet with the following dimension: 1.20x0.805x0.165 with mass 100 Kg.
- _WoodenCrate_: cubic crate with dimensions 0.4x0.4x0.4 and mass 15kg.
- _WoodenCrateSmall_: cubic crate with dimensions 0.2x0.2x0.2 and mass 10kg.
- _WoodCrate4_: wooden crate with dimensions 0.75x0.75x0.50 and mass 20 kg.
- _Stairs_: simple up-down stairs with mass 1000 kg.
- _BrickPile_: unique mesh of a pile bricks. Its mass is 45 kg,


# Examples of Generated Scenarios

<table>
    <tr>
        <td>
            <img src="https://github.com/ADVRHumanoids/world_generator/blob/main/examples/Example1.png?raw=true"/>
        </td>
        <td>
            <img src="https://github.com/ADVRHumanoids/world_generator/blob/main/examples/Example2.png?raw=true"/>
        </td>
    </tr>
    <tr>
        <td>
            <img src="https://github.com/ADVRHumanoids/world_generator/blob/main/examples/Example3.png?raw=true"/>
        </td>
        <td>
            <img src="https://github.com/ADVRHumanoids/world_generator/blob/main/examples/Example4.png?raw=true"/>
        </td>
    </tr>
</table>
