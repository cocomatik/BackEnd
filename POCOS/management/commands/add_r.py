import random
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from POCOS.models import POCOS, Review

class Command(BaseCommand):
    help = "Adds 100 random reviews to existing products"

    def handle(self, *args, **kwargs):
        products = list(POCOS.objects.all())

        if not products:
            self.stdout.write(self.style.ERROR("❌ No products found. Add products first!"))
            return

        user_names = [
            "Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry", "Ivy", "Jack",
            "Katherine", "Leo", "Mia", "Noah", "Olivia", "Peter", "Quinn", "Rachel", "Sam", "Tina",
            "Umar", "Violet", "William", "Xavier", "Yasmin", "Zach"
        ]

        review_comments = [
            "Amazing product! Highly recommend it.", "Not bad, but could be better.", 
            "Good quality for the price.", "Exceeded my expectations!", "Will buy again!",
            "The packaging was great!", "Fast delivery, loved it!", "Not worth the price.",
            "Smells fantastic!", "Really helped my skin feel fresh.", "Best product I have used!",
            "Could improve the texture.", "Too expensive for what it offers.", 
            "Definitely a must-have.", "Very happy with this purchase!", "Would give 10 stars if I could!",
            "Nice fragrance but doesn't last long.", "Great value for money.", 
            "Super smooth and effective.", "Feels really premium!"
        ]

        reviews = []
        for _ in range(100):
            poco = random.choice(products)
            user_name = random.choice(user_names)
            rating = round(random.uniform(3.0, 5.0), 1)
            comment = random.choice(review_comments)
            verified_user = random.choice([True, False])

            review = Review(
                poco=poco,
                user_name=user_name,
                rating=rating,
                comment=comment,
                verified_user=verified_user,
                created_at=now()
            )

            reviews.append(review)

        Review.objects.bulk_create(reviews)

        self.stdout.write(self.style.SUCCESS("✅ Successfully added 100 random reviews!"))
