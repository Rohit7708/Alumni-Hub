from .import views
from django.urls import path,include



urlpatterns = [
    path('', views.signIn,name="login"),
    path('postsignIn/', views.postsignIn),
    path('signUp/', views.signUp, name="signup"),
    path('logout/', views.logout, name="log"),
    path('postsignUp/', views.postsignUp),
    path('navbar/',views.navbar,name="navbar"),
]