from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView

from .cart import Cart
from .forms import *
from .models import *


# class StoreHome(ListView):
#     '''Класс для отображения главной страницы'''
#     paginate_by = 4
#     model = Product
#     template_name = 'store_app/index.html'
#     context_object_name = 'products'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         '''Формирование контекста для шаблона'''
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Sportswear'
#         context['categories'] = Category.objects.all()
#         #context['num_products'] = len(Cart(request))
#         # context['search_form'] = SearchForm()
#         return context


def index(request):
    '''Функция представления главной страницы'''

    paginator = Paginator(Product.objects.all(), 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Sportswear',
        'categories': Category.objects.all(),
        'num_products': len(Cart(request)),
        # 'products': Product.objects.all(),
        'page_obj': page_obj,
    }
    return render(request, 'store_app/index.html', context=context)


# class ProductCategory(ListView):
#     '''Класс для отображения товаров одной категории'''
#     paginate_by = 4
#     model = Product
#     template_name = 'store_app/index.html'
#     context_object_name = 'products'
#
#     def get_queryset(self):
#         '''Выборка товаров только нужной категории'''
#         return Product.objects.filter(category_id=self.kwargs['category_id'])
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         '''Формирование контекста для шаблона'''
#         context = super().get_context_data(**kwargs)
#         context['title'] = context['products'][0].category
#         context['categories'] = Category.objects.all()
#         return context

def product_category(request, category_id):
    '''Функция для отображения товаров одной категории'''

    paginator = Paginator(Product.objects.filter(category_id=category_id), 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': Category.objects.get(pk=category_id),
        # 'products': Product.objects.filter(category_id=category_id),
        'categories': Category.objects.all(),
        'num_products': len(Cart(request)),
        'page_obj': page_obj,
    }
    return render(request, 'store_app/index.html', context=context)


# class ShowProduct(DetailView):
#     '''Класс для детального отображения товара'''
#     model = Product
#     template_name = 'store_app/product.html'
#     pk_url_kwarg = 'product_id'
#     context_object_name = 'product'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         '''Формирование контекста для шаблона'''
#         context = super().get_context_data(**kwargs)
#         context['title'] = context['product'].product_name
#         context['categories'] = Category.objects.all()
#         return context


def show_product(request, product_id):
    '''Функция представления одного товара'''

    product = Product.objects.get(pk=product_id)
    cart_product_form = CartAddProductForm()
    return render(request, 'store_app/product.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'title': product.product_name,
        'categories': Category.objects.all(),
        'num_products': len(Cart(request)),
    })


class RegisterUser(CreateView):
    '''Регистрация пользователя'''

    form_class = RegisterUserForm
    template_name = 'store_app/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Формирование контекста для шаблона'''
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['categories'] = Category.objects.all()
        return context


# def register_user(request):
#     '''Регистрация пользователя'''
#     register_form = RegisterUserForm()
#     context = {
#         'register_form': register_form,
#         'title': 'Регистрация',
#         'categories': Category.objects.all(),
#         'num_products': len(Cart(request)),
#     }
#     return render(request, 'store_app/register.html', context=context)


class LoginUser(LoginView):
    '''Авторизация пользователя'''

    form_class = LoginUserForm
    template_name = 'store_app/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Формирование контекста для шаблона'''
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        context['categories'] = Category.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('home')


# def login_user(request):
#     '''Авторизация пользователя'''
#     login_form = LoginUserForm()
#     context = {
#         'login_form': login_form,
#         'title': 'Авторизация',
#         'categories': Category.objects.all(),
#         'num_products': len(Cart(request)),
#     }
#     return render(request, 'store_app/login.html', context=context)


def logout_user(request):
    '''Функция представления для выхода пользователя из авторизации'''

    logout(request)
    return redirect('login')


# class AccountUser(DetailView):
#     '''Класс для отображения личного кабинета'''
#     model = User
#     template_name = 'store_app/personal_account.html'
#     pk_url_kwarg = 'user_id'
#     context_object_name = 'user'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         '''Формирование контекста для шаблона'''
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Личный кабинет'
#         context['categories'] = Category.objects.all()
#         return context


def account_user(request, user_id):
    '''Личный кабинет пользователя'''

    # user = User.objects.get(pk=user_id)
    orders = Order.objects.filter(customer_id=user_id)
    product_order = ProductOrder.objects.filter(order__in=orders)
    context = {
        'title': 'Личный кабинет',
        'orders': orders,
        'product_order': product_order,
        'categories': Category.objects.all(),
        'num_products': len(Cart(request)),
    }
    return render(request, 'store_app/personal_account.html', context=context)


def product_cart(request):
    '''Отображение корзины'''

    cart = Cart(request)
    total = sum(p['total_price'] for p in cart)
    is_empty = True
    if len(cart):
        is_empty = False
    context = {
        'cart': cart,
        'categories': Category.objects.all(),
        'is_empty': is_empty,
        'num_products': len(Cart(request)),
        'total': total,
    }
    return render(request, 'store_app/product_cart.html', context=context)


def order(request, user_id):
    '''Страница подтверждения оформленного заказа'''

    cart = Cart(request)
    customer = User.objects.get(pk=user_id)
    order = Order.objects.create(customer=customer)
    # products = Product.objects.filter(pk__in=cart.cart.keys())
    for product_id, quantity_price in cart.cart.items():
        product = Product.objects.get(pk=product_id)
        amount = quantity_price['quantity']
        ProductOrder.objects.create(product=product, order=order, amount=amount)

    cart.clear()
    categories = Category.objects.all()
    return render(request, 'store_app/order.html', {'categories': categories})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'])
        cart.save()
    return redirect('product_cart')


# @require_POST
# def search(request):
#     form = SearchForm(request.POST)
#     if form.is_valid():
#         search_query = form.cleaned_data['search_query']
#         products = Product.objects.filter(product_name__icontains=search_query)
#     index(products)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
