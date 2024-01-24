from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import Cart,CartItem
from store.models import Product,Variation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
def _cart_id(request):
     cart=request.session.session_key
     if not cart:
           cart = request.session.create()
     return cart

def add_to_cart(request,product_id):
     current_user=request.user
     product=Product.objects.get(id=product_id)
     if current_user.is_authenticated:
          product_variation = []
          if request.method == 'POST':
               for item in request.POST:
                    key = item
                    value = request.POST[key]

                    try:
                         variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                         product_variation.append(variation)
                    except:
                         pass


          is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
          if is_cart_item_exists:
               cart_item = CartItem.objects.filter(product=product, user=current_user)
               ex_var_list = []
               id = []
               for item in cart_item:
                    existing_variation = item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)

               if product_variation in ex_var_list:
                # increase the cart item quantity
                    index = ex_var_list.index(product_variation)
                    item_id = id[index]
                    item = CartItem.objects.get(product=product, id=item_id)
                    item.quantity += 1
                    item.save()

               else:
                    item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                    if len(product_variation) > 0:
                         item.variations.clear()
                         item.variations.add(*product_variation)
                    item.save()
          else:
               cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    user = current_user,
               )
               if len(product_variation) > 0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
               cart_item.save()
          return redirect('cart')
     # If the user is not authenticated
     else:
          product_variation=[]
          if request.method=='POST':
               for item in request.POST:
                    key=item
                    value=request.POST[key]
                    try:
                         variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                         product_variation.append(variation)
                    except:
                         pass
          try:
               cart=Cart.objects.get(cart_id=_cart_id(request))

          except Cart.DoesNotExist:
               cart=Cart.objects.create(
                    cart_id=_cart_id(request)
               )
          cart.save()
          cart_item_exists=CartItem.objects.filter(product=product,cart=cart).exists()
          if cart_item_exists:
               cart_item=CartItem.objects.filter(product=product,cart=cart)
               ex_var=[]
               id=[]
               for item in cart_item:
                    existing_variations=item.variations.all()
                    ex_var.append(list(existing_variations))
                    id.append(item.id)

               if product_variation in ex_var:
                    item_index=ex_var.index(product_variation)
                    item_id=id[item_index]
                    item=CartItem.objects.get(id=item_id)
                    item.quantity+=1
                    item.save()
               else:
                    item = CartItem.objects.create(product=product, quantity=1,cart=cart)
                    if len(product_variation) > 0:
                         item.variations.clear()
                         item.variations.add(*product_variation)
                    item.save()

          else :
               cart_item=CartItem.objects.create(
                    product=product,
                    quantity=1,
                    cart=cart
               )
               if len(product_variation)>0:
                    for item in product_variation:
                         cart_item.variations.add(item)
               cart_item.save()
          return redirect("cart")

def remove_cart(request,product_id,cart_item_id):
     product=Product.objects.get(id=product_id)
     current_user=request.user
     
     if current_user.is_authenticated:
          cart_item=CartItem.objects.get(product=product,user=current_user,id=cart_item_id)
     else:
          cart=Cart.objects.get(cart_id=_cart_id(request))
          cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
     if cart_item.quantity>1:
          cart_item.quantity-=1
          cart_item.save()
     else:
          cart_item.delete()
     return redirect("cart")

def remove_cart_item(request, product_id, cart_item_id):
     product = get_object_or_404(Product, id=product_id)
     current_user=request.user
     if current_user.is_authenticated:
          cart_item=CartItem.objects.get(product=product,user=current_user,id=cart_item_id)
     else:
          cart = Cart.objects.get(cart_id=_cart_id(request))
          cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
     cart_item.delete()
     return redirect('cart')


def cart(request,total=0,quantity=0,cart_items=None):
    
     try:
          tax = 0
          g_total = 0
          if request.user.is_authenticated:
               cart_items = CartItem.objects.filter(user=request.user, is_active=True)
          else:
               cart=Cart.objects.get(cart_id=_cart_id(request))
               cart_items=CartItem.objects.filter(cart=cart,is_active=True)
               
          for item in cart_items:
               total+=item.quantity*item.product.price
               quantity=item.quantity
          tax=(2*total)/100
          g_total=tax+total
     
     except ObjectDoesNotExist:
          pass
     context={
          'cart_items':cart_items,
          'total':total,
          'quantity':quantity,
          'tax':tax,
          'g_total':g_total
     }
    
     return render(request,"store/cart.html",context)

@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):

     if request.method=='POST':
          first_name=request.POST["first_name"]
          last_name=request.POST["last_name"]
          email=request.POST["email"]
          phone_number=request.POST["phone_number"]
          address1=request.POST["address1"]
          city=request.POST["city"]
          country=request.POST["country"]
          state=request.POST["state"]

     try:
          tax = 0
          g_total = 0
          cart=Cart.objects.get(cart_id=_cart_id(request))
          cart_items=CartItem.objects.filter(cart=cart,is_active=True)
          
          for item in cart_items:
               total+=item.quantity*item.product.price
               quantity=item.quantity
          tax=(2*total)/100
          g_total=tax+total
     
     except ObjectDoesNotExist:
          pass
     context={
          'cart_items':cart_items,
          'total':total,
          'quantity':quantity,
          'tax':tax,
          'g_total':g_total
     }
    
   
     return render(request,'store/checkout.html',context)