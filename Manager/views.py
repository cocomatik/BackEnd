from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from POCOS.models import POCOS, Category
# from .decorators import session_admin_required
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity


def landing(request):
    return render(request,"landing/landing.html")

# @session_admin_required
def dashboard(request):
    total_products = POCOS.objects.count()
    return render(request, "Manager/dashboard.html",{"total_products":total_products})

# @session_admin_required
def products(request):
    query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '')
    stock_filter = request.GET.get('stock', '')

    # Fetch all products
    product_list = POCOS.objects.all().order_by('title')
    categories = Category.objects.all()

    # Apply search filter
    if query:
        product_list = product_list.annotate(
            search=SearchVector('title', 'description')
        ).filter(Q(search=SearchQuery(query)) | Q(title__icontains=query) | Q(description__icontains=query))

    # Apply category filter
    if selected_category:
        product_list = product_list.filter(category__name=selected_category)

    # Apply stock filter
    if stock_filter == "in-stock":
        product_list = product_list.filter(stock__gt=0)
    elif stock_filter == "out-of-stock":
        product_list = product_list.filter(stock=0)
    elif stock_filter == "low-stock-50":
        product_list = product_list.filter(stock__lt=50)
    elif stock_filter == "low-stock-10":
        product_list = product_list.filter(stock__lt=10)

    # Reset only the search query after filtering
    query = ""

    context = {
        "products": product_list,
        "categories": categories,
        "selected_category": selected_category,
        "selected_stock": stock_filter,
        "query": query  # This clears the search bar but keeps filters
    }
    return render(request, "Manager/products.html", context)



# @session_admin_required
def add_product(request):

    if request.method == "POST":
        title = request.POST.get("title", "")
        brand = request.POST.get("brand","")
        description = request.POST.get("description", "")
        mrp = request.POST.get("mrp",0)
        price = request.POST.get("price", 0)
        stock = request.POST.get("stock", 0)
        category_n = request.POST.get("category")
        image = request.FILES.get("product_image")

        if category_n:
            category = Category.objects.get(name=category_n)
            POCOS.objects.create(
                title=title,
                brand = brand,
                description=description,
                mrp=mrp,
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

# @session_admin_required
def edit_product(request, product_id):
    product = get_object_or_404(POCOS, poco_id=product_id)
    categories = Category.objects.all()

    if request.method == "POST":
        product.title = request.POST.get("title", "")
        product.brand = request.POST.get("brand", "")
        product.description = request.POST.get("description", "")
        product.price = request.POST.get("price", 0)
        product.stock = request.POST.get("stock", 0)

        # Get category (Fixed: Use 'name' instead of 'id')
        category_name = request.POST.get("category")
        if category_name:
            product.category = Category.objects.get(name=category_name)

        # Update image if provided
        if "product_image" in request.FILES:
            product.display_image = request.FILES["product_image"]

        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect("products")

    return render(request, "Manager/edit_product.html", {"product": product, "categories": categories})


# @session_admin_required
def delete_product(request, product_id):
    product = get_object_or_404(POCOS, poco_id=product_id)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("products")

    return render(request, "Manager/delete_product.html", {"product": product})

# @session_admin_required
def orders(request):
    return render(request, "Manager/orders.html")

# @session_admin_required
def customers(request):
    return render(request, "Manager/customers.html")

# @session_admin_required
def reports(request):
    return render(request, "Manager/reports.html")

# @session_admin_required
def settings(request):
    return render(request, "Manager/settings.html")

# @session_admin_required
def logout_view(request):
    return render(request, "Manager/login.html")
