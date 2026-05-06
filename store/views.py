from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Cart, CartItem, Order, OrderItem
from django.contrib import messages

def home(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        # Shuffle randomly for "All Products" to simulate dynamic Amazon feed, or just all
        products = Product.objects.all().order_by('?')
        
    latest_products = Product.objects.all().order_by('-created_at')[:6]
    
    context = {
        'products': products,
        'latest_products': latest_products,
        'query': query
    }
    return render(request, 'store/home.html', context)

def search_api(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'results': []})
        
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))[:5]
    
    results = []
    for p in products:
        results.append({
            'id': p.id,
            'name': p.name,
            'price': str(p.price),
            'image_url': p.image.url if p.image else '',
            'detail_url': f'/product/{p.id}/'
        })
        
    return JsonResponse({'results': results})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('cart')

def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return redirect('cart')

def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'store/cart.html', {'cart': cart})

def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('home')

    if request.method == 'POST':
        # Check stock availability first
        insufficient_stock = False
        for item in cart.items.all():
            if item.product.stock < item.quantity:
                messages.error(request, f"Sorry, we only have {item.product.stock} of '{item.product.name}' in stock.")
                insufficient_stock = True
                
        if insufficient_stock:
            return redirect('cart')

        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=name,
            email=email,
            address=address,
            total_price=cart.total_price
        )
        
        for item in cart.items.all():
            # Deduct stock
            item.product.stock -= item.quantity
            item.product.save()
            
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
        
        # Clear cart
        cart.items.all().delete()
        messages.success(request, "Order placed successfully!")
        return redirect('home')
        
    return render(request, 'store/checkout.html', {'cart': cart})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
