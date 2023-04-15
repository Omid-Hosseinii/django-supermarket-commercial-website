from django.shortcuts import render
from django.conf import settings
from apps.product.models import ProductGroup
from django.db.models import Q,Count,Min,Max
#----------------------------------------------------------------

def media_admin(request):
    return {'media_url':settings.MEDIA_URL}

def index(request):
    return render(request, 'main_app/main.html')

def about_us(request):
    return render(request, 'main_app/about_us.html')

def contact_us(request):
    return render(request, 'main_app/contact_us.html')


def navbar_links(request):
    parent=ProductGroup.objects.filter(Q(group_parent=None))
    all_group=ProductGroup.objects.all()
    product_groups_all=[(item.group_title,item.group_parent,item.slug) for item in all_group] 

    product_groups={item.group_title:[(i[0],i[2]) for i in product_groups_all if i[1]==item] for item in parent}  

    context={
            'product_groups':product_groups,
             }    
    
    return render(request, 'partials/main/navbar_links.html',context)