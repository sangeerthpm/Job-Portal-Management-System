from django import forms
from .models import *
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Registerform(UserCreationForm):
    class Meta:
        model =User
        fields=['username','email']
        
class userprofileform(forms.ModelForm):
    class Meta:
        model =UserProfile
        exclude=['user']

class postform(forms.ModelForm):
    class Meta:
        model=Post
        fields=['name','des','img']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets={
            "text":forms.TextInput(attrs={"placeholder":"Comment"})
        }

from django import forms
from .models import Job, Application


# Staff Form to add Job Postings
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['company', 'position', 'education', 'salary', 'description']


# User Form to apply for Job
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['job', 'full_name', 'email', 'phone_number', 'resume']