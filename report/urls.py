from django.urls import path

from .views import mayCalendar, event_create, event_update, event_delete, day_detail

app_name = 'report'

urlpatterns = [
    path('', mayCalendar, name='calendar'),
    path('create/<int:day_number>/', event_create, name='create'),
    path('update/<int:event_id>', event_update, name='update'),
    path('delete/<int:event_id>', event_delete, name='delete'),
    path('detail/<int:day_number>/', day_detail, name='detail'),
]