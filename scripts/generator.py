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

models_used = yaml_generator["WorldGen"]["models"]
models_fixed_inertia = yaml_generator["WorldGen"]["fixed_inertia"]
models_max_inst = yaml_generator["WorldGen"]["max_instances"]
curr_models_inst = [0]*len(models_max_inst)
max_calls = 1000

#Define Object Templates
for i in range(0, len(models_fixed_inertia)):
    with open('../config/obj/'+models_used[i]+'_state.txt') as f:
          obj_states.insert(i, f.read())

    with open('../config/obj/'+models_used[i]+'_model.txt') as f:
          obj_models.insert(i, f.read())

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

    if models_fixed_inertia[obj_id] == 1:
        file_obj.write(obj_models[obj_id] % (
            n, px, py, pz, r, p ,y
        ))
    else:
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

    rand_type = []
    curr_call = 0
    i = 0

    # Define Model in <state>
    while i < yaml_generator["WorldGen"]["num_objs"]:

        if len(models_used) > 1:
            rand_type.insert(i, random.randint(0, len(models_used)-1))
        else:
            rand_type.insert(i, 0)

        curr_models_inst[rand_type[i]] = curr_models_inst[rand_type[i]] +1

        if(models_max_inst[rand_type[i]] > 0 and curr_models_inst[rand_type[i]] > models_max_inst[rand_type[i]]):
            curr_call = curr_call + 1
            i = i -1
            if(curr_call > max_calls):
                i = yaml_generator["WorldGen"]["num_objs"]
        else:
            pos_x.insert(i, rand_num(yaml_generator["WorldGen"]["pos"]["min"][0], yaml_generator["WorldGen"]["pos"]["max"][0]))
            pos_y.insert(i, rand_num(yaml_generator["WorldGen"]["pos"]["min"][1], yaml_generator["WorldGen"]["pos"]["max"][1]))

            dim_x.insert(i, rand_num(yaml_generator["WorldGen"]["dim"]["min"][0], yaml_generator["WorldGen"]["dim"]["max"][0]))
            dim_y.insert(i, rand_num(yaml_generator["WorldGen"]["dim"]["min"][1], yaml_generator["WorldGen"]["dim"]["max"][1]))
            dim_z.insert(i, rand_num(yaml_generator["WorldGen"]["dim"]["min"][2], yaml_generator["WorldGen"]["dim"]["max"][2]))

            yaw.insert(i, rand_num(yaml_generator["WorldGen"]["rpy"]["min"][2], yaml_generator["WorldGen"]["rpy"]["max"][2]))

            create_obj_state(f, rand_type[i], i, pos_x[i], pos_y[i], dim_z[i]*0.5, 0, 0, yaw[i])

        i = i + 1

    #If Wall to be added
    if yaml_generator["WorldGen"]["wall"]["use_walls"]:
        create_walls_state(f, yaml_generator)

    # Close <state>
    f.write(world_state_end)

    # Define Models
    #TODO: mass and inertia
    for i in range(0, yaml_generator["WorldGen"]["num_objs"]):
        create_obj_model(f, rand_type[i], i, pos_x[i], pos_y[i], dim_z[i]*0.5, 0, 0, yaw[i], 1000, 166.7, 0, 0, 166.7, 0, 166.7, dim_x[i], dim_y[i], dim_z[i])

    #If Wall to be added
    if yaml_generator["WorldGen"]["wall"]["use_walls"]:
        create_walls_model(f, yaml_generator)

    # Close <world> and <sdf>
    f.write(world_end)
    
        
    f.close()
        
        

if __name__ == "__main__":
    main()
