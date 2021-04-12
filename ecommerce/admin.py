from django.contrib import admin
from ecommerce.models import (Category,Product,Cart,Orders)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Orders)
