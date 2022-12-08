"""django_tsst1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from pages.views import (
    home_view, about_view,
    # threed_model_view,
    button, button2, get_hand,
    video_stream,
    hand_control,
    cart_delete_view,
    cart_add_view,
    searching_view
)


# 此為向url提出有沒有符合的頁面，有的話就連過去
urlpatterns = [
    path('products/', include('products.urls')),
    path('partners/', include('partners.urls')),

    path('', home_view, name='home'),
    path('<int:p_id>/cart_add', cart_add_view, name='cart_add'),
    path('<int:p_id>/cart_delete', cart_delete_view, name='cart_delete'),
    # path('home/', home_view),
    path('admin/', admin.site.urls),
    path('about/', about_view),
    # path("3dtest/", threed_model_view),
    path("GetHand/", button),
    path("HandControl/", button2),
    path("GetHand/getting", get_hand, name='get_your_hand'),
    path("GetHand/control", hand_control, name='get_hand_and_control'),
    path("GetHand_output/video_stream", video_stream),
    path("Search/", searching_view, name='searching')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
