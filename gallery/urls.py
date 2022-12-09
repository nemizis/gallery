"""gallery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.views.generic import TemplateView

from main import views
from main.views import ProductListView, ProductDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('auth', include('authentication.urls')),
    path('contacts', include('main.urls')),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('shop/', ProductListView.as_view(), name='shop'),
    path('cart/', views.cart_view, name='cart'),
    path('news/', views.news, name='news'),
    path('news/<int:news_id>', views.news_one, name='news_one'),
    path('shop/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
