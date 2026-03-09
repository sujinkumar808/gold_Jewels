from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('home', views.home, name='home'), 
    path('loan/<int:id>/', views.loan_detail, name='loan_detail'),
    path('gold_rate/', views.gold_rate, name='gold_rate'), 
    path('faq/', views.faq_view, name='faq'),
    path('about/', views.about, name='about'),        
    path('contact/', views.contact, name='contact'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy/<int:product_id>/', views.buy_now, name='buy_now'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('checkout-cart/', views.checkout_cart, name='checkout_cart'),
    path("login/", views.login_phone, name="login"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
]
