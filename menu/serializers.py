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
            request = self.context.get('request')
            if request and obj.image.name and not obj.image.name.startswith('http'):
                return request.build_absolute_uri(obj.image.url)
            # If the image field stores a full URL (e.g. Unsplash)
            return obj.image.name if obj.image.name.startswith('http') else obj.image.url
        return None
