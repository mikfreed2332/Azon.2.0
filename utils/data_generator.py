import random
import uuid

from faker import Faker

fake = Faker("en_US")


class DataGenerator:

    @staticmethod
    def generate_email():
        return f"student-{uuid.uuid4().hex[:8]}@example.com"

    @staticmethod
    def generate_password():
        return fake.password(length=12)

    @staticmethod
    def generate_full_name():
        return fake.name()

    @staticmethod
    def generate_product_data(category_id) -> dict:
        return {
            "name": f"Test Product {DataGenerator.generate_full_name()}",
            "description": f"Description for {DataGenerator.generate_full_name()}",
            "sku": f"SKU-{uuid.uuid4().hex[:8]}",
            "price": round(random.uniform(100, 5000), 2),
            "stock": random.randint(1, 100),
            "category_id": category_id
        }
