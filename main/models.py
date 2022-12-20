from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.db.models import Q


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user}, {self.amount}'

    @staticmethod
    def get_balance(user: User):
        amount = Payment.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum']
        return amount or Decimal(0)


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Product')
    img = models.ImageField(blank=True, null=True, upload_to='img/')
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # url = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)

    def __str__(self):
        return f'{self.name}'


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

    @staticmethod
    def get_cart(user: User):
        cart = Order.objects.filter(
            user=user,
            status=Order.STATUS_CART,
        ).first()
        if not cart:
            cart = Order.objects.create(
                user=user,
                status=Order.STATUS_CART,
                amount=0,
            )
        return cart

    @staticmethod
    def get_paid_and_waiting_cart(user: User):
        cart = Order.objects.filter(user=user).filter(
            Q(status=Order.STATUS_WAITING_PAYMENT) | Q(status=Order.STATUS_PAID))
        return cart

    def get_amount(self):
        amount = Decimal(0)
        for i in self.orderitem_set.all():
            amount += i.amount
        return amount

    def make_order(self):
        items = self.orderitem_set.all()
        if items and self.status == Order.STATUS_CART:
            self.status = Order.STATUS_WAITING_PAYMENT
            self.save()
            auto_payment_unpaid(self.user)

    @staticmethod
    def get_amount_unpaid(user: User):
        amount = Order.objects.filter(user=user,
                                      status=Order.STATUS_WAITING_PAYMENT,
                                      ).aggregate(Sum('amount'))['amount__sum']
        return amount or Decimal(0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.product}, {self.quantity}'

    @property
    def amount(self):
        return self.quantity * (self.price - self.discount)


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
        ordering = ['date']


@receiver(post_save, sender=OrderItem)
def calculate_order_amount(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()


@receiver(post_delete, sender=OrderItem)
def calculate_order_amount_delete(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()


@transaction.atomic()
def auto_payment_unpaid(user: User):
    unpaid_orders = Order.objects.filter(user=user,
                                         status=Order.STATUS_WAITING_PAYMENT
                                         )
    for order in unpaid_orders:
        if Payment.get_balance(user) < order.amount:
            break
        order.payment = Payment.objects.all().last()
        order.status = Order.STATUS_PAID
        order.save()
        Payment.objects.create(user=user, amount=-order.amount)


@receiver(post_save, sender=Payment)
def auto_payment(sender, instance, **kwargs):
    user = instance.user
    auto_payment_unpaid(user)
