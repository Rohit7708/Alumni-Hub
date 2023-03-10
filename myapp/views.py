from django.shortcuts import render,redirect
from datetime import datetime,timezone,timedelta
from django.utils import timezone
import uuid
import pyrebase
import smtplib
from email.message import EmailMessage
from django.http import JsonResponse,HttpResponse
from .models import *
import pandas as pd
from django.conf import settings
import schedule
import time
import datetime



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



def home(request):

    
        
    
    return render(request,"home.html")
 
def signIn(request):
    
    
    return render(request,"login.html")
 
def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('password')
    
    
    try:
        user=authe.sign_in_with_email_and_password(email,pasw)
        session_id=user['localId']
        request.session['uid']=str(session_id)
        
        res= database.child("users").child(session_id).child("details").get()
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

    timestamp = timezone.now()
    user_id= request.session['uid']
    database.child("last_login").child(user_id).child("time").set(str(timestamp))
    
    
    return render(request,"login.html")
 
def signUp(request):
    return render(request,"signUp.html")
 
def postsignUp(request):
    email = request.POST.get('oemail')
    passs = request.POST.get('password')
    name = request.POST.get('name')
    roll=request.POST.get('roll_number')
    firstname=request.POST.get('firstname')
    lastname=request.POST.get('lastname')
    phone=request.POST.get('phone')
    batch=request.POST.get('batch')
    pemail=request.POST.get('pemail')
    oemail=request.POST.get('oemail')
    department=request.POST.get('department')

    try:
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        data={'role':"student",'firstname':firstname,'roll':roll,'lastname':lastname,'phone':phone,'batch':batch,'pmeail':pemail,'oemail':oemail,'department':department}
        database.child("users").child(uid).child("details").set(data)
        return redirect('login')
    except:
        return render(request,"signUp.html")
    


def welcome(request,session_id):
    points_list=[]
    pts=database.child("points").get().val()
    if pts is not None:
        for i in pts.keys():
            data=database.child("users").child(i).get().val()
            roll=data["details"]["roll"]
            name=data["details"]["firstname"]
            role=data["details"]["role"]
            points=pts[i]["point"]
            point_data = {"roll": roll, "name": name, "role": role, "points": points}  # create a dictionary with roll, name, role, and points
            points_list.append(point_data)  # append the dictionary to points_list

    res= database.child("users").child(session_id).child("details").get()
    a= res.val()
    firstname=a['firstname']
    lastname=a['lastname']
    name=firstname+lastname

    

    sorted_points_list = sorted(points_list, key=lambda x: x['points'], reverse=True)
    print(sorted_points_list)

    context={'session_id':session_id,'name':name,'points_list':sorted_points_list}

    return render(request,"welcome_msg.html",context)

def update_profile(request,session_id):
    result=database.child("users").child(session_id).child("details").get().val()
    if result is None:
        message="Profile does not exist!"
        return render(request,"welcome_msg.html",{'message':message,'session_id':session_id})

    else:
        if request.method=="POST":
            roll=request.POST.get('rollnumber')
            firstname=request.POST.get('firstname')
            lastname=request.POST.get('lastname')
            phone=request.POST.get('phone')
            batch=request.POST.get('batch')
            pemail=request.POST.get('pemail')
            oemail=request.POST.get('oemail')
            department=request.POST.get('department')
            print(department)
            print(roll)
            print(batch)
            workingat=request.POST.get('workingat')
            data={'firstname':firstname,'roll':roll,'lastname':lastname,'phone':phone,'batch':batch,'pmeail':pemail,'oemail':oemail,'department':department,'role':"student",'workingat':workingat}
            database.child("users").child(session_id).child("details").set(data)

    context={'session_id':session_id,'details':result}
    return render(request,"update_profile.html",context)

def alumnilist(request,session_id):
    final_list=[]
    if request.method=="POST":
        batch=request.POST.get('batch')
        
        result=database.child("users").get().val()
        for i in result.keys():
            if result[i]['details']['batch'] == batch:
                final_list.append(result[i]['details'])

    not_list = sorted(final_list,key= lambda x : x["roll"])
        
    context={'session_id':session_id,'final':not_list}   
    return render(request,"alumni_list.html",context)


def notification_detail_student(request,not_id,session_id,title,startdate,enddate,description):

    print(not_id)
    print(session_id)
    update_status=database.child("view_status").child(session_id).child("notification").child(not_id).child("status").update({'isopen':True})
    context={'session_id':session_id,'title':title,'startdate':startdate,'enddate':enddate,'description':description}
    return render(request,"st_notification_detail.html",context)

def notification_history(request,session_id):
    mail_list=["21mx123@psgtech.ac.in"]
    if request.method=="POST": 
        title=request.POST.get('title')
        des=request.POST.get('des')
        att=request.POST.get('attachment')
        startdate=request.POST.get('startdate')
        enddate=request.POST.get('enddate')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = timezone.now().timestamp()
        notification_id = uuid.uuid4()

        data={'id':str(notification_id),'title':title,'startdate':startdate,'enddate':enddate,'description':des,'attachment':att,'time':current_time,'date':today,'sender_id':session_id,'notification_pushedby':"student",'session_id':session_id}
        database.child("event_notification").child(notification_id).child("details").set(data)

        result=database.child("users").get().val()
        print(result)
        for i in result.keys():
            not_details={'isopen':False}
            notification=database.child("view_status").child(i).child("notification").child(notification_id).child("status").set(not_details)

        # result=database.child("users").get().val()
        # if result is not None:
        #     for i in result.keys():
        #         if(result[i]['details']['role'] == "alumni"):
        #             mail_list.append(result[i]['details'])      

        for i in mail_list:
            print("working")
            EMAIL_ADDRESS='alumnihub.portal@gmail.com'
            EMAIL_PASSWORD='kiliblelhkqlpsqp'
            msg=EmailMessage()
            msg['subject']='Event notification'
            msg['form']=EMAIL_ADDRESS
            msg['To']=i
            msg.set_content('Event notification has been posted. Kindly check your AlumniHub !')

            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
                smtp.send_message(msg)
                print("msg sent")
    
    status=database.child("view_status").child(session_id).child("notification").get().val() 

    not_list=[]
    al_not_count=int(0)
    event = database.child("event_notification").get().val()
    if event is not None:
        for i in event.keys():
            if(event[i]['details']['notification_pushedby'] == "alumni"):
                not_list.append(event[i]['details'])
        
    else:
        Message="No events"
        print(Message)

    if status is not None:
        for i in status.keys():
            notification_details = database.child("event_notification").child(i).child("details").get().val()
            if notification_details["notification_pushedby"] == "alumni":
                if status[i]['status']['isopen'] == False:
                    al_not_count+= int(1)
        
        print(al_not_count)

    st_not_count=int(0)
    st_notificataion_list=[]
    events = database.child("event_notification").get().val()
    if events is not None:
        for i in events.keys():
            if(events[i]['details']['notification_pushedby'] == "faculty"):
                st_notificataion_list.append(events[i]['details'])
                
        print(st_notificataion_list)
        
    else:
        message="No Events to Display"
        print(message)

    if status is not None:
        for i in status.keys():
            notification_details = database.child("event_notification").child(i).child("details").get().val()
            if notification_details["notification_pushedby"] == "student":
                if status[i]['status']['isopen'] == False:
                    st_not_count+= int(1)
        
        print(st_not_count)

    fl_list=[]
    fl_not_count=int(0)
    events = database.child("event_notification").get().val()
    if events is not None:
        for i in events.keys():
            if(events[i]['details']['notification_pushedby'] == "faculty"):
                fl_list.append(events[i]['details'])
 
    if status is not None:
        for i in status.keys():
            notification_details = database.child("event_notification").child(i).child("details").get().val()
            if notification_details["notification_pushedby"] == "faculty":
                if status[i]['status']['isopen'] == False:
                    fl_not_count+= int(1)
        
        print(fl_not_count)
                
    my_list=[]
    my_notification = database.child("event_notification").get().val()
    if my_notification is not None:
        for i in my_notification.keys():
            if(my_notification[i]['details']['session_id']==session_id):
                my_list.append(my_notification[i]['details'])

    else:
        print("no notification")

    

    st_notificataion_list = sorted(st_notificataion_list,key= lambda x : x["date"], reverse=True)

    not_list = sorted(not_list,key= lambda x : x["date"], reverse=True)
    

    my_list=sorted(my_list,key=lambda x: x["date"],reverse=True)
    

    fl_notification_list=sorted(fl_list,key=lambda x: x["date"],reverse=True)

    context={'session_id':session_id,'not_list':not_list,'st_notification_list':st_notificataion_list,'my_list':my_list,'fl_notification_list':fl_notification_list,
    'st_not_count':st_not_count,'fl_not_count':fl_not_count,'al_not_count':al_not_count}
    return render(request,"notification_history.html",context)

def jobs(request,session_id):
    job_list=[]
    result=database.child("interview_posts").get().val()
    if result is not None:
        for i in result.keys():
            job_list.append(result[i])

    else:
        print("None")

    context={'session_id':session_id,'job_list':job_list}
    return render(request,"jobs.html",context)

def job_details(request,session_id,profile,rounds,description,interview_date,attachment):
    
    return render(request,"job_details.html",{'session_id':session_id,'profile':profile,'rounds':rounds,'description':description,'interview_date':interview_date,'attachment':attachment})

def profile_card(request,session_id,roll,firstname,lastname,batch,oemail,pemail,phone):
    
    # list=[]
    # for i in details:
    #     list.append(i)
    context={'roll':roll,'firstname':firstname,'lastname':lastname,'batch':batch,'oemail':oemail,'pemail':pemail,'phone':phone,'session_id':session_id}
    return render(request,"detail_card.html",context)

def interview_experience(request,session_id):
    roll=None
    batch=None
    
    # company_list=sorted(com_list,key=lambda x: x["company"])
    # print(company_list)


    result=database.child("users").get().val()
    if result is not None:
        for i in result.keys():
            if(result[i] == session_id):
                roll=result[i]["details"]["roll"]
                batch=result[i]["details"]["batch"]

    if request.method=="POST":
        name=request.POST.get('name')
        company=request.POST.get('company_name')
        round=request.POST.get('rounds')
        mode=request.POST.get('mode')
        exp=request.POST.get('exp')
        id=uuid.uuid4()


    
        data={
            'name':name,
            'company':company,
            'round':round,
            'mode':mode,
            'exp':exp,
            'roll':roll,
            'batch':batch
        }
        print(data)
        database.child("Interview_exp").child(id).set(data)
        return redirect('interview_exp',session_id)

    
    

    context={'session_id':session_id}
    return render(request,'interview_exp.html',context)

def company_submit(request,session_id):

    int_exp_list=[]
    co_list=[]
    res=database.child("Interview_Exp").get().val()
    if res is not None:
        for i in res.keys():
            if res[i]["details"]["company"] not in co_list:
                co_list.append(res[i]["details"]["company"])
    else:
        print("None")

    if request.method=="POST":
        company=request.POST.get('company')
        print("company")
        print(company)
        for i in res.keys():
            if res[i]["details"]['company'] == company:
                int_exp_list.append(res[i]["details"])
    print(int_exp_list)


    return render(request,"company.html",{'session_id':session_id,'company_list':co_list,'int_exp_list':int_exp_list})

def alumni_login(request):
    users_data = database.child("users").get().val()

    # Loop through each user's data and update the email field to an empty string
    for i, data in users_data.items():
        database.child("users").child(i).child("details").update({"pmeail": "rohitsmash06@gmail.com"})

    return render(request,'alumni/alumni_login.html')

def alumni_postsignin(request):
    email=request.POST.get('email')
    pasw=request.POST.get('password')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
        session_id=user['localId']
        request.session['uid']=str(session_id)
        res= database.child("users").child(session_id).child("report").get()
        print(res)
        value=res.val()
        rol=value['role']
        print(rol)
        if rol=="alumni":
            return redirect('/alumni_mainpage/{}'.format(session_id))
        else:
            message="your role is student. Please login with student login"
            return render(request,"alumni.alumni/login.html",{"mess":message})
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
        database.child("users").child(uid).child("report").set(data)
        return redirect('alumni_login')

    except:
        return redirect('alumni_signup')


    return render(request,'alumni_login.html')

def alumni_mainpage(request,session_id):
    points_list=[]
    pts=database.child("points").get().val()
    if pts is not None:
        for i in pts.keys():
            data=database.child("users").child(i).get().val()
            roll=data["details"]["roll"]
            name=data["details"]["firstname"]
            role=data["details"]["role"]
            points=pts[i]["point"]
            point_data = {"roll": roll, "name": name, "role": role, "points": points}  # create a dictionary with roll, name, role, and points
            points_list.append(point_data)  # append the dictionary to points_list

    res= database.child("users").child(session_id).child("details").get()
    # a= res.val()
    # firstname=a['firstname']
    # lastname=a['lastname']
    # name=firstname+lastname
    # print(name)

    sorted_points_list = sorted(points_list, key=lambda x: x['points'], reverse=True)
    print(sorted_points_list)

    context={'session_id':session_id,'points_list':sorted_points_list}
    return render(request,'alumni/alumni_mainpage.html',context)

def a_interview_experience(request,session_id):
    roll=None
    batch=None
    
    # company_list=sorted(com_list,key=lambda x: x["company"])
    # print(company_list)


    result=database.child("users").get().val()
    if result is not None:
        for i in result.keys():
            if(result[i] == session_id):
                roll=result[i]["details"]["roll"]
                batch=result[i]["details"]["batch"]

    if request.method=="POST":
        name=request.POST.get('name')
        company=request.POST.get('company_name')
        round=request.POST.get('rounds')
        mode=request.POST.get('mode')
        exp=request.POST.get('exp')
        id=uuid.uuid4()


    
        data={
            'name':name,
            'company':company,
            'round':round,
            'mode':mode,
            'exp':exp,
            'roll':roll,
            'batch':batch
        }
        print(data)
        database.child("Interview_exp").child(id).set(data)
        return redirect('interview_exp',session_id)

    
    

    context={'session_id':session_id}
    return render(request,'a_interview_exp.html',context)

def a_company_submit(request,session_id):

    int_exp_list=[]
    co_list=[]
    res=database.child("Interview_Exp").get().val()
    if res is not None:
        for i in res.keys():
            if res[i]["details"]["company"] not in co_list:
                co_list.append(res[i]["details"]["company"])
    else:
        print("None")

    if request.method=="POST":
        company=request.POST.get('company')
        print("company")
        print(company)
        for i in res.keys():
            if res[i]["details"]['company'] == company:
                int_exp_list.append(res[i]["details"])
    print(int_exp_list)


    return render(request,"a_company.html",{'session_id':session_id,'company_list':co_list,'int_exp_list':int_exp_list})




def alumni_notification(request,session_id):
    mail_list=["21mx123@psgtech.ac.in"]
    if request.method=="POST":
        title=request.POST.get('title')
        des=request.POST.get('des')
        att=request.POST.get('attachment')
        startdate=request.POST.get('startdate')
        enddate=request.POST.get('enddate')
        print(att)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = timezone.now().timestamp()
        notification_id = uuid.uuid4()

        data={'title':title,'startdate':startdate,'enddate':enddate,'description':des,'time':current_time,'date':today,'student_id':session_id,'notification_pushedby':"alumni",'session_id':session_id}
        database.child("event_notification").child(notification_id).child("details").set(data)

        # result=database.child("users").get().val()
        # for i in result.keys():
        #     if(result[i]['details']['role'] == "alumni"):
        #         mail_list.append(result[i]['details'])      

        for i in mail_list:
            EMAIL_ADDRESS='alumnihub.portal@gmail.com'
            EMAIL_PASSWORD='kiliblelhkqlpsqp'
            msg=EmailMessage()
            msg['subject']='Event notification'
            msg['form']=EMAIL_ADDRESS
            msg['To']=i
            msg.set_content('Event notification has been posted. Kindly check your AlumniHub !')

            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
                smtp.send_message(msg)
                print("msg sent")
    
    status=database.child("view_status").child(session_id).child("notification").get().val() 

    not_list=[]
    event = database.child("event_notification").get().val()
    if event is not None:
        for i in event.keys():
            if(event[i]['details']['notification_pushedby'] == "alumni"):
                not_list.append(event[i]['details']) 
        
    else:
        Message="No events"
        print(Message)

    st_notificataion_list=[]
    events = database.child("event_notification").get().val()
    if events is not None:
        for i in events.keys():
            if(events[i]['details']['notification_pushedby'] == "student"):
                st_notificataion_list.append(events[i]['details']) 
        
    else:
        message="No Events to Display"
        print(message)

    my_list=[]
    my_notification = database.child("event_notification").get().val()
    if my_notification is not None:
        for i in my_notification.keys():
            if(my_notification[i]['details']['session_id']==session_id):
                my_list.append(my_notification[i]['details'])

    else:
        print("no notification")

    

    st_notificataion_list = sorted(st_notificataion_list,key= lambda x : x["date"], reverse=True)
    print("st_not")
    print(st_notificataion_list)

    not_list = sorted(not_list,key= lambda x : x["date"], reverse=True)
    print(not_list)

    my_list=sorted(my_list,key=lambda x: x["date"],reverse=True)
    print("mylist")
    print(my_list)

    


    context={'session_id':session_id,'not_list':not_list,'st_notification_list':st_notificataion_list,'my_list':my_list}
    return render(request,"alumni/alumni_notification.html",context)

def students_list(request,session_id):
    final_list=[]
    if request.method=="POST":
        batch=request.POST.get('batch')
        print(batch)
        result=database.child("users").get().val()
        print(result)
        for i in result.keys():
            if(result[i]['details']['batch'] == batch):
                final_list.append(result[i]['details'])
        print("the final")
        print(final_list)
    not_list = sorted(final_list,key= lambda x : x["roll"])

    context={'session_id':session_id,'not_list':not_list}
    return render(request,'alumni/students_list.html',context)

def alumni_detailcard(request,session_id,roll,firstname,lastname,batch,oemail,pemail,phone,workingat):

    context={'roll':roll,'firstname':firstname,'lastname':lastname,'batch':batch,'oemail':oemail,'pemail':pemail,'phone':phone,'session_id':session_id,'workingat':workingat}
    return render(request,"alumni/alumni_detailcard.html",context)

def alumni_profile(request,session_id):
    result= database.child("users").child(session_id).child("details").get().val()
    print(result)
    if result is not None:
        message="your profile is being already created"
        return render(request,"alumni/alumni_mainpage.html",{'message':message,'session_id':session_id})

    else: 
        if request.method=="POST":
            roll=request.POST.get('roll_number')
            firstname=request.POST.get('firstname')
            lastname=request.POST.get('lastname')
            phone=request.POST.get('phone')
            batch=request.POST.get('batch')
            pemail=request.POST.get('pemail')
            oemail=request.POST.get('oemail')
            department=request.POST.get('department')
            print(department)
            print(roll)
            print(batch)
            workingat=request.POST.get('workingat')


            data={'role':"alumni",'firstname':firstname,'roll':roll,'lastname':lastname,'phone':phone,'batch':batch,'pmeail':pemail,'oemail':oemail,'department':department,'workingat':workingat}
            database.child("users").child(session_id).child("details").set(data)
    context={'session_id':session_id}
    return render(request,"alumni/alumni_profileset.html",context)

def alumni_updateprofile(request,session_id):
    result=database.child("users").child(session_id).child("details").get().val()
    if result is None:
        message="Profile does not exist!"
        return render(request,"alumni/alumni_mainpage.html",{'message':message,'session_id':session_id})

    else:
        if request.method=="POST":
            roll=request.POST.get('rollnumber')
            firstname=request.POST.get('firstname')
            lastname=request.POST.get('lastname')
            phone=request.POST.get('phone')
            batch=request.POST.get('batch')
            pemail=request.POST.get('pemail')
            oemail=request.POST.get('oemail')
            department=request.POST.get('department')
            print(department)
            print(roll)
            print(batch)
            workingat=request.POST.get('workingat')
            data={'role':'alumni','firstname':firstname,'roll':roll,'lastname':lastname,'phone':phone,'batch':batch,'pmeail':pemail,'oemail':oemail,'department':department,'workingat':workingat}
            database.child("users").child(session_id).child("details").set(data)
            resul=database.child("users").child(session_id).child("details").get().val()
            return render(request,"alumni/alumni_updateprofile.html",{'session_id':session_id,'details':resul})

    context={'session_id':session_id,'details':result}
    return render(request,"alumni/alumni_updateprofile.html",context)

def notification_detail(request,description,title,att,startdate,enddate):
    print(description)
    print(title)
    context={'description':description,'title':title,'att':att,'startdate':startdate,'enddate':enddate}
    return render(request,"alumni/notification_detail.html",context)

def al_event_notify(request,session_id):
    mail_list=["21mx123@psgtech.ac.in"]
    if request.method=="POST":
        title=request.POST.get('title')
        startdate=request.POST.get('startdate')
        enddate=request.POST.get('enddate')
        des=request.POST.get('des')
        att=request.POST.get('attachment')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = datetime.today()
        date = today.strftime("%B %d, %Y")
        notification_id = uuid.uuid4()

        data={'title':title,'startdate':startdate,'enddate':enddate,'description':des,'attachment':att,'time':current_time,'date':date,'student_id':session_id,'notification_pushedby':"alumni"}
        database.child("Student_event_notification").child(notification_id).child("details").set(data)

        # result=database.child("users").get().val()
        # for i in result.keys():
        #     if(result[i]['detail']['role'] == "student"):
        #         mail_list.append(result[i]['details'])      

        for i in mail_list:
            EMAIL_ADDRESS='alumnihub.123@gmail.com'
            EMAIL_PASSWORD='veicbwofgzonpzih'
            msg=EmailMessage()
            msg['subject']='Event notification'
            msg['form']=EMAIL_ADDRESS
            msg['To']=i
            msg.set_content('Event notification has been posted. Kindly check your AlumniHub !')

            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
                smtp.send_message(msg)
                print("msg sent")

    context={'session_id':session_id}
    return render(request,"alumni/al_event_notify.html",context)

def alumni_job(request,session_id):

    context={'session_id':session_id}
    return render(request,"alumni/alumni_job",context)

def get_rollnumber(request,session_id):
    sender = None
    result=database.child("users").get().val()
    for i in result.keys():
        if(i == session_id):
            sender=result[i]["details"]["roll"]
    
    print(sender)
    user_list=[]
    if request.method=="POST":
        batch=request.POST.get('batch')
        result=database.child("users").get().val()
        for i in result.keys():
            if(result[i]['details']['batch'] == batch):
                user_list.append(result[i]['details'])
    users_list = sorted(user_list,key= lambda x : x["roll"])
    
    chat_hist=[]
    result=database.child("Messages").get().val()
    if result is not None:
        for i in result.keys():
            print(i)
            if result[i]['details']['sender'] == sender and result[i]['details']['sender']:
                chat_hist.append(result[i]['details'])

    hist=sorted(chat_hist,key=lambda x: x["timestamp"],reverse=True)

    unique_receivers = set()

    # create an empty list to store the unique messages
    unique_messages = []

    # iterate through each message
    for message in hist:
        # if the receiver is not in the unique_receivers set, add it to the set
        if message['receiver'] not in unique_receivers:
            unique_receivers.add(message['receiver'])
            # add the message to the unique_messages list
            unique_messages.append(message)

        
    print(unique_messages)
    context={'session_id':session_id,'users_list':users_list,'sender':sender,'hist':unique_messages}
    return render(request,"chat/roll.html",context)

def room(request,session_id,sender,receiver):
    if database.child('Room').child(receiver).get().val() is not None:
        return redirect('chat', session_id, sender, receiver)
    else:
        database.child('Room').child(receiver).set({'name': receiver})
        print("new chat room created")
        return redirect('chat', session_id, sender, receiver)

    return HttpResponse("Done")

def chat(request,session_id,sender,receiver):
    
    context={'session_id':session_id,'sender':sender,'receiver':receiver}
    return render(request,"chat/chat.html",context)
import datetime
def send(request):
    sender=request.POST.get('username')
    receiver=request.POST.get('room_id')
    message=request.POST.get('message')
    timest = datetime.datetime.now()

# display the timestamp in a specific format
    timestamp = timest.strftime("%Y-%m-%d %H:%M:%S")
    data={'room_id':receiver,'message':message,'timestamp':timestamp,'sender':sender,'receiver':receiver}
    print(data)
    database.child("Messages").child(timestamp).child("details").set(data)

    return HttpResponse('Message sent successfully')


def getMessages(request,receiver,sender):
    print(sender)
    print(receiver)
    
    messages=[]
    result=database.child("Messages").get().val()
    if result is not None:
        for i in result.keys():
            if result[i]['details']['sender']==sender and result[i]['details']['receiver'] == receiver or result[i]['details']['sender']==receiver and result[i]['details']['receiver']==sender:
                messages.append(result[i]['details'])
    mes=sorted(messages,key=lambda x: x["timestamp"])
    return JsonResponse({"message":mes})



def job_post(request,session_id):
    sender=None
    rollnumber=None
    result=database.child("users").get().val()
    for i in result.keys():
        if(i == session_id):
            sender=result[i]["details"]["firstname"]
            rollnumber=result[i]["details"]["roll"]
    if request.method == "POST":
        print("working")
        company_name=request.POST.get('company_name')
        profile=request.POST.get('profile')
        description=request.POST.get('description')
        rounds=request.POST.get('rounds')
        interview_date=request.POST.get('interview_date')
        last_date=request.POST.get('last_date')
        attachment=request.POST.get('attachment')

        data={
            'company_name':company_name,
            'profile':profile,
            'description':description,
            'rounds':rounds,
            'interview_date':interview_date,
            'last_date':last_date,
            'attachment':attachment,
            'posted_by':session_id,
            'sender_name':sender,
            'sender_rollnumber':rollnumber
            }
        
        post_id = uuid.uuid4()

        database.child("interview_posts").child(post_id).set(data)

        mail_list=["21mx123@psgtech.ac.in"]
        # result=database.child("users").get().val()
        # for i in result.keys():
        #     if(result[i]['details']['role'] == "student"):
        #         mail_list.append(result[i]['details'])      

        for i in mail_list:
            EMAIL_ADDRESS='alumnihub.portal@gmail.com'
            EMAIL_PASSWORD='kiliblelhkqlpsqp'
            
            msg=EmailMessage()
            msg['subject']='Job Notification'
            msg['form']=EMAIL_ADDRESS
            msg['To']=i
            # name=i['firstname']
            
            msg.set_content("Hi" +"\U0001F600 \n A new job opportunity has been posted\n Company:" + company_name +"\n\nCheck your AlumniHub for more details!")
            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
                smtp.send_message(msg)
                print("msg sent")







    context={'session_id':session_id}
    return render(request,"alumni/job_post.html",context)



# faculty views

def faculty_signIn(request):
    return render(request,"faculty/faculty_login.html")
def faculty_signUp(request):
    return render(request,"faculty/faculty_signup.html")


def faculty_login(request):
    email=request.POST.get('email')
    pasw=request.POST.get('password')
    try:
        user=authe.sign_in_with_email_and_password(email,pasw)
        session_id=user['localId']
        request.session['uid']=str(session_id)
        res= database.child("faculty").child(session_id).child("details").get()
        print(res)
        value=res.val()
        rol=value['role']
        print(rol)
        if rol=="faculty":
            return redirect('/faculty_mainpage/{}'.format(session_id))
        else:
            message=" This is faculty login. kindly login with your corerect role"
            return render(request,"faculty/faculty_login.html",{"message":message})
                
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"faculty/faculty_login.html",{"message":message})

    return render(request,"faculty/faculty_login.html")

def faculty_signup(request):
    email = request.POST.get('email')
    pass1 = request.POST.get('password')
    pass2 = request.POST.get('password2')
    username=request.POST.get('username')
    if pass1 != pass2:

        try:
            user=authe.create_user_with_email_and_password(email,pass1)
            uid = user['localId']
            data={'role':"faculty",'email':email,'username':username}
            database.child("faculty").child(uid).child("details").set(data)
            return redirect('faculty_signIn')
        except:
            return render(request,"faculty/faculty_signup.html")

    else:
        print("not matched")
        return redirect('faculty_signUp')
        

    return render(request,"faculty/faculty_signup.html")

def faculty_mainpage(request,uid):

    res= database.child("faculty").child(uid).child("details").get()
    
    a= res.val()
    name=a['username']
    context={'uid':uid,'name':name}
    return render(request,"faculty/faculty_mainpage.html",context)

def student_details(request,uid):
    final_list=[]
    if request.method=="POST":
        batch=request.POST.get('batch')
        result=database.child("users").get().val()
        for i in result.keys():
            if(result[i]['details']['batch'] == batch):
                final_list.append(result[i]['details'])
    print(final_list)
    context={'uid':uid,'final_list':final_list}
    return render(request,"faculty/student_details.html",context)

def user_detail_card(request,uid,roll,firstname,lastname,batch,oemail,pemail,phone):
    
    # list=[]
    # for i in details:
    #     list.append(i)
    context={'roll':roll,'firstname':firstname,'lastname':lastname,'batch':batch,'oemail':oemail,'pemail':pemail,'phone':phone,'uid':uid}
    return render(request,"faculty/u_detail_card.html",context)
    
def notifications(request,uid):
    mail_list=["21mx123@psgtech.ac.in"]
    if request.method=="POST":
        title=request.POST.get('title')
        des=request.POST.get('des')
        att=request.POST.get('attachment')
        startdate=request.POST.get('startdate')
        enddate=request.POST.get('enddate')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = timezone.now().timestamp()
        notification_id = uuid.uuid4()

        data={'id':str(notification_id),'title':title,'startdate':startdate,'enddate':enddate,'description':des,'attachment':att,'time':current_time,'date':today,'sender_id':uid,'notification_pushedby':"faculty",'session_id':uid}
        database.child("event_notification").child(notification_id).child("details").set(data)

        result=database.child("users").get().val()
        print(result)
        for i in result.keys():
            not_details={'isopen':False}
            notification=database.child("view_status").child(i).child("notification").child(notification_id).child("status").set(not_details)
        # result=database.child("users").get().val()
        # if result is not None:
        #     for i in result.keys():
        #         if(result[i]['details']['role'] == "alumni"):
        #             mail_list.append(result[i]['details'])      

        for i in mail_list:
            EMAIL_ADDRESS='alumnihub.portal@gmail.com'
            EMAIL_PASSWORD='kiliblelhkqlpsqp'
            msg=EmailMessage()
            msg['subject']='Event notification'
            msg['form']=EMAIL_ADDRESS
            msg['To']=i
            msg.set_content('Event notification has been posted. Kindly check your AlumniHub !')

            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
                smtp.send_message(msg)
                print("msg sent")

    status=database.child("view_status").child(uid).child("notification").get().val() 

    not_list=[]
    event = database.child("event_notification").get().val()
    if event is not None:
        for i in event.keys():
            if(event[i]['details']['notification_pushedby'] == "alumni"):
                not_list.append(event[i]['details']) 
        
    else:
        Message="No events"
        print(Message)

    st_notificataion_list=[]
    events = database.child("event_notification").get().val()
    if events is not None:
        for i in events.keys():
            if(events[i]['details']['notification_pushedby'] == "student"):
                st_notificataion_list.append(events[i]['details']) 
        
    else:
        message="No Events to Display"
        print(message)

    fl_list=[]
    events = database.child("event_notification").get().val()
    if events is not None:
        for i in events.keys():
            if(events[i]['details']['notification_pushedby'] == "faculty"):
                fl_list.append(events[i]['details'])

    fl_not_count=int(0)
    if status is not None:
        for i in status.keys():
            notification_details = database.child("event_notification").child(i).child("details").get().val()
            if notification_details["notification_pushedby"] == "faculty":
                if status[i]['status']['isopen'] == False:
                    fl_not_count+= int(1)
    print("count")
    print(fl_not_count)


    my_list=[]
    my_notification = database.child("event_notification").get().val()
    if my_notification is not None:
        for i in my_notification.keys():
            if(my_notification[i]['details']['session_id']==uid):
                my_list.append(my_notification[i]['details'])

    else:
        print("no notification")

    

    st_notificataion_list = sorted(st_notificataion_list,key= lambda x : x["date"], reverse=True)

    not_list = sorted(not_list,key= lambda x : x["date"], reverse=True)
    

    my_list=sorted(my_list,key=lambda x: x["date"],reverse=True)
    

    fl_notification_list=sorted(fl_list,key=lambda x: x["date"],reverse=True)

    context={'uid':uid,'not_list':not_list,'st_notification_list':st_notificataion_list,'my_list':my_list,'fl_notification_list':fl_notification_list,'fl_not_count':fl_not_count}

    return render(request,"faculty/notifications.html",context)

def notification_details(request,uid,id,title,startdate,enddate,description):

    context={'uid':uid,'title':title,'startdate':startdate,'enddate':enddate,'description':description}
    return render(request,"faculty/notification_details.html",context)

def f_jobs(request,uid):
    job_list=[]
    result=database.child("interview_posts").get().val()
    if result is not None:
        for i in result.keys():
            job_list.append(result[i])

    else:
        print("None")

    context={'uid':uid,'job_list':job_list}
    return render(request,"faculty/f_jobs.html",context)

def f_job_details(request,uid,profile,rounds,description,interview_date,attachment):
    
    return render(request,"faculty/f_job_details.html",{'uid':uid,'profile':profile,'rounds':rounds,'description':description,'interview_date':interview_date,'attachment':attachment})

def f_company(request,session_id):
    int_exp_list=[]
    co_list=[]
    res=database.child("Interview_Exp").get().val()
    if res is not None:
        for i in res.keys():
            if res[i]["details"]["company"] not in co_list:
                co_list.append(res[i]["details"]["company"])
    else:
        print("None")

    if request.method=="POST":
        company=request.POST.get('company')
        print("company")
        print(company)
        for i in res.keys():
            if res[i]["details"]['company'] == company:
                int_exp_list.append(res[i]["details"])
    print(int_exp_list)


    context={'session_id':session_id,'company_list':co_list,'int_exp_list':int_exp_list}
    return render(request,'faculty/f_company.html',context)







# quizz 
def category(request,session_id):
    print("function called")
    category=Category.objects.all()
    creds=None
    print(category.values())
    cred=database.child("points").child(session_id).get('point').val()
    if cred is not None:
        creds=cred['point']

    else:
        creds=int(0)

    context={'session_id':session_id,'category':category,'creds':creds}
    return render(request,"Quizz/category.html",context)

from datetime import timedelta
def category_questions(request,session_id,id):
    category=Category.objects.get(id=id)
    question=QuizQuestion.objects.filter(category=category).order_by('id').first()
    lastAttemp=None
    futureTime=None
    hoursLimit=24
    countAttempt=UserCategoryAttempts.objects.filter(user=session_id,category=category).count()  
    if countAttempt == 0:
        UserCategoryAttempts.objects.create(user=session_id,category=category)
    else:
        lastAttemp=UserCategoryAttempts.objects.filter(user=session_id,category=category).order_by('-id').first()
        futureTime = lastAttemp.attemt_time +  timedelta(hours=hoursLimit)

        if lastAttemp and lastAttemp.attemt_time < futureTime:
            return HttpResponse('you can submit')    
        else:
            UserCategoryAttempts.objects.create(user=session_id,category=category)
        

    
    context={'session_id':session_id,'question':question,'category':category,'lastAttemp':futureTime}
    return render(request,"Quizz/questions.html",context)

def submit_answer(request,category_id,question_id,session_id):
    if request.method == "POST":
        category=Category.objects.get(id=category_id)
        question=QuizQuestion.objects.filter(category=category,id__gt=question_id).exclude(id=question_id).order_by('id').first()
        if 'skip' in request.POST:
            if question:
                quest=QuizQuestion.objects.get(id=question_id)
                user=session_id
                answer='Not Submitted'
                UserSubmittedAnswer.objects.create(user=user,question=quest,right_answer=answer)
                return render(request,'Quizz/questions.html',{'question':question,'category':category,'session_id':session_id})
        else:
            quest=QuizQuestion.objects.get(id=question_id)
            user=session_id
            answer=request.POST['answer']
            UserSubmittedAnswer.objects.create(user=user,question=quest,right_answer=answer)

        if question:
            return render(request,'Quizz/questions.html',{'question':question,'category':category,'session_id':session_id})
        else:
            result=UserSubmittedAnswer.objects.filter(user=session_id)
            skipped=UserSubmittedAnswer.objects.filter(user=session_id,right_answer="Not Submitted").count()
            attempted=UserSubmittedAnswer.objects.filter(user=session_id).exclude(right_answer="Not Submitted").count()
            rightans=0
            percentage=0
            for i in result:
                if i.question.right_opt == i.right_answer:
                    rightans+=1
            percentage=(rightans*100)/attempted

            res=database.child("points").child(session_id).get().val()
            if res is not None:
                score= int(res["point"]) + int(rightans)
                data={'point':score}
                database.child("points").child(session_id).set(data)

            else:
                data={'point':rightans}
                database.child("points").child(session_id).set(data)
                    
            return render(request,'Quizz/result.html',{'result':result,'session_id':session_id,'total_skipped':skipped,'total_attempted':attempted,'rightans':rightans})

    else:
        return HttpResponse("method not allowed")

def result(request,category_id,session_id):
    result=UserSubmittedAnswer.objects.filter(user=session_id)
    skipped=UserSubmittedAnswer.objects.filter(user=session_id,right_answer="Not Submitted").count()
    attempted=UserSubmittedAnswer.objects.filter(user=session_id).exclude(right_answer="Not Submitted").count()
    rightans=0
    percentage=0
    if result is not None:
        for i in result:
            if i.question.right_opt == i.right_answer:
                rightans+=1
    percentage=(rightans*100)/attempted

    return render(request,'Quizz/result.html',{'result':result,'session_id':session_id,'total_skipped':skipped,'total_attempted':attempted,'rightans':rightans})

#alumni_quizz

def category_a(request,session_id):
    print("function called")
    category=Category.objects.all()
    print(category.values())
    creds=database.child("points").child(session_id).get('point').val()
    print(creds)
    
    context={'session_id':session_id,'category':category,'creds':creds}
    return render(request,"Quizz_A/category_a.html",context)

from datetime import timedelta
def category_questions_a(request,session_id,id):
    category=Category.objects.get(id=id)
    question=QuizQuestion.objects.filter(category=category).order_by('id').first()
    lastAttemp=None
    futureTime=None
    hoursLimit=24
    countAttempt=UserCategoryAttempts.objects.filter(user=session_id,category=category).count()  
    if countAttempt == 0:
        UserCategoryAttempts.objects.create(user=session_id,category=category)
    else:
        lastAttemp=UserCategoryAttempts.objects.filter(user=session_id,category=category).order_by('-id').first()
        futureTime = lastAttemp.attemt_time +  timedelta(hours=hoursLimit)

        if lastAttemp and lastAttemp.attemt_time < futureTime:
            return HttpResponse('you can submit')    
        else:
            UserCategoryAttempts.objects.create(user=session_id,category=category)
        

    
    context={'session_id':session_id,'question':question,'category':category,'lastAttemp':futureTime}
    return render(request,"Quizz_A/questions_a.html",context)

def submit_answer_a(request,category_id,question_id,session_id):
    if request.method == "POST":
        category=Category.objects.get(id=category_id)
        question=QuizQuestion.objects.filter(category=category,id__gt=question_id).exclude(id=question_id).order_by('id').first()
        if 'skip' in request.POST:
            if question:
                quest=QuizQuestion.objects.get(id=question_id)
                user=session_id
                answer='Not Submitted'
                UserSubmittedAnswer.objects.create(user=user,question=quest,right_answer=answer)
                return render(request,'Quizz_A/questions_a.html',{'question':question,'category':category,'session_id':session_id})
        else:
            quest=QuizQuestion.objects.get(id=question_id)
            user=session_id
            answer=request.POST['answer']
            UserSubmittedAnswer.objects.create(user=user,question=quest,right_answer=answer)

        if question:
            return render(request,'Quizz_A/questions_a.html',{'question':question,'category':category,'session_id':session_id})
        else:
            result=UserSubmittedAnswer.objects.filter(user=session_id)
            skipped=UserSubmittedAnswer.objects.filter(user=session_id,right_answer="Not Submitted").count()
            attempted=UserSubmittedAnswer.objects.filter(user=session_id).exclude(right_answer="Not Submitted").count()
            rightans=0
            percentage=0
            for i in result:
                if i.question.right_opt == i.right_answer:
                    rightans+=1
            percentage=(rightans*100)/attempted

            res=database.child("points").child(session_id).get().val()
            if res is not None:
                score= int(res["point"]) + int(rightans)
                data={'point':score}
                database.child("points").child(session_id).set(data)

            else:
                data={'point':rightans}
                database.child("points").child(session_id).set(data)
                    
            return render(request,'Quizz_A/result_a.html',{'result':result,'session_id':session_id,'total_skipped':skipped,'total_attempted':attempted,'rightans':rightans})

    else:
        return HttpResponse("method not allowed")

def result_a(request,category_id,session_id):
    result=UserSubmittedAnswer.objects.filter(user=session_id)
    skipped=UserSubmittedAnswer.objects.filter(user=session_id,right_answer="Not Submitted").count()
    attempted=UserSubmittedAnswer.objects.filter(user=session_id).exclude(right_answer="Not Submitted").count()
    
    rightans=0
    percentage=0
    if result is not None:
        for i in result:
            if i.question.right_opt == i.right_answer:
                rightans+=1
    percentage=(rightans*100)/attempted

    return render(request,'Quizz_A/result_a.html',{'result':result,'session_id':session_id,'total_skipped':skipped,'total_attempted':attempted,'rightans':rightans})


