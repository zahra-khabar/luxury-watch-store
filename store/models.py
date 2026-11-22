from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SluggedMixinModel(models.Model):
    slug = models.SlugField(unique=True, allow_unicode=True)

    class Meta:
        abstract = True


class Brand(BaseModel):
    name = models.CharField(max_length=255)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    def __str__(self):
        return self.name



class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(BaseModel, SluggedMixinModel):
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('unisex', 'Unisex'),
    ]
    ORIGIN_CHOICES = [
        ('swiss', 'Swiss'),
        ('japan', 'Japan'),
        ('germany', 'Germany'),
        ('other', 'Other'),
    ]
    STRAP_CHOICES = [
        ('leather', 'Leather'),
        ('metal', 'Metal'),
        ('rubber', 'Rubber'),
        ('fabric', 'Fabric'),
    ]
    USAGE_CHOICES = [
        ('casual', 'Casual'),
        ('sport', 'Sport'),
        ('formal', 'Formal'),
        ('diving', 'Diving'),
    ]
    DESIGN_CHOICES = [
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('vintage', 'Vintage'),
    ]
    ENGINE_CHOICES = [
        ('automatic', 'Automatic'),
        ('quartz', 'Quartz'),
        ('manual', 'Manual'),
        ('smart', 'Smart'),
    ]

    title = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_discount = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_special = models.BooleanField(default=False)

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    origin = models.CharField(max_length=20, choices=ORIGIN_CHOICES)
    strap_material = models.CharField(max_length=20, choices=STRAP_CHOICES)
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES)
    design = models.CharField(max_length=20, choices=DESIGN_CHOICES)
    engine = models.CharField(max_length=20, choices=ENGINE_CHOICES)

    main_image = models.ImageField(upload_to='products/', blank=True, null=True)
    features = models.JSONField(default=dict, blank=True)
    is_luxury = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    stash = models.IntegerField(default=0)
    click_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')



class ProductColor(BaseModel, SluggedMixinModel):
    title = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, related_name='colors')



class Comment(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()

class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)

class Wishlist(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)