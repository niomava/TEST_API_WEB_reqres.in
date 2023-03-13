import pytest


class TestAPI_Positive:

    verify = False

    # Получение информации о пользователях
    @pytest.mark.parametrize("endpoint, status_code, value_page, amount_keys", [("users?page=2", 200, 2, 6)])
    def test_get_list_users(self, api_client, api_url, endpoint, status_code, value_page, amount_keys):
        response = api_client.get(f'{api_url}{endpoint}', verify=self.verify)
        assert response.status_code == status_code
        assert response.json()["page"] == value_page
        assert len(response.json()) == amount_keys
        assert len(response.json()["data"]) == response.json()["per_page"]

    # Получение информации о пользователях с параметром запроса delay=3
    @pytest.mark.parametrize("endpoint, status_code, value_page, amount_keys", [("users?delay=3", 200, 1, 6)])
    def test_get_list_delay(self, api_client, api_url, endpoint, status_code, value_page, amount_keys):
        response = api_client.get(f'{api_url}{endpoint}', verify=self.verify)
        assert response.status_code == status_code
        assert response.json()["page"] == value_page
        assert len(response.json()) == amount_keys
        assert len(response.json()["data"]) == response.json()["per_page"]
        assert response.elapsed.seconds >= 3

    # Получение информации о пользователе
    @pytest.mark.parametrize("endpoint, status_code,value_id", [("users/2", 200, 2)])
    def test_get_single_user(self, api_client, api_url, endpoint, status_code, value_id):
        response = api_client.get(f'{api_url}{endpoint}', verify=self.verify)
        assert response.status_code == status_code
        assert response.json()["data"]["id"] == value_id

    # Получение информации <RESOURCE> всех пользователей
    @pytest.mark.parametrize("endpoint, status_code, amount_keys, value_page", [("unknown", 200, 6, 1)])
    def test_get_list_resource(self, api_client, api_url, endpoint, status_code, amount_keys, value_page):
        response = api_client.get(f'{api_url}{endpoint}', verify=self.verify)
        assert response.status_code == status_code
        assert len(response.json()) == amount_keys
        assert response.json()["page"] == value_page
        assert len(response.json()["data"]) == response.json()["per_page"]

    # Получение информации <RESOURCE> для пользователя
    @pytest.mark.parametrize("endpoint, status_code, amount_keys, value_id", [("unknown/2", 200, 2, 2)])
    def test_get_single_resource(self, api_client, api_url, endpoint, status_code, amount_keys, value_id):
        response = api_client.get(f'{api_url}{endpoint}', verify=self.verify)
        assert response.status_code == status_code
        assert len(response.json()) == amount_keys
        assert response.json()["data"]["id"] == value_id

    # Создание пользователя
    @pytest.mark.parametrize("endpoint, status_code, body", [("users", 201, {"name": "morpheus", "job": "leader"})])
    def test_post_create(self, api_client, api_url, endpoint, status_code, body):
        response = api_client.post(f'{api_url}{endpoint}', data=body, verify=self.verify)
        assert response.status_code == status_code
        assert response.json()["name"], response.json()["job"] == body

    # Редактирование пользователя полное обновление данных
    @pytest.mark.parametrize("endpoint, status_code, body",
                             [("users/2", 200, {"name": "morpheus", "job": "zion resident"})])
    def test_put_update(self, api_client, api_url, endpoint, status_code, body):
        response = api_client.put(f'{api_url}{endpoint}', data=body, verify=self.verify)
        assert response.status_code == status_code
        assert response.json()["name"], response.json()["job"] == body

    # Редактирование пользователя частичное обновление данных
    @pytest.mark.parametrize("endpoint, status_code, body",
                             [("users/2", 200, {"name": "morpheus", "job": "zion resident"})])
    def test_patch_update(self, api_client, api_url, endpoint, status_code, body):
        response = api_client.patch(f'{api_url}{endpoint}', data=body, verify=self.verify)
        assert response.status_code == status_code
        assert response.json()["name"], response.json()["job"] == body

    # Удаление пользователя
    @pytest.mark.parametrize("endpoint, status_code", [("users/2", 204)])
    def test_delete_user(self, api_client, api_url, endpoint, status_code):
        response = api_client.delete(f'{api_url}{endpoint}', verify=self.verify)
        assert response.status_code == status_code

    # Регистрация пользователя
    @pytest.mark.parametrize("endpoint, status_code,amount_keys, body",
                             [("register", 200, 2, {"email": "eve.holt@reqres.in",
                                                    "password": "pistol"})])
    def test_register_user(self, api_client, api_url, endpoint, status_code, amount_keys, body):
        response = api_client.post(f'{api_url}{endpoint}', data=body, verify=self.verify)
        assert response.status_code == status_code
        assert len(response.json()) == amount_keys
        assert response.json()["id"] > 0
        assert len(response.json()["token"]) == 17

    # Авторизация пользователя
    @pytest.mark.parametrize("endpoint, status_code, body",
                             [("login", 200, {"email": "eve.holt@reqres.in",
                                              "password": "cityslicka"})])
    def test_login_user(self, api_client, api_url, endpoint, status_code, body):
        response = api_client.post(f'{api_url}{endpoint}', data=body, verify=self.verify)
        assert response.status_code == status_code
        assert len(response.json()["token"]) == 17


class TestApi_Negative:

    verify = False

    # Получение информации о несуществующем пользователе
    @pytest.mark.parametrize("endpoint, status_code,value_body_response", [("users/23", 404, {})])
    def test_get_single_user_not_found(self, api_client, api_url, endpoint, status_code, value_body_response):
        response = api_client.get(f'{api_url}{endpoint}', verify=self.verify)
        assert response.status_code == status_code
        assert response.json() == value_body_response

    # Получение информации <RESOURCE> для несуществующего пользователя
    @pytest.mark.parametrize("endpoint, status_code,value_body_response", [("unknown/23", 404, {})])
    def test_get_single_resource_not_found(self, api_client, api_url, endpoint, status_code, value_body_response):
        response = api_client.get(f'{api_url}{endpoint}', verify=self.verify)
        assert response.status_code == status_code
        assert response.json() == value_body_response

    # Создание пользователя c пустым телом запроса и endpoint
    @pytest.mark.parametrize("endpoint, status_code, body", [("", 404, {})])
    def test_post_create_not_found(self, api_client, api_url, endpoint, status_code, body):
        response = api_client.post(f'{api_url}{endpoint}', data=body, verify=self.verify)
        assert response.status_code == status_code

    # Обновление пользователя c пустым endpoint
    @pytest.mark.parametrize("endpoint, status_code, body", [("", 404, {"name": "morpheus", "job": "zion resident"})])
    def test_put_not_found(self, api_client, api_url, endpoint, status_code, body):
        response = api_client.put(f'{api_url}{endpoint}', data=body, verify=self.verify)
        assert response.status_code == status_code

    # Удаление пользователя с пустым endpoint
    @pytest.mark.parametrize("endpoint, status_code", [("", 404)])
    def test_delete_user_not_found(self, api_client, api_url, endpoint, status_code):
        response = api_client.delete(f'{api_url}{endpoint}', verify=self.verify)
        assert response.status_code == status_code

    # Регистрация пользователя без пароля и email без доменной зоны
    @pytest.mark.parametrize("endpoint, status_code, error, body",
                             [("register", 400, "Missing password", {"email": "sydney@fife"})])
    def test_register_user_not_password(self, api_client, api_url, endpoint, status_code, error, body):
        response = api_client.post(f'{api_url}{endpoint}', data=body, verify=self.verify)
        assert response.status_code == status_code
        assert response.json()["error"] == error

    # Авторизация пользователя без пароля и email без доменной зоны
    @pytest.mark.parametrize("endpoint, status_code, error, body",
                             [("login", 400, "Missing password", {"email": "peter@klaven"})])
    def test_login_user_not_password(self, api_client, api_url, endpoint, status_code, error, body, tear_down):
        response = api_client.post(f'{api_url}{endpoint}', data=body, verify=self.verify)
        assert response.status_code == status_code
        assert response.json()["error"] == error
