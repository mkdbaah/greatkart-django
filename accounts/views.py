from django.shortcuts import render, redirect
from . forms import RegistrationForm
from . models import Account
from django.contrib import messages

# Create your views here.

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      phone_number = form.cleaned_data['phone_number']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      username = email.split('@')[0]

      user =  Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username)

      user.phone_number = phone_number
      user.save()
      messages.success(request, 'Registration Successful')
      return redirect('register')

  else:
    form = RegistrationForm()

  context = {
    'form': form,
  }
  return render(request, 'accounts/register.html', context)
  
def login(request):
  return render(request, 'accounts/login.html')

def logout(request):
  return 

























## we will use django model forms to replicate the data in the model
## request.POST will contain all the field values
## in the accounts model file, we have the create_user and create_superuser functions and we are leveraging it
## in the else case means it is just a GET request and hence it should render just the form
## if you get to the page first, it is a get request and the registration form will render and it you submit the form it will parse it to the request.POST and it will create a user in the views(controller) and a pre defined model function

## in the installed apps we have django messages and it is the default one installed in django for us to use
