from django.urls import path
from .views import add_comment , add_post, delete_post , get_all_posts , get_comments_on_post , like_on_post , get_someone_posts,get_number_of_comments_on_post,add_post_with_image,force_delete_post

urlpatterns = [
  path('addpost/<author_id>/',add_post,name="Add Post"),
  path('addpost_with_image/<author_id>/',add_post_with_image,name="Add Post With image"),
  path('addcomment/<str:post_id>/<str:user_id>/',add_comment,name="Add Comment"),
  path('like/<str:post_id>/<user_id>/',like_on_post,name="Like On Post"),
  path('getallposts/',get_all_posts,name="Get All Post"),
  path('getsomeoneposts/<str:user_id>/',get_someone_posts,name='Get Someone Post'),
  path('getcommentsonpost/<str:post_id>/',get_comments_on_post,name="Get Comments On Post"),
  path("deletepost/<str:post_id>/<str:user_id>/", delete_post , name="Delete post"),
  path("get_nuber_of_comments/<str:post_id>/",get_number_of_comments_on_post,name="Number of Comments"),
  path("force_delete_post/<str:post_id>/",force_delete_post,name="delete post by force")

]


