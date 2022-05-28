from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Review, Comment, Cocomment
from movies.models import Movie



class ReviewSerializer(serializers.ModelSerializer):
    class ReviewUserSerializer(serializers.ModelSerializer):
            class Meta:
                model = get_user_model()
                fields = ('pk', 'username', )

    class MovieinReviewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('movie_id', 'title', 'poster_path')

    user = ReviewUserSerializer(read_only=True)
    user_good_eval = ReviewUserSerializer(many=True, read_only=True)
    good_eval_count = serializers.IntegerField(source='user_good_eval.count', read_only=True)
    user_bad_eval = ReviewUserSerializer(many=True, read_only=True)
    bad_eval_count = serializers.IntegerField(source='user_bad_eval.count', read_only=True)
    movie = MovieinReviewSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        

class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('title', 'content', 'rating', )



class UserCommnetSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username')
    

class CommentSerializer(serializers.ModelSerializer):
    
    class CommentCocommentSerializer(serializers.ModelSerializer):
        username = serializers.ReadOnlyField(source='user.username')

        class Meta:
            model = Cocomment
            fields = ('user', 'username', 'content', 'created_at')

    user = UserCommnetSerializer(read_only=True)
    replies = CommentCocommentSerializer(many=True, read_only=True)


    class Meta:
        model = Comment
        fields = '__all__'



class CocommentSerializer(serializers.ModelSerializer):
    
    user = UserCommnetSerializer(read_only=True)


    class Meta:
        model = Cocomment
        fields = '__all__'



class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content',)


class CocommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cocomment
        fields = ('content',)


