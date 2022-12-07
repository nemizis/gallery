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
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth', include('authentication.urls')),
    path('contacts', include('main.urls')),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('news/', views.news, name='news'),
    path('news/<int:news_id>', views.news_one, name='news_one'),
    path('shop/<int:product_id>', views.product_detail, name='product_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
