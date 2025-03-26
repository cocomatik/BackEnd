from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib import messages
from django.db import transaction
from POCOS.models import POCOS, Category as POCOSCategory
from POJOS.models import POJOS, Category as POJOSCategory
#from Accounts.decorators import session_auth_required
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity

#BEST_OF_Cosmetics
from POCOS.modelsxs import BestOfBodyCare,BestOfColorCosmetic,BestOfFragrance,BestOfHairCare,BestOfImportedProducts,BestOfSkinCare,BestSellers as BSC,FeatureProducts as FPC

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
        product = POCOS.objects.get(sku=product_id)
        categories = POCOSCategory.objects.all()
        product_type = "cosmetic"
    except POCOS.DoesNotExist:
        pass

    # If not found in POCOS, try finding in POJOS (Jewellery)
    if product is None:
        try:
            product = POJOS.objects.get(sku=product_id)  # Fixed: Use sku for POJOS
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
    product = POCOS.objects.filter(sku=product_id).first() or POJOS.objects.filter(sku=product_id).first()

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


    if  nm == "BestOfSkinCare":
        p = BestOfSkinCare.objects.get(id=1).pocos.all().order_by('title')
        z = POCOS.objects.filter(category= 'Skincare')
        q=z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

    elif  nm == "BestOfImportedProducts":
        p = BestOfImportedProducts.objects.get(id=1).pocos.all().order_by('title')
        z = POCOS.objects.filter(category= 'Imported Products')
        q=z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

    elif  nm == "BestOfHairCare":
        p = BestOfHairCare.objects.get(id=1).pocos.all().order_by('title')
        z = POCOS.objects.filter(category= 'Haircare')
        q=z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

    elif  nm == "BestOfFragrance":
        p = BestOfFragrance.objects.get(id=1).pocos.all().order_by('title')
        z = POCOS.objects.filter(category= 'Fragrances')
        q=z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

    elif  nm == "BestOfColorCosmetic":
        p = BestOfColorCosmetic.objects.get(id=1).pocos.all().order_by('title')
        z = POCOS.objects.filter(category= 'Color Cosmetics')
        q=z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

    elif  nm == "BestOfBodyCare":
        p = BestOfBodyCare.objects.get(id=1).pocos.all().order_by('title')
        z = POCOS.objects.filter(category= 'Bodycare')
        q=z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')




    elif  nm=="BestOfWeddingJewellery":
        p = BestOfWeddingJewellery.objects.get(id=1).pojos.all().order_by('title')
        z = POJOS.objects.filter(category= 'Wedding Jewellery')
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')


    elif  nm=="BestOfPendants":
        p = BestOfPendants.objects.get(id=1).pojos.all().order_by('title')
        z = POJOS.objects.filter(category= 'Pendants')
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')


    elif  nm=="BestOfNoseRings":
        p = BestOfNoseRings.objects.get(id=1).pojos.all().order_by('title')
        z = POJOS.objects.filter(category= 'Nose Rings')
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')


    elif  nm=="BestOfNecklace":
        p = BestOfNecklace.objects.get(id=1).pojos.all().order_by('title')
        z = POJOS.objects.filter(category= 'Necklace')
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')


    elif  nm=="BestOfOneGramGoldenJewellery":
        p = BestOfOneGramGoldenJewellery.objects.get(id=1).pojos.all().order_by('title')
        z = POJOS.objects.filter(category= 'One Gram Golden Jewellery')
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')


    elif  nm=="BestOfImportedJewellery":
        p = BestOfImportedJewellery.objects.get(id=1).pojos.all().order_by('title')
        z = POJOS.objects.filter(category= 'Imported Jewellery')
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')


    elif  nm=="BestOfFingerRings":
        p = BestOfFingerRings.objects.get(id=1).pojos.all().order_by('title')
        z = POJOS.objects.filter(category= 'Finger Rings')
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')


    elif  nm=="BestOfEarRings":
        p = BestOfEarRings.objects.get(id=1).pojos.all().order_by('title')
        z = POJOS.objects.filter(category= 'Ear Rings')
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')


    elif  nm=="BestOfChains":
        p = BestOfChains.objects.get(id=1).pojos.all().order_by('title')
        z = POJOS.objects.filter(category= 'Chains')
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')


    elif  nm=="BestOfBracelets":
        p = BestOfBracelets.objects.get(id=1).pojos.all().order_by('title')
        z = POJOS.objects.filter(category= 'Bracelets')
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')


    elif  nm=="BestOfBangles":
        p = BestOfBangles.objects.get(id=1).pojos.all().order_by('title')
        z = POJOS.objects.filter(category= 'Bangles')
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')




    elif tp=="POCOS" and nm=="BestSellers":
        p = BSC.objects.get(id=1).pocos.all().order_by('title')
        z = POCOS.objects.all()
        q=z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

    elif tp=="POCOS" and nm=="FeatureProducts":
        p = FPC.objects.get(id=1).pocos.all().order_by('title')
        z = POCOS.objects.all()
        q=z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

    elif tp=="POJOS" and nm=="BestSellers":
        p = BSJ.objects.get(id=1).pojos.all().order_by('title')
        z = POJOS.objects.all()
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')


    elif tp=="POJOS" and nm=="FeatureProducts":
        p = FPJ.objects.get(id=1).pojos.all().order_by('title')
        z = POJOS.objects.all()
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')




    context = {
    "prd": p,
    "tp":tp,
    "nm":nm,
    "qrd":q
    }
    return render(request, "Manager/product/best.html", context)

def dbop(request):
    #pid=product id
    pid = request.POST.get('pid')
    #tpn = product type(" POCOS/POJOS as string") 
    tpn = (request.POST.get('type'))
    #tp = search particular variables by tpn
    tp = globals().get(tpn)
    #nmn = bestOfCategories as a string
    nmn = (request.POST.get('name'))
    if nmn == 'BestSellers'  :
        if tp == POCOS:
            nm=BSC
        else:
            nm=BSJ
    elif nmn =='FeatureProducts' :
        if tp == POCOS:
            nm=FPC
        else:
            nm=FPJ
    else :
        nm=globals().get(nmn)
    pm = nm.objects.get(id=1)

    if tp == POCOS:
        pn = tp.objects.get(poco_id=pid)
        pm.pocos.remove(pn)
        p = pm.pocos.all().order_by('title')
        x = p.first().category if p.exists() else None
        if nm =='BestSellers' or nm == 'FeatureProducts':
            z=POCOS.objects.all()
        else:
            z = POCOS.objects.filter(category= f'{x}')
        q=z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')
    else :
        pn = tp.objects.get(pojo_id=pid)
        pm.pojos.remove(pn)
        p = pm.pojos.all().order_by('title')
        x = p.first().category if p.exists() else None
        if nm =='BestSellers' or nm == 'FeatureProducts':
            z=POJOS.objects.all()
        else:
            z = POJOS.objects.filter(category= f'{x}')
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')

    
    
    context = {'prd': p, 'tp': tpn, 'nm': nmn, 'qrd':q}
    return render(request, 'Manager/product/best.html', context)
    
def abop(request):
    lst = request.POST.getlist("selected_products")
    #tpn = product type(" POCOS/POJOS as string") 
    tpn = (request.POST.get('type'))
    #tp = search particular variables by tpn
    tp = globals().get(tpn)
    #nmn = bestOfCategories as a string
    nmn = (request.POST.get('name'))
    print(nmn == 'BestSellers')
    print(tp == POCOS)



    if nmn == 'BestSellers'  :
        if tp == POCOS:
            nm=BSC
        else:
            nm=BSJ
    elif nmn =='FeatureProducts' :
        if tp == POCOS:
            nm=FPC
        else:
            nm=FPJ
    
    else :
        nm=globals().get(nmn)
    pm = nm.objects.get(id=1)
    for s in lst:
        pn = tp.objects.get(sku=s)

    if tp == POCOS:
        for s in lst:
            
            pn = tp.objects.get(poco_id=s)
            pm.pocos.add(pn)
        p = pm.pocos.all().order_by('title')
        x = p.first().category if p.exists() else None
        if nm==BSC or nm==FPC:
            z = POCOS.objects.all()
        else:
            z = POCOS.objects.filter(category= f'{x}')
        
        q=z.exclude(poco_id__in=p.values_list('poco_id', flat=True)).order_by('title')        
    else :
        for s in lst:
                
            pn = tp.objects.get(pojo_id=s)
            pm.pojos.add(pn)
        p = pm.pojos.all().order_by('title')
        x = p.first().category if p.exists() else None
        if nm==BSJ or nm ==FPJ:
            z = POJOS.objects.all()
        else:
            z = POJOS.objects.filter(category= f'{x}')
        q=z.exclude(pojo_id__in=p.values_list('pojo_id', flat=True)).order_by('title')
    

    
    
    context = {'prd': p, 'tp': tpn, 'nm': nmn, 'qrd':q}
    return render(request, 'Manager/product/best.html', context)

    


from Orders.models import Order
#@session_auth_required

def orders(request):
    order_list = Order.objects.all()

    context ={
        'order_list':order_list
    }
    return render(request, "Manager/orders.html",context)

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


