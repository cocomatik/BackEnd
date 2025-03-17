from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from POCOS.models import POCOS, Category
from Accounts.decorators import session_auth_required

def landing(request):
    return render(request,"landing/landing.html")

@session_auth_required
def dashboard(request):
    total_products = POCOS.objects.count()
    return render(request, "Manager/dashboard.html",{"total_products":total_products})

@session_auth_required
def products(request):
    product_list = POCOS.objects.all()
    categories = Category.objects.all()

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
@session_auth_required
def add_product(request):

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
                brand = brand,
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
@session_auth_required
def edit_product(request, product_id):
    product = get_object_or_404(POCOS, poco_id=product_id)
    categories = Category.objects.all()

    if request.method == "POST":
        product.title = request.POST.get("title", "")
        product.brand = request.POST.get("brand", "")
        product.description = request.POST.get("description", "")
        product.price = request.POST.get("price", 0)
        product.stock = request.POST.get("stock", 0)

        category_id = request.POST.get("category")
        if category_id:
            product.category = Category.objects.get(id=category_id)

        if "product_image" in request.FILES:
            product.display_image = request.FILES["product_image"]

        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect("products")

    return render(request, "Manager/edit_product.html", {"product": product, "categories": categories})

@session_auth_required
def delete_product(request, product_id):
    product = get_object_or_404(POCOS, poco_id=product_id)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("products")

    return render(request, "Manager/delete_product.html", {"products":products})

@session_auth_required
def orders(request):
    return render(request, "Manager/orders.html")

@session_auth_required
def customers(request):
    return render(request, "Manager/customers.html")

@session_auth_required
def reports(request):
    return render(request, "Manager/reports.html")

@session_auth_required
def settings(request):
    return render(request, "Manager/settings.html")

@session_auth_required
def logout_view(request):
    return render(request, "Manager/login.html")
