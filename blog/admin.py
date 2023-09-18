from django.contrib import admin
from .models import Tag, Blog, Feedback
# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    ordering = ('id',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'tag')
    list_display_links = ('title',)
    ordering = ('-id',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'animal')
    list_display_links = ('title',)
    ordering = ('-id',)

