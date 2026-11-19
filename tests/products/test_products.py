from decimal import Decimal
from utils.data_generator import DataGenerator


class TestProducts:

    def test_get_products_returns_paginated_catalog(self, api_manager):
        response = api_manager.products_api.get_products()

        data = response.json()
        assert data["total"] > 0
        assert len(data["items"]) <= data["size"]

    def test_products_price_filter(self, api_manager):
        response = api_manager.products_api.get_products(
            params={"price_min": 5000, "size": 100}
        )

        products = response.json()["items"]
        assert products, "Ожидали хотя бы один товар дороже 5000"
        for product in products:
            assert Decimal(product["price"]) >= 5000

    def test_get_product_by_id(self, api_manager):
        products = api_manager.products_api.get_products().json()["items"]
        product_id = products[0]["id"]

        response = api_manager.products_api.get_product(product_id)
        assert response.json()["id"] == product_id

    def test_create_product(self, api_manager, authenticated_manager, registered_admin):
        categories_list = api_manager.categories_api.get_categories().json()
        category_id = categories_list[0]["id"]
        new_product = DataGenerator.generate_product_data(category_id)

        created = None

        try:
            response = api_manager.products_api.create_product(new_product)
            created = response.json()

            assert "id" in created
            assert created["sku"] == new_product["sku"]
            assert created["category_id"] == category_id

        finally:
            if created and "id" in created:
                api_manager.auth_api.authenticate((
                    registered_admin["email"],
                    registered_admin["password"]
                ))
                api_manager.products_api.delete_product(created["id"])

    def test_update_product(self, api_manager, created_product):
        update_data = {"name": "Updated product name"}

        response = api_manager.products_api.update_product(
            update_data, created_product["id"])

        updated_product = response.json()

        assert updated_product["id"] == created_product["id"]
        assert updated_product["name"] == update_data["name"]

    def test_update_price(self, api_manager, created_product, registered_admin):
        new_price = 6999
        api_manager.auth_api.authenticate((
            registered_admin["email"],
            registered_admin["password"]
        ))
        response = api_manager.products_api.update_price(created_product["id"], new_price)
        updated_product = response.json()

        assert updated_product["id"] == created_product["id"]
        assert Decimal(updated_product["price"]) == Decimal(str(new_price))

    def test_delete_product(self, api_manager, authenticated_admin):
        categories_list = api_manager.categories_api.get_categories().json()
        category_id = categories_list[0]["id"]
        new_product = DataGenerator.generate_product_data(category_id)

        response = api_manager.products_api.create_product(new_product)
        created = response.json()
        api_manager.products_api.delete_product(created["id"], )

        response = api_manager.products_api.get_product(created["id"])

        assert response.json()["is_available"] is False
