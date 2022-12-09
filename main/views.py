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


# def shop(request):
#     product = Product.objects.all()
#     return render(request, 'shop.html', context={
#         'product': product,
#     })

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


# def product_detail(request, product_id):
#     selected_product = get_object_or_404(Product, pk=product_id)
#     return render(request, 'product_detail.html', context={
#         'product': selected_product,
#     })

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
                return redirect('cart')
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
