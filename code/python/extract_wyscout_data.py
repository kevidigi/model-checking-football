#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script for extraction of transition probabilities (state to state) 
# from Wyscout football data (json).

# @author: Kevin Lynch <kevin.lynch@glasgow.ac.uk>

import pandas as pd
import numpy as np
import json
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

def fromZoneX(j, event):
    if (zoneXYs[j][0][0] <= (event['positions'][0]['x']) 
        and (event['positions'][0]['x']) <= zoneXYs[j][1][0]):
        return True
    else:
        return False
    
def fromZoneY(j, event):
    if (zoneXYs[j][0][1] <= (event['positions'][0]['y']) 
        and (event['positions'][0]['y']) <= zoneXYs[j][1][1]):
        return True
    else:
        return False

def calculate_transition_matrix(filename):

    with open (filename) as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    shots = df[df['eventId'] == 10]
    passes = df[df['eventId'] == 8]
    
    teams = df.teamId.unique()
    
    eventsByTeam = {} 
    
    for t in teams:
        eventsByTeam[str(t)] = df.loc[(df['teamId'] == t)]
        
    # populate transition matrix with goals            
    for i, shot in shots.iterrows():        
        for tag in shot['tags']:
            if tag['id'] == 101:
                for j in range(0,7):
                    if fromZoneX(j, shot) and fromZoneY(j, shot):
                        trans_mat[j][8] += 1 
    
# transition matrix - trans_mat[state][state']
# trans_mat[..][7] is possession lost
# trans_mat[..][8] is a goal
trans_mat = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
    ]

calculate_transition_matrix("../../data/events_Italy.json")
calculate_transition_matrix("../../data/events_France.json")
calculate_transition_matrix("../../data/events_Spain.json")
calculate_transition_matrix("../../data/events_Germany.json")
calculate_transition_matrix("../../data/events_England.json")

print(trans_mat)