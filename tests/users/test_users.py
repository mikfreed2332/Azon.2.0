from data.users import UserData
from utils.data_generator import DataGenerator


class TestUsers:

    def test_get_user_info_without_token(self, api_manager):
        response = api_manager.user_api.get_user_info(expected_status=401)

        assert response.json()["error"]["code"] == "TOKEN_MISSING"

    def test_get_user_info(self, api_manager, authenticated_user):
        response = api_manager.user_api.get_user_info()

        user = response.json()
        assert user["email"] == authenticated_user["email"]
        assert user["id"] == authenticated_user["id"]

    def test_update_full_name(self, api_manager, authenticated_user):
        new_profile = UserData.update_profile_data()

        response = api_manager.user_api.update_user_info(new_profile)

        assert response.json()["full_name"] == new_profile["full_name"]
        assert api_manager.user_api.get_user_info().json()["full_name"] == new_profile["full_name"]

    def test_change_password(self, api_manager, authenticated_user):
        new_password = DataGenerator.generate_password()

        api_manager.user_api.change_password(
            UserData.change_password_data(authenticated_user, new_password)
        )

        old_credentials = UserData.login_data(authenticated_user)
        response = api_manager.auth_api.login_user(old_credentials, expected_status=401)
        assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"

        api_manager.auth_api.authenticate((authenticated_user["email"], new_password))

    def test_manager_role(self, api_manager, authenticated_manager):
        response = api_manager.user_api.get_user_info()
        assert response.json()["role"] == "MANAGER"

    def test_admin_role(self, api_manager, authenticated_admin):
        response = api_manager.user_api.get_user_info()
        assert response.json()["role"] == "ADMIN"

    def test_register_with_invalid_invite_code(self, api_manager):
        user_data = UserData.registration_data(invite_code="invalid_code")

        response = api_manager.auth_api.register_user(
            user_data,
            expected_status=403
        )
        assert response.json()["error"]["code"] == "INVALID_INVITE_CODE"

    def test_user_role(self, api_manager, registered_user):
        api_manager.auth_api.authenticate(
            (registered_user["email"], registered_user["password"])
        )

        response = api_manager.user_api.get_user_info()

        assert response.json()["role"] == "USER"



