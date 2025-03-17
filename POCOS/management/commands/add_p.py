from django.core.management.base import BaseCommand
from django.db.models import Q
from POCOS.models import POCOS

class Command(BaseCommand):
    help = "Debug search functionality for POCOS."

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help="Search query to test")

    def handle(self, *args, **options):
        query = options['query'].strip()
        if not query:
            self.stdout.write(self.style.ERROR("❌ Query parameter is required."))
            return

        # Partial match search
        partial_results = POCOS.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

        if not partial_results.exists():
            self.stdout.write(self.style.WARNING(f"⚠️ No POCOS found with '{query}'."))
        else:
            self.stdout.write(self.style.SUCCESS(f"✅ Found {partial_results.count()} results."))
            for p in partial_results[:5]:  # Print first 5 results
                self.stdout.write(f"- {p.title}: {p.description}")
