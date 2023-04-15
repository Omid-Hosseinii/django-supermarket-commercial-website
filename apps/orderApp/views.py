from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .shop_cart import shopCart
from apps.product.models import Product
from django.http import HttpResponse
from apps.accounts.models import Customer
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order,OrderDetail,Payment
from .forms import OrderForm
from django.core.exceptions import ObjectDoesNotExist
from apps.discountsApp.forms import CouponForm
from django.db.models import Q
from apps.discountsApp.models import Coupons
from datetime import datetime
from django.contrib import messages
import utils
#----------------------------------------------------------------------------------

class shopCartView(View):
    def get(self, request,*args, **kwargs):
        shop_cart=shopCart(request)
        return render(request, 'order_app/order.html',{'shop_cart':shop_cart})
  
  
  
### for reload after delete from shop cart   
def show_shop_cart(request):
        shop_cart=shopCart(request)
        total_price_detail=shop_cart.calc_total_price()
        final_price,delivery,tax=utils.get_price_delivery_tax(total_price_detail)
        context={
            'shop_cart':shop_cart,
            'shop_cart_count':shop_cart.count,
            'total_price_detail':total_price_detail,
            'delivery':delivery, 
            'tax':tax,
            'final_price':final_price
        }
        return render(request, 'order_app/partials/show_shop_cart.html',context)     
    
    
    
def add_to_shop_cart(request):
    product_id=request.GET.get('product_id')
    qty=request.GET.get('qty')
    shop_cart=shopCart(request)
    product=get_object_or_404(Product,id=product_id)
    shop_cart.add_to_shop_cart(product,qty)
    return HttpResponse(shop_cart.count)
        
        
        
def delete_from_shop_cart(request):
    product_id=request.GET.get('product_id')        
    shop_cart=shopCart(request)
    product=get_object_or_404(Product,id=product_id)
    shop_cart.delete_from_shop_cart(product)
    return redirect('orders:show_shop_cart')   


def update_shop_cart(request):
    product_id_list=request.GET.getlist('product_id_list[]')
    qty_list=request.GET.getlist('qty_list[]')
    shop_cart=shopCart(request)
    shop_cart.update_shop_cart(product_id_list,qty_list)
    return redirect('orders:show_shop_cart')


def status_of_shop_cart(request):
    shop_cart=shopCart(request)
    return HttpResponse(shop_cart.count)   



#------------------------------------------------------------------------------------------------

class CreateOrderView(LoginRequiredMixin,View):
    def get(self, request):
        try:
            customer=Customer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            customer=Customer.objects.create(user=request.user)  
                    
        order=Order.objects.create(customer=customer,payment=get_object_or_404(Payment,id=1))    
        
        shop_cart=shopCart(request)
        for item in shop_cart:
            OrderDetail.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                qty=item['qty']

            )
        return redirect('orders:checkout_order',order.id) 
       
#------------------------------------------------------------------------------------------------

class CheckoutOrderView(LoginRequiredMixin,View):
    def get(self,request,order_id):
        user=request.user
        customer=get_object_or_404(Customer,user=user)
        order=get_object_or_404(Order,id=order_id)
        shop_cart=shopCart(request)
        
        total_price_detail=shop_cart.calc_total_price()
        final_price,delivery,tax=utils.get_price_delivery_tax(total_price_detail,order.discount)
        
        data_form={
            "name":user.name,
            "family":user.family,
            "email":user.email,
            "phone_number":customer.phone_number,
            "address":customer.address,
            
        }

        form=OrderForm(data_form)
        form_coupon=CouponForm()
        context={
            'shop_cart':shop_cart,
            'total_price_detail':total_price_detail,
            'delivery':delivery,
            'tax':tax,
            'final_price':final_price,
            'order':order,
            'form':form,    
            'form_coupon':form_coupon
        }
        return render(request,'order_app/checkout.html',context)
    
    
    
    def post(self,request,order_id):
        form=OrderForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
           
            try:
                order=Order.objects.get(id=order_id)
                order.description=data['description']
                order.payment=Payment.objects.get(id=data['payment'])
                order.save()
                
                user=request.user
                user.name=data['name']
                user.family=data['family']
                user.email=data['email']
                user.save()
                
                customer=Customer.objects.get(user=user)
                customer.phone_number=data['phone_number']
                customer.address=data['address']
                customer.save()
                
                messages.success(request,'اطلاعات با موفقیت ثبت شد','success')
                return redirect('payments:zarinpal_payment',order_id)   
              
            except ObjectDoesNotExist:
                messages.error(request,'فاکتوری با این مشخصات یافت نشد.','danger')
                return redirect('orders:checkout_order',order_id)   
           
           
           
           
           
           
               
#------------------------------------------------------------------------------------------------
        
class ApplyCoupon(View):
    def post(self, request, *args, **kwargs):
        order_id=kwargs['order_id']
        form=CouponForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            coupon_code=data['coupon_code']
            
            coupon=Coupons.objects.filter(
                Q(coupon_code=coupon_code) &
                Q(is_active=True) &
                Q(start_date__lte=datetime.now()) &
                Q(end_date__gte=datetime.now())
            )
            discount=0
            try:
                order=Order.objects.get(id=order_id)
                if coupon:
                    discount=coupon[0].discount
                    order.discount=discount
                    order.save()
                    messages.success(request,'کد تخفیف اعمال شد','success')
                    return redirect('orders:checkout_order',order_id) 
                else:
                    messages.error(request,'کد تخفیف اعمال نشد','danger')
                    order.discount=discount
                    order.save()
            except ObjectDoesNotExist:
                messages.error(request,'سفارش موجود نیست','danger')
            return redirect('orders:checkout_order',order_id) 
                    



