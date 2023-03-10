from django.core.management.base import BaseCommand
import datetime
import pyrebase
import schedule
import time
from email.message import EmailMessage
import smtplib
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

def send_inactive_user_emails():
    now = datetime.datetime.now(datetime.timezone.utc)  # make now offset-aware with UTC timezone
    twenty_seconds_ago = now - datetime.timedelta(seconds=20)
    inactive_users = []
    result = database.child("last_login").get().val()
    for i in result.keys():
        last_time = result[i]['time']
        if last_time:
            last_login = datetime.datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S.%f%z").astimezone(datetime.timezone.utc)
            # make last_login offset-aware with UTC timezone
            if last_login < twenty_seconds_ago:
                inactive_users.append(i)

    # Send email to inactive users
    for user_id in inactive_users:
        # your email sending code here
       res=database.child("users").child(user_id).child("details").get().val()
       mail_id=res['pmeail']
       print(mail_id)
       EMAIL_ADDRESS='alumnihub.portal@gmail.com'
       EMAIL_PASSWORD='kiliblelhkqlpsqp'
       msg=EmailMessage()
       msg['subject']='We Miss You! Log in to our AlumniHub'
       msg['form']=EMAIL_ADDRESS
       msg['To']=mail_id
       msg.set_content('Dear [User],Its been a while since you last logged into our website, and we miss seeing you around! We hope everything is going well for you. We wanted to remind you that youre always welcome on our AlumniHub, where you can reconnect with old classmates, discover new opportunities, and stay up-to-date on the latest alumni news and events.So why not log in today and see whats new? Wed love to hear from you and catch up on everything thats been happening in your life. \n Best regards,[AlumniHub Team]')
       
       with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("msg sent")

# Schedule the task to run every minute
schedule.every(1).minutes.do(send_inactive_user_emails)

while True:
    schedule.run_pending()
    time.sleep(1)