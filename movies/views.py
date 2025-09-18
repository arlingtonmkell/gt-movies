from django.shortcuts import render
from .models import Movie
from django.shortcuts import render, get_object_or_404
from .models import Movie, Order, OrderItem, Review   
from .forms import SignUpForm, ReviewForm           



def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "POST" and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect("movie_detail", pk=pk)
    else:
        form = ReviewForm()

    return render(request, "movie_detail.html", {"movie": movie, "form": form})


def home(request):
    q = request.GET.get('q', '')
    movies = Movie.objects.all()
    if q:
        movies = movies.filter(title__icontains=q)
    return render(request, 'home.html', {'movies': movies, 'q': q})

from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import SignUpForm, ReviewForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})

from django.contrib import messages

def add_to_cart(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    cart = request.session.get("cart", {})

    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session["cart"] = cart

    messages.success(request, f"Added {movie.title} to cart.")
    return redirect("home")

def view_cart(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0
    for pk, qty in cart.items():
        movie = Movie.objects.get(pk=pk)
        subtotal = movie.price * qty
        total += subtotal
        items.append({"movie": movie, "qty": qty, "subtotal": subtotal})
    return render(request, "cart.html", {"items": items, "total": total})

def checkout(request):
    if not request.user.is_authenticated:
        return redirect("login")

    cart = request.session.get("cart", {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect("home")

    order = Order.objects.create(user=request.user, total_price=0)
    total = 0
    for pk, qty in cart.items():
        movie = Movie.objects.get(pk=pk)
        subtotal = movie.price * qty
        OrderItem.objects.create(order=order, movie=movie, quantity=qty)
        total += subtotal
        movie.stock -= qty
        movie.save()
    order.total_price = total
    order.save()

    request.session["cart"] = {}
    messages.success(request, f"Order #{order.id} placed successfully!")
    return redirect("home")

from django.contrib.auth.decorators import login_required

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "my_orders.html", {"orders": orders})

from django.views.decorators.http import require_POST

@require_POST
def remove_from_cart(request, pk):
    cart = request.session.get("cart", {})
    cart.pop(str(pk), None)   # remove the entire line item
    request.session["cart"] = cart
    messages.info(request, "Item removed from cart.")
    return redirect("view_cart")

@require_POST
def clear_cart(request):
    request.session["cart"] = {}
    messages.info(request, "Cart cleared.")
    return redirect("view_cart")

from django.core.exceptions import PermissionDenied

@login_required
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        raise PermissionDenied("You can only edit your own review.")

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated.")
            return redirect("movie_detail", pk=review.movie.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "review_edit.html", {"form": form, "review": review})

@require_POST
@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        raise PermissionDenied("You can only delete your own review.")
    movie_pk = review.movie.pk
    review.delete()
    messages.info(request, "Review deleted.")
    return redirect("movie_detail", pk=movie_pk)
