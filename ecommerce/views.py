from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ecommerce.models import Category, Product,Cart
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from ecommerce.forms import ProductForm
from django.db.models import Q
from datetime import datetime
from django.core.mail import EmailMessage

###############################################################################################################################


def index(request):
    cats = Category.objects.all().order_by("name")
    return render(request,"ecommerce/home.html",{"category":cats})


###############################################################################################################################


def products(request):
    context = {}
    cats = Category.objects.all().order_by("name")
    context["category"] = cats
    all_products = Product.objects.all().order_by("name")
    context["products"] = all_products
    if "qry" in request.GET:
        q = request.GET["qry"]
        # p = request.GET["price"]
        prd = Product.objects.filter(Q(name__icontains=q)|Q(category__name__contains=q))
        # prd = add_product.objects.filter(Q(product_name__icontains=q)& Q(sale_price__lt=p))
        # prd = add_product.objects.filter(product_name__contains=q)
        context["products"] = prd   
        context["abcd"]="search"
    if "cat" in request.GET:
        cid = request.GET["cat"]
        prd = Product.objects.filter(category__id=cid)
        context["products"] = prd   
        context["abcd"]="search"

    return render(request,"ecommerce/products.html",context)


###############################################################################################################################


def add_to_cart(request):
    context={}
    items = Cart.objects.filter(user__id=request.user.id,status=False)
    context["items"] = items

    if request.user.is_authenticated:
        if request.method=="POST":
            pid = request.POST["pid"]
            qty = request.POST["qty"]
            is_exist = Cart.objects.filter(product__id=pid,user__id=request.user.id,status=False)
            if len(is_exist)>0:
                context["msz"] = "Item Already Exists in Your Cart"
                context["cls"] = "alert alert-warning"
            else:    
                product =get_object_or_404(Product,id=pid)
                usr = get_object_or_404(User,id=request.user.id)
                c = Cart(user=usr,product=product,quantity=qty)
                c.save()
                context["msz"] = "{} Added in Your Cart".format(product.name)
                context["cls"] = "alert alert-success"
    else:
        context["status"] = "Please Login First to View Your Cart"
    return render(request,"ecommerce/cart.html",context)



###############################################################################################################################




def get_cart_data(request):
    items = Cart.objects.filter(user__id=request.user.id, status=False)
    sale,total,quantity =0,0,0
    for i in items:
        sale += float(i.product.sale_price)*i.quantity
        total += float(i.product.price)*i.quantity
        quantity+= int(i.quantity)

    res = {
        "total":total,"offer":sale,"quan":quantity,
    }
    return JsonResponse(res)



###############################################################################################################################


def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(Cart,id=cid)
        cart_obj.quantity = qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)

    if "delete_cart" in request.GET:
        id = request.GET["delete_cart"]
        cart_obj = get_object_or_404(Cart,id=id)
        cart_obj.delete()
        return HttpResponse(1)



###############################################################################################################################
