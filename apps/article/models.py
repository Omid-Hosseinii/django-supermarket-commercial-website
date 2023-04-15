from django.db import models
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from jalali_date import datetime2jalali, date2jalali
from django.db.models.signals import post_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os
from django.conf import settings
#-----------------------------------------------------------------------------------------

class Author(models.Model):
    name=models.CharField(max_length=50,verbose_name='نام')
    family=models.CharField(max_length=100,verbose_name='نام خانوادگی')
    email=models.EmailField(max_length=200,verbose_name='ایمیل',null=True,blank=True)
    is_active=models.BooleanField(default=False,verbose_name='وضعیت فعال/غیرفعال')
    slug=models.SlugField(max_length=300,verbose_name='هنوان لاتین',null=True,blank=True)
    
    def __str__(self):
        return self.name+" "+self.family
    
    class Meta:
        verbose_name='نویسنده'
        verbose_name_plural='نویسنده ها'
        db_table='t_blog_author'
        
#-----------------------------------------------------------------------------------------     
        
class ArticleGroup(models.Model):
    title=models.CharField(max_length=100,verbose_name='عنوان')  
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name='گروه مقاله'
        verbose_name_plural='گروه مقالات'
        db_table='t_article_group'      
        
#-----------------------------------------------------------------------------------------
        
def main_image_blog_path(instance,filename):
    ext=filename.split('.')[-1]
    name=filename.split('.')[0]
    current_date=datetime.utcnow().strftime('%Y%m%d%H%M%S')    
    return f'article_images/{name}-{current_date}.{ext}'

      

class Article(models.Model):
    group=models.ForeignKey(ArticleGroup,verbose_name='گروه مقاله',on_delete=models.CASCADE)      
    author=models.ManyToManyField(Author,verbose_name='نویسنده')
    title=models.CharField(max_length=400,verbose_name='عنوان مقاله')
    main_image_name=models.ImageField(upload_to=main_image_blog_path,verbose_name='تصویر عکس اصلی')
    short_text=models.TextField(verbose_name='متن خلاصه')
    text=RichTextUploadingField(verbose_name='متن اصلی')
    key_words=models.CharField(max_length=200,verbose_name='کلمات کلیدی',null=True,blank=True)
    register_date=models.DateField(auto_now_add=True,verbose_name='تاریخ درج مقاله')
    is_active=models.BooleanField(verbose_name='وضعیت فعال/غیرفعال')
    view_number=models.PositiveBigIntegerField(default=0,verbose_name='تعداد بازدید')
    slug=models.SlugField(max_length=200)  
      
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name='مقاله'
        verbose_name_plural='مقالات'
        db_table='t_article'      
        
    def get_jalali_date(self):
        return date2jalali(self.register_date) 


def delete_article_main_image(instance, **kwargs):
    if instance.main_image_name:
        os.remove(instance.main_image_name.path)

@receiver(post_delete, sender=Article)
def gallery_post_delete(sender, instance, **kwargs):
    delete_article_main_image(instance)    
    
    
@receiver(pre_save, sender=Article)
def delete_old_article_image(sender, instance, **kwargs):
    """
    A signal handler function to delete the old image file from the media
    directory when the `image` field of an `Article` instance is updated.
    """
    # Check if this is an update to an existing instance
    if instance.id:
        # Get the current instance from the database
        old_instance = Article.objects.get(id=instance.id)
        # Check if the `image` field of the old instance is being changed
        if old_instance.main_image_name != instance.main_image_name:
            # Delete the old image file associated with the `image` field
            if os.path.isfile(old_instance.main_image_name.path):
                os.remove(old_instance.main_image_name.path)          

  
      
#-----------------------------------------------------------------------------------------
      
def gallery_image_path(instance,filename):
    return f'article_images/article_{instance.article.id}/{filename}'       

class ArticleGallery(models.Model):
    image_name=models.ImageField(upload_to=gallery_image_path,verbose_name='تصویر')
    article=models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name='مقاله',related_name="image_article")
    
    def __str__(self):
        return str(self.image_name)
    
    class Meta:
        verbose_name='گالری مقاله'
        verbose_name_plural='گالری مقالات'
        db_table='t_article_gallery'


def calculate_file_size(path):
    size=0
    for path, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)    
    return size          
              
def delete_gallery_image(instance, **kwargs):
    if instance.image_name:
        os.remove(instance.image_name.path)

    media_dir_path = os.path.join(settings.MEDIA_ROOT,f'article_images/article_{instance.article.id}')
    size=calculate_file_size(media_dir_path)
    if size==0:
        os.rmdir(media_dir_path)
    
@receiver(post_delete, sender=ArticleGallery)
def gallery_post_delete(sender, instance, **kwargs):
    delete_gallery_image(instance)
    
@receiver(pre_save, sender=ArticleGallery)
def delete_old_article_gallery_image(sender, instance, **kwargs):
    """
    A signal handler function to delete the old image file from the media
    directory when the `image` field of an `Article` instance is updated.
    """
    # Check if this is an update to an existing instance
    if instance.id:
        # Get the current instance from the database
        old_instance = ArticleGallery.objects.get(id=instance.id)
        # Check if the `image` field of the old instance is being changed
        if old_instance.image_name != instance.image_name:
            # Delete the old image file associated with the `image` field
            if os.path.isfile(old_instance.image_name.path):
                os.remove(old_instance.image_name.path)     
    