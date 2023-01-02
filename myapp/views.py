
#demo
from django.shortcuts import render,redirect
import pyrebase

# Create your views here.
config = {
    'apiKey': "AIzaSyDVXhouxFLB3wvUrXzkYS0lasnppSijJjU",
    'authDomain': "myfirst-f209c.firebaseapp.com",
    'projectId': "myfirst-f209c",
    'databaseURL': "https://myfirst-f209c-default-rtdb.firebaseio.com/",
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
        session_id=user['localId']
        request.session['uid']=str(session_id)
        return redirect('welcome')
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"Login.html",{"message":message})
    
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
     name = request.POST.get('name')
     try:
        # creating a user with the given email and password
        print(name)
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        print(user)
        print(uid)
        data={"name":name,"role":"student"}
        print(data)
        database.child("student").child(uid).child("details").set(data)
        return redirect('login')
     except:
        return render(request,"signUp.html")
     return render(request,"login.html")

def navbar(request):

    return render(request,"navbar.html")

def welcome(request):
    
    # res= database.child("student").child(session_id).child("details").get()
    # a= res.val()
    # name=a["name"]
    # print(name)
    
   
    # context={'name':name}

    return render(request,"welcome_msg.html")

def profile(request):
    return render(request,'profile.html')

def alumni_login(request):

    return render(request,'alumni_login.html')

def alumni_postsignin(request):
    email=request.POST.get('email')
    pasw=request.POST.get('password')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
        session_id=user['idToken']
        request.session['uid']=str(session_id)
        return redirect('navbar')
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"alumni_login.html",{"message":message})

    return render(request,'alumni_mainpage.html')

def alumni_signup(request):

    return render(request,'alumni_signup.html')

def alumni_postsignup(request):
    email = request.POST.get('email')
    passs = request.POST.get('password')
    name = request.POST.get('name')

    try:
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        data={"name":name,"role":"alumni"}
        database.child("alumni").child(uid).child("details").set(data)
        return redirect('alumni_login')

    except:
        return redirect('alumni_signup')


    return render(request,'alumni_login.html')

def alumni_mainpage(request):

    return render(request,'alumni_mainpage.html')
