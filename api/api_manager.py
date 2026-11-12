from api.auth_api import AuthAPI
from api.products_api import ProductsAPI
from api.payment_api import PaymentAPI


class ApiManager:
    """Единая точка доступа ко всем API стенда"""

    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.products_api = ProductsAPI(session)
        self.payment_api = PaymentAPI(session)