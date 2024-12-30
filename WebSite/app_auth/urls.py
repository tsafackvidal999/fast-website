from django.urls import path,include
from . import views

urlpatterns=[
    
    path('login',views.login_blog,name='login_blog'),
    path('login/',views.login_blog,name='login_blog'),
    path('register',views.register,name='register'),
    path('logout',views.logout_blog,name='logout_blog'),
]


