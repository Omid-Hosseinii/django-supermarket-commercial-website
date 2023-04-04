from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
#------------------------------------------------------------------------------

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('',include('apps.main.urls',namespace='main')),
    path('accounts/',include('apps.accounts.urls',namespace='accounts')),
    path('products/',include('apps.product.urls',namespace='products')),
    path('ckeditor',include('ckeditor_uploader.urls')),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.site_header='پنل مدیریت'
admin.site.index_title='به پنل مدیریت خوش آمدید'