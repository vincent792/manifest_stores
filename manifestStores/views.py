from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from manifestStores.models import Product
from category.models import Category
from cart.models import Cart, CartItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from accounts.forms import RegistrationForm
from accounts.models import Account
from django.contrib import messages, auth


# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.


def home(request):
    context = {}
    products = Product.objects.all().filter(is_available=True)
    context['products'] = products

    return render(request, 'main/index.html', context)


def store(request, category_slug=None):
    context = {}
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        products_count = products.count()

        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        products_count = products.count()
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    context['products'] = paged_products
    context['products_count'] = products_count
    return render(request, 'main/store.html', context)


def product_detail(request, category_slug, product_slug):
    context = {}
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        # check if product is added to cart
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(
            request), product=single_product).exists()
        # return HttpResponse(in_cart)
        # exit()

    except Exception as e:

        raise e

    context['single_product'] = single_product
    context['in_cart'] = in_cart

    return render(request, 'main/product-detail.html', context)


def _cart_id(request):

    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
# use sessions
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    # what if cart doesnt exist
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)

        )
    cart.save()

    # bring cart item
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        # increment cart item by 1

        cart_item.quantity+1
        cart_item.save()
        # whatif cart item doent exist
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,

        )
        cart_item.save()
    # check if cart item is saved
    # return HttpResponse(cart_item.quantity)
    # exit()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    context = {}
    tax = 0
    grand_total = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = tax + total

    except ObjectDoesNotExist:
        pass
    context['total'] = total
    context['quantity'] = quantity
    context['cart_items'] = cart_items
    context['tax'] = tax
    context['grand_total'] = grand_total

    return render(request, 'main/cart.html', context)


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def add_cart2(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity <= 100**1000000:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def delete_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()
    return redirect('cart')


def search(request):
    context = {}
    # return HttpResponse('Search page')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            products_count = products.count()

    context['products'] = products
    context['products_count'] = products_count
    return render(request, 'main/search.html', context)


def about(request):
    return render(request, 'advertisement/about.html')


def contact(request):
    return render(request, 'advertisement/contact.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            print('success login')
            messages.success(request, 'Login Successfull')
            return redirect('/')
        else:
            messages.error(request, 'Invalid Details ')
            print('invalid')
            return redirect('login')
    return render(request, 'account/signin.html')


def register(request):
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone = phone
            user.save()
            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('account/verify-email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Account Created Successfully!')
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
            return redirect('activate_email')
            # return redirect('login/?command=verification&email='+email)

    else:
        form = RegistrationForm()

    context['form'] = form

    return render(request, 'account/register.html', context)


def logout(request):
    auth.logout(request)
    messages.warning(request, "You're logged out!")
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


def activate_email(request):
    return render(request, 'account/activate-email.html')




def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')