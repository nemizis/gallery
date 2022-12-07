from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user}, {self.amount}'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Product')
    img = models.ImageField(blank=True, null=True, upload_to='img/')
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # url = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)

    def __str__(self):
        return f'{self.name}, {self.price}'


class Order(models.Model):
    STATUS_CART = 'cart'
    STATUS_WAITING_PAYMENT = 'waiting_payment'
    STATUS_PAID = 'paid'
    STATUS = [
        (STATUS_CART, 'Корзина'),
        (STATUS_WAITING_PAYMENT, 'Ожидает оплаты'),
        (STATUS_PAID, 'Оплачено')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS, default=STATUS_CART)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user}, {self.amount}, {self.status}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.product}, {self.quantity}'


class News(models.Model):
    title = models.CharField(max_length=255)
    Description = models.TextField(blank=True, null=True)
    # slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    # def get_absolute_url(self):
    #     return reverse('news_one', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'
