from django.db import models
from django.conf import settings
from movies.models import Movie
from django.core.validators import MinValueValidator, MaxValueValidator



class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    rating = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(10)])
    user_good_eval = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='good_reviews')
    user_bad_eval = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bad_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)


# 대댓글 구현
class Cocomment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
