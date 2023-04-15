from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views import View
from .models import Author,ArticleGroup,Article,ArticleGallery
import os
from django.conf import settings

#--------------------------------------------------------------------------------


class ArticleView(ListView):
    model=Article
    template_name="article_app/blog.html"
    context_object_name="artciles"
    queryset=Article.objects.filter(is_active=True)


    
def last_article(request,*args,**kwargs):
    Articles=Article.objects.filter(is_active=True).order_by('-register_date')[:2]
    context={
        'articles':Articles,
    } 
    return render(request,'article_app/partials/last_articles.html',context)  
    
#--------------------------------------------------------------------------------

class ArtcileDetailView(View):
    def get(self,request,*args, **kwargs):
        article=Article.objects.get(slug=kwargs['slug'])
        if os.path.exists(settings.MEDIA_ROOT+'article_images/article_'+str(article.id)):
            image_list=os.listdir(settings.MEDIA_ROOT+'article_images/article_'+str(article.id))
        else:
            image_list=''   
        article_author=Article.objects.get(id=article.id).author.through.objects.filter(article_id=article.id)
        author=[Author.objects.get(id=author.author_id) for author in article_author]
        
        
        context={
            'article':article,
            'authors':author,
            'image_list':image_list,
            'article_title':article.title,
            
            
        }
        return render(request,'article_app/article_detail.html',context)
    
#--------------------------------------------------------------------------------



