#!/usr/bin/env python3
#
#usage: ./make_dataset.py ../../data/raw/database.sqlite ../../data/processed/matches.csv

import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import sqlite3
import pandas as pd
from src.features.build_features import process
from src.visualization.visualize import make_visualizations

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)

    logger.info('making final data set from raw data..')

    with sqlite3.connect(f"{input_filepath}/database.sqlite") as con:
        # (downloaded from https://www.kaggle.com/hugomathien/soccer, updated on 2016)

        countries = pd.read_sql_query("SELECT * FROM Country", con)
        countries.to_csv(f"{output_filepath}/countries.csv", index=False)

        matches = pd.read_sql_query("SELECT league_id, season, date, home_team_api_id, away_team_api_id, B365H, B365D, B365A FROM Match", con)
        #matches.to_csv(f"{output_filepath}/matches-2008-2016.csv", index=False)

        teams = pd.read_sql_query("SELECT team_api_id, team_long_name FROM Team", con)
        teams.to_csv(f"{output_filepath}/teams.csv", index=False)

        leagues = pd.read_sql_query("SELECT * FROM League", con)
        leagues.to_csv(f"{output_filepath}/leagues.csv", index=False)

    # matches from 2016/17 to 2019/20 downloaded from https://www.football-data.co.uk/

    def get_team_api_id(team_name):
        """ Scrubbing-data function to get the unique team_api_id,
            because the csv files for matches since 2016/2017 contain team names instead.
        """

        # solve ambiguities:
        if team_name=="Schalke 04":
            team_name = "Schalke 04"
        elif team_name=="M'gladbach":
            team_name = "Borussia Mönchengladbach"
        elif team_name=="Man City":
            team_name = "Manchester City"
        elif team_name=="Man United":
            team_name = "Manchester United"
        elif team_name=="West Brom":
            team_name = "West Bromwich Albion"
        elif team_name=="West Ham":
            team_name = "West Ham United"
        elif team_name=="Aston Villa":
            team_name = "Aston Villa"
        elif team_name=="Sheffield United":
            team_name = "Sheffield United"
        elif team_name=="Verona":
            team_name = "Hellas Verona"
        elif team_name=="Ath Madrid":
            team_name = "Atlético Madrid"
        elif team_name=="Real Madrid":
            team_name = "Real Madrid"
        else:
            team_name = team_name.split()[-1] # when team_name is two words or more, get the last one

        founded_team_api_id = teams[teams.team_long_name.str.contains(team_name)].team_api_id
        team_api_id = int(founded_team_api_id) if not founded_team_api_id.empty else 0

        return team_api_id

    league_id = {'D1-bundesliga_1': 7809, 'E0-premier_league': 1729, 'F1-le_championnat': 4769, 'I1-serie_a': 10257, 'SP1-la_liga_primera_div': 21518}

    for league in ['D1-bundesliga_1', 'E0-premier_league', 'F1-le_championnat', 'I1-serie_a', 'SP1-la_liga_primera_div']:
        for season in ['2016-2017', '2017-2018', '2018-2019', '2019-2020']:
            new_matches = pd.read_csv(f"{input_filepath}/{league}-{season}.csv", usecols=['Date','HomeTeam','AwayTeam', 'B365H', 'B365D' ,'B365A'], parse_dates=['Date'])
            new_matches['league_id'] = league_id[league]
            new_matches['season'] = season.replace('-','/')
            new_matches['home_team_api_id'] = new_matches['HomeTeam'].apply(get_team_api_id)
            new_matches['away_team_api_id'] = new_matches['AwayTeam'].apply(get_team_api_id)
            matches = pd.concat([matches, new_matches])

    matches.to_csv(f"{output_filepath}/matches.csv", index=False)

    #./src/features/build_features.py
    logger = logging.getLogger(".".join([process.__module__,process.__name__]))
    logger.info('building features..')
    entropy_means, matches = process(matches, countries, leagues)

    #./src/visualization/visualize.py
    logger = logging.getLogger(".".join([make_visualizations.__module__,make_visualizations.__name__]))
    logger.info('making visualizations..')
    make_visualizations(matches, entropy_means, teams)

    logger.info('final data set done.')

#                                                                                     B365{H,D,A}: Bet365 {home win, draw, away win} odds
#db_df = pd.read_sql_query("SELECT Country.name as 'Country', League.name as 'League', B365H, B365D, B365A, \
#        league_id, season, date, home_team_api_id, away_team_api_id FROM Match \
#        left JOIN Country ON Match.country_id = Country.id \
#        WHERE Country.name IN ('England','France','Germany','Italy','Spain')", con)
#db_df.to_csv(f"{output_filepath}/matches.csv", index=False)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
