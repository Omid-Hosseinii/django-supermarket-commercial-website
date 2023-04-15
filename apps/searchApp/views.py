from django.shortcuts import render
from django.views import View
from apps.product.models import Product
from django.db.models import Q
#------------------------------------------------------------------------------

class Search(View):
    def get(self,request,*args,**kwargs):
        query=self.request.GET.get("q")
        print(query)
        
        products=Product.objects.filter(
            Q(product_name__icontains=query)
        )
        context={
            "products": products
        }
        
        return render(request,"search_app/search_result.html",context)



