from django.db import models
from app_auth.models import User

# Create your models here.
class Article(models.Model):
    
    title=models.CharField(max_length=80)
    body=models.TextField()
    autor=models.CharField(max_length=100)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Cathegorie(models.Model):
    name=models.CharField(max_length=150)

    def __str__(self):
        return self.name


class MyArticle(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    cathegorie=models.ForeignKey(Cathegorie,on_delete=models.CASCADE)
    title=models.CharField(max_length=80)
    desc=models.TextField()
    image=models.ImageField(upload_to="static/img")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    nombre_de_vue=models.IntegerField()

    def __str__(self):
        return self.title
    

class Telechargement(models.Model):
    #nom_fichier = models.CharField(max_length=255)
    user= models.ForeignKey(User, on_delete= models.CASCADE, null=True)
    cathegorie=models.ForeignKey(Cathegorie,on_delete=models.CASCADE)
    title=models.CharField(max_length=80)
    desc=models.TextField()
    my_file = models.FileField(upload_to='static/download/files')
    logo = models.ImageField(upload_to='static/download/logos',default='static/download/logos/default logo.ico')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    #path_file = models.FilePathField(default='aaaa')
    nombre_de_techargement = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.my_file)
    

class MyAffilliates(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    code_affillie = models.CharField(max_length=30,unique=True)
    number_of_free_days = models.PositiveSmallIntegerField(default=0)
    solde = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f'{self.user.username}  >>  {self.code_affillie}  >>  {self.solde}'



class ContactUs (models.Model):
    user= models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    name = models.CharField(max_length=150,)
    phone_number = models.PositiveIntegerField(null=True)
    message = models.TextField(null=True)