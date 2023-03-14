from .import views
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('',views.home,name="home"),
    path('login/', views.signIn,name="login"),
    path('postsignIn/', views.postsignIn,name="postsignIn"),
    path('signUp/', views.signUp, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('postsignUp/', views.postsignUp),
    path('welcome_msg/<session_id>/',views.welcome,name="welcome"),
    path('alumni_login/',views.alumni_login,name="alumni_login"),
    path('alumni_signup/',views.alumni_signup,name="alumni_signup"),
    path('alumni_postsignUp/',views.alumni_postsignup),
    path('alumni_postsignIn/',views.alumni_postsignin),
    path('alumni_mainpage/<session_id>/',views.alumni_mainpage,name="alumni_mainpage"),
    path('alumni_profileset/<session_id>/',views.alumni_profile,name="alumni_profileset"),
    path('alumni_updateprofile/<session_id>/',views.alumni_updateprofile,name="alumni_updateprofile"),
    # path('profile/<session_id>/',views.profile,name="profile"),
    path('update_profile/<session_id>/',views.update_profile,name="update_profile"),
    path('alumni_list/<session_id>/',views.alumnilist,name="alumni_list"),
    path('students_list/<session_id>/',views.students_list,name="students_list"),
    path('alumni_detailcard/<session_id>/',views.alumni_detailcard,name="alumni_detailcard"),
    path('notification_history/<session_id>/',views.notification_history,name="notification_history"),
    path('alumni_notification/<session_id>/',views.alumni_notification,name="alumni_notification"),
    path('job_post/<session_id>/',views.job_post,name="job_post"),
    path('jobs/<session_id>/',views.jobs,name="jobs"),
    path('job_details/<session_id>/<profile>/<rounds>/<description>/<interview_date>/<attachment>/',views.job_details,name="job_details"),
    path('st_notification_detail/<session_id>/<not_id>/<title>/<startdate>/<enddate>/<description>/',views.notification_detail_student,name="st_notification_detail"),
    # path('notification_detail/<description>/<title>/<att>/<startdate>/<enddate>/',views.notification_detail,name="notification_detail"),
    path('al_event_notify/<session_id>/',views.al_event_notify,name="al_event_notify"),
    path('alumni_job/<session_id>/',views.alumni_job,name="alumni_job"),
    path('detail_card/<session_id>/<roll>/<firstname>/<lastname>/<batch>/<oemail>/<pemail>/<phone>/',views.profile_card,name="detail_card"),
    path('roll/<session_id>/',views.get_rollnumber,name="roll"),
    path('chat/<session_id>/<sender>/<receiver>/',views.chat,name="chat"),
    path('send',views.send,name="send"),
    path('room/<session_id>/<sender>/<receiver>/',views.room,name="room"),
    path('getMessages/<receiver>/<sender>/',views.getMessages,name='getMessages'),
    path('interview_exp/<session_id>/',views.interview_experience,name="interview_exp"),
    path('company_submit/<session_id>/',views.company_submit,name="company_submit"),
    path('a_interview_exp/<session_id>/',views.a_interview_experience,name="a_interview_exp"),
    path('a_company_submit/<session_id>/',views.a_company_submit,name="a_company_submit"),
    
    #faculty
    path('faculty_signin/',views.faculty_signIn,name="faculty_signIn"),
    path('faculty_signUp/',views.faculty_signUp,name="faculty_signUp"),
    path('faculty_login/',views.faculty_login,name="faculty_login"),
    path('faculty_signup/',views.faculty_signup,name="faculty_signup"),
    path('faculty_mainpage/<uid>/',views.faculty_mainpage,name="faculty_mainpage"),
    path('student_details/<uid>/',views.student_details,name="student_detail"),
    path('u_detail_card/<uid>/<roll>/<firstname>/<lastname>/<batch>/<oemail>/<pemail>/<phone>/',views.user_detail_card,name="u_detail_card"),
    path('notifications/<uid>/',views.notifications,name="notifications"),
    path('notification_detail/<uid>/<id>/<title>/<startdate>/<enddate>/<description>/',views.notification_details,name="notification_detail"),
    path('f_jobs/<uid>/',views.f_jobs,name="f_jobs"),
    path('f_job_details/<uid>/<profile>/<rounds>/<description>/<interview_date>/<attachment>/',views.f_job_details,name="f_job_details"),
    path('f_company/<session_id>/',views.f_company,name="f_company"),



    #quizz

    path('category/<session_id>/',views.category,name="category"),
    path('questions/<session_id>/<id>/',views.category_questions,name="questions"),
    path('submit-answer/<category_id>/<question_id>/<session_id>/',views.submit_answer,name="submit_answer"),
    path('result/<category_id>/<session_id>/',views.result,name="result"),
    

    path('category_a/<session_id>/',views.category_a,name="category_a"),
    path('questions_A/<session_id>/<id>/',views.category_questions_a,name="questions_a"),
    path('submit-answer_a/<category_id>/<question_id>/<session_id>/',views.submit_answer_a,name="submit_answer_a"),
    path('result_a/<category_id>/<session_id>/',views.result_a,name="result_a"),

] 
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)