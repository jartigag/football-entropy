#!/usr/bin/env python3
#
#usage: ./make_dataset.py ../../data/raw/database.sqlite ../../data/processed/matches.csv

import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import sqlite3
import pandas as pd


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)

    logger.info('making final data set from raw data')

    with sqlite3.connect(f"{input_filepath}/database.sqlite") as con:
        # (downloaded from https://www.kaggle.com/hugomathien/soccer, updated on 2016)

        db_df = pd.read_sql_query("SELECT * FROM Country", con)
        db_df.to_csv(f"{output_filepath}/countries.csv", index=False)

        db_df = pd.read_sql_query("SELECT * FROM Match", con)
        db_df.to_csv(f"{output_filepath}/matches.csv", index=False)

        db_df = pd.read_sql_query("SELECT * FROM League", con)
        db_df.to_csv(f"{output_filepath}/leagues.csv", index=False)

        db_df = pd.read_sql_query("SELECT team_api_id, team_long_name FROM Team", con)
        db_df.to_csv(f"{output_filepath}/teams.csv", index=False)

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
