#!/usr/bin/env python3

import pandas as pd
from scipy.stats import entropy


#load data
countries = pd.read_csv('data/processed/countries.csv')
matches = pd.read_csv('data/processed/matches.csv')
leagues = pd.read_csv('data/processed/leagues.csv')


def match_entropy(row):
    odds = [row['B365H'],row['B365D'],row['B365A']]
    #change odds to probability
    probs = [1/o for o in odds]
    #normalize to sum to 1
    norm = sum(probs)
    probs = [p/norm for p in probs]
    return entropy(probs)


#select relevant countries and merge with leagues
selected_countries = ['England','France','Germany','Italy','Spain']
countries = countries[countries.name.isin(selected_countries)]
leagues = countries.merge(leagues,on='id',suffixes=('', '_y'))

#select relevant fields
matches = matches[matches.league_id.isin(leagues.id)]
matches = matches[['id', 'country_id' ,'league_id', 'season', 'stage', 'date','match_api_id', 'home_team_api_id', 'away_team_api_id',
    'B365H', 'B365D' ,'B365A']]

#compute match entropy
matches['entropy'] = matches.apply(match_entropy,axis=1)

#compute mean entropy for every league in every season
entropy_means = matches.groupby(['season','League']).entropy.mean()
entropy_means = entropy_means.reset_index().pivot(index='season', columns='League', values='entropy')
entropy_means.to_csv('data/processed/entropy_means.csv')
