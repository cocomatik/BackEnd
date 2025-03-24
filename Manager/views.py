from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib import messages
from django.db import transaction
from POCOS.models import POCOS, Category as POCOSCategory
from POJOS.models import POJOS, Category as POJOSCategory
# from .decorators import session_admin_required
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity

#BEST_OF_Cosmetics
from POCOS.modelsxs import BestOfBodyCare,BestOfColorCosmetic,BestOfFragrance,BestOfHairCare,BestOfImportedProducts,BestOfSkinCare,BestSellers as BSC,FeatureProducts as Fp

#BEST_OF_Jewellery
from POJOS.modelsxs import BestOfBangles,BestOfBracelets,BestOfChains,BestOfEarRings,BestOfFingerRings,BestOfImportedJewellery,BestOfNecklace,BestOfNoseRings,BestOfOneGramGoldenJewellery,BestOfPendants,BestOfWeddingJewellery,BestSellers as BSJ,FeatureProducts as FPJ


def landing(request):
    return render(request,"landing/landing.html")

# @session_admin_required
def dashboard(request):
    total_cosmetic_products = POCOS.objects.count()
    total_jewellery_products = POJOS.objects.count()
    total_products = total_cosmetic_products + total_jewellery_products

    return render(request, "Manager/dashboard.html", {
        "total_products": total_products
    })

# @session_admin_required
def products(request):
    query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '')
    stock_filter = request.GET.get('stock', '')
    product_type = request.GET.get('type', '')

    # Determine product types to fetch
    fetch_cosmetic = product_type in ["", "cosmetic"]
    fetch_jewellery = product_type in ["", "jewellery"]

    # Fetch products
    cosmetic_products = POCOS.objects.all().order_by('title') if fetch_cosmetic else POCOS.objects.none()
    jewellery_products = POJOS.objects.all().order_by('title') if fetch_jewellery else POJOS.objects.none()

    # Fetch categories
    categories = list(POCOSCategory.objects.all()) if fetch_cosmetic else []
    categories += list(POJOSCategory.objects.all()) if fetch_jewellery else []

    # Apply search filter
    if query:
        search_filter = Q(title__icontains=query) | Q(description__icontains=query)
        if fetch_cosmetic:
            cosmetic_products = cosmetic_products.filter(search_filter)
        if fetch_jewellery:
            jewellery_products = jewellery_products.filter(search_filter)

    # Apply category filter
    if selected_category:
        if fetch_cosmetic:
            cosmetic_products = cosmetic_products.filter(category__name=selected_category)
        if fetch_jewellery:
            jewellery_products = jewellery_products.filter(category__name=selected_category)

    # Apply stock filter
    stock_filters = {
        "in-stock": lambda qs: qs.filter(stock__gt=0),
        "out-of-stock": lambda qs: qs.filter(stock=0),
        "low-stock-50": lambda qs: qs.filter(stock__lt=50),
        "low-stock-10": lambda qs: qs.filter(stock__lt=10),
    }

    if stock_filter in stock_filters:
        if fetch_cosmetic:
            cosmetic_products = stock_filters[stock_filter](cosmetic_products)
        if fetch_jewellery:
            jewellery_products = stock_filters[stock_filter](jewellery_products)

    # Reset query in context to clear search bar after submission
    query = ""

    context = {
        "cosmetic_products": cosmetic_products,
        "jewellery_products": jewellery_products,
        "categories": categories,
        "selected_category": selected_category,
        "selected_stock": stock_filter,
        "product_type": product_type,
        "query": query,  # Clears search box
    }

    return render(request, "Manager/product/product.html", context)




# @session_admin_required
def add_product(request):
    categories = []
    selected_type = request.GET.get("product_type", request.POST.get("product_type", ""))  # Remember selection

    if selected_type == "cosmetic":
        categories = POCOSCategory.objects.all()
    elif selected_type == "jewellery":
        categories = POJOSCategory.objects.all()

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        brand = request.POST.get("brand", "").strip()
        description = request.POST.get("description", "").strip()
        category_n = request.POST.get("category", "").strip()
        product_type = request.POST.get("product_type", "").strip()
        image = request.FILES.get("product_image")

        # Convert numeric values safely
        try:
            mrp = int(request.POST.get("mrp", 0))
            price = int(request.POST.get("price", 0))
            stock = int(request.POST.get("stock", 0))
        except ValueError:
            mrp, price, stock = 0, 0, 0  # Default values if conversion fails

        # Fetch category instance
        category = None
        if product_type == "cosmetic":
            category = POCOSCategory.objects.filter(name=category_n).first()
        elif product_type == "jewellery":
            category = POJOSCategory.objects.filter(name=category_n).first()

        if category:
            if product_type == "cosmetic":
                POCOS.objects.create(
                    title=title, 
                    brand=brand, 
                    description=description,
                    mrp=mrp, 
                    price=price, 
                    stock=stock,
                    category=category, 
                    display_image=image
                )
            elif product_type == "jewellery":
                POJOS.objects.create(
                    title=title, 
                    brand=brand, 
                    description=description,
                    mrp=mrp, 
                    price=price, 
                    stock=stock,
                    category=category, 
                    display_image=image
                )
                

            messages.success(request, "Product added successfully!")
            if product_type == "cosmetic":
                return redirect("/products/?type=cosmetic")
            elif product_type == "jewellery":
                return redirect("/products/?type=jewellery")

    return render(request, "Manager/product/add_product.html", {
        "categories": categories,
        "selected_type": selected_type
    })

# @session_admin_required
def edit_product(request, product_id):
    # Determine if the product is from POCOS (Cosmetics) or POJOS (Jewellery)
    product = None
    categories = []

    # Try finding in POCOS (Cosmetic)
    try:
        product = POCOS.objects.get(poco_id=product_id)
        categories = POCOSCategory.objects.all()
        product_type = "cosmetic"
    except POCOS.DoesNotExist:
        pass

    # If not found in POCOS, try finding in POJOS (Jewellery)
    if product is None:
        try:
            product = POJOS.objects.get(pojo_id=product_id)  # Fixed: Use pojo_id for POJOS
            categories = POJOSCategory.objects.all()
            product_type = "jewellery"
        except POJOS.DoesNotExist:
            messages.error(request, "Product not found!")
            return redirect("products")

    if request.method == "POST":
        product.title = request.POST.get("title", "").strip()
        product.brand = request.POST.get("brand", "").strip()
        product.description = request.POST.get("description", "").strip()
        product.price = request.POST.get("price", 0)
        product.stock = request.POST.get("stock", 0)

        # Get category (Fixed: Use 'name' instead of 'id')
        category_name = request.POST.get("category")
        if category_name:
            try:
                if product_type == "cosmetic":
                    product.category = POCOSCategory.objects.get(name=category_name)
                elif product_type == "jewellery":
                    product.category = POJOSCategory.objects.get(name=category_name)
            except (POCOSCategory.DoesNotExist, POJOSCategory.DoesNotExist):
                messages.error(request, "Invalid category selected!")

        # Update image if provided
        if "product_image" in request.FILES:
            product.display_image = request.FILES["product_image"]

        product.save()

        messages.success(request, "Product updated successfully!")
        return redirect(f"/products/?type={product_type}")

    return render(
        request,
        "Manager/product/edit_product.html",
        {"product": product, "categories": categories, "product_type": product_type},
    )



# @session_admin_required
def delete_product(request, product_id):
    # Check if the product exists in either POCOS or POJOS
    product = POCOS.objects.filter(poco_id=product_id).first() or POJOS.objects.filter(pojo_id=product_id).first()

    if not product:
        messages.error(request, "Product not found!")
        return redirect("dashboard")  # Redirect to dashboard if product doesn't exist

    product_type = "cosmetic" if isinstance(product, POCOS) else "jewellery"

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect(f"/products/?type={product_type}")

    return render(request, "Manager/product/delete_product.html", {"product": product, "product_type": product_type})



def bop(request):
    tp = request.POST.get('type')
    nm = request.POST.get('name')


    if tp=="POCOS" and nm == "BestOfSkinCare":
        p = BestOfSkinCare.objects.get(id=1).pocos.all().pocos.all()

    elif tp=="POCOS" and nm == "BestOfImportedProducts":
        p = BestOfImportedProducts.objects.get(id=1).pocos.all()

    elif tp=="POCOS" and nm == "BestOfHairCare":
        p = BestOfHairCare.objects.get(id=1).pocos.all()

    elif tp=="POCOS" and nm == "BestOfFragrance":
        p = BestOfFragrance.objects.get(id=1).pocos.all()

    elif tp=="POCOS" and nm == "BestOfColorCosmetic":
        p = BestOfColorCosmetic.objects.get(id=1).pocos.all()

    elif tp=="POCOS" and nm == "BestOfBodyCare":
        p = BestOfBodyCare.objects.get(id=1).pocos.all()


    elif tp=="POJOS" and nm=="BestOfWeddingJewellery":
        p = BestOfWeddingJewellery.objects.get(id=1).pojos.all()
    elif tp=="POJOS" and nm=="BestOfPendants":
        p = BestOfPendants.objects.get(id=1).pojos.all()
    elif tp=="POJOS" and nm=="BestOfNoseRings":
        p = BestOfNoseRings.objects.get(id=1).pojos.all()
    elif tp=="POJOS" and nm=="BestOfNecklace":
        p = BestOfNecklace.objects.get(id=1).pojos.all()
    elif tp=="POJOS" and nm=="BestOfOneGramGoldenJewellery":
        p = BestOfOneGramGoldenJewellery.objects.get(id=1).pojos.all()
    elif tp=="POJOS" and nm=="BestOfImportedJewellery":
        p = BestOfImportedJewellery.objects.get(id=1).pojos.all()
    elif tp=="POJOS" and nm=="BestOfFingerRings":
        p = BestOfFingerRings.objects.get(id=1).pojos.all()
    elif tp=="POJOS" and nm=="BestOfEarRings":
        p = BestOfEarRings.objects.get(id=1).pojos.all()
    elif tp=="POJOS" and nm=="BestOfChains":
        p = BestOfChains.objects.get(id=1).pojos.all()
    elif tp=="POJOS" and nm=="BestOfBracelets":
        p = BestOfBracelets.objects.get(id=1).pojos.all()
    elif tp=="POJOS" and nm=="BestOfBangles":
        p = BestOfBangles.objects.get(id=1).pojos.all()


    elif tp=="POCOS" and nm=="BestSellers":
        p = BSC.objects.get(id=1).pocos.all()
    elif tp=="POCOS" and nm=="FeatureProducts":
        p = Fp.objects.get(id=1).pocos.all()
    elif tp=="POJOS" and nm=="BestSellers":
        p = BSJ.objects.get(id=1).pojos.all()
    elif tp=="POJOS" and nm=="FeatureProducts":
        p = FPJ.objects.get(id=1).pojos.all()


    context = {
    "prd": p
    }
    return render(request, "Manager/product/best.html", context)

def dbop(request):
    pid = request.POST.get('pid')
    return redirect('best_of_products')



#@session_auth_required

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



def best_of_products(request):
    
    return render(request,"Manager/product/best_of_products.html",)


# def update_best_of_category(request):
#     if request.method == "POST":
#         best_of_cosmetics = request.POST.getlist("best_of_cosmetic")
#         best_of_jewellery = request.POST.getlist("best_of_jewellery")

#         try:
#             with transaction.atomic():  # Ensures atomic updates

#                 # Update Cosmetics
#                 all_cosmetics = POCOS.objects.all()
#                 cosmetics_to_update = []
#                 for product in all_cosmetics:
#                     is_best = str(product.id) in best_of_cosmetics
#                     if product.is_best_of != is_best:
#                         product.is_best_of = is_best
#                         cosmetics_to_update.append(product)

#                 if cosmetics_to_update:
#                     POCOS.objects.bulk_update(cosmetics_to_update, ["is_best_of"])

#                 # Update Jewellery
#                 all_jewellery = POJOS.objects.all()
#                 jewellery_to_update = []
#                 for product in all_jewellery:
#                     is_best = str(product.id) in best_of_jewellery
#                     if product.is_best_of != is_best:
#                         product.is_best_of = is_best
#                         jewellery_to_update.append(product)

#                 if jewellery_to_update:
#                     POJOS.objects.bulk_update(jewellery_to_update, ["is_best_of"])

#             return JsonResponse({"status": "success", "message": "Best of Products updated successfully!"})

#         except Exception as e:
#             return JsonResponse({"status": "error", "message": f"Error: {str(e)}"})

#     return JsonResponse({"status": "error", "message": "Invalid request method."})

