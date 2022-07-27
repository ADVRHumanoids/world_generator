import random
import math
import numpy as np

import sys
import yaml
from yaml.loader import SafeLoader

#Open Yaml file
with open('../config/generator.yaml') as f:
    yaml_generator = yaml.load(f, Loader=SafeLoader)

#Acquire world template
with open('../config/base/world_init.txt') as f:
      world_init = f.read()
with open('../config/base/world_state_init.txt') as f:
      world_state_init = f.read()
with open('../config/base/world_state_end.txt') as f:
      world_state_end = f.read()
with open('../config/base/world_end.txt') as f:
      world_end = f.read()

obj_states = []
obj_models = []

#Define Object Templates
with open('../config/obj/box_state.txt') as f:
      obj_states.insert(0, f.read())

with open('../config/obj/box_model.txt') as f:
      obj_models.insert(0, f.read())

#Define Wall Templates
with open('../config/obj/wall_model.txt') as f:
    wall_model = f.read()

with open('../config/obj/wall_state.txt') as f:
      wall_state = f.read()


def create_obj_state(file_obj, obj_id, n, px, py, pz, r, p ,y):
    file_obj.write(obj_states[obj_id] % (
        n, px, py, pz, r, p ,y, px, py, pz, r, p ,y
    ))
    
def create_obj_model(file_obj, obj_id, n, px, py, pz, r, p ,y, mass, ixx, ixy, ixz, iyy, iyz, izz, dim_x, dim_y, dim_z):
    file_obj.write(obj_models[obj_id] % (
        n, px, py, pz, r, p ,y, mass, ixx, ixy, ixz, iyy, iyz, izz, dim_x, dim_y, dim_z, dim_x, dim_y, dim_z
    ))

def create_walls_state(file_obj, yaml_generator):

    wall_thick = yaml_generator["WorldGen"]["wall"]["thickness"]
    short_width = yaml_generator["WorldGen"]["wall"]["offset_dist"]

    file_obj.write(wall_state % (
        0, yaml_generator["WorldGen"]["pos"]["min"][0] - short_width,
        (yaml_generator["WorldGen"]["pos"]["min"][1] + yaml_generator["WorldGen"]["pos"]["max"][1])/2,
        0,
        yaml_generator["WorldGen"]["pos"]["min"][0] - short_width,
        (yaml_generator["WorldGen"]["pos"]["min"][1] + yaml_generator["WorldGen"]["pos"]["max"][1])/2,
        0
    ))

    file_obj.write(wall_state % (
        1, yaml_generator["WorldGen"]["pos"]["max"][0] + short_width,
        (yaml_generator["WorldGen"]["pos"]["min"][1] + yaml_generator["WorldGen"]["pos"]["max"][1])/2,
        0,
        yaml_generator["WorldGen"]["pos"]["max"][0] + short_width,
        (yaml_generator["WorldGen"]["pos"]["min"][1] + yaml_generator["WorldGen"]["pos"]["max"][1])/2,
        0
    ))

    file_obj.write(wall_state % (
        2,
        (yaml_generator["WorldGen"]["pos"]["min"][0] + yaml_generator["WorldGen"]["pos"]["max"][0])/2,
        yaml_generator["WorldGen"]["pos"]["min"][1] - short_width/2,
        0,
        (yaml_generator["WorldGen"]["pos"]["min"][0] + yaml_generator["WorldGen"]["pos"]["max"][0])/2,
        yaml_generator["WorldGen"]["pos"]["min"][1] - wall_thick,
        0
    ))

    file_obj.write(wall_state % (
        3,
        (yaml_generator["WorldGen"]["pos"]["min"][0] + yaml_generator["WorldGen"]["pos"]["max"][0])/2,
        yaml_generator["WorldGen"]["pos"]["max"][1] + short_width/2,
        0,
        (yaml_generator["WorldGen"]["pos"]["min"][0] + yaml_generator["WorldGen"]["pos"]["max"][0])/2,
        yaml_generator["WorldGen"]["pos"]["max"][1] + wall_thick,
        0
    ))


def create_walls_model(file_obj, yaml_generator):

    wall_thick = yaml_generator["WorldGen"]["wall"]["thickness"]
    short_width = yaml_generator["WorldGen"]["wall"]["offset_dist"]

    file_obj.write(wall_model % (
        0, yaml_generator["WorldGen"]["pos"]["min"][0] - short_width,
        (yaml_generator["WorldGen"]["pos"]["min"][1] + yaml_generator["WorldGen"]["pos"]["max"][1])/2,
        0,
        wall_thick,
        (yaml_generator["WorldGen"]["pos"]["max"][1] - yaml_generator["WorldGen"]["dim"]["min"][1]) + short_width*2,
        wall_thick,
        (yaml_generator["WorldGen"]["pos"]["max"][1] - yaml_generator["WorldGen"]["dim"]["min"][1]) + short_width*2
    ))

    file_obj.write(wall_model % (
        1, yaml_generator["WorldGen"]["pos"]["max"][0] + short_width,
        (yaml_generator["WorldGen"]["pos"]["min"][1] + yaml_generator["WorldGen"]["pos"]["max"][1])/2,
        0,
        wall_thick,
        (yaml_generator["WorldGen"]["pos"]["max"][1] - yaml_generator["WorldGen"]["dim"]["min"][1]) + short_width*2,
        wall_thick,
        (yaml_generator["WorldGen"]["pos"]["max"][1] - yaml_generator["WorldGen"]["dim"]["min"][1]) + short_width*2
    ))

    file_obj.write(wall_model % (
        2,
        (yaml_generator["WorldGen"]["pos"]["min"][0] + yaml_generator["WorldGen"]["pos"]["max"][0])/2,
        yaml_generator["WorldGen"]["pos"]["min"][1] - wall_thick,
        0,
        (yaml_generator["WorldGen"]["pos"]["max"][0] - yaml_generator["WorldGen"]["dim"]["min"][0]) + short_width + wall_thick,
        wall_thick,
        (yaml_generator["WorldGen"]["pos"]["max"][0] - yaml_generator["WorldGen"]["dim"]["min"][0]) + short_width + wall_thick,
        wall_thick
    ))

    file_obj.write(wall_model % (
        3,
        (yaml_generator["WorldGen"]["pos"]["min"][0] + yaml_generator["WorldGen"]["pos"]["max"][0])/2,
        yaml_generator["WorldGen"]["pos"]["max"][1] + wall_thick,
        0,
        (yaml_generator["WorldGen"]["pos"]["max"][0] - yaml_generator["WorldGen"]["dim"]["min"][0]) + short_width + wall_thick,
        wall_thick,
        (yaml_generator["WorldGen"]["pos"]["max"][0] - yaml_generator["WorldGen"]["dim"]["min"][0]) + short_width + wall_thick,
        wall_thick
    ))



def rand_num(min_val, max_val):
    return random.uniform(min_val, max_val)

def main():
    f = open("../data/test_data.world", "w")

    # Init World
    f.write(world_init)
    f.write(world_state_init)

    pos_x = []
    pos_y = []
    
    dim_x = []
    dim_y = []
    dim_z = []

    yaw = []
    
      # Define Model in <state>
    for i in range(0, yaml_generator["WorldGen"]["num_objs"]):
        
        pos_x.insert(i, rand_num(yaml_generator["WorldGen"]["pos"]["min"][0], yaml_generator["WorldGen"]["pos"]["max"][0]))
        pos_y.insert(i, rand_num(yaml_generator["WorldGen"]["pos"]["min"][1], yaml_generator["WorldGen"]["pos"]["max"][1]))
                      
        dim_x.insert(i, rand_num(yaml_generator["WorldGen"]["dim"]["min"][0], yaml_generator["WorldGen"]["dim"]["max"][0]))
        dim_y.insert(i, rand_num(yaml_generator["WorldGen"]["dim"]["min"][1], yaml_generator["WorldGen"]["dim"]["max"][1]))
        dim_z.insert(i, rand_num(yaml_generator["WorldGen"]["dim"]["min"][2], yaml_generator["WorldGen"]["dim"]["max"][2]))
                      
        yaw.insert(i, rand_num(yaml_generator["WorldGen"]["rpy"]["min"][2], yaml_generator["WorldGen"]["rpy"]["max"][2]))
        
        create_obj_state(f, 0, i, pos_x[i], pos_y[i], dim_z[i]*0.5, 0, 0, yaw[i])

    #If Wall to be added
    if yaml_generator["WorldGen"]["wall"]["use_walls"]:
        create_walls_state(f, yaml_generator)

    # Close <state>
    f.write(world_state_end)

    # Define Models
    #TODO: mass and inertia
    for i in range(0, yaml_generator["WorldGen"]["num_objs"]):
        create_obj_model(f, 0, i, pos_x[i], pos_y[i], dim_z[i]*0.5, 0, 0, yaw[i], 1000, 166.7, 0, 0, 166.7, 0, 166.7, dim_x[i], dim_y[i], dim_z[i])

    #If Wall to be added
    if yaml_generator["WorldGen"]["wall"]["use_walls"]:
        create_walls_model(f, yaml_generator)

    # Close <world> and <sdf>
    f.write(world_end)
    
        
    f.close()
        
        

if __name__ == "__main__":
    main()
