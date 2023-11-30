from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
def user_login(request):
    return render(request, 'registration/login.html')

def authenticate_user(request):
    username = request.POST['username'] 
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponseRedirect(
            reverse('user_auth:login')
        )
    else:
        login(request, user)
        return HttpResponseRedirect(
            reverse('user_auth:show_user')
        )

def show_user(request):
    print(request.user.username)
    return render(request, 'registration/user.html', {
        "username": request.user.username,
        "password": request.user.password
    })


def signup(request):
    if request.method == 'POST':
        # Get user data from the POST request
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
      
        if User.objects.filter(username=username).exists(): 
            return HttpResponse("User already exists")
        
        user = User.objects.create_user(username=username, password=password)
        user.first_name = username
        user.save()
    return render(request, 'registration/login.html')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"