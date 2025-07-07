# Manual de Uso del Framework Agno

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Conceptos Básicos](#conceptos-básicos)
4. [Primeros Pasos](#primeros-pasos)
5. [Rutas y Controladores](#rutas-y-controladores)
6. [Modelos y Base de Datos](#modelos-y-base-de-datos)
7. [Vistas y Plantillas](#vistas-y-plantillas)
8. [Middleware](#middleware)
9. [Autenticación y Autorización](#autenticación-y-autorización)
10. [API REST](#api-rest)
11. [Mejores Prácticas](#mejores-prácticas)
12. [Solución de Problemas](#solución-de-problemas)

## 1. Introducción

Agno es un framework web moderno para Python que se centra en la simplicidad, velocidad y escalabilidad. Está diseñado para crear aplicaciones web robustas con una sintaxis clara y una arquitectura flexible.

### Características Principales:
- **Ligero y rápido**: Optimizado para alto rendimiento
- **Sintaxis intuitiva**: API simple y fácil de aprender
- **Asíncrono por defecto**: Soporte completo para programación asíncrona
- **Sistema de rutas flexible**: Enrutamiento dinámico y paramétrico
- **ORM integrado**: Manejo simplificado de bases de datos
- **Sistema de plantillas potente**: Motor de renderizado eficiente
- **Middleware personalizable**: Extensibilidad completa
- **Soporte para WebSockets**: Comunicación en tiempo real
- **CLI integrada**: Herramientas de línea de comandos

## 2. Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Entorno virtual (recomendado)

### Instalación Básica

```bash
# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar Agno
pip install agno

# Verificar la instalación
agno --version
```

### Instalación con Extras

```bash
# Instalación completa con todas las dependencias
pip install agno[full]

# Instalación con soporte para PostgreSQL
pip install agno[postgres]

# Instalación con soporte para desarrollo
pip install agno[dev]
```

## 3. Conceptos Básicos

### Arquitectura MVC
Agno sigue el patrón Modelo-Vista-Controlador (MVC):

- **Modelo**: Representa los datos y la lógica de negocio
- **Vista**: Maneja la presentación de datos
- **Controlador**: Gestiona las solicitudes y coordina entre modelos y vistas

### Estructura de Proyecto

```
mi-proyecto-agno/
├── app/
│   ├── __init__.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── home_controller.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── views/
│   │   ├── base.html
│   │   └── home.html
│   ├── middleware/
│   │   └── __init__.py
│   └── config.py
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── tests/
├── requirements.txt
├── .env
└── main.py
```

## 4. Primeros Pasos

### Crear una Aplicación Básica

```python
# main.py
from agno import Agno, Request, Response

# Crear instancia de la aplicación
app = Agno()

# Definir una ruta básica
@app.route('/')
async def home(request: Request) -> Response:
    return Response("¡Hola, mundo con Agno!")

# Ruta con parámetros
@app.route('/saludo/<nombre>')
async def saludo(request: Request, nombre: str) -> Response:
    return Response(f"¡Hola, {nombre}!")

# Iniciar el servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
```

### Ejecutar la Aplicación

```bash
# Ejecutar directamente
python main.py

# O usar el CLI de Agno
agno run

# Ejecutar en modo producción
agno run --production
```

## 5. Rutas y Controladores

### Definición de Rutas

```python
from agno import Agno, Request, Response, JsonResponse

app = Agno()

# Ruta GET básica
@app.route('/users', methods=['GET'])
async def get_users(request: Request) -> Response:
    users = await User.all()
    return JsonResponse({'users': users})

# Ruta POST
@app.route('/users', methods=['POST'])
async def create_user(request: Request) -> Response:
    data = await request.json()
    user = await User.create(**data)
    return JsonResponse({'user': user.to_dict()}, status=201)

# Rutas con parámetros
@app.route('/users/<int:user_id>')
async def get_user(request: Request, user_id: int) -> Response:
    user = await User.get(user_id)
    if not user:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    return JsonResponse({'user': user.to_dict()})

# Rutas con expresiones regulares
@app.route('/posts/<slug:[\w-]+>')
async def get_post(request: Request, slug: str) -> Response:
    post = await Post.get_by_slug(slug)
    return JsonResponse({'post': post.to_dict()})
```

### Controladores Organizados

```python
# app/controllers/user_controller.py
from agno import Controller, Request, Response, JsonResponse

class UserController(Controller):
    async def index(self, request: Request) -> Response:
        """Listar todos los usuarios"""
        users = await User.all()
        return self.render('users/index.html', {'users': users})
    
    async def show(self, request: Request, user_id: int) -> Response:
        """Mostrar un usuario específico"""
        user = await User.get_or_404(user_id)
        return self.render('users/show.html', {'user': user})
    
    async def create(self, request: Request) -> Response:
        """Crear un nuevo usuario"""
        if request.method == 'POST':
            data = await request.form()
            user = await User.create(**data)
            return self.redirect(f'/users/{user.id}')
        return self.render('users/create.html')
    
    async def update(self, request: Request, user_id: int) -> Response:
        """Actualizar un usuario"""
        user = await User.get_or_404(user_id)
        if request.method == 'PUT':
            data = await request.json()
            await user.update(**data)
            return JsonResponse({'user': user.to_dict()})
        return self.render('users/edit.html', {'user': user})
    
    async def delete(self, request: Request, user_id: int) -> Response:
        """Eliminar un usuario"""
        user = await User.get_or_404(user_id)
        await user.delete()
        return JsonResponse({'message': 'Usuario eliminado'}, status=204)

# Registrar controlador
app.register_controller(UserController, prefix='/users')
```

### Grupos de Rutas

```python
# Crear un grupo de rutas
api = app.group('/api/v1')

# Agregar middleware al grupo
api.middleware(auth_middleware)
api.middleware(rate_limit_middleware)

# Definir rutas en el grupo
@api.route('/products')
async def get_products(request: Request) -> Response:
    products = await Product.all()
    return JsonResponse({'products': products})

@api.route('/orders')
async def get_orders(request: Request) -> Response:
    orders = await Order.filter(user_id=request.user.id)
    return JsonResponse({'orders': orders})
```

## 6. Modelos y Base de Datos

### Configuración de Base de Datos

```python
# app/config.py
from agno import Config

class DevelopmentConfig(Config):
    DATABASE = {
        'driver': 'postgresql',
        'host': 'localhost',
        'port': 5432,
        'database': 'agno_db',
        'username': 'postgres',
        'password': 'password'
    }
    
    # Para SQLite
    # DATABASE = {
    #     'driver': 'sqlite',
    #     'database': 'db.sqlite3'
    # }
```

### Definición de Modelos

```python
# app/models/user.py
from agno.orm import Model, Field
from datetime import datetime

class User(Model):
    __tablename__ = 'users'
    
    id = Field.Integer(primary_key=True)
    username = Field.String(50, unique=True, nullable=False)
    email = Field.String(120, unique=True, nullable=False)
    password_hash = Field.String(128)
    first_name = Field.String(50)
    last_name = Field.String(50)
    is_active = Field.Boolean(default=True)
    created_at = Field.DateTime(default=datetime.utcnow)
    updated_at = Field.DateTime(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    posts = Field.Relationship('Post', back_populates='author')
    profile = Field.Relationship('Profile', back_populates='user', uselist=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    async def set_password(self, password: str):
        """Hashear y establecer contraseña"""
        from agno.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    async def check_password(self, password: str) -> bool:
        """Verificar contraseña"""
        from agno.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
```

### Operaciones con Base de Datos

```python
# Crear registros
user = await User.create(
    username='johndoe',
    email='john@example.com',
    first_name='John',
    last_name='Doe'
)
await user.set_password('secretpassword')
await user.save()

# Consultas básicas
# Obtener todos los usuarios
users = await User.all()

# Obtener por ID
user = await User.get(1)
user = await User.get_or_404(1)  # Lanza 404 si no existe

# Filtrar registros
active_users = await User.filter(is_active=True)
john_users = await User.filter(first_name='John')

# Consultas complejas
from agno.orm import Q

# OR queries
users = await User.filter(
    Q(first_name='John') | Q(first_name='Jane')
)

# AND queries
users = await User.filter(
    Q(is_active=True) & Q(created_at__gt=datetime(2025, 1, 1))
)

# Ordenamiento
users = await User.order_by('-created_at')  # Descendente
users = await User.order_by('username')     # Ascendente

# Paginación
users = await User.paginate(page=1, per_page=20)

# Actualizar
user = await User.get(1)
user.email = 'newemail@example.com'
await user.save()

# O actualizar directamente
await User.filter(id=1).update(email='newemail@example.com')

# Eliminar
user = await User.get(1)
await user.delete()

# O eliminar directamente
await User.filter(is_active=False).delete()
```

### Migraciones

```bash
# Crear una nueva migración
agno db migrate --create "add_users_table"

# Ejecutar migraciones pendientes
agno db upgrade

# Revertir última migración
agno db downgrade

# Ver estado de migraciones
agno db status
```

## 7. Vistas y Plantillas

### Configuración del Motor de Plantillas

```python
# app/config.py
class Config:
    TEMPLATE_ENGINE = 'jinja2'
    TEMPLATE_FOLDER = 'app/views'
    TEMPLATE_AUTO_RELOAD = True
```

### Plantilla Base

```html
<!-- app/views/base.html -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mi App Agno{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="{{ url_for('home') }}" class="brand">Mi App</a>
            <ul class="nav-links">
                <li><a href="{{ url_for('home') }}">Inicio</a></li>
                {% if current_user.is_authenticated %}
                    <li><a href="{{ url_for('profile') }}">Perfil</a></li>
                    <li><a href="{{ url_for('logout') }}">Salir</a></li>
                {% else %}
                    <li><a href="{{ url_for('login') }}">Iniciar Sesión</a></li>
                    <li><a href="{{ url_for('register') }}">Registrarse</a></li>
                {% endif %}
            </ul>
        </div>
    </nav>
    
    <main class="content">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </main>
    
    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 Mi App Agno. Todos los derechos reservados.</p>
        </div>
    </footer>
    
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Plantillas de Contenido

```html
<!-- app/views/users/index.html -->
{% extends "base.html" %}

{% block title %}Usuarios - {{ super() }}{% endblock %}

{% block content %}
<div class="container">
    <h1>Lista de Usuarios</h1>
    
    <div class="toolbar">
        <a href="{{ url_for('users.create') }}" class="btn btn-primary">Nuevo Usuario</a>
    </div>
    
    <table class="table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Usuario</th>
                <th>Email</th>
                <th>Estado</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            {% for user in users %}
            <tr>
                <td>{{ user.id }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>
                    {% if user.is_active %}
                        <span class="badge badge-success">Activo</span>
                    {% else %}
                        <span class="badge badge-danger">Inactivo</span>
                    {% endif %}
                </td>
                <td>
                    <a href="{{ url_for('users.show', user_id=user.id) }}" class="btn btn-sm btn-info">Ver</a>
                    <a href="{{ url_for('users.edit', user_id=user.id) }}" class="btn btn-sm btn-warning">Editar</a>
                    <form action="{{ url_for('users.delete', user_id=user.id) }}" method="POST" style="display: inline;">
                        {{ csrf_token() }}
                        <button type="submit" class="btn btn-sm btn-danger" onclick="return confirm('¿Estás seguro?')">Eliminar</button>
                    </form>
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="5" class="text-center">No hay usuarios registrados</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    {% if pagination %}
    <div class="pagination">
        {% if pagination.has_prev %}
            <a href="{{ url_for('users.index', page=pagination.prev_num) }}">« Anterior</a>
        {% endif %}
        
        {% for page_num in pagination.iter_pages() %}
            {% if page_num %}
                {% if page_num != pagination.page %}
                    <a href="{{ url_for('users.index', page=page_num) }}">{{ page_num }}</a>
                {% else %}
                    <strong>{{ page_num }}</strong>
                {% endif %}
            {% else %}
                ...
            {% endif %}
        {% endfor %}
        
        {% if pagination.has_next %}
            <a href="{{ url_for('users.index', page=pagination.next_num) }}">Siguiente »</a>
        {% endif %}
    </div>
    {% endif %}
</div>
{% endblock %}
```

### Renderizar Plantillas desde Controladores

```python
from agno import Controller, Request, Response

class UserController(Controller):
    async def index(self, request: Request) -> Response:
        users = await User.paginate(
            page=request.args.get('page', 1, type=int),
            per_page=20
        )
        
        return self.render('users/index.html', {
            'users': users.items,
            'pagination': users
        })
    
    async def show(self, request: Request, user_id: int) -> Response:
        user = await User.get_or_404(user_id)
        posts = await user.posts.limit(10)
        
        return self.render('users/show.html', {
            'user': user,
            'posts': posts
        })
```

## 8. Middleware

### Crear Middleware Personalizado

```python
# app/middleware/auth.py
from agno import Middleware, Request, Response
from functools import wraps

class AuthMiddleware(Middleware):
    async def process_request(self, request: Request) -> Optional[Response]:
        """Ejecutado antes de procesar la solicitud"""
        # Verificar token de autenticación
        token = request.headers.get('Authorization')
        
        if not token:
            return JsonResponse({'error': 'Token no proporcionado'}, status=401)
        
        try:
            # Verificar y decodificar token
            user = await verify_token(token)
            request.user = user
        except InvalidTokenError:
            return JsonResponse({'error': 'Token inválido'}, status=401)
        
        # Continuar con la solicitud
        return None
    
    async def process_response(self, request: Request, response: Response) -> Response:
        """Ejecutado después de procesar la solicitud"""
        # Agregar headers de seguridad
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        return response

# Middleware de logging
class LoggingMiddleware(Middleware):
    async def process_request(self, request: Request) -> None:
        """Registrar solicitud entrante"""
        import logging
        logger = logging.getLogger('agno.requests')
        logger.info(f"{request.method} {request.path} - {request.remote_addr}")
        request.start_time = time.time()
    
    async def process_response(self, request: Request, response: Response) -> Response:
        """Registrar respuesta"""
        duration = time.time() - request.start_time
        logger.info(f"{request.method} {request.path} - {response.status_code} - {duration:.3f}s")
        return response

# Middleware de CORS
class CORSMiddleware(Middleware):
    def __init__(self, allowed_origins=['*'], allowed_methods=['GET', 'POST', 'PUT', 'DELETE']):
        self.allowed_origins = allowed_origins
        self.allowed_methods = allowed_methods
    
    async def process_response(self, request: Request, response: Response) -> Response:
        origin = request.headers.get('Origin', '*')
        
        if '*' in self.allowed_origins or origin in self.allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Methods'] = ', '.join(self.allowed_methods)
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        return response
```

### Registrar Middleware

```python
# main.py
from agno import Agno
from app.middleware import AuthMiddleware, LoggingMiddleware, CORSMiddleware

app = Agno()

# Registrar middleware global
app.add_middleware(LoggingMiddleware())
app.add_middleware(CORSMiddleware(allowed_origins=['https://example.com']))

# Middleware para rutas específicas
@app.route('/api/protected')
@app.middleware(AuthMiddleware())
async def protected_route(request: Request) -> Response:
    return JsonResponse({'message': f'Hola {request.user.username}'})
```

### Decorador de Middleware

```python
# Crear decorador personalizado
def require_auth(f):
    @wraps(f)
    async def decorated_function(request: Request, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user:
            return JsonResponse({'error': 'Autenticación requerida'}, status=401)
        return await f(request, *args, **kwargs)
    return decorated_function

# Usar el decorador
@app.route('/profile')
@require_auth
async def profile(request: Request) -> Response:
    return JsonResponse({'user': request.user.to_dict()})
```

## 9. Autenticación y Autorización

### Sistema de Autenticación

```python
# app/auth.py
from agno import Request, Response, JsonResponse
from agno.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

class AuthService:
    def __init__(self, app):
        self.app = app
        self.secret_key = app.config.SECRET_KEY
        self.token_expiration = timedelta(hours=24)
    
    async def register(self, request: Request) -> Response:
        """Registrar nuevo usuario"""
        data = await request.json()
        
        # Validar datos
        if not all(k in data for k in ['username', 'email', 'password']):
            return JsonResponse({'error': 'Datos incompletos'}, status=400)
        
        # Verificar si el usuario existe
        existing_user = await User.filter(
            Q(username=data['username']) | Q(email=data['email'])
        ).first()
        
        if existing_user:
            return JsonResponse({'error': 'Usuario ya existe'}, status=409)
        
        # Crear usuario
        user = await User.create(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password'])
        )
        
        # Generar token
        token = self.generate_token(user)
        
        return JsonResponse({
            'user': user.to_dict(),
            'token': token
        }, status=201)
    
    async def login(self, request: Request) -> Response:
        """Iniciar sesión"""
        data = await request.json()
        
        # Buscar usuario
        user = await User.filter(username=data.get('username')).first()
        
        if not user or not check_password_hash(user.password_hash, data.get('password')):
            return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
        
        # Generar token
        token = self.generate_token(user)
        
        return JsonResponse({
            'user': user.to_dict(),
            'token': token
        })
    
    def generate_token(self, user) -> str:
        """Generar JWT token"""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + self.token_expiration,
            'iat': datetime.utcnow()
        }
        
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    async def verify_token(self, token: str) -> User:
        """Verificar y decodificar token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            user = await User.get(payload['user_id'])
            if not user:
                raise ValueError('Usuario no encontrado')
            return user
        except jwt.ExpiredSignatureError:
            raise ValueError('Token expirado')
        except jwt.InvalidTokenError:
            raise ValueError('Token inválido')
```

### Sistema de Roles y Permisos

```python
# app/models/role.py
class Role(Model):
    __tablename__ = 'roles'
    
    id = Field.Integer(primary_key=True)
    name = Field.String(50, unique=True, nullable=False)
    description = Field.String(200)
    permissions = Field.Relationship('Permission', secondary='role_permissions')
    users = Field.Relationship('User', secondary='user_roles', back_populates='roles')

class Permission(Model):
    __tablename__ = 'permissions'
    
    id = Field.Integer(primary_key=True)
    name = Field.String(50, unique=True, nullable=False)
    resource = Field.String(50)
    action = Field.String(50)
    roles = Field.Relationship('Role', secondary='role_permissions', back_populates='permissions')

# Decorador para verificar permisos
def require_permission(permission_name):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            if not hasattr(request, 'user'):
                return JsonResponse({'error': 'Autenticación requerida'}, status=401)
            
            # Verificar si el usuario tiene el permiso
            has_permission = await request.user.has_permission(permission_name)
            
            if not has_permission:
                return JsonResponse({'error': 'Permiso denegado'}, status=403)
            
            return await f(request, *args, **kwargs)
        return decorated_function
    return decorator

# Usar el decorador
@app.route('/admin/users')
@require_permission('admin.users.view')
async def admin_users(request: Request) -> Response:
    users = await User.all()
    return JsonResponse({'users': [u.to_dict() for u in users]})
```

## 10. API REST

### Crear una API RESTful

```python
# app/api/v1/resources.py
from agno import Blueprint, Request, Response, JsonResponse
from agno.decorators import validate_json

api_v1 = Blueprint('api_v1', url_prefix='/api/v1')

# Esquemas de validación
USER_SCHEMA = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string', 'minLength': 3, 'maxLength': 50},
        'email': {'type': 'string', 'format': 'email'},
        'password': {'type': 'string', 'minLength': 8}
    },
    'required': ['username', 'email', 'password']
}

@api_v1.route('/users', methods=['GET'])
async def get_users(request: Request) -> Response:
    """Obtener lista de usuarios con paginación y filtros"""
    # Parámetros de consulta
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    # Construir consulta
    query = User.query()
    if search:
        query = query.filter(
            Q(username__icontains=search) | Q(email__icontains=search)
        )
    
    # Paginar resultados
    pagination = await query.paginate(page=page, per_page=per_page)
    
    return JsonResponse({
        'users': [user.to_dict() for user in pagination.items],
        'pagination': {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next
        }
    })

@api_v1.route('/users/<int:user_id>', methods=['GET'])
async def get_user(request: Request, user_id: int) -> Response:
    """Obtener un usuario específico"""
    user = await User.get_or_404(user_id)
    return JsonResponse({'user': user.to_dict()})

@api_v1.route('/users', methods=['POST'])
@validate_json(USER_SCHEMA)
async def create_user(request: Request) -> Response:
    """Crear un nuevo usuario"""
    data = await request.json()
    
    # Verificar duplicados
    existing = await User.filter(
        Q(username=data['username']) | Q(email=data['email'])
    ).first()
    
    if existing:
        return JsonResponse(
            {'error': 'Usuario ya existe'},
            status=409
        )
    
    # Crear usuario
    user = await User.create(**data)
    
    return JsonResponse(
        {'user': user.to_dict()},
        status=201,
        headers={'Location': f'/api/v1/users/{user.id}'}
    )

@api_v1.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
async def update_user(request: Request, user_id: int) -> Response:
    """Actualizar un usuario"""
    user = await User.get_or_404(user_id)
    data = await request.json()
    
    # Actualizar campos
    for field, value in data.items():
        if hasattr(user, field) and field not in ['id', 'created_at']:
            setattr(user, field, value)
    
    await user.save()
    
    return JsonResponse({'user': user.to_dict()})

@api_v1.route('/users/<int:user_id>', methods=['DELETE'])
async def delete_user(request: Request, user_id: int) -> Response:
    """Eliminar un usuario"""
    user = await User.get_or_404(user_id)
    await user.delete()
    
    return Response(status=204)

# Registrar blueprint
app.register_blueprint(api_v1)
```

### Versionado de API

```python
# app/api/__init__.py
from agno import Blueprint

# Versión 1
from .v1 import api_v1

# Versión 2 (con cambios incompatibles)
api_v2 = Blueprint('api_v2', url_prefix='/api/v2')

@api_v2.route('/users', methods=['GET'])
async def get_users_v2(request: Request) -> Response:
    """API v2 con estructura de respuesta diferente"""
    users = await User.all()
    
    return JsonResponse({
        'data': [user.to_dict() for user in users],
        'meta': {
            'version': '2.0',
            'timestamp': datetime.utcnow().isoformat()
        }
    })

# Registrar ambas versiones
app.register_blueprint(api_v1)
app.register_blueprint(api_v2)
```

### Documentación de API con OpenAPI/Swagger

```python
# app/api/docs.py
from agno import Agno
from agno.openapi import OpenAPI

app = Agno()
openapi = OpenAPI(app, title="Mi API", version="1.0.0")

@app.route('/api/users', methods=['GET'])
@openapi.document(
    summary="Listar usuarios",
    description="Obtiene una lista paginada de usuarios",
    tags=["users"],
    parameters=[
        {
            "name": "page",
            "in": "query",
            "type": "integer",
            "default": 1,
            "description": "Número de página"
        },
        {
            "name": "per_page",
            "in": "query",
            "type": "integer",
            "default": 20,
            "description": "Elementos por página"
        }
    ],
    responses={
        200: {
            "description": "Lista de usuarios",
            "schema": {
                "type": "object",
                "properties": {
                    "users": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/User"}
                    }
                }
            }
        }
    }
)
async def get_users(request: Request) -> Response:
    # Implementación...
    pass

# Servir documentación Swagger UI
@app.route('/api/docs')
async def api_docs(request: Request) -> Response:
    return openapi.swagger_ui()
```

## 11. Mejores Prácticas

### Estructura de Proyecto Escalable

```
mi-proyecto/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── products.py
│   │   └── v2/
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── web/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   └── product.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── email_service.py
│   │   └── cache_service.py
│   ├── middleware/
│   ├── utils/
│   ├── validators/
│   └── config/
│       ├── __init__.py
│       ├── base.py
│       ├── development.py
│       ├── production.py
│       └── testing.py
├── migrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── static/
├── templates/
├── scripts/
├── docker/
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── docker-compose.yml
└── README.md
```

### Configuración por Entornos

```python
# app/config/base.py
import os
from pathlib import Path

class Config:
    """Configuración base"""
    BASE_DIR = Path(__file__).parent.parent.parent
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Base de datos
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Cache
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# app/config/development.py
from .base import Config

class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    TESTING = False
    DATABASE_URL = 'postgresql://user:pass@localhost/devdb'
    LOG_LEVEL = 'DEBUG'

# app/config/production.py
from .base import Config

class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    TESTING = False
    # Usar variables de entorno en producción
    assert os.environ.get('SECRET_KEY'), 'SECRET_KEY debe estar configurado'
    assert os.environ.get('DATABASE_URL'), 'DATABASE_URL debe estar configurado'
```

### Manejo de Errores

```python
# app/errors.py
from agno import Request, Response, JsonResponse

class ErrorHandler:
    @staticmethod
    async def handle_404(request: Request, exc: Exception) -> Response:
        """Manejar errores 404"""
        if request.path.startswith('/api/'):
            return JsonResponse(
                {'error': 'Recurso no encontrado'},
                status=404
            )
        return render_template('errors/404.html'), 404
    
    @staticmethod
    async def handle_500(request: Request, exc: Exception) -> Response:
        """Manejar errores 500"""
        # Log del error
        import logging
        logging.error(f"Error interno: {exc}", exc_info=True)
        
        if request.path.startswith('/api/'):
            return JsonResponse(
                {'error': 'Error interno del servidor'},
                status=500
            )
        return render_template('errors/500.html'), 500

# Registrar manejadores
app.error_handler(404)(ErrorHandler.handle_404)
app.error_handler(500)(ErrorHandler.handle_500)
```

### Testing

```python
# tests/conftest.py
import pytest
from agno import Agno
from app import create_app
from app.models import db

@pytest.fixture
async def app():
    """Crear aplicación de prueba"""
    app = create_app('testing')
    async with app.app_context():
        await db.create_all()
        yield app
        await db.drop_all()

@pytest.fixture
async def client(app):
    """Cliente de prueba"""
    return app.test_client()

# tests/unit/test_models.py
import pytest
from app.models import User

@pytest.mark.asyncio
async def test_user_creation():
    """Test crear usuario"""
    user = await User.create(
        username='testuser',
        email='test@example.com'
    )
    
    assert user.id is not None
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'

# tests/integration/test_api.py
@pytest.mark.asyncio
async def test_get_users(client):
    """Test endpoint GET /api/users"""
    response = await client.get('/api/v1/users')
    
    assert response.status_code == 200
    data = await response.json()
    assert 'users' in data
    assert isinstance(data['users'], list)
```

### Optimización de Rendimiento

```python
# Caché con Redis
from agno.cache import cache

@app.route('/api/products')
@cache.cached(timeout=300)  # Cache por 5 minutos
async def get_products(request: Request) -> Response:
    products = await Product.all()
    return JsonResponse({'products': [p.to_dict() for p in products]})

# Lazy loading de relaciones
user = await User.get(1)
# Solo carga los posts cuando se acceden
posts = await user.posts.all()

# Eager loading para evitar N+1 queries
users = await User.with_('posts', 'profile').all()

# Consultas optimizadas
users = await User.select('id', 'username', 'email').where(is_active=True).all()

# Índices en base de datos
class User(Model):
    username = Field.String(50, index=True)
    email = Field.String(120, unique=True, index=True)
    
    class Meta:
        indexes = [
            Index('idx_user_email_active', 'email', 'is_active'),
        ]
```

## 12. Solución de Problemas

### Problemas Comunes y Soluciones

#### 1. Error de Importación de Módulos

```python
# Problema: ModuleNotFoundError: No module named 'app'
# Solución: Asegurarse de que el directorio raíz esté en PYTHONPATH

# En el archivo principal (main.py)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
```

#### 2. Problemas de Conexión a Base de Datos

```python
# Verificar conexión
from app.models import db

async def check_db_connection():
    try:
        await db.execute('SELECT 1')
        print("Conexión a base de datos exitosa")
    except Exception as e:
        print(f"Error de conexión: {e}")
```

#### 3. Problemas de Rendimiento

```python
# Habilitar logging de consultas SQL
import logging
logging.basicConfig()
logging.getLogger('agno.db').setLevel(logging.DEBUG)

# Profiling de rutas
from agno.debug import profile

@app.route('/slow-route')
@profile
async def slow_route(request: Request) -> Response:
    # Código a analizar
    pass
```

### Debugging

```python
# Modo debug
app.run(debug=True)

# Debugger interactivo
import pdb; pdb.set_trace()

# Logging detallado
import logging

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
```

### Herramientas de Desarrollo

```bash
# Linter
pip install flake8
flake8 app/

# Formateo de código
pip install black
black app/

# Type hints
pip install mypy
mypy app/

# Coverage de tests
pip install pytest-cov
pytest --cov=app tests/
```

## Conclusión

Este manual cubre los aspectos fundamentales y avanzados del framework Agno. Para mantenerse actualizado:

1. Consulta la documentación oficial en https://agno.dev
2. Únete a la comunidad en Discord/Slack
3. Sigue el repositorio en GitHub
4. Participa en los foros de discusión

Recuerda que Agno está en constante evolución, por lo que es importante mantenerse al día con las nuevas características y mejores prácticas.

### Recursos Adicionales

- **Documentación oficial**: https://docs.agno.dev
- **Ejemplos de proyectos**: https://github.com/agno-framework/examples
- **Blog de Agno**: https://blog.agno.dev
- **Stack Overflow**: Tag `agno-framework`
- **Videos tutoriales**: YouTube - Agno Framework

¡Feliz desarrollo con Agno! 🚀