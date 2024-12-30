from django.urls import path,include
from . import views

urlpatterns=[
    
    path('',views.home_index,name='home_index'),
    path('article/<int:id_article>/',views.article,name='article'),
    path('article/<str:chaine>/',views.article_introuvable,name='article_introuvable'),
    path('article/',views.article_introuvable,name='article_introuvable'),
    path('article/recherche',views.search,name="search"),
    path('sms',views.sms,name="sms"),
    #path('download',views.download,name="download _page"),
    path('auth/',include("app_auth.urls")),
    path('downloads/', views.page_telechargement, name='downloads'),
    path('download/<int:fichier_id>/', views.telecharger_fichier, name='download'),
    path('Affiliation/', views.affilliation, name='Affiliation'),
    path('condictions_d_affilliation/', views.condictions_d_affilliation, name='condictions_d_affilliation'),
    path("contact_us", views.contact_us,name = 'contact_us')


]


