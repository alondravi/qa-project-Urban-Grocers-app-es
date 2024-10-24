import sender_stand_request
import data

def get_new_user_token():
    response = sender_stand_request.post_new_user(data.user_body)
    assert response.status_code == 201
    return response.json()["authToken"]

def get_kit_body(names):
    current_body = data.kit_body.copy()
    for name in names:
        if name is not None:
            current_body["name"] = name
        else:
            current_body.pop("name", None)
    return current_body

def positive_assert(kit_name):
    auth_token = get_new_user_token()
    kit_body = get_kit_body(kit_name)
    response = sender_stand_request.post_new_client_kit(kit_body, auth_token)
    assert response.status_code == 201
    assert kit_body["name"] == response.json()["name"]

def negative_assert_code_400(kit_name):
    auth_token = get_new_user_token()
    kit_body = get_kit_body(kit_name)
    response = sender_stand_request.post_new_client_kit(kit_body, auth_token)
    assert response.status_code == 400
    assert response.json()["code"] == 400

def test_create_kit_with_1_character_in_name_get_success_response():
    positive_assert("a")

def test_create_kit_with_511_characters_in_name_get_success_response():
    positive_assert("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")

def test_create_kit_with_0_characters_in_name_get_error_response():
    negative_assert_code_400("")

def test_create_kit_with_512_characters_in_name_get_error_response():
    negative_assert_code_400("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")

def test_create_kit_with_special_characters_in_name_get_success_response():
    positive_assert("!№%@,")

def test_create_kit_with_spaces_in_name_get_success_response():
    positive_assert(" A Aaa ")

def test_create_kit_with_numbers_character_in_name_get_success_response():
    positive_assert("123")

def test_create_kit_without_name_param_get_error_response():
    negative_assert_code_400(get_kit_body(None))

def test_create_kit_with_name_as_number_get_error_response():
    kit_body = data.kit_body.copy()
    kit_body["name"] = 123
    negative_assert_code_400(kit_body)
