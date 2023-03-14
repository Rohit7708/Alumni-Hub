from socket import fromshare
from django import forms
from django.forms import ModelForm
from .models import *


class ChatMessageForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"class":"forms", "rows":3, "placeholder": "Type message here"}))
    class Meta:
        model = Message
        fields = ["body",]


class ImageForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['image','user_id']

        enctype='multipart/form-data'