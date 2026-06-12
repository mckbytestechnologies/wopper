# wopper/urls.py

from django.urls import path
from wopper import views

app_name = "wopper"

urlpatterns = [
    # ═════════════════════════════════════════════════════════════════════════
    # PUBLIC WEBSITE PAGES (No Login Required)
    # ═════════════════════════════════════════════════════════════════════════
    path('', views.WebsiteHomeView.as_view(), name='website_home'),
    path('products/', views.AllProductsView.as_view(), name='all_products'),
    path('category/<slug:slug>/', views.CategoryDataView.as_view(), name='category_products'),
    path('product/<slug:slug>/', views.ProductDataView.as_view(), name='product_detail'),
    path('search/', views.SearchView.as_view(), name='search'),

    # ═════════════════════════════════════════════════════════════════════════
    # CART URLs
    # ═════════════════════════════════════════════════════════════════════════
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('cart/coupon/apply/', views.apply_coupon, name='apply_coupon'),
    path('cart/coupon/remove/', views.remove_coupon, name='remove_coupon'),

    # ═════════════════════════════════════════════════════════════════════════
    # WISHLIST URLs (Working - Don't Change)
    # ═════════════════════════════════════════════════════════════════════════
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('api/wishlist/toggle/', views.toggle_wishlist, name='toggle_wishlist'),
    path('api/wishlist/status/', views.get_wishlist_status, name='wishlist_status'),
    path('api/wishlist/check/', views.check_wishlist, name='check_wishlist'),
    path('api/wishlist/items/', views.get_wishlist_items, name='get_wishlist_items'),
    path('api/wishlist/bulk/', views.bulk_wishlist_action, name='bulk_wishlist_action'),
    path('api/wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('api/wishlist/move-to-cart/<int:item_id>/', views.move_wishlist_to_cart, name='move_wishlist_to_cart'),

    # ═════════════════════════════════════════════════════════════════════════
    # CHECKOUT & PAYMENT URLs
    # ═════════════════════════════════════════════════════════════════════════
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/address/add/', views.add_address_quick, name='add_address_quick'),
    path('checkout/create-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('checkout/verify-payment/', views.verify_razorpay_payment, name='verify_razorpay_payment'),
    path('order/success/<str:order_number>/', views.OrderSuccessView.as_view(), name='order_success'),

    # ═════════════════════════════════════════════════════════════════════════
    # USER PAGES
    # ═════════════════════════════════════════════════════════════════════════
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]