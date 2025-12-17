# data.py

# Encabezados de solicitud
headers = {
    "Content-Type": "application/json"
}

# Cuerpo base para la solicitud de creación de usuario
user_body = {
    "firstName": "TuNombre",
    # Formato de teléfono estricto: solo '+' y números, sin espacios
    "phone": "+34911234567",
    "address": "123 Elm Street, Hilltop"
}