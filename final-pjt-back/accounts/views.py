from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from .serializers import UserSerializer, UserProfileSerializer, UserSearchSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .models import GenreCounts, ActorCounts
from movies.models import Movie, Genre




User = get_user_model()

# 해당 함수는 최초 가입시와 영화에 대한 좋아요 버튼을 누를 떄 모두 사용됨
@api_view(['POST',])
def likes_movie(request):
    # 좋아요 누른 영화 목록과 username을 받아온다
    movie_ids = request.data.get('likeMovieIds')
    username = request.data.get('username')
    
    # username으로 해당 유저를 조회함 
    user = User.objects.get(username=username)
    

    # 받은 영화 목록을 유저의 좋아요 영화 목록에 추가함 
    for movie_id in movie_ids:
        movie = get_object_or_404(Movie, movie_id=movie_id)
        genres = list(movie.genres.all())  # 장르 객체들의 리스트
        actors = list(movie.actors.all())  # 배우 객체들의 리스트
        
        if not user.movie_likes.filter(movie_id=movie_id).exists():
            user.movie_likes.add(movie)

            # results = GenreCounts.objects.filter(genre=genre, user=user)
            for genre in genres:
                genre_cnt = list(GenreCounts.objects.filter(counted_genre=genre, recorded_user=user))
                if genre_cnt:
                    genre_cnt[0].genre_cnt += 1
                    genre_cnt[0].save()
                else:
                    genre_cnt = GenreCounts(counted_genre=genre, recorded_user=user)
                    genre_cnt.genre_cnt = 1
                    genre_cnt.save()
            for actor in actors:
                actor_cnt = list(ActorCounts.objects.filter(counted_actor=actor, recorded_user=user))
                if actor_cnt:
                    actor_cnt[0].actor_cnt += 1
                    actor_cnt[0].save()
                else:
                    actor_cnt = ActorCounts(counted_actor=actor, recorded_user=user)
                    actor_cnt.actor_cnt = 1
                    actor_cnt.save()

        else: # 만일 해당 영화가 좋아하는 영화에 이미 있었다면 좋아요 취소 
            user.movie_likes.remove(movie)

            for genre in genres:
                genre_cnt = list(GenreCounts.objects.filter(counted_genre=genre, recorded_user=user))
                if genre_cnt:
                    genre_cnt[0].genre_cnt -= 1
                    genre_cnt[0].save()
            for actor in actors:
                actor_cnt = list(ActorCounts.objects.filter(counted_actor=actor, recorded_user=user))
                if actor_cnt:
                    actor_cnt[0].actor_cnt -= 1
                    actor_cnt[0].save()
    
    beloved_genre = GenreCounts.objects.filter(recorded_user=user).order_by('-genre_cnt')[:1][0].counted_genre
    
    # 받은 영화의 장르를 장르 카운트에 반영해줌
    results = {
        'beloved_genre_sort': beloved_genre.genre_sort_id,
        'beloved_genre_id': beloved_genre.genre_id,
        'beloved_genre_name': beloved_genre.genre_name
    }
    
    return Response(results)  



'''
이후 가장 좋아하는 장르를 추출해서 API로 정보를 쏴주어야 함.
어떻게 좋아하는 장르를 빠른 시간 내에 추출할 수 있을까?
1) 해당 User가 좋아하는 영화들 목록을 추출 (-> 이건 빠름)
2) 추출된 영화 목록을 순회 (-> 이건 n배 늘어남)
3) 해당 영화가 속한 장르들 누적해서 세어 줌  (-> 이걸 따로 칼럼에 적어주는 게 나을까?)
   어차피 영화를 좋아할 때만 좋아하는 장르가 달라지니 기록해주는 게 나을 듯.  

--> 결론: genre_counts와 actor_counts를 기록해준다
'''


# User 데이터를 보내면서 좋아하는 영화의 모든 정보까지 다 보낸다 
@api_view(['GET'])
def profile(request, username):  # 해당 request에 username이 함께 옴
    profile_user = get_object_or_404(User, username=username)
    movies = profile_user.movie_likes.all()
    ids = []
    for movie in movies:
        ids.append(movie.movie_id)


    favorite_actors = list(profile_user.counted_actors.all())
    favorite_actors.sort(key=lambda x: ActorCounts.objects.get(recorded_user=profile_user, counted_actor=x).actor_cnt, reverse=True)
    favorite_actors = favorite_actors[:5]
    
    liked_actors = []

    for favorite_actor in favorite_actors:
        temp_obj = {}
        temp_obj['actor_id'] = favorite_actor.actor_id
        temp_obj['actor_name'] = favorite_actor.name
        temp_obj['profile_path'] = favorite_actor.profile_path
        liked_actors.append(temp_obj)

    followers = list(profile_user.followers.all())
    
    user_followers = []

    for follower in followers:
        user_followers.append(follower.pk)


    profile_infos = {
       'liked_movie_ids' : ids,
       'favorite_actors' : liked_actors,
       'followers' : user_followers
    }   
    
    serializer = UserProfileSerializer(profile_user)
    profile_infos.update(serializer.data)
    
    return Response(profile_infos)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def user_follow(request, username):
    profile_user = get_object_or_404(User, username=username)
    
    # 자기 스스로는 follow할 수 없게 설정
    follower = get_object_or_404(User, username=request.user)

    if follower == profile_user:
        return Response({'fail': '스스로를 팔로우할 수 없습니다'}, status=status.HTTP_403_FORBIDDEN)
    
    else:
        if follower.followings.filter(pk=profile_user.pk).exists():
            follower.followings.remove(profile_user)
            return Response({'message': '언팔로우 하였습니다'}, status=status.HTTP_200_OK)
        else:
            follower.followings.add(profile_user)
            return Response({'message': '팔로우 하였습니다'}, status=status.HTTP_200_OK)



@api_view(['GET', ])
def user_search(request):
    words = request.GET.get('search')
    targets = User.objects.filter(username__contains=words)
    
    serializer = UserSearchSerializer(targets, many=True)

    return Response(serializer.data)