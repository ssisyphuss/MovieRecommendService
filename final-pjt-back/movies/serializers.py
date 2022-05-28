from rest_framework import serializers
from .models import Genre, Movie, MovieImage, Actor
from communities.models import Comment, Review
from django.contrib.auth import get_user_model


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('genre_id', 'genre_name',)


class SignupMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('movie_id', 'title', 'poster_path', 'genres',)


# 검색창 API 요청에 대한 응답으로 주어질 serializer
class MovieSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('movie_id', 'title', 'poster_path', 'vote_average', 'genres',)


# 배우 정보 시리얼라이즈 
class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = '__all__'


# 영화 이미지(배경)까지 합친 시리얼라이저 (메인화면용도) 
class MovieSerializerWithImages(serializers.ModelSerializer):
    
    class GenreNestedSerializer(serializers.ModelSerializer):

        class Meta:
            model = Genre
            fields = ('genre_id', 'genre_name',)
    

    class MovieImageSerializer(serializers.ModelSerializer):
        class Meta:
            model = MovieImage
            fields = ('image_URL',)

    genres = GenreNestedSerializer(many=True, read_only=True)
    movieimage_set = MovieImageSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'


# 영화 디테일 페이지 시리얼라이즈
class MovieDetailSerializer(serializers.ModelSerializer):
    class GenreNestedSerializer(serializers.ModelSerializer):

        class Meta:
            model = Genre
            fields = ('genre_id', 'genre_name',)
    

    class MovieImageSerializer(serializers.ModelSerializer):
        class Meta:
            model = MovieImage
            fields = ('image_URL',)


    class ReviewSerializer(serializers.ModelSerializer):
        class ReviewUserSerializer(serializers.ModelSerializer):
            class Meta:
                model = get_user_model()
                fields = ('pk', 'username', )

        user = ReviewUserSerializer(read_only=True)
        user_good_eval = ReviewUserSerializer(many=True, read_only=True)
        good_eval_count = serializers.IntegerField(source='user_good_eval.count', read_only=True)
        user_bad_eval = ReviewUserSerializer(many=True, read_only=True)
        bad_eval_count = serializers.IntegerField(source='user_bad_eval.count', read_only=True)

        class Meta:
            model = Review
            fields = ('id', 'user', 'title', 'content', 'rating', 'created_at', 'user_good_eval', 'good_eval_count', 'user_bad_eval', 'bad_eval_count', )
    
    review_set = ReviewSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreNestedSerializer(many=True, read_only=True)
    movieimage_set = MovieImageSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'    


    
class MovieTestSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    
    class Meta:
        model = Movie
        fields = ('title', 'genres',)



class MovieRecommendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('movie_id', 'title', 'poster_path', )