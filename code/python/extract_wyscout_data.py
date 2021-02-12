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

with open ("../../data/events_Italy.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)

shots = df[df['eventId'] == 10]
passes = df[df['eventId'] == 8]
freekicks = df[df['eventId'] == 3]

teams = df.teamId.unique()

eventsByTeam = {} 

for t in teams:
    eventsByTeam[str(t)] = df.loc[(df['teamId'] == t)]
            
zoneXYs = [
    [(50, 0),   (67, 100)],
    [(68, 0),    (83, 33)],
    [(68, 34),   (83, 66)],
    [(68, 67),  (83, 100)],
    [(84, 0),   (100, 33)],
    [(84, 34),  (100, 66)],
    [(84, 67), (100, 100)]
    ]    

# transition matrix - transmat[state][state']
transmat = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
    ]

# verifying all goals are accounted for

def fromZoneX(zone):
    if (zoneXYs[j][0][0] <= (event['positions'][0]['x']) 
        and (event['positions'][0]['x']) < zoneXYs[j][1][0]):
        return True
    else:
        return False
    
def fromZoneY(zone):
    if (zoneXYs[j][0][1] <= (event['positions'][0]['y']) 
        and (event['positions'][0]['y']) < zoneXYs[j][1][1]):
        return True
    else:
        return False
    
goals = 0

for i, fk in freekicks.iterrows():
    for tag in fk['tags']:
        if tag['id'] == 101:
            goals += 1
            
print("goals from free kicks: " + str(goals)) 

goals = 0

for i, event in df.iterrows():
    for tag in event['tags']:
        if tag['id'] == 102:
            goals += 1

print("own goals: " + str(goals))

goals = 0 

for i, shot in shots.iterrows():        
    for tag in shot['tags']:
        if tag['id'] == 101:
            goals += 1
            for j in range(0,7):
                if fromZoneX(j) and fromZoneY(j):
                    
                    

print("goals from open play: " + str(goals))   

# for j in range(0, 7):

#     for item in eventsByTeam.items():
#         for i, event in item[1].iterrows():
            
#             if (zoneXYs[j][0] <= \
#                 (event['positions'][0]['x'], event['positions'][0]['y'])) and \
#                 ((event['positions'][0]['x'], event['positions'][0]['y']) <= \
#                  zoneXYs[j][1]):
            
#                 # shots
#                  if (event['eventId'] == 10):
#                     for tag in event['tags']:
#                         if tag['id'] == 101:
#                             transmat[j][7]
#                         elif tag['id'] == 1802:
#                             transmat[j][8]
                            
                        
#                  elif (event['eventId'] == 8):
                    
#                     for tag in event['tags']:
                        
#                         if tag['id'] == 1802:
#                             transmat[j][8] += 1
                        
#                         elif tag['id'] == 1801:
                           
#                             # terminus zone 0
#                             if ((zoneXYs[0][0] <= \
#                             (event['positions'][1]['x'], event['positions'][1]['y'])) and \
#                             ((event['positions'][1]['x'], event['positions'][1]['y']) <= \
#                             zoneXYs[0][1])):
#                                 transmat[j][0] += 1
                            
#                             # terminus zone 1
#                             elif (zoneXYs[1][0] <= \
#                             (event['positions'][1]['x'], event['positions'][1]['y'])) and \
#                             ((event['positions'][1]['x'], event['positions'][1]['y']) <= \
#                             zoneXYs[1][1]):
#                                 transmat[j][1] += 1
                                
#                             # terminus zone 2
#                             elif (zoneXYs[2][0] <= \
#                             (event['positions'][1]['x'], event['positions'][1]['y'])) and \
#                             ((event['positions'][1]['x'], event['positions'][1]['y']) <= \
#                             zoneXYs[2][1]):
#                                 transmat[j][2] += 1
                                
#                             # terminus zone 3
#                             elif (zoneXYs[3][0] <= \
#                             (event['positions'][1]['x'], event['positions'][1]['y'])) and \
#                             ((event['positions'][1]['x'], event['positions'][1]['y']) <= \
#                             zoneXYs[3][1]):
#                                 transmat[j][3] += 1
                                
#                             # terminus zone 4
#                             elif (zoneXYs[4][0] <= \
#                             (event['positions'][1]['x'], event['positions'][1]['y'])) and \
#                             ((event['positions'][1]['x'], event['positions'][1]['y']) <= \
#                             zoneXYs[4][1]):
#                                 transmat[j][4] += 1
                                
#                             # terminus zone 5
#                             elif (zoneXYs[5][0] <= \
#                             (event['positions'][1]['x'], event['positions'][1]['y'])) and \
#                             ((event['positions'][1]['x'], event['positions'][1]['y']) <= \
#                             zoneXYs[5][1]):
#                                 transmat[j][5] += 1
                                
#                             # terminus zone 6
#                             elif (zoneXYs[6][0] <= \
#                             (event['positions'][1]['x'], event['positions'][1]['y'])) and \
#                             ((event['positions'][1]['x'], event['positions'][1]['y']) <= \
#                             zoneXYs[6][1]):
#                                 transmat[j][6] += 1
                                    
        
#     print(transmat[j])
            