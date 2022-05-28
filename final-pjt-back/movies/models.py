from tkinter import CASCADE
from django.db import models


class GenreSort(models.Model):  # 장르 구분을 위한 모델. 수동으로 입력해주어야 함.
    '''
    1. [범죄, 스릴러, 미스터리, 공포] 
    2. [판타지, SF]
    3. [애니메이션]
    4. [액션, 모험, 서부, 전쟁]
    5. [드라마, 가족, 로맨스, 음악, TV 영화]
    6. [다큐멘터리, 역사]
    7. [코미디]
    '''
    pass

class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    genre_name = models.CharField(max_length=20)
    genre_sort = models.ForeignKey(GenreSort, related_name='genres', null=True, on_delete=models.SET_NULL)


class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    overview = models.TextField(null=True)
    en_overview = models.TextField(null=True)
    release_date = models.DateField()
    runtime = models.IntegerField()
    poster_path = models.TextField()
    original_title = models.CharField(max_length=100)
    original_language = models.CharField(max_length=100)
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    imdb_id = models.CharField(max_length=10, null=True)


class Actor(models.Model):
    actor_id = models.IntegerField(primary_key=True)
    gender = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    biography = models.TextField(null=True)
    imdb_id = models.CharField(max_length=100, null=True)
    profile_path = models.CharField(max_length=500, null=True)
    popularity = models.FloatField(default=0)
    filmographies = models.ManyToManyField(Movie, related_name='actors')

class MovieImage(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    image_URL = models.CharField(max_length=500)


class Director(models.Model):
    director_id = models.IntegerField(primary_key=True)
    gender = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    biography = models.TextField(null=True)
    imdb_id = models.CharField(max_length=100, null=True)
    profile_path = models.CharField(max_length=500, null=True)
    popularity = models.FloatField(default=0)
    filmographies = models.ManyToManyField(Movie, related_name='directors')



class Provider(models.Model):
    provider_id = models.IntegerField(primary_key=True)
    provider_name = models.CharField(max_length=30)
    owned_movies = models.ManyToManyField(Movie, related_name='OTTs')