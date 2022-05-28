from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from pprint import pprint
from .models import Genre, Movie, Actor, MovieImage, Director, Provider
from accounts.models import User, GenreCounts
from .serializers import (SignupMovieSerializer,
                        MovieSerializerWithImages,
                        MovieSearchSerializer,
                        MovieDetailSerializer,
                        MovieTestSerializer,
                        MovieRecommendSerializer,
                        )
from django.db.models import Q

from movies import serializers
import requests, random
import pickle

# 자연어 처리 알고리즘으로 추출받은 추천데이터 임포트
with open('movies/recommendations.p', 'rb') as file:
    recomm = pickle.load(file)

genre_sorts =   [[12, 14, 16, 18, 27, 28, 35, 36, 37, 53, 80, 99, 878, 9648, 10402, 10749, 10751, 10752, 10770],
                [80, 53, 9648, 27], 
                [14, 878],
                [16],
                [28, 12, 37, 10752],
                [18, 10751, 10749, 10402, 10770],
                [99, 36],
                [35]]


# 로그인을 하면서 동시에 좋아하는 영활를 고를 수 있도록 영화 360개를 송출합니다.
@api_view(['GET',])
def signup_movies(request):
    movies = get_list_or_404(Movie)
    # 평점이 매겨진 개수가 많은 순서대로 정렬을 하고 상위 360개만을 남깁니다.
    movies.sort(key=lambda x: x.vote_count, reverse=True)
    movies = movies[:360]
    random.shuffle(movies)  # 영화를 섞어줌 
    
    serializer = SignupMovieSerializer(movies, many=True)
    
    return Response(serializer.data)


# 장르페이지 이전 메인 화면에 최애 장르의 랜덤 영화 추천
# 로그인한 사용자라면 가장 좋아하는 장르의 id, 이름과 해당 장르 영화 3개 랜덤으로 추천받음
# 만일 로그인하지 않았다면, 적당히 유명하고 평점이 괜찮은 영화 세 개를 랜덤으로 추천받음
@api_view(['GET',])  
def main_page_recommend(request):
    if request.user.is_authenticated:  
        now_user = User.objects.get(username=request.user)
        genre_set = list(GenreCounts.objects.filter(recorded_user=now_user))
        favorite_genre = genre_set[0]
        max_likes = 0
        for genre in genre_set:
            if genre.genre_cnt > max_likes:
                max_likes = genre.genre_cnt
                favorite_genre = genre.counted_genre
        
        # 최애 장르의 영화들 추출
        favor_movies = list(favorite_genre.movies.all())
        favor_movies.sort(key=lambda x: (x.vote_count, x.vote_average), reverse=True)
        random.shuffle(favor_movies)
        favor_movies = favor_movies[:3]
        serializer = MovieSerializerWithImages(favor_movies, many=True)
    
        results = {
        'favorite_genre_id': favorite_genre.pk,
        'favorite_genre_name' : favorite_genre.genre_name,
        'recommended_movies' : serializer.data,
        }
    
    else:
        movies = list(Movie.objects.filter(vote_count__gte=3000, vote_average__gte=7.5))
        movies = random.sample(movies, 3)
        random_movie = MovieSerializerWithImages([movie for movie in movies], many=True)
    
        results = {
            'recommended_movies': random_movie.data,
        }
    return Response(results)



# 이후 Review와 합쳐주기 
@api_view(['GET', ])
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    temp_results = []

    for temp_id in recomm[movie_id]:
        temp_results.append(Movie.objects.get(movie_id=temp_id))
    temp_results = temp_results[1:4]
    temp_serializer = MovieRecommendSerializer(temp_results, many=True)
    serializer = MovieDetailSerializer(movie)

    results = {
        'similar_movies': temp_serializer.data
        }

    results.update(serializer.data)

    
    return Response(results)

'''
1. 내가 받은 영화 중 현재 OTT에서 상영하는 영화 (-> 메인페이지)
2. 평점 순으로 Top 10
3. 내가 팔로우한 친구들이 좋아하는 영화들 추천
4. 줄거리와 장르유사도를 고려해서 선정한 좋아요영화와 유사 영화들 
5. 기획전(e.g. 애니메이션은 미야자키 하야오 등)



'''

# 장르에서 가장 평점이 높은 영화 3개
@api_view(['GET',])  
def genre_main_page(request, genre_sort):
    genre_ids = genre_sorts[genre_sort]  # 요청받은 구분에 속하는 장르들
    movies = []

    for genre_id in genre_ids:
        genre = Genre.objects.get(genre_id=genre_id)
        movies.extend(list(genre.movies.filter(vote_average__gte=8.0, vote_count__gte=3000)))
    
    movies = list(set(movies))
    movies = movies[:3]
    
    serializer = MovieDetailSerializer(movies, many=True)

    return Response(serializer.data)
        
    # 영화 추천시 만일 이미 본 영화에 속한다면 
    # 만일 해당 장르에 속하는 좋아요 영화가 n개 이하일 경우 평점이 좋은 영화를 추천



# 이하는 genre_recommend에서 사용할 함수들 모음
# 장르별 평점 순위 10 영화 추천 
def genre_top_ten(request, genre_sort):
    genre_ids = genre_sorts[genre_sort]  # 요청받은 구분에 속하는 장르들
    movies = []
    
    for genre_id in genre_ids:
        genre = Genre.objects.get(genre_id=genre_id)
        movies.extend(list(genre.movies.filter(vote_average__gte=7.5, vote_count__gte=2000)))
    
    movies = list(set(movies))  # 중복 제거
    movies = movies[3:13]
    movies.sort(key=lambda x: x.vote_average, reverse=True)

    # serializer = MovieDetailSerializer(movies, many=True)

    # return Response(serializer.data)
    return movies


# 팔로잉하는 유저가 좋아하는 영화
def following_top_ten(request, genre_sort):
    now_user = User.objects.get(username=request.user)
    followings = list(now_user.followings.all())
    
    genre_set = set()
    for genre_id in list(genre_sorts[genre_sort]):
        genre_set.add(Genre.objects.get(genre_id=genre_id))

    followings_movies = []

    for following in followings:
        temp_movies = list(following.movie_likes.all())
        for movie in temp_movies:
            if set(list(movie.genres.all())) & genre_set:
                followings_movies.append(movie)
    
    if len(followings_movies) >= 10:
        random.shuffle(followings_movies)
        followings_movies = followings_movies[:10]
    
    else:
        movies = []
        for genre_id in genre_sorts[genre_sort]:
            genre = Genre.objects.get(genre_id=genre_id)
            movies.extend(list(genre.movies.filter(vote_average__gte=7.0)))
        
        movies = list(set(movies))  # 중복 제거
        movies = movies[13:23]
        i = 0
        while len(followings_movies) < 10:
            followings_movies.append(movies[i])
            i += 1

    return followings_movies


def user_info_movies(request, genre_sort):
    genre_set = set()
    for genre_id in list(genre_sorts[genre_sort]):
        genre_set.add(Genre.objects.get(genre_id=genre_id))

    genre_ids = genre_sorts[genre_sort]  # 요청받은 구분에 속하는 장르들
    now_user = User.objects.get(username=request.user)
    user_movies = list(now_user.movie_likes.all())
    random.shuffle(user_movies)
    
    r_movies = []
    for movie in user_movies:
        r_movies.extend(recomm[movie.movie_id][:3])
    
    random.shuffle(r_movies)

    results = []
    for r_movie_id in r_movies:
        r_movie = Movie.objects.get(movie_id=r_movie_id)
        if set(r_movie.genres.all()) & genre_set:
            results.append(r_movie)
        
        if len(results) >= 10:
            break

    if len(results) <= 10:
        less_movies = []
        for genre_id in genre_sorts[genre_sort]:
            genre = Genre.objects.get(genre_id=genre_id)
            less_movies.extend(list(genre.movies.filter(vote_average__gte=7.0)))
        
        less_movies = list(set(less_movies))  # 중복 제거
        random.shuffle(less_movies)
        less_movies = less_movies[13:23]
        i = 0
        while len(results) < 10:
            if less_movies[i] not in results:
                results.append(less_movies[i])
            i += 1
    
    return results


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def genre_recommend(request, genre_sort):
    
    top_ten_movies = MovieRecommendSerializer(genre_top_ten(request, genre_sort), many=True)
    followings_movies = MovieRecommendSerializer(following_top_ten(request, genre_sort), many=True)
    info_movies = MovieRecommendSerializer(user_info_movies(request, genre_sort), many=True)

    # 좋아하는 감독, 배우 순회해서 영화 추천 (이 장르는 아니지만...)
    # 장르별 특화 캐루셀 

    results = {
        '이 장르의 Top 10' : top_ten_movies.data,
        '팔로잉하는 사람이 좋아하는 영화' : followings_movies.data,
        '어쩌면, 좋아하실 거예요' : info_movies.data,
    }

    if genre_sort == 1:
        director = Director.objects.get(director_id=2636)
        director_movies = list(director.filmographies.all())
        director_movies.sort(key=lambda x: x.vote_average, reverse=True)
        director_movies = MovieRecommendSerializer(director_movies, many=True)

        results['스릴러 좋아하면 히치콕은 알아야지'] = director_movies.data        

    elif genre_sort == 2:
        temp_movies = recomm[438631]  # 듄 설정
        recom = []
        for movie_id in temp_movies:
            recom.append(Movie.objects.get(movie_id=movie_id))
        
        recom.sort(key=lambda x: (x.vote_average, x.vote_count))
        
        recom_movies = MovieRecommendSerializer(recom, many=True)

        results['듄을 좋아하신다면!?'] = recom_movies.data        

    elif genre_sort == 3:
        director = Director.objects.get(director_id=608)
        director_movies = list(director.filmographies.all())
        director_movies.sort(key=lambda x: x.vote_average, reverse=True)
        director_movies = MovieRecommendSerializer(director_movies, many=True)

        results['한 여름 수채화 같은, 지브리 스튜디오'] = director_movies.data

    elif genre_sort == 4:
        director = Director.objects.get(director_id=608)
        director_movies = list(director.filmographies.all())
        director_movies.sort(key=lambda x: x.vote_average, reverse=True)
        director_movies = MovieRecommendSerializer(director_movies, many=True)

        results['한 여름 수채화 같은, 미야자키 하야오'] = director_movies.data


    elif genre_sort == 5:
        director = Director.objects.get(director_id=564)
        director_movies = list(director.filmographies.all())
        director_movies.sort(key=lambda x: x.vote_average, reverse=True)
        director_movies = director_movies[:5]
        director_movies = MovieRecommendSerializer(director_movies, many=True)

        results['실제 시간이 흐르는 영화가 보고 싶다면'] = director_movies.data        


    elif genre_sort == 6:
        temp_movies = recomm[954]  # 미션임파서블 설정
        recom = []
        for movie_id in temp_movies:
            recom.append(Movie.objects.get(movie_id=movie_id))
        
        recom.sort(key=lambda x: (x.vote_average, x.vote_count))
        
        recom_movies = MovieRecommendSerializer(recom, many=True)

        results['Mission Impossible'] = recom_movies.data               

    elif genre_sort == 7:
        genre_ids = genre_sorts[genre_sort]  # 요청받은 구분에 속하는 장르들
        movies = []
        
        for genre_id in genre_ids:
            genre = Genre.objects.get(genre_id=genre_id)
            movies.extend(list(genre.movies.filter(vote_average__gte=7.0)))
        
        movies = list(set(movies))  # 중복 제거
        N = len(movies)
        for i in range(N-1, -1, -1):
            if len(movies[i].genres.all()) > 1:
                movies.pop(i)

        movies.sort(key=lambda x: x.runtime)
        movies = movies[:10]
        random.shuffle(movies)
        
        movies = MovieRecommendSerializer(movies, many=True)
        
        results['후딱 보기 좋은 짧은 코미디 영화들!'] = movies.data
    
    return Response(results)



@api_view(['GET', ])
def search(request):
    words = request.GET.get('search')
    movies = Movie.objects.filter(Q(title__contains=words) | Q(original_title__contains=words))
    
    serializer = MovieSearchSerializer(movies, many=True)

    return Response(serializer.data)




# #  이하는 Data 받아오는 함수
# URL = 'https://api.themoviedb.org/3'
# API_KEY = 'ca33ee1ba3a143bb89f377cdff3e719c'

# def genre_register(request):
#     path = '/genre/movie/list'
#     params = {
#         'api_key' : API_KEY,
#         'language' : 'ko-KR' 
#     }

#     genres = requests.get(URL+path, params=params).json().get('genres')
#     results = []
#     # all_genres_id = list(Genre.objects.values_list('genre_id', flat = True))
#     all_genres = list(Genre.objects.all())
#     for genre in genres:
#         instance = Genre()
#         instance.genre_id = genre['id']
#         instance.genre_name = genre['name']
#         if instance not in all_genres:
#             instance.save()
#         else:
#             results.append('중복입니다')
#     context = {
#         'results' : results,
#     }
    
#     return render(request, 'movies/register.html', context)
        

# def movie_register(request):
#     path = '/discover/movie'
#     params = {
#         'api_key' : API_KEY,
#         'language' : 'ko-KR',
#         'sort_by' : 'vote_average.desc',
#         'include_adult': True,
#         'include_video': True,
#         'vote_count.gte': 1000,
#         'vote_average.gte': 7.0,
#         'with_genres': 18,
#         'with_watch_monetization_types': 'flatrate',
#         'page': 1,
#     }
#     results = []
#     all_genres_id = list(Genre.objects.values_list('genre_id', flat = True))

#     for genre in all_genres_id:
#         temp = 0
#         all_movies = list(Movie.objects.all())
#         params['with_genres'] = genre
#         for i in range(1, 40):  # 모수복구
#             params['page'] = i
#             movies = requests.get(URL+path, params=params).json().get('results')
            
#             for movie in movies:
#                 instance = Movie(
#                     movie_id=movie['id'],
#                     title=movie['title'],
#                     overview=movie['overview'],
#                     release_date=movie['release_date'],
#                     poster_path=movie['poster_path'],
#                     original_title=movie['original_title'],
#                     original_language=movie['original_language'],
#                     vote_count=movie['vote_count'],
#                     vote_average=movie['vote_average'],
#                 )
#                 if instance not in all_movies:
#                     instance.save()

#                     for genre_id in movie['genre_ids']:
#                         genre_instance = Genre.objects.get(genre_id=genre_id)
#                         instance.genres.add(genre_instance)
#                     instance.save()
#                     temp += 1

#             genre_name = list(Genre.objects.filter(genre_id=genre).values_list('genre_name', flat = True))[0]
#             results.append(f'{genre_name} : {temp}')                 

#     context = {
#         'results' : results,
#     }
    
#     return render(request, 'movies/register.html', context)


# def movie_detail_register(request):
#     all_movie_ids = list(Movie.objects.all().values_list('movie_id', flat=True))
#     temp = 0
#     provider_sort = ['flatrate', 'buy', 'rent','nothing']
#     params = {
#         'api_key': API_KEY,
#         'language': 'en-US'
#     }

#     for movie_id in all_movie_ids:
#         path = f'/movie/{movie_id}'
#         res_1 = requests.get(URL+path, params=params).json()
#         movie = Movie.objects.get(movie_id=movie_id)
#         movie.imdb_id = res_1.get('imdb_id')
#         movie.en_overview = res_1.get('overview')
#         movie.runtime = res_1.get('runtime')
#         path = f'/movie/{movie_id}/watch/providers'
#         res_2 = requests.get(URL+path, params=params).json().get('results')
#         KR_data = res_2.get('KR')
        
#         if KR_data:
#             for sort in provider_sort:
#                 providers = KR_data.get(sort)
#                 if providers:
#                     for provider in providers:
#                         provider_id = provider['provider_id']
#                         provider_name = provider['provider_name']
#                         provider_instance = Provider(
#                             provider_id = provider_id,
#                             provider_name = provider_name            
#                         )
#                         if not Provider.objects.filter(provider_id=provider_id).exists():
#                             provider_instance.save()
#                         else:
#                             provider_instance = Provider.objects.get(provider_id=provider_id)
#                     provider_instance.owned_movies.add(movie)
#                     provider_instance.save()
#                     temp += 1
                
#         movie.save()
        
    
#     context = {
#         'results' : KR_data,
#         'temp': temp,
#     }

#     return render(request, 'movies/register.html', context)


# def movie_images_register(request):
#     all_movie_ids = list(Movie.objects.all().values_list('movie_id', flat=True))
#     temp = 0
#     params = {
#     'api_key': API_KEY,
#     }
    
#     for movie_id in all_movie_ids:
#         path = f'/movie/{movie_id}/images'
#         movie = Movie.objects.get(movie_id=movie_id)
#         images = requests.get(URL+path, params=params).json()['backdrops'][:3]
#         for image in images:
#             image_instance = MovieImage()
#             image_instance.movie = movie
#             image_instance.image_URL = 'https://www.themoviedb.org/t/p/original' + image['file_path']
#             image_instance.save()
#             temp += 1

#     context = {
#         'results': temp
#     }

#     return render(request, 'movies/register.html', context)



# # 영화 배우와 감독 모두 저장하기 
# def actor_register(request):
   
#     results = []
#     temp = 0

#     all_movie_ids = list(Movie.objects.all().values_list('movie_id', flat=True))
#     params = {
#         'api_key': API_KEY,
#         'language': 'ko-KR'
#     }
    
#     for movie_id in all_movie_ids:
#         movie = Movie.objects.get(movie_id=movie_id)
#         path = f'/movie/{movie_id}/credits'
#         movie_credits = requests.get(URL+path, params=params).json()
#         movie_casts = movie_credits.get('cast')
#         movie_casts.sort(key=lambda x: x['popularity'], reverse=True)
#         movie_casts = movie_casts[:5]  # 영화당 5명만 저장할 것

#         this_movie_cast = []
#         for cast in movie_casts:
#             results.append(cast['id'])  # 전체 목록과 비교
#             this_movie_cast.append(cast['id'])  # 해당 영화의 캐스트 목록 
                
#         for actor_id in this_movie_cast:
#             path = f'/person/{actor_id}'
#             actor = requests.get(URL+path, params=params).json()
#             actor_instance = Actor(
#                 actor_id=actor['id'],
#                 gender=actor['gender'],
#                 name=actor['name'],
#                 biography=actor['biography'],
#                 imdb_id=actor['imdb_id'],
#                 popularity = actor['popularity'],
#                 profile_path=actor['profile_path'],
#             )
#             if not Actor.objects.filter(actor_id=actor_id).exists():
#                 actor_instance.save()
#                 temp += 1
#             else:
#                 actor_instance = Actor.objects.get(actor_id=actor_id) 
#             actor_instance.filmographies.add(movie)
#             actor_instance.save()
    
#         movie_director_ids = []
#         movie_crews = movie_credits.get('crew')
#         for crew in movie_crews:
#             if crew['job'] == 'Director':
#                 movie_director_ids.append(crew['id'])
        
#         for director_id in movie_director_ids:
#             path = f'/person/{director_id}'
#             director = requests.get(URL+path, params=params).json()
#             director_instance = Director(
#                 director_id= director['id'],
#                 gender= director['gender'],
#                 name= director['name'],
#                 biography= director['biography'],
#                 imdb_id= director['imdb_id'],
#                 popularity = director['popularity'],
#                 profile_path= director['profile_path'],
#             )
#             if not Director.objects.filter(director_id=director_id).exists():
#                 director_instance.save()
#             else:
#                 director_instance = Director.objects.get(actor_id=actor_id)
#             director_instance.filmographies.add(movie)
#             director_instance.save()

        
        
#     context = {
#         'results' : results,
#         'temp' : temp,
#     }
    
#     return render(request, 'movies/register.html', context)



# POSTMAN 테스트용
# @api_view(['GET',])
# def test(request, movie_id):
#     result = []
#     for i in range(10):
#         movie = Movie.objects.get(movie_id=recomm[movie_id][i])
#         result.append(movie)

#     serializers = MovieTestSerializer(result, many=True)

#     return Response(serializers.data)