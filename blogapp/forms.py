# blog/forms.py
from django import forms
from .models import Post,Question,Answer,Category
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    class Meta:
        content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

        model = Post
        fields = ['title', 'content','short_description','keywords','image','category']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
                'style': 'padding: 8px 12px; border: 1px solid #ccc; border-radius: 5px;'
            }),
            'keywords': forms.TextInput(attrs={
                'placeholder': 'Enter at least 3 comma-separated keywords',
                'class': 'form-control'
            }),
            'short_description': forms.Textarea(attrs={
                'placeholder': 'Enter a short description for your blog',
                'class': 'form-control',
                'rows': 3
            })
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title','short_description','keywords']

    widgets ={
        'keywords' : forms.TextInput(attrs={
            'placeholder' : 'Enter at least 3 comma-separated keywords',
            'class' : 'form-control'
        }),
        'short_description' : forms.Textarea(attrs={
            'placeholder' : 'Enter a short description for your question',
            'class' : 'form-control',
            'rows' : 3
            })
    }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write your answer...'}),
            'class':'border-transparent'
        }
 
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name'})
        }
