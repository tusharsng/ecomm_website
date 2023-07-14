from django.shortcuts import render, get_object_or_404,redirect
from .models import Category, Product,Profile,Apply
from .forms import ApplyForm, CartAddProductForm, EditproductForm,ProfileForm
from django.views.decorators.http import require_POST
from .cart import Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict

import requests
from django.conf import settings
def home(request, category_slug=None):
    category = None
    categories = Category.objects.all()[:5]
    keyword = request.GET.get('q') 
    

    products = Product.objects.filter(available=True)
    if keyword :
        products = Product.objects.filter(available=True,name__icontains=keyword , description__icontains=keyword)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        if keyword:
            products=products.filter(category=category,name__icontains=keyword , description__icontains=keyword)
    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    return render(request,
                'home.html',
                {'category': category,
                'categories': categories,'keyword':keyword,
                'products': products})
                
                
def product_detail(request, id, slug):
    category = None
    categories = Category.objects.all()[:5]
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                'detail.html',
                {'categories': categories,
                'cart_product_form': cart_product_form,
                'product': product})



def cart_detail(request):
    cart = None
    cart = Cart(request)
    categories = Category.objects.all()[:5]
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={'quantity': item['quantity'],
                                        'update': True})
    return render(request, 'cart_detail.html', 
                {'cart': cart, 
                'categories': categories})
                
    
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')
    
    
@require_POST
def cart_add(request, product_id):
   
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
   
    form = CartAddProductForm(request.POST)
   
    if form.is_valid():
        
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                update_quantity=cd['update'])
        
    return redirect('cart_detail')

@login_required(login_url='/accounts/login/')
def profileupdate(request):
    user = request.user
    userprofile=Profile.objects.get(userpro=request.user)
    
    
    form = ProfileForm(initial={"bio":userprofile.bio, "pro_pic":userprofile.pro_pic})
  
    if request.method =="POST":
        form = ProfileForm(data=request.POST or None,files=request.FILES ,instance=userprofile)
  
      

        if form.is_valid():
            form.save(commit=False)
            
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''

            form.userpro=request.user.pk
            if result['success']:
                form.save()
                messages.success(request, 'Profile updated!')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return redirect('profileupdate')
            
 
        
    context ={
        
        'form':form, 
       
         }       
    return render(request, 'account/profile_update.html',context)
@login_required(login_url='/accounts/login/')
def profiles(request):
    user = request.user
   
    context ={
     
        'user':user,
        'obj':Profile.objects.get(userpro=user),
       #'obj':upload_short.objects.filter(user_id=id),
    }       
          
    return render(request, 'account/profile.html',context)
@login_required(login_url='/accounts/login/')
def applytobeaseller(request):
    user = request.user
    userprofile=Profile.objects.get(userpro=request.user)
    try:
        apply=Apply.objects.get(profile=userprofile)
    except:
        apply=None
    
    if request.method =="POST":
        if apply:
             messages.success(request, "You arleady submitted the document wait for it to be processed")
        else:

            form = ApplyForm(request.POST,request.FILES )

            if form.is_valid():
                b=form.save(commit=False)
                
                b.profile=userprofile
                b.applied=True
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
                    b.save()
                    messages.success(request, 'Submitted the document!')
                    return redirect('profile')
                else:
                    messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                    return redirect('apply')
                    
            else:
                messages.success(request, "wrong file format")
    form=ApplyForm()   
    context ={
        
        'form':form,"apply":apply  }       
    return render(request, 'account/sellerapply.html',context)


@login_required(login_url='/accounts/login/')
def myproducts(request):
    user = request.user
    posts = Product.objects.filter(creator=user).order_by('-created')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context ={
        
      'posts':posts ,
    
    }  


    return render(request,"account/myproducts.html",context)
@login_required(login_url='/accounts/login/')
def editproduct(request,id):
    product=Product.objects.get(id=id)
    data=model_to_dict(product)
    form=EditproductForm(initial=data)
    if request.method =="POST":
        form = EditproductForm(data=request.POST or None,files=request.FILES ,instance=product)
        if form.is_valid():
            form.save(commit=False)
            
     
            form.creator=product.creator
            form.save()
            return redirect('myproducts')
 
    context ={
        
      'product':product ,
      'form':form,
    
    }  
    return render(request,"account/editproduct.html",context)
@login_required(login_url='/accounts/login/')
def addproduct(request):
 
 
    form=EditproductForm()
    if request.method =="POST":
        form = EditproductForm(data=request.POST or None,files=request.FILES )
        print(form.errors)
        if form.is_valid():
            b=form.save(commit=False)
            b.creator=request.user
           
            b.save()
            return redirect('myproducts')
 
    context ={
        
     
      'form':form,
    
    }  
    return render(request,"account/addproduct.html",context)
@login_required(login_url='/accounts/login/')
def deleteproduct(request,id):
    product=Product.objects.get(id=id)
    product.delete()
    return redirect('myproducts')