from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth import authenticate, login, logout as auth_logout  # type: ignore
from django.contrib import messages # type: ignore
from .forms import MenuForm
from .models import Orders, Customer, Restaurant, Delivery_Driver, Menu
from django.http import Http404  # Add this import


# Create your views here.
def test(request):
    return render(request, "myApp/test.html")

def login(request):
    if request.method == 'POST':
        customer_id = request.POST['customer_id']
        password = request.POST['password']
        
        try:
            customer = Customer.objects.get(customer_id=customer_id, password=password)
            request.session['customer_id'] = customer.customer_id  # Store customer_id in session
            messages.success(request, 'Login successful')
            return render(request, "myApp/home.html", {'customer': customer})
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return render(request, "myApp/login.html")

    return render(request, "myApp/login.html")

def logout(request):
    auth_logout(request)
    request.session.pop('customer_id', None)
    messages.success(request, 'You have been logged out.')
    return render(request, "myApp/login.html")

def signup(request):
    if request.method == 'POST':
        customer_id = request.POST['customer_id']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']  # Get the confirm password
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        address = request.POST['address']

        # Check if passwords match
        if password != password_confirm:
            messages.error(request, 'Passwords must match')  # Error message
            return render(request, "myApp/signup.html")  # Render the signup page again

        # Create a new Customer instance
        customer = Customer(
            customer_id=customer_id,
            password=password,  # Consider hashing the password
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address
        )
        customer.save()
        messages.success(request, 'New user added')
        return render(request, "myApp/signup.html")
    return render(request, "myApp/signup.html")

def add_order(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')  # Get the item ID from the POST request
        menu_item = get_object_or_404(Menu, pk=item_id)  # Fetch the menu item
        
        # Retrieve the delivery address from the logged-in customer
        delivery_address = None
        order_customer = None  # Initialize order_customer
        if 'customer_id' in request.session:
            try:
                customer = Customer.objects.get(customer_id=request.session['customer_id'])
                delivery_address = customer.address  # Get the customer's address
                order_customer = customer.customer_id  # Get the customer_id for the order
            except Customer.DoesNotExist:
                delivery_address = ''  # Fallback if customer does not exist

        # Create a new order
        order = Orders(
            order_name=menu_item.item_name,
            order_description=menu_item.item_description,
            order_price=menu_item.item_price,
            orders_image=menu_item.image if menu_item.image else None,  # Set the image if it exists
            delivery_address=delivery_address,  # Use the customer's address
            order_customer=order_customer  # Associate the order with the customer
        )
        order.save()  # Save the order to the database
        messages.success(request, 'Order added successfully!')
        return redirect('Orders')  # Redirect back to the Orders page

    return redirect('Orders')  # Redirect if not a POST request

def delete_order(request, order_id):
    order_item = get_object_or_404(Orders, pk=order_id)
    order_item.delete()
    messages.success(request, 'Order removed successfully!')
    return redirect('Orders')

def home(request):
    customer = None
    if 'customer_id' in request.session:
        try:
            customer = Customer.objects.get(customer_id=request.session['customer_id'])
        except Customer.DoesNotExist:
            customer = None

    return render(request, "myApp/home.html", {'customer': customer})

def orders_list(request):
    customer = None
    if 'customer_id' in request.session:
        try:
            customer = Customer.objects.get(customer_id=request.session['customer_id'])
        except Customer.DoesNotExist:
            customer = None

    orders = Orders.objects.all()  # Fetch all orders from the database
    drivers = Delivery_Driver.objects.all()  # Fetch all delivery drivers
    context = {'orders': orders, 'customer': customer, 'drivers': drivers}  # Pass drivers to the template
    return render(request, "myApp/Orders.html", context)  # Pass orders to the template

def Drivers(request):
    customer = None
    if 'customer_id' in request.session:
        try:
            customer = Customer.objects.get(customer_id=request.session['customer_id'])
        except Customer.DoesNotExist:
            customer = None

    drivers = Delivery_Driver.objects.all()  # Fetch all delivery drivers
    context = {'drivers': drivers, 'customer': customer}
    return render(request, "myApp/Drivers.html", context)  # Pass drivers to the template

def McDonalds(request):
    customer = None
    if 'customer_id' in request.session:
        try:
            customer = Customer.objects.get(customer_id=request.session['customer_id'])
        except Customer.DoesNotExist:
            customer = None

    menu_items = Menu.objects.filter(restaurant_name2="McDonalds")
    context = {'menu_items': menu_items, 'customer': customer}
    return render(request, "myApp/McDonalds.html", context)

def Jollibee(request):
    customer = None
    if 'customer_id' in request.session:
        try:
            customer = Customer.objects.get(customer_id=request.session['customer_id'])
        except Customer.DoesNotExist:
            customer = None

    menu_items = Menu.objects.filter(restaurant_name2="Jollibee")
    context = {'menu_items': menu_items, 'customer': customer}
    return render(request, "myApp/Jollibee.html", context)

def KFC(request):
    customer = None
    if 'customer_id' in request.session:
        try:
            customer = Customer.objects.get(customer_id=request.session['customer_id'])
        except Customer.DoesNotExist:
            customer = None

    menu_items = Menu.objects.filter(restaurant_name2="KFC")
    context = {'menu_items': menu_items, 'customer': customer}
    return render(request, "myApp/KFC.html", context)

def BurgerKing(request):
    customer = None
    if 'customer_id' in request.session:
        try:
            customer = Customer.objects.get(customer_id=request.session['customer_id'])
        except Customer.DoesNotExist:
            customer = None

    menu_items = Menu.objects.filter(restaurant_name2="BurgerKing")
    context = {'menu_items': menu_items, 'customer': customer}
    return render(request, "myApp/BurgerKing.html", context)

def Chowking(request):
    customer = None
    if 'customer_id' in request.session:
        try:
            customer = Customer.objects.get(customer_id=request.session['customer_id'])
        except Customer.DoesNotExist:
            customer = None

    menu_items = Menu.objects.filter(restaurant_name2="Chowking")
    context = {'menu_items': menu_items, 'customer': customer}
    return render(request, "myApp/Chowking.html", context)

def Greenwich(request):
    customer = None
    if 'customer_id' in request.session:
        try:
            customer = Customer.objects.get(customer_id=request.session['customer_id'])
        except Customer.DoesNotExist:
            customer = None

    menu_items = Menu.objects.filter(restaurant_name2="Greenwich")
    context = {'menu_items': menu_items, 'customer': customer}
    return render(request, "myApp/Greenwich.html", context)

def MangInasal(request):
    customer = None
    if 'customer_id' in request.session:
        try:
            customer = Customer.objects.get(customer_id=request.session['customer_id'])
        except Customer.DoesNotExist:
            customer = None

    menu_items = Menu.objects.filter(restaurant_name2="MangInasal")
    context = {'menu_items': menu_items, 'customer': customer}
    return render(request, "myApp/MangInasal.html", context)

def PizzaHut(request):
    customer = None
    if 'customer_id' in request.session:
        try:
            customer = Customer.objects.get(customer_id=request.session['customer_id'])
        except Customer.DoesNotExist:
            customer = None

    menu_items = Menu.objects.filter(restaurant_name2="PizzaHut")
    context = {'menu_items': menu_items, 'customer': customer}
    return render(request, "myApp/PizzaHut.html", context)


#McDonalds-----------------------------------------------------------------------------------------------
def edit_menu(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('McDonalds')
    else:
        form = MenuForm(instance=menu_item)
    
    return render(request, "myApp/edit_menu.html", {'form': form, 'menu_item': menu_item})

def delete_menu(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    menu_item.delete()
    return redirect('McDonalds')

def add_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant_name2 = "McDonalds"
            menu_item.save()
            return redirect('McDonalds')
    else:
        form = MenuForm()
    
    return render(request, 'myApp/add_menu.html', {'form': form})


#Jollibee-----------------------------------------------------------------------------------------------
def edit_menu_jollibee(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('Jollibee')
    else:
        form = MenuForm(instance=menu_item)
    
    return render(request, "myApp/edit_menu_jollibee.html", {'form': form, 'menu_item': menu_item})

def delete_menu_jollibee(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    menu_item.delete()
    return redirect('Jollibee')

def add_menu_jollibee(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant_name2 = "Jollibee"
            menu_item.save()
            return redirect('Jollibee')
    else:
        form = MenuForm()
    
    return render(request, 'myApp/add_menu_jollibee.html', {'form': form})


#KFC-----------------------------------------------------------------------------------------------
def edit_menu_kfc(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('KFC')
    else:
        form = MenuForm(instance=menu_item)
    
    return render(request, "myApp/edit_menu_kfc.html", {'form': form, 'menu_item': menu_item})

def delete_menu_kfc(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    menu_item.delete()
    return redirect('KFC')

def add_menu_kfc(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant_name2 = "KFC"
            menu_item.save()
            return redirect('KFC')
    else:
        form = MenuForm()
    
    return render(request, 'myApp/add_menu_kfc.html', {'form': form})



#BurgerKing-----------------------------------------------------------------------------------------------
def edit_menu_burgerking(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('BurgerKing')
    else:
        form = MenuForm(instance=menu_item)
    
    return render(request, "myApp/edit_menu_burgerking.html", {'form': form, 'menu_item': menu_item})

def delete_menu_burgerking(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    menu_item.delete()
    return redirect('BurgerKing')

def add_menu_burgerking(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant_name2 = "BurgerKing"
            menu_item.save()
            return redirect('BurgerKing')
    else:
        form = MenuForm()
    
    return render(request, 'myApp/add_menu_burgerking.html', {'form': form})


#Chowking-----------------------------------------------------------------------------------------------
def edit_menu_chowking(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('Chowking')
    else:
        form = MenuForm(instance=menu_item)
    
    return render(request, "myApp/edit_menu_chowking.html", {'form': form, 'menu_item': menu_item})

def delete_menu_chowking(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    menu_item.delete()
    return redirect('Chowking')

def add_menu_chowking(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant_name2 = "Chowking"
            menu_item.save()
            return redirect('Chowking')
    else:
        form = MenuForm()
    
    return render(request, 'myApp/add_menu_chowking.html', {'form': form})


#MangInasal-----------------------------------------------------------------------------------------------
def edit_menu_manginasal(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('MangInasal')
    else:
        form = MenuForm(instance=menu_item)
    
    return render(request, "myApp/edit_menu_manginasal.html", {'form': form, 'menu_item': menu_item})

def delete_menu_manginasal(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    menu_item.delete()
    return redirect('MangInasal')

def add_menu_manginasal(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant_name2 = "MangInasal"
            menu_item.save()
            return redirect('MangInasal')
    else:
        form = MenuForm()
    
    return render(request, 'myApp/add_menu_manginasal.html', {'form': form})


#PizzaHut-----------------------------------------------------------------------------------------------
def edit_menu_pizzahut(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('PizzaHut')
    else:
        form = MenuForm(instance=menu_item)
    
    return render(request, "myApp/edit_menu_pizzahut.html", {'form': form, 'menu_item': menu_item})

def delete_menu_pizzahut(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    menu_item.delete()
    return redirect('PizzaHut')

def add_menu_pizzahut(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant_name2 = "PizzaHut"
            menu_item.save()
            return redirect('PizzaHut')
    else:
        form = MenuForm()
    
    return render(request, 'myApp/add_menu_pizzahut.html', {'form': form})
    

#Greenwich-----------------------------------------------------------------------------------------------
def edit_menu_greenwich(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('Greenwich')
    else:
        form = MenuForm(instance=menu_item)
    
    return render(request, "myApp/edit_menu_greenwich.html", {'form': form, 'menu_item': menu_item})

def delete_menu_greenwich(request, menu_id):
    menu_item = get_object_or_404(Menu, pk=menu_id)
    menu_item.delete()
    return redirect('Greenwich')

def add_menu_greenwich(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant_name2 = "Greenwich"
            menu_item.save()
            return redirect('Greenwich')
    else:
        form = MenuForm()
    
    return render(request, 'myApp/add_menu_greenwich.html', {'form': form})