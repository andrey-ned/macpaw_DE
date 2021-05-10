import sqlalchemy as sa
import pandas as pd
psql_host = 'local'

engine = sa.create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/macpaw')

# Створення бази даних
def init_db():


    engine.execute('''CREATE TABLE IF NOT EXISTS songs (index SERIAL, artist_name VARCHAR(512),
     title VARCHAR(512), year smallint , release VARCHAR(512),
     ingestion_time timestamp default now())''')

    engine.execute('''CREATE TABLE IF NOT EXISTS apps(index SERIAL, name VARCHAR(512),
         genre VARCHAR(512), rating FLOAT , version VARCHAR(512), 
         size_bytes Bigint, is_awesome bool)''')

    engine.execute('''CREATE TABLE IF NOT EXISTS movies(index SERIAL, original_title VARCHAR(512),
         original_language VARCHAR(512), budget Bigint, is_adult bool, release_date DATE ,
         original_title_normalized VARCHAR(512))
         ''')


def insert_songs(songs: pd.DataFrame):

    songs.to_sql('songs', con=engine, if_exists='append')


def insert_apps(songs: pd.DataFrame):

    songs.to_sql('apps', con=engine, if_exists='append')


def insert_movies(songs: pd.DataFrame):

    songs.to_sql('movies', con=engine, if_exists='append')
