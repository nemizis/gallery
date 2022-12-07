from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from main.models import Product, News, Order


def index(request):
    product = Product.objects.all()
    news_on_home = News.objects.all()[:3]
    return render(request, 'index.html', context={
        'product': product,
        'news_home': news_on_home,
    })


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contacts.html')


def shop(request):
    product = Product.objects.all()
    return render(request, 'shop.html', context={
        'product': product,
    })


def cart(request):
    product = Product.objects.all()
    user = User.objects.all()
    order = Order.objects.all()
    return render(request, 'cart.html', context={
        'product': product,
        'user': user,
        'order': order,
    })


def news(request):
    news_page = News.objects.all()
    return render(request, 'news.html', context={
        'news': news_page,
    })


def news_one(request, news_id):
    selected_news = get_object_or_404(News, pk=news_id)
    return render(request, 'news_one.html', context={
        'news': selected_news,
    })


def product_detail(request, product_id):
    selected_product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', context={
        'product': selected_product,
    })
