import random
import requests
import json
from django.shortcuts import render,get_object_or_404, redirect
from django.http import JsonResponse
from .models import OTPLogin

# -------------------------
# PRODUCT DATA (STATIC)
# -------------------------
loans_data = {
    1: {
        "id": 1,
        "name": "RINGS",
        "price": 550000,
        "image": "img/myring.jpg",
        "description": "Beautiful luxury gold rings crafted for timeless elegance."
    },
    2: {
        "id": 2,
        "name": "BRACELET",
        "price": 1000000,
        "image": "img/bracelet.jpg",
        "description": "Premium gold bracelet with stunning handcrafted design."
    },
    3: {
        "id": 3,
        "name": "EARINGS",
        "price": 750000,
        "image": "img/earing.jpg",
        "description": "Elegant temple earrings perfect for weddings and festivals."
    },
    4: {
        "id": 4,
        "name": "NECKLACE",
        "price": 600000,
        "image": "img/neck.jpg",
        "description": "Royal necklace inspired by traditional temple jewellery."
    },
    5: {
        "id": 5,
        "name": "BANGELS",
        "price": 600000,
        "image": "img/bang.jpg",
        "description": "Wearing heritage proudly."
    },
    6: {
        "id": 6,
        "name": "ANKLE CHAIN",
        "price": 550000,
        "image": "img/kolusugirl.jpg",
        "description": "Heritage in every step."
    },
    7: {
        "id": 7,
        "name": "RING",
        "price": 150000,
        "image": "img/ringboy.jpg",
        "description": "Bold and Timeless."
    },
    8: {
        "id": 8,
        "name": "BRACELET",
        "price": 750000,
        "image": "img/braceletboy.jpg",
        "description":"Define your style."
    },
    9:{
        "id": 9,
        "name": "STUD",
        "price": 550000,
        "image": "img/studboy.jpg",
        "description":"Subtle elegance for him."
    },
    10: {
        "id": 10,
        "name": "CHAIN",
        "price":230000,
        "image": "img/chain_boy.jpg",
        "description": "A mark of heritage."
    },
    11: {
        "id": 11,
        "name": "WRISTBAND",
        "price":320000,
        "image": "img/kappuboy.jpg",
        "description":"Strong and sophisticated."
    },
    12: {
        "id": 12,
        "name": "CROSS DOLLER",
        "price":75000,
        "image": "img/dollerboy.jpg",
        "description":"The ultimate statement."
    },
}
json_data = json.dumps(loans_data, indent=4)
with open("loans_data.json", "w") as file:
    json.dump(loans_data, file, indent=4)


def product_list(request):
    products = Product.objects.all()
    return render(request, 'loans/product_list.html', {'products': products})



# -------------------------
# HOME 
# -------------------------
def home(request):
    return render(request, 'loans/home.html', {'products': loans_data.values()})


# -------------------------
# PRODUCT DETAIL
# -------------------------
def loan_detail(request, id):
    product = loans_data.get(id)

    if not product:
        return redirect('app:home')

    # Get 5 other products except current one
    related_products = []

    for key, value in loans_data.items():
        if key != id:
            related_products.append((key, value))

    related_products = related_products[:5]  # only 5 products

    return render(request, 'loans/loan_detail.html', {
        'product': product,
        'related_products': related_products
    })

    return render(request, 'loans/loan_detail.html', {'product': product})
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = loans_data.get(int(product_id))  # get from dictionary

        if not product:
            continue  # skip if product not found

        subtotal = product['price'] * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'loans/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    request.session.modified = True 

    return redirect('app:view_cart')  


# Remove from cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('app:view_cart')


# Update cart (increment/decrement)
def update_cart(request):
    if request.method == "POST":
        product_id = str(request.POST.get('product_id'))
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        if product_id not in cart:
            return JsonResponse({'success': False})

        # Increment
        if action == 'increment':
            cart[product_id] += 1

        # Decrement
        elif action == 'decrement':
            cart[product_id] -= 1
            if cart[product_id] <= 0:
                del cart[product_id]

        request.session['cart'] = cart

        # Rebuild cart data from dictionary
        cart_data = []
        total = 0

        for pid, qty in cart.items():
            product = loans_data.get(int(pid))
            if not product:
                continue

            subtotal = product['price'] * qty
            total += subtotal

            cart_data.append({
                'product_id': pid,
                'quantity': qty,
                'subtotal': subtotal
            })

        return JsonResponse({
            'success': True,
            'cart': cart_data,
            'total': total
        })

    return JsonResponse({'success': False})




# -------------------------
# BUY NOW
# -------------------------
def buy_now(request, product_id):
    return redirect('app:checkout', product_id=product_id)


# -------------------------
# CHECKOUT
# -------------------------


def checkout(request, product_id):

    # If user not logged in → go to login
    if not request.session.get('phone'):
        request.session['next_product'] = product_id
        return redirect('app:login')

    # Get product
    product = loans_data.get(int(product_id))

    if not product:
        return redirect('app:home')   # prevent None error

    product = product.copy()
    product['image_url'] = product['image']

    if request.method == "POST":

        quantity = int(request.POST.get('quantity', 1))

        doorno = request.POST.get('doorno')
        street = request.POST.get('street')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        address = f"{doorno}, {street}, {district}, {state} - {pincode}"

        payment = request.POST.get('payment')

        total = product['price'] * quantity

        return render(request, 'loans/order_success.html', {
            'product': product,
            'quantity': quantity,
            'total': total,
            'address': address,
            'payment': payment
        })

    return render(request, 'loans/checkout.html', {'product': product})
def gold_rate(request):
    rates = [
        {"weight": "1 gram", "price":14426},
        {"weight": "8 grams", "price":115128},
        {"weight": "10 grams", "price":159765},
        {"weight": "50 grams", "price":721300},
    ]
    return render(request, 'loans/gold_rate.html', {"rates": rates})

    return render(request, 'loans/checkout.html', {'product': product})
def faq_view(request):
    return render(request, 'loans/faq.html')
def about(request):
    return render(request, 'loans/about.html')
def contact(request):
    return render(request, 'loans/contact.html')
def checkout_cart(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('app:view_cart')
    
    checkout_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = loans_data.get(int(product_id)).copy()
        product['image_url'] = product['image']
        if product:
            subtotal = product['price'] * quantity
            total += subtotal
            checkout_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

    address = None
    payment = None
    if request.method == "POST":

        doorno = request.POST.get('DoorNo')
        street = request.POST.get('Street')
        district = request.POST.get('District')
        pincode = request.POST.get('Pincode')
        state = request.POST.get('State')

        quantity = int(request.POST.get('quantity', 1))
        payment = request.POST.get('payment')

        address = f"{doorno}, {street}, {district}, {state} - {pincode}"

        return render(request, 'loans/order_success.html', {
        'checkout_items': checkout_items,
        'total': total,
        'address': address,
        'payment': payment  
    })

    return render(request, 'loans/checkout_cart.html', {
        'checkout_items': checkout_items,
        'total': total
    })
    import random
def login_phone(request):

    if request.method == "POST":
        phone = request.POST.get("phone")

        otp = random.randint(1000,9999)

        print("OTP:", otp)   # OTP will show in terminal

        OTPLogin.objects.create(
            phone=phone,
            otp=otp
        )

        return render(request,"loans/verify_otp.html",{"phone":phone})

    return render(request,"loans/login.html")

    return render(request,"loans/login.html")
def verify_otp(request):

    print("VERIFY OTP VIEW RUNNING")

    if request.method == "POST":
        print("POST REQUEST RECEIVED")

        phone = request.POST.get("phone")
        otp = request.POST.get("otp")

        print("PHONE:", phone)
        print("OTP ENTERED:", otp)

        user = OTPLogin.objects.filter(phone=phone, otp=otp).first()

        if user:
            print("OTP SUCCESS")

            request.session['phone'] = phone

            product_id = request.session.get('next_product')

            if product_id:
                return redirect('app:checkout', product_id=product_id)

            return redirect('app:home')

        else:
            print("OTP FAILED")

            return render(request,"loans/verify_otp.html",{"error":"Invalid OTP","phone":phone})