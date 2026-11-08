<h1 align="center">Proyecto Flask MVC · Administración de Cuadra</h1>

<p align="center">
  <img src="static/img/logo.png" alt="Logo de Cuadra: una letra C formada por dos figuras verdes que se unen" width="140">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/STATUS-FINALIZADO-2e7d32">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Flask-MVC-000000?logo=flask&logoColor=white">
  <img src="https://img.shields.io/badge/PostgreSQL-Neon-4169E1?logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=white">
  <img src="https://img.shields.io/badge/Licencia-MIT-green">
</p>

<p align="center"><i>"Tú pones las ganas, nosotros cuadramos"</i></p>

---

## 📑 Índice

* [Descripción del proyecto](#-descripción-del-proyecto)
* [Estado del proyecto](#-estado-del-proyecto)
* [Funcionalidades y demostración](#-funcionalidades-y-demostración)
* [Validación en back-end del dato sensible](#-validación-en-back-end-del-dato-sensible)
* [Listas desplegables dependientes](#-listas-desplegables-dependientes)
* [Arquitectura MVC](#-arquitectura-mvc)
* [Seguridad](#-seguridad)
* [Acceso al proyecto](#-acceso-al-proyecto)
* [Abre y ejecuta el proyecto](#️-abre-y-ejecuta-el-proyecto)
* [Tecnologías utilizadas](#-tecnologías-utilizadas)
* [Persona desarrolladora](#-persona-desarrolladora)
* [Licencia](#-licencia)
* [Conclusión](#-conclusión)

---

## 📝 Descripción del proyecto

**Cuadra** es una plataforma que conecta deportistas que necesitan un compañero para jugar o entrenar. Su core es un **motor de emparejamiento por compatibilidad** para **fútbol** y **jiu-jitsu**, que ordena las publicaciones de cada deportista según esta fórmula:

```
Compatibilidad = 0,40 · Nivel + 0,25 · Zona + 0,15 · Horario + 0,20 · Confiabilidad
```

Este proyecto es la **administración MVC** que alimenta ese core. Desarrollada con **Flask** y **PostgreSQL**, permite al administrador registrar los datos que el motor necesita para calcular la compatibilidad:

* Los **deportes** y sus **niveles**, para el componente *Nivel*.
* Las **ciudades** y sus **zonas**, para el componente *Zona*.
* Los **deportistas**, identificados por su cédula, y sus **perfiles deportivos**.

**Objetivos cumplidos:**

* Aplicar el patrón MVC separando modelos, vistas y controladores.
* Implementar el CRUD de todas las tablas que alimentan el core.
* Validar en el **back-end** un dato sensible (la cédula) antes de guardarlo en la base de datos.
* Usar **listas desplegables dependientes** para las relaciones entre tablas, sin escribir claves foráneas a mano.
* Versionar el código en Git y publicar la aplicación en internet.

---

## 🚦 Estado del proyecto

<h4 align="center">✅ Versión 2.0 finalizada: administración del core con PostgreSQL ✅</h4>

Próximas mejoras planeadas: publicaciones de "busco compañero", postulaciones, registro de asistencia y el motor de emparejamiento.

---

## 🔨 Funcionalidades y demostración

* `Inicio de sesión y registro`: los deportistas crean su cuenta con su cédula, su WhatsApp y su zona.
* `Panel de administración`: solo el administrador puede entrar. Si un deportista intenta abrir una URL del panel, es redirigido.
* `CRUD de deportistas`: usuario, contraseña, cédula, teléfono, ciudad y zona.
* `CRUD de perfiles deportivos`: deporte, nivel, posición y peso de cada deportista (máximo un perfil por deporte).
* `CRUD de deportes y niveles`: cada nivel pertenece a un deporte y tiene un orden (1 = el más bajo).
* `CRUD de ciudades y zonas`: cada zona pertenece a una ciudad.
* `Integridad de los datos`: no se puede eliminar un deporte, nivel, ciudad o zona que esté en uso.
* `Datos iniciales`: la primera vez que se ejecuta, se crean el administrador, los deportes del core con sus niveles y las ciudades de Quito y Guayaquil con sus zonas.

### 🌐 Aplicación publicada

https://cuadra-85xn.onrender.com

### 🎥 Video de demostración

https://youtu.be/z20BVmVjpNI

### 📸 Capturas

| Inicio de sesión | Registro de deportista |
| :---: | :---: |
| ![Pantalla de inicio de sesión](docs/img/login.png) | ![Pantalla de registro](docs/img/registro.png) |

| Gestión de deportistas | Cédula rechazada por el back-end |
| :---: | :---: |
| ![Panel con la lista de deportistas](docs/img/panel.png) | ![Formulario con el error de cédula no válida](docs/img/validacion.png) |

| Lista dependiente: deporte → nivel |
| :---: |
| ![Formulario de perfil deportivo con los niveles de jiu-jitsu](docs/img/listas.png) |

---

## 🚨 Validación en back-end del dato sensible

El dato sensible del core es la **cédula**. La confiabilidad de cada deportista baja cuando falta a una actividad. Si una persona pudiera abrir otra cuenta, volvería a empezar con 100 % de confiabilidad. La cédula asegura **una sola cuenta por persona**, así su historial de asistencia no se puede borrar.

La cédula **no se valida con JavaScript**. El formulario la envía tal cual y el servidor la revisa en `services/validaciones.py` antes de guardarla:

1. Tiene exactamente **10 números**.
2. Los dos primeros dígitos son una **provincia del Ecuador** (01 a 24, o 30 para ecuatorianos en el exterior).
3. El tercer dígito es **menor a 6** (persona natural).
4. El último dígito coincide con el **dígito verificador** del algoritmo **módulo 10** del Registro Civil.
5. **No está repetida** en la base de datos.

```python
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
```

Los controladores llaman a `validar_deportista()` **antes** de `db.session.commit()`. Si hay un error, se muestra el mensaje y no se guarda nada. Además, la columna `cedula` es `UNIQUE` en PostgreSQL como última barrera. El teléfono también se valida en el servidor: debe ser un celular de Ecuador (`09` y 8 números más).

---

## 🔗 Listas desplegables dependientes

Ninguna clave foránea se escribe a mano. Las relaciones se eligen con listas desplegables y, cuando una depende de otra, la segunda se carga según lo elegido en la primera:

| Formulario | Primera lista | Segunda lista (se carga según la primera) | Se guarda |
| --- | --- | --- | --- |
| Deportista | Ciudad | Zonas de esa ciudad | `zona_id` |
| Perfil deportivo | Deporte | Niveles de ese deporte | `nivel_id` |
| Nivel | Deporte | — | `deporte_id` |
| Zona | Ciudad | — | `ciudad_id` |

**Cómo funciona:**

1. Al cambiar la ciudad, `static/js/listas.js` pide las zonas al servidor con `fetch`.
2. La ruta `/api/ciudades/<id>/zonas` de `controllers/api_controller.py` consulta PostgreSQL y responde en JSON.
3. El JavaScript llena la lista de zonas con esa respuesta.
4. Al guardar, el back-end vuelve a comprobar que la zona pertenezca a la ciudad elegida (y el nivel al deporte), por si alguien manipula el formulario.

---

## 🧱 Arquitectura MVC

```
proyecto_cuadra/
├── app.py                         # Punto de entrada: crea la app, registra los controladores y carga los datos iniciales
├── config.py                      # Configuración: lee la base de datos y la clave secreta del archivo .env
├── extensions.py                  # Instancias de SQLAlchemy y Flask-Login
├── requirements.txt               # Dependencias del proyecto
│
├── models/                        # MODELO: tablas de la base de datos
│   ├── usuario.py                 # Deportistas y administrador (cédula, teléfono, zona)
│   ├── perfil_deportivo.py        # Deporte y nivel de cada deportista
│   ├── deporte.py
│   ├── nivel.py
│   ├── ciudad.py
│   └── zona.py
│
├── services/
│   └── validaciones.py            # Validación de cédula, teléfono y datos del deportista
│
├── controllers/                   # CONTROLADOR: reciben las peticiones y deciden qué hacer
│   ├── auth_controller.py         # Login, registro y cierre de sesión
│   ├── usuario_controller.py      # CRUD de deportistas
│   ├── perfil_controller.py       # CRUD de perfiles deportivos
│   ├── deporte_controller.py      # CRUD de deportes
│   ├── nivel_controller.py        # CRUD de niveles
│   ├── ciudad_controller.py       # CRUD de ciudades
│   ├── zona_controller.py         # CRUD de zonas
│   ├── api_controller.py          # JSON para las listas dependientes
│   └── decoradores.py             # @admin_requerido
│
├── templates/                     # VISTA: plantillas HTML (Jinja2)
│   ├── base.html                  # Panel con barra lateral
│   ├── base_acceso.html           # Pantallas de login y registro
│   ├── index.html · registro.html · inicio.html
│   ├── _campos_deportista.html    # Campos compartidos por registro y admin
│   └── usuarios/ · perfiles/ · deportes/ · niveles/ · ciudades/ · zonas/
│
└── static/
    ├── css/style.css              # Estilos propios
    ├── js/listas.js               # Listas desplegables dependientes
    └── img/logo.png
```

| Capa | Responsabilidad |
| --- | --- |
| **Modelo** | Define las tablas y sus relaciones (claves foráneas y restricciones `UNIQUE`). |
| **Vista** | Muestra la información con plantillas Jinja2, HTML y CSS. |
| **Controlador** | Recibe cada petición, valida los datos, consulta o modifica el modelo y elige qué vista mostrar. |

### Modelo de datos

| Relación | Tipo | Clave foránea |
| --- | --- | --- |
| Una ciudad tiene muchas zonas | 1 a N | `zonas.ciudad_id` |
| Una zona tiene muchos deportistas | 1 a N | `usuarios.zona_id` |
| Un deporte tiene muchos niveles | 1 a N | `niveles.deporte_id` |
| Un deportista tiene un perfil por deporte | 1 a N, `UNIQUE (usuario_id, deporte_id)` | `perfiles_deportivos.usuario_id` |
| Cada perfil tiene un deporte y un nivel | N a 1 | `perfiles_deportivos.deporte_id`, `perfiles_deportivos.nivel_id` |

### Rutas de la aplicación

| Método | Ruta | Descripción | Acceso |
| --- | --- | --- | :---: |
| GET / POST | `/` | Inicio de sesión | Público |
| GET / POST | `/registro` | Registro de deportista | Público |
| GET | `/logout` | Cerrar sesión | Con sesión |
| GET | `/usuarios/` · `/perfiles/` · `/deportes/` · `/niveles/` · `/ciudades/` · `/zonas/` | Listar | Admin |
| GET / POST | `/<sección>/crear` | Crear | Admin |
| GET / POST | `/<sección>/editar/<id>` | Editar | Admin |
| POST | `/<sección>/eliminar/<id>` | Eliminar | Admin |
| GET | `/api/ciudades/<id>/zonas` | Zonas de una ciudad (JSON) | Público |
| GET | `/api/deportes/<id>/niveles` | Niveles de un deporte (JSON) | Público |

---

## 🔐 Seguridad

### Contraseñas hasheadas

Las contraseñas **nunca se guardan en texto plano**. El modelo `Usuario` usa las funciones de **Werkzeug**:

```python
def set_contrasena(self, contrasena):
    self.contrasena_hash = generate_password_hash(contrasena)

def verificar_contrasena(self, contrasena):
    return check_password_hash(self.contrasena_hash, contrasena)
```

`generate_password_hash` usa el algoritmo **scrypt** con una **sal aleatoria**, así dos usuarios con la misma contraseña tienen hashes distintos.

### Rutas protegidas

Las rutas del panel llevan el decorador `@admin_requerido`, que combina `@login_required` de **Flask-Login** con la revisión del rol:

```python
def admin_requerido(vista):
    @wraps(vista)
    @login_required
    def envoltura(*args, **kwargs):
        if not current_user.es_admin:
            flash("Solo el administrador puede entrar a esa sección", "error")
            return redirect(url_for("auth.inicio"))
        return vista(*args, **kwargs)
    return envoltura
```

### Datos privados fuera del repositorio

La dirección de la base de datos y la clave secreta se leen del archivo `.env`, que está en el `.gitignore` y **no se sube a GitHub**. En el servidor se configuran como variables de entorno.

---

## 📁 Acceso al proyecto

Clona el repositorio:

```bash
git clone https://github.com/Alejo2442/proyecto_cuadra.git
cd proyecto_cuadra
```

O descárgalo como ZIP desde el botón **Code → Download ZIP** de esta página.

---

## 🛠️ Abre y ejecuta el proyecto

**Requisitos:** Python 3.10 o superior y una base de datos PostgreSQL (por ejemplo, gratis en [Neon](https://neon.com)).

1. **Crea y activa un entorno virtual**

   ```bash
   python -m venv venv
   ```

   Windows:
   ```bash
   venv\Scripts\activate
   ```

   macOS / Linux:
   ```bash
   source venv/bin/activate
   ```

2. **Instala las dependencias**

   ```bash
   pip install -r requirements.txt
   ```

3. **Crea el archivo `.env`** en la raíz del proyecto con estas variables:

   ```
   DATABASE_URL=postgresql://usuario:clave@servidor/neondb?sslmode=require
   SECRET_KEY=una-clave-secreta
   ADMIN_PASSWORD=contraseña-del-admin
   ```

4. **Ejecuta la aplicación**

   ```bash
   python app.py
   ```

5. **Abre el navegador** en [http://127.0.0.1:5000](http://127.0.0.1:5000)

Las tablas y los datos iniciales se crean automáticamente la primera vez. El administrador es el usuario `admin` con la contraseña definida en `ADMIN_PASSWORD`.

> En Windows, si al activar el entorno aparece un error de "ejecución de scripts deshabilitada", ejecuta una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

### Publicación en Render

| Campo | Valor |
| --- | --- |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Variables de entorno | `DATABASE_URL`, `SECRET_KEY`, `ADMIN_PASSWORD` |

---

## 💻 Tecnologías utilizadas

| Tecnología | Uso en el proyecto |
| --- | --- |
| **Python** | Lenguaje principal |
| **Flask** | Framework web: rutas, controladores y plantillas |
| **PostgreSQL (Neon)** | Base de datos en la nube |
| **Flask-SQLAlchemy** | ORM para trabajar con la base de datos usando clases de Python |
| **psycopg** | Conexión entre Python y PostgreSQL |
| **Flask-Login** | Manejo de la sesión y protección de rutas |
| **Werkzeug** | Hash seguro de contraseñas (scrypt) |
| **python-dotenv** | Lectura de las variables del archivo `.env` |
| **Jinja2** | Motor de plantillas de las vistas |
| **HTML, CSS y JavaScript** | Interfaz con estilos propios y listas dependientes con `fetch` |
| **Gunicorn y Render** | Servidor y publicación de la aplicación |

---

## 👤 Persona desarrolladora

| [<img src="https://github.com/Alejo2442.png" width=115><br><sub>Alejandro Martínez</sub>](https://github.com/Alejo2442) |
| :---: |

Proyecto desarrollado para la materia de **Ingeniería Web**.

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## ✅ Conclusión

Este proyecto implementa la administración que alimenta el core de Cuadra siguiendo el patrón **MVC**. Los datos sensibles se validan en el **back-end** antes de llegar a **PostgreSQL**, las relaciones entre tablas se eligen con **listas dependientes** y el panel está protegido por rol. Con estos datos, el motor de emparejamiento podrá calcular la compatibilidad entre deportistas.
