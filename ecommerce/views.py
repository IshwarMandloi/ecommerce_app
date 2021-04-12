from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ecommerce.models import Category, Product,Cart,Orders, OrderUpdate
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from ecommerce.forms import ProductForm,OrdersForm
from django.db.models import Q
from datetime import datetime
from django.core.mail import EmailMessage
from django.views import View
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
#from Paytm import Checksum
from django.http import HttpResponse
MERCHANT_KEY = 'Your-Merchant-Key-Here'

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


class CheckoutView(View):
    
    def get(self,request):
        return render(request,'ecommerce/checkout.html')
    
    def post(self,request):
        order = Orders(request.POST)
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'ecommerce/checkout.html', {'thank':thank, 'id': id})
        #request paytm to transfer the amount to your account after payment by user
        param_dict={

                'MID': 'WorldP64425807474247',
                'ORDER_ID': 'order.order_id',
                'TXN_AMOUNT': '1',
                'CUST_ID': 'email',
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/ecommerce/handlerequest/',

        }
        return  render(request, 'ecommerce/paytm.html', {'param_dict': param_dict})
    
        return render(request, 'ecommerce/checkout.html')


###############################################################################################################################


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'ecommerce/paymentstatus.html', {'response': response_dict})



###############################################################################################################################

