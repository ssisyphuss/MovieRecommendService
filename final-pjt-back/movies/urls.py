from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # 회원가입시 영화 선택지 제공
    path('signup_movies/', views.signup_movies),

    # 회원정보 토대로 메인 페이지에 영화 추천
    path('main_page_recommend/', views.main_page_recommend),

    # 영화 검색 API 제공
    path('search/', views.search),

    # 영화 세부 정보 제공
    path('detail/<int:movie_id>/', views.movie_detail),



    # 영화 추천하는 url 모음
    path('genre_main_page/<int:genre_sort>', views.genre_main_page),
    path('genre_recommend/<int:genre_sort>/', views.genre_recommend),
    

    # 이하는 TMDB서버에서 장고 서버로 데이터 받아오는 URL
    # path('genre/', views.genre_register),
    # path('movie/', views.movie_register),
    # path('actor/', views.actor_register),
    # path('movie_detail_register/', views.movie_imdb_register),
    # path('movie_images_register/', views.movie_images_register),
    
    # POSTMAN 테스트용 
    # path('test/<int:movie_id>/', views.test)
]