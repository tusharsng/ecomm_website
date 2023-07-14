from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from orders.models import Payment,Order
from products.models import Category, Product
from products.cart import Cart
from .forms import OrderCreateForm
from django.conf import settings
from django.contrib import messages
import stripe

import requests

# Create your views here.
@login_required(login_url='/accounts/login/')
def order_create(request):
    cart = Cart(request)
#Multiply total price for stripe
    
    categories = Category.objects.all()
    total=0
    ids=[]
    
    for item in cart:
        
        total= int(item['total_price'] )
        ids.append(int(item['ids']))
        

    total = int(cart.get_total_price() )
    #get FORM
    products=Product.objects.filter(id__in= ids)
   
    if request.method == 'POST':
      
        form = OrderCreateForm(request.POST)
       
       
        if form.is_valid():
            cd = form.cleaned_data
            for item in cart:
                order = form.save(commit=False)
                order.save()
                for prod in products:
                    order.products.add(prod.id)

                if request.user:
                    order.user = request.user
                order.total = total
                ''' Begin reCAPTCHA validation '''
                recaptcha_response = request.POST.get('g-recaptcha-response')
                data = {
                    'secret': settings.RECAPTCHA_PRIVATE_KEY,
                    'response': recaptcha_response
                }
                r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
                result = r.json()
                ''' End reCAPTCHA validation '''


                if result['success']:
                    order.save()
                    messages.success(request, 'you created an Order !')
                    return redirect('my_order')
                else:
                    messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                    return redirect('order_create')
                   

            # clear the cart
            #cart.clear()
        
            
        
    else:
        
        form = OrderCreateForm()
        
    return render(request,
                'create.html',
                {'cart': cart, 'form': form,   'total':total,'categories': categories})



@login_required(login_url='/accounts/login/')
def sucess(request):
    sucess=Payment.objects.filter(user=request.user).last()

    return render(request,
                'sucess.html',
                {
                    'sucess':sucess,
                }
               )

#Importing stripe key
stripe.api_key = settings.STRIPE_SECRET
@login_required(login_url='/accounts/login/')
def payment(request,order_id):
    orders = Order.objects.get(user=request.user,id=order_id)
    cart = Cart(request)
    quantity=0
    products={}
    for item in cart:
        quantity+=int(item['quantity'])
       
#total price for stripe
    total = orders.total
    totaltosend=orders.total*100
    
    
    key = settings.STRIPE_PUBLISHABLE
   
    if request.method == 'POST':
        
  
        charge = stripe.PaymentIntent.create(
            amount= total,
            currency='usd',
            description= orders.id,
          
                 )  
        customer=stripe.Customer.create(
            name = orders.name,
            address = {
                "line1": orders.address,
                "postal_code": orders.zip_code,
                "city": "San Francisco",
                "state": "CA",
                "country": "US",
            },
            )
        if charge and customer:
            Payment.objects.create(order=orders,
                    
                                        price=orders.total,
                                        quantity=1,
                                        user=request.user
                                    )
        
            # clear the cart
            orders.paid=True
            
            orders.quantity=quantity
            orders.save()
            cart.clear()
    
            return redirect('sucess')
        return redirect('my_order')
    
        
    return render(request,
                'payment.html',
                {'cart': cart, 'orders':orders, 'key':key, 'total':total,
                'totaltosend':totaltosend})


@login_required(login_url='/accounts/login/')
def my_order(request):
    categories = Category.objects.all()
    orders = Order.objects.filter(user=request.user)
   
    return render(request, 'my_orders.html', {'orders':orders,'categories': categories})
