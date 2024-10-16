from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from .models import Post,Like,Profile,Follow
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from .forms import RegisterForm,Postform,ProfileEdit
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    posts = Post.objects.all().order_by('-create_at')
    
    


    context = {"posts":posts,}
    return render(request,'home.html',context)

def post_detail(request,post_id):
    post = Post.objects.get(id=post_id)
    if request.user.is_authenticated:
        liked = Like.objects.filter(user=request.user,post=post)
    
        context = {"post":post,'liked':liked}
        return render(request,'post.html',context)
    else:
        context = {"post":post}
        return render(request,'post.html',context)

def delete_post(request,post_id):
    post_delete = Post.objects.get(id=post_id)
    
    if request.user.is_authenticated:
        if request.user == post_delete.user:
            if request.method == 'POST':
                post_delete.delete()
                return redirect('home')
            
            context = {"post":post_delete}
            return render(request,'delete.html',context)
        else:
            messages.error(request,"You aren't allowed here")
            return redirect('home')
        
    else:
        messages.error(request,"You must log in to preform any action")
        return redirect('home')
    
    

def like_detail(request,like_post):
    if request.user.is_authenticated:
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
    else:
        messages.success(request,'You cant like without log in')
        return redirect('home')

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

@login_required(login_url='login')
def profile_user(request,username):
    try:
        user = get_object_or_404(User,username=username)
        profile = Profile.objects.get(user=user)
        pic = user.post_set.all()
        following = Follow.objects.filter(follower=request.user,following=user)

    except :
        messages.success(request,'doesnt exist')
        return redirect('home')

    


    context = {'profile':profile,'pic':pic,'following':following}
    return render(request,'profile.html',context)

def editprofile(request,username):
    profile = User.objects.get(username=username)
    if profile == request.user:
        profiles = Profile.objects.get(user=profile)
        edit = ProfileEdit(instance=profiles)

        if request.method == "POST":
            edit = ProfileEdit(request.POST,request.FILES,instance=profiles)
            if edit.is_valid():
                edit.save()
                return redirect('profile')

        context = {'profile':profile,'edit':edit}
        return render(request,'editprofile.html',context)
    else:
        messages.success(request,'You aren'/'t allowed here')
        return redirect('home')

@login_required(login_url='login')
def upload(request):
    form = Postform()

    if request.method == 'POST':
        form = Postform(request.POST,request.FILES)
        if form.is_valid():
            forms = form.save(commit=False)
            forms.user = request.user
            forms.save()
        return redirect('home')



    context = {'form':form}
    return render(request,'upload_post.html',context)


def update_upload(request,post_id):
    post = Post.objects.get(id=post_id)
    if request.user.is_authenticated:
        if request.user == post.user :
            post = Post.objects.get(id=post_id)
            form = Postform(instance=post)

            if request.method == 'POST':
                form = Postform(request.POST,request.FILES,instance=post)
                if form.is_valid():
                    form.save()
                    return redirect('home')
    
            context = {'form':form}
            return render(request,'upload_post.html',context)
        else:
            messages.success(request,'you arent allowed here')
            return redirect('home')
    else:
        messages.error(request,"You must log in to preform any action")
        return redirect('home')

@login_required(login_url='login')
def follow_user(request,username):
    user_to_follow = get_object_or_404(User,username=username)

    if user_to_follow != request.user:
        Follow.objects.get_or_create(follower=request.user,following=user_to_follow)
        messages.success(request,'You have follow this user')
        return redirect('profile',username=user_to_follow)
    else:
        messages.success(request,"You can't follow yourself")
        return redirect('profile',username=user_to_follow)
    

@login_required(login_url='login')
def unfollow_user(request,username):
    user_to_unfollow = get_object_or_404(User,username=username)
    if user_to_unfollow != request.user:
        Follow.objects.filter(follower=request.user,following=user_to_unfollow).delete()
        messages.success(request,'You have unfollow this user')
        return redirect('profile',username=user_to_unfollow)
    else:
        messages.success(request,"You can't unfollow yourself")
        return redirect('profile',username=user_to_unfollow)


def search(request):
    if request.method == 'POST':
        searched = request.POST.get('search')
        user = User.objects.filter(Q(username__icontains=searched))

        if not searched:
            messages.success(request,'Please Type Something....')

        if not user :
            messages.success(request,'That Username Doesn\'t exist ')
            return render(request,'search.html' )
        

    context = {'searched':searched,'users':user}
    return render(request,'search.html',context )