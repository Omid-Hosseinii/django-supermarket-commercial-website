from django.contrib import admin
from .models import *
from django_admin_listfilter_dropdown.filters import DropdownFilter

#------------------------------------------------------------------------------


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=['name','family','email','is_active','slug']
    list_filter=['family','is_active']
    list_editable=['is_active',]
    
#------------------------------------------------------------------------------

@admin.register(ArticleGroup)
class ArticleGroupAdmin(admin.ModelAdmin):
    list_display=['title']
    
#------------------------------------------------------------------------------

def active_article(modeladmin,request,queryset):
    result = queryset.update(is_active=True)
    message=f'تعداد {result} مقاله برای شما فعال شد.'
    modeladmin.message_user(request,message)

def deactive_article(modeladmin,request,queryset):
    result = queryset.update(is_active=False)
    message=f'تعداد {result} مقاله برای شما غیر فعال شد.'
    modeladmin.message_user(request,message)

### for add image blow of article model    
class ArticleGalleryInstanceInline(admin.TabularInline):
    model = ArticleGallery
    
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display=['group','title','main_image_name','key_words','register_date','is_active','view_number','slug']
    list_filter=(('title',DropdownFilter),'group','register_date','is_active',)
    inlines = [ArticleGalleryInstanceInline]
    list_editable = ['is_active',]
    actions=[active_article,deactive_article]
 
    active_article.short_description='فعال کردن مقاله های انتخابی'
    deactive_article.short_description='غیر فعال کردن مقاله های انتخابی'


#------------------------------------------------------------------------------
    
@admin.register(ArticleGallery)
class ArticleGalleryAdmin(admin.ModelAdmin):
    list_display=['image_name','article']
    list_filter=['article']