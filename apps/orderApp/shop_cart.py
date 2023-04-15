from apps.product.models import Product

class shopCart:
    def __init__(self,request):
        self.session=request.session
        temp=self.session.get('shop_cart')
        if not temp:
            temp=self.session['shop_cart']={}
        self.shop_cart=temp
        self.count=sum([int(item[1]['qty']) for item in self.shop_cart.items()])       
            
      
      
    def __iter__(self):
        list_id=self.shop_cart.keys()
        products=Product.objects.filter(id__in=list_id) 
        temp=self.shop_cart.copy()
        for product in products:
            temp[str(product.id)]['product']=product
            
        for item in temp.values():
            item["total_price"]=item["qty"]*int(item["discount_price"])
            yield item 
      
            
            
    def add_to_shop_cart(self,product,qty):
        product_id=str(product.id)
        if product_id not in self.shop_cart:
            self.shop_cart[product_id]={"qty":0,"price":product.price,"discount_price":product.get_price_by_discount()}
        self.shop_cart[product_id]["qty"]+=int(qty)
        self.count=len(self.shop_cart.keys())
        self.session.modified=True   
        
        
    def delete_from_shop_cart(self,product):
        product_id=str(product.id)
        del self.shop_cart[product_id]
        self.session.modified=True
        
        
    def update_shop_cart(self,product_id_list,qty_list):
        i=0
        for product_id in product_id_list:
            self.shop_cart[product_id]['qty']=int(qty_list[i])
            i+=1
        self.session.modified=True    
               
        
    def calc_total_price(self):
        sum=0
        for item in self.shop_cart.values():
            sum+=int(item['discount_price'])*item['qty']
        return sum        
        
        
        
        
        
        