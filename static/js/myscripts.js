// scripts for product page by group and filters for them
$(document).ready(
    function() {
        var urlParams = new URLSearchParams(window.location.search);
        if (urlParams == "") {
            localStorage.clear();
            $("#filter_state").css("display", "none");
        } else{
            $("#filter_state").css("display", "inline-block");
        }
        $('input:checkbox').on('click', function() {
            var fav ;
            var favs=[];
            $('input:checkbox').each(function () {
                fav = { id: $(this).attr('id'), value: $(this).prop('checked') };
                favs.push(fav);
            })
            localStorage.setItem("favorites" , JSON.stringify(favs));
            
        })
        var favorites=JSON.parse(localStorage.getItem('favorites'));
        for (var i=0; i < favorites.length; i++) {
            document.getElementById(favorites[i].id).checked = favorites[i].value;
           
        }
    }
);



function querystring_on_url(number){
    
    var data="?"
    var url = removeURLParameter(window.location.href,"show_products");
    if ( url.includes(data)) {
        window.location = url + "&show_products=" + number;
    } else {
         window.location = url + "?show_products=" + number;
     }
}


// for show count product
$(document).ready(
    function() {
        
        var urlParams1 = new URLSearchParams(window.location.search);
        var count_product=urlParams1.get('show_products')
        var page_number=urlParams1.get('page')
        if (page_number == null){
            page_number = "1"
        }  

        if (count_product ){
            document.getElementById("show_count_product_"+count_product).setAttribute('selected', true);
            localStorage.setItem("count_product" ,count_product);

        }else if(count_product == null && page_number === "1"){
            var count_product=localStorage.getItem('count_product')
            if (count_product ){
                document.getElementById("show_count_product_"+count_product).setAttribute('selected', true);
                querystring_on_url(count_product)
            }
            else{
                document.getElementById("show_count_product_"+4).setAttribute('selected', true);
            }
        }else if(page_number!="1") {
           var count_product=localStorage.getItem('count_product')
           if (count_product){
               querystring_on_url(count_product);
               count_product=Number(count_product)
           }else {
            count_product=4
           }
           document.getElementById("show_count_product_"+count_product).setAttribute('selected', true);
        }
        
    }
);




function showVal(x){
    x=x.toString().replace(/\B(?=(\d{3})+(?!\d))/g,',');
    document.getElementById('cur_price').innerText=x;
    }


function removeURLParameter(url,parameter){
    var urlparts=url.split('?')
    if (urlparts.length >=2){
        var prefix= encodeURIComponent(parameter)+'=';
        var pars=urlparts[1].split(/[&;]/g);
        for (var i=pars.length; i-- > 0;){
            if (pars[i].lastIndexOf(prefix,0) !== -1){
                pars.splice(i,1);
            }
        }
        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
    }
    return url

}


function select_sort(){
    var select_sort_value=$("#select_sort").val();

    var data="?"
    var url = removeURLParameter(window.location.href,"sort_type");
    if ( url.includes(data)) {
        window.location = url + "&sort_type=" + select_sort_value;
    } else {
        window.location = url + "?sort_type=" + select_sort_value;
    }

}    


function select_show(){
    var select_show_value=$("#show_products").val();
    querystring_on_url(select_show_value)
}    


// End scripts for product page by group and filters for them



// scripts ajax for shop cart

status_of_shop_cart()

function status_of_shop_cart(){
    $.ajax({
        type: "GET",
        url:'/order/status_of_shop_cart/',
        success:function(res){
            $("#indicator__value").text(res);
        }
    });
}


function add_to_shop_cart(product_id,qty){
    if (qty === 0){
        qty=$("#product-quantity").val();
    } 
    $.ajax({
        type: "GET",
        url:'/order/add_to_shop_cart/',
        data:{
            "product_id":product_id,
            "qty":qty
        },
        success: function(res){
            alert("کالای مورد نظر به سبد خرید اضافه شد");
            status_of_shop_cart();
            
        }
    });
}


function delete_from_shop_cart(product_id){
    $.ajax({
        type: "GET",
        url:'/order/delete_from_shop_cart/',
        data:{
            "product_id":product_id,
        },
        success: function(res){
            alert("کالای مورد نظر از سبد خرید حذف شد");
            $("#shop_cart_list").html(res);
            status_of_shop_cart();
            
        }
    });
}


function update_shop_cart(){
    var product_id_list =[]
    var qty_list =[]
    $("input[id^='qty_']").each(function(index) {
        product_id_list.push($(this).attr('id').slice(4))
        qty_list.push($(this).val());
    });
    $.ajax({
        type: "GET",
        url:'/order/update_shop_cart/',
        data:{
            "product_id_list":product_id_list,
            "qty_list":qty_list
        },
        success: function(res){
            $("#shop_cart_list").html(res);
            status_of_shop_cart();
            
        }
    });
}

// End scripts ajax for shop cart



// scripts ajax for comments scoring 

function showcreatecommentForm(productId,commentId,slug){
    $.ajax({
        type: "GET",
        url: '/csw/create_comment/'+slug,
        data:{
            productId:productId,
            commentId:commentId
        },
        success:function(res){
            $("#btn_"+commentId).hide();
            $("#comment_form_"+commentId).html(res);

        }
    });
}


function addScore(score,productid){
    var scoreRate=document.querySelectorAll(".fa-star");
    scoreRate.forEach( element => {
        element.classList.remove('scoring_checked')
    });
    for(let i=1 ; i <= score ; i++){
        const element=document.getElementById("star_"+i)
        element.classList.add('scoring_checked')
    }
    $.ajax({
        type: "GET",
        url: '/csw/add_score/',
        data:{
            productid:productid,
            score:score
        },
        success:function(res){
            alert("امتیاز شما درج شد");
            document.getElementById("avg_score").innerText=res;
            
        }
    });
    scoreRate.forEach( element => {
        element.classList.add('disable')
    });
}



// End scripts ajax for comments scoring 


