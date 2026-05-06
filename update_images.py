import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_core.settings')
django.setup()

from store.models import Product

# Update images
p1 = Product.objects.filter(name="Premium Wireless Headphones").first()
if p1:
    p1.image = 'products/headphones.png'
    p1.save()
    print(f"Updated image for {p1.name}")

p2 = Product.objects.filter(name="Mechanical Gaming Keyboard").first()
if p2:
    p2.image = 'products/keyboard.png'
    p2.save()
    print(f"Updated image for {p2.name}")

p3 = Product.objects.filter(name="Ultra HD Smart Monitor").first()
if p3:
    p3.image = 'products/monitor.png'
    p3.save()
    print(f"Updated image for {p3.name}")
