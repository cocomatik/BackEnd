from django.shortcuts import render
from POCOS.models import POCOS,Category


def dashboard(request):
    return render(request, "Manager/dashboard.html")

def products(request):
    product_list = POCOS.objects.all()
    categories = Category.objects.all()
    try:
        selected_category = request.GET.get('category')
        if selected_category:
            products = POCOS.filter(category=selected_category)
        context = {
            "products": products,
            "categories": categories,
        }
        return render(request, "Manager/products.html", context)
    except:
        return render(request,"Manager/products.html", {
            "products": product_list,
            "categories": categories,
        })
    

def add_product(request):
    return render(request,"Manager/add_product.html")
def add_product(request):
    return render(request,"Manager/edit_product.html")
def add_product(request):
    return render(request,"Manager/delete_product.html")

def orders(request):
    return render(request, "Manager/orders.html")
    

# def customers(request):
#     return render(request, "manager/customers.html")

# def reports(request):
#     return render(request, "manager/reports.html")

# def settings(request):
#     return render(request, "manager/settings.html")

# def logout_view(request):
#     # Add logout logic here
#     return render(request, "manager/login.html")
#     return render(request,"Manager/dashboard.html")

