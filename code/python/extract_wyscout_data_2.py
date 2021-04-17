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
                        decision_mat[j][7] += 1
            # and 'possession lost' from a shot
            else:
                for j in range(0,7):
                    if fromZoneX(j, shot) and fromZoneY(j, shot):
                        trans_mat[j][7] += 1
                        decision_mat[j][7] += 1
    
    # populate transition matrix for 'possession lost' from passes
    for i, aPass in passes.iterrows():
        for tag in aPass['tags']:
            if tag['id'] == 1802:
                for j in range(0,7):
                    if fromZoneX(j, aPass) and fromZoneY(j, aPass):
                        trans_mat[j][7] += 1
                        for k in range (0,7):
                            if toZoneX(k, aPass) and toZoneY(k, aPass):
                                    decision_mat[j][k] += 1
            # and terminal zones for each successful pass
            elif tag['id'] == 1801:
                for j in range(0,7):
                    if fromZoneX(j, aPass) and fromZoneY(j, aPass):
                        for k in range (0,7):
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
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1]
]

# pass from [i] to [j] or shoot ( [i][7] ) 
decision_mat = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

succ_mat = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

start = time.time()

calculate_transition_matrix("../../data/events_Italy.json")
calculate_transition_matrix("../../data/events_France.json")
calculate_transition_matrix("../../data/events_Spain.json")
calculate_transition_matrix("../../data/events_Germany.json")
calculate_transition_matrix("../../data/events_England.json")

for r in range (0,7):
    for c in range (0,7):
        succ_mat[r][c] = (trans_mat[r][c] / decision_mat[r][c])
        
    succ_mat[r][7] = trans_mat[r][8] / decision_mat[r][7]

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

pd.DataFrame(trans_mat).to_csv("./probabilities.txt")   
pd.DataFrame(succ_mat).to_csv("./decision_success.txt")

end = time.time()
print("time elapsed: " + str(round(((end - start) / 60), 2)) 
      + " mins (approx)")

prismFile = open("../prism/markovdecisionprocess.pm", "w");
prismFile.write("mdp\n\n" +
                "module passes_and_shots\n\n\t" +
                "// states: 0-6 = zones on the pitch; 7 = possession lost;" +
                " 8 = goal scored\n\t" +
                "s : [0..8];\n\t" +
                "// player actions from zone 0 (s=0)\n\t" +
                "[pass_0_0]\t      s=0 ->\n\t" +
                str(succ_mat[0][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[0][0]) + ") : (s'=7);\n\t" +
                "[pass_0_1]\t      s=0 ->\n\t" +
                str(succ_mat[0][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[0][1]) + ") : (s'=7);\n\t" +
                "[pass_0_2]\t      s=0 ->\n\t" +
                str(succ_mat[0][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[0][2]) + ") : (s'=7);\n\t" +
                "[pass_0_3]\t      s=0 ->\n\t" +
                str(succ_mat[0][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[0][3]) + ") : (s'=7);\n\t" +
                "[pass_0_4]\t      s=0 ->\n\t" +
                str(succ_mat[0][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[0][4]) + ") : (s'=7);\n\t" +
                "[pass_0_5]\t      s=0 ->\n\t" +
                str(succ_mat[0][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[0][5]) + ") : (s'=7);\n\t" +
                "[pass_0_6]\t      s=0 ->\n\t" +
                str(succ_mat[0][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[0][6]) + ") : (s'=7);\n\t" +
                "[shoot_0]\t       s=0 ->\n\t" +
                str(succ_mat[0][7]) + " : (s'=8) + (1 - " + 
                str(succ_mat[0][7]) + ") : (s'=7);\n\n\t" +

                "// player actions from zone 1 (s=1)\n\t" +
                "[pass_1_0]\t      s=1 ->\n\t" +
                str(succ_mat[1][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[1][0]) + ") : (s'=7);\n\t" +
                "[pass_1_1]\t      s=1 ->\n\t" +
                str(succ_mat[1][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[1][1]) + ") : (s'=7);\n\t" +
                "[pass_1_2]\t      s=1 ->\n\t" +
                str(succ_mat[1][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[1][2]) + ") : (s'=7);\n\t" +
                "[pass_1_3]\t      s=1 ->\n\t" +
                str(succ_mat[1][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[1][3]) + ") : (s'=7);\n\t" +
                "[pass_1_4]\t      s=1 ->\n\t" +
                str(succ_mat[1][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[1][4]) + ") : (s'=7);\n\t" +
                "[pass_1_5]\t      s=1 ->\n\t" +
                str(succ_mat[1][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[1][5]) + ") : (s'=7);\n\t" +
                "[pass_1_6]\t      s=1 ->\n\t" +
                str(succ_mat[1][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[1][6]) + ") : (s'=7);\n\t" +
                "[shoot_1]\t       s=1 ->\n\t" +
                str(succ_mat[1][7]) + " : (s'=8) + (1 - " 
                + str(succ_mat[1][7]) + ") : (s'=7);\n\n\t" +

                "// player actions from zone 2 (s=2)\n\t" +
                "[pass_2_0]\t      s=2 ->\n\t" +
                str(succ_mat[2][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[2][0]) + ") : (s'=7);\n\t" +
                "[pass_2_1]\t      s=2 ->\n\t" +
                str(succ_mat[2][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[2][1]) + ") : (s'=7);\n\t" +
                "[pass_2_2]\t      s=2 ->\n\t" +
                str(succ_mat[2][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[2][2]) + ") : (s'=7);\n\t" +
                "[pass_2_3]\t      s=2 ->\n\t" + 
                str(succ_mat[2][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[2][3]) + ") : (s'=7);\n\t" +
                "[pass_2_4]\t      s=2 ->\n\t" +
                str(succ_mat[2][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[2][4]) + ") : (s'=7);\n\t" +
                "[pass_2_5]\t      s=2 ->\n\t" +
                str(succ_mat[2][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[2][5]) + ") : (s'=7);\n\t" +
                "[pass_2_6]\t      s=2 ->\n\t" +
                str(succ_mat[2][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[2][6]) + ") : (s'=7);\n\t" +
                "[shoot_2]\t       s=2 ->\n\t" +
                str(succ_mat[2][7]) + " : (s'=8) + (1 - " + 
                str(succ_mat[2][7]) + ") : (s'=7);\n\n\t" +

                "// player actions from zone 3 (s=3)\n\t" +
                "[pass_3_0]\t      s=3 ->\n\t" +
                str(succ_mat[3][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[3][0]) + ") : (s'=7);\n\t" +
                "[pass_3_1]\t      s=3 ->\n\t" +
                str(succ_mat[3][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[3][1]) + ") : (s'=7);\n\t" +
                "[pass_3_2]\t      s=3 ->\n\t" +
                str(succ_mat[3][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[3][2]) + ") : (s'=7);\n\t" +
                "[pass_3_3]\t      s=3 ->\n\t" +
                str(succ_mat[3][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[3][3]) + ") : (s'=7);\n\t" + 
                "[pass_3_4]\t      s=3 ->\n\t" +
                str(succ_mat[3][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[3][4]) + ") : (s'=7);\n\t" +
                "[pass_3_5]\t      s=3 ->\n\t" +
                str(succ_mat[3][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[3][5]) + ") : (s'=7);\n\t" +
                "[pass_3_6]\t      s=3 ->\n\t" +
                str(succ_mat[3][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[3][6]) + ") : (s'=7);\n\t" +
                "[shoot_3]\t       s=3 ->\n\t" +
                str(succ_mat[3][7]) + " : (s'=8) + (1 - " + 
                str(succ_mat[3][7]) + ") : (s'=7);\n\n\t" +

                "// player actions from zone 4 (s=4)\n\t" +
                "[pass_4_0]\t      s=4 ->\n\t" +
                str(succ_mat[4][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[4][0]) + ") : (s'=7);\n\t" +
                "[pass_4_1]\t      s=4 ->\n\t" +
                str(succ_mat[4][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[4][1]) + ") : (s'=7);\n\t" +
                "[pass_4_2]\t      s=4 ->\n\t" +
                str(succ_mat[4][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[4][2]) + ") : (s'=7);\n\t" +
                "[pass_4_3]\t      s=4 ->\n\t" +
                str(succ_mat[4][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[4][3]) + ") : (s'=7);\n\t" +
                "[pass_4_4]\t      s=4 ->\n\t" +
                str(succ_mat[4][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[4][4]) + ") : (s'=7);\n\t" +
                "[pass_4_5]\t      s=4 ->\n\t" +
                str(succ_mat[4][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[4][5]) + ") : (s'=7);\n\t" +
                "[pass_4_6]\t      s=4 ->\n\t" +
                str(succ_mat[4][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[4][6]) + ") : (s'=7);\n\t" +
                "[shoot_4]\t       s=4 ->\n\t" +
                str(succ_mat[4][7]) + " : (s'=8) + (1 - " + 
                str(succ_mat[4][7]) + ") : (s'=7);\n\n\t" +

                "// player actions from zone 5 (s=5)\n\t" +
                "[pass_5_0]\t      s=5 ->\n\t" +
                str(succ_mat[5][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[5][0]) + ") : (s'=7);\n\t" +
                "[pass_5_1]\t      s=5 ->\n\t" +
                str(succ_mat[5][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[5][1]) + ") : (s'=7);\n\t" +
                "[pass_5_2]\t      s=5 ->\n\t" +
                str(succ_mat[5][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[5][2]) + ") : (s'=7);\n\t" +
                "[pass_5_3]\t      s=5 ->\n\t" +
                str(succ_mat[5][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[5][3]) + ") : (s'=7);\n\t" +
                "[pass_5_4]\t      s=5 ->\n\t" + 
                str(succ_mat[5][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[5][4]) + ") : (s'=7);\n\t" +
                "[pass_5_5]\t      s=5 ->\n\t" +
                str(succ_mat[5][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[5][5]) + ") : (s'=7);\n\t" +
                "[pass_5_6]\t      s=5 ->\n\t" +
                str(succ_mat[5][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[5][6]) + ") : (s'=7);\n\t" +
                "[shoot_5]\t       s=5 ->\n\t" +
                str(succ_mat[5][7]) + " : (s'=8) + (1 - " + 
                str(succ_mat[5][7]) + ") : (s'=7);\n\n\t" +

                "// player actions from zone 6 (s=6)\n\t" +
                "[pass_6_0]\t      s=6 ->\n\t" +
                str(succ_mat[6][0]) + " : (s'=0) + (1 - " + 
                str(succ_mat[6][0]) + ") : (s'=7);\n\t" +
                "[pass_6_1]\t      s=6 ->\n\t" +
                str(succ_mat[6][1]) + " : (s'=1) + (1 - " + 
                str(succ_mat[6][1]) + ") : (s'=7);\n\t" +
                "[pass_6_2]\t      s=6 ->\n\t" +
                str(succ_mat[6][2]) + " : (s'=2) + (1 - " + 
                str(succ_mat[6][2]) + ") : (s'=7);\n\t" +
                "[pass_6_3]\t      s=6 ->\n\t" +
                str(succ_mat[6][3]) + " : (s'=3) + (1 - " + 
                str(succ_mat[6][3]) + ") : (s'=7);\n\t" +
                "[pass_6_4]\t      s=6 ->\n\t" +
                str(succ_mat[6][4]) + " : (s'=4) + (1 - " + 
                str(succ_mat[6][4]) + ") : (s'=7);\n\t" +
                "[pass_6_5]\t      s=6 ->\n\t" +
                str(succ_mat[6][5]) + " : (s'=5) + (1 - " + 
                str(succ_mat[6][5]) + ") : (s'=7);\n\t" +
                "[pass_6_6]\t      s=6 ->\n\t" +
                str(succ_mat[6][6]) + " : (s'=6) + (1 - " + 
                str(succ_mat[6][6]) + ") : (s'=7);\n\t" +
                "[shoot_6]\t       s=6 ->\n\t" +
                str(succ_mat[6][7]) + " : (s'=8) + (1 - " + 
                str(succ_mat[6][7]) + ") : (s'=7);\n\n\t" +

                "// absorbing states\n\t" +
                "[] s=7 -> (s'=7);\n\t" +
                "[] s=8 -> (s'=8);\n\n" +

                "endmodule\n\n" +
                
                "label \"ball_in_zone_0\" = (s=0);\n" +
                "label \"ball_in_zone_1\" = (s=1);\n" +
                "label \"ball_in_zone_2\" = (s=2);\n" +
                "label \"ball_in_zone_3\" = (s=3);\n" +
                "label \"ball_in_zone_4\" = (s=4);\n" +
                "label \"ball_in_zone_5\" = (s=5);\n" +
                "label \"ball_in_zone_6\" = (s=6);\n" +
                "label \"possession_lost\" = (s=7);\n" +
                "label \"goal\" = (s=8);")

prismFile.close()
