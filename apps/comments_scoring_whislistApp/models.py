from django.db import models
from apps.product.models import Product
from apps.accounts.models import CustomUser
from django.core.validators import MaxValueValidator,MinValueValidator
#------------------------------------------------------------------------------

class Comment(models.Model):
    product=models.ForeignKey(Product, related_name='comments_product',
                              on_delete=models.CASCADE,verbose_name='کالا')
    commenting_user=models.ForeignKey(CustomUser, related_name='comments_user1',
                                      on_delete=models.CASCADE,verbose_name='فرد نظر دهنده')
    approving_user=models.ForeignKey(CustomUser, related_name='comments_user2',
                                     on_delete=models.CASCADE,verbose_name='ادمین قبول نظر',
                                     null=True,blank=True)
    comment_text=models.TextField(verbose_name='نظر')
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت دیده شدن')
    comments_parent=models.ForeignKey('Comment' ,related_name='comment_child',
                                      on_delete=models.CASCADE,verbose_name='والد نظر',
                                      null=True,blank=True)

    def __str__(self):
        return   f"{self.product} - {self.commenting_user}"
    
    class Meta:
        verbose_name = "نظر"
        verbose_name_plural ="نظرات"
        db_table = "t_comment"

#------------------------------------------------------------------------------


class Scoring(models.Model):
    product=models.ForeignKey(Product,verbose_name='امتیاز دهی',
                              on_delete=models.CASCADE,related_name='scoring_product')
    scoring_user=models.ForeignKey(CustomUser,verbose_name='کاربر امتیاز دهنده',
                                   on_delete=models.CASCADE,related_name='scoring_user')
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج امتیاز')
    score=models.PositiveSmallIntegerField(verbose_name='امتیاز',
                                           validators=[MinValueValidator(0),MaxValueValidator(5)])

    def __str__(self):
        return   f"{self.product} - {self.scoring_user}"

    class Meta:
        verbose_name = "امتیاز"
        verbose_name_plural ="امتیازات"
        db_table = "t_scoring"   
        
        
        
        
         
#------------------------------------------------------------------------------


class Favorite(models.Model):
    product=models.ForeignKey(Product,verbose_name='محصول مورد علاقه',
                              on_delete=models.CASCADE,related_name='favorite_product')
    favorite_user=models.ForeignKey(CustomUser,verbose_name='کاربر',
                                    on_delete=models.CASCADE,related_name='favorite_user')
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج محصول مورد علاقه')

    def __str__(self):
        return   f"{self.product} - {self.favorite_user}"

    class Meta:
        verbose_name = "علاقه"
        verbose_name_plural ="علاقه مندی ها"
        db_table = "t_favorite"    
    
    
    
    