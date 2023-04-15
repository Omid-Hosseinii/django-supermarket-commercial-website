from django.contrib import admin
from .models import Order,OrderDetail,OrderState
# Register your models here.


class OrderDetailInline(admin.TabularInline):
    model=OrderDetail
    extra=3

@admin.register(Order)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display=['id','customer','order_state','register_date','is_finaly','discount',]
    inlines=[OrderDetailInline]
    
@admin.register(OrderState)
class OrderStateAdmin(admin.ModelAdmin):
    list_display=['order_state_title',]
    