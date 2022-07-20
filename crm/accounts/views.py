from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from .models import *
from .forms import OrderForm

def home(request):
    orders= Order.objects.all()
    customers= Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()


    context = {'orders':orders, 'customers': customers,
    'total_orders':total_orders, 'delivered':delivered, 
    'pending' : pending, 'total_customers':total_customers}
    return render(request,'accounts/dashboard.html', context)

def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders= customer.order_set.all()

    context ={'customer':customer,
    'orders':orders,
    }
    return render(request,'accounts/customer.html',context) 

def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra =7)
    customer=Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form= OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        # print('printing POST:',request.method)
        # form =OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset,}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    if request.method == 'POST':
        # print('printing POST:',request.method)
        form =OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form,'order':order }
    return render(request, 'accounts/order_form.html', context)

# Create your views here.

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        # print('printing POST:',request.method)
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)