import pytest
import json
from application.controllers.user_controller import user_service
from main import create_app
from application.config import TestConfig
from flask import jsonify


@pytest.fixture
def client():
    app = create_app(TestConfig)
    return app


def test_create_valid_user(client, mocker):
    app = client.test_client()
    mocker.patch('application.controllers.user_controller.user_service.create_user')
    request_data = {
        "name": "Leonard Graham",
        "username": "legra",
        "email": "legrah@may.biz",
        "phone": "1-770-736-8031 x56443"
    }
    expected_response = {"message": "Entries successfully created"}
    with client.app_context():
        user_service.create_user.return_value = jsonify(expected_response)
        response = app.post('/users', json=request_data)
    user_service.create_user.assert_called_once_with(request_data)
    response_data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert response_data == expected_response
