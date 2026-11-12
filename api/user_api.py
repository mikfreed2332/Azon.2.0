from config.hosts import AUTH_URL
from requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):
    """Клиент User API: профиль и данные пользователей."""
    