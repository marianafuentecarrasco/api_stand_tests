import sender_stand_request
import data


# Esta función cambia los valores en el parámetro "firstName"
def get_user_body(first_name):
    # El diccionario que contiene el cuerpo de solicitud se copia del archivo "data" (datos)
    current_body = data.user_body.copy()
    # Se cambia el valor del parámetro firstName
    current_body["firstName"] = first_name
    # Se devuelve un nuevo diccionario con el valor firstName requerido
    return current_body


# Función de prueba positiva
def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    #  Imprime el código de estado y el JSON de la respuesta
    print(user_response.status_code)
    print(user_response.json())

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1


# Función de prueba negativa
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)

    print(response.status_code)
    print(response.json())

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Has introducido un nombre de usuario no válido. El nombre solo puede contener letras del alfabeto latino, la longitud debe ser de 2 a 15 caracteres."


# Función de prueba negativa
# La respuesta contiene el siguiente mensaje de error: "No se han aprobado todos los parámetros requeridos"
def negative_assert_no_firstname(user_body):
    response = sender_stand_request.post_new_user(user_body)

    print(response.status_code)
    print(response.json())

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "No se han aprobado todos los parámetros requeridos"


# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------

# Prueba 1. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene dos caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    user_body = get_user_body("Aa")
    user_response = sender_stand_request.post_new_user(user_body)

    print(user_response.status_code)
    print(user_response.json())

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1


# Prueba 2. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene 15 caracteres
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")


# Prueba 3. Error
# El parámetro "firstName" contiene un carácter
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")


# Prueba 4. Error
# El parámetro "firstName" contiene 16 caracteres
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")


# Prueba 5. Error
# El parámetro "firstName" contiene palabras con espacios
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A Aaa")


# Prueba 6. Error
# El parámetro "firstName" contiene un string de caracteres especiales
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")


# Prueba 7. Error
# El parámetro "firstName" contiene un string de números
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")


# Prueba 8. Error
# La solicitud no contiene el parámetro "firstName"
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_firstname(user_body)


# Prueba 9. Error
# El parámetro "firstName" contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_firstname(user_body)


# Prueba 10. Error
# El tipo del parámetro "firstName" es un número
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)

    print(response.status_code)
    print(response.json())

    assert response.status_code == 400
