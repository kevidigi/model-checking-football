#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script to build xG model using logistic regression
# For use with Wyscout data - avialable from 
# https://figshare.com/collections/Soccer_match_event_dataset/4415000/2

# Based on code provided by David Sumpter / Friends of Tracking (2020)
# https://www.youtube.com/channel/UCUBFJYcag8j2rm_9HkrrA7w

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import FCPython

def import_wyscout_data(filepath, df):
    with open(filepath) as f:
        data = json.load(f)
        
        df = df.append(data)
        return df



# intialise empty dataframe
df = pd.DataFrame()

# import leagues 
df = import_wyscout_data("../../data/events_Italy.json", df)
df = import_wyscout_data("../../data/events_Spain.json", df)
df = import_wyscout_data("../../data/events_France.json", df)
df = import_wyscout_data("../../data/events_Germany.json", df)
df = import_wyscout_data("../../data/events_England.json", df)

# strip shots from the event data
shots = df[df['subEventName'] == 'Shot']
shots_model = pd.DataFrame(columns = ['Goal', 'X', 'Y'])

for i, shot in shots.iterrows():
    
    # flag headers (to be ignored - significant difference in xG)
    header = 0
    for tag in shot['tags']:
        if tag['id'] == 403:
            header = 1
            
    if not(header):
        
        # calculate shot distance and angle (radians)
        shots_model.at[i, 'X'] = 100 - shot['positions'][0]['x']
        shots_model.at[i, 'Y'] = shot['positions'][0]['y']
        shots_model.at[i, 'C'] = abs(shot['positions'][0]['y'] - 50)
        
        # (first convert x,y to match FCPython.py pitch drawings
        x = shots_model.at[i, 'X'] * 105/100
        y = shots_model.at[i, 'C'] * 65/100
        
        # do some trig for distance and angle
        shots_model.at[i, 'Distance'] = np.sqrt(x**2 + y**2)
        a = np.arctan(7.32 * x / (x**2 + y**2 - (7.32/2)**2))
        
        if a < 0:
            a = np.pi + a
        shots_model.at[i, 'Angle'] = a
        
        # flag goals
        shots_model.at[i, 'Goal'] = 0
        for tag in shot['tags']:
            if tag['id'] == 101:
                shots_model.at[i, 'Goal'] = 1
                
# plot a 2D histogram of shots
shotplot = np.histogram2d(shots_model['X'], shots_model['Y'], bins = 50,
                          range = [[0,100], [0,100]])

# get goals and plot a 2D histogram of them
goals_only = shots_model[shots_model['Goal'] == 1]
goalplot = np.histogram2d(goals_only['X'], goals_only['Y'], bins = 50,
                          range = [[0,100], [0,100]])


# plot the shotplot
(fig, ax) = FCPython.createGoalMouth()
pos = ax.imshow(shotplot[0], extent = [-1, 66, 104, -1], aspect = 'auto',
                cmap = plt.cm.Blues)
fig.colorbar(pos, ax = ax)
ax.set_title('Number of Shots')
plt.xlim((-1, 66))
plt.ylim((-3, 35))
plt.tight_layout()
plt.gca().set_aspect('equal', adjustable = 'box')
plt.show()

# plot the goal plot
(fig, ax) = FCPython.createGoalMouth()
pos = ax.imshow(goalplot[0], extent = [-1, 66, 104, -1], aspect = 'auto',
                cmap = plt.cm.Greens)
fig.colorbar(pos, ax = ax)
ax.set_title('Number of Goals')
plt.xlim((-1, 66))
plt.ylim((-3, 35))
plt.tight_layout()
plt.gca().set_aspect('equal', adjustable = 'box')
plt.show()

# plot an xG histogram: goals / shots
(fig, ax) = FCPython.createGoalMouth()
pos = ax.imshow(goalplot[0] / shotplot[0], extent = [-1, 66, 104, -1],
                aspect = 'auto', cmap = plt.cm.Reds, vmin = 0, vmax = 0.5)
fig.colorbar(pos, ax = ax)
ax.set_title('Ratio of Goals to Shots')
plt.xlim((-1, 66))
plt.ylim((-3, 35))
plt.tight_layout()
plt.gca().set_aspect('equal', adjustable = 'box')
plt.show()

# plotting xG as a function of angle

shotcount_dist = np.histogram(shots_model['Angle'] * 180 / np.pi, bins=30,
                            range=[0, 150])
goalcount_dist = np.histogram(goals_only['Angle'] * 180 / np.pi, bins=30,
                            range=[0, 150])
prob_goal = np.divide(goalcount_dist[0], shotcount_dist[0])
angle = shotcount_dist[1]
midangle = (angle[:-1] + angle[1:]) / 2
(fig, ax) = plt.subplots(num = 2)
ax.plot(midangle, prob_goal, linestyle='none', marker = '.', markerSize = 6, 
        color = 'green')
ax.set_ylabel('Probability of Goal')
ax.set_xlabel("Shot Angle (degrees)")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# single variable model of xG as a function of angle
# logistic regression finds the optimal coefficients
# by minimising the loglikelihood

test_model = smf.glm(formula = "Goal ~ Angle" , data = shots_model, 
                           family = sm.families.Binomial()).fit()
print(test_model.summary())        
b = test_model.params

xGprob = 1 / (1+np.exp(b[0] + b[1] * midangle * np.pi / 180)) 
(fig, ax) = plt.subplots(num = 1)
ax.plot(midangle, prob_goal, linestyle='none', marker = '.', markerSize = 6, 
        color = 'green')
ax.plot(midangle, xGprob, linestyle = 'solid', color = 'grey')
ax.set_ylabel('Probability of Goal')
ax.set_xlabel("Shot Angle (degrees)")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()

# same again but for xG as a function of distance

shotcount_dist = np.histogram(shots_model['Distance'], bins = 30,
                              range = [0, 70])
goalcount_dist = np.histogram(goals_only['Distance'], bins = 30,
                              range = [0, 70])
prob_goal = np.divide(goalcount_dist[0], shotcount_dist[0])
distance = shotcount_dist[1]
middistance = (distance[:-1] + distance[1:]) / 2
(fig, ax) = plt.subplots(num = 1)
ax.plot(middistance, prob_goal, linestyle = 'none', marker = '.', 
        color='green')
ax.set_ylabel('Probability of Goal')
ax.set_xlabel("Distance from Goal (metres)")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

test_model = smf.glm(formula = "Goal ~ Distance" , data = shots_model, 
                           family = sm.families.Binomial()).fit()
print(test_model.summary())        
b = test_model.params

xGprob = 1 / (1 + np.exp(b[0] + b[1] * middistance)) 
ax.plot(middistance, xGprob, linestyle = 'solid', color='grey')
plt.show()

# create a 2-variable model - xG as function of angle and distance

model_variables = ['Angle','Distance']
model=''
for v in model_variables[:-1]:
    model = model  + v + ' + '
model = model + model_variables[-1]

# fit the model
test_model = smf.glm(formula = "Goal ~ " + model, data = shots_model, 
                     family = sm.families.Binomial()).fit()
print(test_model.summary())        
b=test_model.params

# return xG value for more general model
def calculate_xG(sh):    
   bsum = b[0]
   for i, v in enumerate(model_variables):
       bsum = bsum + b[i + 1] * sh[v]
   xG = 1 / (1 + np.exp(bsum)) 
   return xG   

# add an xG column to the original shots_model dataframe
# xG = shots_model.apply(calculate_xG, axis = 1) 
# shots_model = shots_model.assign(xG = xG)

# xgplot = np.histogram2d(shots_model['X'], shots_model['Y'], bins = [5, 5],
#                           weights = shots_model['xG'], normed = False, range = [[0,100], [0,100]])

# # plot the shotplot
# (fig, ax) = FCPython.createGoalMouth()
# pos = ax.imshow(xgplot[0], extent = [-1, 66, 104, -1], aspect = 'auto',
#                 cmap = plt.cm.Blues)
# fig.colorbar(pos, ax = ax)
# ax.set_title('Probability of Goal')
# plt.xlim((-1, 66))
# plt.ylim((-3, 35))
# plt.tight_layout()
# plt.gca().set_aspect('equal', adjustable = 'box')
# plt.show()
        
#Add an xG to my dataframe
xG=shots_model.apply(calculate_xG, axis=1) 
shots_model = shots_model.assign(xG=xG)

#Create a 2D map of xG
pgoal_2d=np.zeros((65,65))
for x in range(65):
    for y in range(65):
        sh=dict()
        a = np.arctan(7.32 *x /(x**2 + abs(y-65/2)**2 - (7.32/2)**2))
        if a<0:
            a = np.pi + a
        sh['Angle'] = a
        sh['Distance'] = np.sqrt(x**2 + abs(y-65/2)**2)
        
        pgoal_2d[x,y] =  calculate_xG(sh)

(fig,ax) = FCPython.createGoalMouth()
pos=ax.imshow(pgoal_2d, extent=[-1,65,65,-1], aspect='auto',cmap=plt.cm.Reds,vmin=0, vmax=0.3)
fig.colorbar(pos, ax=ax)
ax.set_title('Probability of goal')
plt.xlim((0,66))
plt.ylim((-3,35))
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
fig.savefig('Output/goalprobfor_' + model  + '.pdf', dpi=None, bbox_inches="tight")   
