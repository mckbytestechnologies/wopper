from django.urls import path
from mck_website import views

app_name = "mck_website"

urlpatterns = [

    # --------------------
    # Main Pages
    # --------------------
#     path('', views.HomePage.as_view(), name='home_page'),

    path(
    'category/list/',
    views.CategoryList.as_view(),
    name='mck_category_list'
),

path(
    'category/create/',
    views.CategoryCreateView.as_view(),
    name='mck_category_create'
),

path(
    'category/update/<int:id>/',
    views.CategoryUpdateView.as_view(),
    name='mck_category_update'
),

path(
    'category/delete/<int:id>/',
    views.CategoryDeleteView.as_view(),
    name='mck_category_delete'
),



path(
    'product/list/',
    views.ProductList.as_view(),
    name='mck_product_list'
),

path(
    'product/create/',
    views.ProductCreateView.as_view(),
    name='mck_product_create'
),

path(
    'product/update/<int:id>/',
    views.ProductUpdateView.as_view(),
    name='mck_product_update'
),

path(
    'product/delete/<int:id>/',
    views.ProductDeleteView.as_view(),
    name='mck_product_delete'
),

path('homepage-video/',
         views.HomePageVideoList.as_view(),
         name='mck_homepage_video_list'),
 
    path('homepage-video/create/',
         views.HomePageVideoCreateView.as_view(),
         name='mck_homepage_video_create'),
 
    path('homepage-video/<int:id>/edit/',
         views.HomePageVideoUpdateView.as_view(),
         name='mck_homepage_video_update'),
 
    path('homepage-video/<int:id>/delete/',
         views.HomePageVideoDeleteView.as_view(),
         name='mck_homepage_video_delete'),
 
    # ── HeroBanner ───────────────────────────────────────────────────────
    path('hero-banner/',
         views.HeroBannerList.as_view(),
         name='mck_hero_banner_list'),
 
    path('hero-banner/create/',
         views.HeroBannerCreateView.as_view(),
         name='mck_hero_banner_create'),
 
    path('hero-banner/<int:id>/edit/',
         views.HeroBannerUpdateView.as_view(),
         name='mck_hero_banner_update'),
 
    path('hero-banner/<int:id>/delete/',
         views.HeroBannerDeleteView.as_view(),
         name='mck_hero_banner_delete'),

    
# ─────────────────────────────────────────────────────────────────────────────
# Customer URLs
# ─────────────────────────────────────────────────────────────────────────────
path('customers/',
     views.CustomerList.as_view(),
     name='mck_customer_list'),

path('customers/create/',
     views.CustomerCreateView.as_view(),
     name='mck_customer_create'),

path('customers/<int:id>/edit/',
     views.CustomerUpdateView.as_view(),
     name='mck_customer_update'),

path('customers/<int:id>/delete/',
     views.CustomerDeleteView.as_view(),
     name='mck_customer_delete'),

# ─────────────────────────────────────────────────────────────────────────────
# Address URLs
# ─────────────────────────────────────────────────────────────────────────────
path('addresses/',
     views.AddressList.as_view(),
     name='mck_address_list'),

path('addresses/create/',
     views.AddressCreateView.as_view(),
     name='mck_address_create'),

path('addresses/<int:id>/edit/',
     views.AddressUpdateView.as_view(),
     name='mck_address_update'),

path('addresses/<int:id>/delete/',
     views.AddressDeleteView.as_view(),
     name='mck_address_delete'),

# ─────────────────────────────────────────────────────────────────────────────
# Coupon URLs
# ─────────────────────────────────────────────────────────────────────────────
path('coupons/',
     views.CouponList.as_view(),
     name='mck_coupon_list'),

path('coupons/create/',
     views.CouponCreateView.as_view(),
     name='mck_coupon_create'),

path('coupons/<int:id>/edit/',
     views.CouponUpdateView.as_view(),
     name='mck_coupon_update'),

path('coupons/<int:id>/delete/',
     views.CouponDeleteView.as_view(),
     name='mck_coupon_delete'),

# ─────────────────────────────────────────────────────────────────────────────
# PaymentGateway URLs
# ─────────────────────────────────────────────────────────────────────────────
path('payment-gateways/',
     views.PaymentGatewayList.as_view(),
     name='mck_payment_gateway_list'),

path('payment-gateways/create/',
     views.PaymentGatewayCreateView.as_view(),
     name='mck_payment_gateway_create'),

path('payment-gateways/<int:id>/edit/',
     views.PaymentGatewayUpdateView.as_view(),
     name='mck_payment_gateway_update'),

path('payment-gateways/<int:id>/delete/',
     views.PaymentGatewayDeleteView.as_view(),
     name='mck_payment_gateway_delete'),

# ─────────────────────────────────────────────────────────────────────────────
# Cart URLs
# ─────────────────────────────────────────────────────────────────────────────
path('carts/',
     views.CartList.as_view(),
     name='mck_cart_list'),

path('carts/<int:id>/delete/',
     views.CartDeleteView.as_view(),
     name='mck_cart_delete'),

# ─────────────────────────────────────────────────────────────────────────────
# Order URLs
# ─────────────────────────────────────────────────────────────────────────────
path('orders/',
     views.OrderList.as_view(),
     name='mck_order_list'),

path('orders/<int:id>/edit/',
     views.OrderUpdateView.as_view(),
     name='mck_order_update'),

path('orders/<int:id>/delete/',
     views.OrderDeleteView.as_view(),
     name='mck_order_delete'),

# ─────────────────────────────────────────────────────────────────────────────
# ProductReview URLs
# ─────────────────────────────────────────────────────────────────────────────
path('product-reviews/',
     views.ProductReviewList.as_view(),
     name='mck_product_review_list'),

path('product-reviews/<int:id>/edit/',
     views.ProductReviewUpdateView.as_view(),
     name='mck_product_review_update'),

path('product-reviews/<int:id>/delete/',
     views.ProductReviewDeleteView.as_view(),
     name='mck_product_review_delete'),

# ─────────────────────────────────────────────────────────────────────────────
# Newsletter URLs
# ─────────────────────────────────────────────────────────────────────────────
path('newsletters/',
     views.NewsletterList.as_view(),
     name='mck_newsletter_list'),

path('newsletters/<int:id>/delete/',
     views.NewsletterDeleteView.as_view(),
     name='mck_newsletter_delete'),

# ─────────────────────────────────────────────────────────────────────────────
# ContactUs URLs
# ─────────────────────────────────────────────────────────────────────────────
path('contact-us/',
     views.ContactUsList.as_view(),
     name='mck_contact_us_list'),

path('contact-us/<int:id>/edit/',
     views.ContactUsUpdateView.as_view(),
     name='mck_contact_us_update'),

path('contact-us/<int:id>/delete/',
     views.ContactUsDeleteView.as_view(),
     name='mck_contact_us_delete'),

# ─────────────────────────────────────────────────────────────────────────────
# SiteSettings URLs (Singleton)
# ─────────────────────────────────────────────────────────────────────────────
path('site-settings/',
     views.SiteSettingsUpdateView.as_view(),
     name='mck_site_settings'),

path('contact/', views.ContactPageView.as_view(), name='contact'),
path('contact/ajax-submit/', views.ajax_contact_submit, name='contact_ajax_submit'),

]