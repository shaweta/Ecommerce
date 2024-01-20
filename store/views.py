from django.shortcuts import render,get_object_or_404
from store.models import Product
from django.db.models import Q
from category.models import Category
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.
def store(request,category_slug=None):
    category=Category.objects.all()
    product=None
    categories=None
    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug)
        product=Product.objects.all().filter(category=categories, is_available=True).order_by('id')
        paginator=Paginator(product,3)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
        product_count=product.count()
    else:
        product = Product.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(product,3)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
        product_count=product.count()

    context={
        "product":paged_product,
        "product_count":product_count
    }
    return render(request,"store/store.html",context)

def product_detail(request,category_slug,product_slug):
    product=Product.objects.get(category__slug=category_slug,slug=product_slug)

    return render(request,"store/product-detail.html",{"product":product})

def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            product=Product.objects.order_by('-created_date').filter( Q(description__icontains=keyword) | Q(product_name__icontains=keyword))

    context={
        'product':product
        }
    return render(request,"store/store.html",context)
