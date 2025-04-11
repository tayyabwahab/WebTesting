from django.urls import path
from . import views

urlpatterns = [
    path('', views.FileUploading),
    path('signup', views.signup, name="signup"),
    path('home', views.Home, name="home"),
    path('how_to_use', views.how),
    path('feedback', views.feedback, name="feedback"),
    path('excercise', views.excercise),
    # path('live_feed/', views.live_feed, name='live_feed'),
]