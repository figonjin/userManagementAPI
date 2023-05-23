import requests
import json


def test_create_valid_user():
    url = "http://localhost:5000/users"
    body = {
        "name": "Spike Spiegel",
        "username": "spigel",
        "email": "spike@bhff.biz",
        "address": {
            "street": "Kulas Light",
            "suite": "Apt. 556",
            "city": "Gwenborough",
            "zipcode": "92998-3874"
        },
        "phone": "0-800-fake-number"
    }

    x = requests.post(url, json=body)

    assert x.status_code == 201

    response = requests.get('http://localhost:5000/users')
    json_data = json.loads(response.text)
    user_id = None

    for i in json_data:
        if i["name"] == "Spike Spiegel":
            assert i["id"] is not None
            assert i["name"] == "Spike Spiegel"
            assert i["email"] == "spike@bhff.biz"
            assert i["phone"] == "0-800-fake-number"
            assert i["address"] == {
                "street": "Kulas Light",
                "suite": "Apt. 556",
                "city": "Gwenborough",
                "zipcode": "92998-3874",
                "geo": {"lat": "-1", "lng": "-1"}
            }
            user_id = i["id"]
    # Clean up the database
    response = requests.post(f'http://localhost:5000/users/{user_id}/delete')
    json_response = json.loads(response.text)
    assert json_response == {"message": "User successfully deleted"}


def test_create_invalid_user():
    url = "http://localhost:5000/users"
    body = {
        "name": "Spike Spiegel",
        "username": "spigel",
        "address": {
            "street": "Kulas Light",
            "suite": "Apt. 556",
            "city": "Gwenborough",
            "zipcode": "92998-3874"
        },
    }

    x = requests.post(url, json=body)

    json_response = json.loads(x.text)
    assert x.status_code == 400
    assert json_response == {"message": "Failed to create entries with the following error\n"
                                        "The following user fields are mandatory email, phone"}


def test_sql_injection():
    url = "http://localhost:5000/users"
    body = {
        "name": "'DROP TABLE users'",
        "username": "spigel",
        "email": "spike@bhff.biz",
        "address": {
            "street": "Kulas Light",
            "suite": "Apt. 556",
            "city": "Gwenborough",
            "zipcode": "92998-3874"
        },
        "phone": "0-800-fake-number"
    }

    x = requests.post(url, json=body)
    assert x.status_code == 201

    response = requests.get('http://localhost:5000/users')
    json_data = json.loads(response.text)
    for i in json_data:
        if i["name"] == "&#39;DROP TABLE users&#39;":
            response = requests.post(f'http://localhost:5000/users/{i["id"]}/delete')
            json_response = json.loads(response.text)
            assert json_response == {"message": "User successfully deleted"}


def test_xss_injection():
    url = "http://localhost:5000/users"
    body = {
        "name": "<script>alert('XSS Injection')</script>",
        "username": "spigel",
        "email": "spike@bhff.biz",
        "address": {
            "street": "Kulas Light",
            "suite": "Apt. 556",
            "city": "Gwenborough",
            "zipcode": "92998-3874"
        },
        "phone": "0-800-fake-number"
    }

    x = requests.post(url, json=body)
    assert x.status_code == 201

    response = requests.get('http://localhost:5000/users')
    json_data = json.loads(response.text)
    for i in json_data:
        if i["name"] == "&lt;script&gt;alert(&#39;XSS Injection&#39;)&lt;/script&gt;":
            response = requests.post(f'http://localhost:5000/users/{i["id"]}/delete')
            json_response = json.loads(response.text)
            assert json_response == {"message": "User successfully deleted"}