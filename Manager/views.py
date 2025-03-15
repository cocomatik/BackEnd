from django.shortcuts import render, redirect
from django.contrib import messages
from POCOS.models import POCOS, Category

def dashboard(request):
    total_products = POCOS.objects.count()
    return render(request, "Manager/dashboard.html",{"total_products":total_products})

def products(request):
    product_list = POCOS.objects.all()
    categories = Category.objects.all()

    # Get selected category from GET request
    selected_category = request.GET.get('category')

    if selected_category:
        products = POCOS.objects.filter(category__name=selected_category)
    else:
        products = product_list

    context = {
        "products": products,
        "categories": categories,
    }
    return render(request, "Manager/products.html", context)

# Correct function names for different views
def add_product(request):
    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST.get("title", "")
        brand = request.POST.get("brand","")
        description = request.POST.get("description", "")
        price = request.POST.get("price", 0)
        stock = request.POST.get("stock", 0)
        category_id = request.POST.get("category")
        image = request.FILES.get("product_image")

        if category_id:
            category = Category.objects.get(id=category_id)
            POCOS.objects.create(
                title=title,
                description=description,
                price=price,
                stock=stock,
                category=category,
                display_image=image
            )
            messages.success(request, "Product added successfully!")
        else:
            messages.error(request, "Please select a valid category.")

        return redirect("products")
    
    categories = Category.objects.all()
    return render(request, "Manager/add_product.html", {"categories": categories})

def edit_product(request):
    return render(request, "Manager/edit_product.html")

def delete_product(request):
    return render(request, "Manager/delete_product.html")

def orders(request):
    return render(request, "Manager/orders.html")

def customers(request):
    return render(request, "Manager/customers.html")

def reports(request):
    return render(request, "Manager/reports.html")

def settings(request):
    return render(request, "Manager/settings.html")

def logout_view(request):
    return render(request, "Manager/login.html")
