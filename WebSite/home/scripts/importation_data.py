""" from blog.models import MyArticle

def run():
    id=MyArticle.objects.count()
    for i in range(id,id+20):
        article=MyArticle()
        article.title= "Article numero "+str(i)
        article.desc="ceci est la descrition de l'article numero " +str(i)
        article.image="static/img/default_image.jpg"
        article.save()

 """

from home.models import Telechargement
try:
    Telechargement.objects.create(nom_fichier='DS3231.zip')

except Exception as e:
    print("oupsss! echec de la creation du fichier")

else:
    print("operation reussie")