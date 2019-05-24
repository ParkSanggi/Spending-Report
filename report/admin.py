from django.contrib import admin
from .models import Day, Category, Event

class DayOption(admin.ModelAdmin):
    list_display = ['m_day']

class CategoryOption(admin.ModelAdmin):
    list_display = ['name']

class EventOption(admin.ModelAdmin):
    list_display = ['f_day', 'category','description','expense','created']

admin.site.register(Day, DayOption)
admin.site.register(Category, CategoryOption)
admin.site.register(Event, EventOption)

