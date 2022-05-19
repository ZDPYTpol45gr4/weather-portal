from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
def home(response):
    return render(response, "register/home.html", {})


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = RegisterForm()
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Stworzono Twoje nowe konto, możesz się zalogować ' + user)

                return redirect('login')

        return render(request, 'register/register.html', {'form':form})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Wprowadzono niespójne dane')

        return render(request, 'register/login.html', {})

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')