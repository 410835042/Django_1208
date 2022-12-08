from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Brand, Account, Cart, HandSize  # 從.models中引用Product函數建立的模型樣式

admin.site.register(Cart)
admin.site.register(Brand)
admin.site.register(Account)
admin.site.register(HandSize)

