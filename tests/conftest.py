import pytest
import requests

from api.api_manager import ApiManager
from data.users import UserData


@pytest.fixture
def api_manager():
    session = requests.Session()
    yield ApiManager(session)
    session.close()

@pytest.fixture()
def registered_user(api_manager):
    user_data = UserData.registration_data()
    api_manager.auth_api.register_user(user_data)
    return user_data


@pytest.fixture()
def authorized_user(api_manager, registered_user):
    api_manager.auth_api.authenticate(UserData.login_data(registered_user))
    return registered_user