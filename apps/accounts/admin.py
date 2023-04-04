from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm,UserChangeForm
from .models import CustomUser
#------------------------------------------------------------------------------


class CustomUserAdmin(UserAdmin):
    form=UserChangeForm
    add_form=UserCreationForm
    
    
    list_display=['mobile_number','email','name','family','gender','is_active','is_admin']
    list_filter=['is_active','is_admin','family']
    
    fieldsets=(
        (None,{'fields':('mobile_number','password')}),
        ('personal information',{'fields':('email','name','family','gender','active_code')}),
        ('permission',{'fields':('is_active','is_admin','is_superuser','user_permissions','groups')}),
    )
    
    add_fieldsets=(
        (None,{'fields':('mobile_number','email','name','family','gender','password1','password2',)}),
    )

    search_fields=('mobile_number',)
    ordering=('mobile_number',)
    filter_horizontal=('user_permissions','groups')
    
admin.site.register(CustomUser,CustomUserAdmin)    
#------------------------------------------------------------------------------










