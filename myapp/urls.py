from .import views
from django.urls import path,include



urlpatterns = [
    path('', views.signIn,name="login"),
    path('postsignIn/', views.postsignIn),
    path('signUp/', views.signUp, name="signup"),
    path('logout/', views.logout, name="log"),
    path('postsignUp/', views.postsignUp),
    path('navbar/',views.navbar,name="navbar"),
    path('welcome_msg/',views.welcome,name="welcome"),
    path('alumni_login/',views.alumni_login,name="alumni_login"),
    path('alumni_signup/',views.alumni_signup,name="alumni_signup"),
    path('alumni_postsignUp/',views.alumni_postsignup),
    path('alumni_postsignIn/',views.alumni_postsignin),
    path('alumni_mainpage/',views.alumni_mainpage),
    path('profile/',views.profile,name="profile"),
]