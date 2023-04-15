from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .forms import CommentForm
from apps.product.models import Product
from . models import Comment,Scoring,Favorite
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Avg,Q
#------------------------------------------------------------------------------------------------------------------------
class CommentView(View):
    def get(self,request,*args,**kwargs):
        productId=request.GET.get('productId')
        commentId=request.GET.get('commentId')
        slug=kwargs['slug']

        initial_info={
            'product_id':productId,
            'comment_id':commentId,
        }
        form=CommentForm(initial=initial_info)
        return render(request,'csw_app/partials/create_comment.html',{'form':form,'slug':slug})


    
    
    def post(self,request,*args,**kwargs):
        slug=kwargs['slug']
        product=get_object_or_404(Product,slug=slug)
        form=CommentForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
        
            print(100*'-')
            print(cd['comment_id'])
            print(100*'-')
            parent=None
            if cd['comment_id']:
                obj=Comment.objects.get(id=cd['comment_id'])
                parent=obj
                
            Comment.objects.create(
                product=product,
                commenting_user=request.user,
                comment_text=cd['comment_text'],
                comments_parent=parent
            ) 
            messages.success(request,'نظر شما با موفقیت درج شد','success')  
            return redirect('products:product_detail',slug) 
        messages.error(request,'پیام شما ارسال نشد','danger')  
        return redirect('products:product_detail',slug) 
            
#------------------------------------------------------------------------------------------------------------------------

def add_score(request):
    product_id=request.GET.get('productid')
    score=request.GET.get('score')
    
    product=Product.objects.get(id=product_id)
    Scoring.objects.create(
        product=product,
        scoring_user=request.user,
        score=score
    )
    avg_score=product.scoring_product.all().aggregate(Avg('score'))['score__avg']  
    return HttpResponse(("%.2f" % avg_score) )


#------------------------------------------------------------------------------------------------------------------------

def add_favorite(request):
    product_id=request.GET.get('productId')
    flag=Favorite.objects.filter(
        Q(favorite_user_id=request.user.id) &
        Q(product_id=product_id)
    ).exists()
    
    if not flag:
        product=Product.objects.get(id=product_id)
        Favorite.objects.create(
            product=product,
            favorite_user=request.user,
        )
        return HttpResponse("محصول مورد نظر به لیست علاقه مندی ها اظافه شد")
    return HttpResponse("این کالا قبلا به لیست علاقه مندی ها اضافه شده است")

#------------------------------------------------------------------------------------------------------------------------
class UserFavoriteView(View):
    def get(self, request, *args, **kwargs):
        user_favorite=Favorite.objects.filter(Q(favorite_user_id=request.user.id))
        return render(request,'csw_app/favorite_list.html',{'user_favorite':user_favorite})

