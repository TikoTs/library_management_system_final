# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Account created successfully. You can now log in."
            )
    else:
        form = CustomUserCreationForm()
    return render(request, "authentication/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page, or in this case, the homepage
                return redirect("home")
            else:
                messages.error(request, "Invalid email or password. Please try again.")
    else:
        form = LoginForm()
    return render(request, "authentication/login.html", {"form": form})


def home(request):
    return render(request, "home.html")
