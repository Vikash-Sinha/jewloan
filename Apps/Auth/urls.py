from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns=[
    # url(r'^register/$',views.register,name='register'),
    path('user-login/register',views.register,name='auth_register'),
    path('user-login/',views.user_login,name='user_login'),
]