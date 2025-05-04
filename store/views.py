from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Order, OrderItem
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from .utils import send_telegram_message
from django.http import JsonResponse

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})
    return render(request, 'store/product_list.html', {'products': products, 'cart': cart})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})  # безопасно извлекаем cart
    return render(request, 'store/product_detail.html', {
        'product': product,
        'cart': cart
    })

def clear_cart(request):
    if 'cart' in request.session:
        request.session['cart'] = {}
    return redirect('cart')

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    
    # Возвращаем данные в формате JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'quantity': cart[str(product_id)]})
    return redirect('product_list')

def update_cart(request, product_id, action):
    cart = request.session.get('cart', {})
    
    if action == 'increment':
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    elif action == 'decrement' and str(product_id) in cart:
        cart[str(product_id)] -= 1
        if cart[str(product_id)] <= 0:
            del cart[str(product_id)]
    
    request.session['cart'] = cart

    return JsonResponse({'quantity': cart.get(str(product_id), 0)})
    
    return JsonResponse({'quantity': cart.get(str(product_id), 0)})
def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total = 0
    for product in products:
        quantity = cart[str(product.id)]
        item_total = product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'total': item_total})
        total += item_total
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')

def about(request):
    return render(request, 'store/about.html')

def delivery(request):
    return render(request, 'store/delivery.html')

@login_required
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            for pid, qty in cart.items():
                product = Product.objects.get(id=pid)
                OrderItem.objects.create(order=order, product=product, quantity=qty)

            # очистка корзины
            request.session['cart'] = {}

            # Уведомление в Telegram (добавим ниже)
            send_telegram_message(order)

            return render(request, 'store/order_success.html', {'order': order})
    else:
        form = OrderForm()

    return render(request, 'store/order.html', {'form': form})