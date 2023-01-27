from .import views
from django.urls import path,include



urlpatterns = [
    path('',views.home,name="home"),
    path('login/', views.signIn,name="login"),
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
    path('alumni_profileset/<session_id>/',views.alumni_profile,name="alumni_profileset"),
    path('alumni_updateprofile/<session_id>/',views.alumni_updateprofile,name="alumni_updateprofile"),
    path('profile/<session_id>/',views.profile,name="profile"),
    path('update_profile/<session_id>/',views.update_profile,name="update_profile"),
    path('alumni_list/<session_id>/',views.alumnilist,name="alumni_list"),
    path('students_list/<session_id>/',views.students_list,name="students_list"),
    path('alumni_detailcard/<session_id>/',views.alumni_detailcard,name="alumni_detailcard"),
    path('notification_history/<session_id>/',views.notification_history,name="notification_history"),
    path('alumni_notification/<session_id>/',views.alumni_notification,name="alumni_notification"),
    path('jobs/<session_id>/',views.jobs,name="jobs"),
    path('st_notification_detail/<session_id>/<title>/<startdate>/<enddate>/<description>/<attachment>/',views.notification_detail_student,name="st_notification_detail"),
    path('notification_detail/<description>/<title>/<att>/<startdate>/<enddate>/',views.notification_detail,name="notification_detail"),
    path('al_event_notify/<session_id>/',views.al_event_notify,name="al_event_notify"),
    path('alumni_job/<session_id>/',views.alumni_job,name="alumni_job"),
    path('detail_card/<session_id>/<roll>/<firstname>/<lastname>/<batch>/<oemail>/<pemail>/<phone>/',views.profile_card,name="detail_card"),
    path('st_event_notify/<session_id>/',views.create_notification,name="st_event_notify"),
    path('roll/<session_id>/',views.get_rollnumber,name="roll"),
    path('chat/<session_id>/<sender>/<receiver>/',views.chat,name="chat"),
    path('send',views.send,name="send"),
    path('getMessages/<receiver>/<sender>/',views.getMessages,name='getMessages'),
]
