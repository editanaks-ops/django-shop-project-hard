from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomLoginForm, ProfileUpdateForm
from shop.models import Order, Cart, CartItem, Product


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            activation_link = request.build_absolute_uri(
                f'/accounts/activate/{uid}/{token}/'
            )

            subject = 'Подтверждение регистрации'
            from_email = 'admin@shop.com'
            to = [user.email]

            text_content = f'Перейдите по ссылке для активации: {activation_link}'
            html_content = render_to_string('accounts/email_sent.html', {
                'activation_link': activation_link,
                'user': user,
            })

            email = EmailMultiAlternatives(subject, text_content, from_email, to)
            email.attach_alternative(html_content, "text/html")
            email.send()

            return render(request, 'accounts/email_sent.html', {
                'email': user.email,
                'activation_link': activation_link,
            })
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'accounts/activation_success.html')
    else:
        return render(request, 'accounts/activation_invalid.html')


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)

            merge_session_cart_to_user(request, user)

            return render(request, 'accounts/login_success.html', {'user': user})
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')


@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')

    cart = Cart.objects.filter(user=user).first()
    cart_items = cart.items.all() if cart else []

    total_price = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/profile.html', {
                'form': form,
                'orders': orders,
                'cart_items': cart_items,
                'total_price': total_price,
                'success_message': 'Профиль обновлён!',
            })
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'orders': orders,
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return render(request, 'accounts/account_deleted.html')

    return render(request, 'accounts/account_delete_forbidden.html')


def merge_session_cart_to_user(request, user):
    session_cart = request.session.get('cart', {})

    if not session_cart:
        return

    cart, created = Cart.objects.get_or_create(user=user)

    for product_id, quantity in session_cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
        except Product.DoesNotExist:
            continue

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()

    request.session['cart'] = {}