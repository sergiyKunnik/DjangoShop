import json
from decimal import Decimal
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as user_logout
from django.contrib.auth import login as user_login
from app.models import Category, Product, CartItem, Cart, Order
from app.forms import OrderForm, RegisterForm, LoginForm
# Create your views here.


def get_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=int(cart_id))
        request.session['count'] = cart.items.count()
        return cart
    except:
        cart = Cart()
        cart.save()
        request.session['cart_id'] = cart.id
        cart = Cart.objects.get(id=cart.id)
        return cart


def base_view(request):
    cart = get_cart(request)
    return render(request, 'base/base.html', {
        'cart': cart,
        'categories': Category.objects.all(),
        'products': Product.objects.all(cart.items.all())
    })


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = get_cart(request)
    products_in_cart = [item.product for item in cart.items.all()]
    if product in products_in_cart:
        product.in_cart = True
        print(product)
    return render(request, 'product.html', {
        'cart': cart,
        'product': product,
        'categories': Category.objects.all(),
    })


def products_by_category(request, category_slug):
    cart = get_cart(request)
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.filter_by_category(cart.items.all(), category)

    return render(request, 'category.html', {
        'cart': cart,
        'categories': Category.objects.all(),
        'category': category,
        'products': products
    })


def cart(request):
    cart = get_cart(request)
    if not cart.items.aggregate(Sum('item_total'))['item_total__sum'] == None:
        cart.cart_total = cart.items.aggregate(Sum('item_total'))['item_total__sum']
    else:
        cart.cart_total = 0.00
    cart.save()

    return render(request, 'cart.html', {
        'categories': Category.objects.all(),
        'cart': cart,
    })


def add_to_cart(request, id):
    cart = get_cart(request)

    if cart.add_to_cart(int(id)):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, item_id):
    cart = get_cart(request)
    if cart.remove_from_cart(int(item_id)):
        return HttpResponseRedirect('/cart/')


@csrf_exempt
def edit_cart_item(request):
    cart = get_cart(request)
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        cart_item = CartItem.objects.get(id=int(body['item_id']))
        cart_item.qty = int(body['qty'])
        cart_item.item_total = int(body['qty']) * Decimal(cart_item.product.price)
        cart_item.save()
        cart.cart_total = cart.items.aggregate(Sum('item_total'))['item_total__sum']
        cart.save()
        return JsonResponse({
            'status': True,
            'item_total': cart_item.item_total,
            'cart_total': cart.cart_total
        })


def checkout(request):
    cart = get_cart(request)

    return render(request, 'checkout.html', {
        'cart': cart
    })


def order(request):
    cart = get_cart(request)
    form = OrderForm(request.POST or None)

    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']
        new_order = Order(
            user=request.user,
            first_name=name,
            last_name=last_name,
            phone=phone,
            address=address,
            comments=comments,
            total_price=cart.cart_total
        )
        new_order.user = request.user
        new_order.save()
        new_order.items.add(*cart.items.all())
        Cart.objects.get(id=int(request.session['cart_id'])).delete()
        del request.session['cart_id']
        email_list = []
        for user in User.objects.filter(is_superuser=True):
            email_list.append(user.email)
        send_mail(
            'Нове замовлення',
            'До вас прийшло нове замовлення. Його деталі зможете перглянути в адмінці',
            'from@example.com',
            [email_list],
        )
        return HttpResponseRedirect('/thank_you')

    return render(request, 'order.html', {
        'form': form,
        'cart': cart
    })


def thank_you(request):
    return render(request, 'thank_you.html', {})


def account(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'account.html', {
        'orders': orders
    })


def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        User.objects.create(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        return HttpResponseRedirect('/login')

    return render(request, 'register.html', {
        'form': form
    })


def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = User.objects.get(username=username, password=password)
        user_logout(request)
        user_login(request, user)
        return HttpResponseRedirect('/')
    return render(request, 'login.html', {
        'form': form,
    })


def logout(request):
    if request.user.is_authenticated:
        user_logout(request)
        return HttpResponseRedirect('/')