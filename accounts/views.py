from django.shortcuts import render,redirect,HttpResponse
from .forms import Registrationform
from .models import Account
from django.contrib import messages,auth,sessions
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.core.mail import EmailMessage,send_mail
from django.template.loader import render_to_string
from cart.models import Cart,CartItem
from cart.views import _cart_id
# Create your views here.


def register(request):
    
    if request.method=="POST":
        form = Registrationform(request.POST)  
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username=email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number=phone_number
            user.save()

            #User Activation
            current_site=get_current_site(request)
            mail_subject="Please Activate your account...."
            message=render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            #messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')

            return redirect('/account/login/?command=verification&email='+email)

    else:
        form = Registrationform() 
    return render(request,'accounts/register.html',{'form':form})
def login(request):
    
    if request.method =='POST':
        email=request.POST['email']
        password=request.POST["password"]
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            try:
                cart= Cart.objects.get(cart_id=_cart_id(request))
                cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if cart_item_exists:
                    product_variation=[]
                    cart_item=CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    cart_item = CartItem.objects.filter(user=user)
                    id=[]
                    ex_var=[]
                    for item in cart_item:
                        existing_variations=item.variations.all()
                        ex_var.append(list(existing_variations))
                        id.append(item.id)
                    
                    for pr in product_variation:
                        if pr in ex_var:
                            index = ex_var.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
                        

                
            except:
                pass
            auth.login(request,user)
            # messages.success(request, 'You are now logged in.')
            return redirect("home")

        else:
            messages.error( request,'Invalid login credential')
            return redirect("login")
    return render(request,"accounts/login.html")

@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    messages.success(request, 'You are now logged in.')
    return render(request,"accounts/dashboard.html")

def forgotPassword(request):
    if request.method=='POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site=get_current_site(request)
            mail_subject="Forgot password!. please reset here"
            message=render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotpassword')
    return render(request, 'accounts/forgotPassword.html')



def resetpassword_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except (TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    c=default_token_generator.check_token(user,token)
    print(c)
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        print(uid)
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    
    else:
        messages.error(request,"Account doesnot exists")
        return redirect('register')


def resetPassword(request):
    if request.method=="POST":
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password == confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request,"Password Donot match")
            return redirect('resetPassword')
    
    return render(request,"accounts/reset_password.html")