import logging
import json

DEFAULT_TIMEOUT = 10

logger = logging.getLogger("azon_tests")


class CustomRequester:
    """Базовый класс всех API-клиентов: отправка запросов и проверка статуса"""

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    def send_request(self, method, endpoint, expected_status=200, **kwargs):
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)

        response = self.session.request(method, url, **kwargs)
        self._log_request_and_response(response)

        if response.status_code != expected_status:
            raise AssertionError(
                f"{method} {url}: ожидали статус {expected_status},"
                f"получили {response.status_code}. Тело ответа: {response.text}"
            )
        return response

    def _update_session_headers(self, **headers):
        self.session.headers.update(headers)

    def _mask_sensitive_data(self, body, headers):

        safe_headers = dict(headers)
        safe_headers.pop("Authorization", None)

        safe_body = body
        if body:
            if isinstance(body, bytes):
                body = body.decode("utf-8")
            try:
                body = json.loads(body)

                if isinstance(body, dict) and "password" in body:
                    body["password"] = "***"

                safe_body = json.dumps(body)
            except json.JSONDecodeError:
                pass

        return safe_body, safe_headers

    def _log_request_and_response(self, response):
        request = response.request
        safe_body, safe_headers = self._mask_sensitive_data(
            request.body,
            request.headers,
        )

        logger.info("--> %s %s headers=%s", request.method, request.url, safe_headers)
        logger.info("    тело запроса: %s", safe_body)
        logger.info(
            "<-- %s за %.2f с: %s",
            response.status_code,
            response.elapsed.total_seconds(),
            response.text[:500],
        )

    def get_health(self):
        return self.send_request("GET", "/health")
