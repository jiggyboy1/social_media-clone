from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import Post,Like
from django.urls import reverse
# Create your views here.

def home(request):
    posts = Post.objects.all().order_by('-create_at')
    
    context = {"posts":posts}
    return render(request,'home.html',context)

