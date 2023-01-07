

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
        user=authe.sign_in_with_email_and_password(email,pasw)
        session_id=user['localId']
        request.session['uid']=str(session_id)
        res= database.child("users").child(session_id).child("report").get()
        print(res)
        value=res.val()
        rol=value['role']
        print(rol)
        if rol=="student":
            return redirect('/welcome_msg/{}'.format(session_id))
        else:
            message="your role is changed as Alumni. Please login with alumni login"
            return render(request,"login.html",{"message":message})
                
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
        database.child("users").child(uid).child("report").set(data)
        return redirect('login')
     except:
        return render(request,"signUp.html")
     return render(request,"login.html")


def welcome(request,session_id):
    print(session_id)

    res= database.child("users").child(session_id).child("report").get()
    
    a= res.val()
    name=a['name']
    print(name)

    context={'session_id':session_id,'name':name}

    return render(request,"welcome_msg.html",context)

def profile(request,session_id):
    roll=request.POST.get('roll')
    firstname=request.POST.get('firstname')
    lastname=request.POST.get('lastname')
    phone=request.POST.get('phone')
    batch=request.POST.get('batch')
    pemail=request.POST.get('pemail')
    oemail=request.POST.get('oemail')

    # res= database.child("users").child(session_id).child("details").get()
    # a= res.val()
    # a=a['localId']

    data={'firstname':firstname,'roll':roll,'lastname':lastname,'phone':phone,'batch':batch,'pmeail':pemail,'oemail':oemail}
    database.child("users").child(session_id).child("details").set(data)

    context={'session_id':session_id}
    return render(request,'profile.html',context)

def alumnilist(request,session_id):
    final=[]
    if request.method=="POST":
        batch=request.POST.get('batch')
        print(batch)
        result=database.child("users").get().val()
        print(result)
        for i in result.keys():
            if(result[i]['details']['batch'] == batch):
                final.append(result[i]['details'])
        print("the final")
        print(final)
        


    context={'session_id':session_id,'final':final}
    return render(request,"alumni_list.html",context)

def news(request,session_id):

    context={'session_id':session_id}
    return render(request,"news.html",context)

def jobs(request,session_id
):

    context={'session_id':session_id}
    return render(request,"jobs.html",context)

def profile_card(request,session_id,roll,firstname,lastname,batch,oemail,pemail,phone):
    
    # list=[]
    # for i in details:
    #     list.append(i)
    context={'roll':roll,'firstname':firstname,'lastname':lastname,'batch':batch,'oemail':oemail,'pemail':pemail,'phone':phone,'session_id':session_id}
    return render(request,"detail_card.html",context)

def alumni_login(request):

    return render(request,'alumni/alumni_login.html')

def alumni_postsignin(request):
    email=request.POST.get('email')
    pasw=request.POST.get('password')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
        session_id=user['localId']
        request.session['uid']=str(session_id)
        
        
        return redirect('/alumni_mainpage/{}'.format(session_id))
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"alumni/alumni_login.html",{"message":message})
    return render(request,'alumni_mainpage.html')

def alumni_signup(request):

    return render(request,'alumni/alumni_signup.html')

def alumni_postsignup(request):
    email = request.POST.get('email')
    passs = request.POST.get('password')
    name = request.POST.get('name')

    try:
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        data={"name":name,"role":"alumni"}
        database.child("users").child(uid).child("details").set(data)
        return redirect('alumni_login')

    except:
        return redirect('alumni_signup')


    return render(request,'alumni_login.html')

def alumni_mainpage(request,session_id):

    context={'session_id':session_id}
    return render(request,'alumni/alumni_mainpage.html',context)

def alumni_news(request,session_id):

    context={'session_id':session_id}
    return render(request,"alumni/alumni_not.html",context)

def alumni_job(request,session_id):

    context={'session_id':session_id}
    return render(request,"alumni/alumni_job",context)
