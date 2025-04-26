from django.core.management.base import BaseCommand
from POCOS.models import POCOS
from POJOS.models import POJOS

class Command(BaseCommand):
    help = "Check which products (POCOS/POJOS) are missing an SKU."

    def handle(self, *args, **kwargs):
        pocos_without_sku = POCOS.objects.filter(sku__isnull=True) | POCOS.objects.filter(sku="")
        pojos_without_sku = POJOS.objects.filter(sku__isnull=True) | POJOS.objects.filter(sku="")
        total_missing = pocos_without_sku.count() + pojos_without_sku.count()

        if total_missing == 0:
            self.stdout.write(self.style.SUCCESS("✅ All products have an SKU."))
        
        else:
            self.stdout.write(self.style.WARNING(f"⚠️ {total_missing} products are missing an SKU:"))

            if pocos_without_sku.exists():
                self.stdout.write(self.style.WARNING("\n🔹 Missing SKUs in POCOS:"))
                for product in pocos_without_sku:
                    self.stdout.write(f"   - {product.title} (ID: {product.id})")

            if pojos_without_sku.exists():
                self.stdout.write(self.style.WARNING("\n🔹 Missing SKUs in POJOS:"))
                for product in pojos_without_sku:
                    self.stdout.write(f"   - {product.title} (ID: {product.id})")

        self.stdout.write(self.style.SUCCESS("✅ Check completed!"))
