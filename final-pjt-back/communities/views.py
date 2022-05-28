from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Review, Comment, Cocomment
from movies.models import Movie, GenreSort
from.serializers import (CommentSerializer,
                          ReviewSerializer,
                          ReviewCreateSerializer,
                          CommentCreateSerializer,
                          CocommentCreateSerializer)


# 리뷰는 어떻게 띄울 것?

User = get_user_model()

@api_view(['GET'])
def review_list(request):
    reviews = Review.objects.all().order_by('-pk')
    serializer = ReviewSerializer(reviews, many=True)

    return Response(serializer.data)


@api_view(['GET', 'POST',])
def review_create(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    serializer = ReviewCreateSerializer(data=request.data)
    user = User.objects.get(username=request.user)
    if not Review.objects.filter(user=user, movie=movie).exists():
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    results = {
        'error': '리뷰 등록에 실패하였습니다',
    }

    return Response(results)
    
# 각 리뷰의 디테일 정보 요청
@api_view(['GET'])
def review_detail(request, movie_id, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    serializer = ReviewSerializer(review)
    
    return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_update(request, movie_id, review_pk):
    this_user = User.objects.get(username=request.user)
    review = get_object_or_404(Review, pk=review_pk)
    
    if not this_user.review_set.filter(pk=review_pk).exists():
        return Response({'fail': '작성자가 아닙니다'})
    
    else:
        if request.method == 'PUT':
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

        elif request.method == 'DELETE':
            review.delete()
            return Response({'complete': '삭제가 완료되었습니다'}, status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET', ])
def genre_review_list(request, genre_sort_id):
    genre_sort = GenreSort.objects.get(pk=genre_sort_id)  # 해당 분류에 속하는 장르소트객체 불러옴 
    genres = list(genre_sort.genres.all())
    
    reviews = list()
    for genre in genres:
        temp_movies = list(genre.movies.all())
        for temp_movie in temp_movies:
            temp_reviews = list(temp_movie.review_set.all())
            reviews.extend(temp_reviews)
    reviews = list(set(reviews))  # 중복 리뷰 제거
    reviews.sort(key=lambda x:x.created_at, reverse=True)

    serializer = ReviewSerializer(reviews, many=True)

    return Response(serializer.data)



@api_view(['POST'])
def comment_create(request, review_pk):
    if not request.user.is_authenticated:
        return Response({'fail': '인증되지 않은 사용자입니다'})

    review = get_object_or_404(Review, pk=review_pk)
    serializer = CommentCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, review=review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def cocomment_create(request, review_pk, comment_pk):
    if not request.user.is_authenticated:
        return Response({'fail': '인증되지 않은 사용자입니다'})

    now_user = User.objects.get(username=request.user)
    parent = get_object_or_404(Comment, pk=comment_pk)

    serializer = CocommentCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=now_user, parent=parent)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, review_pk, comment_id):
    now_user = User.objects.get(username=request.user)
    comment = get_object_or_404(Comment, pk=comment_id)
    # comment = Comment.objects.get(pk=comment_id)

    if not now_user.comment_set.filter(pk=comment_id).exists():
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({ 'complete': '댓글이 삭제되었습니다' }, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cocomment_delete(request, review_pk, cocomment_id):
    now_user = User.objects.get(username=request.user)
    cocomment = get_object_or_404(Cocomment, pk=cocomment_id)
    # comment = Comment.objects.get(pk=comment_id)

    if not now_user.cocomment_set.filter(pk=cocomment_id).exists():
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    cocomment.delete()
    return Response({ 'complete': '댓글이 삭제되었습니다' }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', ])
def comment_list(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = list(Comment.objects.filter(review=review))

    serializer = CommentSerializer(comments, many=True)

    return Response(serializer.data)


# 리뷰에 대한 good 평가를 추가함
@api_view(['POST'])
def review_good(request, movie_id, review_pk):
    user = get_object_or_404(User, username=request.user)
    review = get_object_or_404(Review, pk=review_pk)
    if not review.user_good_eval.filter(pk=review_pk).exists():
        review.user_good_eval.add(user)
    else:
        review.user_good_eval.remove(user)
    
    # 이미 싫어요 한 유저는 좋아요도 누르지 못하게 해야 함
    if user.good_reviews.filter(pk=review_pk).exists():
        return Response({'error': '이미 좋아요를 누르셨습니다'})
    
    return Response({ f'{review.user.username}의 리뷰에 좋아요를 누르셨습니다': 'success'}, status=status.HTTP_201_CREATED)


@api_view(['POST',])
def review_bad(request, movie_id, review_pk):
    user = get_object_or_404(User, username=request.user)
    review = get_object_or_404(Review, pk=review_pk)
    if not review.user_bad_eval.filter(pk=review_pk).exists():
        review.user_bad_eval.add(user)
    else:
        review.user_bad_eval.remove(user)
    
    # 이미 싫어요 한 유저는 좋아요도 누르지 못하게 해야 함
    if user.bad_reviews.filter(pk=review_pk).exists():
        return Response({'error': '이미 싫어요를 누르셨습니다'})
    
    return Response({ f'{review.user.username}의 리뷰에 싫어요를 누르셨습니다': 'success'}, status=status.HTTP_201_CREATED)

