from django import forms
from django.forms import ModelForm
from .models import CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
#------------------------------------------------------------------------------


class UserCreationForm(forms.ModelForm):
    password1= forms.CharField(label='password',widget=forms.PasswordInput)
    password2= forms.CharField(label='Repassword',widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields=['mobile_number','email','name','family','gender']
        
    def clean_password2(self):
        pass1=self.cleaned_data['password1']    
        pass2=self.cleaned_data['password2']    
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('تکرار رمز عبور صحیح نمی باشد')
        return pass2
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user 
    

class UserChangeForm(forms.ModelForm):  
    password=ReadOnlyPasswordHashField(help_text="برای تغیر رمز عبور <a href='../password'>اینجا</a> کلیک کنید.")
    class Meta:
        model=CustomUser
        fields=['mobile_number','password','email','name','family','gender','is_active','is_admin']
        
#------------------------------------------------------------------------------
        
class RegisterUserForm(forms.ModelForm):
    password1=forms.CharField(label='رمز عبور',
                              widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                }))             
    password2=forms.CharField(label='تکرار رمز عبور',
                              widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                })) 
    class Meta:
        model=CustomUser
        fields=['mobile_number']
        widgets={
            'mobile_number':forms.TextInput(attrs={'class': 'form-control',
                                                   })}
    
    def clean_password2(self):
        pass1=self.cleaned_data['password1']                
        pass2=self.cleaned_data['password2']                
        if pass1 and pass2 and pass1!=pass2:
            raise ValidationError('رمز عبر و تکرار آن یکسان نمی باشد')
        return pass2
    
#------------------------------------------------------------------------------
    
class VerifyRegisterForm(forms.Form):
    active_code=forms.CharField(label='کد فعالسازی',
                                error_messages={'required':'این فیلد نمی تواند خالی باشد'}
                                ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد فعال سازی را وارد کنید'}))    

#------------------------------------------------------------------------------

class LoginUserForm(forms.Form):
    mobile_number=forms.CharField(label='شماره موبایل',
                                  error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                                  widget=forms.TextInput(attrs={
                                      'class':'form-control',
                                      'autofocus':""
                                  }))
    password=forms.CharField(label='رمز عبور',
                                  error_messages={'required':'این فیلد نمی تواند خالی باشد'},
                                  widget=forms.PasswordInput(attrs={
                                      'class':'form-control',
                                  }))
#------------------------------------------------------------------------------
    
class RemmemberedPasswordForm(forms.Form):
    mobile_number = forms.CharField(
        label='شماره موبایل',
        error_messages={'required':'این فیلد باید پر شود'},
        widget=forms.TextInput(attrs={'class':'form-control',
                                      'placeholder':'شماره موبایل را وارد کنید'},))    

#------------------------------------------------------------------------------

class ChangePasswordForm(forms.Form):
    password1=forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'رمز عبور را وارد کنید'
        }))
    
    password2=forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'تکرار رمز عبور را وارد کنید'
        }))
    
    def clean_password2(self):
        pass1=self.cleaned_data['password1']
        pass2=self.cleaned_data['password2']
        if pass1 and pass2 and pass1!=pass2:
            raise ValidationError('رمز عبور و تکرار آن باهم مغاییرت دارد')
        return pass2
    
#------------------------------------------------------------------------------

class UserPanelUpdateForm(forms.Form):
    mobile_number = forms.CharField(
        label='شماره موبایل',
        error_messages={'required':'این فیلد نمی تواند خالی باشد'},
        widget=forms.TextInput(attrs={'class':'form-control',
                                      'readonly': 'readonly',}))
    name = forms.CharField(
        label='نام',
        error_messages={'required':'این فیلد نمی تواند خالی باشد'},
        widget=forms.TextInput(attrs={'class':'form-control',
                                      'placeholder':'نام خود را وارد کنید',})) 
    family = forms.CharField(
        label='نام خانوادگی',
        error_messages={'required':'این فیلد نمی تواند خالی باشد'},
        widget=forms.TextInput(attrs={'class':'form-control',
                                      'placeholder':'نام خانوادگی را وارد کنید',}))    
    email = forms.CharField(
        label='ایمیل',
        error_messages={'required':'این فیلد نمی تواند خالی باشد'},
        widget=forms.EmailInput(attrs={'class':'form-control',
                                      'placeholder':'آدرس ایمیل را وارد کنید',}))
    phone_number = forms.CharField(
        label='تلفن',
        error_messages={'required':'این فیلد نمی تواند خالی باشد'},
        widget=forms.TextInput(attrs={'class':'form-control',
                                      'placeholder':'شماره موبایل را وارد کنید',}))
    address = forms.CharField(
        label='آدرس',
        error_messages={'required':'این فیلد نمی تواند خالی باشد'},
        widget=forms.Textarea(attrs={'class':'form-control',
                                      'placeholder':'آدرس را وارد کنید',}))
    image = forms.ImageField(label="عکس پروفایل",required=False)


























