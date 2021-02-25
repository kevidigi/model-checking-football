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

