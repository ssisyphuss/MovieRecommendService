from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    # 영화 좋아요/좋아요 해제
    path('likes_movie/', views.likes_movie),

    # 프로필 페이지
    path('profile/<str:username>/', views.profile),
    
    # 유저 팔로우/언팔로우
    path('profile/<str:username>/follow', views.user_follow),

    # 유저 검색
    path('search/', views.user_search),
]