from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from utils import UploadFile
#------------------------------------------------------------------------------

class CustomUserManager(BaseUserManager):
    def create_user(self,mobile_number,email="",name="",family="",active_code=None,gender=None,password=None):
        if not mobile_number:
            raise ValueError('شماره موبایل باید وارد شود')
        
        user=self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,mobile_number,email,name,family,password=None,active_code=None,gender=None):
        user=self.create_user(
            mobile_number=mobile_number,
            email=email,
            name=name,
            family=family,
            password=password,
            active_code=active_code,
            gender=gender
        )
        user.is_active=True
        user.is_admin=True
        user.save(using=self._db)
        return user

#------------------------------------------------------------------------------
class CustomUser(AbstractBaseUser,PermissionsMixin):
    mobile_number=models.CharField(max_length=11,unique=True,verbose_name='شماره موبایل')
    email=models.EmailField(max_length=200,verbose_name='ایمیل',blank=True)
    name=models.CharField(max_length=50,blank=True,verbose_name='نام')
    family=models.CharField(max_length=50,blank=True,verbose_name='نام خانوادگی')
    CHOICES=(('True','مرد'),('False','زن'))
    gender=models.CharField(max_length=20,blank=True,null=True,choices=CHOICES,verbose_name='جنسیت')
    register_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ ثبت در سیستم')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت فعال/غیرفعال')
    active_code=models.CharField(max_length=100,null=True,blank=True,verbose_name='کد فعال سازی')
    is_admin=models.BooleanField(default=False,verbose_name='وضعیت ادمینی')
    
    
    USERNAME_FIELD = 'mobile_number'
    
    REQUIRED_FIELDS=['email','name','family']
    
    objects=CustomUserManager()
    
    def __str__(self):
        return self.name+" "+self.family
    
    @property
    def is_staff(self):
        return self.is_admin
#------------------------------------------------------------------------------

### defined model for customer 

class Customer(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)
    phone_number=models.CharField(max_length=11,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    file_upload=UploadFile('images','customer')
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر پروفایل',null=True,blank=True)    

    def __str__(self):
        return str(self.user.id)

    class Meta:
        verbose_name ='مشتری'
        verbose_name_plural ='مشتری ها'
        db_table ='t_customer'





