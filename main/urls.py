from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('post/<int:post_id>/',views.post_detail,name='post_detail'),
    path('like/<str:like_post>/',views.like_detail,name="like_detail"),
    path('delete/<str:post_id>/',views.delete_post,name="delete"),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register',views.register_user,name='register'),
    path('<str:username>/',views.profile_user,name="profile"),
    path('upload',views.upload,name='upload'),
    path('search',views.search,name='search'),
    path('follow/<str:username>/',views.follow_user,name="follow"),
    path('unfollow/<str:username>/',views.unfollow_user,name="unfollow"),
    path('update_upload/<str:post_id>/',views.update_upload,name='update_upload'),
    path('edit/<str:username>',views.editprofile,name='editprofile')
]