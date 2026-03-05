"""
Management command to seed the database with sample data
matching the frontend mockData.ts.
"""

from django.core.management.base import BaseCommand
from menu.models import Category, Product
from tables.models import Table


class Command(BaseCommand):
    help = 'Seeds the database with categories, products, and tables from frontend mockData'

    def handle(self, *args, **options):
        self.stdout.write('Seeding categories...')
        categories_data = [
            {'id': 'all', 'name': 'All', 'icon': '🍽️'},
            {'id': 'starters', 'name': 'Starters', 'icon': '🥗'},
            {'id': 'main', 'name': 'Main Course', 'icon': '🍛'},
            {'id': 'fastfood', 'name': 'Fast Food', 'icon': '🍔'},
            {'id': 'drinks', 'name': 'Drinks', 'icon': '🍹'},
            {'id': 'desserts', 'name': 'Desserts', 'icon': '🍰'},
        ]
        for cat_data in categories_data:
            Category.objects.update_or_create(
                id=cat_data['id'],
                defaults={'name': cat_data['name'], 'icon': cat_data['icon']},
            )
        self.stdout.write(self.style.SUCCESS(f'  Created {len(categories_data)} categories'))

        self.stdout.write('Seeding products...')
        products_data = [
            {
                'id': '1',
                'name': 'Chicken Burger',
                'price': 180,
                'rating': 4.5,
                'total_reviews': 120,
                'description': 'Grilled chicken with cheese, lettuce, and our secret sauce.',
                'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80',
                'category_id': 'fastfood',
            },
            {
                'id': '2',
                'name': 'Margherita Pizza',
                'price': 250,
                'rating': 4.8,
                'total_reviews': 95,
                'description': 'Classic pizza with tomato sauce, fresh mozzarella, and basil.',
                'image': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?auto=format&fit=crop&w=800&q=80',
                'category_id': 'fastfood',
            },
            {
                'id': '3',
                'name': 'Paneer Tikka',
                'price': 220,
                'rating': 4.6,
                'total_reviews': 78,
                'description': 'Marinated paneer cubes grilled to perfection in a tandoor.',
                'image': 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?auto=format&fit=crop&w=800&q=80',
                'category_id': 'starters',
            },
            {
                'id': '4',
                'name': 'Butter Chicken',
                'price': 320,
                'rating': 4.9,
                'total_reviews': 200,
                'description': 'Tender chicken in a rich, creamy tomato-based gravy.',
                'image': 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=800&q=80',
                'category_id': 'main',
            },
            {
                'id': '5',
                'name': 'Chocolate Brownie',
                'price': 150,
                'rating': 4.7,
                'total_reviews': 65,
                'description': 'Warm chocolate brownie served with vanilla ice cream.',
                'image': 'https://images.unsplash.com/photo-1564355808539-22fda35bed7e?auto=format&fit=crop&w=800&q=80',
                'category_id': 'desserts',
            },
            {
                'id': '6',
                'name': 'Virgin Mojito',
                'price': 120,
                'rating': 4.4,
                'total_reviews': 55,
                'description': 'Refreshing blend of lime, mint, and soda.',
                'image': 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=800&q=80',
                'category_id': 'drinks',
            },
            {
                'id': '7',
                'name': 'Caesar Salad',
                'price': 190,
                'rating': 4.3,
                'total_reviews': 42,
                'description': 'Fresh romaine lettuce with croutons and parmesan cheese.',
                'image': 'https://images.unsplash.com/photo-1550304943-4f24f54ddde9?auto=format&fit=crop&w=800&q=80',
                'category_id': 'starters',
            },
            {
                'id': '8',
                'name': 'Hakka Noodles',
                'price': 160,
                'rating': 4.5,
                'total_reviews': 88,
                'description': 'Stir-fried noodles with crisp vegetables and soy sauce.',
                'image': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?auto=format&fit=crop&w=800&q=80',
                'category_id': 'main',
            },
        ]
        for prod_data in products_data:
            Product.objects.update_or_create(
                id=prod_data['id'],
                defaults={
                    'name': prod_data['name'],
                    'price': prod_data['price'],
                    'rating': prod_data['rating'],
                    'total_reviews': prod_data.get('total_reviews', 0),
                    'description': prod_data['description'],
                    'image': prod_data['image'],
                    'category_id': prod_data['category_id'],
                },
            )
        self.stdout.write(self.style.SUCCESS(f'  Created {len(products_data)} products'))

        self.stdout.write('Seeding tables...')
        for i in range(1, 11):
            Table.objects.get_or_create(
                table_number=i,
                defaults={'qr_code': f'/table/{i}'},
            )
        self.stdout.write(self.style.SUCCESS('  Created 10 tables'))

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
