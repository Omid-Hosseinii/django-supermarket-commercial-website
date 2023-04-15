from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,ProductGroup,FeatureValue,Brand
from django.db.models import Q,Count,Min,Max
from django.views import View
from django.http import JsonResponse,HttpResponse
from .filters import ProductFilter
from django.core.paginator import Paginator
# from .compare import CompareProduct
#------------------------------------------------------------------------------------------------

def get_brand(request,*args,**kwargs):
    brands=Brand.objects.all()[:6]
    context={
        'brands':brands,
    } 
    return render(request,'product_app/partials/brand.html',context)


#------------------------------------------------------------------------------------------------
# return parent group
def get_root_groups():
    return ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))

#--------------------------------------------------------------------
### the cheapest products with parent groups for show in main page
def cheapest_products(request,*args,**kwargs):
    products=Product.objects.filter(is_active=True).order_by('price')[:4]
    # call parent group method
    product_group=get_root_groups()
    context={
        'products':products,
        'product_group':product_group,
    } 
    return render(request,'product_app/partials/cheapest_products.html',context)

#------------------------------------------------------------------------------------------------

def th_newest_products(request,*args,**kwargs):
    products=Product.objects.filter(is_active=True).order_by('-register_published')[:4]
    # call parent group method
    product_group=get_root_groups()
    context={
        'products':products,
        'product_group':product_group,
    } 
    return render(request,'product_app/partials/newes_products.html',context)

#---------------------------------------------------------------------------------------------------

### detail product

class ProductDetailView(View):
    def get(self, request,slug):
        product=get_object_or_404(Product,slug=slug)
        if product.is_active:
            return render(request,'product_app/product_detail.html',{'product':product})
        
#---------------------------------------------------------------------------------------------------

### popular groups show in main page

def popular_groups(request,*args,**kwargs): 
    sub_group=ProductGroup.objects.filter(~Q(group_parent=None))\
        .annotate(count=Count('products_of_group'))\
        .order_by('-count')[:8]
    groups=set([item.group_parent for item in sub_group])
    product_groups=[item.group_title for item in groups]
    # product_groups=ProductGroup.objects.filter(Q(is_active=True))\
    #     .annotate(count=Count('products_of_group'))\
    #     .order_by('-count')[:8]
        
    context={
        'product_groups':sub_group,
    }
    return render(request,'product_app/partials/popular_groups.html',context)

#---------------------------------------------------------------------------------------------------

def related_products(request,*args,**kwargs):
    current_product=get_object_or_404(Product,slug=kwargs['slug'])
    related_products=[]
    for group in current_product.product_group.all():
        related_products.extend(Product.objects.filter(Q(is_active=True) & Q(product_group=group) & ~Q(id=current_product.id)))
    return render(request,'product_app/partials/related_product.html',{'related_products':related_products}) 



#---------------------------------------------------------------------------------------------------
### dropdown ajax for featurevalue in adminpanel part add product
def get_filter_value_for_feature(request):
    
    if request.method == 'GET':
        feature_id=request.GET["feature_id"]
        feature_values=FeatureValue.objects.filter(feature_id=feature_id)
        res={fv.value_title:fv.id for fv in feature_values}
        
        ### another way to handle response
        # import json
        # json_stats = json.dumps(res)
        #return HttpResponse(json_stats,content_type='application/json')
        return JsonResponse(data=res,safe=False)  
#---------------------------------------------------------------------------------------------------
### get all product about ech product groups
class products_ech_groups(View):
    def get(self,request,*args,**kwargs):
        slug=kwargs['slug']
        current_group=get_object_or_404(ProductGroup,slug=slug)
        products=Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))
        
       
        ### price filter
        res_aggre=products.aggregate(min=Min('price'),max=Max('price')) ### price for min and max
        price_filter=ProductFilter(request.GET,queryset=products)
        products=price_filter.qs
        
        ### brand filter
        filter_brand=request.GET.getlist('brand')
        if filter_brand:
            products=products.filter(brand__id__in=filter_brand)
        
        ### features filter
        filter_features=request.GET.getlist('feature')
        if filter_features:
            products=products.filter(product_features__filter_value__id__in=filter_features).distinct()
        
        
        
        sort_type=request.GET.get('sort_type')
        if not sort_type:
            sort_type="0"
        elif sort_type=="1":
            products=products.order_by("price")
        elif sort_type=="2":        
            products=products.order_by("-price")
            
            
            
        select_show_product_number=request.GET.get('show_products')
        if not select_show_product_number:
            product_per_page=4
        else:
            product_per_page=int(select_show_product_number)
              
              
        group_slug=slug
        paginator=Paginator(products,product_per_page)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        product_count=products.count()
        
        show_count_product=[i for i in range(0,product_count,2) if i<=product_count+2 and i!=0] 
        
            
        
        
        context={
            'products':products,
            'current_group':current_group,
            'res_aggre':res_aggre,
            'group_slug':group_slug,
            'page_obj':page_obj,
            'product_count':product_count,
            'sort_type':sort_type,
            'price_filter':price_filter,
            'show_count_product':show_count_product,
            }
        
        return render(request,'product_app/products.html',context) 
#---------------------------------------------------------------------------------------------------

def filter_get_product_groups(request):
    product_groups=ProductGroup.objects.annotate(count=Count('products_of_group'))\
                                .filter(Q(is_active=True) & ~Q(count=0))\
                                .order_by('-count')
    return render(request,'product_app/partials/product_group.html',{'product_groups':product_groups,}) 

#---------------------------------------------------------------------------------------------------

### render_partial view for filter of brands :

def filter_get_product_brands(request,*args,**kwargs):
    current__group=get_object_or_404(ProductGroup, slug=kwargs['slug'])
    ### list of product include this current group , brand id values
    brand_list_id=current__group.products_of_group.filter(Q(is_active=True)).values('brand_id')
    
    brands=Brand.objects.filter(pk__in=brand_list_id)\
        .annotate(count=Count('brands'))\
        .filter(~Q(count=0))\
        .order_by('-count')    
 
    return render(request,'product_app/partials/filter_brands.html',{'brands':brands})  


#---------------------------------------------------------------------------------------------------

### render_partial view for filter of brands :

def filter_get_product_features(request,*args,**kwargs):
    current_group=get_object_or_404(ProductGroup, slug=kwargs['slug'])
    feature_list=current_group.features_of_groups.all()
    feature_dict=dict()
    for feature in feature_list:
        feature_dict[feature]=feature.feature_value.all() 
    return render(request,'product_app/partials/filter_features.html',{'feature_dict':feature_dict}) 
