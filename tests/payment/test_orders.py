class TestOrders:

    def test_new_user_has_no_orders(self, api_manager, authorized_user):
        response = api_manager.payment_api.get_orders()

        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []