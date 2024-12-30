from django.urls import path,include
from . import views

urlpatterns=[
    
    path('',views.activation_index,name='activation_index'),
    path('get_activation',views.get_activation,name='get_activation'),
    path('confirme_quote_before_init_payement', views.confirme_quote_before_init_payement, name='confirme_quote_before_init_payement'),
    path('init_payement', views.init_payement, name='init_payement'),
    path('check_ativation',views.check_ativation,name="check_ativation"),


]


