from django.urls import path

import accounts.views as views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name ='password_reset_complete'),

    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('products/', views.products, name='products'),

    path('user/', views.user_page, name='user'),
    path('profile/', views.profile, name='profile'),

    path('customer/<int:customer_pk>/', views.customer_view, name='customer'),
    path('update_customer/<int:customer_pk>/', views.update_customer, name='update-customer'),

    path('create_order/<int:customer_pk>/', views.create_order, name='create-order'),
    path('update_order/<int:order_pk>', views.update_order, name='update-order'),
    path('delete_order/<int:order_pk>', views.delete_order, name='delete-order'),
]
