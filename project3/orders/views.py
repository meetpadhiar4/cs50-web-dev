from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.urls import reverse
from django.db.models import Sum
from .models import Regular_pizza, Sicilian_pizza, Pasta, Subs, Dinner_platters, Salads, Toppings, OrderItem, Order

# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('home')
        else:
            return render(request, 'login.html', {"message": "Invalid credentails"})
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {"message": "Username already is exits, please try another username"})
            elif User.objects.filter(email=email).exists():
                return render(request, 'register.html', {"message": "Email already exists, please use another email address"})
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=firstname, last_name=lastname)
                user.save()
                print('user created')
                user_order = Order(user=user)
                user_order.save()
                return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, 'register.html', {"message": "Enter a correct password"})
    else:
        return render(request, 'register.html')


def home(request):
    context = {"regular_pizza": Regular_pizza.objects.first().category, "sicilian_pizza": Sicilian_pizza.objects.first().category,
               "pasta": Pasta.objects.first().category, "subs": Subs.objects.first().category, "dinner_platters": Dinner_platters.objects.first().category, "salads": Salads.objects.first().category,
               "toppings": Toppings.objects.first().category}
    return render(request, 'home.html', context=context)


def menu(request, category):
    if category == "Regular Pizza":
        items = Regular_pizza.objects.all()
    elif category == "Sicilian Pizza":
        items = Sicilian_pizza.objects.all()
    elif category == "Pasta":
        items = Pasta.objects.all()
    elif category == "Subs":
        items = Subs.objects.all()
    elif category == "Salads":
        items = Salads.objects.all()
    elif category == "Toppings":
        items = Toppings.objects.all()
    else:
        items = Dinner_platters.objects.all()
    return render(request, 'menu.html', {"items": items, "category": category})


def add(request, name, category, price):
    number_of_toppings = Order.objects.get(user=request.user)
    if category == "Regular Pizza" or category == "Sicilian Pizza":
        if name == "1 topping":
            number_of_toppings.number_of_toppings += 1
            number_of_toppings.save()
        elif name == "2 toppings":
            number_of_toppings.number_of_toppings += 2
            number_of_toppings.save()
        elif name == "3 toppings":
            number_of_toppings.number_of_toppings += 3
            number_of_toppings.save()
    if category == "Toppings" and number_of_toppings.number_of_toppings == 0:
        return render(request, 'menu.html', {"items": Toppings.objects.all(), "category": category, "message": "You have used all toppings"})
    if category == "Toppings" and number_of_toppings.number_of_toppings > 0:
        number_of_toppings.number_of_toppings -= 1
        number_of_toppings.save()
    add_order_item = OrderItem(
        user=request.user, name=name, category=category, price=price)
    add_order_item.save()
    context = {"name": name, "category": category,
               "price": price,
               "orderitems": OrderItem.objects.filter(user=request.user),
               "total": list(OrderItem.objects.filter(user=request.user).aggregate(Sum('price')).values())[0]}
    return render(request, 'order.html', context)


def cart(request):
    context = {"orderitems": OrderItem.objects.filter(user=request.user),
               "total": list(OrderItem.objects.filter(user=request.user).aggregate(Sum('price')).values())[0],
               "order": Order.objects.get(user=request.user)}
    return render(request, 'cart.html', context)


def confirm(request):
    order = Order.objects.get(user=request.user)
    order.status = "Initiated"
    order.save()
    return HttpResponseRedirect(reverse(cart))


def delete(request, name, category, price):
    number_of_toppings = Order.objects.get(user=request.user)
    if category == "Regular Pizza" or category == "Sicilian Pizza":
        if name == "1 topping":
            number_of_toppings.number_of_toppings -= 1
            number_of_toppings.save()
        if name == "2 toppings":
            number_of_toppings.number_of_toppings -= 2
            number_of_toppings.save()
        if name == "3 toppings":
            number_of_toppings.number_of_toppings -= 3
            number_of_toppings.save()
        number_of_toppings.number_of_toppings = 0
        number_of_toppings.save()
        delete_toppings = OrderItem.objects.filter(user=request.user, category="Toppings")
        delete_toppings.delete()
    if category == "Toppings":
        number_of_toppings.number_of_toppings += 1
        number_of_toppings.save()
    delete_item = OrderItem.objects.filter(
        user=request.user, name=name, category=category, price=price)
    delete_item.delete()
    context = {"name": name, "category": category,
               "price": price,
               "orderitems": OrderItem.objects.filter(user=request.user),
               "total": list(OrderItem.objects.filter(user=request.user).aggregate(Sum('price')).values())[0]}
    return render(request, 'order.html', context)
