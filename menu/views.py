from rest_framework.generics import ListAPIView
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryListView(ListAPIView):
    """GET /api/categories/ — list all menu categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(ListAPIView):
    """GET /api/products/ — list all available products."""
    serializer_class = ProductSerializer

    def get_queryset(self):
        return (
            Product.objects
            .filter(is_available=True)
            .select_related('category')
        )
