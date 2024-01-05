from django.shortcuts import render,get_object_or_404
from store.models import Product
from category.models import Category
# Create your views here.
def store(request,category_slug=None):
    category=Category.objects.all()
    product=None
    categories=None
    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug)
        product=Product.objects.all().filter(category=categories, is_available=True)
    else:
        product = Product.objects.all().filter(is_available=True).order_by('id')

    
    context={
        "product":product
    }
    return render(request,"store.html",context)

def product_detail(request,category_slug,product_slug):
    product=Product.objects.get(category__slug=category_slug,slug=product_slug)

    return render(request,"product-detail.html",{"product":product})
