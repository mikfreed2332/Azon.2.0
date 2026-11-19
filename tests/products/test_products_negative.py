import uuid

from utils.data_generator import DataGenerator



class TestProductsNegative:

    def test_get_nonexistent_product(self, api_manager):
        response = api_manager.products_api.get_product(
            uuid.uuid4(), expected_status=404)

        assert response.json()["error"]["code"] == "PRODUCT_NOT_FOUND"

    def test_delete_product_without_auth(self, api_manager, created_product):
        api_manager.products_api.session.headers.pop("Authorization", None)
        response = api_manager.products_api.delete_product(
            created_product["id"], expected_status=401)

        assert response.json()["error"]["code"] == "TOKEN_MISSING"

    def test_delete_product_as_user(self, api_manager, created_product, registered_user):
        api_manager.auth_api.authenticate((registered_user["email"], registered_user["password"]))
        response = api_manager.products_api.delete_product(created_product["id"],
                                                           expected_status=403)
        assert response.json()["error"]["code"] == "FORBIDDEN"

    def test_delete_product_as_manager(self, api_manager, created_product):
        response = api_manager.products_api.delete_product(
            created_product["id"], expected_status=403
        )

        assert response.json()["error"]["code"] == "FORBIDDEN"

    def test_create_product_with_existing_sku(self, api_manager, created_product):
        new_product = DataGenerator.generate_product_data(
            created_product["category_id"]
        )

        new_product["sku"] = created_product["sku"]

        response = api_manager.products_api.create_product(
            new_product, expected_status=409
        )

        assert response.json()["error"]["code"] == "SKU_EXISTS"