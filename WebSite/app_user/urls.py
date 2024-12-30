from django.urls import path,include
from . import views

urlpatterns=[
    
    path('',views.dashboard,name='user_dashboard'),
    path('retrait_commission_affillie',views.retrait_commission_affillie,name='retrait_commission_affillie'),
    path('mes_articles',views.user_articles,name='user_articles'),

]


