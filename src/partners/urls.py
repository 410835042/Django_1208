from django.urls import path
from .views import (
    brand_list_view,
    brand_create_view,
    brand_detail_view,
    brand_update_view,
    brand_delete_view,
    sign_up_view,
    login_view,
    index_view,
    information_view,
    update,
    cart_view,
    hand_size_view,
    cart_delete_view,
    logout_view,
    delete_user,
)

app_name = 'partners'
urlpatterns = [
    path('index/', index_view, name='partner-index'),
    path('', information_view, name='partner-information'),
    path('cart/', cart_view, name='partner-cart'),
    path('handsize/', hand_size_view, name='partner-hand-size'),
    path('<int:c_id>/cart_delete/', cart_delete_view, name='partner-cart-delete'),
    path('signup/', sign_up_view, name='partner-signup'),
    path('login/', login_view, name='partner-login'),
    path('update_user_infor/', update, name='update-user-date'),
    path('logout/', logout_view, name='partner-logout'),
    path('delete_user/', delete_user, name='partner-delete_user'),

    path('list/', brand_list_view, name='brand-list'),
    path('create/', brand_create_view, name='brand-create'),
    path('<int:b_id>/', brand_detail_view, name='brand-detail'),
    path('<int:b_id>/update/', brand_update_view, name='brand-update'),
    path('<int:b_id>/delete/', brand_delete_view, name='brand-delete'),

]

