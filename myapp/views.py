from django.shortcuts import render,redirect
import time
from datetime import datetime,timezone
import pytz
from django.utils import timezone
import uuid
import pyrebase
import smtplib
from email.message import EmailMessage
from django.http import JsonResponse,HttpResponse
import json

from .models import *


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
    result= database.child("users").child(session_id).child("details").get().val()
    print(result)
    if result is not None:
        message="your profile is being already created"
        return render(request,"welcome_msg.html",{'message':message,'session_id':session_id})
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


            data={'firstname':firstname,'roll':roll,'lastname':lastname,'phone':phone,'batch':batch,'pmeail':pemail,'oemail':oemail,'department':department,'workingat':workingat}
            database.child("users").child(session_id).child("details").set(data)

    context={'session_id':session_id}
    return render(request,'profile.html',context)

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
            data={'firstname':firstname,'roll':roll,'lastname':lastname,'phone':phone,'batch':batch,'pmeail':pemail,'oemail':oemail,'department':department,'workingat':workingat}
            database.child("users").child(session_id).child("details").set(data)

    context={'session_id':session_id,'details':result}
    return render(request,"update_profile.html",context)

def alumnilist(request,session_id):
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
        
    context={'session_id':session_id,'final':not_list}
    return render(request,"alumni_list.html",context)


def notification_detail_student(request,session_id,title,startdate,enddate,description,attachment):

    context={'session_id':session_id,'title':title,'startdate':startdate,'enddate':enddate,'description':description,'attachment':attachment}
    return render(request,"st_notification_detail.html",context)

def create_notification(request,session_id):
    

    return render(request,"st_event_notify.html")

def notification_history(request,session_id):
    mail_list=[]
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

        data={'title':title,'startdate':startdate,'enddate':enddate,'description':des,'attachment':att,'time':current_time,'date':today,'student_id':session_id,'notification_pushedby':"student",'session_id':session_id}
        database.child("event_notification").child(notification_id).child("details").set(data)

        result=database.child("users").get().val()
        for i in result.keys():
            if(result[i]['report']['role'] == "alumni"):
                mail_list.append(result[i]['details'])      

        for i in mail_list:
            EMAIL_ADDRESS='alumnihub.123@gmail.com'
            EMAIL_PASSWORD='veicbwofgzonpzih'
            msg=EmailMessage()
            msg['subject']='Event notification'
            msg['form']=EMAIL_ADDRESS
            msg['To']=i['pmeail']
            msg.set_content('Event notification has been posted. Kindly check your AlumniHub !')

            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
                smtp.send_message(msg)
                print("msg sent")

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
            if(my_notification[i]['details']['student_id']==session_id):
                my_list.append(my_notification[i]['details'])

    else:
        print("no notification")

    

    st_notificataion_list = sorted(st_notificataion_list,key= lambda x : x["date"], reverse=True)
    print("st_not")
    print(st_notificataion_list)

    not_list = sorted(not_list,key= lambda x : x["date"], reverse=True)
    print(not_list)

    my_list=sorted(my_list,key=lambda x: x["date"],reverse=True)
    print(my_list)

    


    context={'session_id':session_id,'not_list':not_list,'st_notification_list':st_notificataion_list,'my_list':my_list}
    return render(request,"notification_history.html",context)

def jobs(request,session_id):

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

    context={'session_id':session_id}
    return render(request,'alumni/alumni_mainpage.html',context)

def alumni_notification(request,session_id):
    mail_list=[]
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

        data={'title':title,'startdate':startdate,'enddate':enddate,'description':des,'attachment':att,'time':current_time,'date':today,'student_id':session_id,'notification_pushedby':"alumni",'session_id':session_id}
        database.child("event_notification").child(notification_id).child("details").set(data)

        result=database.child("users").get().val()
        for i in result.keys():
            if(result[i]['report']['role'] == "alumni"):
                mail_list.append(result[i]['details'])      

        for i in mail_list:
            EMAIL_ADDRESS='alumnihub.123@gmail.com'
            EMAIL_PASSWORD='veicbwofgzonpzih'
            msg=EmailMessage()
            msg['subject']='Event notification'
            msg['form']=EMAIL_ADDRESS
            msg['To']=i['pmeail']
            msg.set_content('Event notification has been posted. Kindly check your AlumniHub !')

            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
                smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
                smtp.send_message(msg)
                print("msg sent")

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
            if(my_notification[i]['details']['student_id']==session_id):
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


            data={'firstname':firstname,'roll':roll,'lastname':lastname,'phone':phone,'batch':batch,'pmeail':pemail,'oemail':oemail,'department':department,'workingat':workingat}
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
            data={'firstname':firstname,'roll':roll,'lastname':lastname,'phone':phone,'batch':batch,'pmeail':pemail,'oemail':oemail,'department':department,'workingat':workingat}
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
    mail_list=[]
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

        result=database.child("users").get().val()
        for i in result.keys():
            if(result[i]['report']['role'] == "student"):
                mail_list.append(result[i]['details'])      

        for i in mail_list:
            EMAIL_ADDRESS='alumnihub.123@gmail.com'
            EMAIL_PASSWORD='veicbwofgzonpzih'
            msg=EmailMessage()
            msg['subject']='Event notification'
            msg['form']=EMAIL_ADDRESS
            msg['To']=i['pmeail']
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
    
    if request.method=="POST":
        receiver=request.POST.get('rollnumber')
        if Room.objects.filter(name=receiver).exists():
            return redirect('chat',session_id,sender,receiver)
        else:
            new_room = Room.objects.create(name=receiver)
            new_room.save()
            print("new chat room created")
            return redirect('chat',session_id,sender,receiver)
            
    context={'session_id':session_id}
    return render(request,"chat/roll.html",context)

def chat(request,session_id,sender,receiver):
    
    
    

    # messages=[]

    # if request.method=="POST":
    #     text=request.POST.get('messagebox')
    #     now = datetime.now()
    #     current_time = now.strftime("%H:%M:%S")
    #     msg = {
    #         'text': text,
    #         'timestamp': time.time(),
    #         'sender': sender,
    #         'receiver': receiver,
    #         'session_id': session_id
    #     }
    #     database.child("messages").child(session_id).child(current_time).set(msg)        
    # msg = database.child("messages").child(session_id).get().val()
    # if msg is not None:
    #     for i in msg.keys():
    #         if msg[i]["sender"]==sender and msg[i]["receiver"]==receiver:
    #             messages.append(msg[i])

    # else:
    #     print("No")
    # messages = sorted(messages,key= lambda x : x["timestamp"],reverse=True)
    # print(messages)
    context={'session_id':session_id,'sender':sender,'receiver':receiver}
    return render(request,"chat/chat.html",context)

def send(request):
    username=request.POST.get('username')
    room_id=request.POST.get('room_id')
    message=request.POST.get('message')
    new_message = Message.objects.create(body=message, msg_sender=username, msg_reciver=room_id)
    new_message.save()

    return HttpResponse('Message sent successfully')

def getMessages(request,receiver,sender):
    room_details = Room.objects.get(name=receiver)
    room_detail = Room.objects.get(name=sender)
    print(room_detail)

    messages1 = Message.objects.filter(msg_reciver=receiver)
    messages2 = Message.objects.filter(msg_reciver=sender)

    message3 = Message.objects.filter(msg_sender=receiver)
    message4 = Message.objects.filter(msg_sender=sender)
    print(messages2)
    join_messages= messages1|messages2|message3|message4
    messages = join_messages.order_by('date')
    print(messages)

    return JsonResponse({"message":list(messages.values())})

def job_post(request):

    return render(request,"alumni/job_post.html"
    )


