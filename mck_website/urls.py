# urls.py

from django.urls import path
from mck_website import views
from .views import (
    UserList, UserCreateView, UserUpdateView, UserDeleteView,
    # Order Views - Add these imports
    OrderList, OrderCreateView, OrderUpdateView, OrderDeleteView,
    OrderItemList, OrderItemCreateView, OrderItemUpdateView, OrderItemDeleteView,
    # Other views
    CategoryList, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    BlogList, BlogCreateView, BlogUpdateView, BlogDeleteView,
    ProductList, ProductCreateView, ProductUpdateView, ProductDeleteView,
    HomePageVideoList, HomePageVideoCreateView, HomePageVideoUpdateView, HomePageVideoDeleteView,
    HeroBannerList, HeroBannerCreateView, HeroBannerUpdateView, HeroBannerDeleteView,
    CustomerList, CustomerCreateView, CustomerUpdateView, CustomerDeleteView,
    AddressList, AddressCreateView, AddressUpdateView, AddressDeleteView,
    CouponList, CouponCreateView, CouponUpdateView, CouponDeleteView,
    PaymentGatewayList, PaymentGatewayCreateView, PaymentGatewayUpdateView, PaymentGatewayDeleteView,
    CartList, CartDeleteView,
    ProductReviewList, ProductReviewUpdateView, ProductReviewDeleteView,
    NewsletterList, NewsletterDeleteView,
    ContactUsList, ContactUsUpdateView, ContactUsDeleteView,
    SiteSettingsUpdateView, ContactPageView, ajax_contact_submit,
)

app_name = "mck_website"

urlpatterns = [

    # --------------------
    # Main Pages
    # --------------------
    # path('', views.HomePage.as_view(), name='home_page'),

    path(
        'category/list/',
        CategoryList.as_view(),
        name='mck_category_list'
    ),

    path(
        'category/create/',
        CategoryCreateView.as_view(),
        name='mck_category_create'
    ),

    path(
        'category/update/<int:id>/',
        CategoryUpdateView.as_view(),
        name='mck_category_update'
    ),

    path(
        'category/delete/<int:id>/',
        CategoryDeleteView.as_view(),
        name='mck_category_delete'
    ),

    path(
        'blog/list/',
        BlogList.as_view(),
        name='mck_blog_list'
    ),

    path(
        'blog/create/',
        BlogCreateView.as_view(),
        name='mck_blog_create'
    ),

    path(
        'blog/update/<int:id>/',
        BlogUpdateView.as_view(),
        name='mck_blog_update'
    ),

    path(
        'blog/delete/<int:id>/',
        BlogDeleteView.as_view(),
        name='mck_blog_delete'
    ),

    path(
        'product/list/',
        ProductList.as_view(),
        name='mck_product_list'
    ),

    path(
        'product/create/',
        ProductCreateView.as_view(),
        name='mck_product_create'
    ),

    path(
        'product/update/<int:id>/',
        ProductUpdateView.as_view(),
        name='mck_product_update'
    ),

    path(
        'product/delete/<int:id>/',
        ProductDeleteView.as_view(),
        name='mck_product_delete'
    ),

    path('homepage-video/',
         HomePageVideoList.as_view(),
         name='mck_homepage_video_list'),
 
    path('homepage-video/create/',
         HomePageVideoCreateView.as_view(),
         name='mck_homepage_video_create'),
 
    path('homepage-video/<int:id>/edit/',
         HomePageVideoUpdateView.as_view(),
         name='mck_homepage_video_update'),
 
    path('homepage-video/<int:id>/delete/',
         HomePageVideoDeleteView.as_view(),
         name='mck_homepage_video_delete'),
 
    # ── HeroBanner ───────────────────────────────────────────────────────
    path('hero-banner/',
         HeroBannerList.as_view(),
         name='mck_hero_banner_list'),
 
    path('hero-banner/create/',
         HeroBannerCreateView.as_view(),
         name='mck_hero_banner_create'),
 
    path('hero-banner/<int:id>/edit/',
         HeroBannerUpdateView.as_view(),
         name='mck_hero_banner_update'),
 
    path('hero-banner/<int:id>/delete/',
         HeroBannerDeleteView.as_view(),
         name='mck_hero_banner_delete'),

    
    # ─────────────────────────────────────────────────────────────────────────────
    # Customer URLs
    # ─────────────────────────────────────────────────────────────────────────────
    path('customers/',
         CustomerList.as_view(),
         name='mck_customer_list'),

    path('customers/create/',
         CustomerCreateView.as_view(),
         name='mck_customer_create'),

    path('customers/<int:id>/edit/',
         CustomerUpdateView.as_view(),
         name='mck_customer_update'),

    path('customers/<int:id>/delete/',
         CustomerDeleteView.as_view(),
         name='mck_customer_delete'),

    # ─────────────────────────────────────────────────────────────────────────────
    # Address URLs
    # ─────────────────────────────────────────────────────────────────────────────
    path('addresses/',
         AddressList.as_view(),
         name='mck_address_list'),

    path('addresses/create/',
         AddressCreateView.as_view(),
         name='mck_address_create'),

    path('addresses/<int:id>/edit/',
         AddressUpdateView.as_view(),
         name='mck_address_update'),

    path('addresses/<int:id>/delete/',
         AddressDeleteView.as_view(),
         name='mck_address_delete'),

    # ─────────────────────────────────────────────────────────────────────────────
    # Coupon URLs
    # ─────────────────────────────────────────────────────────────────────────────
    path('coupons/',
         CouponList.as_view(),
         name='mck_coupon_list'),

    path('coupons/create/',
         CouponCreateView.as_view(),
         name='mck_coupon_create'),

    path('coupons/<int:id>/edit/',
         CouponUpdateView.as_view(),
         name='mck_coupon_update'),

    path('coupons/<int:id>/delete/',
         CouponDeleteView.as_view(),
         name='mck_coupon_delete'),

    # ─────────────────────────────────────────────────────────────────────────────
    # PaymentGateway URLs
    # ─────────────────────────────────────────────────────────────────────────────
    path('payment-gateways/',
         PaymentGatewayList.as_view(),
         name='mck_payment_gateway_list'),

    path('payment-gateways/create/',
         PaymentGatewayCreateView.as_view(),
         name='mck_payment_gateway_create'),

    path('payment-gateways/<int:id>/edit/',
         PaymentGatewayUpdateView.as_view(),
         name='mck_payment_gateway_update'),

    path('payment-gateways/<int:id>/delete/',
         PaymentGatewayDeleteView.as_view(),
         name='mck_payment_gateway_delete'),

    # ─────────────────────────────────────────────────────────────────────────────
    # Cart URLs
    # ─────────────────────────────────────────────────────────────────────────────
    path('carts/',
         CartList.as_view(),
         name='mck_cart_list'),

    path('carts/<int:id>/delete/',
         CartDeleteView.as_view(),
         name='mck_cart_delete'),

    # ─────────────────────────────────────────────────────────────────────────────
    # Order URLs
    # ─────────────────────────────────────────────────────────────────────────────
    # Order URLs
    path('orders/', OrderList.as_view(), name='mck_order_list'),
    path('orders/create/', OrderCreateView.as_view(), name='mck_order_create'),
    path('orders/<int:id>/update/', OrderUpdateView.as_view(), name='mck_order_update'),
    path('orders/<int:id>/delete/', OrderDeleteView.as_view(), name='mck_order_delete'),

    # OrderItem URLs
    path('order-items/', OrderItemList.as_view(), name='mck_order_item_list_all'),
    path('orders/<int:order_id>/items/', OrderItemList.as_view(), name='mck_order_item_list'),
    path('order-items/create/', OrderItemCreateView.as_view(), name='mck_order_item_create'),
    path('orders/<int:order_id>/items/create/', OrderItemCreateView.as_view(), name='mck_order_item_create_with_order'),
    path('order-items/<int:id>/update/', OrderItemUpdateView.as_view(), name='mck_order_item_update'),
    path('order-items/<int:id>/delete/', OrderItemDeleteView.as_view(), name='mck_order_item_delete'),

    # ─────────────────────────────────────────────────────────────────────────────
    # ProductReview URLs
    # ─────────────────────────────────────────────────────────────────────────────
    path('product-reviews/',
         ProductReviewList.as_view(),
         name='mck_product_review_list'),

    path('product-reviews/<int:id>/edit/',
         ProductReviewUpdateView.as_view(),
         name='mck_product_review_update'),

    path('product-reviews/<int:id>/delete/',
         ProductReviewDeleteView.as_view(),
         name='mck_product_review_delete'),

    # ─────────────────────────────────────────────────────────────────────────────
    # Newsletter URLs
    # ─────────────────────────────────────────────────────────────────────────────
    path('newsletters/',
         NewsletterList.as_view(),
         name='mck_newsletter_list'),

    path('newsletters/<int:id>/delete/',
         NewsletterDeleteView.as_view(),
         name='mck_newsletter_delete'),

    # ─────────────────────────────────────────────────────────────────────────────
    # ContactUs URLs
    # ─────────────────────────────────────────────────────────────────────────────
    path('contact-us/',
         ContactUsList.as_view(),
         name='mck_contact_us_list'),

    path('contact-us/<int:id>/edit/',
         ContactUsUpdateView.as_view(),
         name='mck_contact_us_update'),

    path('contact-us/<int:id>/delete/',
         ContactUsDeleteView.as_view(),
         name='mck_contact_us_delete'),

    # ─────────────────────────────────────────────────────────────────────────────
    # SiteSettings URLs (Singleton)
    # ─────────────────────────────────────────────────────────────────────────────
    path('site-settings/',
         SiteSettingsUpdateView.as_view(),
         name='mck_site_settings'),

    path('contact/', ContactPageView.as_view(), name='contact'),
    path('contact/ajax-submit/', ajax_contact_submit, name='contact_ajax_submit'),

    # User Management
    path('users/', UserList.as_view(), name='mck_user_list'),
    path('users/create/', UserCreateView.as_view(), name='mck_user_create'),
    path('users/<int:id>/update/', UserUpdateView.as_view(), name='mck_user_update'),
    path('users/<int:id>/delete/', UserDeleteView.as_view(), name='mck_user_delete'),
    # path('users/<int:id>/hard-delete/', UserHardDeleteView.as_view(), name='mck_user_hard_delete'),

]