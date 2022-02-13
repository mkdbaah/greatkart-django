from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime

from . models import Order
from carts.models import CartItem
from . forms import OrderForm

# Create your views here.


def payments(request):
  return render(request, 'orders/payments.html')


def place_order(request, total=0, quantity=0):
  current_user = request.user  ### because we know we are already logged in so the user is in the request object

  ### if the cart count is less than or equal to 0, then redirect to the store (continue shopping)
  cart_items = CartItem.objects.filter(user=current_user)
  cart_count = cart_items.count()

  if cart_count <= 0:
    return redirect('store')

  
  grand_total = 0
  tax  = 0
  for cart_item in cart_items:
    total +=  (cart_item.product.price * cart_item.quantity)
    quantity += cart_item.quantity
  
  tax = 0.02 * total
  grand_total = total + tax



  if request.method == 'POST':
    form = OrderForm(request.POST)
    if form.is_valid():
      ### if the form is valid, store all the billing information inside the order table
      data = Order()
      data.user              = current_user
      data.first_name        = form.cleaned_data['first_name']
      data.last_name         = form.cleaned_data['last_name']
      data.phone             = form.cleaned_data['phone']
      data.email             = form.cleaned_data['email']
      data.address_line_1    = form.cleaned_data['address_line_1']
      data.address_line_2    = form.cleaned_data['address_line_2']
      data.country           = form.cleaned_data['country']
      data.state             = form.cleaned_data['state']
      data.city              = form.cleaned_data['city']
      data.order_note        = form.cleaned_data['order_note']
      data.order_total       = grand_total
      data.tax               = tax
      data.ip                = request.META.get('REMOTE_ADDR')
      data.save()

      ### generate order number
      yr = int(datetime.date.today().strftime('%Y'))
      dt = int(datetime.date.today().strftime('%d'))
      mt = int(datetime.date.today().strftime('%m'))
      d  = datetime.date(yr, mt, dt)
      current_date = d.strftime("%Y%m%d") # 20220213   13th Feb 2022
      order_number = current_date + str(data.id)

      data.order_number      = order_number
      data.save()

      order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

      context = {
        'order': order,
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
      }

      return render(request, 'orders/payments.html', context)

  else:
    return redirect('checkout')
    
















### if we use filter means we can get more than one response, but if we use get means we are targeting only one response
### if you want your tax to be dynamic you can create a single model for your tax and give it one field on tax value, but for now we will set it to be static

### this is where we set the billing address and if you want to order for someone, set his name, billing address and pay for him / her or say (your loved ones)
