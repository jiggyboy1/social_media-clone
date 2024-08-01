from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('post/<int:post_id>/',views.post_detail,name='post_detail'),
    path('like/<str:like_post>/',views.like_detail,name="like_detail"),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
]