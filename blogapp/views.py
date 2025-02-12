# blog/views.py
from django.shortcuts import render, redirect,get_object_or_404,HttpResponse 
from .forms import PostForm
from .models import Post
from .models import datauser
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.conf import settings

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # Redirect to post list view after saving
    else:
        form = PostForm()
    
    return render(request, 'create_post.html', {'form': form})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

def loginpage(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username = username, password = pass1 )

        if user is not None:
            login(request, user)
            fname = user.first_name 
            return redirect('post_list')
        else:
            messages.error(request,"wrong passwords")
            return redirect('/')
    
    return render(request, 'loginpage.html')

def registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        pass1 = request.POST.get('pass1')
        email = request.POST.get('email')
        pass2 = request.POST.get('pass2')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.error(request,"username already exists")
            return redirect('/registration/')
        else:
            user = User.objects.create_user(username = username, email = email,password = pass1)
            user.save()
            messages.success(request,"account succesfully created")
            return redirect('/')
    
    return render(request, 'registration.html')

def signout(request):
    logout(request)
    return redirect('loginpage.html')

