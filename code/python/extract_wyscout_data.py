#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script for extraction of transition probabilities (state to state) 
# from Wyscout football data (json).

# @author: Kevin Lynch <kevin.lynch@glasgow.ac.uk>

import pandas as pd
import numpy as np
import json
import time
import matplotlib.pyplot as plt


from draw_pitch import draw_pitch

zoneXYs = [
        [(50, 0),   (67, 100)],
        [(68, 0),    (83, 33)],
        [(68, 34),   (83, 66)],
        [(68, 67),  (83, 100)],
        [(84, 0),   (100, 33)],
        [(84, 34),  (100, 66)],
        [(84, 67), (100, 100)]
        ]

# alongside fromZoneY(), tells you if event originated in zone j
def fromZoneX(j, event):
    if (zoneXYs[j][0][0] <= (event['positions'][0]['x']) 
        and (event['positions'][0]['x']) <= zoneXYs[j][1][0]):
        return True
    else:
        return False

# alongside fromZoneX(), tells you if event originated in zone j    
def fromZoneY(j, event):
    if (zoneXYs[j][0][1] <= (event['positions'][0]['y']) 
        and (event['positions'][0]['y']) <= zoneXYs[j][1][1]):
        return True
    else:
        return False

# alongside toZoneY(), tells you if event ended in zone j    
def toZoneX(j, event):
    if (zoneXYs[j][0][0] <= (event['positions'][1]['x'])
        and (event['positions'][1]['x']) <= zoneXYs[j][1][0]):
        return True
    else:
        return False

# alsongside toZoneX(), tells you if event ended in zone j    
def toZoneY(j, event):
    if (zoneXYs[j][0][1] <= (event['positions'][1]['y'])
        and (event['positions'][1]['y']) <= zoneXYs[j][1][1]):
        return True
    else:
        return False
            
# fill a 2d array with instances of the ball moving s -> s'
def calculate_transition_matrix(filename):
    with open (filename) as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    shots = df[df['eventId'] == 10]
    passes = df[df['eventId'] == 8]
    
    # teams = df.teamId.unique()
    
    # eventsByTeam = {} 
    
    # for t in teams:
    #     eventsByTeam[str(t)] = df.loc[(df['teamId'] == t)]
        
    # populate transition matrix for goals (from open play)            
    for i, shot in shots.iterrows():        
        for tag in shot['tags']:
            if tag['id'] == 101:
                for j in range(0,7):
                    if fromZoneX(j, shot) and fromZoneY(j, shot):
                        trans_mat[j][8] += 1
            # and 'possession lost' from a shot
            else:
                for j in range(0,7):
                    if fromZoneX(j, shot) and fromZoneY(j, shot):
                        trans_mat[j][7] += 1
    
    # populate transition matrix for 'possession lost' from passes
    for i, aPass in passes.iterrows():
        for tag in aPass['tags']:
            if tag['id'] == 1802:
                for j in range(0,7):
                    if fromZoneX(j, aPass) and fromZoneY(j, aPass):
                        trans_mat[j][7] += 1
            # and terminal zones for each successful pass
            elif tag['id'] == 1801:
                for j in range(0,7):
                    if fromZoneX(j, aPass) and fromZoneY(j, aPass):
                        for k in range (0,7):
                            if toZoneX(k, aPass) and toZoneY(k, aPass):
                                trans_mat[j][k] += 1

# calculate probability of s -> s' 
def convert_to_probabilities():
    for i in range(0,7):
        transSum = sum(trans_mat[i])
        for j in range(0,9):
             trans_mat[i][j] = (trans_mat[i][j] / transSum)
             
# quick check that probabilities sum to 1
def check_sum_P():
    for i in range(0,7):
        print("S" + str(i) + ": " + str((sum(trans_mat[i]) == 1)) + " (" 
              + str((sum(trans_mat[i]))) + ")")

# transition matrix - trans_mat[state][state']
# trans_mat[..][7] is 'possession lost'
# trans_mat[..][8] is 'goal scored'
trans_mat = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

start = time.time()

calculate_transition_matrix("../../data/events_Italy.json")
calculate_transition_matrix("../../data/events_France.json")
calculate_transition_matrix("../../data/events_Spain.json")
calculate_transition_matrix("../../data/events_Germany.json")
calculate_transition_matrix("../../data/events_England.json")

convert_to_probabilities()

# fix for floating point error - all Ps must add to 1
trans_mat[3][0] += 0.0000000000000001

# double check!
check_sum_P()

print()
print(pd.DataFrame(trans_mat))
pd.DataFrame(trans_mat).to_csv("./probabilities.txt")   

end = time.time()
print("time elapsed: " + str(round(((end - start) / 60), 2)) 
      + " mins (approx)")

prismFile = open("../prism/markovchain.pm", "w");
prismFile.write("dtmc\n\nmodule possession\n\n\t" +
                "// state: i.e. area of the pitch where ball is" + 
                "in possession\n" + 
                "\ts : [0..8];\n" +
                "\t\t// 0 - 6: areas of the pitch\n" +
                "\t\t// 7    : posession lost\n" +
                "\t\t// 8    : goal scored\n\n" +
                "\t[] s=0 -> " + str(trans_mat[0][0]) + " : (s'=0) + " + 
                str(trans_mat[0][1]) + "  : (s'=1) + " + 
                str(trans_mat[0][2]) + "  : (s'=2) + " + 
                str(trans_mat[0][3]) + "  : (s'=3) + " + 
                str(trans_mat[0][4]) + "  : (s'=4) + " + 
                str(trans_mat[0][5]) + "  : (s'=5) + " + 
                str(trans_mat[0][6]) + "  : (s'=6) + " + 
                str(trans_mat[0][7]) + "  : (s'=7) + " + 
                str(trans_mat[0][8]) + "  : (s'=8);\n\t" +
                "[] s=1 -> " + str(trans_mat[1][0]) + " : (s'=0) + " + 
                str(trans_mat[1][1]) + "  : (s'=1) + " + 
                str(trans_mat[1][2]) + "  : (s'=2) + " + 
                str(trans_mat[1][3]) + "  : (s'=3) + " + 
                str(trans_mat[1][4]) + "  : (s'=4) + " + 
                str(trans_mat[1][5]) + "  : (s'=5) + " + 
                str(trans_mat[1][6]) + "  : (s'=6) + " + 
                str(trans_mat[1][7]) + "  : (s'=7) + " + 
                str(trans_mat[1][8]) + "  : (s'=8);\n\t" +
                "[] s=2 -> " + str(trans_mat[2][0]) + " : (s'=0) + " + 
                str(trans_mat[2][1]) + "  : (s'=1) + " + 
                str(trans_mat[2][2]) + "  : (s'=2) + " + 
                str(trans_mat[2][3]) + "  : (s'=3) + " + 
                str(trans_mat[2][4]) + "  : (s'=4) + " + 
                str(trans_mat[2][5]) + "  : (s'=5) + " + 
                str(trans_mat[2][6]) + "  : (s'=6) + " + 
                str(trans_mat[2][7]) + "  : (s'=7) + " + 
                str(trans_mat[2][8]) + "  : (s'=8);\n\t" +
                "[] s=3 -> " + str(trans_mat[3][0]) + " : (s'=0) + " + 
                str(trans_mat[3][1]) + "  : (s'=1) + " + 
                str(trans_mat[3][2]) + "  : (s'=2) + " + 
                str(trans_mat[3][3]) + "  : (s'=3) + " + 
                str(trans_mat[3][4]) + "  : (s'=4) + " + 
                str(trans_mat[3][5]) + "  : (s'=5) + " + 
                str(trans_mat[3][6]) + "  : (s'=6) + " + 
                str(trans_mat[3][7]) + "  : (s'=7) + " + 
                str(trans_mat[3][8]) + "  : (s'=8);\n\t" +
                "[] s=4 -> " + str(trans_mat[4][0]) + " : (s'=0) + " + 
                str(trans_mat[4][1]) + "  : (s'=1) + " + 
                str(trans_mat[4][2]) + "  : (s'=2) + " + 
                str(trans_mat[4][3]) + "  : (s'=3) + " + 
                str(trans_mat[4][4]) + "  : (s'=4) + " + 
                str(trans_mat[4][5]) + "  : (s'=5) + " + 
                str(trans_mat[4][6]) + "  : (s'=6) + " + 
                str(trans_mat[4][7]) + "  : (s'=7) + " + 
                str(trans_mat[4][8]) + "  : (s'=8);\n\t" +
                "[] s=5 -> " + str(trans_mat[5][0]) + "  : (s'=0) + " + 
                str(trans_mat[5][1]) + "  : (s'=1) + " + 
                str(trans_mat[5][2]) + "  : (s'=2) + " + 
                str(trans_mat[5][3]) + "  : (s'=3) + " + 
                str(trans_mat[5][4]) + "  : (s'=4) + " + 
                str(trans_mat[5][5]) + "  : (s'=5) + " + 
                str(trans_mat[5][6]) + "  : (s'=6) + " + 
                str(trans_mat[5][7]) + "  : (s'=7) + " + 
                str(trans_mat[5][8]) + "  : (s'=8);\n\t" +
                "[] s=6 -> " + str(trans_mat[6][0]) + " : (s'=0) + " + 
                str(trans_mat[6][1]) + "  : (s'=1) + " + 
                str(trans_mat[6][2]) + "  : (s'=2) + " + 
                str(trans_mat[6][3]) + "  : (s'=3) + " + 
                str(trans_mat[6][4]) + "  : (s'=4) + " + 
                str(trans_mat[6][5]) + "  : (s'=5) + " + 
                str(trans_mat[6][6]) + "  : (s'=6) + " + 
                str(trans_mat[6][7]) + "  : (s'=7) + " + 
                str(trans_mat[6][8]) + "  : (s'=8);\n\n" +
                "\t// absorbing states\n\t[] s=7 -> (s'=7);\n" +
                "\t[] s=8 -> (s'=8);\n\nendmodule")

prismFile.close()
