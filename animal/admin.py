from django.contrib import admin
from .models import Animal, AnimalMedia, Sex, Schedule, AnimalType, Feedback


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('id','name','type','sex','age','breed','availability','description','healthy')
    list_display_links = ('id',)
    ordering = ('id',)

@admin.register(AnimalMedia)
class AnimalMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'animal', 'media_link', 'main')
    list_display_links = ('id',)
    ordering = ('id',)

@admin.register(Sex)
class SexAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    ordering = ('id',)

@admin.register(AnimalType)
class AnimalTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    ordering = ('id',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time','end_time','animal','user',)
    list_display_links = ('id',)
    ordering = ('id',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'animal')
    list_display_links = ('title',)
    ordering = ('-id',)
