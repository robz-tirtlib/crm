from django.shortcuts import render, redirect

from .models import Customer, Order, Product
from .forms import OrderForm, CustomerForm, CreateUserForm, ProfileForm
from .filters import OrderFilter
from .decorators import group_specific, unauthenticated_user

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.contrib import messages


@unauthenticated_user
def register_view(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('home')
        messages.error(request, "Unsuccessful registration. Invalid information.")

    return render(request, 'accounts/register.html', context={'form': form})


@unauthenticated_user
def login_view(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.groups.filter(name__in=['admin']).exists():
                    return redirect('home')
                else:
                    return redirect('user')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html', context={'form': form})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    if request.user.groups.filter(name__in=['admin']).exists():
        return redirect('dashboard')
    else:
        return redirect('user')


@group_specific('admin')
@login_required(login_url='login')
def dashboard(request):
    customers = Customer.objects.all()
    all_orders = Order.objects.all()
    orders = all_orders.order_by('-date_created')[:5]
    total_orders = all_orders.count
    orders_delivered = all_orders.filter(status='Delivered').count
    orders_packing = all_orders.filter(status='Packing').count

    context = {
        'customers': customers,
        'orders': orders,
        'total_orders': total_orders,
        'orders_delivered': orders_delivered,
        'orders_packing': orders_packing
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@group_specific('admin')
def products(request):
    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@group_specific('customer')
def user_page(request):
    orders = Order.objects.filter(customer=request.user.customer)

    context = {
        'orders': orders,
        'customer': request.user.customer,
    }

    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@group_specific('customer')
def profile(request):
    form = ProfileForm(instance=request.user.customer)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.customer)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {
        'form': form
    }

    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
@group_specific('admin')
def customer_view(request, customer_pk):
    customer = Customer.objects.get(id=customer_pk)
    orders_filter = OrderFilter(request.GET, queryset=Order.objects.filter(customer=customer))
    orders = orders_filter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'orders_filter': orders_filter,
    }

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@group_specific('admin')
def update_customer(request, customer_pk):
    next = request.META['HTTP_REFERER']
    customer = Customer.objects.get(id=customer_pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            next = request.POST.get('next')
            return redirect(next)

    context = {
        'form': form,
        'next': next
    }

    return render(request, 'accounts/update_customer.html', context)


@login_required(login_url='login')
@group_specific('admin')
def create_order(request, customer_pk):
    next = request.META['HTTP_REFERER']
    customer = Customer.objects.get(id=customer_pk)
    form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            next = request.POST.get('next')
            return redirect(next)

    context = {
        'form': form,
        'next': next
    }

    return render(request, 'accounts/order.html', context)


@login_required(login_url='login')
@group_specific('admin')
def update_order(request, order_pk):
    next = request.META['HTTP_REFERER']
    order = Order.objects.get(id=order_pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            next = request.POST.get('next')
            return redirect(next)

    context = {
        'form': form,
        'next': next
    }

    return render(request, 'accounts/order.html', context)


@login_required(login_url='login')
@group_specific('admin')
def delete_order(request, order_pk):
    next = request.META['HTTP_REFERER']
    order = Order.objects.get(id=order_pk)

    if request.method == 'POST':
        order.delete()
        next = request.POST.get('next')
        return redirect(next)

    context = {
        'order': order,
        'next': next
    }

    return render(request, 'accounts/delete_confirm.html', context)
