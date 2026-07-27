from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user=models.CharField(User,null=True,blank=True)
    Address=models.TextField(null=True,blank=True)
    Email=models.EmailField(null=True,blank=True)
    Phone_number=models.IntegerField(null=True,blank=True)
    Education=models.CharField(max_length=100)
    Coures=models.CharField(null=True,blank=True)
    Description=models.TextField(null=True,blank=True)
    Date_of_birth=models.DateField(null=True,blank=True)
    Hobbies=models.CharField(null=True,blank=True)
    
    def __str__(self):
        return self.user.username

class Post(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    des=models.CharField(max_length=100)
    img=models.ImageField(upload_to='uploads/',null=True, blank=True)    
    likes = models.IntegerField(default=0)   # like counter

    def _str_(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()

    def _str_(self):
        return f"{self.post.name} - {self.text[:30]}"




# Company Model
class Company(models.Model):
    name = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name


# Job Posting (created by staff)
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs",null=True)
    position = models.CharField(max_length=100,null=True)
    education = models.CharField(max_length=100,null=True)
    salary = models.IntegerField(null=True)
    description = models.TextField(null=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.position} at {self.company.name}"


# Job Application (created by normal user)
class Application(models.Model):
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('rejected','Rejected')
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications",null=True)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)  # link to logged-in user
    full_name = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15,null=True)
    resume = models.FileField(upload_to="resumes/",null=True)
    status=models.CharField(max_length=10,choices=  STATUS_CHOICES,default='pending')
    def __str__(self):
        return f"{self.full_name} applied for {self.job.position} at {self.job.company.name}"