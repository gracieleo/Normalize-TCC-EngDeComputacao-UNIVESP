from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self, request):
        totalitem = 0
        protecaoCabeca = Product.objects.filter(category='PC')
        protecaoAuditiva = Product.objects.filter(category='PA')
        protecaoRespiratoria = Product.objects.filter(category='PR')
        protecaoMaos = Product.objects.filter(category='PM')
        protecaoPes = Product.objects.filter(category='PP')
        
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',
        {'protecaoCabeca': protecaoCabeca,
         'protecaoAuditiva': protecaoAuditiva, 
         'protecaoRespiratoria': protecaoRespiratoria,
         'protecaoMaos': protecaoMaos,
         'protecaoPes': protecaoPes,
         'totalitem':totalitem})

class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', 
        {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 15.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount
            totalamount = ("%.2f" % totalamount)
        return render(request, 'app/addtocart.html', 
        {'carts':cart, 'totalamount':totalamount, 'amount':amount, 'totalitem':totalitem})
    else:
        return render(request, 'app/emptycart.html',{'totalitem':totalitem})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 15.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
         'quantity': c.quantity,
         'amount':amount,
         'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 15.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
         'quantity': c.quantity,
         'amount':amount,
         'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 15.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
          
        data = {
         'amount':amount,
         'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add,'active':'btn-primary'})

@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html', {'order_placed':op})

def capacete(request, data=None):
    if data == None:
        capacete = Product.objects.filter(category='PC').filter(sub_category='capacete')
    elif data == '3M' or data == 'Montana' or data == 'Camper' or data == 'Floresta':
        capacete = Product.objects.filter(category='PC').filter(brand=data).filter(sub_category='capacete')
    elif data == 'abaixo':
        capacete = Product.objects.filter(category='PC').filter(sub_category='capacete').filter(discounted_price__lt=50)
    elif data == 'acima':
        capacete = Product.objects.filter(category='PC').filter(sub_category='capacete').filter(discounted_price__gt=50)
    return render(request, 'app/capacete.html',{'capacete':capacete})

def touca(request, data=None):
    if data == None:
        touca = Product.objects.filter(category='PC').filter(sub_category='touca')
    elif data == '3M' or data == 'Montana' or data == 'Camper' or data == 'Floresta':
        touca = Product.objects.filter(category='PC').filter(brand=data).filter(sub_category='touca')
    elif data == 'abaixo':
        touca = Product.objects.filter(category='PC').filter(sub_category='touca').filter(discounted_price__lt=10)
    elif data == 'acima':
        touca = Product.objects.filter(category='PC').filter(sub_category='touca').filter(discounted_price__gt=10)
    return render(request, 'app/touca.html',{'touca':touca})

def protetorFacial(request, data=None):
    if data == None:
        protetorFacial = Product.objects.filter(category='PC').filter(sub_category='protetor-facial')
    elif data == '3M' or data == 'Montana' or data == 'Camper' or data == 'Floresta':
        protetorFacial = Product.objects.filter(category='PC').filter(brand=data).filter(sub_category='protetor-facial')
    elif data == 'abaixo':
        protetorFacial = Product.objects.filter(category='PC').filter(sub_category='protetor-facial').filter(discounted_price__lt=50)
    elif data == 'acima':
        protetorFacial = Product.objects.filter(category='PC').filter(sub_category='protetor-facial').filter(discounted_price__gt=50)
    return render(request, 'app/protetorFacial.html',{'protetorFacial':protetorFacial})

def abafadorConcha(request, data=None):
    if data == None:
        abafadorConcha = Product.objects.filter(category='PA').filter(sub_category='abafador-concha')
    elif data == '3M' or data == 'Dystry' or data == 'DeltaPlus':
        abafadorConcha = Product.objects.filter(category='PA').filter(brand=data).filter(sub_category='abafador-concha')
    elif data == 'abaixo':
        abafadorConcha = Product.objects.filter(category='PA').filter(sub_category='abafador-concha').filter(discounted_price__lt=100)
    elif data == 'acima':
        abafadorConcha = Product.objects.filter(category='PA').filter(sub_category='abafador-concha').filter(discounted_price__gt=100)
    return render(request, 'app/abafadorConcha.html',{'abafadorConcha':abafadorConcha})

def protetorPlug(request, data=None):
    if data == None:
        protetorPlug = Product.objects.filter(category='PA').filter(sub_category='protetor-auricular-plug')
    elif data == '3M' or data == 'PompPlus':
        protetorPlug = Product.objects.filter(category='PA').filter(brand=data).filter(sub_category='protetor-auricular-plug')
    elif data == 'abaixo':
        protetorPlug = Product.objects.filter(category='PA').filter(sub_category='protetor-auricular-plug').filter(discounted_price__lt=2)
    elif data == 'acima':
        protetorPlug = Product.objects.filter(category='PA').filter(sub_category='protetor-auricular-plug').filter(discounted_price__gt=2)
    return render(request, 'app/protetorPlug.html',{'protetorPlug':protetorPlug})

def mascaraPFF2(request, data=None):
    if data == None:
        mascaraPFF2 = Product.objects.filter(category='PR').filter(sub_category='mascara')
    elif data == '3M' or data == 'AirSafety' or data == 'Camper':
        mascaraPFF2 = Product.objects.filter(category='PR').filter(brand=data).filter(sub_category='mascara')
    elif data == 'abaixo':
        mascaraPFF2 = Product.objects.filter(category='PR').filter(sub_category='mascara').filter(discounted_price__lt=2)
    elif data == 'acima':
        mascaraPFF2 = Product.objects.filter(category='PR').filter(sub_category='mascara').filter(discounted_price__gt=2)
    return render(request, 'app/mascaraPFF2.html',{'mascaraPFF2':mascaraPFF2})

def mascaraSemiFacial(request, data=None):
    if data == None:
        mascaraSemiFacial = Product.objects.filter(category='PR').filter(sub_category='respirador')
    elif data == 'DeltaPlus' or data == 'AirSafety' or data == 'HoneyWell':
        mascaraSemiFacial = Product.objects.filter(category='PR').filter(brand=data).filter(sub_category='respirador')
    elif data == 'abaixo':
        mascaraSemiFacial = Product.objects.filter(category='PR').filter(sub_category='respirador').filter(discounted_price__lt=1000)
    elif data == 'acima':
        mascaraSemiFacial = Product.objects.filter(category='PR').filter(sub_category='respirador').filter(discounted_price__gt=1000)
    return render(request, 'app/mascaraSemiFacial.html',{'mascaraSemiFacial':mascaraSemiFacial})

def luvaRaspa(request, data=None):
    if data == None:
        luvaRaspa = Product.objects.filter(category='PM').filter(sub_category='luva-raspa')
    elif data == 'ThermplusPromat' or data == 'Danny' or data == 'DeltaPlus' or data == 'Arclan':
        luvaRaspa = Product.objects.filter(category='PM').filter(brand=data).filter(sub_category='luva-raspa')
    elif data == 'abaixo':
        luvaRaspa = Product.objects.filter(category='PM').filter(sub_category='luva-raspa').filter(discounted_price__lt=30)
    elif data == 'acima':
        luvaRaspa = Product.objects.filter(category='PM').filter(sub_category='luva-raspa').filter(discounted_price__gt=30)
    return render(request, 'app/luvaRaspa.html',{'luvaRaspa':luvaRaspa})

def luvaAntiCorte(request, data=None):
    if data == None:
        luvaAntiCorte = Product.objects.filter(category='PM').filter(sub_category='luva-anti-corte')
    elif data == 'ThermplusPromat' or data == 'Danny' or data == 'DeltaPlus' or data == 'Arclan':
        luvaAntiCorte = Product.objects.filter(category='PM').filter(brand=data).filter(sub_category='luva-anti-corte')
    elif data == 'abaixo':
        luvaAntiCorte = Product.objects.filter(category='PM').filter(sub_category='luva-anti-corte').filter(discounted_price__lt=30)
    elif data == 'acima':
        luvaAntiCorte = Product.objects.filter(category='PM').filter(sub_category='luva-anti-corte').filter(discounted_price__gt=30)
    return render(request, 'app/luvaAntiCorte.html',{'luvaAntiCorte':luvaAntiCorte})

def botinaMetatarso(request, data=None):
    if data == None:
        botinaMetatarso = Product.objects.filter(category='PP').filter(sub_category='botina-metatarso')
    elif data == 'Fujiwara' or data == 'Marluvas' or data == 'Bracol':
        botinaMetatarso = Product.objects.filter(category='PP').filter(brand=data).filter(sub_category='botina-metatarso')
    elif data == 'abaixo':
        botinaMetatarso = Product.objects.filter(category='PP').filter(sub_category='botina-metatarso').filter(discounted_price__lt=100)
    elif data == 'acima':
        botinaMetatarso = Product.objects.filter(category='PP').filter(sub_category='botina-metatarso').filter(discounted_price__gt=100)
    return render(request, 'app/botinaMetatarso.html',{'botinaMetatarso':botinaMetatarso})

def botina(request, data=None):
    if data == None:
        botina = Product.objects.filter(category='PP').filter(sub_category='botina')
    elif data == 'Fujiwara' or data == 'Marluvas' or data == 'Bracol' or data == '3M':
        botina = Product.objects.filter(category='PP').filter(brand=data).filter(sub_category='botina')
    elif data == 'abaixo':
        botina = Product.objects.filter(category='PP').filter(sub_category='botina').filter(discounted_price__lt=100)
    elif data == 'acima':
        botina = Product.objects.filter(category='PP').filter(sub_category='botina').filter(discounted_price__gt=100)
    return render(request, 'app/botina.html',{'botina':botina})

def perneiraRaspa(request, data=None):
    if data == None:
        perneiraRaspa = Product.objects.filter(category='PP').filter(sub_category='perneira-raspa')
    elif data == 'Fujiwara' or data == 'Marluvas' or data == 'Bracol':
        perneiraRaspa = Product.objects.filter(category='PP').filter(brand=data).filter(sub_category='perneira-raspa')
    elif data == 'abaixo':
        perneiraRaspa = Product.objects.filter(category='PP').filter(sub_category='perneira-raspa').filter(discounted_price__lt=100)
    elif data == 'acima':
        perneiraRaspa = Product.objects.filter(category='PP').filter(sub_category='perneira-raspa').filter(discounted_price__gt=100)
    return render(request, 'app/perneiraRaspa.html',{'perneiraRaspa':perneiraRaspa})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 15.0
 totalamount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
    totalamount = amount + shipping_amount
    totalamount = ("%.2f" % totalamount)
 return render(request, 'app/checkout.html',{'add':add, 'totalamount':totalamount, 'cart_items':cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
           usr = request.user
           name = form.cleaned_data['name']
           locality = form.cleaned_data['locality']
           city = form.cleaned_data['city']
           state = form.cleaned_data['state']
           zipcode = form.cleaned_data['zipcode']
           reg = Customer(user=usr,name=name, locality=locality, city=city, state=state, zipcode=zipcode)
           reg.save()
           messages.success(request, 'Congratulations!! Profile Updated Successfully')
        return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})

       
def historia(request, data=None):
    return render(request, 'app/historia.html')

def contato(request, data=None):
    return render(request, 'app/contato.html')