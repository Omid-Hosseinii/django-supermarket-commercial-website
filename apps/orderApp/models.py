from django.db import models
from apps.accounts.models import Customer
from apps.product.models import Product
from django.utils import timezone
import uuid
import utils
#------------------------------------------------------------------------------

class Payment(models.Model):
    payment_title = models.CharField(max_length=50,verbose_name='نوع پرداخت')

    def __str__(self):
        return self.payment_title

    class Meta:
        verbose_name ='پرداخت'
        verbose_name_plural ='روش پرداخت'
        db_table ='t_payment'   
#------------------------------------------------------------------------------

class OrderState(models.Model):
    order_state_title=models.CharField(max_length=100,verbose_name='وضعیت سفارش')

    def __str__(self):
        return self.order_state_title

    class Meta:
        verbose_name ='وضعیت سفارش'
        verbose_name_plural ='وضعیت سفارش ها' 
        db_table ='t_order_state'   


#------------------------------------------------------------------------------

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='orders',verbose_name='مشتری')
    register_date=models.DateField(default=timezone.now,verbose_name='تاریخ درج')
    update_date=models.DateField(auto_now=True,verbose_name='تاریخ ویرایش')
    is_finaly=models.BooleanField(default=False,verbose_name='وضعیت سفارش')
    order_code=models.UUIDField(unique=True,verbose_name='کد تولیدی برای سفارش',default=uuid.uuid4,editable=True)
    discount=models.IntegerField(default=0,verbose_name='تخفیف روی فاکتور',null=True,blank=True)
    description=models.TextField(null=True,blank=True,verbose_name='توضیحات')
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,related_name='payment_types',
                              null=True,blank=True,default=None,verbose_name='نوع پرداخت')
    order_state=models.ForeignKey(OrderState,on_delete=models.CASCADE,related_name='order_state',verbose_name='وضعیت سفارش',null=True,blank=True)
    
    
    def get_order_total_price(self):
        sum=0
        for item in self.orders_detail1.all():
            sum+=item.product.get_price_by_discount()*item.qty
        final_price,delivery,tax=utils.get_price_delivery_tax(sum,self.discount)    
        return int(final_price*10)    
            
            
    def __str__(self):
        return f'{self.customer}\t{self.id}\t{self.is_finaly}'

    class Meta:
        verbose_name ='سفارش'
        verbose_name_plural ='سفارشات'
        db_table ='t_order'    

#------------------------------------------------------------------------------

class OrderDetail(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='orders_detail1',verbose_name='سفارش')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='orders_detail2',verbose_name='کالا')
    qty=models.PositiveIntegerField(default=1,verbose_name='تعداد')
    price=models.IntegerField(verbose_name='قیمت')

    def __str__(self):
        return f'{self.order}\t{self.product}\t{self.qty}\t{self.price}' 
     
    class Meta:
        verbose_name ='جزیئات سفارش'
        verbose_name_plural ='جزیئات سفارشات'
        db_table ='t_orderdetails'     
      
#------------------------------------------------------------------------------