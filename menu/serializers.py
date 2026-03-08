from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']


class ProductSerializer(serializers.ModelSerializer):
    # Return the image URL, or an external URL string if stored that way
    image = serializers.SerializerMethodField()
    # DecimalField serializes as string by default; frontend expects numbers
    price = serializers.FloatField()
    rating = serializers.FloatField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'image',
            'rating', 'total_reviews', 'category', 'is_available',
        ]

    def get_image(self, obj):
        if obj.image:
            image_val = str(obj.image)
            # Seed data stores full Unsplash URLs – return as-is
            if image_val.startswith('http'):
                return image_val
            # Cloudinary uploads – .url returns the full https://res.cloudinary.com/... URL
            return obj.image.url
        return None
