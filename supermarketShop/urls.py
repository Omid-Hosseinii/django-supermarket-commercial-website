from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from apps.main.views import navbar_links
#------------------------------------------------------------------------------

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('',include('apps.main.urls',namespace='main')),
    path('accounts/',include('apps.accounts.urls',namespace='accounts')),
    path('product/',include('apps.product.urls',namespace='products')),
    path('ckeditor',include('ckeditor_uploader.urls')),
    path('blog/', include('apps.article.urls',namespace='article',),),
    path('csw/',include('apps.comments_scoring_whislistApp.urls',namespace='csws')),
    path('search/',include('apps.searchApp.urls',namespace='search_app')),
    path('order/',include('apps.orderApp.urls',namespace='orders')),
    path('discount/',include('apps.discountsApp.urls',namespace='discounts')),
    path('payments/',include('apps.paymentApp.urls',namespace='payments')),
    path('warehouse/',include('apps.warehouseApp.urls',namespace='warehouse')),
    path('navbar_links/',navbar_links,name='navbar_links'),
    


    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.site_header='پنل مدیریت'
admin.site.index_title='به پنل مدیریت خوش آمدید'