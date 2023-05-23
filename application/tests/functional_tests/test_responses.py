import requests
import json


def test_response_contains_a_user(capsys):
    response = requests.get("http://localhost:5000/users")
    json_data = json.loads(response.text)

    with capsys.disabled():
        print(f"\nTotal number of users: {len(json_data)}")
    assert json_data[0] is not None
    assert response.status_code == 200


def test_verify_keys_present(capsys):
    response = requests.get("http://localhost:5000/users")
    json_data = json.loads(response.text)

    for i in json_data:
        assert i["id"] is not None
        assert i["name"] is not None
        assert i["email"] is not None
        assert i["phone"] is not None
        with capsys.disabled():
            print(f"<User {i['id']} - name: {i['name']}, email: {i['email']}>")
