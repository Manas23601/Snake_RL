import itertools
import json
import settings

def initialise_q_table(file_location, file_name):
    wall_snake_detect = [''.join(s) for s in list(itertools.product(*[['0','1']] * 4))]
    food_horizontal = ['L','R','NA']
    food_vertical = ['U','D','NA']

    states = {}
    for i in food_horizontal:
        for j in food_vertical:
            for k in wall_snake_detect:
                states[str((i,j,k))] = [0,0,0,0]

    with open("{0}{1}".format(file_location, file_name), "w") as f:
        json.dump(states, f)

    return

def LoadQvalues(file_location, path):
    with open("{0}{1}".format(file_location, path), "r") as f:
        qvalues = json.load(f)
    return qvalues

def SaveQvalues(file_location, path, qvalues):
    with open("{0}{1}".format(file_location, path), "w") as f:
        json.dump(qvalues, f)
    return