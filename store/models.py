from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.

### in the store app is where we are doing our product model (hmmm)

class Product(models.Model):
  product_name = models.CharField(max_length=200, unique=True)
  slug = models.SlugField(max_length=200, unique=True)
  description = models.TextField(max_length=500, blank=True)
  price = models.IntegerField()
  images = models.ImageField(upload_to='photos/products')
  stock = models.IntegerField()
  is_available = models.BooleanField(default=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)


  def get_url(self):
    return reverse('product_detail', args=[self.category.slug, self.slug])

  def __str__(self):
    return self.product_name






### in the vs code file explorer, we will see the images for the products and categories in media photos categories and even in the products folder and so that is where all our uploads went
### we will this render this url in the home.html(you know) to much. So we are just uploading on the server and maybe we will go to the S3 instance or what i don't know 
### to get a store page we must first set up a store url
### this model file can talk to the database without any ORM (wow!) "sweet" and this is the model for the database too and very organised

### this really shows that the slug s are all coming from the url becasue the special name given to the url is what we pass first

### the product objects that will be passed as a context to template, now has the get_url function at it's disposal and it returns the url or slug of the object


### if you want to go to home page or store page then it is ( url 'store' or url 'home' )
### if it deserves some slugs, the you can use the get_url feature that will be defined in the model

### is_available is different from the product going out of stock
