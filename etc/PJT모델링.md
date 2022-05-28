**PJT 모델링 개체/관계 결정**

- User

  - username
  - email
  - password
- 좋아요 한 영화
  - 리스트에 추가한 영화
- 좋아요한 아티클
  - 좋아요한 댓글
- 팔로우한 유저
  - 주 장르 (1:N) (-> 주 장르 셋은 하나만 결정함)




- Article
  - 



- Comment



- Movie

  - poster_path
  - overview
  - release_date
  - genre_ids (array)
  - id
  - original_title
  - original_language
  - title
  - vote_count
  - vote_average
  - genres_id (속한 장르) **M:N**
  - imdb_id

  

  **1:N or M:N field**

  - genres (M:N)
  - 리스트에 추가한 유저 (M:N)
  - vote_average_metacritc(IMDB?)
  - overview
  - poster_path



- Actor  --> **Movie를 먼저 필터링하고, 데이터베이스에 저장된 영화의 출연진을 Actor에 추가하자**
  - gender  (1이 여자 2가 남자)
  - name
  - biography
  - imdb_id
  - profile_path
  - filmographies



- MovieImage

  - movie (ForeignKey)
  - image_URL

  

- Genres

  - genre_id

  - genres_name

  

  - included movies (M:N)
  - User_Follow (M:N)
  
  

 --> 액션:28 / 모험:12 / 애니메이션:16 / 코미디:35 / 범죄:80 / 다큐멘터리:99 / 드라마:18 / 가족:10751 / 판타지:14 / 역사:36 / 공포:27 / 음악:10402 / 미스터리:9648 / 로맨스:10749 / SF:878 / TV 영화:10770 / 스릴러:53 / 전쟁:10752 / 서부:37



**<장르 묶기>**

1. [범죄, 스릴러, 미스터리, 공포] 
2. [판타지, SF]
3. [애니메이션]
4. [액션, 모험, 서부, 전쟁]
5. [드라마, 가족, 로맨스, 음악, TV 영화]
6. [다큐멘터리, 역사]
7. [코미디]



- Article
  - title
  - content
  - created_at
  - updated_at
  - 작성자(ForeignKey)
  - liked_User (M:N)
  - 소속 장르 (ForeignKey)



- Comment

  - 작성자 (MTM)

  - article
  - content
  - created_at
  - updated_at



- rewards(?)



- Review
  - title
  - content
  - movie
  - user
  - like_users
  - dislike_users
  - updated_at



- Comment
  - content
  - review
  - user
  - like_users
  - dislike_users
  - created_at



- Cocoment
  - content
  - review
  - user
  - like_users
  - dislike_users
  - created_at

