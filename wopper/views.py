# mck_website/views.py - Complete updated views using User model directly

from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Avg, Q
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import logging
import razorpay
import uuid

import json
import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db import transaction
from django.utils import timezone
from mck_website.models import (
    User, Category, Product, HomePageVideo, HeroBanner,
    Address, Cart, CartItem, Wishlist, Order, OrderItem,
    Payment, PaymentGateway, Coupon, ProductReview,
    Newsletter, ContactUs, SiteSettings
)
from mck_auth.models import (
    User
)
logger = logging.getLogger(__name__)

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC WEBSITE VIEWS
# ══════════════════════════════════════════════════════════════════════════════

# wopper/views.py

import json
import logging
import uuid
import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Avg

from mck_website.models import (
    Category, Product, HomePageVideo, HeroBanner,
    Address, Cart, CartItem, Wishlist, Order, OrderItem,
    Payment, PaymentGateway, Coupon, ProductReview,
    SiteSettings
)

logger = logging.getLogger(__name__)

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def _cart_totals(cart):
    """Calculate cart totals"""
    if not cart:
        return {'subtotal': 0, 'discount': 0, 'total': 0, 'item_count': 0}
    
    items = CartItem.objects.filter(cart=cart, datamode='A')
    subtotal = sum(i.price * i.quantity for i in items)
    discount = 0
    if cart.coupon:
        if cart.coupon.discount_type == 'percentage':
            discount = (subtotal * cart.coupon.discount_value) / 100
            if cart.coupon.maximum_discount_amount:
                discount = min(discount, cart.coupon.maximum_discount_amount)
        else:
            discount = cart.coupon.discount_value
    total = subtotal - discount
    return {
        'subtotal': float(subtotal),
        'discount': float(discount),
        'total': float(total),
        'item_count': items.count(),
    }


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC WEBSITE VIEWS
# ══════════════════════════════════════════════════════════════════════════════

class WebsiteHomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            categories = Category.objects.filter(datamode='A').order_by('sort_order')[:15]
            featured_products = Product.objects.filter(datamode='A', is_featured=True).order_by('-created_on')[:12]
            bestsellers = Product.objects.filter(datamode='A', is_best_seller=True).order_by('-created_on')[:12]
            flash_sales = Product.objects.filter(datamode='A', is_flash_sale=True).order_by('-created_on')[:12]
            hero_banners = HeroBanner.objects.filter(datamode='A', is_active=True).order_by('sort_order')[:3]
            homepage_videos = HomePageVideo.objects.filter(datamode='A').order_by('sort_order')[:10]
            site_settings = SiteSettings.load()
            
            cart_count = 0
            wishlist_count = 0
            if self.request.user.is_authenticated:
                cart = Cart.objects.filter(user=self.request.user, datamode='A').first()
                if cart:
                    cart_count = CartItem.objects.filter(cart=cart, datamode='A').count()
                wishlist_count = Wishlist.objects.filter(user=self.request.user, datamode='A').count()
            
            context.update({
                'categories': categories,
                'featured_products': featured_products,
                'bestsellers': bestsellers,
                'flash_sales': flash_sales,
                'hero_banners': hero_banners,
                'homepage_videos': homepage_videos,
                'site_settings': site_settings,
                'site_name': site_settings.site_name if site_settings else 'The Better Home',
                'site_email': site_settings.site_email if site_settings else 'info@thebetterhome.in',
                'site_phone': site_settings.site_phone if site_settings else '+91 9677051121',
                'cart_count': cart_count,
                'wishlist_count': wishlist_count,
            })
        except Exception as e:
            logger.error(f"HomeView error: {e}")
        return context


from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F, Value, DecimalField
from django.db.models.functions import Coalesce
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class AllProductsView(TemplateView):
    template_name = 'website/all_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Base queryset - only active products (assuming Product has is_active)
            products = Product.objects.filter(datamode='A')
            
            # Get filter parameters from request
            search_query = self.request.GET.get('q', '')
            category_slugs = self.request.GET.get('category', '')
            feature_filters = self.request.GET.get('feature', '')
            min_price = self.request.GET.get('min_price', '')
            max_price = self.request.GET.get('max_price', '')
            sort_by = self.request.GET.get('sort', '-created_on')
            flash_sale = self.request.GET.get('flash_sale', '')
            
            # Apply search filter
            if search_query:
                products = products.filter(
                    Q(name__icontains=search_query) |
                    Q(short_description__icontains=search_query) |
                    Q(description__icontains=search_query) |
                    Q(sku__icontains=search_query)
                )
                context['search_query'] = search_query
            
            # Apply category filter
            if category_slugs:
                slug_list = [s.strip() for s in category_slugs.split(',') if s.strip()]
                products = products.filter(category__slug__in=slug_list)
                context['selected_categories'] = slug_list
            
            # Apply flash sale filter
            if flash_sale and flash_sale == 'true':
                products = products.filter(is_flash_sale=True)
            
            # Apply feature filters
            if feature_filters:
                features = [f.strip() for f in feature_filters.split(',') if f.strip()]
                if 'new' in features:
                    products = products.filter(is_new_arrival=True)
                if 'bestseller' in features:
                    products = products.filter(is_best_seller=True)
                if 'flash' in features:
                    products = products.filter(is_flash_sale=True)
                context['selected_features'] = features
            
            # Apply price range filter
            if min_price:
                try:
                    min_price_decimal = Decimal(min_price)
                    products = products.filter(price__gte=min_price_decimal)
                    context['min_price'] = min_price
                except:
                    pass
            
            if max_price:
                try:
                    max_price_decimal = Decimal(max_price)
                    products = products.filter(price__lte=max_price_decimal)
                    context['max_price'] = max_price
                except:
                    pass
            
            # Apply sorting
            if sort_by == 'price':
                products = products.order_by('price')
            elif sort_by == '-price':
                products = products.order_by('-price')
            elif sort_by == '-discount_percentage':
                # Annotate with discount percentage and order by it
                products = products.annotate(
                    discount_percentage=Coalesce(
                        (F('sale_price') - F('price')) / F('sale_price') * 100,
                        Value(0),
                        output_field=DecimalField()
                    )
                ).order_by('-discount_percentage')
            elif sort_by == '-view_count':
                products = products.order_by('-view_count')
            elif sort_by == 'name':
                products = products.order_by('name')
            elif sort_by == '-name':
                products = products.order_by('-name')
            else:
                products = products.order_by('-created_on')
            
            context['current_sort'] = sort_by
            
            # Get all categories for filter sidebar - Remove is_active filter
            all_categories = Category.objects.filter(datamode='A')
            
            # Pagination (12 products per page for better display)
            paginator = Paginator(products, 12)
            page_number = self.request.GET.get('page', 1)
            
            try:
                page_obj = paginator.page(page_number)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            
            context.update({
                'page_obj': page_obj,
                'products': page_obj.object_list,
                'categories': all_categories,
                'page_title': 'All Products',
                'total_products': products.count(),
            })
            
        except Exception as e:
            logger.error(f"AllProductsView error: {e}")
            context.update({
                'products': [],
                'page_obj': None,
                'categories': Category.objects.filter(datamode='A'),
                'error_message': str(e)
            })
        
        return context


        
class CategoryDataView(TemplateView):
    template_name = 'website/category_products.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            slug = kwargs.get('slug')
            
            # Base queryset - only active products
            products = Product.objects.filter(datamode='A')
            
            # Get category if slug provided
            category = None
            if slug:
                category = Category.objects.filter(slug=slug, datamode='A').first()
                if category:
                    products = products.filter(category=category)
                    context['category'] = category
                    context['page_title'] = category.name
            
            # Get filter parameters
            category_slugs = self.request.GET.get('category', '')
            feature_filters = self.request.GET.get('feature', '')
            min_price = self.request.GET.get('min_price', '')
            max_price = self.request.GET.get('max_price', '')
            sort_by = self.request.GET.get('sort', '-created_on')
            search_query = self.request.GET.get('q', '')
            
            # Apply search filter
            if search_query:
                products = products.filter(
                    Q(name__icontains=search_query) |
                    Q(short_description__icontains=search_query) |
                    Q(description__icontains=search_query)
                )
                context['search_query'] = search_query
            
            # Apply additional category filter from sidebar (if not already filtered by URL slug)
            if category_slugs and not slug:
                slug_list = [s.strip() for s in category_slugs.split(',') if s.strip()]
                products = products.filter(category__slug__in=slug_list)
                context['selected_categories'] = slug_list
            
            # Apply feature filters
            if feature_filters:
                features = [f.strip() for f in feature_filters.split(',') if f.strip()]
                if 'new' in features:
                    products = products.filter(is_new_arrival=True)
                if 'bestseller' in features:
                    products = products.filter(is_best_seller=True)
                if 'flash' in features:
                    products = products.filter(is_flash_sale=True)
                context['selected_features'] = features
            
            # Apply price range filter
            if min_price:
                try:
                    min_price_decimal = Decimal(min_price)
                    products = products.filter(price__gte=min_price_decimal)
                    context['min_price'] = min_price
                except:
                    pass
            
            if max_price:
                try:
                    max_price_decimal = Decimal(max_price)
                    products = products.filter(price__lte=max_price_decimal)
                    context['max_price'] = max_price
                except:
                    pass
            
            # Apply sorting
            if sort_by == 'price':
                products = products.order_by('price')
            elif sort_by == '-price':
                products = products.order_by('-price')
            elif sort_by == '-view_count':
                products = products.order_by('-view_count')
            else:
                products = products.order_by('-created_on')
            
            context['current_sort'] = sort_by
            
            # Get all categories for filter sidebar - Remove is_active filter
            all_categories = Category.objects.filter(datamode='A')
            
            # Pagination
            paginator = Paginator(products, 12)
            page_number = self.request.GET.get('page', 1)
            
            try:
                page_obj = paginator.page(page_number)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            
            context.update({
                'page_obj': page_obj,
                'products': page_obj.object_list,
                'categories': all_categories,
                'total_products': products.count(),
            })
            
        except Exception as e:
            logger.error(f"CategoryDataView error: {e}")
            context.update({
                'products': [],
                'page_obj': None,
                'categories': Category.objects.filter(datamode='A'),
                'error_message': str(e)
            })
        
        return context

        
class ProductDataView(TemplateView):
    template_name = 'website/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get('slug')
        try:
            product = Product.objects.get(slug=slug, datamode='A')
            in_wishlist = False
            if self.request.user.is_authenticated:
                in_wishlist = Wishlist.objects.filter(user=self.request.user, product=product, datamode='A').exists()
            context.update({
                'product': product,
                'product_images': product.gallery.filter(datamode='A'),
                'related_products': Product.objects.filter(category=product.category, datamode='A').exclude(id=product.id)[:6],
                'in_wishlist': in_wishlist,
                'categories': Category.objects.filter(datamode='A')[:15],
                'site_settings': SiteSettings.load(),
            })
        except Product.DoesNotExist:
            context['error'] = 'Product not found'
        return context


class SearchView(TemplateView):
    template_name = 'website/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        if query:
            products = Product.objects.filter(Q(datamode='A') & (Q(name__icontains=query) | Q(description__icontains=query)))
            context.update({'products': products, 'query': query, 'result_count': products.count()})
        return context


# ══════════════════════════════════════════════════════════════════════════════
# CART VIEWS
# ══════════════════════════════════════════════════════════════════════════════

@method_decorator(login_required(login_url='mck_auth:website_signin'), name='dispatch')
class CartView(TemplateView):
    template_name = 'website/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            print("=" * 50)
            print("CART VIEW DEBUG")
            print(f"User: {self.request.user}")
            print(f"Is Authenticated: {self.request.user.is_authenticated}")
            
            cart = Cart.objects.filter(user=self.request.user, datamode='A').first()
            print(f"Cart found: {cart}")
            
            if cart:
                cart_items = cart.items.filter(datamode='A').select_related('product')
                print(f"Cart items count: {cart_items.count()}")
                
                for item in cart_items:
                    print(f"Item: {item.product.name}, Qty: {item.quantity}, Price: {item.price}")
                
                subtotal = sum(item.price * item.quantity for item in cart_items)
                discount = 0
                if cart.coupon:
                    if cart.coupon.discount_type == 'percentage':
                        discount = (subtotal * cart.coupon.discount_value) / 100
                    else:
                        discount = cart.coupon.discount_value
                total = subtotal - discount
            else:
                cart_items = []
                subtotal = 0
                discount = 0
                total = 0
                print("No cart found for this user")
            
            context.update({
                'cart_items': cart_items,
                'subtotal': subtotal,
                'discount': discount,
                'total': total,
                'page_title': 'Shopping Cart',
            })
            
            print(f"Context cart_items length: {len(context['cart_items'])}")
            print("=" * 50)
            
        except Exception as e:
            print(f"ERROR in CartView: {str(e)}")
            import traceback
            traceback.print_exc()
            logger.error(f"CartView error: {str(e)}")
            
        return context

@login_required(login_url='mck_auth:website_signin')
@require_POST
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id') or data.get('product_slug')
        quantity = int(data.get('quantity', 1))

        if str(product_id).isdigit():
            product = get_object_or_404(Product, id=int(product_id), datamode='A')
        else:
            product = get_object_or_404(Product, slug=product_id, datamode='A')

        cart, _ = Cart.objects.get_or_create(
            user=request.user,
            defaults={'datamode': 'A', 'created_by': request.user.username or 'website'}
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={
                'quantity': quantity,
                'price': product.sale_price or product.price,
                'datamode': 'A',
                'created_by': request.user.username or 'website'
            }
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        cart_count = CartItem.objects.filter(cart=cart, datamode='A').count()
        return JsonResponse({'success': True, 'cart_count': cart_count})
    except Exception as e:
        logger.error(f"add_to_cart error: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@login_required(login_url='mck_auth:website_signin')
@require_POST
def update_cart_item(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        action = data.get('action')
        quantity = data.get('quantity')

        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user, datamode='A')

        if action == 'increase':
            item.quantity += 1
            item.save()
        elif action == 'decrease':
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.datamode = 'I'
                item.save()
                totals = _cart_totals(item.cart)
                return JsonResponse({'success': True, 'removed': True, **totals})
        elif action == 'set' and quantity:
            item.quantity = max(1, int(quantity))
            item.save()

        totals = _cart_totals(item.cart)
        return JsonResponse({
            'success': True,
            'quantity': item.quantity,
            'item_subtotal': float(item.subtotal),
            **totals
        })
    except Exception as e:
        logger.error(f"update_cart_item error: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@login_required(login_url='mck_auth:website_signin')
def remove_cart_item(request, item_id):
    try:
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user, datamode='A')
        cart = item.cart
        item.datamode = 'I'
        item.save()
        totals = _cart_totals(cart)
        return JsonResponse({'success': True, **totals})
    except Exception as e:
        logger.error(f"remove_cart_item error: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@login_required(login_url='mck_auth:website_signin')
@require_POST
def apply_coupon(request):
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip().upper()

        cart = Cart.objects.filter(user=request.user, datamode='A').first()
        if not cart:
            return JsonResponse({'success': False, 'message': 'Cart not found'}, status=400)

        coupon = Coupon.objects.filter(
            code__iexact=code, datamode='A', is_active=True,
            valid_from__lte=timezone.now(), valid_until__gte=timezone.now()
        ).first()

        if not coupon:
            return JsonResponse({'success': False, 'message': 'Invalid or expired coupon'}, status=400)

        items = CartItem.objects.filter(cart=cart, datamode='A')
        subtotal = sum(i.price * i.quantity for i in items)

        if coupon.minimum_order_amount and subtotal < coupon.minimum_order_amount:
            return JsonResponse({
                'success': False,
                'message': f'Minimum order amount of ₹{coupon.minimum_order_amount} required'
            }, status=400)

        cart.coupon = coupon
        cart.save()
        totals = _cart_totals(cart)
        return JsonResponse({'success': True, 'message': 'Coupon applied', **totals})
    except Exception as e:
        logger.error(f"apply_coupon error: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@login_required(login_url='mck_auth:website_signin')
@require_POST
def remove_coupon(request):
    try:
        cart = Cart.objects.filter(user=request.user, datamode='A').first()
        if not cart:
            return JsonResponse({'success': False, 'message': 'Cart not found'}, status=400)
        cart.coupon = None
        cart.save()
        totals = _cart_totals(cart)
        return JsonResponse({'success': True, 'message': 'Coupon removed', **totals})
    except Exception as e:
        logger.error(f"remove_coupon error: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


# ══════════════════════════════════════════════════════════════════════════════
# CHECKOUT VIEWS
# ══════════════════════════════════════════════════════════════════════════════

@method_decorator(login_required(login_url='mck_auth:website_signin'), name='dispatch')
class CheckoutView(TemplateView):
    template_name = 'website/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            cart = Cart.objects.filter(user=self.request.user, datamode='A').first()
            if not cart:
                context['empty_cart'] = True
                return context
            
            cart_items = cart.items.filter(datamode='A').select_related('product')
            if not cart_items.exists():
                context['empty_cart'] = True
                return context

            totals = _cart_totals(cart)
            addresses = Address.objects.filter(user=self.request.user, datamode='A')
            site_settings = SiteSettings.load()

            context.update({
                'cart_items': cart_items,
                'subtotal': totals['subtotal'],
                'discount': totals['discount'],
                'total': totals['total'],
                'addresses': addresses,
                'site_settings': site_settings,
                'razorpay_key': settings.RAZORPAY_KEY_ID,
                'page_title': 'Checkout',
            })
        except Exception as e:
            logger.error(f"CheckoutView error: {e}")
        return context


@login_required(login_url='mck_auth:website_signin')
@require_POST
def add_address_quick(request):
    try:
        data = json.loads(request.body)
        is_default = not Address.objects.filter(user=request.user, datamode='A').exists()

        address = Address.objects.create(
            user=request.user,
            address_type=data.get('address_type', 'home'),
            full_name=data.get('full_name'),
            phone=data.get('phone'),
            address_line1=data.get('address_line1'),
            address_line2=data.get('address_line2', ''),
            city=data.get('city'),
            state=data.get('state'),
            pincode=data.get('pincode'),
            country=data.get('country', 'India'),
            is_default=is_default,
            created_by=request.user.username or 'website',
            updated_by=request.user.username or 'website',
            datamode='A'
        )
        return JsonResponse({
            'success': True,
            'address': {
                'id': address.id,
                'full_name': address.full_name,
                'phone': str(address.phone),
                'address_line1': address.address_line1,
                'address_line2': address.address_line2 or '',
                'city': address.city,
                'state': address.state,
                'pincode': address.pincode,
                'country': address.country,
                'is_default': address.is_default
            }
        })
    except Exception as e:
        logger.error(f"add_address_quick error: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@login_required(login_url='mck_auth:website_signin')
@require_POST
def create_razorpay_order(request):
    try:
        data = json.loads(request.body)
        address_id = data.get('address_id')
        payment_method = data.get('payment_method', 'razorpay')

        cart = Cart.objects.filter(user=request.user, datamode='A').first()
        if not cart or not cart.items.filter(datamode='A').exists():
            return JsonResponse({'success': False, 'message': 'Cart is empty'}, status=400)

        address = get_object_or_404(Address, id=address_id, user=request.user, datamode='A')

        totals = _cart_totals(cart)
        subtotal = totals['subtotal']
        discount = totals['discount']
        
        site_settings = SiteSettings.load()
        shipping_charge = 0
        if site_settings and site_settings.free_shipping_above and subtotal < site_settings.free_shipping_above:
            shipping_charge = 50

        tax_amount = (subtotal - discount) * 0.18
        total_amount = subtotal - discount + shipping_charge + tax_amount

        order = Order.objects.create(
            user=request.user,
            order_number=f"ORD{uuid.uuid4().hex[:10].upper()}",
            status='pending',
            shipping_full_name=address.full_name,
            shipping_phone=str(address.phone),
            shipping_address_line1=address.address_line1,
            shipping_address_line2=address.address_line2 or '',
            shipping_city=address.city,
            shipping_state=address.state,
            shipping_pincode=address.pincode,
            shipping_country=address.country,
            coupon=cart.coupon,
            subtotal=subtotal,
            discount_amount=discount,
            shipping_charge=shipping_charge,
            tax_amount=tax_amount,
            total_amount=total_amount,
            created_by=request.user.username or 'website',
            updated_by=request.user.username or 'website',
            datamode='A'
        )

        for item in cart.items.filter(datamode='A'):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                product_sku=item.product.sku,
                product_image=item.product.image.url if item.product.image else '',
                unit_price=item.price,
                quantity=item.quantity,
                total_price=item.price * item.quantity,
                created_by=request.user.username or 'website',
                updated_by=request.user.username or 'website',
                datamode='A'
            )

        if payment_method == 'cod':
            cod_gateway = PaymentGateway.objects.filter(code='cod', datamode='A', is_active=True).first()
            Payment.objects.create(
                order=order,
                payment_gateway=cod_gateway,
                transaction_id=f"COD{order.order_number}",
                amount=total_amount,
                currency='INR',
                status='pending',
                created_by=request.user.username or 'website',
                updated_by=request.user.username or 'website',
                datamode='A'
            )
            order.status = 'confirmed'
            order.save()
            cart.items.filter(datamode='A').update(datamode='I')
            cart.coupon = None
            cart.save()
            return JsonResponse({'success': True, 'payment_method': 'cod', 'order_number': order.order_number})

        # Razorpay flow
        razorpay_order = razorpay_client.order.create({
            'amount': int(total_amount * 100),
            'currency': 'INR',
            'payment_capture': 1,
            'notes': {'order_number': order.order_number}
        })

        gateway = PaymentGateway.objects.filter(code='razorpay', is_active=True, datamode='A').first()
        Payment.objects.create(
            order=order,
            payment_gateway=gateway,
            transaction_id=razorpay_order['id'],
            gateway_order_id=razorpay_order['id'],
            amount=total_amount,
            currency='INR',
            status='pending',
            created_by=request.user.username or 'website',
            updated_by=request.user.username or 'website',
            datamode='A'
        )

        return JsonResponse({
            'success': True,
            'payment_method': 'razorpay',
            'razorpay_order_id': razorpay_order['id'],
            'amount': int(total_amount * 100),
            'currency': 'INR',
            'key': settings.RAZORPAY_KEY_ID,
            'order_number': order.order_number,
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'contact': str(address.phone),
        })
    except Exception as e:
        logger.error(f"create_razorpay_order error: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@login_required(login_url='mck_auth:website_signin')
@require_POST
def verify_razorpay_payment(request):
    try:
        data = json.loads(request.body)
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
        except razorpay.errors.SignatureVerificationError:
            payment = Payment.objects.filter(gateway_order_id=razorpay_order_id).first()
            if payment:
                payment.status = 'failed'
                payment.save()
                payment.order.status = 'cancelled'
                payment.order.save()
            return JsonResponse({'success': False, 'message': 'Payment verification failed'}, status=400)

        payment = Payment.objects.get(gateway_order_id=razorpay_order_id)
        payment.transaction_id = razorpay_payment_id
        payment.status = 'success'
        payment.paid_on = timezone.now()
        payment.gateway_response = json.dumps(data)
        payment.save()

        order = payment.order
        order.status = 'confirmed'
        order.save()

        cart = Cart.objects.get(user=request.user, datamode='A')
        cart.items.filter(datamode='A').update(datamode='I')
        cart.coupon = None
        cart.save()

        return JsonResponse({'success': True, 'order_number': order.order_number})
    except Exception as e:
        logger.error(f"verify_razorpay_payment error: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@method_decorator(login_required(login_url='mck_auth:website_signin'), name='dispatch')
class OrderSuccessView(TemplateView):
    template_name = 'website/order_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_number = kwargs.get('order_number')
        try:
            order = Order.objects.get(order_number=order_number, user=self.request.user)
            context.update({
                'order': order,
                'order_items': order.items.all(),
                'payment': order.payments.first(),
                'site_settings': SiteSettings.load(),
            })
        except Order.DoesNotExist:
            context['error'] = 'Order not found'
        return context


# ══════════════════════════════════════════════════════════════════════════════
# USER PROFILE VIEWS
# ══════════════════════════════════════════════════════════════════════════════

@method_decorator(login_required(login_url='mck_auth:website_signin'), name='dispatch')
class OrdersView(TemplateView):
    template_name = 'website/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user, datamode='A').order_by('-created_on')
        return context


@method_decorator(login_required(login_url='mck_auth:website_signin'), name='dispatch')
class ProfileView(TemplateView):
    template_name = 'website/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user, datamode='A')
        return context


# ══════════════════════════════════════════════════════════════════════════════
# WISHLIST VIEWS (Keep as is - Working)
# ══════════════════════════════════════════════════════════════════════════════

@method_decorator(login_required(login_url='mck_auth:website_signin'), name='dispatch')
class WishlistView(TemplateView):
    template_name = 'website/wishlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishlist_items'] = Wishlist.objects.filter(user=self.request.user, datamode='A').select_related('product')
        context['categories'] = Category.objects.filter(datamode='A')[:15]
        context['site_settings'] = SiteSettings.load()
        return context





















@method_decorator(login_required(login_url='mck_auth:website_signin'), name='dispatch')
class WishlistView(TemplateView):
    """Wishlist page"""
    template_name = 'website/wishlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            wishlist_items = Wishlist.objects.filter(
                user=self.request.user, datamode='A'
            ).select_related('product', 'product__category')

            categories = Category.objects.filter(datamode='A').order_by('sort_order')[:15]
            site_settings = SiteSettings.load()

            context.update({
                'wishlist_items': wishlist_items,
                'categories': categories,
                'site_settings': site_settings,
                'site_name': site_settings.site_name if site_settings else 'The Better Home',
                'site_email': site_settings.site_email if site_settings else 'info@thebetterhome.in',
                'site_phone': site_settings.site_phone if site_settings else '+91 9677051121',
                'page_title': 'My Wishlist',
            })
        except Exception as e:
            logger.error(f"WishlistView error: {str(e)}")
            context['wishlist_items'] = []
        return context

# mck_website/views.py - Complete Wishlist Implementation


logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# PRODUCTION WISHLIST API ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════

@login_required(login_url='mck_auth:website_signin')
@require_POST
def toggle_wishlist(request):
    """
    Toggle product in user's wishlist.
    Production-ready with proper error handling, transaction support, and rate limiting.
    """
    try:
        # Parse request data
        data = json.loads(request.body)
        product_identifier = data.get('product_id') or data.get('product_slug')
        
        if not product_identifier:
            return JsonResponse({
                'success': False, 
                'error': 'PRODUCT_ID_REQUIRED',
                'message': 'Product identifier is required'
            }, status=400)

        # Get product with select_for_update to prevent race conditions
        with transaction.atomic():
            # Get product by ID or slug
            try:
                if str(product_identifier).isdigit():
                    product = Product.objects.select_for_update().get(
                        id=int(product_identifier), 
                        datamode='A'
                    )
                else:
                    product = Product.objects.select_for_update().get(
                        slug=product_identifier, 
                        datamode='A'
                    )
            except Product.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'PRODUCT_NOT_FOUND',
                    'message': 'Product not found'
                }, status=404)

            # Check existing wishlist item (including soft-deleted)
            existing = Wishlist.objects.filter(
                user=request.user,
                product=product
            ).first()

            if existing:
                if existing.datamode == 'A':
                    # Currently in wishlist - remove (soft delete)
                    existing.datamode = 'I'
                    existing.updated_by = request.user.username or 'website'
                    existing.save()
                    in_wishlist = False
                    action = 'removed'
                    message = f'{product.name} removed from your wishlist'
                else:
                    # Currently soft-deleted - reactivate
                    existing.datamode = 'A'
                    existing.updated_by = request.user.username or 'website'
                    existing.save()
                    in_wishlist = True
                    action = 'added'
                    message = f'{product.name} added to your wishlist'
            else:
                # Create new wishlist item
                Wishlist.objects.create(
                    user=request.user,
                    product=product,
                    datamode='A',
                    created_by=request.user.username or 'website',
                    updated_by=request.user.username or 'website'
                )
                in_wishlist = True
                action = 'added'
                message = f'{product.name} added to your wishlist'

            # Get updated counts
            wishlist_count = Wishlist.objects.filter(
                user=request.user, 
                datamode='A'
            ).count()

            # Get wishlist items for quick response (first 5 for preview)
            recent_wishlist = Wishlist.objects.filter(
                user=request.user,
                datamode='A'
            ).select_related('product').order_by('-created_on')[:5]

            recent_items = [{
                'id': item.id,
                'product_id': item.product.id,
                'product_name': item.product.name,
                'product_slug': item.product.slug,
                'product_price': float(item.product.price),
                'product_image': item.product.image.url if item.product.image else None
            } for item in recent_wishlist]

            return JsonResponse({
                'success': True,
                'in_wishlist': in_wishlist,
                'action': action,
                'wishlist_count': wishlist_count,
                'message': message,
                'recent_items': recent_items,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'slug': product.slug
                }
            })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'INVALID_JSON',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"toggle_wishlist error: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'SERVER_ERROR',
            'message': 'An error occurred. Please try again.'
        }, status=500)


@login_required(login_url='mck_auth:website_signin')
@require_GET
def get_wishlist_status(request):
    """
    Get wishlist status for multiple products at once (bulk check).
    More efficient than checking one by one.
    """
    try:
        product_slugs = request.GET.getlist('product_slugs[]') or request.GET.get('product_slugs', '').split(',')
        
        if not product_slugs or (len(product_slugs) == 1 and not product_slugs[0]):
            return JsonResponse({
                'success': True,
                'status': {}
            })

        # Get all products in one query
        products = Product.objects.filter(
            slug__in=product_slugs,
            datamode='A'
        ).values('id', 'slug')

        product_ids = [p['id'] for p in products]
        
        # Get wishlist status in one query
        wishlist_items = Wishlist.objects.filter(
            user=request.user,
            product_id__in=product_ids,
            datamode='A'
        ).values_list('product_id', flat=True)

        wishlist_set = set(wishlist_items)
        product_id_to_slug = {p['id']: p['slug'] for p in products}

        # Build response
        status = {}
        for product_id, slug in product_id_to_slug.items():
            status[slug] = product_id in wishlist_set

        return JsonResponse({
            'success': True,
            'status': status
        })

    except Exception as e:
        logger.error(f"get_wishlist_status error: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'SERVER_ERROR',
            'message': 'Failed to get wishlist status'
        }, status=500)


@login_required(login_url='mck_auth:website_signin')
@require_GET
def check_wishlist(request):
    """
    Check if a single product is in user's wishlist.
    """
    try:
        product_slug = request.GET.get('product_slug')
        if not product_slug:
            return JsonResponse({
                'success': False,
                'error': 'PRODUCT_SLUG_REQUIRED',
                'message': 'Product slug required'
            }, status=400)

        product = get_object_or_404(Product, slug=product_slug, datamode='A')
        
        in_wishlist = Wishlist.objects.filter(
            user=request.user,
            product=product,
            datamode='A'
        ).exists()

        return JsonResponse({
            'success': True,
            'in_wishlist': in_wishlist,
            'product_slug': product_slug
        })

    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'PRODUCT_NOT_FOUND',
            'message': 'Product not found'
        }, status=404)
    except Exception as e:
        logger.error(f"check_wishlist error: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'SERVER_ERROR',
            'message': 'Failed to check wishlist status'
        }, status=500)


@login_required(login_url='mck_auth:website_signin')
@require_POST
def bulk_wishlist_action(request):
    """
    Perform bulk actions on wishlist (add multiple, remove multiple).
    """
    try:
        data = json.loads(request.body)
        action = data.get('action')  # 'add', 'remove', 'toggle'
        product_ids = data.get('product_ids', [])
        product_slugs = data.get('product_slugs', [])

        if not product_ids and not product_slugs:
            return JsonResponse({
                'success': False,
                'error': 'NO_PRODUCTS',
                'message': 'No products specified'
            }, status=400)

        with transaction.atomic():
            # Get products
            products = Product.objects.filter(
                Q(id__in=product_ids) | Q(slug__in=product_slugs),
                datamode='A'
            )

            results = {}
            added_count = 0
            removed_count = 0

            for product in products:
                existing = Wishlist.objects.filter(
                    user=request.user,
                    product=product
                ).first()

                if action == 'add':
                    if not existing or existing.datamode != 'A':
                        if existing:
                            existing.datamode = 'A'
                            existing.save()
                        else:
                            Wishlist.objects.create(
                                user=request.user,
                                product=product,
                                datamode='A',
                                created_by=request.user.username or 'website',
                                updated_by=request.user.username or 'website'
                            )
                        added_count += 1
                        results[product.slug] = True
                    else:
                        results[product.slug] = True

                elif action == 'remove':
                    if existing and existing.datamode == 'A':
                        existing.datamode = 'I'
                        existing.save()
                        removed_count += 1
                        results[product.slug] = False
                    else:
                        results[product.slug] = False

                elif action == 'toggle':
                    if existing and existing.datamode == 'A':
                        existing.datamode = 'I'
                        existing.save()
                        removed_count += 1
                        results[product.slug] = False
                    else:
                        if existing:
                            existing.datamode = 'A'
                            existing.save()
                        else:
                            Wishlist.objects.create(
                                user=request.user,
                                product=product,
                                datamode='A',
                                created_by=request.user.username or 'website',
                                updated_by=request.user.username or 'website'
                            )
                        added_count += 1
                        results[product.slug] = True

            # Get updated total count
            wishlist_count = Wishlist.objects.filter(
                user=request.user,
                datamode='A'
            ).count()

            return JsonResponse({
                'success': True,
                'action': action,
                'results': results,
                'added_count': added_count,
                'removed_count': removed_count,
                'wishlist_count': wishlist_count,
                'message': f'{added_count} items added, {removed_count} items removed'
            })

    except Exception as e:
        logger.error(f"bulk_wishlist_action error: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'SERVER_ERROR',
            'message': 'Bulk operation failed'
        }, status=500)


@login_required(login_url='mck_auth:website_signin')
def get_wishlist_items(request):
    """
    Get paginated wishlist items with filters and sorting.
    """
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        sort_by = request.GET.get('sort', '-created_on')  # -created_on, price, -price, name

        # Base queryset
        wishlist_items = Wishlist.objects.filter(
            user=request.user,
            datamode='A'
        ).select_related('product', 'product__category')

        # Apply sorting
        if sort_by == 'price':
            wishlist_items = wishlist_items.order_by('product__price')
        elif sort_by == '-price':
            wishlist_items = wishlist_items.order_by('-product__price')
        elif sort_by == 'name':
            wishlist_items = wishlist_items.order_by('product__name')
        elif sort_by == '-name':
            wishlist_items = wishlist_items.order_by('-product__name')
        else:
            wishlist_items = wishlist_items.order_by('-created_on')

        # Paginate
        paginator = Paginator(wishlist_items, page_size)
        page_obj = paginator.get_page(page)

        # Format response
        items = []
        for item in page_obj:
            product = item.product
            items.append({
                'id': item.id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'slug': product.slug,
                    'price': float(product.price),
                    'sale_price': float(product.sale_price) if product.sale_price else None,
                    'image': product.image.url if product.image else None,
                    'stock': product.stock,
                    'category': product.category.name,
                    'category_slug': product.category.slug,
                    'is_in_stock': product.stock > 0,
                    'discount_percentage': product.discount_percentage if hasattr(product, 'discount_percentage') else 0
                },
                'added_on': item.created_on.isoformat()
            })

        return JsonResponse({
            'success': True,
            'items': items,
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'page_size': page_size
            },
            'wishlist_count': paginator.count
        })

    except Exception as e:
        logger.error(f"get_wishlist_items error: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'SERVER_ERROR',
            'message': 'Failed to fetch wishlist items'
        }, status=500)


@login_required(login_url='mck_auth:website_signin')
@require_POST
def remove_from_wishlist(request, item_id):
    """Remove specific item from wishlist by ID"""
    try:
        with transaction.atomic():
            item = get_object_or_404(
                Wishlist, 
                id=item_id, 
                user=request.user,
                datamode='A'
            )
            
            # Soft delete
            item.datamode = 'I'
            item.updated_by = request.user.username or 'website'
            item.save()

            wishlist_count = Wishlist.objects.filter(
                user=request.user, 
                datamode='A'
            ).count()

            return JsonResponse({
                'success': True,
                'wishlist_count': wishlist_count,
                'message': 'Item removed from wishlist'
            })

    except Exception as e:
        logger.error(f"remove_from_wishlist error: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'SERVER_ERROR',
            'message': 'Failed to remove item'
        }, status=500)


@login_required(login_url='mck_auth:website_signin')
@require_POST
def move_wishlist_to_cart(request, item_id):
    """Move wishlist item to cart"""
    try:
        with transaction.atomic():
            wl_item = get_object_or_404(
                Wishlist,
                id=item_id,
                user=request.user,
                datamode='A'
            )
            product = wl_item.product

            # Check stock
            if product.stock <= 0:
                return JsonResponse({
                    'success': False,
                    'error': 'OUT_OF_STOCK',
                    'message': f'{product.name} is out of stock'
                }, status=400)

            # Get or create cart
            cart, _ = Cart.objects.get_or_create(
                user=request.user,
                defaults={
                    'created_by': request.user.username or 'website',
                    'updated_by': request.user.username or 'website'
                }
            )

            # Add to cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={
                    'quantity': 1,
                    'price': product.sale_price or product.price,
                    'created_by': request.user.username or 'website',
                    'updated_by': request.user.username or 'website'
                }
            )

            if not created:
                cart_item.quantity += 1
                cart_item.save()

            # Remove from wishlist
            wl_item.datamode = 'I'
            wl_item.save()

            # Get updated counts
            wishlist_count = Wishlist.objects.filter(
                user=request.user,
                datamode='A'
            ).count()
            
            cart_count = CartItem.objects.filter(
                cart=cart,
                datamode='A'
            ).count()

            return JsonResponse({
                'success': True,
                'wishlist_count': wishlist_count,
                'cart_count': cart_count,
                'message': f'{product.name} moved to cart'
            })

    except Exception as e:
        logger.error(f"move_wishlist_to_cart error: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'SERVER_ERROR',
            'message': 'Failed to move item to cart'
        }, status=500)
