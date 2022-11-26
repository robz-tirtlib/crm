from django.db import models

from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True)
    photo = models.ImageField(default='default_avatar.jpg')

    def __str__(self):
        return self.name


class Order(models.Model):
    ORDER_STATUSES = (
        ('Packing', 'Packing'),
        ('On the way', 'On the way'),
        ('Delivered', 'Delivered')
    )

    customer = models.ForeignKey('Customer', null=True,
                                 on_delete=models.SET_NULL)
    product = models.ForeignKey('Product', null=True,
                                on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, null=True,
                              choices=ORDER_STATUSES)

    def __str__(self):
        return f'{self.customer.name}: {self.product.name}'


class Product(models.Model):
    PRODUCT_CATEGORIES = (
        ('Food', 'Food'),
        ('Electronics', 'Electronics'),
        ('Clothes', 'Clothes')
    )

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=PRODUCT_CATEGORIES)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name
