import pytest
import requests

from api import user_api
from config.credentials import MANAGER_INVITE_CODE, ADMIN_INVITE_CODE
from api.api_manager import ApiManager
from data.users import UserData


@pytest.fixture(scope="function")
def api_manager():
    session = requests.Session()
    yield ApiManager(session)
    session.close()

@pytest.fixture()
def registered_user(api_manager):
    user_data = UserData.registration_data()
    response = api_manager.auth_api.register_user(user_data)
    return {**user_data, "id": response.json()["id"]}

@pytest.fixture(scope="function")
def authenticated_user(api_manager):
    user_data = UserData.registration_data()
    register_response = api_manager.auth_api.register_user(user_data)
    api_manager.auth_api.authenticate((user_data["email"], user_data["password"]))
    return {**user_data, "id": register_response.json()["id"]}

@pytest.fixture()
def registered_manager(api_manager):
    manager_data = UserData.registration_data(invite_code=MANAGER_INVITE_CODE)
    response = api_manager.auth_api.register_user(manager_data)
    return {**manager_data, "id": response.json()["id"]}

@pytest.fixture()
def registered_admin(api_manager):
    admin_data = UserData.registration_data(invite_code=ADMIN_INVITE_CODE)
    response = api_manager.auth_api.register_user(admin_data)
    return {**admin_data, "id": response.json()["id"]}

@pytest.fixture()
def authenticated_manager(api_manager, registered_manager):
    api_manager.auth_api.authenticate((registered_manager["email"],
                                       registered_manager["password"]))
    return registered_manager

@pytest.fixture()
def authenticated_admin(api_manager, registered_admin):
    api_manager.auth_api.authenticate((registered_admin["email"],
                                       registered_admin["password"]))
    return registered_admin

