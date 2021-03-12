#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script for extraction of probabilities for PRISM models
# from Statsbomb football data using the statsbombpy package.
# The state transitions occur via passes and shots.

# @author: Kevin Lynch <kevin.lynch@glasgow.ac.uk>

from statsbombpy import sb
import time

competitions = sb.competitions()
champions_league = competitions[competitions['competition_id'] == 16]
la_liga = competitions[competitions['competition_id'] == 11]
premier_league = competitions[competitions['competition_id'] == 2]
world_cup = competitions[competitions['competition_id'] == 43]

competitions = [champions_league, la_liga, premier_league, world_cup]

def scrape_comp_events(competition):
    # for each competition
    for index, comp in competition.iterrows():
        
        # get matches as dict and convert back to dataframe (bug workaround)
        matches = sb.matches(comp['competition_id'], comp['season_id'], fmt="dict")
        
        # for each match
        for index, match in matches.items():
            
            # get events
            events = sb.events(index)
            print('ok')
            passes = events[events['type'] == 'Pass']
            shots  = events[events['type'] == 'Shot']
            
            # for each pass
            for p in passes:
                # find start zone and record it
                zone_from = p['location']
                # if pass successful
                    # find end zone and record it 
                # else
                    # try to infer intent
                    # take shot angle, note any zones in path
                    # at 1/n to all n zones the ball would reach
                    
                # no explicit indicator of pass success in StatsBomb data 

start = time.time()
    
for c in competitions:
    scrape_comp_events(c)

end = time.time()
print("time elapsed: " + str(round(((end - start) / 60), 2)) 
      + " mins (approx)")

# and this took over half an hour