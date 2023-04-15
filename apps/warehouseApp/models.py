from django.db import models
from apps.accounts.models import CustomUser
from apps.product.models import Product
#------------------------------------------------------------------------------

class WarehouseType(models.Model):
    warehouse_type_title=models.CharField(max_length=50,verbose_name='نوع انبار')

    def __str__(self):
        return self.warehouse_type_title

    class Meta:
        verbose_name = "نوع انبار"
        verbose_name_plural ="نوع انبار ها"
        db_table = "t_warehouse_type"
        
#--------------------------------------------------------------------------------


class Warehouse(models.Model):
    warehouse_type=models.ForeignKey(WarehouseType, related_name="warehouse",
                                     verbose_name="انبار",on_delete=models.CASCADE)        
    user_registered=models.ForeignKey(CustomUser, related_name="warehouse_user_registered",
                                      verbose_name="کاربر ثبت کننده",on_delete=models.CASCADE)        
    product=models.ForeignKey(Product, related_name="warehouse_product",
                              verbose_name="محصول",on_delete=models.CASCADE)   
    qty=models.IntegerField(verbose_name='تعداد')     
    price=models.IntegerField(verbose_name='قیمت',null=True,blank=True)  
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')    

    def __str__(self):
        return f"{self.warehouse_type} - {self.product}"
    
    
    class Meta:
        verbose_name = "انبار"
        verbose_name_plural ="انبار ها"
        db_table = "t_warehouse"

#--------------------------------------------------------------------------------


