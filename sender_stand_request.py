import configuration
import requests
import data


def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)


response = post_new_user(data.user_body)
print(response.status_code)
print(response.json())

assert response.status_code == 201
assert response.json()["authToken"] != ""

auth_token = response.json()["authToken"]

def post_new_client_kit(kit_body, auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    return requests.post(configuration.URL_SERVICE + configuration.KITS_PATH,
                         json=kit_body,
                         headers=headers)


kit_body = data.kit_body.copy()
response = post_new_client_kit(kit_body, auth_token)

print(response.status_code)
print(response.json())

assert response.status_code == 201
assert kit_body["name"] == response.json()["name"]