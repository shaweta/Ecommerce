from django.shortcuts import render,get_object_or_404,redirect
from store.models import Product, ReviewRatings
from orders.models import OrderProduct,Order
from .forms import ReviewForm
from django.db.models import Q
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.contrib import messages

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
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id= _cart_id(request), product=product).exists()
    except Exception as e:
        raise e
    # check product is ordered by user before posting reviews and rating
    if request.user.is_authenticated:
        try:
            orderproduct=OrderProduct.objects.get(user=request.user,product=product).exists()
        except OrderProduct.DoesNotExist:
            orderproduct=None
    else:
        orderproduct=None
    
    
    #get reviewsavg rating
    reviews=ReviewRatings.objects.filter(product=product,status=True)
    context={
        "product":product,
        "orderproduct":orderproduct,
        "reviews":reviews
        }

    return render(request,"store/product-detail.html",context)

def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            product=Product.objects.order_by('-created_date').filter( Q(description__icontains=keyword) | Q(product_name__icontains=keyword))

    context={
        'product':product
        }
    return render(request,"store/store.html",context)


def submit_review(request,product_id):
    url=request.META.get('HTTP_REFERER')
    try:
            reviews = ReviewRatings.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
    except ReviewRatings.DoesNotExist:
        if request.method=="POST":
            form=ReviewForm(request.POST)
            
            if form.is_valid():
                data=ReviewRatings()
                data.subject=form.cleaned_data["subject"]
                data.review=form.cleaned_data["review"]
                data.rating=form.cleaned_data["rating"]
                data.ip=request.META.get("REMOTE_ADDR")
                data.product_id=product_id
                data.user_id=request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)


def dashboard(request):
    orders=Order.objects.filter(user_id=request.user,is_ordered=True).order_by('-created_at')
    orders.count()
    return render(request,"accounts/dashboard.html")
    