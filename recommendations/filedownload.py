import requests
import pandas as pd


URL = 'http://127.0.0.1:8000/api/v1/movies/test/'
params = {}


movies = requests.get(URL).json()
df = pd.json_normalize(movies)

df.to_csv('movie-whole-data.csv')

