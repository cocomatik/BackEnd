import random
import string
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from POCOS.models import POCOS, Category

class Command(BaseCommand):
    help = "Adds 50 sample products to the POCOS database"

    def generate_poco_id(self, length=15):
        """Generate a unique alphanumeric ID with special characters."""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(characters, k=length))

    def handle(self, *args, **kwargs):
        categories = list(Category.objects.all())

        if not categories:
            self.stdout.write(self.style.ERROR("❌ No categories found. Add categories first!"))
            return

        product_names = [
            "Moisturizing Face Cream", "Herbal Shampoo", "Vitamin C Serum", "Anti-Dandruff Shampoo",
            "Sunscreen SPF 50", "Aloe Vera Gel", "Charcoal Face Mask", "Body Lotion",
            "Lip Balm", "Face Wash", "Conditioner", "Hair Oil", "Perfume Spray", "Hand Cream",
            "Shaving Gel", "Body Scrub", "Face Toner", "Hair Wax", "Eye Cream", "Nail Polish",
            "Foot Cream", "BB Cream", "Hair Mousse", "Deodorant", "Night Cream",
            "Aftershave Lotion", "Hair Serum", "Cleansing Milk", "Makeup Remover", "Foundation",
            "Mascara", "Eyeliner", "Blush", "Concealer", "Lipstick", "Highlighter", "Bronzer",
            "Face Primer", "Makeup Setting Spray", "Beard Oil", "Hair Spray", "Eyebrow Pencil",
            "CC Cream", "Talcum Powder", "Soap Bar", "Shower Gel", "Toothpaste", "Mouthwash",
            "Scented Candle", "Hand Sanitizer"
        ]

        products = []
        for i in range(50):
            category = random.choice(categories)
            price = round(random.uniform(100, 2000), 2)
            mrp = round(price * random.uniform(1.1, 1.5), 2)
            stock = random.randint(10, 500)
            rating = round(random.uniform(3.0, 5.0), 1)

            product = POCOS(
                poco_id=self.generate_poco_id(),
                title=product_names[i % len(product_names)],
                description=f"This is a high-quality {product_names[i % len(product_names)]}.",
                price=price,
                mrp=mrp,
                stock=stock,
                category=category,
                brand=f"Brand-{random.randint(1, 10)}",
                size=f"{random.randint(50, 500)}g",
                rating=rating,
                created_at=now(),
                updated_at=now()
            )

            products.append(product)

        POCOS.objects.bulk_create(products)

        self.stdout.write(self.style.SUCCESS("✅ Successfully added 50 products!"))
