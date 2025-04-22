# blog/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.loginpage, name='loginpage'),
    path('homepage/',views.homepage,name='homepage'),
    path('postlist/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('registration/',views.registration,name='signuppage'),
    path('questionlist', views.question_list, name='question_list'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('ask/', views.ask_question, name='ask_question'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.create_category, name='create_category'),
    path('category/<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 