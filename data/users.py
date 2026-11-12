from utils.data_generator import DataGenerator


class UserData:
    """Object Mother для тел запроса Auth API."""

    @staticmethod
    def registration_data() -> dict:
        return {
            "email": DataGenerator.generate_email(),
            "password": DataGenerator.generate_password(),
            "full_name": DataGenerator.generate_full_name(),
        }

    @staticmethod
    def login_data(user_data) -> dict:
        return {"email": user_data["email"], "password": user_data["password"]}