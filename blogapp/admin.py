from django.contrib import admin
from .models import Post, Question, Answer, Category, FeaturedBlog0, FeaturedBlog1, FeaturedBlog2,FeaturedBlog3,FeaturedBlog4,FeaturedBlog5

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'author__username')
    readonly_fields = ('created_at', 'updated_at')

    # Include delete_image in the form fields
    fields = (
        'title', 'content', 'short_description', 'image', 'delete_image',
        'author', 'category', 'keywords', 'status', 'created_at', 'updated_at'
    )
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'author__username')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'created_at')
    search_fields = ('question__title', 'author__username')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Post, PostAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(FeaturedBlog0)
admin.site.register(FeaturedBlog1)
admin.site.register(FeaturedBlog2)
admin.site.register(FeaturedBlog3)
admin.site.register(FeaturedBlog4)
admin.site.register(FeaturedBlog5)
