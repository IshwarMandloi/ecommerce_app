from django.db import models
from django.contrib.auth.models import User
import datetime


################################################################################################################

class Category(models.Model):
    name = models.CharField(max_length=250)
    cover_pic = models.FileField(upload_to="media/%Y/%m/%d")
    description = models.TextField()
    added_on =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


################################################################################################################

class Product(models.Model):
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category,on_delete = models.CASCADE )
    price = models.FloatField()
    sale_price = models.CharField(max_length=200)
    image = models.ImageField(upload_to="products/%Y/%m/%d")
    details = models.TextField()

    def __str__(self):
        return self.name

################################################################################################################
        

class Cart(models.Model):
    user =models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)
    added_on =models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.username


#######################################################################################################


class Orders(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    order_id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=90)
    amount=models.IntegerField(default=0)
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=111)
    phone=models.CharField(max_length=111, default="")


    def __str__(self):
        return self.user.username


#######################################################################################################


class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."        



#######################################################################################################
