from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} × {self.movie.title}"

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie.title} - {self.rating}/5 by {self.user.username}"

# movies/models.py
from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    CART_CHOICES = [(1, "Cart 1"), (2, "Cart 2"), (3, "Cart 3")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_number = models.IntegerField(choices=CART_CHOICES)

    def __str__(self):
        return f"{self.user.username} - Cart {self.cart_number}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE)  # adjust model name if different
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie.title} in {self.cart}"
