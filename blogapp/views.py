# blog/views.py
from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from .forms import PostForm,QuestionForm,AnswerForm,CategoryForm
from .models import Post,Question,Answer, Category,FeaturedBlog0,FeaturedBlog1,FeaturedBlog2,FeaturedBlog3,FeaturedBlog4,FeaturedBlog5
from .models import datauser, EmailOTP
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseForbidden,JsonResponse
from django.db.models import Max,F,Q,Count
from django.db.models.functions import Coalesce
from random import sample
import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import json


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.author = request.user  # Track the author
            form.instance.status = 'pending'    # Set status to pending
            form.save()
            messages.info(request, "Your blog has been submitted and is pending admin approval.")
            return redirect('homepage')
    else:
        form = PostForm()
    
    return render(request, 'create_post.html', {'form': form})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def post_list(request):
    filter_type = request.GET.get('filter')
    category_id = request.GET.get('category')  # get category ID from dropdown
    categories = Category.objects.all()
    featured_blog0 = FeaturedBlog0.objects.first()
    featured_blog1 = FeaturedBlog1.objects.first()
    featured_blog2 = FeaturedBlog2.objects.first()
    featured_blog3 = FeaturedBlog3.objects.first()
    featured_blog4 = FeaturedBlog4.objects.first()
    featured_blog5 = FeaturedBlog5.objects.first()

    top_blog_titles = Post.objects.filter(status='approved').order_by('-views_count')[:10]

    all_approved_questions = list(Question.objects.filter(status='approved'))
    random_questions = sample(all_approved_questions, min(5, len(all_approved_questions)))

    
    if category_id:
        posts = Post.objects.filter(category_id=category_id, status='approved').order_by('-created_at')
    elif filter_type == "most_viewed":
        posts = Post.objects.filter(status='approved').order_by('-views_count', '-created_at')
    else:
        posts = Post.objects.filter(status='approved').order_by('-created_at')
    

    return render(request, 'post_list.html', {
        'posts': posts,
        'categories': categories,
        'selected_category_id': int(category_id) if category_id else None,
        'featured_blog0': featured_blog0,
        'featured_blog1': featured_blog1,
        'featured_blog2': featured_blog2,
        'featured_blog3': featured_blog3,
        'featured_blog4': featured_blog4,
        'featured_blog5': featured_blog5,
        'top_blog_titles': top_blog_titles,
        'random_questions': random_questions,
        
    })


def post_detail(request, pk):

    filter_type = request.GET.get('filter')
    post = get_object_or_404(Post, pk=pk)
    categories = Category.objects.all()  # Fetch categories from DB

    top_blog_titles = Post.objects.filter(status='approved').order_by('-views_count')[:5]

    approved_posts = list(Post.objects.filter(status='approved').exclude(pk=post.pk))
    random_blogs = random.sample(approved_posts, min(10, len(approved_posts)))

    all_approved_questions = list(Question.objects.filter(status='approved'))
    random_questions = sample(all_approved_questions, min(5, len(all_approved_questions)))

    if filter_type == "most_viewed":
        posts = Post.objects.filter(status='approved').order_by('-views_count', '-created_at')

    post.views_count +=1
    post.save( update_fields=['views_count'])

    return render(request, 'post_details.html', {'post': post,'top_blog_titles': top_blog_titles,'random_questions': random_questions,'categories': categories,'random_blogs': random_blogs})

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
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        entered_otp = request.POST.get('otp')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('/registration/')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('/registration/')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('/registration/')

        # check if OTP was sent
        otp_qs = EmailOTP.objects.filter(email=email)
        if not otp_qs.exists():
            messages.error(request, "Please request an OTP first.")
            return redirect('/registration/')

        otp_obj = otp_qs.first()

        # check expiry
        time_diff = timezone.now() - otp_obj.created_at
        if time_diff > timedelta(minutes=2):
            otp_obj.delete()
            messages.error(request, "OTP expired. Please request a new one.")
            return redirect('/registration/')

        if otp_obj.otp != entered_otp:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('/registration/')

        # All good → create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=pass1
        )
        user.first_name = first_name
        user.save()

        otp_obj.delete()

        messages.success(request, "Account created successfully.")
        return redirect('/')  # adjust if your login URL differs

    return render(request, 'registration.html')

def send_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")

        if not email:
            return JsonResponse({"success": False, "message": "Email is required."})

        otp = str(random.randint(100000, 999999))

        # Save or update OTP
        EmailOTP.objects.update_or_create(
            email=email,
            defaults={
                "otp": otp,
                "created_at": timezone.now()
            }
        )

        # Send email
        send_mail(
            subject='Your OTP Code',
            message=f'Your OTP is {otp}',
            from_email='dheerajchauhanjodi@gmail.com',  # replace with your real email
            recipient_list=[email],
            fail_silently=False,
        )

        # try:
        #     send_mail(
        #         subject='Your OTP Code',
        #         message=f'Your OTP is {otp}',
        #         from_email='dheerajchauhanjodi@gmail.com',
        #         recipient_list=[email],
        #         fail_silently=False,
        #     )
        # except Exception as e:
        #     return JsonResponse({
        #         "success": False,
        #         "message": f"Failed to send email: {str(e)}"
        #     })

        return JsonResponse({
            "success": True,
            "message": f"OTP sent to {email}."
        })

    return JsonResponse({"success": False, "message": "Invalid request method."})

def signout(request):
    logout(request)
    return redirect('loginpage.html')


def homepage(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    featured_blog0 = FeaturedBlog0.objects.first()
    featured_blog1 = FeaturedBlog1.objects.first()
    featured_blog2 = FeaturedBlog2.objects.first()
    featured_blog3 = FeaturedBlog3.objects.first()
    featured_blog4 = FeaturedBlog4.objects.first()
    featured_blog5 = FeaturedBlog5.objects.first()

    # news_category = Category.objects.filter(name__iexact='News').first()
    news_posts = Post.objects.filter(status='approved', category__name__iexact='News').order_by('-created_at')[:6]

    top_blog_titles = Post.objects.filter(status='approved').order_by('-views_count')[:10]        

    # news_posts = Post.objects.filter(category=news_category) if news_category else []

    if category_id:
        posts = Post.objects.filter(category_id=category_id, status='approved').order_by('-created_at')[:5]
    else:
        posts = Post.objects.filter(status='approved').order_by('-created_at')[:6]
    

    questions = Question.objects.filter(status='approved') \
                .annotate(answer_count=Count('answers', filter=Q(answers__status='approved'))) \
                .order_by('-created_at')[:6]

    all_approved_questions = list(Question.objects.filter(status='approved'))
    random_questions = sample(all_approved_questions, min(5, len(all_approved_questions)))




    return render(request, 'base.html', {
        'posts': posts,
        'categories': categories,
        'selected_category_id': int(category_id) if category_id else None,
        'questions': questions,  # pass to template
        'featured_blog0': featured_blog0,
        'featured_blog1': featured_blog1,
        'featured_blog2': featured_blog2,
        'featured_blog3': featured_blog3,
        'featured_blog4': featured_blog4,
        'featured_blog5': featured_blog5,
        'news_posts': news_posts,
        'top_blog_titles': top_blog_titles,
        'random_questions': random_questions,

    })

def question_list(request):
    filter_type = request.GET.get('filter')
    # questions = Question.objects.filter(status='approved').order_by('-created_at')
    categories = Category.objects.all()  # Fetch categories from DB

    all_approved_questions = list(Question.objects.filter(status='approved'))
    random_questions = sample(all_approved_questions, min(5, len(all_approved_questions)))

    top_blog_titles = Post.objects.filter(status='approved').order_by('-views_count')[:10]        

    if filter_type == "unanswered":
        questions = Question.objects.filter(status='approved', answers__isnull=True).distinct().order_by('-created_at')
    elif filter_type == "most_viewed":
        questions = Question.objects.filter(status='approved').order_by('-views_count')[:10]
    else:
        questions = Question.objects.filter(
            status='approved',
            answers__status='approved'
        ).annotate(
            latest_activity=Max(
                'answers__created_at',
                filter=Q(answers__status='approved')
            ),
        total_answers=Count(
                'answers',
                filter=Q(answers__status='approved'),
                distinct=True
            )
        ).order_by('-latest_activity').distinct()
    
    return render(request, 'question_list.html', {
        'questions': questions,
        'categories': categories,
        'random_questions': random_questions,
        'top_blog_titles': top_blog_titles,
    })



def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id,status='approved')
    answers = question.answers.filter(status='approved')
    categories = Category.objects.all()  # Fetch categories from DB

    total_answers = answers.count()

    top_blog_titles = Post.objects.filter(status='approved').order_by('-views_count')[:10]
    
    all_approved_questions = list(Question.objects.filter(status='approved'))
    random_questions = sample(all_approved_questions, min(5, len(all_approved_questions)))
    
    form = AnswerForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to answer.")
        
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.status = 'pending'
            answer.save()
            messages.info(request, "Your answer has been submitted and is pending admin approval.")
            return redirect('question_detail', question_id=question.id)
    
    question.views_count +=1
    question.save( update_fields=['views_count'])

    return render(request, 'question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form,
        'categories': categories,
        'total_answers': total_answers,
        'top_blog_titles': top_blog_titles,
        'random_questions': random_questions,
    })

def ask_question(request): 
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to ask a question.")

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.status = 'pending'  # Set status to pending
            question.save()
            messages.info(request, "Your question has been submitted and is pending for the approval by the admin.")
            return redirect('homepage')
    else:
        form = QuestionForm()

    return HttpResponseBadRequest("Invalid request")

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


def user_profile(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)

    if request.user != user_obj:
        return redirect('home')
    
    user_data = datauser.objects.filter(user=user_obj).first()
    categories = Category.objects.all()  # Fetch categories from DB

    blogs = Post.objects.filter(author=user_id)
    questions = Question.objects.filter(author = user_obj)
    answers = Answer.objects.filter(author=user_obj)

    if request.method == 'POST':
        username = request.POST.get('username')


        user_obj.username = username
        user_obj.save()

        return redirect('user_profile', user_id=user_id)


    return render(request, 'user_profile.html', {
        'profile_user': user_obj,
        'user_data': user_data,
        'blogs': blogs,
        'questions': questions,
        'answers': answers,
        'categories': categories,  # Add this line
    })

def post_search(request):
    query = request.GET.get('q')
    categories = Category.objects.all()
    top_blog_titles = Post.objects.filter(status='approved').order_by('-views_count')[:10]

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query),
            status='approved'
        ).order_by('-views_count')  # Prioritize popular results
    else:
        posts = Post.objects.none()  # Return nothing if query is empty

    return render(request, 'post_search_results.html', {
        'query': query,
        'posts': posts,
        'categories': categories,
        'top_blog_titles': top_blog_titles,
    })