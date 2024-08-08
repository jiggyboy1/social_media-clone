from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import Post,Like
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    posts = Post.objects.all().order_by('-create_at')
    
    context = {"posts":posts}
    return render(request,'home.html',context)

def post_detail(request,post_id):
    post = Post.objects.get(id=post_id)

    context = {"post":post}
    return render(request,'post.html',context)

def like_detail(request,like_post):
    user = request.user
    post = Post.objects.get(id=like_post)
    current_like = post.likes
    liked = Like.objects.filter(user=user,post=post).count()

    if not liked:
        liked = Like.objects.create(user=user,post=post)
        current_like = current_like + 1
    else:
        liked = Like.objects.filter(user=user,post=post).delete()
        current_like = current_like - 1

    post.likes = current_like
    post.save()
    return HttpResponseRedirect(reverse('post_detail',args=[like_post]))

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password,)
        if user is not None:
            login(request,user)
            return redirect('home')

    return render(request,'login.html',)

def logout_user(request):
    logout(request)
    messages.success(request,'You have logged out')
    return redirect('home')
    
def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)

    context = {'form':form}
    return render(request,'register.html',context)

def profile_user(request,user_id):
    user = User.objects.get(id=user_id)


    context = {}
    return render(request,'profile.html',context)