#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script for extraction of transition probabilities (state to state) 
# from Wyscout football data (json). Transitions only occur via passes
# and shots for the purposes of my model.

# @author: Kevin Lynch <kevin.lynch@glasgow.ac.uk>

import pandas as pd
import json
import time

zoneXYs = [
        [(50,  0),   (67, 50)],     # zone 0
        [(50, 51),   (67,100)],     # zone 1
        [(68,  0),   (76, 17)],     # zone 2
        [(68, 18),   (76, 33)],     # zone 3
        [(68, 34),   (76, 50)],     # zone 4
        [(68, 51),   (76, 66)],     # zone 5
        [(68, 67),   (76, 83)],     # zone 6
        [(68, 84),   (76,100)],     # zone 7
        [(77,  0),   (83, 17)],     # zone 8
        [(77, 18),   (83, 33)],     # zone 9
        [(77, 34),   (83, 50)],     # zone 10
        [(77, 51),   (83, 66)],     # zone 11
        [(77, 67),   (83, 83)],     # zone 12
        [(77, 84),   (83,100)],     # zone 13
        [(84,  0),   (92, 17)],     # zone 14
        [(84, 18),   (92, 33)],     # zone 15
        [(84, 34),   (92, 50)],     # zone 16
        [(84, 51),   (92, 66)],     # zone 17
        [(84, 67),   (92, 83)],     # zone 18
        [(84, 84),   (92,100)],     # zone 19
        [(93,  0),  (100, 17)],     # zone 20
        [(93, 18),  (100, 33)],     # zone 21
        [(93, 34),  (100, 50)],     # zone 22
        [(93, 51),  (100, 66)],     # zone 23
        [(93, 67),  (100, 83)],     # zone 24
        [(93, 84),  (100,100)],     # zone 25
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
                for j in range(0,26):
                    if fromZoneX(j, shot) and fromZoneY(j, shot):
                        trans_mat[j][27] += 1
                        decision_mat[j][7] += 1
            # and 'possession lost' from a shot
            else:
                for j in range(0,26):
                    if fromZoneX(j, shot) and fromZoneY(j, shot):
                        trans_mat[j][26] += 1
                        decision_mat[j][26] += 1
    
    # populate transition matrix for 'possession lost' from passes
    for i, aPass in passes.iterrows():
        for tag in aPass['tags']:
            if tag['id'] == 1802:
                for j in range(0,26):
                    if fromZoneX(j, aPass) and fromZoneY(j, aPass):
                        trans_mat[j][26] += 1
                        for k in range (0,26):
                            if toZoneX(k, aPass) and toZoneY(k, aPass):
                                    decision_mat[j][k] += 1
            # and terminal zones for each successful pass
            elif tag['id'] == 1801:
                for j in range(0,26):
                    if fromZoneX(j, aPass) and fromZoneY(j, aPass):
                        for k in range (0,26):
                            if toZoneX(k, aPass) and toZoneY(k, aPass):
                                trans_mat[j][k] += 1
                                decision_mat[j][k] += 1

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
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
]

# pass from [i] to [j] or shoot ( [i][7] ) 
decision_mat = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

succ_mat = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

start = time.time()

calculate_transition_matrix("../../data/events_Italy.json")
calculate_transition_matrix("../../data/events_France.json")
calculate_transition_matrix("../../data/events_Spain.json")
calculate_transition_matrix("../../data/events_Germany.json")
calculate_transition_matrix("../../data/events_England.json")

print(pd.DataFrame(decision_mat))

for r in range (0,26):
    for c in range (0,26):
        if decision_mat[r][c] == 0:
            succ_mat[r][c] = 0
        else:
            succ_mat[r][c] = (trans_mat[r][c] / decision_mat[r][c])
        
    succ_mat[r][26] = trans_mat[r][27] / decision_mat[r][26]

convert_to_probabilities()

# fix for floating point error - all Ps must add to 1
trans_mat[3][0] += 0.0000000000000001

# double check!
check_sum_P()

print()
print(pd.DataFrame(trans_mat))
print()
print(pd.DataFrame(decision_mat))

print()
print("Probabilities of successful transition (not losing possession):")
print(pd.DataFrame(succ_mat))
print()

pd.DataFrame(trans_mat).to_csv("./probabilities_2.txt")   
pd.DataFrame(succ_mat).to_csv("./decision_success_2.txt")

end = time.time()
print("time elapsed: " + str(round(((end - start) / 60), 2)) 
      + " mins (approx)")

prismFile = open("../prism/markovdecisionprocess2.pm", "w");
prismFile.write("mdp\n\n" +
                "module passes_and_shots\n\n\t" +
                "// states: 0-25 = zones on the pitch; 26 = possession lost;" +
                " 27 = goal scored\n\t" +
                "s : [0..27];\n\t" +
                "// player actions from zone 0 (s=0)\n\t" +
                "[pass_0_0]\t      s=0 ->\n\t" +
                str(succ_mat[0][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[0][0]) + ") : (s'=26);\n\t" +
                "[pass_0_1]\t      s=0 ->\n\t" +
                str(succ_mat[0][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[0][1]) + ") : (s'=26);\n\t" +
                "[pass_0_2]\t      s=0 ->\n\t" +
                str(succ_mat[0][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[0][2]) + ") : (s'=26);\n\t" +
                "[pass_0_3]\t      s=0 ->\n\t" +
                str(succ_mat[0][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[0][3]) + ") : (s'=26);\n\t" +
                "[pass_0_4]\t      s=0 ->\n\t" +
                str(succ_mat[0][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[0][4]) + ") : (s'=26);\n\t" +
                "[pass_0_5]\t      s=0 ->\n\t" +
                str(succ_mat[0][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[0][5]) + ") : (s'=26);\n\t" +
                "[pass_0_6]\t      s=0 ->\n\t" +
                str(succ_mat[0][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[0][6]) + ") : (s'=26);\n\t" +
                "[pass_0_7]\t      s=0 ->\n\t" +
                str(succ_mat[0][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[0][7]) + ") : (s'=26);\n\t" +
                "[pass_0_8]\t      s=0 ->\n\t" +
                str(succ_mat[0][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[0][8]) + ") : (s'=26);\n\t" +
                "[pass_0_9]\t      s=0 ->\n\t" +
                str(succ_mat[0][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[0][9]) + ") : (s'=26);\n\t" +
                "[pass_0_10]\t      s=0 ->\n\t" +
                str(succ_mat[0][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[0][10]) + ") : (s'=26);\n\t" +
                "[pass_0_11]\t      s=0 ->\n\t" +
                str(succ_mat[0][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[0][11]) + ") : (s'=26);\n\t" +
                "[pass_0_12]\t      s=0 ->\n\t" +
                str(succ_mat[0][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[0][12]) + ") : (s'=26);\n\t" +
                "[pass_0_13]\t      s=0 ->\n\t" +
                str(succ_mat[0][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[0][13]) + ") : (s'=26);\n\t" +
                "[pass_0_14]\t      s=0 ->\n\t" +
                str(succ_mat[0][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[0][14]) + ") : (s'=26);\n\t" +
                "[pass_0_15]\t      s=0 ->\n\t" +
                str(succ_mat[0][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[0][15]) + ") : (s'=26);\n\t" +
                "[pass_0_16]\t      s=0 ->\n\t" +
                str(succ_mat[0][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[0][16]) + ") : (s'=26);\n\t" +
                "[pass_0_17]\t      s=0 ->\n\t" +
                str(succ_mat[0][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[0][17]) + ") : (s'=26);\n\t" +
                "[pass_0_18]\t      s=0 ->\n\t" +
                str(succ_mat[0][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[0][18]) + ") : (s'=26);\n\t" +
                "[pass_0_19]\t      s=0 ->\n\t" +
                str(succ_mat[0][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[0][19]) + ") : (s'=26);\n\t" +
                "[pass_0_20]\t      s=0 ->\n\t" +
                str(succ_mat[0][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[0][20]) + ") : (s'=26);\n\t" +
                "[pass_0_21]\t      s=0 ->\n\t" +
                str(succ_mat[0][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[0][21]) + ") : (s'=26);\n\t" +
                "[pass_0_22]\t      s=0 ->\n\t" +
                str(succ_mat[0][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[0][22]) + ") : (s'=26);\n\t" +
                "[pass_0_23]\t      s=0 ->\n\t" +
                str(succ_mat[0][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[0][23]) + ") : (s'=26);\n\t" +
                "[pass_0_24]\t      s=0 ->\n\t" +
                str(succ_mat[0][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[0][24]) + ") : (s'=26);\n\t" +
                "[pass_0_25]\t      s=0 ->\n\t" +
                str(succ_mat[0][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[0][25]) + ") : (s'=26);\n\t" +
                "[shoot_0]\t       s=0 ->\n\t" +
                str(succ_mat[0][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[0][26]) + ") : (s'=26);\n\n\t" +

                "// player actions from zone 1 (s=1)\n\t" +
                "[pass_1_0]\t      s=1 ->\n\t" +
                str(succ_mat[1][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[1][0]) + ") : (s'=26);\n\t" +
                "[pass_1_1]\t      s=1 ->\n\t" +
                str(succ_mat[1][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[1][1]) + ") : (s'=26);\n\t" +
                "[pass_1_2]\t      s=1 ->\n\t" +
                str(succ_mat[1][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[1][2]) + ") : (s'=26);\n\t" +
                "[pass_1_3]\t      s=1 ->\n\t" +
                str(succ_mat[1][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[1][3]) + ") : (s'=26);\n\t" +
                "[pass_1_4]\t      s=1 ->\n\t" +
                str(succ_mat[1][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[1][4]) + ") : (s'=26);\n\t" +
                "[pass_1_5]\t      s=1 ->\n\t" +
                str(succ_mat[1][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[1][5]) + ") : (s'=26);\n\t" +
                "[pass_1_6]\t      s=1 ->\n\t" +
                str(succ_mat[1][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[1][6]) + ") : (s'=26);\n\t" +
                "[pass_1_7]\t      s=1 ->\n\t" +
                str(succ_mat[1][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[1][7]) + ") : (s'=26);\n\t" +
                "[pass_1_8]\t      s=1 ->\n\t" +
                str(succ_mat[1][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[1][8]) + ") : (s'=26);\n\t" +
                "[pass_1_9]\t      s=1 ->\n\t" +
                str(succ_mat[1][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[1][9]) + ") : (s'=26);\n\t" +
                "[pass_1_10]\t      s=1 ->\n\t" +
                str(succ_mat[1][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[1][10]) + ") : (s'=26);\n\t" +
                "[pass_1_11]\t      s=1 ->\n\t" +
                str(succ_mat[1][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[1][11]) + ") : (s'=26);\n\t" +
                "[pass_1_12]\t      s=1 ->\n\t" +
                str(succ_mat[1][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[1][12]) + ") : (s'=26);\n\t" +
                "[pass_1_13]\t      s=1 ->\n\t" +
                str(succ_mat[1][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[1][13]) + ") : (s'=26);\n\t" +
                "[pass_1_14]\t      s=1 ->\n\t" +
                str(succ_mat[1][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[1][14]) + ") : (s'=26);\n\t" +
                "[pass_1_15]\t      s=1 ->\n\t" +
                str(succ_mat[1][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[1][15]) + ") : (s'=26);\n\t" +
                "[pass_1_16]\t      s=1 ->\n\t" +
                str(succ_mat[1][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[1][16]) + ") : (s'=26);\n\t" +
                "[pass_1_17]\t      s=1 ->\n\t" +
                str(succ_mat[1][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[1][17]) + ") : (s'=26);\n\t" +
                "[pass_1_18]\t      s=1 ->\n\t" +
                str(succ_mat[1][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[1][18]) + ") : (s'=26);\n\t" +
                "[pass_1_19]\t      s=1 ->\n\t" +
                str(succ_mat[1][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[1][19]) + ") : (s'=26);\n\t" +
                "[pass_1_20]\t      s=1 ->\n\t" +
                str(succ_mat[1][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[1][20]) + ") : (s'=26);\n\t" +
                "[pass_1_21]\t      s=1 ->\n\t" +
                str(succ_mat[1][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[1][21]) + ") : (s'=26);\n\t" +
                "[pass_1_22]\t      s=1 ->\n\t" +
                str(succ_mat[1][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[1][22]) + ") : (s'=26);\n\t" +
                "[pass_1_23]\t      s=1 ->\n\t" +
                str(succ_mat[1][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[1][23]) + ") : (s'=26);\n\t" +
                "[pass_1_24]\t      s=1 ->\n\t" +
                str(succ_mat[1][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[1][24]) + ") : (s'=26);\n\t" +
                "[pass_1_25]\t      s=1 ->\n\t" +
                str(succ_mat[1][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[1][25]) + ") : (s'=26);\n\t" +
                "[shoot_1]\t       s=1 ->\n\t" +
                str(succ_mat[1][26]) + " : (s'=27) + (1 - " 
                + str(succ_mat[1][26]) + ") : (s'=26);\n\n\t" +

                "// player actions from zone 2 (s=2)\n\t" +
                "[pass_2_0]\t      s=2 ->\n\t" +
                str(succ_mat[2][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[2][0]) + ") : (s'=26);\n\t" +
                "[pass_2_1]\t      s=2 ->\n\t" +
                str(succ_mat[2][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[2][1]) + ") : (s'=26);\n\t" +
                "[pass_2_2]\t      s=2 ->\n\t" +
                str(succ_mat[2][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[2][2]) + ") : (s'=26);\n\t" +
                "[pass_2_3]\t      s=2 ->\n\t" + 
                str(succ_mat[2][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[2][3]) + ") : (s'=26);\n\t" +
                "[pass_2_4]\t      s=2 ->\n\t" +
                str(succ_mat[2][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[2][4]) + ") : (s'=26);\n\t" +
                "[pass_2_5]\t      s=2 ->\n\t" +
                str(succ_mat[2][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[2][5]) + ") : (s'=26);\n\t" +
                "[pass_2_6]\t      s=2 ->\n\t" +
                str(succ_mat[2][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[2][6]) + ") : (s'=26);\n\t" +
                "[pass_2_7]\t      s=2 ->\n\t" +
                str(succ_mat[2][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[2][7]) + ") : (s'=26);\n\t" +
                "[pass_2_8]\t      s=2 ->\n\t" +
                str(succ_mat[2][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[2][8]) + ") : (s'=26);\n\t" +
                "[pass_2_9]\t      s=2 ->\n\t" +
                str(succ_mat[2][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[2][9]) + ") : (s'=26);\n\t" +
                "[pass_2_10]\t      s=2 ->\n\t" +
                str(succ_mat[2][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[2][10]) + ") : (s'=26);\n\t" +
                "[pass_2_11]\t      s=2 ->\n\t" +
                str(succ_mat[2][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[2][11]) + ") : (s'=26);\n\t" +
                "[pass_2_12]\t      s=2 ->\n\t" +
                str(succ_mat[2][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[2][12]) + ") : (s'=26);\n\t" +
                "[pass_2_13]\t      s=2 ->\n\t" +
                str(succ_mat[2][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[2][13]) + ") : (s'=26);\n\t" +
                "[pass_2_14]\t      s=2 ->\n\t" +
                str(succ_mat[2][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[2][14]) + ") : (s'=26);\n\t" +
                "[pass_2_15]\t      s=2 ->\n\t" +
                str(succ_mat[2][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[2][15]) + ") : (s'=26);\n\t" +
                "[pass_2_16]\t      s=2 ->\n\t" +
                str(succ_mat[2][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[2][16]) + ") : (s'=26);\n\t" +
                "[pass_2_17]\t      s=2 ->\n\t" +
                str(succ_mat[2][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[2][17]) + ") : (s'=26);\n\t" +
                "[pass_2_18]\t      s=2 ->\n\t" +
                str(succ_mat[2][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[2][18]) + ") : (s'=26);\n\t" +
                "[pass_2_19]\t      s=2 ->\n\t" +
                str(succ_mat[2][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[2][19]) + ") : (s'=26);\n\t" +
                "[pass_2_20]\t      s=2 ->\n\t" +
                str(succ_mat[2][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[2][20]) + ") : (s'=26);\n\t" +
                "[pass_2_21]\t      s=2 ->\n\t" +
                str(succ_mat[2][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[2][21]) + ") : (s'=26);\n\t" +
                "[pass_2_22]\t      s=2 ->\n\t" +
                str(succ_mat[2][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[2][22]) + ") : (s'=26);\n\t" +
                "[pass_2_23]\t      s=2 ->\n\t" +
                str(succ_mat[2][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[2][23]) + ") : (s'=26);\n\t" +
                "[pass_2_24]\t      s=2 ->\n\t" +
                str(succ_mat[2][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[2][24]) + ") : (s'=26);\n\t" +
                "[pass_2_25]\t      s=2 ->\n\t" +
                str(succ_mat[2][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[2][25]) + ") : (s'=26);\n\t" +
                "[shoot_2]\t       s=2 ->\n\t" +
                str(succ_mat[2][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[2][26]) + ") : (s'=26);\n\n\t" +

                "// player actions from zone 3 (s=3)\n\t" +
                "[pass_3_0]\t      s=3 ->\n\t" +
                str(succ_mat[3][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[3][0]) + ") : (s'=26);\n\t" +
                "[pass_3_1]\t      s=3 ->\n\t" +
                str(succ_mat[3][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[3][1]) + ") : (s'=26);\n\t" +
                "[pass_3_2]\t      s=3 ->\n\t" +
                str(succ_mat[3][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[3][2]) + ") : (s'=26);\n\t" +
                "[pass_3_3]\t      s=3 ->\n\t" +
                str(succ_mat[3][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[3][3]) + ") : (s'=26);\n\t" + 
                "[pass_3_4]\t      s=3 ->\n\t" +
                str(succ_mat[3][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[3][4]) + ") : (s'=26);\n\t" +
                "[pass_3_5]\t      s=3 ->\n\t" +
                str(succ_mat[3][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[3][5]) + ") : (s'=26);\n\t" +
                "[pass_3_6]\t      s=3 ->\n\t" +
                str(succ_mat[3][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[3][6]) + ") : (s'=26);\n\t" +
                "[pass_3_7]\t      s=3 ->\n\t" +
                str(succ_mat[3][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[3][7]) + ") : (s'=26);\n\t" +
                "[pass_3_8]\t      s=3 ->\n\t" +
                str(succ_mat[3][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[3][8]) + ") : (s'=26);\n\t" +
                "[pass_3_9]\t      s=3 ->\n\t" +
                str(succ_mat[3][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[3][9]) + ") : (s'=26);\n\t" +
                "[pass_3_10]\t      s=3 ->\n\t" +
                str(succ_mat[3][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[3][10]) + ") : (s'=26);\n\t" +
                "[pass_3_11]\t      s=3 ->\n\t" +
                str(succ_mat[3][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[3][11]) + ") : (s'=26);\n\t" +
                "[pass_3_12]\t      s=3 ->\n\t" +
                str(succ_mat[3][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[3][12]) + ") : (s'=26);\n\t" +
                "[pass_3_13]\t      s=3 ->\n\t" +
                str(succ_mat[3][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[3][13]) + ") : (s'=26);\n\t" +
                "[pass_3_14]\t      s=3 ->\n\t" +
                str(succ_mat[3][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[3][14]) + ") : (s'=26);\n\t" +
                "[pass_3_15]\t      s=3 ->\n\t" +
                str(succ_mat[3][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[3][15]) + ") : (s'=26);\n\t" +
                "[pass_3_16]\t      s=3 ->\n\t" +
                str(succ_mat[3][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[3][16]) + ") : (s'=26);\n\t" +
                "[pass_3_17]\t      s=3 ->\n\t" +
                str(succ_mat[3][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[3][17]) + ") : (s'=26);\n\t" +
                "[pass_3_18]\t      s=3 ->\n\t" +
                str(succ_mat[3][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[3][18]) + ") : (s'=26);\n\t" +
                "[pass_3_19]\t      s=3 ->\n\t" +
                str(succ_mat[3][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[3][19]) + ") : (s'=26);\n\t" +
                "[pass_3_20]\t      s=3 ->\n\t" +
                str(succ_mat[3][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[3][20]) + ") : (s'=26);\n\t" +
                "[pass_3_21]\t      s=3 ->\n\t" +
                str(succ_mat[3][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[3][21]) + ") : (s'=26);\n\t" +
                "[pass_3_22]\t      s=3 ->\n\t" +
                str(succ_mat[3][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[3][22]) + ") : (s'=26);\n\t" +
                "[pass_3_23]\t      s=3 ->\n\t" +
                str(succ_mat[3][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[3][23]) + ") : (s'=26);\n\t" +
                "[pass_3_24]\t      s=3 ->\n\t" +
                str(succ_mat[3][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[3][24]) + ") : (s'=26);\n\t" +
                "[pass_3_25]\t      s=3 ->\n\t" +
                str(succ_mat[3][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[3][25]) + ") : (s'=26);\n\t" +
                "[shoot_3]\t       s=3 ->\n\t" +
                str(succ_mat[3][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[3][26]) + ") : (s'=26);\n\n\t" +

                "// player actions from zone 4 (s=4)\n\t" +
                "[pass_4_0]\t      s=4 ->\n\t" +
                str(succ_mat[4][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[4][0]) + ") : (s'=26);\n\t" +
                "[pass_4_1]\t      s=4 ->\n\t" +
                str(succ_mat[4][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[4][1]) + ") : (s'=26);\n\t" +
                "[pass_4_2]\t      s=4 ->\n\t" +
                str(succ_mat[4][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[4][2]) + ") : (s'=26);\n\t" +
                "[pass_4_3]\t      s=4 ->\n\t" +
                str(succ_mat[4][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[4][3]) + ") : (s'=26);\n\t" +
                "[pass_4_4]\t      s=4 ->\n\t" +
                str(succ_mat[4][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[4][4]) + ") : (s'=26);\n\t" +
                "[pass_4_5]\t      s=4 ->\n\t" +
                str(succ_mat[4][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[4][5]) + ") : (s'=26);\n\t" +
                "[pass_4_6]\t      s=4 ->\n\t" +
                str(succ_mat[4][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[4][6]) + ") : (s'=26);\n\t" +
                "[pass_4_7]\t      s=4 ->\n\t" +
                str(succ_mat[4][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[4][7]) + ") : (s'=26);\n\t" +
                "[pass_4_8]\t      s=4 ->\n\t" +
                str(succ_mat[4][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[4][8]) + ") : (s'=26);\n\t" +
                "[pass_4_9]\t      s=4 ->\n\t" +
                str(succ_mat[4][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[4][9]) + ") : (s'=26);\n\t" +
                "[pass_4_10]\t      s=4 ->\n\t" +
                str(succ_mat[4][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[4][10]) + ") : (s'=26);\n\t" +
                "[pass_4_11]\t      s=4 ->\n\t" +
                str(succ_mat[4][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[4][11]) + ") : (s'=26);\n\t" +
                "[pass_4_12]\t      s=4 ->\n\t" +
                str(succ_mat[4][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[4][12]) + ") : (s'=26);\n\t" +
                "[pass_4_13]\t      s=4 ->\n\t" +
                str(succ_mat[4][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[4][13]) + ") : (s'=26);\n\t" +
                "[pass_4_14]\t      s=4 ->\n\t" +
                str(succ_mat[4][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[4][14]) + ") : (s'=26);\n\t" +
                "[pass_4_15]\t      s=4 ->\n\t" +
                str(succ_mat[4][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[4][15]) + ") : (s'=26);\n\t" +
                "[pass_4_16]\t      s=4 ->\n\t" +
                str(succ_mat[4][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[4][16]) + ") : (s'=26);\n\t" +
                "[pass_4_17]\t      s=4 ->\n\t" +
                str(succ_mat[4][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[4][17]) + ") : (s'=26);\n\t" +
                "[pass_4_18]\t      s=4 ->\n\t" +
                str(succ_mat[4][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[4][18]) + ") : (s'=26);\n\t" +
                "[pass_4_19]\t      s=4 ->\n\t" +
                str(succ_mat[4][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[4][19]) + ") : (s'=26);\n\t" +
                "[pass_4_20]\t      s=4 ->\n\t" +
                str(succ_mat[4][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[4][20]) + ") : (s'=26);\n\t" +
                "[pass_4_21]\t      s=4 ->\n\t" +
                str(succ_mat[4][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[4][21]) + ") : (s'=26);\n\t" +
                "[pass_4_22]\t      s=4 ->\n\t" +
                str(succ_mat[4][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[4][22]) + ") : (s'=26);\n\t" +
                "[pass_4_23]\t      s=4 ->\n\t" +
                str(succ_mat[4][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[4][23]) + ") : (s'=26);\n\t" +
                "[pass_4_24]\t      s=4 ->\n\t" +
                str(succ_mat[4][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[4][24]) + ") : (s'=26);\n\t" +
                "[pass_4_25]\t      s=4 ->\n\t" +
                str(succ_mat[4][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[4][25]) + ") : (s'=26);\n\t" +
                "[shoot_4]\t       s=4 ->\n\t" +
                str(succ_mat[4][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[4][26]) + ") : (s'=26);\n\n\t" +

                "// player actions from zone 5 (s=5)\n\t" +
                "[pass_5_0]\t      s=5 ->\n\t" +
                str(succ_mat[5][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[5][0]) + ") : (s'=26);\n\t" +
                "[pass_5_1]\t      s=5 ->\n\t" +
                str(succ_mat[5][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[5][1]) + ") : (s'=26);\n\t" +
                "[pass_5_2]\t      s=5 ->\n\t" +
                str(succ_mat[5][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[5][2]) + ") : (s'=26);\n\t" +
                "[pass_5_3]\t      s=5 ->\n\t" +
                str(succ_mat[5][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[5][3]) + ") : (s'=26);\n\t" +
                "[pass_5_4]\t      s=5 ->\n\t" + 
                str(succ_mat[5][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[5][4]) + ") : (s'=26);\n\t" +
                "[pass_5_5]\t      s=5 ->\n\t" +
                str(succ_mat[5][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[5][5]) + ") : (s'=26);\n\t" +
                "[pass_5_6]\t      s=5 ->\n\t" +
                str(succ_mat[5][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[5][6]) + ") : (s'=26);\n\t" +
                "[pass_5_7]\t      s=5 ->\n\t" +
                str(succ_mat[5][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[5][7]) + ") : (s'=26);\n\t" +
                "[pass_5_8]\t      s=5 ->\n\t" +
                str(succ_mat[5][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[5][8]) + ") : (s'=26);\n\t" +
                "[pass_5_9]\t      s=5 ->\n\t" +
                str(succ_mat[5][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[5][9]) + ") : (s'=26);\n\t" +
                "[pass_5_10]\t      s=5 ->\n\t" +
                str(succ_mat[5][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[5][10]) + ") : (s'=26);\n\t" +
                "[pass_5_11]\t      s=5 ->\n\t" +
                str(succ_mat[5][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[5][11]) + ") : (s'=26);\n\t" +
                "[pass_5_12]\t      s=5 ->\n\t" +
                str(succ_mat[5][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[5][12]) + ") : (s'=26);\n\t" +
                "[pass_5_13]\t      s=5 ->\n\t" +
                str(succ_mat[5][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[5][13]) + ") : (s'=26);\n\t" +
                "[pass_5_14]\t      s=5 ->\n\t" +
                str(succ_mat[5][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[5][14]) + ") : (s'=26);\n\t" +
                "[pass_5_15]\t      s=5 ->\n\t" +
                str(succ_mat[5][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[5][15]) + ") : (s'=26);\n\t" +
                "[pass_5_16]\t      s=5 ->\n\t" +
                str(succ_mat[5][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[5][16]) + ") : (s'=26);\n\t" +
                "[pass_5_17]\t      s=5 ->\n\t" +
                str(succ_mat[5][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[5][17]) + ") : (s'=26);\n\t" +
                "[pass_5_18]\t      s=5 ->\n\t" +
                str(succ_mat[5][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[5][18]) + ") : (s'=26);\n\t" +
                "[pass_5_19]\t      s=5 ->\n\t" +
                str(succ_mat[5][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[5][19]) + ") : (s'=26);\n\t" +
                "[pass_5_20]\t      s=5 ->\n\t" +
                str(succ_mat[5][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[5][20]) + ") : (s'=26);\n\t" +
                "[pass_5_21]\t      s=5 ->\n\t" +
                str(succ_mat[5][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[5][21]) + ") : (s'=26);\n\t" +
                "[pass_5_22]\t      s=5 ->\n\t" +
                str(succ_mat[5][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[5][22]) + ") : (s'=26);\n\t" +
                "[pass_5_23]\t      s=5 ->\n\t" +
                str(succ_mat[5][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[5][23]) + ") : (s'=26);\n\t" +
                "[pass_5_24]\t      s=5 ->\n\t" +
                str(succ_mat[5][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[5][24]) + ") : (s'=26);\n\t" +
                "[pass_5_25]\t      s=5 ->\n\t" +
                str(succ_mat[5][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[5][25]) + ") : (s'=26);\n\t" +
                "[shoot_5]\t       s=5 ->\n\t" +
                str(succ_mat[5][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[5][26]) + ") : (s'=26);\n\n\t" +

                "// player actions from zone 6 (s=6)\n\t" +
                "[pass_6_0]\t      s=6 ->\n\t" +
                str(succ_mat[6][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[6][0]) + ") : (s'=26);\n\t" +
                "[pass_6_1]\t      s=6 ->\n\t" +
                str(succ_mat[6][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[6][1]) + ") : (s'=26);\n\t" +
                "[pass_6_2]\t      s=6 ->\n\t" +
                str(succ_mat[6][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[6][2]) + ") : (s'=26);\n\t" +
                "[pass_6_3]\t      s=6 ->\n\t" +
                str(succ_mat[6][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[6][3]) + ") : (s'=26);\n\t" +
                "[pass_6_4]\t      s=6 ->\n\t" +
                str(succ_mat[6][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[6][4]) + ") : (s'=26);\n\t" +
                "[pass_6_5]\t      s=6 ->\n\t" +
                str(succ_mat[6][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[6][5]) + ") : (s'=26);\n\t" +
                "[pass_6_6]\t      s=6 ->\n\t" +
                str(succ_mat[6][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[6][6]) + ") : (s'=26);\n\t" +
                "[pass_6_7]\t      s=6 ->\n\t" +
                str(succ_mat[6][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[6][7]) + ") : (s'=26);\n\t" +
                "[pass_6_8]\t      s=6 ->\n\t" +
                str(succ_mat[6][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[6][8]) + ") : (s'=26);\n\t" +
                "[pass_6_9]\t      s=6 ->\n\t" +
                str(succ_mat[6][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[6][9]) + ") : (s'=26);\n\t" +
                "[pass_6_10]\t      s=6 ->\n\t" +
                str(succ_mat[6][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[6][10]) + ") : (s'=26);\n\t" +
                "[pass_6_11]\t      s=6 ->\n\t" +
                str(succ_mat[6][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[6][11]) + ") : (s'=26);\n\t" +
                "[pass_6_12]\t      s=6 ->\n\t" +
                str(succ_mat[6][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[6][12]) + ") : (s'=26);\n\t" +
                "[pass_6_13]\t      s=6 ->\n\t" +
                str(succ_mat[6][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[6][13]) + ") : (s'=26);\n\t" +
                "[pass_6_14]\t      s=6 ->\n\t" +
                str(succ_mat[6][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[6][14]) + ") : (s'=26);\n\t" +
                "[pass_6_15]\t      s=6 ->\n\t" +
                str(succ_mat[6][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[6][15]) + ") : (s'=26);\n\t" +
                "[pass_6_16]\t      s=6 ->\n\t" +
                str(succ_mat[6][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[6][16]) + ") : (s'=26);\n\t" +
                "[pass_6_17]\t      s=6 ->\n\t" +
                str(succ_mat[6][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[6][17]) + ") : (s'=26);\n\t" +
                "[pass_6_18]\t      s=6 ->\n\t" +
                str(succ_mat[6][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[6][18]) + ") : (s'=26);\n\t" +
                "[pass_6_19]\t      s=6 ->\n\t" +
                str(succ_mat[6][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[6][19]) + ") : (s'=26);\n\t" +
                "[pass_6_20]\t      s=6 ->\n\t" +
                str(succ_mat[6][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[6][20]) + ") : (s'=26);\n\t" +
                "[pass_6_21]\t      s=6 ->\n\t" +
                str(succ_mat[6][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[6][21]) + ") : (s'=26);\n\t" +
                "[pass_6_22]\t      s=6 ->\n\t" +
                str(succ_mat[6][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[6][22]) + ") : (s'=26);\n\t" +
                "[pass_6_23]\t      s=6 ->\n\t" +
                str(succ_mat[6][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[6][23]) + ") : (s'=26);\n\t" +
                "[pass_6_24]\t      s=6 ->\n\t" +
                str(succ_mat[6][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[6][24]) + ") : (s'=26);\n\t" +
                "[pass_6_25]\t      s=6 ->\n\t" +
                str(succ_mat[6][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[6][25]) + ") : (s'=26);\n\t" +
                "[shoot_6]\t       s=6 ->\n\t" +
                str(succ_mat[6][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[6][26]) + ") : (s'=26);\n\n\t" +

                "// player actions from zone 7 (s=7)\n\t" +
                "[pass_7_0]\t      s=7 ->\n\t" +
                str(succ_mat[7][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[7][0]) + ") : (s'=26);\n\t" +
                "[pass_7_1]\t      s=7 ->\n\t" +
                str(succ_mat[7][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[7][1]) + ") : (s'=26);\n\t" +
                "[pass_7_2]\t      s=7 ->\n\t" +
                str(succ_mat[7][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[7][2]) + ") : (s'=26);\n\t" +
                "[pass_7_3]\t      s=7 ->\n\t" +
                str(succ_mat[7][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[7][3]) + ") : (s'=26);\n\t" +
                "[pass_7_4]\t      s=7 ->\n\t" +
                str(succ_mat[7][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[7][4]) + ") : (s'=26);\n\t" +
                "[pass_7_5]\t      s=7 ->\n\t" +
                str(succ_mat[7][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[7][5]) + ") : (s'=26);\n\t" +
                "[pass_7_6]\t      s=7 ->\n\t" +
                str(succ_mat[7][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[7][6]) + ") : (s'=26);\n\t" +
                "[pass_7_7]\t      s=7 ->\n\t" +
                str(succ_mat[7][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[7][7]) + ") : (s'=26);\n\t" +
                "[pass_7_8]\t      s=7 ->\n\t" +
                str(succ_mat[7][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[7][8]) + ") : (s'=26);\n\t" +
                "[pass_7_9]\t      s=7 ->\n\t" +
                str(succ_mat[7][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[7][9]) + ") : (s'=26);\n\t" +
                "[pass_7_10]\t      s=7 ->\n\t" +
                str(succ_mat[7][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[7][10]) + ") : (s'=26);\n\t" +
                "[pass_7_11]\t      s=7 ->\n\t" +
                str(succ_mat[7][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[7][11]) + ") : (s'=26);\n\t" +
                "[pass_7_12]\t      s=7 ->\n\t" +
                str(succ_mat[7][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[7][12]) + ") : (s'=26);\n\t" +
                "[pass_7_13]\t      s=7 ->\n\t" +
                str(succ_mat[7][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[7][13]) + ") : (s'=26);\n\t" +
                "[pass_7_14]\t      s=7 ->\n\t" +
                str(succ_mat[7][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[7][14]) + ") : (s'=26);\n\t" +
                "[pass_7_15]\t      s=7 ->\n\t" +
                str(succ_mat[7][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[7][15]) + ") : (s'=26);\n\t" +
                "[pass_7_16]\t      s=7 ->\n\t" +
                str(succ_mat[7][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[7][16]) + ") : (s'=26);\n\t" +
                "[pass_7_17]\t      s=7 ->\n\t" +
                str(succ_mat[7][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[7][17]) + ") : (s'=26);\n\t" +
                "[pass_7_18]\t      s=7 ->\n\t" +
                str(succ_mat[7][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[7][18]) + ") : (s'=26);\n\t" +
                "[pass_7_19]\t      s=7 ->\n\t" +
                str(succ_mat[7][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[7][19]) + ") : (s'=26);\n\t" +
                "[pass_7_20]\t      s=7 ->\n\t" +
                str(succ_mat[7][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[7][20]) + ") : (s'=26);\n\t" +
                "[pass_7_21]\t      s=7 ->\n\t" +
                str(succ_mat[7][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[7][21]) + ") : (s'=26);\n\t" +
                "[pass_7_22]\t      s=7 ->\n\t" +
                str(succ_mat[7][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[7][22]) + ") : (s'=26);\n\t" +
                "[pass_7_23]\t      s=7 ->\n\t" +
                str(succ_mat[7][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[7][23]) + ") : (s'=26);\n\t" +
                "[pass_7_24]\t      s=7 ->\n\t" +
                str(succ_mat[7][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[7][24]) + ") : (s'=26);\n\t" +
                "[pass_7_25]\t      s=7 ->\n\t" +
                str(succ_mat[7][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[7][25]) + ") : (s'=26);\n\t" +
                "[shoot_7]\t       s=7 ->\n\t" +
                str(succ_mat[7][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[7][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 8 (s=8)\n\t" +
                "[pass_8_0]\t      s=8 ->\n\t" +
                str(succ_mat[8][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[8][0]) + ") : (s'=26);\n\t" +
                "[pass_8_1]\t      s=8 ->\n\t" +
                str(succ_mat[8][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[8][1]) + ") : (s'=26);\n\t" +
                "[pass_8_2]\t      s=8 ->\n\t" +
                str(succ_mat[8][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[8][2]) + ") : (s'=26);\n\t" +
                "[pass_8_3]\t      s=8 ->\n\t" +
                str(succ_mat[8][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[8][3]) + ") : (s'=26);\n\t" +
                "[pass_8_4]\t      s=8 ->\n\t" +
                str(succ_mat[8][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[8][4]) + ") : (s'=26);\n\t" +
                "[pass_8_5]\t      s=8 ->\n\t" +
                str(succ_mat[8][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[8][5]) + ") : (s'=26);\n\t" +
                "[pass_8_6]\t      s=8 ->\n\t" +
                str(succ_mat[8][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[8][6]) + ") : (s'=26);\n\t" +
                "[pass_8_7]\t      s=8 ->\n\t" +
                str(succ_mat[8][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[8][7]) + ") : (s'=26);\n\t" +
                "[pass_8_8]\t      s=8 ->\n\t" +
                str(succ_mat[8][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[8][8]) + ") : (s'=26);\n\t" +
                "[pass_8_9]\t      s=8 ->\n\t" +
                str(succ_mat[8][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[8][9]) + ") : (s'=26);\n\t" +
                "[pass_8_10]\t      s=8 ->\n\t" +
                str(succ_mat[8][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[8][10]) + ") : (s'=26);\n\t" +
                "[pass_8_11]\t      s=8 ->\n\t" +
                str(succ_mat[8][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[8][11]) + ") : (s'=26);\n\t" +
                "[pass_8_12]\t      s=8 ->\n\t" +
                str(succ_mat[8][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[8][12]) + ") : (s'=26);\n\t" +
                "[pass_8_13]\t      s=8 ->\n\t" +
                str(succ_mat[8][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[8][13]) + ") : (s'=26);\n\t" +
                "[pass_8_14]\t      s=8 ->\n\t" +
                str(succ_mat[8][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[8][14]) + ") : (s'=26);\n\t" +
                "[pass_8_15]\t      s=8 ->\n\t" +
                str(succ_mat[8][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[8][15]) + ") : (s'=26);\n\t" +
                "[pass_8_16]\t      s=8 ->\n\t" +
                str(succ_mat[8][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[8][16]) + ") : (s'=26);\n\t" +
                "[pass_8_17]\t      s=8 ->\n\t" +
                str(succ_mat[8][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[8][17]) + ") : (s'=26);\n\t" +
                "[pass_8_18]\t      s=8 ->\n\t" +
                str(succ_mat[8][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[8][18]) + ") : (s'=26);\n\t" +
                "[pass_8_19]\t      s=8 ->\n\t" +
                str(succ_mat[8][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[8][19]) + ") : (s'=26);\n\t" +
                "[pass_8_20]\t      s=8 ->\n\t" +
                str(succ_mat[8][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[8][20]) + ") : (s'=26);\n\t" +
                "[pass_8_21]\t      s=8 ->\n\t" +
                str(succ_mat[8][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[8][21]) + ") : (s'=26);\n\t" +
                "[pass_8_22]\t      s=8 ->\n\t" +
                str(succ_mat[8][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[8][22]) + ") : (s'=26);\n\t" +
                "[pass_8_23]\t      s=8 ->\n\t" +
                str(succ_mat[8][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[8][23]) + ") : (s'=26);\n\t" +
                "[pass_8_24]\t      s=8 ->\n\t" +
                str(succ_mat[8][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[8][24]) + ") : (s'=26);\n\t" +
                "[pass_8_25]\t      s=8 ->\n\t" +
                str(succ_mat[8][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[8][25]) + ") : (s'=26);\n\t" +
                "[shoot_8]\t       s=8 ->\n\t" +
                str(succ_mat[8][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[8][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 9 (s=9)\n\t" +
                "[pass_9_0]\t      s=9 ->\n\t" +
                str(succ_mat[9][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[9][0]) + ") : (s'=26);\n\t" +
                "[pass_9_1]\t      s=9 ->\n\t" +
                str(succ_mat[9][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[9][1]) + ") : (s'=26);\n\t" +
                "[pass_9_2]\t      s=9 ->\n\t" +
                str(succ_mat[9][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[9][2]) + ") : (s'=26);\n\t" +
                "[pass_9_3]\t      s=9 ->\n\t" +
                str(succ_mat[9][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[9][3]) + ") : (s'=26);\n\t" +
                "[pass_9_4]\t      s=9 ->\n\t" +
                str(succ_mat[9][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[9][4]) + ") : (s'=26);\n\t" +
                "[pass_9_5]\t      s=9 ->\n\t" +
                str(succ_mat[9][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[9][5]) + ") : (s'=26);\n\t" +
                "[pass_9_6]\t      s=9 ->\n\t" +
                str(succ_mat[9][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[9][6]) + ") : (s'=26);\n\t" +
                "[pass_9_7]\t      s=9 ->\n\t" +
                str(succ_mat[9][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[9][7]) + ") : (s'=26);\n\t" +
                "[pass_9_8]\t      s=9 ->\n\t" +
                str(succ_mat[9][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[9][8]) + ") : (s'=26);\n\t" +
                "[pass_9_9]\t      s=9 ->\n\t" +
                str(succ_mat[9][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[9][9]) + ") : (s'=26);\n\t" +
                "[pass_9_10]\t      s=9 ->\n\t" +
                str(succ_mat[9][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[9][10]) + ") : (s'=26);\n\t" +
                "[pass_9_11]\t      s=9 ->\n\t" +
                str(succ_mat[9][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[9][11]) + ") : (s'=26);\n\t" +
                "[pass_9_12]\t      s=9 ->\n\t" +
                str(succ_mat[9][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[9][12]) + ") : (s'=26);\n\t" +
                "[pass_9_13]\t      s=9 ->\n\t" +
                str(succ_mat[9][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[9][13]) + ") : (s'=26);\n\t" +
                "[pass_9_14]\t      s=9 ->\n\t" +
                str(succ_mat[9][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[9][14]) + ") : (s'=26);\n\t" +
                "[pass_9_15]\t      s=9 ->\n\t" +
                str(succ_mat[9][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[9][15]) + ") : (s'=26);\n\t" +
                "[pass_9_16]\t      s=9 ->\n\t" +
                str(succ_mat[9][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[9][16]) + ") : (s'=26);\n\t" +
                "[pass_9_17]\t      s=9 ->\n\t" +
                str(succ_mat[9][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[9][17]) + ") : (s'=26);\n\t" +
                "[pass_9_18]\t      s=9 ->\n\t" +
                str(succ_mat[9][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[9][18]) + ") : (s'=26);\n\t" +
                "[pass_9_19]\t      s=9 ->\n\t" +
                str(succ_mat[9][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[9][19]) + ") : (s'=26);\n\t" +
                "[pass_9_20]\t      s=9 ->\n\t" +
                str(succ_mat[9][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[9][20]) + ") : (s'=26);\n\t" +
                "[pass_9_21]\t      s=9 ->\n\t" +
                str(succ_mat[9][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[9][21]) + ") : (s'=26);\n\t" +
                "[pass_9_22]\t      s=9 ->\n\t" +
                str(succ_mat[9][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[9][22]) + ") : (s'=26);\n\t" +
                "[pass_9_23]\t      s=9 ->\n\t" +
                str(succ_mat[9][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[9][23]) + ") : (s'=26);\n\t" +
                "[pass_9_24]\t      s=9 ->\n\t" +
                str(succ_mat[9][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[9][24]) + ") : (s'=26);\n\t" +
                "[pass_9_25]\t      s=9 ->\n\t" +
                str(succ_mat[9][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[9][25]) + ") : (s'=26);\n\t" +
                "[shoot_9]\t       s=9 ->\n\t" +
                str(succ_mat[9][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[9][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 10 (s=10)\n\t" +
                "[pass_10_0]\t      s=10 ->\n\t" +
                str(succ_mat[10][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[10][0]) + ") : (s'=26);\n\t" +
                "[pass_10_1]\t      s=10 ->\n\t" +
                str(succ_mat[10][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[10][1]) + ") : (s'=26);\n\t" +
                "[pass_10_2]\t      s=10 ->\n\t" +
                str(succ_mat[10][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[10][2]) + ") : (s'=26);\n\t" +
                "[pass_10_3]\t      s=10 ->\n\t" +
                str(succ_mat[10][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[10][3]) + ") : (s'=26);\n\t" +
                "[pass_10_4]\t      s=10 ->\n\t" +
                str(succ_mat[10][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[10][4]) + ") : (s'=26);\n\t" +
                "[pass_10_5]\t      s=10 ->\n\t" +
                str(succ_mat[10][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[10][5]) + ") : (s'=26);\n\t" +
                "[pass_10_6]\t      s=10 ->\n\t" +
                str(succ_mat[10][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[10][6]) + ") : (s'=26);\n\t" +
                "[pass_10_7]\t      s=10 ->\n\t" +
                str(succ_mat[10][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[10][7]) + ") : (s'=26);\n\t" +
                "[pass_10_8]\t      s=10 ->\n\t" +
                str(succ_mat[10][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[10][8]) + ") : (s'=26);\n\t" +
                "[pass_10_9]\t      s=10 ->\n\t" +
                str(succ_mat[10][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[10][9]) + ") : (s'=26);\n\t" +
                "[pass_10_10]\t      s=10 ->\n\t" +
                str(succ_mat[10][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[10][10]) + ") : (s'=26);\n\t" +
                "[pass_10_11]\t      s=10 ->\n\t" +
                str(succ_mat[10][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[10][11]) + ") : (s'=26);\n\t" +
                "[pass_10_12]\t      s=10 ->\n\t" +
                str(succ_mat[10][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[10][12]) + ") : (s'=26);\n\t" +
                "[pass_10_13]\t      s=10 ->\n\t" +
                str(succ_mat[10][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[10][13]) + ") : (s'=26);\n\t" +
                "[pass_10_14]\t      s=10 ->\n\t" +
                str(succ_mat[10][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[10][14]) + ") : (s'=26);\n\t" +
                "[pass_10_15]\t      s=10 ->\n\t" +
                str(succ_mat[10][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[10][15]) + ") : (s'=26);\n\t" +
                "[pass_10_16]\t      s=10 ->\n\t" +
                str(succ_mat[10][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[10][16]) + ") : (s'=26);\n\t" +
                "[pass_10_17]\t      s=10 ->\n\t" +
                str(succ_mat[10][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[10][17]) + ") : (s'=26);\n\t" +
                "[pass_10_18]\t      s=10 ->\n\t" +
                str(succ_mat[10][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[10][18]) + ") : (s'=26);\n\t" +
                "[pass_10_19]\t      s=10 ->\n\t" +
                str(succ_mat[10][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[10][19]) + ") : (s'=26);\n\t" +
                "[pass_10_20]\t      s=10 ->\n\t" +
                str(succ_mat[10][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[10][20]) + ") : (s'=26);\n\t" +
                "[pass_10_21]\t      s=10 ->\n\t" +
                str(succ_mat[10][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[10][21]) + ") : (s'=26);\n\t" +
                "[pass_10_22]\t      s=10 ->\n\t" +
                str(succ_mat[10][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[10][22]) + ") : (s'=26);\n\t" +
                "[pass_10_23]\t      s=10 ->\n\t" +
                str(succ_mat[10][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[10][23]) + ") : (s'=26);\n\t" +
                "[pass_10_24]\t      s=10 ->\n\t" +
                str(succ_mat[10][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[10][24]) + ") : (s'=26);\n\t" +
                "[pass_10_25]\t      s=10 ->\n\t" +
                str(succ_mat[10][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[10][25]) + ") : (s'=26);\n\t" +
                "[shoot_10]\t       s=10 ->\n\t" +
                str(succ_mat[10][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[10][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 11 (s=11)\n\t" +
                "[pass_11_0]\t      s=11 ->\n\t" +
                str(succ_mat[11][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[11][0]) + ") : (s'=26);\n\t" +
                "[pass_11_1]\t      s=11 ->\n\t" +
                str(succ_mat[11][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[11][1]) + ") : (s'=26);\n\t" +
                "[pass_11_2]\t      s=11 ->\n\t" +
                str(succ_mat[11][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[11][2]) + ") : (s'=26);\n\t" +
                "[pass_11_3]\t      s=11 ->\n\t" +
                str(succ_mat[11][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[11][3]) + ") : (s'=26);\n\t" +
                "[pass_11_4]\t      s=11 ->\n\t" +
                str(succ_mat[11][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[11][4]) + ") : (s'=26);\n\t" +
                "[pass_11_5]\t      s=11 ->\n\t" +
                str(succ_mat[11][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[11][5]) + ") : (s'=26);\n\t" +
                "[pass_11_6]\t      s=11 ->\n\t" +
                str(succ_mat[11][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[11][6]) + ") : (s'=26);\n\t" +
                "[pass_11_7]\t      s=11 ->\n\t" +
                str(succ_mat[11][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[11][7]) + ") : (s'=26);\n\t" +
                "[pass_11_8]\t      s=11 ->\n\t" +
                str(succ_mat[11][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[11][8]) + ") : (s'=26);\n\t" +
                "[pass_11_9]\t      s=11 ->\n\t" +
                str(succ_mat[11][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[11][9]) + ") : (s'=26);\n\t" +
                "[pass_11_10]\t      s=11 ->\n\t" +
                str(succ_mat[11][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[11][10]) + ") : (s'=26);\n\t" +
                "[pass_11_11]\t      s=11 ->\n\t" +
                str(succ_mat[11][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[11][11]) + ") : (s'=26);\n\t" +
                "[pass_11_12]\t      s=11 ->\n\t" +
                str(succ_mat[11][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[11][12]) + ") : (s'=26);\n\t" +
                "[pass_11_13]\t      s=11 ->\n\t" +
                str(succ_mat[11][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[11][13]) + ") : (s'=26);\n\t" +
                "[pass_11_14]\t      s=11 ->\n\t" +
                str(succ_mat[11][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[11][14]) + ") : (s'=26);\n\t" +
                "[pass_11_15]\t      s=11 ->\n\t" +
                str(succ_mat[11][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[11][15]) + ") : (s'=26);\n\t" +
                "[pass_11_16]\t      s=11 ->\n\t" +
                str(succ_mat[11][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[11][16]) + ") : (s'=26);\n\t" +
                "[pass_11_17]\t      s=11 ->\n\t" +
                str(succ_mat[11][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[11][17]) + ") : (s'=26);\n\t" +
                "[pass_11_18]\t      s=11 ->\n\t" +
                str(succ_mat[11][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[11][18]) + ") : (s'=26);\n\t" +
                "[pass_11_19]\t      s=11 ->\n\t" +
                str(succ_mat[11][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[11][19]) + ") : (s'=26);\n\t" +
                "[pass_11_20]\t      s=11 ->\n\t" +
                str(succ_mat[11][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[11][20]) + ") : (s'=26);\n\t" +
                "[pass_11_21]\t      s=11 ->\n\t" +
                str(succ_mat[11][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[11][21]) + ") : (s'=26);\n\t" +
                "[pass_11_22]\t      s=11 ->\n\t" +
                str(succ_mat[11][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[11][22]) + ") : (s'=26);\n\t" +
                "[pass_11_23]\t      s=11 ->\n\t" +
                str(succ_mat[11][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[11][23]) + ") : (s'=26);\n\t" +
                "[pass_11_24]\t      s=11 ->\n\t" +
                str(succ_mat[11][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[11][24]) + ") : (s'=26);\n\t" +
                "[pass_11_25]\t      s=11 ->\n\t" +
                str(succ_mat[11][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[11][25]) + ") : (s'=26);\n\t" +
                "[shoot_11]\t       s=11 ->\n\t" +
                str(succ_mat[11][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[11][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 12 (s=12)\n\t" +
                "[pass_12_0]\t      s=12 ->\n\t" +
                str(succ_mat[12][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[12][0]) + ") : (s'=26);\n\t" +
                "[pass_12_1]\t      s=12 ->\n\t" +
                str(succ_mat[12][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[12][1]) + ") : (s'=26);\n\t" +
                "[pass_12_2]\t      s=12 ->\n\t" +
                str(succ_mat[12][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[12][2]) + ") : (s'=26);\n\t" +
                "[pass_12_3]\t      s=12 ->\n\t" +
                str(succ_mat[12][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[12][3]) + ") : (s'=26);\n\t" +
                "[pass_12_4]\t      s=12 ->\n\t" +
                str(succ_mat[12][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[12][4]) + ") : (s'=26);\n\t" +
                "[pass_12_5]\t      s=12 ->\n\t" +
                str(succ_mat[12][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[12][5]) + ") : (s'=26);\n\t" +
                "[pass_12_6]\t      s=12 ->\n\t" +
                str(succ_mat[12][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[12][6]) + ") : (s'=26);\n\t" +
                "[pass_12_7]\t      s=12 ->\n\t" +
                str(succ_mat[12][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[12][7]) + ") : (s'=26);\n\t" +
                "[pass_12_8]\t      s=12 ->\n\t" +
                str(succ_mat[12][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[12][8]) + ") : (s'=26);\n\t" +
                "[pass_12_9]\t      s=12 ->\n\t" +
                str(succ_mat[12][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[12][9]) + ") : (s'=26);\n\t" +
                "[pass_12_10]\t      s=12 ->\n\t" +
                str(succ_mat[12][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[12][10]) + ") : (s'=26);\n\t" +
                "[pass_12_11]\t      s=12 ->\n\t" +
                str(succ_mat[12][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[12][11]) + ") : (s'=26);\n\t" +
                "[pass_12_12]\t      s=12 ->\n\t" +
                str(succ_mat[12][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[12][12]) + ") : (s'=26);\n\t" +
                "[pass_12_13]\t      s=12 ->\n\t" +
                str(succ_mat[12][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[12][13]) + ") : (s'=26);\n\t" +
                "[pass_12_14]\t      s=12 ->\n\t" +
                str(succ_mat[12][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[12][14]) + ") : (s'=26);\n\t" +
                "[pass_12_15]\t      s=12 ->\n\t" +
                str(succ_mat[12][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[12][15]) + ") : (s'=26);\n\t" +
                "[pass_12_16]\t      s=12 ->\n\t" +
                str(succ_mat[12][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[12][16]) + ") : (s'=26);\n\t" +
                "[pass_12_17]\t      s=12 ->\n\t" +
                str(succ_mat[12][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[12][17]) + ") : (s'=26);\n\t" +
                "[pass_12_18]\t      s=12 ->\n\t" +
                str(succ_mat[12][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[12][18]) + ") : (s'=26);\n\t" +
                "[pass_12_19]\t      s=12 ->\n\t" +
                str(succ_mat[12][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[12][19]) + ") : (s'=26);\n\t" +
                "[pass_12_20]\t      s=12 ->\n\t" +
                str(succ_mat[12][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[12][20]) + ") : (s'=26);\n\t" +
                "[pass_12_21]\t      s=12 ->\n\t" +
                str(succ_mat[12][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[12][21]) + ") : (s'=26);\n\t" +
                "[pass_12_22]\t      s=12 ->\n\t" +
                str(succ_mat[12][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[12][22]) + ") : (s'=26);\n\t" +
                "[pass_12_23]\t      s=12 ->\n\t" +
                str(succ_mat[12][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[12][23]) + ") : (s'=26);\n\t" +
                "[pass_12_24]\t      s=12 ->\n\t" +
                str(succ_mat[12][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[12][24]) + ") : (s'=26);\n\t" +
                "[pass_12_25]\t      s=12 ->\n\t" +
                str(succ_mat[12][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[12][25]) + ") : (s'=26);\n\t" +
                "[shoot_12]\t       s=12 ->\n\t" +
                str(succ_mat[12][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[12][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 13 (s=13)\n\t" +
                "[pass_13_0]\t      s=13 ->\n\t" +
                str(succ_mat[13][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[13][0]) + ") : (s'=26);\n\t" +
                "[pass_13_1]\t      s=13 ->\n\t" +
                str(succ_mat[13][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[13][1]) + ") : (s'=26);\n\t" +
                "[pass_13_2]\t      s=13 ->\n\t" +
                str(succ_mat[13][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[13][2]) + ") : (s'=26);\n\t" +
                "[pass_13_3]\t      s=13 ->\n\t" +
                str(succ_mat[13][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[13][3]) + ") : (s'=26);\n\t" +
                "[pass_13_4]\t      s=13 ->\n\t" +
                str(succ_mat[13][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[13][4]) + ") : (s'=26);\n\t" +
                "[pass_13_5]\t      s=13 ->\n\t" +
                str(succ_mat[13][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[13][5]) + ") : (s'=26);\n\t" +
                "[pass_13_6]\t      s=13 ->\n\t" +
                str(succ_mat[13][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[13][6]) + ") : (s'=26);\n\t" +
                "[pass_13_7]\t      s=13 ->\n\t" +
                str(succ_mat[13][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[13][7]) + ") : (s'=26);\n\t" +
                "[pass_13_8]\t      s=13 ->\n\t" +
                str(succ_mat[13][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[13][8]) + ") : (s'=26);\n\t" +
                "[pass_13_9]\t      s=13 ->\n\t" +
                str(succ_mat[13][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[13][9]) + ") : (s'=26);\n\t" +
                "[pass_13_10]\t      s=13 ->\n\t" +
                str(succ_mat[13][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[13][10]) + ") : (s'=26);\n\t" +
                "[pass_13_11]\t      s=13 ->\n\t" +
                str(succ_mat[13][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[13][11]) + ") : (s'=26);\n\t" +
                "[pass_13_12]\t      s=13 ->\n\t" +
                str(succ_mat[13][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[13][12]) + ") : (s'=26);\n\t" +
                "[pass_13_13]\t      s=13 ->\n\t" +
                str(succ_mat[13][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[13][13]) + ") : (s'=26);\n\t" +
                "[pass_13_14]\t      s=13 ->\n\t" +
                str(succ_mat[13][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[13][14]) + ") : (s'=26);\n\t" +
                "[pass_13_15]\t      s=13 ->\n\t" +
                str(succ_mat[13][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[13][15]) + ") : (s'=26);\n\t" +
                "[pass_13_16]\t      s=13 ->\n\t" +
                str(succ_mat[13][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[13][16]) + ") : (s'=26);\n\t" +
                "[pass_13_17]\t      s=13 ->\n\t" +
                str(succ_mat[13][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[13][17]) + ") : (s'=26);\n\t" +
                "[pass_13_18]\t      s=13 ->\n\t" +
                str(succ_mat[13][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[13][18]) + ") : (s'=26);\n\t" +
                "[pass_13_19]\t      s=13 ->\n\t" +
                str(succ_mat[13][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[13][19]) + ") : (s'=26);\n\t" +
                "[pass_13_20]\t      s=13 ->\n\t" +
                str(succ_mat[13][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[13][20]) + ") : (s'=26);\n\t" +
                "[pass_13_21]\t      s=13 ->\n\t" +
                str(succ_mat[13][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[13][21]) + ") : (s'=26);\n\t" +
                "[pass_13_22]\t      s=13 ->\n\t" +
                str(succ_mat[13][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[13][22]) + ") : (s'=26);\n\t" +
                "[pass_13_23]\t      s=13 ->\n\t" +
                str(succ_mat[13][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[13][23]) + ") : (s'=26);\n\t" +
                "[pass_13_24]\t      s=13 ->\n\t" +
                str(succ_mat[13][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[13][24]) + ") : (s'=26);\n\t" +
                "[pass_13_25]\t      s=13 ->\n\t" +
                str(succ_mat[13][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[13][25]) + ") : (s'=26);\n\t" +
                "[shoot_13]\t       s=13 ->\n\t" +
                str(succ_mat[13][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[13][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 14 (s=14)\n\t" +
                "[pass_14_0]\t      s=14 ->\n\t" +
                str(succ_mat[14][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[14][0]) + ") : (s'=26);\n\t" +
                "[pass_14_1]\t      s=14 ->\n\t" +
                str(succ_mat[14][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[14][1]) + ") : (s'=26);\n\t" +
                "[pass_14_2]\t      s=14 ->\n\t" +
                str(succ_mat[14][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[14][2]) + ") : (s'=26);\n\t" +
                "[pass_14_3]\t      s=14 ->\n\t" +
                str(succ_mat[14][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[14][3]) + ") : (s'=26);\n\t" +
                "[pass_14_4]\t      s=14 ->\n\t" +
                str(succ_mat[14][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[14][4]) + ") : (s'=26);\n\t" +
                "[pass_14_5]\t      s=14 ->\n\t" +
                str(succ_mat[14][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[14][5]) + ") : (s'=26);\n\t" +
                "[pass_14_6]\t      s=14 ->\n\t" +
                str(succ_mat[14][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[14][6]) + ") : (s'=26);\n\t" +
                "[pass_14_7]\t      s=14 ->\n\t" +
                str(succ_mat[14][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[14][7]) + ") : (s'=26);\n\t" +
                "[pass_14_8]\t      s=14 ->\n\t" +
                str(succ_mat[14][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[14][8]) + ") : (s'=26);\n\t" +
                "[pass_14_9]\t      s=14 ->\n\t" +
                str(succ_mat[14][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[14][9]) + ") : (s'=26);\n\t" +
                "[pass_14_10]\t      s=14 ->\n\t" +
                str(succ_mat[14][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[14][10]) + ") : (s'=26);\n\t" +
                "[pass_14_11]\t      s=14 ->\n\t" +
                str(succ_mat[14][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[14][11]) + ") : (s'=26);\n\t" +
                "[pass_14_12]\t      s=14 ->\n\t" +
                str(succ_mat[14][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[14][12]) + ") : (s'=26);\n\t" +
                "[pass_14_13]\t      s=14 ->\n\t" +
                str(succ_mat[14][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[14][13]) + ") : (s'=26);\n\t" +
                "[pass_14_14]\t      s=14 ->\n\t" +
                str(succ_mat[14][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[14][14]) + ") : (s'=26);\n\t" +
                "[pass_14_15]\t      s=14 ->\n\t" +
                str(succ_mat[14][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[14][15]) + ") : (s'=26);\n\t" +
                "[pass_14_16]\t      s=14 ->\n\t" +
                str(succ_mat[14][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[14][16]) + ") : (s'=26);\n\t" +
                "[pass_14_17]\t      s=14 ->\n\t" +
                str(succ_mat[14][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[14][17]) + ") : (s'=26);\n\t" +
                "[pass_14_18]\t      s=14 ->\n\t" +
                str(succ_mat[14][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[14][18]) + ") : (s'=26);\n\t" +
                "[pass_14_19]\t      s=14 ->\n\t" +
                str(succ_mat[14][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[14][19]) + ") : (s'=26);\n\t" +
                "[pass_14_20]\t      s=14 ->\n\t" +
                str(succ_mat[14][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[14][20]) + ") : (s'=26);\n\t" +
                "[pass_14_21]\t      s=14 ->\n\t" +
                str(succ_mat[14][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[14][21]) + ") : (s'=26);\n\t" +
                "[pass_14_22]\t      s=14 ->\n\t" +
                str(succ_mat[14][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[14][22]) + ") : (s'=26);\n\t" +
                "[pass_14_23]\t      s=14 ->\n\t" +
                str(succ_mat[14][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[14][23]) + ") : (s'=26);\n\t" +
                "[pass_14_24]\t      s=14 ->\n\t" +
                str(succ_mat[14][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[14][24]) + ") : (s'=26);\n\t" +
                "[pass_14_25]\t      s=14 ->\n\t" +
                str(succ_mat[14][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[14][25]) + ") : (s'=26);\n\t" +
                "[shoot_14]\t       s=14 ->\n\t" +
                str(succ_mat[14][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[14][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 15 (s=15)\n\t" +
                "[pass_15_0]\t      s=15 ->\n\t" +
                str(succ_mat[15][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[15][0]) + ") : (s'=26);\n\t" +
                "[pass_15_1]\t      s=15 ->\n\t" +
                str(succ_mat[15][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[15][1]) + ") : (s'=26);\n\t" +
                "[pass_15_2]\t      s=15 ->\n\t" +
                str(succ_mat[15][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[15][2]) + ") : (s'=26);\n\t" +
                "[pass_15_3]\t      s=15 ->\n\t" +
                str(succ_mat[15][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[15][3]) + ") : (s'=26);\n\t" +
                "[pass_15_4]\t      s=15 ->\n\t" +
                str(succ_mat[15][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[15][4]) + ") : (s'=26);\n\t" +
                "[pass_15_5]\t      s=15 ->\n\t" +
                str(succ_mat[15][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[15][5]) + ") : (s'=26);\n\t" +
                "[pass_15_6]\t      s=15 ->\n\t" +
                str(succ_mat[15][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[15][6]) + ") : (s'=26);\n\t" +
                "[pass_15_7]\t      s=15 ->\n\t" +
                str(succ_mat[15][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[15][7]) + ") : (s'=26);\n\t" +
                "[pass_15_8]\t      s=15 ->\n\t" +
                str(succ_mat[15][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[15][8]) + ") : (s'=26);\n\t" +
                "[pass_15_9]\t      s=15 ->\n\t" +
                str(succ_mat[15][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[15][9]) + ") : (s'=26);\n\t" +
                "[pass_15_10]\t      s=15 ->\n\t" +
                str(succ_mat[15][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[15][10]) + ") : (s'=26);\n\t" +
                "[pass_15_11]\t      s=15 ->\n\t" +
                str(succ_mat[15][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[15][11]) + ") : (s'=26);\n\t" +
                "[pass_15_12]\t      s=15 ->\n\t" +
                str(succ_mat[15][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[15][12]) + ") : (s'=26);\n\t" +
                "[pass_15_13]\t      s=15 ->\n\t" +
                str(succ_mat[15][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[15][13]) + ") : (s'=26);\n\t" +
                "[pass_15_14]\t      s=15 ->\n\t" +
                str(succ_mat[15][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[15][14]) + ") : (s'=26);\n\t" +
                "[pass_15_15]\t      s=15 ->\n\t" +
                str(succ_mat[15][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[15][15]) + ") : (s'=26);\n\t" +
                "[pass_15_16]\t      s=15 ->\n\t" +
                str(succ_mat[15][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[15][16]) + ") : (s'=26);\n\t" +
                "[pass_15_17]\t      s=15 ->\n\t" +
                str(succ_mat[15][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[15][17]) + ") : (s'=26);\n\t" +
                "[pass_15_18]\t      s=15 ->\n\t" +
                str(succ_mat[15][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[15][18]) + ") : (s'=26);\n\t" +
                "[pass_15_19]\t      s=15 ->\n\t" +
                str(succ_mat[15][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[15][19]) + ") : (s'=26);\n\t" +
                "[pass_15_20]\t      s=15 ->\n\t" +
                str(succ_mat[15][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[15][20]) + ") : (s'=26);\n\t" +
                "[pass_15_21]\t      s=15 ->\n\t" +
                str(succ_mat[15][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[15][21]) + ") : (s'=26);\n\t" +
                "[pass_15_22]\t      s=15 ->\n\t" +
                str(succ_mat[15][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[15][22]) + ") : (s'=26);\n\t" +
                "[pass_15_23]\t      s=15 ->\n\t" +
                str(succ_mat[15][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[15][23]) + ") : (s'=26);\n\t" +
                "[pass_15_24]\t      s=15 ->\n\t" +
                str(succ_mat[15][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[15][24]) + ") : (s'=26);\n\t" +
                "[pass_15_25]\t      s=15 ->\n\t" +
                str(succ_mat[15][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[15][25]) + ") : (s'=26);\n\t" +
                "[shoot_15]\t       s=15 ->\n\t" +
                str(succ_mat[15][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[15][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 16 (s=16)\n\t" +
                "[pass_16_0]\t      s=16 ->\n\t" +
                str(succ_mat[16][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[16][0]) + ") : (s'=26);\n\t" +
                "[pass_16_1]\t      s=16 ->\n\t" +
                str(succ_mat[16][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[16][1]) + ") : (s'=26);\n\t" +
                "[pass_16_2]\t      s=16 ->\n\t" +
                str(succ_mat[16][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[16][2]) + ") : (s'=26);\n\t" +
                "[pass_16_3]\t      s=16 ->\n\t" +
                str(succ_mat[16][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[16][3]) + ") : (s'=26);\n\t" +
                "[pass_16_4]\t      s=16 ->\n\t" +
                str(succ_mat[16][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[16][4]) + ") : (s'=26);\n\t" +
                "[pass_16_5]\t      s=16 ->\n\t" +
                str(succ_mat[16][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[16][5]) + ") : (s'=26);\n\t" +
                "[pass_16_6]\t      s=16 ->\n\t" +
                str(succ_mat[16][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[16][6]) + ") : (s'=26);\n\t" +
                "[pass_16_7]\t      s=16 ->\n\t" +
                str(succ_mat[16][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[16][7]) + ") : (s'=26);\n\t" +
                "[pass_16_8]\t      s=16 ->\n\t" +
                str(succ_mat[16][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[16][8]) + ") : (s'=26);\n\t" +
                "[pass_16_9]\t      s=16 ->\n\t" +
                str(succ_mat[16][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[16][9]) + ") : (s'=26);\n\t" +
                "[pass_16_10]\t      s=16 ->\n\t" +
                str(succ_mat[16][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[16][10]) + ") : (s'=26);\n\t" +
                "[pass_16_11]\t      s=16 ->\n\t" +
                str(succ_mat[16][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[16][11]) + ") : (s'=26);\n\t" +
                "[pass_16_12]\t      s=16 ->\n\t" +
                str(succ_mat[16][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[16][12]) + ") : (s'=26);\n\t" +
                "[pass_16_13]\t      s=16 ->\n\t" +
                str(succ_mat[16][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[16][13]) + ") : (s'=26);\n\t" +
                "[pass_16_14]\t      s=16 ->\n\t" +
                str(succ_mat[16][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[16][14]) + ") : (s'=26);\n\t" +
                "[pass_16_15]\t      s=16 ->\n\t" +
                str(succ_mat[16][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[16][15]) + ") : (s'=26);\n\t" +
                "[pass_16_16]\t      s=16 ->\n\t" +
                str(succ_mat[16][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[16][16]) + ") : (s'=26);\n\t" +
                "[pass_16_17]\t      s=16 ->\n\t" +
                str(succ_mat[16][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[16][17]) + ") : (s'=26);\n\t" +
                "[pass_16_18]\t      s=16 ->\n\t" +
                str(succ_mat[16][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[16][18]) + ") : (s'=26);\n\t" +
                "[pass_16_19]\t      s=16 ->\n\t" +
                str(succ_mat[16][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[16][19]) + ") : (s'=26);\n\t" +
                "[pass_16_20]\t      s=16 ->\n\t" +
                str(succ_mat[16][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[16][20]) + ") : (s'=26);\n\t" +
                "[pass_16_21]\t      s=16 ->\n\t" +
                str(succ_mat[16][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[16][21]) + ") : (s'=26);\n\t" +
                "[pass_16_22]\t      s=16 ->\n\t" +
                str(succ_mat[16][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[16][22]) + ") : (s'=26);\n\t" +
                "[pass_16_23]\t      s=16 ->\n\t" +
                str(succ_mat[16][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[16][23]) + ") : (s'=26);\n\t" +
                "[pass_16_24]\t      s=16 ->\n\t" +
                str(succ_mat[16][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[16][24]) + ") : (s'=26);\n\t" +
                "[pass_16_25]\t      s=16 ->\n\t" +
                str(succ_mat[16][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[16][25]) + ") : (s'=26);\n\t" +
                "[shoot_16]\t       s=16 ->\n\t" +
                str(succ_mat[16][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[16][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 17 (s=17)\n\t" +
                "[pass_17_0]\t      s=17 ->\n\t" +
                str(succ_mat[17][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[17][0]) + ") : (s'=26);\n\t" +
                "[pass_17_1]\t      s=17 ->\n\t" +
                str(succ_mat[17][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[17][1]) + ") : (s'=26);\n\t" +
                "[pass_17_2]\t      s=17 ->\n\t" +
                str(succ_mat[17][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[17][2]) + ") : (s'=26);\n\t" +
                "[pass_17_3]\t      s=17 ->\n\t" +
                str(succ_mat[17][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[17][3]) + ") : (s'=26);\n\t" +
                "[pass_17_4]\t      s=17 ->\n\t" +
                str(succ_mat[17][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[17][4]) + ") : (s'=26);\n\t" +
                "[pass_17_5]\t      s=17 ->\n\t" +
                str(succ_mat[17][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[17][5]) + ") : (s'=26);\n\t" +
                "[pass_17_6]\t      s=17 ->\n\t" +
                str(succ_mat[17][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[17][6]) + ") : (s'=26);\n\t" +
                "[pass_17_7]\t      s=17 ->\n\t" +
                str(succ_mat[17][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[17][7]) + ") : (s'=26);\n\t" +
                "[pass_17_8]\t      s=17 ->\n\t" +
                str(succ_mat[17][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[17][8]) + ") : (s'=26);\n\t" +
                "[pass_17_9]\t      s=17 ->\n\t" +
                str(succ_mat[17][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[17][9]) + ") : (s'=26);\n\t" +
                "[pass_17_10]\t      s=17 ->\n\t" +
                str(succ_mat[17][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[17][10]) + ") : (s'=26);\n\t" +
                "[pass_17_11]\t      s=17 ->\n\t" +
                str(succ_mat[17][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[17][11]) + ") : (s'=26);\n\t" +
                "[pass_17_12]\t      s=17 ->\n\t" +
                str(succ_mat[17][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[17][12]) + ") : (s'=26);\n\t" +
                "[pass_17_13]\t      s=17 ->\n\t" +
                str(succ_mat[17][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[17][13]) + ") : (s'=26);\n\t" +
                "[pass_17_14]\t      s=17 ->\n\t" +
                str(succ_mat[17][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[17][14]) + ") : (s'=26);\n\t" +
                "[pass_17_15]\t      s=17 ->\n\t" +
                str(succ_mat[17][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[17][15]) + ") : (s'=26);\n\t" +
                "[pass_17_16]\t      s=17 ->\n\t" +
                str(succ_mat[17][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[17][16]) + ") : (s'=26);\n\t" +
                "[pass_17_17]\t      s=17 ->\n\t" +
                str(succ_mat[17][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[17][17]) + ") : (s'=26);\n\t" +
                "[pass_17_18]\t      s=17 ->\n\t" +
                str(succ_mat[17][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[17][18]) + ") : (s'=26);\n\t" +
                "[pass_17_19]\t      s=17 ->\n\t" +
                str(succ_mat[17][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[17][19]) + ") : (s'=26);\n\t" +
                "[pass_17_20]\t      s=17 ->\n\t" +
                str(succ_mat[17][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[17][20]) + ") : (s'=26);\n\t" +
                "[pass_17_21]\t      s=17 ->\n\t" +
                str(succ_mat[17][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[17][21]) + ") : (s'=26);\n\t" +
                "[pass_17_22]\t      s=17 ->\n\t" +
                str(succ_mat[17][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[17][22]) + ") : (s'=26);\n\t" +
                "[pass_17_23]\t      s=17 ->\n\t" +
                str(succ_mat[17][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[17][23]) + ") : (s'=26);\n\t" +
                "[pass_17_24]\t      s=17 ->\n\t" +
                str(succ_mat[17][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[17][24]) + ") : (s'=26);\n\t" +
                "[pass_17_25]\t      s=17 ->\n\t" +
                str(succ_mat[17][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[17][25]) + ") : (s'=26);\n\t" +
                "[shoot_17]\t       s=17 ->\n\t" +
                str(succ_mat[17][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[17][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 18 (s=18)\n\t" +
                "[pass_18_0]\t      s=18 ->\n\t" +
                str(succ_mat[18][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[18][0]) + ") : (s'=26);\n\t" +
                "[pass_18_1]\t      s=18 ->\n\t" +
                str(succ_mat[18][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[18][1]) + ") : (s'=26);\n\t" +
                "[pass_18_2]\t      s=18 ->\n\t" +
                str(succ_mat[18][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[18][2]) + ") : (s'=26);\n\t" +
                "[pass_18_3]\t      s=18 ->\n\t" +
                str(succ_mat[18][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[18][3]) + ") : (s'=26);\n\t" +
                "[pass_18_4]\t      s=18 ->\n\t" +
                str(succ_mat[18][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[18][4]) + ") : (s'=26);\n\t" +
                "[pass_18_5]\t      s=18 ->\n\t" +
                str(succ_mat[18][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[18][5]) + ") : (s'=26);\n\t" +
                "[pass_18_6]\t      s=18 ->\n\t" +
                str(succ_mat[18][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[18][6]) + ") : (s'=26);\n\t" +
                "[pass_18_7]\t      s=18 ->\n\t" +
                str(succ_mat[18][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[18][7]) + ") : (s'=26);\n\t" +
                "[pass_18_8]\t      s=18 ->\n\t" +
                str(succ_mat[18][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[18][8]) + ") : (s'=26);\n\t" +
                "[pass_18_9]\t      s=18 ->\n\t" +
                str(succ_mat[18][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[18][9]) + ") : (s'=26);\n\t" +
                "[pass_18_10]\t      s=18 ->\n\t" +
                str(succ_mat[18][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[18][10]) + ") : (s'=26);\n\t" +
                "[pass_18_11]\t      s=18 ->\n\t" +
                str(succ_mat[18][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[18][11]) + ") : (s'=26);\n\t" +
                "[pass_18_12]\t      s=18 ->\n\t" +
                str(succ_mat[18][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[18][12]) + ") : (s'=26);\n\t" +
                "[pass_18_13]\t      s=18 ->\n\t" +
                str(succ_mat[18][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[18][13]) + ") : (s'=26);\n\t" +
                "[pass_18_14]\t      s=18 ->\n\t" +
                str(succ_mat[18][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[18][14]) + ") : (s'=26);\n\t" +
                "[pass_18_15]\t      s=18 ->\n\t" +
                str(succ_mat[18][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[18][15]) + ") : (s'=26);\n\t" +
                "[pass_18_16]\t      s=18 ->\n\t" +
                str(succ_mat[18][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[18][16]) + ") : (s'=26);\n\t" +
                "[pass_18_17]\t      s=18 ->\n\t" +
                str(succ_mat[18][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[18][17]) + ") : (s'=26);\n\t" +
                "[pass_18_18]\t      s=18 ->\n\t" +
                str(succ_mat[18][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[18][18]) + ") : (s'=26);\n\t" +
                "[pass_18_19]\t      s=18 ->\n\t" +
                str(succ_mat[18][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[18][19]) + ") : (s'=26);\n\t" +
                "[pass_18_20]\t      s=18 ->\n\t" +
                str(succ_mat[18][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[18][20]) + ") : (s'=26);\n\t" +
                "[pass_18_21]\t      s=18 ->\n\t" +
                str(succ_mat[18][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[18][21]) + ") : (s'=26);\n\t" +
                "[pass_18_22]\t      s=18 ->\n\t" +
                str(succ_mat[18][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[18][22]) + ") : (s'=26);\n\t" +
                "[pass_18_23]\t      s=18 ->\n\t" +
                str(succ_mat[18][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[18][23]) + ") : (s'=26);\n\t" +
                "[pass_18_24]\t      s=18 ->\n\t" +
                str(succ_mat[18][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[18][24]) + ") : (s'=26);\n\t" +
                "[pass_18_25]\t      s=18 ->\n\t" +
                str(succ_mat[18][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[18][25]) + ") : (s'=26);\n\t" +
                "[shoot_18]\t       s=18 ->\n\t" +
                str(succ_mat[18][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[18][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 19 (s=19)\n\t" +
                "[pass_19_0]\t      s=19 ->\n\t" +
                str(succ_mat[19][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[19][0]) + ") : (s'=26);\n\t" +
                "[pass_19_1]\t      s=19 ->\n\t" +
                str(succ_mat[19][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[19][1]) + ") : (s'=26);\n\t" +
                "[pass_19_2]\t      s=19 ->\n\t" +
                str(succ_mat[19][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[19][2]) + ") : (s'=26);\n\t" +
                "[pass_19_3]\t      s=19 ->\n\t" +
                str(succ_mat[19][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[19][3]) + ") : (s'=26);\n\t" +
                "[pass_19_4]\t      s=19 ->\n\t" +
                str(succ_mat[19][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[19][4]) + ") : (s'=26);\n\t" +
                "[pass_19_5]\t      s=19 ->\n\t" +
                str(succ_mat[19][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[19][5]) + ") : (s'=26);\n\t" +
                "[pass_19_6]\t      s=19 ->\n\t" +
                str(succ_mat[19][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[19][6]) + ") : (s'=26);\n\t" +
                "[pass_19_7]\t      s=19 ->\n\t" +
                str(succ_mat[19][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[19][7]) + ") : (s'=26);\n\t" +
                "[pass_19_8]\t      s=19 ->\n\t" +
                str(succ_mat[19][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[19][8]) + ") : (s'=26);\n\t" +
                "[pass_19_9]\t      s=19 ->\n\t" +
                str(succ_mat[19][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[19][9]) + ") : (s'=26);\n\t" +
                "[pass_19_10]\t      s=19 ->\n\t" +
                str(succ_mat[19][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[19][10]) + ") : (s'=26);\n\t" +
                "[pass_19_11]\t      s=19 ->\n\t" +
                str(succ_mat[19][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[19][11]) + ") : (s'=26);\n\t" +
                "[pass_19_12]\t      s=19 ->\n\t" +
                str(succ_mat[19][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[19][12]) + ") : (s'=26);\n\t" +
                "[pass_19_13]\t      s=19 ->\n\t" +
                str(succ_mat[19][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[19][13]) + ") : (s'=26);\n\t" +
                "[pass_19_14]\t      s=19 ->\n\t" +
                str(succ_mat[19][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[19][14]) + ") : (s'=26);\n\t" +
                "[pass_19_15]\t      s=19 ->\n\t" +
                str(succ_mat[19][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[19][15]) + ") : (s'=26);\n\t" +
                "[pass_19_16]\t      s=19 ->\n\t" +
                str(succ_mat[19][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[19][16]) + ") : (s'=26);\n\t" +
                "[pass_19_17]\t      s=19 ->\n\t" +
                str(succ_mat[19][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[19][17]) + ") : (s'=26);\n\t" +
                "[pass_19_18]\t      s=19 ->\n\t" +
                str(succ_mat[19][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[19][18]) + ") : (s'=26);\n\t" +
                "[pass_19_19]\t      s=19 ->\n\t" +
                str(succ_mat[19][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[19][19]) + ") : (s'=26);\n\t" +
                "[pass_19_20]\t      s=19 ->\n\t" +
                str(succ_mat[19][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[19][20]) + ") : (s'=26);\n\t" +
                "[pass_19_21]\t      s=19 ->\n\t" +
                str(succ_mat[19][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[19][21]) + ") : (s'=26);\n\t" +
                "[pass_19_22]\t      s=19 ->\n\t" +
                str(succ_mat[19][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[19][22]) + ") : (s'=26);\n\t" +
                "[pass_19_23]\t      s=19 ->\n\t" +
                str(succ_mat[19][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[19][23]) + ") : (s'=26);\n\t" +
                "[pass_19_24]\t      s=19 ->\n\t" +
                str(succ_mat[19][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[19][24]) + ") : (s'=26);\n\t" +
                "[pass_19_25]\t      s=19 ->\n\t" +
                str(succ_mat[19][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[19][25]) + ") : (s'=26);\n\t" +
                "[shoot_19]\t       s=19 ->\n\t" +
                str(succ_mat[19][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[19][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 20 (s=20)\n\t" +
                "[pass_20_0]\t      s=20 ->\n\t" +
                str(succ_mat[20][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[20][0]) + ") : (s'=26);\n\t" +
                "[pass_20_1]\t      s=20 ->\n\t" +
                str(succ_mat[20][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[20][1]) + ") : (s'=26);\n\t" +
                "[pass_20_2]\t      s=20 ->\n\t" +
                str(succ_mat[20][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[20][2]) + ") : (s'=26);\n\t" +
                "[pass_20_3]\t      s=20 ->\n\t" +
                str(succ_mat[20][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[20][3]) + ") : (s'=26);\n\t" +
                "[pass_20_4]\t      s=20 ->\n\t" +
                str(succ_mat[20][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[20][4]) + ") : (s'=26);\n\t" +
                "[pass_20_5]\t      s=20 ->\n\t" +
                str(succ_mat[20][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[20][5]) + ") : (s'=26);\n\t" +
                "[pass_20_6]\t      s=20 ->\n\t" +
                str(succ_mat[20][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[20][6]) + ") : (s'=26);\n\t" +
                "[pass_20_7]\t      s=20 ->\n\t" +
                str(succ_mat[20][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[20][7]) + ") : (s'=26);\n\t" +
                "[pass_20_8]\t      s=20 ->\n\t" +
                str(succ_mat[20][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[20][8]) + ") : (s'=26);\n\t" +
                "[pass_20_9]\t      s=20 ->\n\t" +
                str(succ_mat[20][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[20][9]) + ") : (s'=26);\n\t" +
                "[pass_20_10]\t      s=20 ->\n\t" +
                str(succ_mat[20][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[20][10]) + ") : (s'=26);\n\t" +
                "[pass_20_11]\t      s=20 ->\n\t" +
                str(succ_mat[20][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[20][11]) + ") : (s'=26);\n\t" +
                "[pass_20_12]\t      s=20 ->\n\t" +
                str(succ_mat[20][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[20][12]) + ") : (s'=26);\n\t" +
                "[pass_20_13]\t      s=20 ->\n\t" +
                str(succ_mat[20][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[20][13]) + ") : (s'=26);\n\t" +
                "[pass_20_14]\t      s=20 ->\n\t" +
                str(succ_mat[20][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[20][14]) + ") : (s'=26);\n\t" +
                "[pass_20_15]\t      s=20 ->\n\t" +
                str(succ_mat[20][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[20][15]) + ") : (s'=26);\n\t" +
                "[pass_20_16]\t      s=20 ->\n\t" +
                str(succ_mat[20][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[20][16]) + ") : (s'=26);\n\t" +
                "[pass_20_17]\t      s=20 ->\n\t" +
                str(succ_mat[20][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[20][17]) + ") : (s'=26);\n\t" +
                "[pass_20_18]\t      s=20 ->\n\t" +
                str(succ_mat[20][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[20][18]) + ") : (s'=26);\n\t" +
                "[pass_20_19]\t      s=20 ->\n\t" +
                str(succ_mat[20][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[20][19]) + ") : (s'=26);\n\t" +
                "[pass_20_20]\t      s=20 ->\n\t" +
                str(succ_mat[20][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[20][20]) + ") : (s'=26);\n\t" +
                "[pass_20_21]\t      s=20 ->\n\t" +
                str(succ_mat[20][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[20][21]) + ") : (s'=26);\n\t" +
                "[pass_20_22]\t      s=20 ->\n\t" +
                str(succ_mat[20][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[20][22]) + ") : (s'=26);\n\t" +
                "[pass_20_23]\t      s=20 ->\n\t" +
                str(succ_mat[20][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[20][23]) + ") : (s'=26);\n\t" +
                "[pass_20_24]\t      s=20 ->\n\t" +
                str(succ_mat[20][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[20][24]) + ") : (s'=26);\n\t" +
                "[pass_20_25]\t      s=20 ->\n\t" +
                str(succ_mat[20][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[20][25]) + ") : (s'=26);\n\t" +
                "[shoot_20]\t       s=20 ->\n\t" +
                str(succ_mat[20][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[20][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 21 (s=21)\n\t" +
                "[pass_21_0]\t      s=21 ->\n\t" +
                str(succ_mat[21][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[21][0]) + ") : (s'=26);\n\t" +
                "[pass_21_1]\t      s=21 ->\n\t" +
                str(succ_mat[21][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[21][1]) + ") : (s'=26);\n\t" +
                "[pass_21_2]\t      s=21 ->\n\t" +
                str(succ_mat[21][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[21][2]) + ") : (s'=26);\n\t" +
                "[pass_21_3]\t      s=21 ->\n\t" +
                str(succ_mat[21][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[21][3]) + ") : (s'=26);\n\t" +
                "[pass_21_4]\t      s=21 ->\n\t" +
                str(succ_mat[21][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[21][4]) + ") : (s'=26);\n\t" +
                "[pass_21_5]\t      s=21 ->\n\t" +
                str(succ_mat[21][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[21][5]) + ") : (s'=26);\n\t" +
                "[pass_21_6]\t      s=21 ->\n\t" +
                str(succ_mat[21][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[21][6]) + ") : (s'=26);\n\t" +
                "[pass_21_7]\t      s=21 ->\n\t" +
                str(succ_mat[21][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[21][7]) + ") : (s'=26);\n\t" +
                "[pass_21_8]\t      s=21 ->\n\t" +
                str(succ_mat[21][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[21][8]) + ") : (s'=26);\n\t" +
                "[pass_21_9]\t      s=21 ->\n\t" +
                str(succ_mat[21][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[21][9]) + ") : (s'=26);\n\t" +
                "[pass_21_10]\t      s=21 ->\n\t" +
                str(succ_mat[21][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[21][10]) + ") : (s'=26);\n\t" +
                "[pass_21_11]\t      s=21 ->\n\t" +
                str(succ_mat[21][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[21][11]) + ") : (s'=26);\n\t" +
                "[pass_21_12]\t      s=21 ->\n\t" +
                str(succ_mat[21][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[21][12]) + ") : (s'=26);\n\t" +
                "[pass_21_13]\t      s=21 ->\n\t" +
                str(succ_mat[21][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[21][13]) + ") : (s'=26);\n\t" +
                "[pass_21_14]\t      s=21 ->\n\t" +
                str(succ_mat[21][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[21][14]) + ") : (s'=26);\n\t" +
                "[pass_21_15]\t      s=21 ->\n\t" +
                str(succ_mat[21][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[21][15]) + ") : (s'=26);\n\t" +
                "[pass_21_16]\t      s=21 ->\n\t" +
                str(succ_mat[21][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[21][16]) + ") : (s'=26);\n\t" +
                "[pass_21_17]\t      s=21 ->\n\t" +
                str(succ_mat[21][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[21][17]) + ") : (s'=26);\n\t" +
                "[pass_21_18]\t      s=21 ->\n\t" +
                str(succ_mat[21][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[21][18]) + ") : (s'=26);\n\t" +
                "[pass_21_19]\t      s=21 ->\n\t" +
                str(succ_mat[21][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[21][19]) + ") : (s'=26);\n\t" +
                "[pass_21_20]\t      s=21 ->\n\t" +
                str(succ_mat[21][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[21][20]) + ") : (s'=26);\n\t" +
                "[pass_21_21]\t      s=21 ->\n\t" +
                str(succ_mat[21][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[21][21]) + ") : (s'=26);\n\t" +
                "[pass_21_22]\t      s=21 ->\n\t" +
                str(succ_mat[21][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[21][22]) + ") : (s'=26);\n\t" +
                "[pass_21_23]\t      s=21 ->\n\t" +
                str(succ_mat[21][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[21][23]) + ") : (s'=26);\n\t" +
                "[pass_21_24]\t      s=21 ->\n\t" +
                str(succ_mat[21][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[21][24]) + ") : (s'=26);\n\t" +
                "[pass_21_25]\t      s=21 ->\n\t" +
                str(succ_mat[21][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[21][25]) + ") : (s'=26);\n\t" +
                "[shoot_21]\t       s=21 ->\n\t" +
                str(succ_mat[21][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[21][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 22 (s=22)\n\t" +
                "[pass_22_0]\t      s=22 ->\n\t" +
                str(succ_mat[22][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[22][0]) + ") : (s'=26);\n\t" +
                "[pass_22_1]\t      s=22 ->\n\t" +
                str(succ_mat[22][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[22][1]) + ") : (s'=26);\n\t" +
                "[pass_22_2]\t      s=22 ->\n\t" +
                str(succ_mat[22][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[22][2]) + ") : (s'=26);\n\t" +
                "[pass_22_3]\t      s=22 ->\n\t" +
                str(succ_mat[22][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[22][3]) + ") : (s'=26);\n\t" +
                "[pass_22_4]\t      s=22 ->\n\t" +
                str(succ_mat[22][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[22][4]) + ") : (s'=26);\n\t" +
                "[pass_22_5]\t      s=22 ->\n\t" +
                str(succ_mat[22][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[22][5]) + ") : (s'=26);\n\t" +
                "[pass_22_6]\t      s=22 ->\n\t" +
                str(succ_mat[22][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[22][6]) + ") : (s'=26);\n\t" +
                "[pass_22_7]\t      s=22 ->\n\t" +
                str(succ_mat[22][7]) + " : (s'=7) + (1 - " +                 
                str(succ_mat[22][7]) + ") : (s'=26);\n\t" +
                "[pass_22_8]\t      s=22 ->\n\t" +
                str(succ_mat[22][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[22][8]) + ") : (s'=26);\n\t" +
                "[pass_22_9]\t      s=22 ->\n\t" +
                str(succ_mat[22][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[22][9]) + ") : (s'=26);\n\t" +
                "[pass_22_10]\t      s=22 ->\n\t" +
                str(succ_mat[22][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[22][10]) + ") : (s'=26);\n\t" +
                "[pass_22_11]\t      s=22 ->\n\t" +
                str(succ_mat[22][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[22][11]) + ") : (s'=26);\n\t" +
                "[pass_22_12]\t      s=22 ->\n\t" +
                str(succ_mat[22][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[22][12]) + ") : (s'=26);\n\t" +
                "[pass_22_13]\t      s=22 ->\n\t" +
                str(succ_mat[22][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[22][13]) + ") : (s'=26);\n\t" +
                "[pass_22_14]\t      s=22 ->\n\t" +
                str(succ_mat[22][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[22][14]) + ") : (s'=26);\n\t" +
                "[pass_22_15]\t      s=22 ->\n\t" +
                str(succ_mat[22][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[22][15]) + ") : (s'=26);\n\t" +
                "[pass_22_16]\t      s=22 ->\n\t" +
                str(succ_mat[22][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[22][16]) + ") : (s'=26);\n\t" +
                "[pass_22_17]\t      s=22 ->\n\t" +
                str(succ_mat[22][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[22][17]) + ") : (s'=26);\n\t" +
                "[pass_22_18]\t      s=22 ->\n\t" +
                str(succ_mat[22][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[22][18]) + ") : (s'=26);\n\t" +
                "[pass_22_19]\t      s=22 ->\n\t" +
                str(succ_mat[22][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[22][19]) + ") : (s'=26);\n\t" +
                "[pass_22_20]\t      s=22 ->\n\t" +
                str(succ_mat[22][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[22][20]) + ") : (s'=26);\n\t" +
                "[pass_22_21]\t      s=22 ->\n\t" +
                str(succ_mat[22][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[22][21]) + ") : (s'=26);\n\t" +
                "[pass_22_22]\t      s=22 ->\n\t" +
                str(succ_mat[22][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[22][22]) + ") : (s'=26);\n\t" +
                "[pass_22_23]\t      s=22 ->\n\t" +
                str(succ_mat[22][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[22][23]) + ") : (s'=26);\n\t" +
                "[pass_22_24]\t      s=22 ->\n\t" +
                str(succ_mat[22][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[22][24]) + ") : (s'=26);\n\t" +
                "[pass_22_25]\t      s=22 ->\n\t" +
                str(succ_mat[22][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[22][25]) + ") : (s'=26);\n\t" +
                "[shoot_22]\t       s=22 ->\n\t" +
                str(succ_mat[22][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[22][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 23 (s=23)\n\t" +
                "[pass_23_0]\t      s=23 ->\n\t" +
                str(succ_mat[23][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[23][0]) + ") : (s'=26);\n\t" +
                "[pass_23_1]\t      s=23 ->\n\t" +
                str(succ_mat[23][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[23][1]) + ") : (s'=26);\n\t" +
                "[pass_23_2]\t      s=23 ->\n\t" +
                str(succ_mat[23][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[23][2]) + ") : (s'=26);\n\t" +
                "[pass_23_3]\t      s=23 ->\n\t" +
                str(succ_mat[23][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[23][3]) + ") : (s'=26);\n\t" +
                "[pass_23_4]\t      s=23 ->\n\t" +
                str(succ_mat[23][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[23][4]) + ") : (s'=26);\n\t" +
                "[pass_23_5]\t      s=23 ->\n\t" +
                str(succ_mat[23][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[23][5]) + ") : (s'=26);\n\t" +
                "[pass_23_6]\t      s=23 ->\n\t" +
                str(succ_mat[23][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[23][6]) + ") : (s'=26);\n\t" +
                "[pass_23_7]\t      s=23 ->\n\t" +
                str(succ_mat[23][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[23][7]) + ") : (s'=26);\n\t" +
                "[pass_23_8]\t      s=23 ->\n\t" +
                str(succ_mat[23][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[23][8]) + ") : (s'=26);\n\t" +
                "[pass_23_9]\t      s=23 ->\n\t" +
                str(succ_mat[23][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[23][9]) + ") : (s'=26);\n\t" +
                "[pass_23_10]\t      s=23 ->\n\t" +
                str(succ_mat[23][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[23][10]) + ") : (s'=26);\n\t" +
                "[pass_23_11]\t      s=23 ->\n\t" +                
                str(succ_mat[23][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[23][11]) + ") : (s'=26);\n\t" +
                "[pass_23_12]\t      s=23 ->\n\t" +
                str(succ_mat[23][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[23][12]) + ") : (s'=26);\n\t" +
                "[pass_23_13]\t      s=23 ->\n\t" +
                str(succ_mat[23][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[23][13]) + ") : (s'=26);\n\t" +
                "[pass_23_14]\t      s=23 ->\n\t" +
                str(succ_mat[23][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[23][14]) + ") : (s'=26);\n\t" +
                "[pass_23_15]\t      s=23 ->\n\t" +
                str(succ_mat[23][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[23][15]) + ") : (s'=26);\n\t" +
                "[pass_23_16]\t      s=23 ->\n\t" +
                str(succ_mat[23][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[23][16]) + ") : (s'=26);\n\t" +
                "[pass_23_17]\t      s=23 ->\n\t" +
                str(succ_mat[23][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[23][17]) + ") : (s'=26);\n\t" +
                "[pass_23_18]\t      s=23 ->\n\t" +
                str(succ_mat[23][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[23][18]) + ") : (s'=26);\n\t" +
                "[pass_23_19]\t      s=23 ->\n\t" +
                str(succ_mat[23][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[23][19]) + ") : (s'=26);\n\t" +
                "[pass_23_20]\t      s=23 ->\n\t" +
                str(succ_mat[23][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[23][20]) + ") : (s'=26);\n\t" +
                "[pass_23_21]\t      s=23 ->\n\t" +
                str(succ_mat[23][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[23][21]) + ") : (s'=26);\n\t" +
                "[pass_23_22]\t      s=23 ->\n\t" +
                str(succ_mat[23][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[23][22]) + ") : (s'=26);\n\t" +
                "[pass_23_23]\t      s=23 ->\n\t" +
                str(succ_mat[23][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[23][23]) + ") : (s'=26);\n\t" +
                "[pass_23_24]\t      s=23 ->\n\t" +
                str(succ_mat[23][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[23][24]) + ") : (s'=26);\n\t" +
                "[pass_23_25]\t      s=23 ->\n\t" +
                str(succ_mat[23][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[23][25]) + ") : (s'=26);\n\t" +
                "[shoot_23]\t       s=23 ->\n\t" +
                str(succ_mat[23][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[23][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 24 (s=24)\n\t" +
                "[pass_24_0]\t      s=24 ->\n\t" +
                str(succ_mat[24][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[24][0]) + ") : (s'=26);\n\t" +
                "[pass_24_1]\t      s=24 ->\n\t" +
                str(succ_mat[24][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[24][1]) + ") : (s'=26);\n\t" +
                "[pass_24_2]\t      s=24 ->\n\t" +
                str(succ_mat[24][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[24][2]) + ") : (s'=26);\n\t" +
                "[pass_24_3]\t      s=24 ->\n\t" +
                str(succ_mat[24][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[24][3]) + ") : (s'=26);\n\t" +
                "[pass_24_4]\t      s=24 ->\n\t" +
                str(succ_mat[24][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[24][4]) + ") : (s'=26);\n\t" +
                "[pass_24_5]\t      s=24 ->\n\t" +
                str(succ_mat[24][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[24][5]) + ") : (s'=26);\n\t" +
                "[pass_24_6]\t      s=24 ->\n\t" +
                str(succ_mat[24][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[24][6]) + ") : (s'=26);\n\t" +
                "[pass_24_7]\t      s=24 ->\n\t" +
                str(succ_mat[24][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[24][7]) + ") : (s'=26);\n\t" +
                "[pass_24_8]\t      s=24 ->\n\t" +
                str(succ_mat[24][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[24][8]) + ") : (s'=26);\n\t" +
                "[pass_24_9]\t      s=24 ->\n\t" +
                str(succ_mat[24][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[24][9]) + ") : (s'=26);\n\t" +
                "[pass_24_10]\t      s=24 ->\n\t" +
                str(succ_mat[24][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[24][10]) + ") : (s'=26);\n\t" +
                "[pass_24_11]\t      s=24 ->\n\t" +
                str(succ_mat[24][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[24][11]) + ") : (s'=26);\n\t" +
                "[pass_24_12]\t      s=24 ->\n\t" +
                str(succ_mat[24][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[24][12]) + ") : (s'=26);\n\t" +
                "[pass_24_13]\t      s=24 ->\n\t" +
                str(succ_mat[24][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[24][13]) + ") : (s'=26);\n\t" +
                "[pass_24_14]\t      s=24 ->\n\t" +
                str(succ_mat[24][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[24][14]) + ") : (s'=26);\n\t" +
                "[pass_24_15]\t      s=24 ->\n\t" +
                str(succ_mat[24][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[24][15]) + ") : (s'=26);\n\t" +
                "[pass_24_16]\t      s=24 ->\n\t" +
                str(succ_mat[24][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[24][16]) + ") : (s'=26);\n\t" +
                "[pass_24_17]\t      s=24 ->\n\t" +
                str(succ_mat[24][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[24][17]) + ") : (s'=26);\n\t" +
                "[pass_24_18]\t      s=24 ->\n\t" +
                str(succ_mat[24][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[24][18]) + ") : (s'=26);\n\t" +
                "[pass_24_19]\t      s=24 ->\n\t" +
                str(succ_mat[24][19]) + " : (s'=19) + (1 - " +                 
                str(succ_mat[24][19]) + ") : (s'=26);\n\t" +
                "[pass_24_20]\t      s=24 ->\n\t" +
                str(succ_mat[24][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[24][20]) + ") : (s'=26);\n\t" +
                "[pass_24_21]\t      s=24 ->\n\t" +
                str(succ_mat[24][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[24][21]) + ") : (s'=26);\n\t" +
                "[pass_24_22]\t      s=24 ->\n\t" +
                str(succ_mat[24][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[24][22]) + ") : (s'=26);\n\t" +
                "[pass_24_23]\t      s=24 ->\n\t" +
                str(succ_mat[24][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[24][23]) + ") : (s'=26);\n\t" +
                "[pass_24_24]\t      s=24 ->\n\t" +
                str(succ_mat[24][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[24][24]) + ") : (s'=26);\n\t" +
                "[pass_24_25]\t      s=24 ->\n\t" +
                str(succ_mat[24][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[24][25]) + ") : (s'=26);\n\t" +
                "[shoot_24]\t       s=24 ->\n\t" +
                str(succ_mat[24][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[24][26]) + ") : (s'=26);\n\n\t" +
                
                "// player actions from zone 25 (s=25)\n\t" +
                "[pass_25_0]\t      s=25 ->\n\t" +
                str(succ_mat[25][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[25][0]) + ") : (s'=26);\n\t" +
                "[pass_25_1]\t      s=25 ->\n\t" +
                str(succ_mat[25][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[25][1]) + ") : (s'=26);\n\t" +
                "[pass_25_2]\t      s=25 ->\n\t" +
                str(succ_mat[25][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[25][2]) + ") : (s'=26);\n\t" +
                "[pass_25_3]\t      s=25 ->\n\t" +
                str(succ_mat[25][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[25][3]) + ") : (s'=26);\n\t" +
                "[pass_25_4]\t      s=25 ->\n\t" +
                str(succ_mat[25][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[25][4]) + ") : (s'=26);\n\t" +
                "[pass_25_5]\t      s=25 ->\n\t" +
                str(succ_mat[25][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[25][5]) + ") : (s'=26);\n\t" +
                "[pass_25_6]\t      s=25 ->\n\t" +
                str(succ_mat[25][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[25][6]) + ") : (s'=26);\n\t" +
                "[pass_25_7]\t      s=25 ->\n\t" +
                str(succ_mat[25][7]) + " : (s'=7) + (1 - " + 
                str(succ_mat[25][7]) + ") : (s'=26);\n\t" +
                "[pass_25_8]\t      s=25 ->\n\t" +
                str(succ_mat[25][8]) + " : (s'=8) + (1 - " + 
                str(succ_mat[25][8]) + ") : (s'=26);\n\t" +
                "[pass_25_9]\t      s=25 ->\n\t" +
                str(succ_mat[25][9]) + " : (s'=9) + (1 - " + 
                str(succ_mat[25][9]) + ") : (s'=26);\n\t" +
                "[pass_25_10]\t      s=25 ->\n\t" +
                str(succ_mat[25][10]) + " : (s'=10) + (1 - " + 
                str(succ_mat[25][10]) + ") : (s'=26);\n\t" +
                "[pass_25_11]\t      s=25 ->\n\t" +
                str(succ_mat[25][11]) + " : (s'=11) + (1 - " + 
                str(succ_mat[25][11]) + ") : (s'=26);\n\t" +
                "[pass_25_12]\t      s=25 ->\n\t" +
                str(succ_mat[25][12]) + " : (s'=12) + (1 - " + 
                str(succ_mat[25][12]) + ") : (s'=26);\n\t" +
                "[pass_25_13]\t      s=25 ->\n\t" +
                str(succ_mat[25][13]) + " : (s'=13) + (1 - " + 
                str(succ_mat[25][13]) + ") : (s'=26);\n\t" +
                "[pass_25_14]\t      s=25 ->\n\t" +
                str(succ_mat[25][14]) + " : (s'=14) + (1 - " + 
                str(succ_mat[25][14]) + ") : (s'=26);\n\t" +
                "[pass_25_15]\t      s=25 ->\n\t" +
                str(succ_mat[25][15]) + " : (s'=15) + (1 - " + 
                str(succ_mat[25][15]) + ") : (s'=26);\n\t" +
                "[pass_25_16]\t      s=25 ->\n\t" +
                str(succ_mat[25][16]) + " : (s'=16) + (1 - " + 
                str(succ_mat[25][16]) + ") : (s'=26);\n\t" +
                "[pass_25_17]\t      s=25 ->\n\t" +
                str(succ_mat[25][17]) + " : (s'=17) + (1 - " + 
                str(succ_mat[25][17]) + ") : (s'=26);\n\t" +
                "[pass_25_18]\t      s=25 ->\n\t" +
                str(succ_mat[25][18]) + " : (s'=18) + (1 - " + 
                str(succ_mat[25][18]) + ") : (s'=26);\n\t" +
                "[pass_25_19]\t      s=25 ->\n\t" +
                str(succ_mat[25][19]) + " : (s'=19) + (1 - " + 
                str(succ_mat[25][19]) + ") : (s'=26);\n\t" +
                "[pass_25_20]\t      s=25 ->\n\t" +
                str(succ_mat[25][20]) + " : (s'=20) + (1 - " + 
                str(succ_mat[25][20]) + ") : (s'=26);\n\t" +
                "[pass_25_21]\t      s=25 ->\n\t" +
                str(succ_mat[25][21]) + " : (s'=21) + (1 - " + 
                str(succ_mat[25][21]) + ") : (s'=26);\n\t" +
                "[pass_25_22]\t      s=25 ->\n\t" +
                str(succ_mat[25][22]) + " : (s'=22) + (1 - " + 
                str(succ_mat[25][22]) + ") : (s'=26);\n\t" +
                "[pass_25_23]\t      s=25 ->\n\t" +
                str(succ_mat[25][23]) + " : (s'=23) + (1 - " + 
                str(succ_mat[25][23]) + ") : (s'=26);\n\t" +
                "[pass_25_24]\t      s=25 ->\n\t" +
                str(succ_mat[25][24]) + " : (s'=24) + (1 - " + 
                str(succ_mat[25][24]) + ") : (s'=26);\n\t" +
                "[pass_25_25]\t      s=25 ->\n\t" +
                str(succ_mat[25][25]) + " : (s'=25) + (1 - " + 
                str(succ_mat[25][25]) + ") : (s'=26);\n\t" +
                "[shoot_25]\t       s=25 ->\n\t" +
                str(succ_mat[25][26]) + " : (s'=27) + (1 - " + 
                str(succ_mat[25][26]) + ") : (s'=26);\n\n\t" +

                "// absorbing states\n\t" +
                "[] s=26 -> (s'=26);\n\t" +
                "[] s=27 -> (s'=27);\n\n" +

                "endmodule\n\n" +
                
                "label \"ball_in_zone_0\" = (s=0);\n" +
                "label \"ball_in_zone_1\" = (s=1);\n" +
                "label \"ball_in_zone_2\" = (s=2);\n" +
                "label \"ball_in_zone_3\" = (s=3);\n" +
                "label \"ball_in_zone_4\" = (s=4);\n" +
                "label \"ball_in_zone_5\" = (s=5);\n" +
                "label \"ball_in_zone_6\" = (s=6);\n" +
                "label \"ball_in_zone_7\" = (s=7);\n" +
                "label \"ball_in_zone_8\" = (s=8);\n" +
                "label \"ball_in_zone_9\" = (s=9);\n" +
                "label \"ball_in_zone_10\" = (s=10);\n" +
                "label \"ball_in_zone_11\" = (s=11);\n" +
                "label \"ball_in_zone_12\" = (s=12);\n" +
                "label \"ball_in_zone_13\" = (s=13);\n" +
                "label \"ball_in_zone_14\" = (s=14);\n" +
                "label \"ball_in_zone_15\" = (s=15);\n" +
                "label \"ball_in_zone_16\" = (s=16);\n" +
                "label \"ball_in_zone_17\" = (s=17);\n" +
                "label \"ball_in_zone_18\" = (s=18);\n" +
                "label \"ball_in_zone_19\" = (s=19);\n" +
                "label \"ball_in_zone_20\" = (s=20);\n" +
                "label \"ball_in_zone_21\" = (s=21);\n" +
                "label \"ball_in_zone_22\" = (s=22);\n" +
                "label \"ball_in_zone_23\" = (s=23);\n" +
                "label \"ball_in_zone_24\" = (s=24);\n" +
                "label \"ball_in_zone_25\" = (s=25);\n" +

                "label \"possession_lost\" = (s=26);\n" +

                "label \"goal\" = (s=27);")

prismFile.close()
