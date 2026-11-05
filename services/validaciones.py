import re
from extensions import db
from models.usuario import Usuario
from models.zona import Zona


def limpiar(texto):
    return re.sub(r"[\s-]", "", texto or "")


def validar_cedula(cedula):
    if not re.fullmatch(r"\d{10}", cedula):
        return "La cédula debe tener exactamente 10 números"

    provincia = int(cedula[:2])
    if not (1 <= provincia <= 24 or provincia == 30):
        return "Los dos primeros dígitos de la cédula no corresponden a una provincia del Ecuador"

    if int(cedula[2]) >= 6:
        return "El tercer dígito de la cédula no corresponde a una persona natural"

    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0
    for digito, coeficiente in zip(cedula[:9], coeficientes):
        producto = int(digito) * coeficiente
        if producto > 9:
            producto -= 9
        suma += producto

    verificador = (10 - suma % 10) % 10
    if verificador != int(cedula[9]):
        return "La cédula no es válida: el dígito verificador no coincide"

    return None


def validar_telefono(telefono):
    if not re.fullmatch(r"09\d{8}", telefono):
        return "El teléfono debe ser un celular de Ecuador: 10 números que empiecen por 09"
    return None


def validar_deportista(form, deportista=None):
    errores = []

    usuario = form.get("usuario", "").strip()
    contrasena = form.get("contrasena", "")
    cedula = limpiar(form.get("cedula"))
    telefono = limpiar(form.get("telefono"))
    ciudad_id = form.get("ciudad_id", type=int)
    zona_id = form.get("zona_id", type=int)

    if not usuario:
        errores.append("El usuario es obligatorio")
    else:
        existente = Usuario.query.filter_by(usuario=usuario).first()
        if existente and existente is not deportista:
            errores.append("Ese usuario ya existe")

    if deportista is None and not contrasena:
        errores.append("La contraseña es obligatoria")

    error = validar_cedula(cedula)
    if error:
        errores.append(error)
    else:
        existente = Usuario.query.filter_by(cedula=cedula).first()
        if existente and existente is not deportista:
            errores.append("Ya existe un deportista registrado con esa cédula")

    error = validar_telefono(telefono)
    if error:
        errores.append(error)

    zona = db.session.get(Zona, zona_id) if zona_id else None
    if zona is None:
        errores.append("Elige una ciudad y una zona")
    elif zona.ciudad_id != ciudad_id:
        errores.append("La zona elegida no pertenece a esa ciudad")

    datos = {
        "usuario": usuario,
        "contrasena": contrasena,
        "cedula": cedula,
        "telefono": telefono,
        "zona_id": zona.id if zona else None,
    }
    return errores, datos
