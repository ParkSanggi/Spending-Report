from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import signup

app_name = 'account'

urlpatterns =[
    path('signin/', LoginView.as_view(template_name='account/signin.html'), name='signin'),
    path('signout/', LogoutView.as_view(template_name='account/signout.html'), name='signout'),
    path('signup/', signup, name='signup'),
]