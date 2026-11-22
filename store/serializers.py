from rest_framework import serializers
from .models import Product, Wishlist, Brand, Category, ProductImage, ProductColor, Comment

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'price', 'brand', 'category', 'is_available', 'stash']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['id', 'title']  # چون مدل ما title داشت
class CommentSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(source='customer.user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'customer_username', 'body', 'created_at']
class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
class WishlistSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=12, decimal_places=2, read_only=True)
    product_stash = serializers.IntegerField(source='product.stash', read_only=True)
    product_main_image = serializers.ImageField(source='product.main_image', read_only=True)

    customer_username = serializers.CharField(source='customer.user.username', read_only=True)
    customer_email = serializers.EmailField(source='customer.user.email', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone_number', read_only=True)

    class Meta:
        model = Wishlist
        fields = [
            'product_title', 'product_slug', 'product_price', 'product_stash', 'product_main_image',
            'customer_username', 'customer_email', 'customer_phone'
        ]