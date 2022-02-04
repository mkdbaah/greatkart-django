from django.shortcuts import render, get_object_or_404
from . models import Product
from category.models import Category
from carts.models import CartItem

from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def store(request, category_slug=None):

  categories = None
  products = None

  if category_slug != None:
    categories = get_object_or_404(Category, slug = category_slug)
    products = Product.objects.filter(category=categories, is_available=True)
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()
  else:
    products = Product.objects.all().filter(is_available=True)
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()



  context = {
    'products': paged_products,
    'product_count': product_count,
  }

  return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
  try:
    single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    
  except Exception as e:
    raise e
  
  context = {
    'single_product': single_product,
    'in_cart'       : in_cart,
  }
  return render (request, 'store/product_detail.html', context)





### this is exactly where we render the store.html template and i am sure we can reach the database from this place (by importing the Products model here)
### you can pass the products into the template but when there are a lot of things you need to pass you can form it into a dictionary and pass it into the template in the render function call
### after adding to cart, we can change the button to be inactive and it will display (added to cart). I think this will be a good a good feature
### in the model you can set up a deleted price and even calculate a small percentage that will be shown in the frontend. Please do this as it will be very useful
### I think server side code and server side calculations can be done here

### we need to get the category of the Product (which is a foreign key in the product model) and we must also get the slug of the that Product's category
### so when we click on the product to go to the product details, we must get the product category, and we must also get the slug of that category
### underscore underscore is a synthax to get the slug of the category   category__slug 

## the double underscore(__) means that we will check the cart model, because the cart is a foreign key of the cartItem (which means that we are searching the cartItem with a foreign key)
## we will access the cart first, and with the cart (in the cartItem) we will access the cart id in the main cart model

### we went to where the product detail is and that is why we were able to see the true or false
### in_cart context is telling us whether that single product is a cart_item in the cart or not (true / false)

# 'page' is the page in the url when it comes to the pagination
### the 'paged_products' is now the number of products

## in the store function, the if statement is for when the is no slug and the else is for when the user will click on lets say shirts, jeans or anything else and it must filter according to the slug