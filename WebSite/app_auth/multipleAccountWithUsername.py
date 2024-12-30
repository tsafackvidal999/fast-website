from .models import User
from time import time_ns
from django.contrib.auth.hashers import check_password

def  search_the_user(small_username,pwd):
    
    if type(small_username) != str:
        raise ValueError(f"la valeur {small_username} n'est pas un string")
    
    if type(pwd) != str:
        raise ValueError(f"la valeur {pwd} n'est pas un string")
    
    users= User.objects.filter(username__contains = small_username)
    for user in users:
        #format du username  vidal|1733083118243114   (small_username|timespam)
        if user.username.split('|')[0]==small_username and check_password(pwd, user.password  ):
            return user.username, pwd
    return small_username,pwd

def create_unique_username(small_username):
    if type(small_username) != str:
        raise ValueError(f"la valeur {small_username} n'est pas un string")
    return f'{small_username}|{time_ns()}'

def clean_username(big_username):
    
    if type(big_username) != str:
        raise ValueError(f"la valeur {big_username} n'est pas un string")
    return str(big_username.split('|')[0])

def check_if_the_user_exist_before_creation(small_username:str ,pwd:str):    
    if type(small_username) != str:
        raise ValueError(f"la valeur {small_username} n'est pas un string")
    
    if type(pwd) != str:
        raise ValueError(f"la valeur {pwd} n'est pas un string")
    
    users= User.objects.filter(username__contains = small_username)
    for user in users:
        #format du username  vidal|1733083118243114   (small_username|timespam)
        if user.username.split('|')[0] == small_username and check_password(pwd, user.password):
            return True
    return False

    

