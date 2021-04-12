from django import forms
from ecommerce.models import Product,Orders

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        
        # exclude = ["product_name","details"]
        fields = ["name","category","price","sale_price","image","details"]


  


class OrdersForm(forms.ModelForm):  
    class Meta:  
        model = Orders 
        fields = "__all__" 
        