from django.contrib import admin

# Register your models here.
from .models import Product, Size, Search  # 從.models中引用Product函數建立的模型樣式

admin.site.register(Size)
admin.site.register(Product)  # 將products放置在網站上


class SearchAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'brand')


admin.site.register(Search, SearchAdmin)
