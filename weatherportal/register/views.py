from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def home(response):
    return render(response, "templates/home.html", {})


def registerPage(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Stworzono konto ' + user)
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form":form})

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, username)
            return redirect('')
        else:
            messages.info(request, 'Wprowadzono niespójne dane')

        context = {}
        return render(request, 'register.login.html', context)

