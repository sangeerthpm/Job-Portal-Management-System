from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .form import *
# Create your views here.
from .form import CommentForm
from .models import *
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

def Registerpage(request):
    if request.method=='POST':
        form= Registerform(request.POST)
        if form.is_valid():
            a=form.save()
            UserProfile.objects.create(user=a)
            send_mail(f'Welcome {a.username}','Welcome to Job Portal',settings.EMAIL_HOST_USER, [a.email])
            return redirect(loginpage)
    else:
        form = Registerform()
    return render(request,'register.html',{'form':form})

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            if user.is_superuser:
                return redirect(Adminpage)
            elif user.is_staff:
                return redirect(staff_user)
            else:
                messages.success(request,'user authenticated successfully')
                return redirect(home)
        else:
            print("No such user")
    return render(request,'login.html')

def logoutpage(request):
    logout(request)
    return redirect(loginpage)

def staff_user(request):
    return render(request,'staff.html')
def home(request):
    return render(request,'home.html')
def Adminpage(request):
    return render(request,'admin.html')

def home1(request):
    return render(request,'home1.html')

@login_required
def poster(request):
        if request.method == 'POST':
            form = postform(request.POST,request.FILES)
            if form.is_valid():
                form.save()
            return render(request,'newpost.html')
        else:
            form = postform()
        return render(request, 'post.html',{'form': form})

@login_required
def displaypost(request):
        posts=Post.objects.all()
        form = CommentForm()
        return render(request, "allpost.html", {"posts": posts, "form": form})


def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes += 1
    post.save()
    return redirect("all_posts")

# Add comment
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    return redirect("all_posts")

# Share post (just give link)
def share_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    url = request.build_absolute_uri(f"/post/{pk}/")
    return HttpResponse(f"🔗 Share this link: {url}")

# Single post detail (useful for share link)
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    return render(request, "post_detail.html", {"post": post,"form":form})




# Staff: Add Job Posting
@login_required
def add_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user  # set the staff user
            job.save()
            return redirect("job_list")
    else:
        form = JobForm()
    return render(request, "add_job.html", {"form": form})


# Show all Jobs
def job_list(request):
    jobs = Job.objects.all()
    return render(request, "job_list.html", {"jobs": jobs})


# User: Apply for Job
@login_required
def apply_job(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.save()
            return redirect("apply_success")
    else:
        form = ApplicationForm()
    return render(request, "apply_job.html", {"form": form})


def apply_success(request):
    return render(request, "apply_success.html")

def allrequests(request):
    if request.user.is_staff:
        # Show pending applications for jobs posted by this staff
        requests = Application.objects.filter(status='pending', job__posted_by=request.user)
    else:
        # Show user's own pending applications
        requests = Application.objects.filter(status='pending', applicant=request.user)
    return render(request,'allrequest.html',{'request':requests})

def profilepage(request):
    usr = request.user
    pro = UserProfile.objects.get(user=usr)
    return render(request,'profile.html',{'pro':pro})

def profileedit(request):
    pro=UserProfile.objects.get(user=request.user)
    if request.method=='POST':
        form=userprofileform(request.POST,request.FILES,instance=pro)
        if form.is_valid():
            form.save()
            return redirect(profilepage)
    else:
        form=userprofileform(instance=pro)
    return render(request,'editprofile.html',{'form':form})




def accept(request,bid):
    book=Application.objects.get(id=bid)
    book.status ='approved'
    book.save()
    send_mail(f'Dear {book.applicant}',f'Your appointment for job application  has been accepted,\n'
               ,settings.EMAIL_HOST_USER, [book.email])
    return redirect(allrequests)


def reject(request,bid):
    book=Application.objects.get(id=bid)
    book.status ='rejected'
    book.save()
    send_mail(f'Dear {book.applicant}',f'Your appointment for job application  has been rejected\n',settings.EMAIL_HOST_USER, [book.email])
    return redirect(allrequests)

def accepted(request):
    accepted_booking=Application.objects.filter(status='approved',applicant=request.user)
    return render(request,'accepted.html',{'bookings':accepted_booking})