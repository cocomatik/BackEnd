from django.shortcuts import render
from POCOS.models import POCOS


def dashboard(request):
<<<<<<< HEAD
    return render(request, "manager/dashboard.html")

def products(request):
    product_list = POCOS.objects.select_related('category').all()
    return render(request, "manager/products.html", {"products": product_list})

def add_product(request):
    return render(request,"manager/add_product.html")

def orders(request):
    return render(request, "manager/orders.html")

def customers(request):
    return render(request, "manager/customers.html")

def reports(request):
    return render(request, "manager/reports.html")

def settings(request):
    return render(request, "manager/settings.html")

def logout_view(request):
    # Add logout logic here
    return render(request, "manager/login.html")
=======
    return render(request,"Manager/dashboard.html")
>>>>>>> 7a210bd4e80239b789493a5f440e0e430af87c7b
