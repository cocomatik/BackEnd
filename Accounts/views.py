from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def user_login(request):
    if request.user.is_authenticated:
        return redirect("/dashboard/")  

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect("/dashboard/")  
        else:
            messages.error(request, "Invalid credentials!")

    return render(request, "Accounts/Admin/login.html")  

def user_logout(request):
    logout(request)
    return redirect("/accounts/login/")  
