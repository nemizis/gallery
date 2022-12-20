from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, DeleteView

from main.forms import AddQuantity
from main.models import Product, News, Order, OrderItem


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


class ProductListView(ListView):
    model = Product
    template_name = 'shop.html'


@login_required(login_url=reverse_lazy('login'))
def cart_view(request):
    cart = Order.get_cart(request.user)
    items = cart.orderitem_set.all()
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'cart.html', context)


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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'


@login_required(login_url=reverse_lazy('login'))
def add_to_cart(request, pk):
    if request.method == 'POST':
        quantity_form = AddQuantity(request.POST)
        if quantity_form.is_valid():
            quantity = quantity_form.cleaned_data['quantity']
            if quantity:
                cart = Order.get_cart(request.user)
                product = get_object_or_404(Product, pk=pk)
                cart.orderitem_set.create(
                    product=product,
                    price=product.price,
                    quantity=quantity,
                )
                cart.save()
                return redirect('shop')
            else:
                pass
    return redirect('shop')


@method_decorator(login_required, name='dispatch')
class CartDeleteItem(DeleteView):
    model = OrderItem
    template_name = 'cart.html'
    success_url = reverse_lazy('cart')

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(order__user=self.request.user)
        return qs


@login_required(login_url=reverse_lazy('login'))
def my_orders(request):
    cart = Order.get_paid_and_waiting_cart(request.user)
    context = {
        'cart': cart,
    }
    return render(request, 'my_orders.html', context)


@login_required(login_url=reverse_lazy('login'))
def add_to_my_orders(request):
    if request.method == 'POST':
        cart = Order.get_cart(request.user)
        cart.status = Order.STATUS_WAITING_PAYMENT
        cart.save()
        return redirect('my_orders')
    else:
        pass
    return redirect('shop')


@login_required(login_url=reverse_lazy('login'))
def delete_cart(request):
    if request.method == 'POST':
        cart = Order.get_paid_and_waiting_cart(request.user)
        cart.delete()
        return redirect('my_orders')
    else:
        pass
    return redirect('shop')


def manage_orders(request):
    context = {
        'orders': Order.objects.all(),
    }
    return render(request, 'manage_orders.html', context)


@login_required(login_url=reverse_lazy('login'))
def delete_cart_manager(request, pk):
    if request.method == 'POST':
        cart = Order.objects.all()
        cart = cart.filter(pk=pk)
        cart.delete()
        return redirect('manage_orders')
    else:
        pass
    return redirect('manage_orders')


@login_required(login_url=reverse_lazy('login'))
def status_paid(request, pk):
    if request.method == 'POST':
        cart = Order.objects.filter(pk=pk)
        for objects in cart:
            objects.status = Order.STATUS_PAID
            objects.save()
        return redirect('manage_orders')
    else:
        pass
    return redirect('manage_orders')
