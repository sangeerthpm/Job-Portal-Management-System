from django.urls import path
from . import views
from .views import *
urlpatterns=[
    path('home1',home1),
    path('post',poster,name="poster"),
    path("allpost/", views.displaypost, name="all_posts"),
    path("like/<int:pk>/", views.like_post, name="like_post"),
    path("comment/<int:pk>/", views.add_comment, name="add_comment"),
    path("share/<int:pk>/", views.share_post, name="share_post"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    
    path("login",loginpage,name='login'),
    path("register",Registerpage,name='register'),
    path("staff",staff_user),
    path("home",home,name='home'),
    path('admin',Adminpage),
    path('logout',logoutpage,name='logout'),
    path('profile',profilepage,name='profile'),
    path('edit',profileedit,name='edit'),

    path('addjob',add_job,name='addjob'),
    path('joblist',job_list,name="job_list"),
    path('apply_job',apply_job,name='apply_job'),
    path("apply_success",apply_success,name='apply_success'),
    path('allrequest',allrequests,name='allrequest'),

    
    path('accept/<int:bid>/',accept,name='accept'),
    path('reject/<int:bid>/',reject,name='reject'),
    path('accepted',accepted,name='accepted')
    

]