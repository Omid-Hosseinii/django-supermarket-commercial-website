from django.db import models
from utils import UploadFile    ### custom class for upload files
from django.utils import timezone
from django.urls import reverse
from datetime import datetime
from django.db.models import Sum,Avg
# from middlewares.middlewares import RequesMiddleware
#--------------------------------------------------------------------------------------------------------------------------------

class Brand(models.Model):
    brand_title = models.CharField(max_length=100,verbose_name='برند کالا')
    file_upload=UploadFile('images','brand')
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر گروه کالا')
    slug=models.SlugField(max_length=200,verbose_name='عنوان لاتین',null=True)

    def __str__(self):
        return self.brand_title

    class Meta:
        verbose_name ='برند'
        verbose_name_plural ='برند ها'
        db_table ='t_brand'
#------------------------------------------------------------------------------

class ProductGroup(models.Model):
    group_title = models.CharField(max_length=100,verbose_name='عنوان گروه کالا')
    file_upload=UploadFile('images','product_group')
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر گروه کالا')
    description=models.TextField(blank=True,null=True,verbose_name='توضحیات گروه کالا')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت فعال/غیرفعال')
    group_parent=models.ForeignKey('ProductGroup',on_delete=models.CASCADE,null=True,blank=True,verbose_name='والد گروه کالا',related_name='groups')
    slug=models.SlugField(max_length=200,verbose_name='عنوان لاتین',null=True)
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    register_published=models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')  
    register_update=models.DateTimeField(auto_now=True,verbose_name='تاریخ آخرین به روز رسانی')    
   

    
    def __str__(self):
        return self.group_title

    class Meta:
        verbose_name ='گروه کالا'
        verbose_name_plural ='گروه کالا ها'
        db_table ='t_productgroup'
        
#------------------------------------------------------------------------------


class Feature(models.Model):
    feature_name= models.CharField(max_length=100,verbose_name='نام ویژگی')
    product_group=models.ManyToManyField(ProductGroup,verbose_name='گروه کالا',related_name='features_of_groups')
    
    def __str__(self):
        return self.feature_name

    class Meta:
        verbose_name ='ویژگی کالا'
        verbose_name_plural ='ویژگی کالا ها'
        db_table ='t_feature'

#------------------------------------------------------------------------------

###============================================================================================================================================
class Product(models.Model):
    product_name= models.CharField(max_length=500,verbose_name='نام کالا')
    short_text= models.TextField(default="",verbose_name='خلاصه توضیحات',null=True,blank=True)
    
    description=RichTextUploadingField(blank=True,null=True,verbose_name='توضحیات کالا')
    file_upload=UploadFile('images','products')
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر کالا')  
    price=models.PositiveIntegerField(default=0,verbose_name='قیمت')
    product_group=models.ManyToManyField(ProductGroup,verbose_name='گروه کالا',related_name='products_of_group')
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,verbose_name='برند کالا',null=True,blank=True,related_name='brands')
    is_active=models.BooleanField(default=True,blank=True,verbose_name='وضعیت فعال/غیرفعال')
    slug=models.SlugField(max_length=200,verbose_name='عنوان لاتین',null=True)
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    register_published=models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')  
    register_update=models.DateTimeField(auto_now=True,verbose_name='تاریخ آخرین به روز رسانی')
    
    ### write custom class to make 3rd table for feature and product     
    feature=models.ManyToManyField(Feature,through='ProductFeature')


    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name ='کالا'
        verbose_name_plural ='کالا ها'
        db_table ='t_product'
    
    #_______________________________________________________________________________________________
    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug':self.slug})
    
    
    #_______________________________________________________________________________________________
    def get_price_by_discount(self):
        list1=[]
        for dbd in self.discount_basket_details2.all():
            if (dbd.discount_basket.is_active==True and 
                dbd.discount_basket.start_date <= datetime.now() and 
                datetime.now() <= dbd.discount_basket.end_date):
                
                list1.append(dbd.discount_basket.discount)
        discount=0
        if (len(list1)>0):
            discount=max(list1)   
        return round(self.price - (self.price*discount/100))         
            

    #_______________________________________________________________________________________________
    def get_number_in_warehouse(self):
        sum1=self.warehouse_product.filter(warehouse_type=1).aggregate(Sum('qty'))
        sum2=self.warehouse_product.filter(warehouse_type=2).aggregate(Sum('qty'))
        
        input=0
        if sum1['qty__sum']!=None:
            input=sum1['qty__sum']
            
        output=0    
        if sum2['qty__sum']!=None:
            output=sum2['qty__sum']
            
        return input-output    
    #_______________________________________________________________________________________________
    def get_avg_scores(self):
        avg_score=self.scoring_product.all().aggregate(Avg('score'))['score__avg']      
        if avg_score==None:
            avg_score=0
        return  ("%.2f" % avg_score)   
    #_______________________________________________________________________________________________
    def get_score_user(self):
        request=RequesMiddleware(get_response=None)
        request=request.thread_local.current_request
        score=0
        score_user=self.scoring_product.filter(scoring_user=request.user)
        if score_user.count()>0:
            score=score_user[0].score
        return score    
    #_______________________________________________________________________________________________
    
    
    
    def get_user_favorites(self):
        request=RequesMiddleware(get_response=None)
        request=request.thread_local.current_request
        
        flag=self.favorite_product.filter(favorite_user=request.user).exists()
        return flag
    #_______________________________________________________________________________________________
    
    
    
    def GetMainProductGroups(self):
        return self.product_group.all()[0].id

###============================================================================================================================================








