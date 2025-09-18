from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('signup/', views.signup, name='signup'),

    # Multi-cart routes
    path('add-to-cart/<int:movie_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/<int:cart_number>/', views.view_cart, name='view_cart'),
    path('cart/<int:cart_number>/checkout/', views.checkout, name='checkout'),
    path('cart/<int:cart_number>/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/<int:cart_number>/clear/', views.clear_cart, name='clear_cart'),

    path('my-orders/', views.my_orders, name='my_orders'),

    # Reviews
    path('review/<int:pk>/edit/', views.review_edit, name='review_edit'),
    path('review/<int:pk>/delete/', views.review_delete, name='review_delete'),
]
