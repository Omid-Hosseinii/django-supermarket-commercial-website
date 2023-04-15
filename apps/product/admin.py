from django.contrib import admin
from .models import Brand,ProductGroup,Product,ProductFeature,Feature,ProductGallery,FeatureValue
from django.db.models.aggregates import Count
from django.contrib.admin.actions import delete_selected
from django.http import HttpResponse
from django.core import serializers
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description,order_field
#--------------------------------------------------------------------------------------------------------------------------------

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display=('brand_title',)
    list_filter=('brand_title',)
    search_fields=('brand_title',)
    ordering=('brand_title',)

#-----------------------------------------------------------------

class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model=ProductGroup
    extra=1
#*******************************************    
    
def deactive_product_group(modeladmin,request,queryset):
    result=queryset.update(is_active=False)
    message=f'.تعداد {result} رکورد برا شما غیر فعال شد'   
    modeladmin.message_user(request,message) 
#*******************************************    
def active_product_group(modeladmin,request,queryset):
    result=queryset.update(is_active=True)
    message=f'.تعداد {result} رکورد برا شما فعال شد'   
    modeladmin.message_user(request,message) 
#*******************************************
def export_json(modeladmin,request,queryset):
    response=HttpResponse(content_type='application/json')
    serializers.serialize("json",queryset,stream=response)
    return response
#*******************************************
class GroupFilter(SimpleListFilter):
    title = "گروه محصولات"
    parameter_name='group'
    
    def lookups(self,request,model_admin):
        sub_group=ProductGroup.objects.filter(~Q(group_parent=None))
        groups=set([item.group_parent for item in sub_group])
        return [(item.id , item.group_title) for item in groups]
    
    def queryset(self,request,queryset):
        if self.value()!=None:
            return queryset.filter(Q(group_parent=self.value()))
        return queryset
    
    
#____________________________________________________________________________  

@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display=('group_title','is_active','group_parent','register_date',
                  'register_update','count_sub_group','count_of_product')
    list_filter=(('group_title',DropdownFilter),('group_parent',DropdownFilter),GroupFilter,)
    search_fields=('group_title',)
    ordering=('group_parent','group_title')
    inlines=[ProductGroupInstanceInlineAdmin]
    actions=[deactive_product_group,active_product_group,export_json]
    list_editable=['is_active']
    
    def get_queryset(self,*args, **kwargs):
        qs=super(ProductGroupAdmin,self).get_queryset(*args,**kwargs)
        ## add column for count group parent for ech fields
        qs=qs.annotate(sub_group=Count('groups'))
        ## add column for count product parent for ech fields
        qs=qs.annotate(product_of_group=Count('products_of_group'))
        return qs
    
    ## write getter for column count group parent ech fields and then write method name in list_display
    def count_sub_group(self,obj):
        return obj.sub_group
    
    @short_description('تعداد کالا های گروه')
    @order_field('products_of_group')
    def count_of_product(self,obj):
        return obj.product_of_group
    
    
    
    delete_selected.short_description='حذف'
    count_sub_group.short_description='تعداد زیر گروه ها'
    deactive_product_group.short_description='غیر فعال'
    active_product_group.short_description='فعال'
    export_json.short_description='خروجی جیسون'

    
#-----------------------------------------------------------------

class ProductFeatureInstanceInlineAdmin(admin.TabularInline):
    model=ProductFeature
    extra=3
    
    class Media:
        css={
            'all':('css/admin_style.css',)
        }
       
        js=('https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/admin_scripts.js',)
#*******************************************    

class ProductInstanceInlineAdmin(admin.TabularInline):
    model=ProductGallery
    extra=3
#*******************************************    
    
def deactive_product(modeladmin,request,queryset):
    result=queryset.update(is_active=False)
    message=f'.تعداد {result} رکورد برا شما غیر فعال شد'   
    modeladmin.message_user(request,message) 
#*******************************************    
def active_product(modeladmin,request,queryset):
    result=queryset.update(is_active=True)
    message=f'.تعداد {result} رکورد برا شما فعال شد'   
    modeladmin.message_user(request,message) 
#*******************************************



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','brand','is_active','register_update','display_product_groups')
    list_filter=('brand','product_group')
    search_fields=('product_name',)
    ordering=('register_update','product_name') 
    inlines=[ProductFeatureInstanceInlineAdmin,ProductInstanceInlineAdmin]   
    actions=[deactive_product,active_product]
    list_editable=['is_active']
    
    def display_product_groups(self,obj):
       return ", ".join([group.group_title for group in obj.product_group.all()]) 
    
    def formfield_for_manytomany(self,db_field,request,**kwargs):  
        if db_field.name=='product_group':
            kwargs["queryset"]=ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field,request,**kwargs)    
    
    fieldsets=(
        ('اطلاعات محصول',{'fields':(
            ('product_name','image_name',),
            ('product_group','is_active'),
            ('brand','slug'),
            'price',
            'short_text',
            'description',
            )}),
        ('تاریخ و زمان',{'fields':(
            'register_published',
            )}),
    )
    
    
    deactive_product.short_description='غیر فعال'
    active_product.short_description='فعال'
    display_product_groups.short_description='گروه محصول'

#-----------------------------------------------------------------

class FeatureValueInstanceInline(admin.TabularInline):
    model = FeatureValue
    extra=5


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display=('feature_name','display_group','display_feature_value')
    list_filter=('feature_name',)
    search_fields=('feature_name',)
    ordering=('feature_name',)   
    inlines=[FeatureValueInstanceInline,]
    

    
    def formfield_for_manytomany(self,db_field,request,**kwargs):  
        if db_field.name=='product_group':
            kwargs["queryset"]=ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field,request,**kwargs)     
    
    
    def display_group(self,obj):
        return ", ".join([group.group_title for group in obj.product_group.all()])
    
    def display_feature_value(self,obj):
        value=", ".join([feature_value.value_title for feature_value in obj.feature_value.all()])
        if value:
            return value
        else:
            return 'تعریف نشده است'
    
    display_group.short_description='گروه های دارای این ویژگی'
    display_feature_value.short_description='مقادیر ممکن برای این ویژگی'

#-----------------------------------------------------------------

#-----------------------------------------------------------------