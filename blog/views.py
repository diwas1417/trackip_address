from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import loginform, signupform,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group

# Create your views here.
def home(request):
    posts=Post.objects.all()

    return render(request,'blog/home.html',{'posts':posts})

def about(request):
    return render(request,'blog/about.html')

def contact(request):
    return render(request,'blog/contact.html')        

def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user=request.user
        full_name=user.get_full_name()
        gps=user.groups.all()
        id=request.session.get('ip',0)
        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,'gps':gps,'id':id}) 
    else:
        return HttpResponseRedirect('/login/')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm=loginform(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'la moj gara')
                    return HttpResponseRedirect('/dashboard/')
        else:                
            fm=loginform()
        return render(request,'blog/login.html',{'form':fm}) 
    else:
        return HttpResponseRedirect('/dashboard/')


def user_signup(request):
    if request.method=="POST":
        fm=signupform(request.POST)
        if fm.is_valid():
            messages.success(request,'la badai xa hai')
            user=fm.save()
            group=Group.objects.get(name='auther')
            user.groups.add(group)
    else:        
     fm=signupform()
    
    return render(request,'blog/signup.html',{'form':fm})     

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def addpost(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            fm=PostForm(request.POST)
            if fm.is_valid():
                title=fm.cleaned_data['title']
                desc=fm.cleaned_data['desc']
                pst=Post(title=title,desc=desc)
                pst.save()
                fm=PostForm()
        else:
            fm=PostForm()
        return render(request,'blog/post.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')


def updatepost(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=id)
            fm=PostForm(request.POST,instance=pi)
            if fm.is_valid():
                fm.save()
        else:
            pi=Post.objects.get(pk=id)
            fm=PostForm(instance=pi)

        return render(request,'blog/updatepost.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')        


def deletepost(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=id)
            pi.delete()

        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')                