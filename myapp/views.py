
from logging import config
from django.shortcuts import render,redirect
import pyrebase

# Create your views here.
config = {
    'apiKey': "AIzaSyDVXhouxFLB3wvUrXzkYS0lasnppSijJjU",
    'authDomain': "myfirst-f209c.firebaseapp.com",
    'projectId': "myfirst-f209c",
    'databaseURL': "noreply@myfirst-f209c.firebaseapp.com",
    'storageBucket': "myfirst-f209c.appspot.com",
    'messagingSenderId': "1083995112715",
    'appId': "1:1083995112715:web:4d8b25edd10e5d2a024e0e",
    'measurementId': "G-FJ3CW3KRMS"
}

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
 
def signIn(request):
    return render(request,"login.html")
def home(request):
    return render(request,"home.html")
 
def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('password')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"Login.html",{"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request,"Home.html",{"email":email})
 
def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"Login.html")
 
def signUp(request):
    return render(request,"signUp.html")
 
def postsignUp(request):
     email = request.POST.get('email')
     passs = request.POST.get('password')
    #     name = request.POST.get('name')
     try:
        # creating a user with the given email and password
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        print(user)
        print(uid)
        return redirect('login')
     except:
        return render(request,"signUp.html")
     return render(request,"login.html")

def navbar(request):

    return render(request,"navbar.html")
