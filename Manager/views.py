from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib import messages
from django.db import transaction
from POCOS.models import POCOS, Category as POCOSCategory,PocoImage
from POJOS.models import POJOS, Category as POJOSCategory,PojoImage
from Accounts.decorators import session_auth_required
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity

from Orders.models import Order,CartItem,Address,OrderHistoryItem
#BEST_OF_Cosmetics
from POCOS.modelsxs import BestOfBodyCare,BestOfColorCosmetic,BestOfFragrance,BestOfHairCare,BestOfImportedProducts,BestOfSkinCare,BestSellers as BSC,FeatureProducts as FPC

#BEST_OF_Jewellery
from POJOS.modelsxs import BestOfBangles,BestOfBracelets,BestOfChains,BestOfEarRings,BestOfFingerRings,BestOfImportedJewellery,BestOfNecklace,BestOfNoseRings,BestOfOneGramGoldenJewellery,BestOfPendants,BestOfWeddingJewellery,BestSellers as BSJ,FeatureProducts as FPJ

from Orders.models import Order,OrderHistory

def landing(request):
    return render(request,"landing/landing.html")

@session_auth_required
def dashboard(request):
    total_cosmetic_products = POCOS.objects.count()
    total_jewellery_products = POJOS.objects.count()
    total_products = total_cosmetic_products + total_jewellery_products
    total_orders = OrderHistory.objects.count()
    total_customers = UserAccount.objects.count()
    orders=OrderHistory.objects.all()
    value=0
    for order in orders:
        value += order.total_price

    context = {
        "total_products": total_products,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'value':value
    }
    

    return render(request, "Manager/dashboard.html", context)

@session_auth_required
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




@session_auth_required
def add_product(request):
    categories = []
    selected_type = request.GET.get("product_type", request.POST.get("product_type", ""))

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

        # Convert numeric fields safely
        try:
            mrp = int(request.POST.get("mrp", 0))
            price = int(request.POST.get("price", 0))
            stock = int(request.POST.get("stock", 0))
            rating = float(request.POST.get("rating", 0))
        except ValueError:
            mrp, price, stock, rating = 0, 0, 0, 0.0

        size = request.POST.get("size", "").strip()
        display_image = request.FILES.get("product_image")
        extra_images = request.FILES.getlist("extra_images")

        # Fetch category instance
        category = None
        if product_type == "cosmetic":
            category = POCOSCategory.objects.filter(name=category_n).first()
        elif product_type == "jewellery":
            category = POJOSCategory.objects.filter(name=category_n).first()

        if category:
            if product_type == "cosmetic":
                poco = POCOS.objects.create(
                    title=title,
                    brand=brand,
                    description=description,
                    mrp=mrp,
                    price=price,
                    stock=stock,
                    size=size,
                    rating=rating,
                    category=category,
                    display_image=display_image,
                )

                # Handle extra images for POCOS
                for extra_image in extra_images:
                    PocoImage.objects.create(
                        poco=poco,  # Correct: use the actual POCOS instance
                        image=extra_image,
                    )

            elif product_type == "jewellery":
                pojo = POJOS.objects.create(
                    title=title,
                    brand=brand,
                    description=description,
                    mrp=mrp,
                    price=price,
                    stock=stock,
                    size=size,
                    rating=rating,
                    category=category,
                    display_image=display_image,
                )

                # Handle extra images for POJOS
                for extra_image in extra_images:
                    PojoImage.objects.create(
                        pojo=pojo,  # Correct: use the actual POJOS instance
                        image=extra_image,
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


@session_auth_required
def edit_product(request, product_id):
    product = None
    categories = []
    extra_images = []
    product_type = None

    try:
        product = POCOS.objects.get(sku=product_id)
        categories = POCOSCategory.objects.all()
        product_type = "cosmetic"
    except POCOS.DoesNotExist:
        try:
            product = POJOS.objects.get(sku=product_id)
            categories = POJOSCategory.objects.all()
            product_type = "jewellery"
        except POJOS.DoesNotExist:
            messages.error(request, "Product not found!")
            return redirect("products")

    if product_type == "cosmetic":
        extra_images = PocoImage.objects.filter(poco=product)
    elif product_type == "jewellery":
        extra_images = PojoImage.objects.filter(pojo=product)

    if request.method == "POST":
        product.title = request.POST.get("title", "").strip()
        product.brand = request.POST.get("brand", "").strip()
        product.description = request.POST.get("description", "").strip()
        product.mrp = request.POST.get("mrp", 0)
        product.price = request.POST.get("price", 0)
        product.stock = request.POST.get("stock", 0)
        product.size = request.POST.get("size", "").strip()
        product.rating = request.POST.get("rating", 0)

        category_name = request.POST.get("category")
        try:
            if product_type == "cosmetic":
                product.category = POCOSCategory.objects.get(name=category_name)
            else:
                product.category = POJOSCategory.objects.get(name=category_name)
        except (POCOSCategory.DoesNotExist, POJOSCategory.DoesNotExist):
            messages.error(request, "Invalid category selected!")

        if "product_image" in request.FILES:
            product.display_image = request.FILES["product_image"]

        product.save()

        if "extra_images" in request.FILES:
            new_images = request.FILES.getlist("extra_images")

            if product_type == "cosmetic":
                # Just remove old DB references
                PocoImage.objects.filter(poco=product).delete()
                for img in new_images:
                    PocoImage.objects.create(poco=product, image=img)

            elif product_type == "jewellery":
                PojoImage.objects.filter(pojo=product).delete()
                for img in new_images:
                    PojoImage.objects.create(pojo=product, image=img)

        messages.success(request, "Product updated successfully!")
        return redirect(f"/products/?type={product_type}")

    return render(
        request,
        "Manager/product/edit_product.html",
        {
            "product": product,
            "categories": categories,
            "product_type": product_type,
            "extra_images": extra_images,
        }
    )






@session_auth_required
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

@session_auth_required
def best_of_products(request):
    return render(request,"Manager/product/best_of_products.html",)

@session_auth_required
def bop(request):
    tp = request.POST.get('type')
    nm = request.POST.get('name')

    try:
        if nm == "BestOfSkinCare":
            p_obj, _ = BestOfSkinCare.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POCOS.objects.filter(category='Skincare')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfImportedProducts":
            p_obj, _ = BestOfImportedProducts.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POCOS.objects.filter(category='Imported Products')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfHairCare":
            p_obj, _ = BestOfHairCare.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POCOS.objects.filter(category='Haircare')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfFragrance":
            p_obj, _ = BestOfFragrance.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POCOS.objects.filter(category='Fragrances')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfColorCosmetic":
            p_obj, _ = BestOfColorCosmetic.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POCOS.objects.filter(category='Color Cosmetics')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfBodyCare":
            p_obj, _ = BestOfBodyCare.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POCOS.objects.filter(category='Bodycare')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfWeddingJewellery":
            p_obj, _ = BestOfWeddingJewellery.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POJOS.objects.filter(category='Wedding Jewellery')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfPendants":
            p_obj, _ = BestOfPendants.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POJOS.objects.filter(category='Pendants')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfNoseRings":
            p_obj, _ = BestOfNoseRings.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POJOS.objects.filter(category='Nose Rings')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfNecklace":
            p_obj, _ = BestOfNecklace.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POJOS.objects.filter(category='Necklace')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfOneGramGoldenJewellery":
            p_obj, _ = BestOfOneGramGoldenJewellery.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POJOS.objects.filter(category='One Gram Golden Jewellery')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfImportedJewellery":
            p_obj, _ = BestOfImportedJewellery.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POJOS.objects.filter(category='Imported Jewellery')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfFingerRings":
            p_obj, _ = BestOfFingerRings.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POJOS.objects.filter(category='Finger Rings')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfEarRings":
            p_obj, _ = BestOfEarRings.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POJOS.objects.filter(category='Ear Rings')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfChains":
            p_obj, _ = BestOfChains.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POJOS.objects.filter(category='Chains')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfBracelets":
            p_obj, _ = BestOfBracelets.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POJOS.objects.filter(category='Bracelets')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif nm == "BestOfBangles":
            p_obj, _ = BestOfBangles.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POJOS.objects.filter(category='Bangles')
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif tp == "POCOS" and nm == "BestSellers":
            p_obj, _ = BSC.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POCOS.objects.all()
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif tp == "POCOS" and nm == "FeatureProducts":
            p_obj, _ = FPC.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POCOS.objects.all()
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif tp == "POJOS" and nm == "BestSellers":
            p_obj, _ = BSJ.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POJOS.objects.all()
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        elif tp == "POJOS" and nm == "FeatureProducts":
            p_obj, _ = FPJ.objects.get_or_create(id=1)
            p = p_obj.objs.all().order_by('title')
            z = POJOS.objects.all()
            q = z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title')

        context = {
            "prd": p,
            "tp": tp,
            "nm": nm,
            "qrd": q
        }
        return render(request, "Manager/product/best.html", context)
    except:
        return render(request, "Manager/product/best.html")



@session_auth_required
def mbop(request):
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
    pm.objs.clear()
    for s in lst:
        pn = tp.objects.get(sku=s)
        try:
            pm.objs.add(pn)
        except :
            pass
    p = pm.objs.all().order_by('title')
    x = p.first().category if p.exists() else None
    if nm==BSC or nm==FPC:
        z = tp.objects.all()
    else:
        z = tp.objects.filter(category= f'{x}')
            
    q=z.exclude(sku__in=p.values_list('sku', flat=True)).order_by('title') 
    
    context = {'prd': p, 'tp': tpn, 'nm': nmn, 'qrd':q}
    return redirect("best_of_products")


@session_auth_required
def orders(request):
    order_list = OrderHistory.objects.all().order_by('-created_at')

    return render(request, "Manager/order/orders.html", {"order_list": order_list})


@session_auth_required
def order_detail(request, order_number):
    order = get_object_or_404(OrderHistory, order_number=order_number)
    return render(request, 'Manager/order/order_detail.html', {'order': order})




@session_auth_required
def shipment_form(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'Manager/shipment/ship.html',{'order':order})



from Delivery.models import ShiprocketOrder

@session_auth_required
def shipment_details(request):
    shipments = ShiprocketOrder.objects.all().order_by('-created_at')

    return render(request, 'Manager/shipment/shipment_details.html', {'shipments': shipments})




from Accounts.models import UserAccount
@session_auth_required
def customers(request):
    customer_list = UserAccount.objects.all()
    return render(request, "Manager/customer/customer.html",{'customer_list':customer_list})

@session_auth_required
def customer_details(request, customer_id):
    customer = get_object_or_404(UserAccount, id=customer_id)  # Fetch customer by ID
    orders = Order.objects.filter(user=customer)  # Fetch orders of this customer
    address = Address.objects.filter(user=customer).first()  # Get the first address or None
    

    context = {
        'customer': customer,
        'orders': orders,
        'address': address  # Pass the single address
    }
    
    return render(request, 'Manager/customer/customer_details.html', context)




from django.db.models import Sum, F, DecimalField, Count
from django.db.models.functions import TruncMonth
from Orders.models import OrderHistory, OrderHistoryItem
from django.shortcuts import render

@session_auth_required
def revenue_report(request):
    # Filter orders with relevant statuses
    queryset = OrderHistory.objects.filter(status__in=["DELIVERED", "SHIPPED", "PROCESSING"])

    # Monthly revenue aggregation
    monthly_revenues = (
        queryset
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(monthly_total=Sum('total_price'), total_orders=Count('id'))  # Added total_orders per month
        .annotate(avg_order_value=F('monthly_total') / F('total_orders'))  # Calculated AOV directly
        .order_by('month')
    )

    # Revenue growth rate: Compare current and previous month
    monthly_list = list(monthly_revenues)
    growth_rate = 0.0

    if len(monthly_list) >= 2:
        previous = monthly_list[-2]['monthly_total'] or 0
        current = monthly_list[-1]['monthly_total'] or 0
        if previous > 0:
            growth_rate = ((current - previous) / previous) * 100

    # General stats
    total_revenue = queryset.aggregate(total=Sum('total_price'))['total'] or 0
    total_orders = queryset.count()
    avg_monthly_revenue = total_revenue / len(monthly_list) if monthly_list else 0
    avg_order_value = total_revenue / total_orders if total_orders else 0

    # Top 10 products by revenue
    top_products = (
        OrderHistoryItem.objects
        .values('title', 'product_type__model')
        .annotate(
            total_revenue=Sum(F('selling_price') * F('quantity'), output_field=DecimalField()),
            total_units_sold=Sum('quantity')
        )
        .order_by('-total_revenue')[:10]
    )

    return render(request, 'Manager/reports/revenue_report.html', {
        'revenues': monthly_list,
        'total_revenue': total_revenue,
        'avg_monthly_revenue': avg_monthly_revenue,
        'avg_order_value': avg_order_value,
        'growth_rate': round(growth_rate, 2),
        'top_products': top_products,
    })
