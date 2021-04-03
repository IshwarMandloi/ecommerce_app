from django.contrib import admin
from ecommerce.models import (Category,add_product,cart)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id","cat_name","description","added_on"]


admin.site.register(Category,CategoryAdmin)
admin.site.register(add_product)
admin.site.register(cart)
# admin.site.register(Order)