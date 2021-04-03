from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ecommerce.models import Category,add_product,cart
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from ecommerce.forms import add_product_form
from django.db.models import Q
from datetime import datetime
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required



def index(request):   
    #recent = Contact_Us.objects.all().order_by("-id")[:5]
    cats = Category.objects.all().order_by("cat_name")
    return render(request,"ecommerce/index.html",{"category":cats})
    

# def home(request):
#     return render(request,'ecommerce/home.html')




########################################################################################################################################################

def all_products(request):
    context = {}
    cats = Category.objects.all().order_by("cat_name")
    context["category"] = cats
    all_products = add_product.objects.all().order_by("product_name")
    context["products"] = all_products
    if "qry" in request.GET:
        q = request.GET["qry"]
        prd = add_product.objects.filter(Q(product_name__icontains=q)|Q(product_category__cat_name__contains=q))
        context["products"] = prd   
        context["abcd"]="search"
    if "cat" in request.GET:
        cid = request.GET["cat"]
        prd = add_product.objects.filter(product_category__id=cid)
        context["products"] = prd   
        context["abcd"]="search"

    return render(request,"ecommerce/allproducts.html",context)

########################################################################################################################################################


def add_to_cart(request):
    context={}
    items = cart.objects.filter(user__id=request.user.id,status=False)
    context["items"] = items

    if request.user.is_authenticated:
        if request.method=="POST":
            pid = request.POST["pid"]
            qty = request.POST["qty"]
            is_exist = cart.objects.filter(product__id=pid,user__id=request.user.id,status=False)
            if len(is_exist)>0:
                context["msz"] = "Item Already Exists in Your Cart"
                context["cls"] = "alert alert-warning"
            else:    
                product =get_object_or_404(add_product,id=pid)
                usr = get_object_or_404(User,id=request.user.id)
                c = cart(user=usr,product=product,quantity=qty)
                c.save()
                context["msz"] = "{} Added in Your Cart".format(product.product_name)
                context["cls"] = "alert alert-success"
    else:
        context["status"] = "Please Login First to View Your Cart"
    return render(request,"ecommerce/cart.html",context)


def get_cart_data(request):
    items = cart.objects.filter(user__id=request.user.id, status=False)
    sale,total,quantity =0,0,0
    for i in items:
        sale += float(i.product.sale_price)*i.quantity
        total += float(i.product.product_price)*i.quantity
        quantity+= int(i.quantity)

    res = {
        "total":total,"offer":sale,"quan":quantity,
    }
    return JsonResponse(res)

def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(cart,id=cid)
        cart_obj.quantity = qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)

    if "delete_cart" in request.GET:
        id = request.GET["delete_cart"]
        cart_obj = get_object_or_404(cart,id=id)
        cart_obj.delete()
        return HttpResponse(1)