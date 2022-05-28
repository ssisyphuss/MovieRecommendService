from django.urls import path
from . import views


app_name = 'communities'

urlpatterns = [

    # 리뷰 작성, 조회 및 좋아요/싫어요/수정
    path('<int:movie_id>/review_create/', views.review_create),
    path('<int:movie_id>/<int:review_pk>/', views.review_detail),
    path('<int:movie_id>/<int:review_pk>/good/', views.review_good),
    path('<int:movie_id>/<int:review_pk>/bad/', views.review_bad),
    path('<int:movie_id>/<int:review_pk>/update/', views.review_update),

    # 장르별 리뷰 모음 신청
    path('genre-reviews/<int:genre_sort_id>/', views.genre_review_list),

    # 커멘트 리뷰 작성 및 삭제
    path('review/<int:review_pk>/comment_create/', views.comment_create),

    # 대댓글 달기
    path('review/<int:review_pk>/comment_create/<int:comment_pk>/', views.cocomment_create),
    path('review/<int:review_pk>/comment_delete/<int:comment_id>/', views.comment_delete),
    path('review/<int:review_pk>/comment_delete/<int:cocomment_id>/', views.cocomment_delete),
    path('review/<int:review_pk>/comments/', views.comment_list),      # 커멘트 전체 조회


    

]