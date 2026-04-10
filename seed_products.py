"""
Sample products to add to the Pink Toy Store admin panel.
Run this script to quickly add sample 3D printed products.

Usage:
    python manage.py shell < seed_products.py
"""

# Sample products to add through admin or shell
SAMPLE_PRODUCTS = [
    {
        'name': 'Superwoman 3D Model',
        'slug': 'superwoman-3d-model',
        'description': 'Iconic superhero pose with detailed costume. High-quality 3D printed collectible, perfect for fans.',
        'price': 149.99,
        'stock': 25,
        'available': True,
    },
    {
        'name': 'Catwoman 3D Model',
        'slug': 'catwoman-3d-model',
        'description': 'Sleek design with authentic cat-inspired outfit. Premium 3D printed collectible.',
        'price': 139.99,
        'stock': 20,
        'available': True,
    },
    {
        'name': 'Batman 3D Model',
        'slug': 'batman-3d-model',
        'description': 'Classic Batman pose with detailed cape and bat logo. Collectible quality.',
        'price': 129.99,
        'stock': 30,
        'available': True,
    },
    {
        'name': 'Wonder Woman 3D Model',
        'slug': 'wonder-woman-3d-model',
        'description': 'Powerful Wonder Woman pose with lasso and tiara. Expertly crafted.',
        'price': 159.99,
        'stock': 15,
        'available': True,
    },
    {
        'name': 'Spider-Man 3D Model',
        'slug': 'spider-man-3d-model',
        'description': 'Iconic wall-crawling pose. Detailed web effects and suit texture.',
        'price': 119.99,
        'stock': 40,
        'available': True,
    },
    {
        'name': 'Iron Man 3D Model',
        'slug': 'iron-man-3d-model',
        'description': 'Mark 85 armor with detailed repulsors. Die-cast quality 3D print.',
        'price': 189.99,
        'stock': 10,
        'available': True,
    },
    {
        'name': 'Captain America 3D Model',
        'slug': 'captain-america-3d-model',
        'description': 'Classic shield pose. Vibrant colors and detailed battle gear.',
        'price': 129.99,
        'stock': 25,
        'available': True,
    },
    {
        'name': 'Black Panther 3D Model',
        'slug': 'black-panther-3d-model',
        'description': 'Wakandaforever pose with detailed vibranium suit. Premium finish.',
        'price': 149.99,
        'stock': 18,
        'available': True,
    },
    {
        'name': 'Thor 3D Model',
        'slug': 'thor-3d-model',
        'description': 'Stormbreaker ready pose with detailed armor and cape.',
        'price': 139.99,
        'stock': 22,
        'available': True,
    },
    {
        'name': ' Harley Quinn 3D Model',
        'slug': 'harley-quinn-3d-model',
        'description': 'Iconic costume with bat and hammer. Vibrant colors and detailed hair.',
        'price': 119.99,
        'stock': 35,
        'available': True,
    },
]

# Categories
CATEGORIES = [
    {'name': 'Superheroes', 'slug': 'superheroes'},
    {'name': 'Villains', 'slug': 'villains'},
    {'name': 'Anime Characters', 'slug': 'anime-characters'},
    {'name': 'Custom Orders', 'slug': 'custom-orders'},
]

print("=" * 50)
print("PINK TOY STORE - SAMPLE PRODUCTS")
print("=" * 50)
print("\nTo add these products:")
print("1. Go to http://127.0.0.1:8000/admin/")
print("2. Login with your admin account")
print("3. Go to Products > Categories - add categories first")
print("4. Go to Products > Products - add each product")
print("\nOr use Django shell:")
print("  python manage.py shell")
print("  Then paste the code from seed_products.py")
print("=" * 50)