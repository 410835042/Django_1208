from django.urls import path
from .views import (
    product_detail_view,
    product_create_view,
    product_delete_view,
    product_update_view,
    product_list_view,
    product_all_view,
    cart_delete_view,
    wear_a_ring
)

app_name = 'products'
urlpatterns = [
    path('brand/<int:b_id>/', product_list_view, name='product-list'),
    path('all/', product_all_view, name='product-all'),
    path('create/', product_create_view, name='product-list'),
    path('<int:p_id>/', product_detail_view, name='product-detail'),
    path('<int:p_id>/update/', product_update_view, name='product-update'),
    path('<int:p_id>/delete/', product_delete_view, name='product-delete'),
    path('<int:p_id>/Simulate/', wear_a_ring, name='product-threed'),

    path('<int:p_id>/cart_delete/', cart_delete_view, name='partner-cart-delete'),
    # path('products/<int:p_id>/', dynamic_lookup_view, name='product-detail'),
]

