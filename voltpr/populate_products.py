import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voltpr.settings')
django.setup()

from voltvibe.models import Product

# Define image to product mapping
products_data = [
    # Laptops
    {'name': 'HP EliteBook 830 G7', 'image': 'EliteBook_830_G7.jpg', 'category': 'laptop', 'price': 85000},
    {'name': 'HP Pavilion 1030 G4', 'image': 'Hp_1030_G4.jpg', 'category': 'laptop', 'price': 45000},
    {'name': 'HP Victus Gaming Laptop', 'image': 'HP_Victus_Gaming_Laptop.jpg', 'category': 'laptop', 'price': 120000},
    {'name': 'Lenovo ThinkPad', 'image': 'thinkpad.jpg', 'category': 'laptop', 'price': 95000},
    
    # Phones
    {'name': 'Samsung Galaxy A73 5G', 'image': 'samsung-galaxy-a73-5g.jpg', 'category': 'phone', 'price': 35000},
    
    # Generic product images (split between phones and laptops)
    {'name': 'Premium Smartphone Model V39-139', 'image': 'v39_139.png', 'category': 'phone', 'price': 28000},
    {'name': 'Professional Laptop V39-142', 'image': 'v39_142.png', 'category': 'laptop', 'price': 65000},
    {'name': 'Business Phone V39-155', 'image': 'v39_155.png', 'category': 'phone', 'price': 32000},
    {'name': 'Flagship Smartphone V39-156', 'image': 'v39_156.png', 'category': 'phone', 'price': 45000},
    {'name': 'Ultra Phone V39-157', 'image': 'v39_157.png', 'category': 'phone', 'price': 42000},
    {'name': 'Advanced Notebook V39-169', 'image': 'v39_169.png', 'category': 'laptop', 'price': 75000},
    {'name': 'Portable Laptop V39-172', 'image': 'v39_172.png', 'category': 'laptop', 'price': 55000},
    {'name': 'Ultra Laptop V39-174', 'image': 'v39_174.png', 'category': 'laptop', 'price': 98000},
    {'name': 'Gaming Laptop V39-177', 'image': 'v39_177.png', 'category': 'laptop', 'price': 110000},
    {'name': 'Power Phone V40-188', 'image': 'v40_188.png', 'category': 'phone', 'price': 38000},
    {'name': 'Pro Phone V40-189', 'image': 'v40_189.png', 'category': 'phone', 'price': 48000},
    {'name': 'Expert Phone V40-190', 'image': 'v40_190.png', 'category': 'phone', 'price': 52000},
    {'name': 'Elite Laptop V40-191', 'image': 'v40_191.png', 'category': 'laptop', 'price': 88000},
    {'name': 'Pro Workstation V40-192', 'image': 'v40_192.png', 'category': 'laptop', 'price': 125000},
    {'name': 'Business Phone V40-193', 'image': 'v40_193.png', 'category': 'phone', 'price': 40000},
    {'name': 'Compact Phone V40-194', 'image': 'v40_194.png', 'category': 'phone', 'price': 25000},
    {'name': 'Smart Laptop V40-195', 'image': 'v40_195.png', 'category': 'laptop', 'price': 72000},
    {'name': 'Premium Laptop V40-196', 'image': 'v40_196.png', 'category': 'laptop', 'price': 102000},
    {'name': 'Ultimate Phone V40-197', 'image': 'v40_197.png', 'category': 'phone', 'price': 58000},
]

def populate_products():
    created_count = 0
    skipped_count = 0
    error_count = 0
    
    for product_info in products_data:
        try:
            # Check if product already exists
            if Product.objects.filter(image=product_info['image']).exists():
                print(f"⊘ Skipped: {product_info['name']} (already exists)")
                skipped_count += 1
                continue
            
            # Create the product
            product = Product.objects.create(
                name=product_info['name'],
                image=product_info['image'],
                category=product_info['category'],
                price=product_info['price'],
                description=f"{product_info['name']} - Premium {product_info['category'].capitalize()}",
                detailed_description=f"High-quality {product_info['category']} device with excellent features and performance.",
                digital=False
            )
            print(f"✓ Created: {product.name} ({product.category}) - KES {product.price}")
            created_count += 1
        except Exception as e:
            print(f"✗ Error creating {product_info['name']}: {str(e)}")
            error_count += 1
            continue
    
    print(f"\n{'='*60}")
    print(f"Summary: {created_count} products created, {skipped_count} skipped, {error_count} errors")
    print(f"Total in database: {Product.objects.count()}")
    print(f"{'='*60}")

if __name__ == '__main__':
    populate_products()
