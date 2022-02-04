from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from . models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _cart_id(request):
  cart = request.session.session_key
  if not cart:
    cart = request.session.create()
  
  return cart


def add_cart(request, product_id):
  product = Product.objects.get(id=product_id)

  try:
    cart = Cart.objects.get(cart_id=_cart_id(request))
  
  except Cart.DoesNotExist:
    cart = Cart.objects.create(
      cart_id = _cart_id(request)
    )
  cart.save()  ### this cart saving is for both the try and the exception

  try:
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.quantity += 1
    cart_item.save()

  except CartItem.DoesNotExist:
    cart_item = CartItem.objects.create(
      product = product,
      quantity = 1,
      cart = cart
    )
    cart_item.save()

  return redirect('cart')


## reduce the number on the cart items by 1 (one)
def remove_cart(request, product_id):
  cart = Cart.objects.get(cart_id=_cart_id(request))
  product = get_object_or_404(Product, id=product_id)
  cart_item = CartItem.objects.get(product=product, cart=cart)

  if cart_item.quantity > 1:
    cart_item.quantity -= 1
    cart_item.save()
  else:
    cart_item.delete()
  
  return redirect('cart')


def remove_cart_item(request, product_id):
  cart = Cart.objects.get(cart_id=_cart_id(request))
  product = get_object_or_404(Product, id=product_id)
  cart_item = CartItem.objects.get(product=product, cart=cart)
  cart_item.delete()
  return redirect('cart')

 

def cart(request, total=0, quantity=0, cart_items=None):
  try:
    tax = 0
    grand_total = 0
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)

    for cart_item in cart_items:
      total += (cart_item.product.price * cart_item.quantity)
      quantity += cart_item.quantity

    tax = 0.02 * total
    grand_total = total + tax
  
  except ObjectDoesNotExist:
    ## Just ignore
    pass 

  context = {
    'total': total,
    'quantity': quantity,
    'cart_items': cart_items,
    'tax': tax,
    'grand_total': grand_total
  }
  return render(request, 'store/cart.html', context)









### we will store the cart id in the database
### the cart id is the session id (but it is stored in the cookies and it says "3 in use")


### if you want to get all the data it is Product.objects.all()
### if you want to query some of the data it is Product.objects.get(id=product_id)
### the add to cart might be bound to the button
### product_id is got from the product we click on and we quickly use that one to get the corresponding product before going to the cart or addding it to the cart

## Just by starting the function name with an underscore it becomes a private function

## the private function _cart_id is just to extract the cart id (session id)

### get the cart using the cart id present in the session

### we can exit the page for now if we don't want to go to the cart page immediately


### {% url 'add_cart' cart_item.product.id %} 
# in the url s we have a add_cart and we are also passing in the proudct id corresponding to what we clicked
# this line in the front end is basically actuating that whole process again in this view file (which is a backend operation) // but the whole page was refreshing and i guess these are some of the reasons why we need react

### in the cart.html page the context passed into it is the cart or cart item but we can get the product from it (so this is working with both frontend and backend at the same time)