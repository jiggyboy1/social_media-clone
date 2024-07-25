from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import Post,Like
from django.urls import reverse
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