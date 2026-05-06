import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_core.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Product

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Superuser created: admin / admin")

# Create mock products
if not Product.objects.exists():
    Product.objects.create(
        name="Premium Wireless Headphones",
        description="High-quality noise-canceling wireless headphones with a 30-hour battery life.",
        price=199.99,
        stock=50
    )
    Product.objects.create(
        name="Mechanical Gaming Keyboard",
        description="RGB backlit mechanical keyboard with tactile switches for the ultimate typing experience.",
        price=129.50,
        stock=25
    )
    Product.objects.create(
        name="Ultra HD Smart Monitor",
        description="27-inch 4K resolution monitor with smart features and eye-care technology.",
        price=349.00,
        stock=10
    )
    print("3 Mock products created successfully.")
