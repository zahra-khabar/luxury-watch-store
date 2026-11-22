from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import F, Avg
from .models import Product, Wishlist
from .serializers import ProductListSerializer, ProductDetailSerializer, WishlistSerializer


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.select_related('brand', 'category').all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    def get(self, request, slug):
        Product.objects.filter(slug=slug).update(click_count=F('click_count') + 1)

        product = get_object_or_404(
            Product.objects
            .select_related('brand', 'category')
            .prefetch_related('images', 'colors', 'comments__customer__user'),
            slug=slug
        )
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


class LuxurySpecialView(APIView):
    def get(self, request):
        products = Product.objects.filter(
            is_special=True,
            is_luxury=True,
            is_available=True
        ).only('title', 'price', 'gender', 'strap_material', 'engine')
        avg_price = Product.objects.filter(is_luxury=True).aggregate(Avg('price'))['price__avg']

        data = {
            'average_luxury_price': avg_price,
            'products': [
                {
                    'title': p.title,
                    'price': p.price,
                    'gender': p.get_gender_display(),
                    'strap_material': p.get_strap_material_display(),
                    'engine': p.get_engine_display(),
                } for p in products
            ]
        }
        return Response(data)


class WishlistView(APIView):
    def get(self, request):
        wishlists = Wishlist.objects.filter(
            customer__user_id=1
        ).select_related('product', 'customer__user')
        serializer = WishlistSerializer(wishlists, many=True)
        return Response(serializer.data)