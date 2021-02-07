#!/usr/bin/env python3

import pandas as pd
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def make_visualizations(matches, entropy_means, teams):

    ## -- Leagues Predictability -- ##

    num_seasons = len(matches.season.unique())
    ax = entropy_means.plot(figsize=(12,8),marker='o') #plot graph
    plt.title('Leagues Predictability', fontsize=16)   #set title
    plt.xticks(np.arange(0, num_seasons, 1), matches.season.unique(), rotation=50) #set ticks frequency, labels and rotation
    colors = [x.get_color() for x in ax.get_lines()]   #keep colors for next graph
    colors_mapping = dict(zip(matches.League.unique(),colors))
    ax.set_xlabel('')                                  #remove x label
    plt.legend(loc='lower left')                       #locate legend
    #add arrows:
    ax.annotate('', xytext=(11.7, 1),xy=(11.7, 1.029),
                arrowprops=dict(facecolor='black',arrowstyle="->, head_length=.7, head_width=.3",linewidth=1), annotation_clip=False)
    ax.annotate('', xytext=(11.7, 0.96),xy=(11.7, 0.931),
                arrowprops=dict(facecolor='black',arrowstyle="->, head_length=.7, head_width=.3",linewidth=1), annotation_clip=False)
    ax.annotate('less predictable', xy=(11.8, 0.99), annotation_clip=False,fontsize=14,rotation='vertical')
    ax.annotate('more predictable', xy=(11.8, 0.952), annotation_clip=False,fontsize=14,rotation='vertical')

    plt.savefig('reports/figures/leagues_pred.png', bbox_inches='tight',dpi=600)

    ## -- Teams Predictability -- ##

    offsets = [-0.16,-0.08,0,0.08,0.16]
    colors_mapping = dict(zip(matches.league_id.unique(),colors))
    offsets_mapping = dict(zip(colors_mapping.keys(),offsets))
    y = []
    x = []
    c = []

    i = -1
    for season,season_df in matches.groupby('season'):
        i+=1
        for team,name in zip(teams.team_api_id,teams.team_long_name):
            team_df = season_df[(season_df.home_team_api_id==team)|(season_df.away_team_api_id==team)]
            team_entropy = team_df.entropy.mean()
            if team_entropy>0:
                league_id = team_df.league_id.values[0]
                x.append(i+offsets_mapping[league_id])
                y.append(team_entropy)
                c.append(colors_mapping[league_id])

    plt.figure(figsize=(16,8))
    plt.scatter(x,y,color=c,s=[60]*len(x))
    plt.title('Teams Predictability', fontsize=16)

    #create ticks and labels
    ax = plt.gca()
    plt.xlim((-0.5,num_seasons-0.5))
    plt.xticks(np.arange(0,num_seasons,1),rotation=50)

    #create grid
    ax.set_xticklabels(entropy_means.index,fontsize=12)
    for i in range(num_seasons-1):
        ax.axvline(x=0.5+i,ls='--',c='w')
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)

    #create legend
    circles = []
    labels = []
    leagues = matches.groupby(['league_id','League']).count().reset_index()
    for league_id,name in zip(leagues.league_id,leagues.League):
        labels.append(name)
        circles.append(Line2D([0], [0], linestyle="none", marker="o", markersize=8, markerfacecolor=colors_mapping[league_id]))
    plt.legend(circles, labels, numpoints=3, loc=(0.005,0.02))

    #add arrows
    ax.annotate('', xytext=(11.65, 0.93),xy=(11.65, 1.07),
                arrowprops=dict(facecolor='black',arrowstyle="->, head_length=.7, head_width=.3",linewidth=1), annotation_clip=False)
    ax.annotate('', xytext=(11.65, 0.77),xy=(11.65, 0.61),
                arrowprops=dict(facecolor='black',arrowstyle="->, head_length=.7, head_width=.3",linewidth=1), annotation_clip=False)
    ax.annotate('less predictable', xy=(11.75, 0.88), annotation_clip=False,fontsize=14,rotation='vertical')
    ax.annotate('more predictable', xy=(11.75, 0.73), annotation_clip=False,fontsize=14,rotation='vertical')

    #add labels
    ax.annotate('Barcelona', xy=(6.55, 0.634),fontsize=9)
    ax.annotate('B. Munich', xy=(6.5, 0.655),fontsize=9)
    ax.annotate('Real Madrid', xy=(6.51, 0.731),fontsize=9)
    ax.annotate('PSG', xy=(6.93, 0.78),fontsize=9)

    plt.savefig('reports/figures/teams_pred.png', bbox_inches='tight',dpi=600)

if __name__ == '__main__':
    #load data
    matches = pd.read_csv('data/processed/matches_with_entropy.csv')
    entropy_means = pd.read_csv('data/processed/entropy_means.csv')
    teams = pd.read_csv('data/processed/teams.csv')
    #leagues = pd.read_csv('data/processed/leagues.csv')
    #TODO: load so 'season' appears on x axis

    make_visualizations(matches, entropy_means, teams)
