from django.shortcuts import render,redirect
from django.views import View
from . forms import (RegisterUserForm,VerifyRegisterForm,
                     LoginUserForm,RemmemberedPasswordForm,
                     ChangePasswordForm,)
import utils
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
#----------------------------------------------------------------------------


class RegisterUserView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    template_name='accounts_app/register.html'
    def get(self, request, *args, **kwargs):
        form=RegisterUserForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            active_code=utils.create_random_code(5)
            
            CustomUser.objects.create_user(
                mobile_number=data['mobile_number'],
                active_code=active_code,
                password=data['password1'],)
         
            utils.send_sms(data['mobile_number'],f'کد فعال سازی شما {active_code} می باشد')
            request.session['user_session']={
                'active_code':str(active_code),
                'mobile_number':data['mobile_number'],
                'remmember_password':False
            }
            
            messages.success(request,'اطلاعات شما ثبت شد','success')
            return redirect('accounts:user_veryify_register')
        messages.error(request,'اطلاعات شما اشتباه می باشد','danger')
        return render(request,self.template_name,{'form':form})    
#----------------------------------------------------------------------------

class VerifyRegisterUserView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)  
    
      
    template_name = 'accounts_app/verify_register.html'
    def get(self, request, *args, **kwargs):
        form=VerifyRegisterForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form=VerifyRegisterForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session=request.session['user_session']
            if data['active_code']==user_session['active_code']:
                if user_session['remmember_password']==False:
                    user_database=CustomUser.objects.get(mobile_number=user_session['mobile_number'])
                    user_database.is_active=True
                    user_database.active_code=utils.create_random_code(5)
                    user_database.save()
                    messages.success(request,'ثبت نام شما با موفقیت انجام شد، به فِرِش مارکت خوش آمدید','success')
                    return redirect('main:index')
                else:
                    return redirect('accounts:change_password')  
            messages.error(request,'کد فعال سازی صحیح نمی باشد','danger')
            return render(request,self.template_name,{'form':form})
                  
        messages.error(request,'اطلاعات شما صحیح نمی باشد','danger')
        return render(request,self.template_name,{'form':form})    
        

class LoginUserView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)     
    
    template_name='accounts_app/login_user.html'
    def get(self, request, *args, **kwargs):
        form=LoginUserForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form=LoginUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            try:
                user=authenticate(username=data['mobile_number'],password=data['password'])
                user_database=CustomUser.objects.get(mobile_number=data['mobile_number'])
            except:
                messages.error(request,'نام کاربری یا رمز عبور صحیح نمی باشد','danger')
                return render(request,self.template_name,{'form':form})
                
            if user_database.is_active==True:
                if user_database.is_admin==True:
                    messages.warning(request,'کاربر ادمین از این بخش نمی تواند وارد شود','warning')
                    return render(request,self.template_name,{'form':form})
                else:
                    messages.success(request,'شما با موفقیت وارد سایت شدید','success')
                    try:
                        login(request,user)
                    except:
                        messages.error(request,'نام کاربری یا رمز عبور صحیح نمی باشد','danger')
                        return render(request,self.template_name,{'form':form})
                            
                    next_url=request.GET.get('next_url')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('main:index')
            
            messages.error(request,'حساب کاربری شما مسدود می باشد لطفا با پشتیبان تماس بگیرید','danger')            
            return render(request,self.template_name,{'form':form}) 
        
        messages.error(request,'اطلاعات شما اشتباه می باشد','danger')
        return render(request,self.template_name,{'form':form})   
    
#----------------------------------------------------------------------------

class LogoutUserView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request,*args, **kwargs):
        logout(request)
        return redirect('main:index')
    
#----------------------------------------------------------------------------

class RemmeberedPasswordView(View):
    template_name='accounts_app/remmbered_password.html'
    def get(self, request, *args, **kwargs):
        form=RemmemberedPasswordForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self, request, *args, **kwargs):
        form=RemmemberedPasswordForm(request.POST)
        if form.is_valid():
            try:
                data=form.cleaned_data
                user=CustomUser.objects.get(mobile_number=data['mobile_number'])
                active_code=utils.create_random_code(5)
                user.active_code=active_code
                user.save()
                utils.send_sms(data['mobile_number'],f'کد فعال سازی شما : {active_code} ')
                request.session['user_session']={
                    'active_code':str(active_code),
                    'mobile_number':data['mobile_number'],
                    'remmember_password':True
                }
                messages.success(request,'کد دریافتی را وارد کنید','success')
                return redirect('accounts:user_veryify_register')
            except:
                messages.error(request,'شماره موبایل وارد شده موجود نمی باشد','danger')
                
#----------------------------------------------------------------------------
    
class ChangePasswordView(View):
    template_name='accounts_app/change_password.html'
    def get(self, request,*args, **kwargs):
        form=ChangePasswordForm()
        return render(request,self.template_name,{'form':form}) 
    
    def post(self, request, *args, **kwargs):
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_session=request.session['user_session']
            user_database=CustomUser.objects.get(mobile_number=user_session['mobile_number'])
            user_database.set_password(data['password1'])
            user_database.active_code=utils.create_random_code(5)
            user_database.save()
            messages.success(request,'رمز عبور شما با موفقیت تغییر کرد','success')
            return redirect('accounts:user_login')
        messages.error(request,'ایرادی در اطلاعات وارد شده وجود دارد','danger')
        return render(request,self.template_name,{'form':form})