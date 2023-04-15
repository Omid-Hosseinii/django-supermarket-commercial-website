from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
import requests
import json
from apps.orderApp.models import Order,OrderState
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Payment
from apps.accounts.models import Customer
from apps.warehouseApp.models import Warehouse,WarehouseType
#--------------------------------------------------------------------------------------------------------------------------


MERCHANT="387BB107-7FE2-411E-B55C-B8B7811D2AA2"
ZP_API_REQUEST = "https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.banktest.ir/zarinpal/www.zarinpal.com/pg/StartPay/{authority}"
CallbackURL = 'http://127.0.0.1:8000/payments/verify/'

class ZarinpalPayment(LoginRequiredMixin,View):
    def get(self,request, order_id):
        try:
            user=request.user
            description='پرداخت از طریق درگاه پرداخت زرین پال'
            order=Order.objects.get(id=order_id)
            payment=Payment.objects.create(
                order=order,
                customer=Customer.objects.get(user=user),
                amount=order.get_order_total_price(),
                description=description,
                is_finaly=False
            )
            payment.save()
            request.session['payment_session']={
                'order_id': order.id,
                'payment_id': payment.id
            }

            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.get_order_total_price(),
                "callback_url": CallbackURL,
                "description":description ,
                "metadata": {"mobile": user.mobile_number, "email": user.email}
            }
            req_header = {"accept": "application/json","content-type": "application/json'"}
            req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
            authority = req.json()['data']['authority']
            if len(req.json()['errors']) == 0:
                return redirect(ZP_API_STARTPAY.format(authority=authority))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        except ObjectDoesNotExist:
            return redirect('orders:checkout_order',order_id) 
        
    
    
class ZarinpalPaymentVerify(LoginRequiredMixin,View):
    def get(self, request, *args,**kwargs):
        order_id=request.session['payment_session']['order_id']
        payment_id=request.session['payment_session']['payment_id']
        order=Order.objects.get(id=order_id)
        payment=Payment.objects.get(id=payment_id)
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                        "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.get_order_total_price(),
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                
                if t_status == 100:
                    
                    message1=str(req.json()['data']['ref_id'])
                    order.is_finaly=True
                    order.order_state=OrderState.objects.get(id=1)
                    order.save()
                    payment.is_finaly=True
                    payment.status_code=t_status
                    payment.ref_id=str(req.json()['data']['ref_id'])
                    payment.save()
                    
                    for item in order.orders_detail1.all():
                        Warehouse.objects.create(
                            warehouse_type=WarehouseType.objects.get(id=2),
                            user_registered=request.user,
                            product=item.product,
                            qty=item.qty,
                            price=item.price,
                            
                        )
                    
                        
                    
                    del request.session['shop_cart']
                    return redirect('payments:show_verify_message',
                                    f"پرداخت با موفقیت انجام شد ، کد رهگیری شما {message1} می باشد")
                elif t_status == 101:
                    message2=str(req.json()['data']['message'])
                    order.is_finaly=True
                    order.save()
                    payment.is_finaly=True
                    payment.status_code=t_status
                    payment.ref_id=str(req.json()['data']['ref_id'])
                    payment.save()
                    del request.session['shop_cart']
                    return redirect('payments:show_verify_message',
                                    f"پرداخت با موفقیت انجام شد ، کد رهگیری شما {message2} می باشد")  
                else:
                    message3=str(req.json()['data']['ref_id'])
                    payment.status_code=t_status
                    payment.save()
                    return redirect('payments:show_verify_message',
                                    f"پرداخت قبلا انجام شده ، کد رهگیری شما {message3} می باشد")
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return redirect('payments:show_verify_message',
                                f"خطا در فرآیند پرداخت Error code: {e_code}, Error Message: {e_message}")
        else:
            return redirect('payments:show_verify_message',f"خطا در فرآیند پرداخت")
   
    
    
    
def show_verify_message(request,message):
    return render(request,'payment_app/verify_message.html',{'message':message})   
    
    
    
            