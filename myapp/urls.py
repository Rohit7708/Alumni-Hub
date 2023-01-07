from .import views
from django.urls import path,include



urlpatterns = [
    path('', views.signIn,name="login"),
    path('postsignIn/', views.postsignIn,name="postsignIn"),
    path('signUp/', views.signUp, name="signup"),
    path('logout/', views.logout, name="log"),
    path('postsignUp/', views.postsignUp),
    path('welcome_msg/<session_id>/',views.welcome,name="welcome"),
    path('alumni_login/',views.alumni_login,name="alumni_login"),
    path('alumni_signup/',views.alumni_signup,name="alumni_signup"),
    path('alumni_postsignUp/',views.alumni_postsignup),
    path('alumni_postsignIn/',views.alumni_postsignin),
    path('alumni_mainpage/<session_id>/',views.alumni_mainpage,name="alumni_mainpage"),
    path('profile/<session_id>/',views.profile,name="profile"),
    path('alumni_list/<session_id>/',views.alumnilist,name="alumni_list"),
    path('news/<session_id>/',views.news,name="news"),
    path('jobs/<session_id>/',views.jobs,name="jobs"),
    path('news_not/<session_id>/',views.alumni_news,name="news_not"),
    path('alumni_job/<session_id>/',views.alumni_job,name="news_job"),
    path('detail_card/<session_id>/<roll>/<firstname>/<lastname>/<batch>/<oemail>/<pemail>/<phone>/',views.profile_card,name="detail_card")
]
