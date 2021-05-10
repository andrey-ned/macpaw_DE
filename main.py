import json
import time
from string import punctuation, digits

import requests
import pandas as pd

import db

file_list_name = 'files_list.data'
target_url = f'https://data-engineering-interns.macpaw.io/'
cache = set()


def main():
    global cache
    response = requests.get(target_url + file_list_name)
    list_of_json = response.text.split('\n')

    local_cache = set(list_of_json)

    if not local_cache.difference(cache):
        return
    json_urls = iter(local_cache.difference(cache))
    cache |= local_cache

    for url in json_urls:
        parser(url)
    print('ready')


def parser(json_url):
    response = requests.get(target_url + json_url).text
    data = json.loads(response)

    df = pd.DataFrame(data)

    df_songs = df[df['type'] == 'song']['data']
    df_songs = pd.json_normalize(df_songs)

    df_apps = df[df['type'] == 'app']['data']
    df_apps = pd.json_normalize(df_apps)
    df_apps.loc[df_apps['rating'] >= 4, 'is_awesome'] = True

    df_movies = df[df['type'] == 'movie']['data']
    df_movies = pd.json_normalize(df_movies)
    df_movies['original_title_normalized'] = df_movies['original_title'].str.lower()\
        .str.translate({'':punctuation+digits}).replace('(\s)', '_', regex=True)

    db.insert_songs(df_songs)
    db.insert_apps(df_apps)
    db.insert_movies(df_movies)


if __name__ == '__main__':
    db.init_db()
    while True:
        main()
        time.sleep(5)
