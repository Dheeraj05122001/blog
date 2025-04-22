# blog/views.py
from django.shortcuts import render, redirect,get_object_or_404,HttpResponse 
from .forms import PostForm,QuestionForm,AnswerForm,CategoryForm
from .models import Post,Question,Answer, Category
from .models import datauser
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from django.http import HttpResponseForbidden


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.author = request.user  # assuming you track authors
            form.save()
            return redirect('post_list')  # Redirect to post list view after saving
    else:
        form = PostForm()
    
    return render(request, 'create_post.html', {'form': form})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def user_profile(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    user_data = datauser.objects.filter(user=user_obj).first()

    blogs = Post.objects.filter(author=user_id)
    questions = Question.objects.filter(author = user_obj)
    answers = Answer.objects.filter(author=user_obj)

    return render(request, 'user_profile.html', {
        'profile_user': user_obj,
        'user_data': user_data,
        'blogs': blogs,
        'questions': questions,
        'answers': answers,
    })

def post_list(request):
    category_id = request.GET.get('category')  # get category ID from dropdown
    categories = Category.objects.all()

    if category_id:
        posts = Post.objects.filter(category_id=category_id)
    else:
        posts = Post.objects.all()

    return render(request, 'post_list.html', {
        'posts': posts,
        'categories': categories,
        'selected_category_id': int(category_id) if category_id else None,
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_details.html', {'post': post})

def loginpage(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['password']

        user = authenticate(username = username, password = pass1 )

        if user is not None:
            login(request, user)
            fname = user.first_name 
            return redirect('homepage')
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
            return render(request,'registration.html')
    
    return render(request, 'registration.html')

def signout(request):
    logout(request)
    return redirect('loginpage.html')


def homepage(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()

    if category_id:
        posts = Post.objects.filter(category_id=category_id).order_by('-created_at')[:5]
    else:
        posts = Post.objects.all().order_by('-created_at')[:5]

    questions = Question.objects.all().order_by('-created_at')[:3]  # Latest 3 questions

    return render(request, 'base.html', {
        'posts': posts,
        'categories': categories,
        'selected_category_id': int(category_id) if category_id else None,
        'questions': questions,  # pass to template
    })

def question_list(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'question_list.html', {'questions': questions})

def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all()
    form = AnswerForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to answer.")
        
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', question_id=question.id)

    return render(request, 'question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form,
    })

def ask_question(request): 
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to ask a question.")

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm()

    return render(request, 'ask_question.html', {'form': form})

def create_category(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Only logged-in users can create categories.")

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'create_category.html', {'form': form})

def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category)
    return render(request, 'posts_by_category.html', {
        'category': category,
        'posts': posts
    })
