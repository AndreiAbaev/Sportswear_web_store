from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Product(models.Model):
    '''Модель товара'''
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')

    def __str__(self):
        return self.product_name


class Brand(models.Model):
    '''Модель бренда'''
    brand_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.brand_name


class Category(models.Model):
    '''Модель категории'''
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})


class Order(models.Model):
    '''Модель заказа'''
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)


class ProductOrder(models.Model):
    '''Связка между продуктом и заказом'''
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    amount = models.IntegerField()
