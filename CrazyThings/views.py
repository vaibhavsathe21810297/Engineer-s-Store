from django import views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.forms import Form
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced,Feedback
from .forms import  CustomerRegistrationForm,CustomerProfileForm,feedbackForm
from django.contrib import messages
from CrazyThings import models
from CrazyThings.models import Customer
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
# from .serializers import CustomerSerializer, OrderPlacedSerializer,ProductSerializer,CartSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class ProductView(View):
  def get(self, request):
     totalitem=0
     cricket = Product.objects.filter(category='cr')
     badminton = Product.objects.filter(category='ba')
     cycling = Product.objects.filter(category='cy')
     football = Product.objects.filter(category='fo')
     swimming = Product.objects.filter(category='sw')
     volleyball = Product.objects.filter(category='vb')
     basketball = Product.objects.filter(category='bb')
     tabletennis = Product.objects.filter(category='tt')
     mobile = Product.objects.filter(category='m')

     chair= Product.objects.filter(category='ch')
     table= Product.objects.filter(category='tb')
     officechair= Product.objects.filter(category='oc')
     officetable=Product.objects.filter(category='ot')
     kidsseating=Product.objects.filter(category='kst')
     kidsstudy=Product.objects.filter(category='ks')
     if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
     return render(request, 'home.html',{'mobile':mobile,'cricket':cricket,'badminton':badminton,'cycling':cycling,'football':football,'swimming':swimming,'volleyball':volleyball,'basketball':basketball,'tabletennis':tabletennis,'chair':chair,'table':table,'officechair':officechair,'totalitem':totalitem,'officetable':officetable,'kidsseating':kidsseating,'kidsstudy':kidsstudy})


class ProductDetailView(View):
    def get(self,request,pk):
       totalitem=0
       product= Product.objects.get(pk=pk)
       item_already_in_cart =False
       if request.user.is_authenticated:
        item_already_in_cart=Cart.objects.filter(Q(product=product.id)& Q(user=request.user)).exists()
        if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
       return render(request,'productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})


@login_required
def add_to_cart(request):
 totalitem=0
 user=request.user
 product_id=request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 if request.user.is_authenticated:
  totalitem= len(Cart.objects.filter(user=request.user))
 return redirect('/cart',{'totalitem':totalitem})


def show_cart(request):
 if request.user.is_authenticated:
     totalitem=0
     user=request.user
     cart=Cart.objects.filter(user=user)
     amount=0.0
     shipping_amount=70.0
     totalamount=0.0
     cart_product=[p for p in Cart.objects.all() if p.user==user]
     if request.user.is_authenticated:
      totalitem= len(Cart.objects.filter(user=request.user))
     if cart_product:
         for p in cart_product:
             tempamount=(p.quantity * p.product.discounted_price)
             amount+=tempamount
             totalamount=amount+shipping_amount
         return render(request, 'addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'shipping_amount':shipping_amount,'totalitem':totalitem})
     else:
         return render(request,'emptycart.html')

def buy_now(request):
 return render(request, 'buynow.html')

def address(request):
 totalitem=0
 add =Customer.objects.filter(user=request.user)
 if request.user.is_authenticated:
  totalitem= len(Cart.objects.filter(user=request.user))
 return render(request, 'address.html',{'add':add,'active':'btn-warning','totalitem':totalitem})

def orders(request):
 totalitem=0
 op=OrderPlaced.objects.filter(user=request.user)
 if request.user.is_authenticated:
         totalitem= len(Cart.objects.filter(user=request.user))
 return render(request, 'orders.html',{'order_placed':op,'totalitem':totalitem})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations!! You are registered Successfully.')
        return render(request, 'customerregistration.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class Feedbacks(View):
    def get(self, request):
        form = feedbackForm()
        return render(request, 'feedback.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = feedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            city = form.cleaned_data['city']
            pincode = form.cleaned_data['pincode']
            state = form.cleaned_data['state']
            description = form.cleaned_data['description']
            reg = Feedback(name=name, mobile=mobile, city=city, pincode=pincode, state=state, description=description)
            reg.save()
            messages.success(request, 'Congratulations!! Feedback Submit Successfully.')
        return render(request, 'feedback.html', {'form': form, 'active': 'btn-primary'})


@login_required
def checkout(request):
    totalitem = 0
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
    totalamount = amount + shipping_amount
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'checkout.html',
                  {'add': add, 'totalamount': totalamount, 'cart_items': cart_items, 'totalitem': totalitem})


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
    totalitem = 0

    def get(self, request):
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'profile.html', {'form': form, 'active': 'btn-warning', 'totalitem': totalitem})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, mobile=mobile, locality=locality, city=city, state=state,
                           zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile Updated Successfully')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'profile.html', {'form': form, 'active': 'btn-warning', 'totalitem': totalitem})


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }

        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }

        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount

        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }

        return JsonResponse(data)



def cricket(request, data=None):
   totalitem = 0
   if data == None:
      cricket = Product.objects.filter(category='cr')
   elif data == 'Bat':
       cricket = Product.objects.filter(category='cr').filter(brand=data)
   elif data == 'Ball':
       cricket = Product.objects.filter(category='cr').filter(brand=data)
   elif data == 'ProtectiveGears':
       cricket = Product.objects.filter(category='cr').filter(brand=data)
   elif data == 'Clothes':
       cricket = Product.objects.filter(category='cr').filter(brand=data)
   elif data == 'Shoes':
       cricket = Product.objects.filter(category='cr').filter(brand=data)
   elif data == 'Kitbags':
       cricket = Product.objects.filter(category='cr').filter(brand=data)
   elif data == 'below':
      cricket = Product.objects.filter(category='cr').filter(discounted_price__lt=500)
   elif data == 'above':
      cricket = Product.objects.filter(category='cr').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'sports/cricket.html', {'cricket': cricket, 'totalitem': totalitem})

def badminton(request, data=None):
   totalitem = 0
   if data == None:
      badminton = Product.objects.filter(category='ba')
   elif data == 'Racket':
      badminton = Product.objects.filter(category='ba').filter(brand=data)
   elif data == 'Cock':
      badminton = Product.objects.filter(category='ba').filter(brand=data)
   elif data == 'Kit':
      badminton = Product.objects.filter(category='ba').filter(brand=data)
   elif data == 'below':
      badminton = Product.objects.filter(category='ba').filter(discounted_price__lt=500)
   elif data == 'above':
      badminton = Product.objects.filter(category='ba').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'sports/badminton.html', {'badminton': badminton, 'totalitem': totalitem})

def cycling(request, data=None):
   totalitem = 0
   if data == None:
      cycling = Product.objects.filter(category='cy')
   elif data == 'Lock':
       cycling = Product.objects.filter(category='cy').filter(brand=data)
   elif data == 'Helmet':
       cycling = Product.objects.filter(category='cy').filter(brand=data)
   elif data == 'WithoutGear':
       cycling = Product.objects.filter(category='cy').filter(brand=data)
   elif data == 'WithGear':
       cycling = Product.objects.filter(category='cy').filter(brand=data)
   elif data == 'below':
      cycling = Product.objects.filter(category='cy').filter(discounted_price__lt=500)
   elif data == 'above':
      cycling = Product.objects.filter(category='cy').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'sports/cycling.html', {'cycling': cycling, 'totalitem': totalitem})

def football(request, data=None):
   totalitem = 0
   if data == None:
      football = Product.objects.filter(category='fo')
   elif data == 'Train':
      football = Product.objects.filter(category='fo').filter(brand=data)
   elif data == 'Gloves':
      football = Product.objects.filter(category='fo').filter(brand=data)
   elif data == 'FootBall':
      football = Product.objects.filter(category='fo').filter(brand=data)
   elif data == 'below':
      football = Product.objects.filter(category='fo').filter(discounted_price__lt=500)
   elif data == 'above':
      football = Product.objects.filter(category='fo').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'sports/football.html', {'football': football, 'totalitem': totalitem})

def swimming(request, data=None):
   totalitem = 0
   if data == None:
      swimming = Product.objects.filter(category='sw')
   elif data == 'Goggles':
       swimming = Product.objects.filter(category='sw').filter(brand=data)
   elif data == 'Costumes':
       swimming = Product.objects.filter(category='sw').filter(brand=data)
   elif data == 'below':
      swimming = Product.objects.filter(category='sw').filter(discounted_price__lt=500)
   elif data == 'above':
      swimming = Product.objects.filter(category='sw').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'sports/swimming.html', {'swimming': swimming, 'totalitem': totalitem})

def volleyball(request, data=None):
   totalitem = 0
   if data == None:
      volleyball = Product.objects.filter(category='vb')
   elif data == 'below':
      volleyball = Product.objects.filter(category='vb').filter(discounted_price__lt=500)
   elif data == 'above':
      volleyball = Product.objects.filter(category='vb').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'sports/volleyball.html', {'volleyball': volleyball, 'totalitem': totalitem})

def basketball(request, data=None):
   totalitem = 0
   if data == None:
      basketball = Product.objects.filter(category='bb')
   elif data == 'below':
      basketball = Product.objects.filter(category='bb').filter(discounted_price__lt=500)
   elif data == 'above':
      basketball = Product.objects.filter(category='bb').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'sports/basketball.html', {'basketball': basketball, 'totalitem': totalitem})

def tabletennis(request, data=None):
   totalitem = 0
   if data == None:
      tabletennis = Product.objects.filter(category='tt')
   elif data == 'below':
      tabletennis = Product.objects.filter(category='tt').filter(discounted_price__lt=500)
   elif data == 'above':
      tabletennis = Product.objects.filter(category='tt').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'sports/tabletennis.html', {'tabletennis': tabletennis, 'totalitem': totalitem})

# 2nd Module

def mobile(request, data=None):
   totalitem = 0
   if data == None:
      mobile = Product.objects.filter(category='m')
   elif data == 'below':
      mobile = Product.objects.filter(category='m').filter(discounted_price__lt=500)
   elif data == 'above':
      mobile = Product.objects.filter(category='m').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'electronics/mobile.html', {'mobile': mobile, 'totalitem': totalitem})

def television(request, data=None):
   totalitem = 0
   if data == None:
      television = Product.objects.filter(category='tv')
   elif data == 'below':
      television = Product.objects.filter(category='tv').filter(discounted_price__lt=500)
   elif data == 'above':
      television = Product.objects.filter(category='tv').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'electronics/television.html', {'television': television, 'totalitem': totalitem})

def laptop(request, data=None):
   totalitem = 0
   if data == None:
      laptop = Product.objects.filter(category='l')
   elif data == 'below':
      laptop = Product.objects.filter(category='l').filter(discounted_price__lt=500)
   elif data == 'above':
      laptop = Product.objects.filter(category='l').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'electronics/laptop.html', {'laptop': laptop, 'totalitem': totalitem})

def camera(request, data=None):
   totalitem = 0
   if data == None:
      camera = Product.objects.filter(category='c')
   elif data == 'below':
      camera = Product.objects.filter(category='c').filter(discounted_price__lt=500)
   elif data == 'above':
      camera = Product.objects.filter(category='c').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'electronics/camera.html', {'camera': camera, 'totalitem': totalitem})

def headset(request, data=None):
   totalitem = 0
   if data == None:
      headset = Product.objects.filter(category='hp')
   elif data == 'below':
      headset = Product.objects.filter(category='hp').filter(discounted_price__lt=500)
   elif data == 'above':
      headset = Product.objects.filter(category='hp').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'electronics/headset.html', {'headset': headset, 'totalitem': totalitem})

def speaker(request, data=None):
   totalitem = 0
   if data == None:
      speaker = Product.objects.filter(category='s')
   elif data == 'below':
      speaker = Product.objects.filter(category='s').filter(discounted_price__lt=500)
   elif data == 'above':
      speaker = Product.objects.filter(category='s').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'electronics/speaker.html', {'speaker': speaker, 'totalitem': totalitem})

def smartwatches(request, data=None):
   totalitem = 0
   if data == None:
      smartwatches = Product.objects.filter(category='sm')
   elif data == 'below':
      smartwatches = Product.objects.filter(category='sm').filter(discounted_price__lt=500)
   elif data == 'above':
      smartwatches = Product.objects.filter(category='sm').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'electronics/smartwatches.html', {'smartwatches': smartwatches, 'totalitem': totalitem})

def printer(request, data=None):
   totalitem = 0
   if data == None:
      printer = Product.objects.filter(category='p')
   elif data == 'below':
      printer = Product.objects.filter(category='p').filter(discounted_price__lt=500)
   elif data == 'above':
      printer = Product.objects.filter(category='p').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'electronics/printer.html', {'printer': printer, 'totalitem': totalitem})

def beds(request, data=None):
   totalitem = 0
   if data == None:
      beds = Product.objects.filter(category='b')
   elif data == 'below':
      beds = Product.objects.filter(category='b').filter(discounted_price__lt=500)
   elif data == 'above':
      beds = Product.objects.filter(category='b').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'furniture/beds.html', {'beds': beds, 'totalitem': totalitem})

def sofas(request, data=None):
   totalitem = 0
   if data == None:
      sofas = Product.objects.filter(category='so')
   elif data == 'below':
      sofas = Product.objects.filter(category='so').filter(discounted_price__lt=500)
   elif data == 'above':
      sofas = Product.objects.filter(category='so').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'furniture/sofas.html', {'sofas': sofas, 'totalitem': totalitem})

def chairs(request, data=None):
   totalitem = 0
   if data == None:
      chairs = Product.objects.filter(category='ch')
   elif data == 'below':
      chairs = Product.objects.filter(category='ch').filter(discounted_price__lt=500)
   elif data == 'above':
      chairs = Product.objects.filter(category='ch').filter(discounted_price__gt=500)
   if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'furniture/chairs.html', {'chairs': chairs, 'totalitem': totalitem})

def tables(request, data=None):
    totalitem = 0
    if data == None:
        tables = Product.objects.filter(category='t')
    elif data == 'below':
        tables = Product.objects.filter(category='t').filter(discounted_price__lt=500)
    elif data == 'above':
        tables = Product.objects.filter(category='t').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'furniture/tables.html', {'tables': tables, 'totalitem': totalitem})

def wardrobes(request, data=None):
    totalitem = 0
    if data == None:
        wardrobes = Product.objects.filter(category='wr')
    elif data == 'below':
        wardrobes = Product.objects.filter(category='wr').filter(discounted_price__lt=500)
    elif data == 'above':
        wardrobes = Product.objects.filter(category='wr').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'furniture/wardrobes.html', {'wardrobes': wardrobes, 'totalitem': totalitem})

def shelves(request, data=None):
    totalitem = 0
    if data == None:
        shelves = Product.objects.filter(category='sh')
    elif data == 'below':
        shelves = Product.objects.filter(category='sh').filter(discounted_price__lt=500)
    elif data == 'above':
        shelves = Product.objects.filter(category='sh').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'furniture/shelves.html', {'shelves': shelves, 'totalitem': totalitem})

def cabinets(request, data=None):
    totalitem = 0
    if data == None:
        cabinets = Product.objects.filter(category='ca')
    elif data == 'below':
        cabinets = Product.objects.filter(category='ca').filter(discounted_price__lt=500)
    elif data == 'above':
        cabinets = Product.objects.filter(category='ca').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'furniture/cabinets.html', {'cabinets': cabinets, 'totalitem': totalitem})

def children(request, data=None):
    totalitem = 0
    if data == None:
        children = Product.objects.filter(category='cd')
    elif data == 'below':
        children = Product.objects.filter(category='cd').filter(discounted_price__lt=500)
    elif data == 'above':
        children = Product.objects.filter(category='cd').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'books/children.html', {'children': children, 'totalitem': totalitem})

def comic(request, data=None):
    totalitem = 0
    if data == None:
        comic = Product.objects.filter(category='cm')
    elif data == 'below':
        comic = Product.objects.filter(category='cm').filter(discounted_price__lt=500)
    elif data == 'above':
        comic = Product.objects.filter(category='cm').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'books/comic.html', {'comic': comic, 'totalitem': totalitem})

def exam(request, data=None):
    totalitem = 0
    if data == None:
        exam = Product.objects.filter(category='ex')
    elif data == 'below':
        exam = Product.objects.filter(category='ex').filter(discounted_price__lt=500)
    elif data == 'above':
        exam = Product.objects.filter(category='ex').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'books/exam.html', {'exam': exam, 'totalitem': totalitem})

def school(request, data=None):
    totalitem = 0
    if data == None:
        school = Product.objects.filter(category='sc')
    elif data == 'below':
        school = Product.objects.filter(category='sc').filter(discounted_price__lt=500)
    elif data == 'above':
        school = Product.objects.filter(category='sc').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'books/school.html', {'school': school, 'totalitem': totalitem})

def university(request, data=None):
    totalitem = 0
    if data == None:
        university = Product.objects.filter(category='un')
    elif data == 'below':
        university = Product.objects.filter(category='un').filter(discounted_price__lt=500)
    elif data == 'above':
        university = Product.objects.filter(category='un').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'books/university.html', {'university': university, 'totalitem': totalitem})

def air(request, data=None):
    totalitem = 0
    if data == None:
        air = Product.objects.filter(category='ac')
    elif data == 'below':
        air = Product.objects.filter(category='ac').filter(discounted_price__lt=500)
    elif data == 'above':
        air = Product.objects.filter(category='ac').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'appliances/air.html', {'air': air, 'totalitem': totalitem})

def refrigerator(request, data=None):
    totalitem = 0
    if data == None:
        refrigerator = Product.objects.filter(category='r')
    elif data == 'below':
        refrigerator = Product.objects.filter(category='r').filter(discounted_price__lt=500)
    elif data == 'above':
        refrigerator = Product.objects.filter(category='r').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'appliances/refrigerator.html', {'refrigerator': refrigerator, 'totalitem': totalitem})

def washing(request, data=None):
    totalitem = 0
    if data == None:
        washing = Product.objects.filter(category='w')
    elif data == 'below':
        washing = Product.objects.filter(category='w').filter(discounted_price__lt=500)
    elif data == 'above':
        washing = Product.objects.filter(category='w').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'appliances/washing.html', {'washing': washing, 'totalitem': totalitem})

def cooler(request, data=None):
    totalitem = 0
    if data == None:
        cooler = Product.objects.filter(category='cl')
    elif data == 'below':
        cooler = Product.objects.filter(category='cl').filter(discounted_price__lt=500)
    elif data == 'above':
        cooler = Product.objects.filter(category='cl').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'appliances/cooler.html', {'cooler': cooler, 'totalitem': totalitem})

def fan(request, data=None):
    totalitem = 0
    if data == None:
        fan = Product.objects.filter(category='f')
    elif data == 'below':
        fan = Product.objects.filter(category='f').filter(discounted_price__lt=500)
    elif data == 'above':
        fan = Product.objects.filter(category='f').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'appliances/fan.html', {'fan': fan, 'totalitem': totalitem})

def fruitvegetable(request, data=None):
    totalitem = 0
    if data == None:
        fruitvegetable = Product.objects.filter(category='fv')
    elif data == 'below':
        fruitvegetable = Product.objects.filter(category='fv').filter(discounted_price__lt=500)
    elif data == 'above':
        fruitvegetable = Product.objects.filter(category='fv').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'grocery/fruitvegetable.html', {'fruitvegetable': fruitvegetable, 'totalitem': totalitem})


def beverages(request, data=None):
    totalitem = 0
    if data == None:
        beverages = Product.objects.filter(category='be')
    elif data == 'below':
        beverages = Product.objects.filter(category='be').filter(discounted_price__lt=500)
    elif data == 'above':
        beverages = Product.objects.filter(category='be').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'grocery/beverages.html', {'beverages': beverages, 'totalitem': totalitem})

def foodgrains(request, data=None):
    totalitem = 0
    if data == None:
        foodgrains = Product.objects.filter(category='fg')
    elif data == 'below':
        foodgrains = Product.objects.filter(category='fg').filter(discounted_price__lt=500)
    elif data == 'above':
        foodgrains = Product.objects.filter(category='fg').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'grocery/foodgrains.html', {'foodgrains': foodgrains, 'totalitem': totalitem})

def cookies(request, data=None):
    totalitem = 0
    if data == None:
        cookies = Product.objects.filter(category='co')
    elif data == 'below':
        cookies = Product.objects.filter(category='co').filter(discounted_price__lt=500)
    elif data == 'above':
        cookies = Product.objects.filter(category='co').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'grocery/cookies.html', {'cookies': cookies, 'totalitem': totalitem})

def noodles(request, data=None):
    totalitem = 0
    if data == None:
        noodles = Product.objects.filter(category='no')
    elif data == 'below':
        noodles = Product.objects.filter(category='no').filter(discounted_price__lt=500)
    elif data == 'above':
        noodles = Product.objects.filter(category='no').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'grocery/noodles.html', {'noodles': noodles, 'totalitem': totalitem})

def oil(request, data=None):
    totalitem = 0
    if data == None:
        oil = Product.objects.filter(category='ol')
    elif data == 'below':
        oil = Product.objects.filter(category='ol').filter(discounted_price__lt=500)
    elif data == 'above':
        oil = Product.objects.filter(category='ol').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'grocery/oil.html', {'oil': oil, 'totalitem': totalitem})

def snacks(request, data=None):
    totalitem = 0
    if data == None:
        snacks = Product.objects.filter(category='sn')
    elif data == 'below':
        snacks = Product.objects.filter(category='sn').filter(discounted_price__lt=500)
    elif data == 'above':
        snacks = Product.objects.filter(category='sn').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'grocery/snacks.html', {'snacks': snacks, 'totalitem': totalitem})

def deo(request, data=None):
    totalitem = 0
    if data == None:
        deo = Product.objects.filter(category='de')
    elif data == 'below':
        deo = Product.objects.filter(category='de').filter(discounted_price__lt=500)
    elif data == 'above':
        deo = Product.objects.filter(category='de').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'grocery/deo.html', {'deo': deo, 'totalitem': totalitem})
