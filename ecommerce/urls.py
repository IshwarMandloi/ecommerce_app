from django.urls import path
from ecommerce import views


urlpatterns = [

   	path('', views.index, name='index'),
   	path("products",views.products, name="products"),
   	path("cart",views.add_to_cart,name="cart"),
   	path("get_cart_data",views.get_cart_data,name="get_cart_data"),
    path("change_quan",views.change_quan,name="change_quan"),

    path('checkout',views.CheckoutView.as_view(),name='checkout'),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),

      	
]
