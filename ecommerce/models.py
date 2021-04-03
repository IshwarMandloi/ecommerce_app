# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import datetime




class Category(models.Model):
    cat_name = models.CharField(max_length=250)
    cover_pic = models.FileField(upload_to="media/%Y/%m/%d")
    description = models.TextField()
    added_on =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cat_name



class add_product(models.Model):
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250)
    product_category = models.ForeignKey(Category,on_delete = models.CASCADE )
    product_price = models.FloatField()
    sale_price = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="products/%Y/%m/%d")
    details = models.TextField()

    def __str__(self):
        return self.product_name

class cart(models.Model):
    user =models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(add_product,on_delete = models.CASCADE)
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)
    added_on =models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.username

# class Order(models.Model):
#     cust_id = models.ForeignKey(User,on_delete=models.CASCADE)
#     cart_ids = models.CharField(max_length=250)
#     product_ids = models.CharField(max_length=250)
#     invoice_id = models.CharField(max_length=250)
#     status = models.BooleanField(default=False)
#     processed_on = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.cust_id.username