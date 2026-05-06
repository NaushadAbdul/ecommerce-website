import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_core.settings')
django.setup()

from store.models import Product

source_dir = r"C:\Users\white\.gemini\antigravity\brain\c16e7bb9-16e6-45c8-a616-8c93fc6e734c"
dest_dir = r"c:\Users\white\Downloads\codealphatask\media\products"
os.makedirs(dest_dir, exist_ok=True)

products_to_add = [
    {
        "name": "Men's Casual Navy T-Shirt",
        "description": "A stylish, comfortable cotton t-shirt perfect for casual outings.",
        "price": 24.99,
        "stock": 100,
        "image_file": "mens_tshirt_1777746996840.png",
        "dest_name": "mens_tshirt.png"
    },
    {
        "name": "Women's Elegant Red Evening Dress",
        "description": "A beautiful deep red evening dress for special occasions.",
        "price": 89.99,
        "stock": 40,
        "image_file": "womens_dress_1777747013013.png",
        "dest_name": "womens_dress.png"
    },
    {
        "name": "Premium Leather Men's Wallet",
        "description": "Genuine dark brown leather wallet with multiple card slots.",
        "price": 45.00,
        "stock": 75,
        "image_file": "mens_wallet_1777747028866.png",
        "dest_name": "mens_wallet.png"
    },
    {
        "name": "Women's Designer Leather Handbag",
        "description": "Luxurious black leather handbag with gold hardware.",
        "price": 199.50,
        "stock": 20,
        "image_file": "womens_handbag_1777747045555.png",
        "dest_name": "womens_handbag.png"
    },
    {
        "name": "Men's High-Performance Running Shoes",
        "description": "Sleek aerodynamic running shoes with neon accents.",
        "price": 115.00,
        "stock": 60,
        "image_file": "mens_shoes_1777747059868.png",
        "dest_name": "mens_shoes.png"
    },
    {
        "name": "Classic Women's Black Stiletto Heels",
        "description": "Elegant glossy black high heels for formal wear.",
        "price": 75.99,
        "stock": 50,
        "image_file": "womens_heels_1777747076439.png",
        "dest_name": "womens_heels.png"
    },
    {
        "name": "Off-Road RC Truck Toy",
        "description": "Fast and rugged remote control car for kids, great for off-road.",
        "price": 59.99,
        "stock": 35,
        "image_file": "rc_car_1777747090460.png",
        "dest_name": "rc_car.png"
    },
    {
        "name": "Castle Building Blocks Playset",
        "description": "Colorful building blocks set to construct a majestic castle.",
        "price": 34.50,
        "stock": 80,
        "image_file": "lego_set_1777747105232.png",
        "dest_name": "lego_set.png"
    },
    {
        "name": "Smart Robot Vacuum Cleaner",
        "description": "Automated vacuum cleaner with smart home integration and mapping.",
        "price": 249.00,
        "stock": 15,
        "image_file": "smart_vacuum_1777747123022.png",
        "dest_name": "smart_vacuum.png"
    },
    {
        "name": "Premium 10-Piece Cookware Set",
        "description": "Stainless steel pots and pans set for the modern kitchen.",
        "price": 149.99,
        "stock": 25,
        "image_file": "cookware_set_1777747138140.png",
        "dest_name": "cookware_set.png"
    }
]

for p in products_to_add:
    src_path = os.path.join(source_dir, p["image_file"])
    dst_path = os.path.join(dest_dir, p["dest_name"])
    
    # Copy file if exists
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
    
    # Create product in db
    product, created = Product.objects.get_or_create(name=p["name"], defaults={
        "description": p["description"],
        "price": p["price"],
        "stock": p["stock"],
        "image": f'products/{p["dest_name"]}'
    })
    
    if not created:
        product.description = p["description"]
        product.price = p["price"]
        product.stock = p["stock"]
        product.image = f'products/{p["dest_name"]}'
        product.save()
    print(f"Added {product.name}")

print("Successfully seeded 10 new products across various categories.")
