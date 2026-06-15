from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from config import app_gv as gv

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=250, unique=True)

    image = models.ImageField(
        upload_to='category/',
        null=True,
        blank=True
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    sort_order = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=False)

    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    datamode = models.CharField(
        max_length=20,
        default='A',
        choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'category'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True)

    sku = models.CharField(
        max_length=100,
        unique=True,
        db_index=True
    )

    short_description = models.TextField(
        null=True,
        blank=True
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to='products/'
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    stock = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_flash_sale = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_top_rated = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    datamode = models.CharField(
        max_length=20,
        default='A',
        choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'product'
        ordering = ['-created_on']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery'
    )

    image = models.ImageField(
        upload_to='products/gallery/'
    )

    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    datamode = models.CharField(
        max_length=20,
        default='A',
        choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'productimage'

    def __str__(self):
        return self.product.name


class HomePageVideo(models.Model):

    thumbnail_image = models.ImageField(
        upload_to='homepage/videos/'
    )

    video = models.FileField(
        upload_to='homepage/videos/'
    )

    cat_button = models.CharField(
        max_length=100
    )

    title = models.CharField(
        max_length=255
    )

    sort_order = models.PositiveIntegerField(
        default=1,
        help_text="1,2,3,4..."
    )

    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now=True
    )

    datamode = models.CharField(
        max_length=20,
        default='A',
        choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = "homepage_video"
        ordering = ['sort_order']

    def __str__(self):
        return self.title


class HeroBanner(models.Model):

    desktop_image = models.ImageField(
        upload_to='hero_banner/desktop/'
    )

    mobile_image = models.ImageField(
        upload_to='hero_banner/mobile/'
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    sort_order = models.PositiveIntegerField(
        default=1
    )

    is_active = models.BooleanField(
        default=True
    )

    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now=True
    )

    datamode = models.CharField(
        max_length=20,
        default='A',
        choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = "hero_banner"
        ordering = ['sort_order']

    def __str__(self):
        return self.title if self.title else f"Banner {self.id}"


# ─────────────────────────────────────────────────────────────────────────────
# ADD THESE MODELS to your existing models.py
# (Category, Product, ProductImage, HomePageVideo, HeroBanner already exist)
# ─────────────────────────────────────────────────────────────────────────────

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from config import app_gv as gv


# ══════════════════════════════════════════════════════════════════════════════
# Customer
# ══════════════════════════════════════════════════════════════════════════════

class Customer(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email      = models.EmailField(unique=True, db_index=True)
    phone      = PhoneNumberField(blank=True, null=True)
    gender     = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(
        upload_to='customers/profiles/',
        blank=True,
        null=True
    )
    is_verified   = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(
        default=True,
        help_text="Subscribed to marketing emails"
    )

    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode   = models.CharField(
        max_length=20, default='A', choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'customer'
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


# ══════════════════════════════════════════════════════════════════════════════
# Address
# ══════════════════════════════════════════════════════════════════════════════
# wopper/models.py - Updated to use User instead of Customer

from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from config import app_gv as gv
from django.conf import settings 
User = get_user_model()

# ... keep your existing Category, Product, ProductImage, HomePageVideo, HeroBanner models as they are ...


# ══════════════════════════════════════════════════════════════════════════════
# Address - Updated to use User
# ══════════════════════════════════════════════════════════════════════════════

class Address(models.Model):

    ADDRESS_TYPE_CHOICES = [
        ('home',   'Home'),
        ('work',   'Work'),
        ('other',  'Other'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Changed from 'User' to settings.AUTH_USER_MODEL
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    address_type = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPE_CHOICES,
        default='home'
    )
    full_name    = models.CharField(max_length=200)
    phone        = PhoneNumberField()
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city         = models.CharField(max_length=100)
    state        = models.CharField(max_length=100)
    pincode      = models.CharField(max_length=20)
    country      = models.CharField(max_length=100, default='India')
    is_default   = models.BooleanField(default=False)

    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode   = models.CharField(
        max_length=20, default='A', choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'address'
        ordering = ['-is_default', '-created_on']

    def __str__(self):
        return f"{self.full_name} – {self.city}, {self.state}"


# ══════════════════════════════════════════════════════════════════════════════
# Coupon (no changes needed)
# ══════════════════════════════════════════════════════════════════════════════

class Coupon(models.Model):

    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed',      'Fixed Amount'),
    ]

    code          = models.CharField(max_length=50, unique=True, db_index=True)
    description   = models.TextField(blank=True, null=True)
    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default='percentage'
    )
    discount_value   = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    maximum_discount_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        blank=True, null=True,
        help_text="Cap for percentage discounts"
    )
    usage_limit      = models.PositiveIntegerField(
        blank=True, null=True,
        help_text="Max total uses. Leave blank for unlimited."
    )
    usage_count      = models.PositiveIntegerField(default=0)
    per_user_limit   = models.PositiveIntegerField(
        default=1,
        help_text="Max uses per customer"
    )
    valid_from       = models.DateTimeField()
    valid_until      = models.DateTimeField()
    is_active        = models.BooleanField(default=True)

    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode   = models.CharField(
        max_length=20, default='A', choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'coupon'
        ordering = ['-created_on']

    def __str__(self):
        return self.code


# ══════════════════════════════════════════════════════════════════════════════
# PaymentGateway (no changes needed)
# ══════════════════════════════════════════════════════════════════════════════

class PaymentGateway(models.Model):

    name        = models.CharField(max_length=100)
    code        = models.CharField(
        max_length=50, unique=True,
        help_text="e.g. razorpay, stripe, cod"
    )
    description = models.TextField(blank=True, null=True)
    logo        = models.ImageField(
        upload_to='payment_gateways/',
        blank=True, null=True
    )
    is_active   = models.BooleanField(default=True)
    sort_order  = models.PositiveIntegerField(default=1)

    config_json = models.TextField(
        blank=True, null=True,
        help_text="Optional JSON config (non-sensitive)"
    )

    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode   = models.CharField(
        max_length=20, default='A', choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'payment_gateway'
        ordering = ['sort_order']

    def __str__(self):
        return self.name


# ══════════════════════════════════════════════════════════════════════════════
# Cart - Updated to use User
# ══════════════════════════════════════════════════════════════════════════════

class Cart(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Changed from 'User'
        on_delete=models.CASCADE,
        related_name='cart',
        blank=True, null=True
    )
    session_key = models.CharField(
        max_length=100,
        blank=True, null=True,
        help_text="For guest / anonymous carts"
    )
    coupon     = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='carts'
    )

    created_by = models.CharField(max_length=8, blank=True)
    updated_by = models.CharField(max_length=8, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode   = models.CharField(
        max_length=20, default='A', choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'cart'
        ordering = ['-updated_on']

    def __str__(self):
        return f"Cart – {self.user or self.session_key}"


# ══════════════════════════════════════════════════════════════════════════════
# CartItem (no changes needed)
# ══════════════════════════════════════════════════════════════════════════════

class CartItem(models.Model):

    cart     = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product  = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    price    = models.DecimalField(
        max_digits=12, decimal_places=2,
        help_text="Unit price at time of adding to cart"
    )

    created_by = models.CharField(max_length=8, blank=True)
    updated_by = models.CharField(max_length=8, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode   = models.CharField(
        max_length=20, default='A', choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'cart_item'
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity


# ══════════════════════════════════════════════════════════════════════════════
# Wishlist - Updated to use User
# ══════════════════════════════════════════════════════════════════════════════
class Wishlist(models.Model):
    user = models.ForeignKey(  # Changed from OneToOneField to ForeignKey
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wishlist_items',
        blank=True, null=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='wishlisted_by'
    )
    
    created_by = models.CharField(max_length=8, blank=True)
    updated_by = models.CharField(max_length=8, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(
        max_length=20, default='A', choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'wishlist'
        unique_together = ('user', 'product')  # This prevents duplicate user-product pairs
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.user} ♥ {self.product.name}"
# ══════════════════════════════════════════════════════════════════════════════
# Order - Updated to use User
# ══════════════════════════════════════════════════════════════════════════════

class Order(models.Model):

    ORDER_STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('confirmed',  'Confirmed'),
        ('processing', 'Processing'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
        ('returned',   'Returned'),
        ('refunded',   'Refunded'),
    ]

    user             = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='orders'
    )
    order_number    = models.CharField(
        max_length=50, unique=True, db_index=True
    )
    status          = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending'
    )

    # Snapshot of shipping address at time of order
    shipping_full_name    = models.CharField(max_length=200)
    shipping_phone        = models.CharField(max_length=20)
    shipping_address_line1 = models.CharField(max_length=255)
    shipping_address_line2 = models.CharField(max_length=255, blank=True, null=True)
    shipping_city         = models.CharField(max_length=100)
    shipping_state        = models.CharField(max_length=100)
    shipping_pincode      = models.CharField(max_length=20)
    shipping_country      = models.CharField(max_length=100, default='India')

    coupon          = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='orders'
    )

    subtotal        = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount    = models.DecimalField(max_digits=12, decimal_places=2)

    notes           = models.TextField(blank=True, null=True)
    delivered_on    = models.DateTimeField(blank=True, null=True)

    created_by = models.CharField(max_length=8, blank=True)
    updated_by = models.CharField(max_length=8, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode   = models.CharField(
        max_length=20, default='A', choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'order'
        ordering = ['-created_on']

    def __str__(self):
        return self.order_number


# ══════════════════════════════════════════════════════════════════════════════
# OrderItem (no changes needed - keep as is)
# ══════════════════════════════════════════════════════════════════════════════

class OrderItem(models.Model):

    order       = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product     = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items'
    )
    product_name  = models.CharField(max_length=255)
    product_sku   = models.CharField(max_length=100)
    product_image = models.CharField(max_length=500, blank=True, null=True)
    unit_price    = models.DecimalField(max_digits=12, decimal_places=2)
    quantity      = models.PositiveIntegerField(default=1)
    total_price   = models.DecimalField(max_digits=12, decimal_places=2)

    created_by = models.CharField(max_length=8, blank=True)
    updated_by = models.CharField(max_length=8, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode   = models.CharField(
        max_length=20, default='A', choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'order_item'

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"


# ══════════════════════════════════════════════════════════════════════════════
# Payment - Updated to use User
# ══════════════════════════════════════════════════════════════════════════════

class Payment(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('success',   'Success'),
        ('failed',    'Failed'),
        ('refunded',  'Refunded'),
        ('cancelled', 'Cancelled'),
    ]

    order           = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    payment_gateway = models.ForeignKey(
        PaymentGateway,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='payments'
    )
    transaction_id  = models.CharField(
        max_length=200, unique=True, db_index=True
    )
    gateway_order_id = models.CharField(
        max_length=200, blank=True, null=True
    )
    amount          = models.DecimalField(max_digits=12, decimal_places=2)
    currency        = models.CharField(max_length=10, default='INR')
    status          = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    gateway_response = models.TextField(
        blank=True, null=True,
        help_text="Raw JSON response from the gateway"
    )
    paid_on         = models.DateTimeField(blank=True, null=True)

    created_by = models.CharField(max_length=8, blank=True)
    updated_by = models.CharField(max_length=8, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode   = models.CharField(
        max_length=20, default='A', choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'payment'
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.transaction_id} – {self.status}"


# ══════════════════════════════════════════════════════════════════════════════
# ProductReview - Updated to use User
# ══════════════════════════════════════════════════════════════════════════════

class ProductReview(models.Model):

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    product   = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user      = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reviews'
    )
    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='review'
    )
    rating     = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    title      = models.CharField(max_length=255, blank=True, null=True)
    body       = models.TextField()
    is_approved = models.BooleanField(default=False)

    created_by = models.CharField(max_length=8, blank=True)
    updated_by = models.CharField(max_length=8, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode   = models.CharField(
        max_length=20, default='A', choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'product_review'
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.product.name} – {self.rating}★"





# ══════════════════════════════════════════════════════════════════════════════
# Newsletter
# ══════════════════════════════════════════════════════════════════════════════

class Newsletter(models.Model):

    email      = models.EmailField(unique=True, db_index=True)
    is_active  = models.BooleanField(default=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    created_by = models.CharField(max_length=8, blank=True)
    updated_by = models.CharField(max_length=8, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode   = models.CharField(
        max_length=20, default='A', choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'newsletter'
        ordering = ['-created_on']

    def __str__(self):
        return self.email


# ══════════════════════════════════════════════════════════════════════════════
# ContactUs
# ══════════════════════════════════════════════════════════════════════════════

class ContactUs(models.Model):

    STATUS_CHOICES = [
        ('new',         'New'),
        ('in_progress', 'In Progress'),
        ('resolved',    'Resolved'),
        ('closed',      'Closed'),
    ]

    name       = models.CharField(max_length=200)
    email      = models.EmailField()
    phone      = PhoneNumberField(blank=True, null=True)
    subject    = models.CharField(max_length=255)
    message    = models.TextField()
    status     = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    admin_notes = models.TextField(
        blank=True, null=True,
        help_text="Internal notes (not visible to customer)"
    )
    replied_on = models.DateTimeField(blank=True, null=True)

    created_by = models.CharField(max_length=8, blank=True)
    updated_by = models.CharField(max_length=8, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode   = models.CharField(
        max_length=20, default='A', choices=gv.DATAMODE_CHOICES
    )

    class Meta:
        db_table = 'contact_us'
        ordering = ['-created_on']
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us Entries'

    def __str__(self):
        return f"{self.name} – {self.subject}"


# ══════════════════════════════════════════════════════════════════════════════
# SiteSettings  (singleton – enforce via save())
# ══════════════════════════════════════════════════════════════════════════════

class SiteSettings(models.Model):

    site_name        = models.CharField(max_length=200)
    site_tagline     = models.CharField(max_length=255, blank=True, null=True)
    site_email       = models.EmailField()
    site_phone       = PhoneNumberField(blank=True, null=True)
    site_phone_alt   = PhoneNumberField(blank=True, null=True)
    site_address     = models.TextField(blank=True, null=True)
    site_logo        = models.ImageField(
        upload_to='site/', blank=True, null=True
    )
    site_favicon     = models.ImageField(
        upload_to='site/', blank=True, null=True
    )

    # Social links
    facebook_url     = models.URLField(blank=True, null=True)
    instagram_url    = models.URLField(blank=True, null=True)
    twitter_url      = models.URLField(blank=True, null=True)
    youtube_url      = models.URLField(blank=True, null=True)
    linkedin_url     = models.URLField(blank=True, null=True)

    # SEO
    meta_title       = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords    = models.TextField(blank=True, null=True)
    google_analytics_id = models.CharField(max_length=50, blank=True, null=True)

    # Policies
    privacy_policy   = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    return_policy    = models.TextField(blank=True, null=True)
    shipping_policy  = models.TextField(blank=True, null=True)

    # Commerce settings
    currency_code    = models.CharField(max_length=5, default='INR')
    currency_symbol  = models.CharField(max_length=5, default='₹')
    free_shipping_above = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="0 = no free shipping threshold"
    )
    tax_percentage   = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )

    created_by = models.CharField(max_length=8, blank=True)
    updated_by = models.CharField(max_length=8, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'site_settings'
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Singleton enforcement: only one record allowed
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            'site_name': 'My Store',
            'site_email': 'admin@mystore.com',
            'created_by': 'system',
            'updated_by': 'system',
        })
        return obj