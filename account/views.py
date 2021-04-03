from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth 
from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, View, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from .models import register_table
from django.core.mail import EmailMessage

#########################################################################################################################################



def register(request):
    if "user_id"in request.COOKIES:
        uid = request.COOKIES["user_id"]
        usr = get_object_or_404(User,id=uid)
        login(request,usr)
        if usr.is_superuser:
            return HttpResponseRedirect("/admin")
        if usr.is_active:
            return HttpResponseRedirect("/my_account")
    if request.method=="POST":
        fname = request.POST["first"]
        last = request.POST["last"]
        un = request.POST["uname"]
        pwd = request.POST["password"]
        em = request.POST["email"]
        con = request.POST["contact"]
        tp = request.POST["utype"]
        
        usr = User.objects.create_user(un,em,pwd)
        usr.first_name = fname
        usr.last_name = last
        if tp=="sell":
            usr.is_staff = True
        usr.save()

        reg = register_table(user=usr, contact_number=con)
        reg.save()
        return render(request,"account/sign_up.html",{"status":"Mr/Miss. {} your Account created Successfully".format(fname)})
    return render(request,"account/sign_up.html")


#########################################################################################################################################    

def check_user(request):
    if request.method=="GET":
        un = request.GET["usern"]
        check = User.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")


#########################################################################################################################################


@login_required
def user_logout(request):
    logout(request)
    res =  HttpResponseRedirect("/")
    res.delete_cookie("user_id")
    res.delete_cookie("date_login")
    messages.success(request,"Successfull Logged Out")
    return res


#########################################################################################################################################

def user_login(request):
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["password"]

        user = authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            if user.is_superuser:
                return HttpResponseRedirect("/admin")
            else:
                messages.success(request," Successfully Logged in ")
                res = HttpResponseRedirect("/all_products")
                if "rememberme" in request.POST:
                    res.set_cookie("user_id",user.id)
                    res.set_cookie("date_login",datetime.now())
                return res
        else:
            messages.success(request,"Incorrect username or Password")
            return render(request,"account/login.html")

    return render(request,"account/login.html")



#########################################################################################################################################



def change_password(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check==True:
            user.set_password(new_pas)
            user.save()
            messages.success(request," Password Changed Successfully!!! ")
            context["msz"] = "Password Changed Successfully!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        else:
            messages.success(request," Incorrect Current Password!!! ")
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"

    return render(request,"account/change_password.html",context)

#########################################################################################################################################

