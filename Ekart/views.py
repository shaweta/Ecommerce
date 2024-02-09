from django.shortcuts import render
from store.models import Product,ReviewRatings
# from store.models import Product, ReviewRating

def home(request):
    products=Product.objects.all().filter(is_available=True).order_by("created_date")
    for product in products:
        reviews=ReviewRatings.objects.filter(product_id=product.id,status=True)
    context={
        "products":products,
        "reviews":reviews
    }
    return render(request, 'index.html',context)