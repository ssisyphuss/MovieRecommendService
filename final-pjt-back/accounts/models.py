from django.contrib.auth.models import AbstractUser
from django.db import models
from movies.models import Movie, Genre, Actor
from django.conf import settings

class User(AbstractUser):
    followings = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')
    movie_likes = models.ManyToManyField(Movie, related_name = 'liking_users')  # 좋아요한 영화 등록
    actor_likes = models.ManyToManyField(Actor, related_name = 'liking_users')  # 좋아하는 영화에 나온 배우들 등록
    counted_genres = models.ManyToManyField(Genre, through='GenreCounts', related_name='recorded_user')
    counted_actors = models.ManyToManyField(Actor, through='ActorCounts', related_name='recorded_user')
    
    # article_likes = models.ManyToManyField
    # comment_likes
    # 


class GenreCounts(models.Model):
    recorded_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    counted_genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    genre_cnt = models.IntegerField(default=0)


class ActorCounts(models.Model):
    recorded_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    counted_actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    actor_cnt = models.IntegerField(default=0)

