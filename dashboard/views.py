from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm,OrderForm
from django.contrib.auth.models import User
from .models import Order
from django.contrib import messages
# Create your views here.
@login_required
def index(request):
    orders=Order.objects.all()
    products=Product.objects.all()
    worker_count=User.objects.all().count()
    order_count=Order.objects.all().count()
    products_count=Product.objects.all().count()

    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            instance =form.save(commit=False)
            instance.staff=request.user
            
            product=instance.product
            if product.quantity > 0 and (instance.orderQty <= product.quantity) :
                product.quantity-=instance.orderQty
                product.save()
                
                instance.save()
            return redirect('dashboard-index')

    else:
        form=OrderForm()
    context={
        'orders':orders,
        'form':form,
        'products':products,
        'worker_count':worker_count,
        'order_count':order_count,
        'products_count':products_count,
    }
    return  render(request,'dashboard/index.html',context)

@login_required
def staff(request):
    workers=User.objects.all()
    worker_count=workers.count()
    order_count=Order.objects.all().count()
    products_count=Product.objects.all().count()
    context={
        'workers':workers,
        'worker_count':worker_count,
        'order_count':order_count,
        'products_count':products_count,
    }
    return  render(request,'dashboard/staff.html',context)

@login_required
def staff_detail(request,pk):
    worker=User.objects.get(id=pk)
    context={
        'worker':worker,
    }
    return  render(request,'dashboard/staff_detail.html',context)

@login_required
def products(request):
    items=Product.objects.all()
    worker_count=User.objects.all().count()
    order_count=Order.objects.all().count()
    products_count=Product.objects.all().count()
    if request.method=="POST":
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name=form.cleaned_data.get('name')
            messages.success(request,f'{product_name} has been added')
            
            return redirect('dashboard-products')
    else:
        form=ProductForm()
    context={
        "items":items,
        'form':form,
        'worker_count':worker_count,
        'order_count':order_count,
        'products_count':products_count,
    }
    return  render(request,'dashboard/products.html',context)

@login_required
def product_delete(request,pk):
    item=Product.objects.get(id=pk)
    if request.method=="POST":
        item.delete()
        return redirect("dashboard-products")
    return  render(request,'dashboard/product_delete.html')

@login_required
def product_update(request,pk):
    item=Product.objects.get(id=pk)
    if request.method=="POST":
        form=ProductForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-products')
    else:
        form=ProductForm(instance=item)    
    context={
        'form':form,
    }
    return  render(request,'dashboard/product_update.html',context)

@login_required
def order(request):
    orders=Order.objects.all()
    worker_count=User.objects.all().count()
    order_count=Order.objects.all().count()
    products_count=Product.objects.all().count()
    context={
        "orders":orders,
        'worker_count':worker_count,
        'order_count':order_count,
        'products_count':products_count,
    }
    return  render(request,'dashboard/order.html',context)