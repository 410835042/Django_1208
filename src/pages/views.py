from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, HttpResponse
from .script.GetHand import V_Camera2, to_gen2, hand_video
from .script.camera import VideoCamera, gen
from .script.mixed import V_Camera, to_gen
from .script.filters import ProductFilter
from products.models import Product
from partners.forms import CartForm, Test
from partners.models import Cart, HandSize
from partners.forms import HandSizeForm
from .models import Search

import re
# Create your views here.


def home_view(request, *args, **kwargs):
    queryset = Product.objects.all()  # list of objects
    cart_queryset = Cart.objects.filter(account=request.user.id)
    form = CartForm(request.POST or None)

    context = {
        "object_list": queryset,
        "cart": cart_queryset,
        "times": 0,
        "form": form,
    }
    return render(request, "index.html", context)  # 從名為home.html模板中抓取此頁應有樣貌


def cart_add_view(request, p_id):
    form = CartForm(request.POST or None)

    instance = form.save(commit=False)
    instance.account = request.user
    instance.product = Product.objects.get(id=p_id)
    instance.save()
    return redirect('../../')


def cart_delete_view(request, p_id):
    obj = Cart.objects.get(product=p_id, account=request.user.id)
    # if request.method == "POST":
    obj.delete()
    return redirect('../')


def about_view(request, *args, **kwargs):
    return render(request, "about.html")


def threed_model_view(request):
    queryset = Product.objects.all()  # list of objects
    size = HandSize.objects.get(account=request.user.id)
    context = {
        "object_list": queryset,
        "times": 0,
        "size": size
    }
    return render(request, "3D_model/3d_js.html", context)


# ~~~~ 手勢追蹤、手部比例 ~~~~

def button(request):
    form = Test(request.POST or None)
    context = {
        'form': form,
    }
    return render(request, 'get_hand_button.html', context)


def button2(request):
    form = Test(request.POST or None)
    context = {
        'form': form,
    }
    return render(request, 'get_hand_control.html', context)


def get_hand(request):
    vid = StreamingHttpResponse(to_gen2(V_Camera2(), False), content_type='multipart/x-mixed-replace; boundary=frame')
    handsizs = HandSize.objects.get(account=request.user.id)
    form = HandSizeForm(request.POST or None, instance=request.user)
    f = open('static/Ratio.txt', 'r')
    if f.mode == 'r':
        contents = f.read()
        cut = re.sub('[^a-zA-Z0-9\n\.]', ' ', contents)
        print(contents)
        print(cut)
        temp = cut.split()
        print(temp)
        handsizs.thumb_width = abs(float(temp[0]))
        handsizs.index_width = abs(float(temp[1]))
        handsizs.middle_width = abs(float(temp[2]))
        handsizs.ring_width = abs(float(temp[3]))
        handsizs.little_width = abs(float(temp[4]))

        handsizs.thumb_length = abs(float(temp[5]))
        handsizs.index_length = abs(float(temp[6]))
        handsizs.middle_length = abs(float(temp[7]))
        handsizs.ring_length = abs(float(temp[8]))
        handsizs.little_length = abs(float(temp[9]))

        handsizs.palm_length = abs(float(temp[10]))
        handsizs.palm_width = abs(float(temp[11]))

        handsizs.save()
    return vid


def hand_control(request):
    vid = StreamingHttpResponse(to_gen(V_Camera(), False), content_type='multipart/x-mixed-replace; boundary=frame')
    return vid


# ~~~~ outside ~~~~

def video_stream(request):
    vid = StreamingHttpResponse(gen(VideoCamera(), False), content_type='multipart/x-mixed-replace; boundary=frame')
    return vid


# ~~~~ search ~~~~

def index(request):
    search = Search.objects.all()
    product_filter = ProductFilter(queryset=search)
    if request.method == "POST":
        product_filter = ProductFilter(request.POST, queryset=search)
    context = {
        'product_Filter': product_filter
    }
    return render(request, 'movies/index.html', context)


def searching_view(request):
    return  render(request, 'search.html', {})
