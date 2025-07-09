---
applyTo: "**/*.jinja2,**/*.j2,**/*.jinja"
---
# Buenas Prácticas de Jinja2

## 1. **Fundamentos y Sintaxis**

### 1.1 Sintaxis Básica
- Usa delimitadores estándar de Jinja2 consistentemente
- Mantén espacios para legibilidad en expresiones complejas
- Documenta templates complejos con comentarios

```jinja2
{# ✅ Comentarios descriptivos #}
{# Template para mostrar información de usuario #}

{# ✅ Variables #}
{{ variable_name }}
{{ user.name }}
{{ config['database']['host'] }}

{# ✅ Expresiones con espacios para legibilidad #}
{{ (user.first_name + ' ' + user.last_name).title() }}

{# ✅ Statements de control #}
{% if user.is_active %}
{% for item in items %}
{% set variable = value %}

{# ✅ Comentarios multi-línea #}
{#
  Este template maneja la renderización de la página de perfil de usuario.
  Variables requeridas:
  - user: objeto Usuario con campos name, email, is_active
  - permissions: lista de permisos del usuario
#}
```

### 1.2 Espaciado y Formato
```jinja2
{# ✅ Espaciado consistente #}
{% if condition %}
    <div class="content">
        {{ content }}
    </div>
{% endif %}

{# ✅ Control de whitespace #}
{%- if user.is_admin -%}
    <admin-panel></admin-panel>
{%- endif -%}

{# ✅ Múltiples condiciones bien formateadas #}
{% if user.is_active 
   and user.email_verified 
   and user.has_permission('read') %}
    Welcome, {{ user.name }}!
{% endif %}

{# ❌ Evitar formato inconsistente #}
{%if condition%}<div>{{content}}</div>{%endif%}
```

## 2. **Variables y Contexto**

### 2.1 Nomenclatura de Variables
```jinja2
{# ✅ Nombres descriptivos y consistentes #}
{{ user_profile.display_name }}
{{ article.publication_date }}
{{ shopping_cart.total_amount }}

{# ✅ Convención snake_case #}
{{ current_user }}
{{ is_authenticated }}
{{ max_retry_attempts }}

{# ❌ Evitar nombres poco descriptivos #}
{{ u }}  {# user #}
{{ d }}  {# data #}
{{ x }}  {# cualquier cosa #}
```

### 2.2 Verificación de Variables
```jinja2
{# ✅ Verificar existencia antes de usar #}
{% if user is defined and user %}
    Hello, {{ user.name }}!
{% endif %}

{# ✅ Valores por defecto #}
{{ user.name | default('Guest') }}
{{ config.timeout | default(30) }}

{# ✅ Verificar atributos de objetos #}
{% if user and user.profile %}
    {{ user.profile.bio }}
{% endif %}

{# ✅ Usar el operador ternario para casos simples #}
{{ 'Active' if user.is_active else 'Inactive' }}
```

### 2.3 Manejo de Tipos de Datos
```jinja2
{# ✅ Listas #}
{% for item in items %}
    <li>{{ item.name }}</li>
{% else %}
    <li>No items found</li>
{% endfor %}

{# ✅ Diccionarios #}
{% for key, value in config.items() %}
    <dt>{{ key }}</dt>
    <dd>{{ value }}</dd>
{% endfor %}

{# ✅ Verificar tipos #}
{% if items is iterable %}
    {% for item in items %}
        {{ item }}
    {% endfor %}
{% endif %}

{# ✅ Manejo de números #}
{{ price | round(2) }}
{{ percentage | round(1) }}%
{{ count | int }}
```

## 3. **Filtros y Funciones**

### 3.1 Filtros Comunes
```jinja2
{# ✅ Filtros de texto #}
{{ user.name | title }}
{{ content | truncate(100) }}
{{ description | striptags }}
{{ code | indent(4) }}

{# ✅ Filtros de fecha #}
{{ created_at | strftime('%Y-%m-%d') }}
{{ updated_at | strftime('%B %d, %Y at %I:%M %p') }}

{# ✅ Filtros de lista #}
{{ users | length }}
{{ scores | max }}
{{ prices | sum }}
{{ items | sort(attribute='name') }}

{# ✅ Filtros personalizados encadenados #}
{{ article.content | striptags | truncate(200) | title }}
```

### 3.2 Filtros Personalizados
```python
# ✅ Definición de filtros personalizados en Python
from jinja2 import Environment

def format_currency(amount, currency='USD'):
    """Formato de moneda personalizado."""
    if currency == 'USD':
        return f"${amount:,.2f}"
    elif currency == 'EUR':
        return f"€{amount:,.2f}"
    return f"{amount:,.2f} {currency}"

def slugify(text):
    """Convierte texto a slug URL-friendly."""
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

# Registrar filtros
env = Environment()
env.filters['currency'] = format_currency
env.filters['slugify'] = slugify
```

```jinja2
{# ✅ Uso de filtros personalizados #}
{{ product.price | currency('EUR') }}
{{ article.title | slugify }}
```

### 3.3 Tests (Funciones de Prueba)
```jinja2
{# ✅ Tests incorporados #}
{% if user.email is email %}
    <span class="valid-email">{{ user.email }}</span>
{% endif %}

{% if value is number %}
    {{ value | round(2) }}
{% endif %}

{% if items is empty %}
    <p>No items to display</p>
{% endif %}

{# ✅ Tests personalizados #}
{% if user is admin %}
    <admin-menu></admin-menu>
{% endif %}
```

## 4. **Estructuras de Control**

### 4.1 Condicionales
```jinja2
{# ✅ If/elif/else bien estructurado #}
{% if user.role == 'admin' %}
    <div class="admin-panel">
        <h2>Admin Dashboard</h2>
        {% include 'admin/dashboard.html' %}
    </div>
{% elif user.role == 'moderator' %}
    <div class="moderator-panel">
        <h2>Moderator Tools</h2>
        {% include 'moderator/tools.html' %}
    </div>
{% else %}
    <div class="user-panel">
        <h2>User Dashboard</h2>
        {% include 'user/dashboard.html' %}
    </div>
{% endif %}

{# ✅ Condiciones complejas #}
{% if user.is_authenticated 
   and user.has_permission('view_content') 
   and not user.is_suspended %}
    {{ content }}
{% endif %}
```

### 4.2 Bucles
```jinja2
{# ✅ Bucle for con información de loop #}
<ul class="user-list">
{% for user in users %}
    <li class="user-item {{ 'first' if loop.first }} {{ 'last' if loop.last }}">
        <span class="user-number">{{ loop.index }}</span>
        <span class="user-name">{{ user.name }}</span>
        {% if not loop.last %}
            <hr class="separator">
        {% endif %}
    </li>
{% else %}
    <li class="no-users">No users found</li>
{% endfor %}
</ul>

{# ✅ Bucles anidados con nombres de loop #}
{% for category in categories %}
    <div class="category">
        <h3>{{ category.name }}</h3>
        {% for product in category.products %}
            {%- set outer_loop = loop -%}
            <div class="product" data-category-index="{{ outer_loop.index0 }}">
                <h4>{{ product.name }}</h4>
                <p>Product {{ loop.index }} of {{ loop.length }}</p>
            </div>
        {% endfor %}
    </div>
{% endfor %}

{# ✅ Control de bucle #}
{% for item in large_list %}
    {% if loop.index > 10 %}
        {% break %}
    {% endif %}
    {{ item }}
{% endfor %}
```

### 4.3 Asignaciones de Variables
```jinja2
{# ✅ Variables simples #}
{% set page_title = "User Profile - " + user.name %}
{% set is_owner = current_user.id == profile_user.id %}

{# ✅ Variables complejas #}
{% set user_permissions = user.get_permissions() | list %}
{% set formatted_date = created_at | strftime('%B %d, %Y') %}

{# ✅ Variables de bloque #}
{% set navigation %}
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        {% if user.is_authenticated %}
            <a href="/profile">Profile</a>
        {% endif %}
    </nav>
{% endset %}

{{ navigation }}
```

## 5. **Templates y Herencia**

### 5.1 Template Base
```jinja2
{# ✅ base.html - Template base bien estructurado #}
<!DOCTYPE html>
<html lang="{{ language | default('en') }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>{% block title %}{{ site_name }}{% endblock %}</title>
    
    {% block meta %}
        <meta name="description" content="{% block description %}{{ site_description }}{% endblock %}">
        <meta name="keywords" content="{% block keywords %}{{ site_keywords }}{% endblock %}">
    {% endblock %}
    
    {# CSS base #}
    <link rel="stylesheet" href="{{ url_for('static', filename='css/base.css') }}">
    {% block extra_css %}{% endblock %}
    
    {# JavaScript head #}
    {% block head_js %}{% endblock %}
</head>
<body class="{% block body_class %}{% endblock %}">
    {# Header #}
    <header class="main-header">
        {% block header %}
            {% include 'partials/navigation.html' %}
        {% endblock %}
    </header>
    
    {# Main content #}
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>
    
    {# Footer #}
    <footer class="main-footer">
        {% block footer %}
            {% include 'partials/footer.html' %}
        {% endblock %}
    </footer>
    
    {# JavaScript bottom #}
    <script src="{{ url_for('static', filename='js/base.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 5.2 Templates Hijos
```jinja2
{# ✅ user_profile.html - Template hijo #}
{% extends "base.html" %}

{% block title %}{{ user.name }} - User Profile{% endblock %}

{% block description %}Profile page for {{ user.name }}{% endblock %}

{% block body_class %}profile-page{% endblock %}

{% block extra_css %}
    <link rel="stylesheet" href="{{ url_for('static', filename='css/profile.css') }}">
{% endblock %}

{% block content %}
<div class="profile-container">
    <div class="profile-header">
        <img src="{{ user.avatar_url | default('/static/img/default-avatar.png') }}" 
             alt="{{ user.name }}'s avatar" 
             class="profile-avatar">
        <h1 class="profile-name">{{ user.name }}</h1>
        <p class="profile-bio">{{ user.bio | default('No bio available') }}</p>
    </div>
    
    <div class="profile-content">
        {% block profile_content %}
            {# Contenido específico del perfil #}
        {% endblock %}
    </div>
</div>
{% endblock %}

{% block extra_js %}
    <script src="{{ url_for('static', filename='js/profile.js') }}"></script>
{% endblock %}
```

### 5.3 Includes y Partials
```jinja2
{# ✅ partials/user_card.html #}
<div class="user-card" data-user-id="{{ user.id }}">
    <div class="user-avatar">
        <img src="{{ user.avatar_url | default('/static/img/default-avatar.png') }}" 
             alt="{{ user.name }}">
    </div>
    <div class="user-info">
        <h3 class="user-name">{{ user.name }}</h3>
        <p class="user-role">{{ user.role | title }}</p>
        {% if user.last_login %}
            <p class="user-last-seen">
                Last seen: {{ user.last_login | strftime('%B %d, %Y') }}
            </p>
        {% endif %}
    </div>
    {% if show_actions | default(false) %}
        <div class="user-actions">
            <a href="{{ url_for('user.profile', user_id=user.id) }}" 
               class="btn btn-sm btn-primary">View Profile</a>
        </div>
    {% endif %}
</div>

{# ✅ Uso del partial #}
<div class="users-grid">
{% for user in users %}
    {% include 'partials/user_card.html' with context %}
{% endfor %}
</div>

{# ✅ Include con variables específicas #}
{% include 'partials/user_card.html' with context 
   user=current_user, show_actions=true %}
```

## 6. **Macros y Funciones Reutilizables**

### 6.1 Macros Básicos
```jinja2
{# ✅ macros/forms.html #}
{% macro input(name, label, type='text', value='', required=false, placeholder='') %}
<div class="form-group">
    <label for="{{ name }}" class="form-label">
        {{ label }}
        {% if required %}<span class="required">*</span>{% endif %}
    </label>
    <input type="{{ type }}" 
           id="{{ name }}" 
           name="{{ name }}" 
           value="{{ value }}" 
           class="form-control"
           {% if placeholder %}placeholder="{{ placeholder }}"{% endif %}
           {% if required %}required{% endif %}>
</div>
{% endmacro %}

{% macro button(text, type='button', class='btn-primary', disabled=false) %}
<button type="{{ type }}" 
        class="btn {{ class }}"
        {% if disabled %}disabled{% endif %}>
    {{ text }}
</button>
{% endmacro %}

{% macro alert(message, type='info', dismissible=true) %}
<div class="alert alert-{{ type }}{% if dismissible %} alert-dismissible{% endif %}">
    {{ message }}
    {% if dismissible %}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    {% endif %}
</div>
{% endmacro %}
```

### 6.2 Macros Avanzados
```jinja2
{# ✅ macros/pagination.html #}
{% macro pagination(pagination_obj, endpoint, **kwargs) %}
{% if pagination_obj.pages > 1 %}
<nav aria-label="Page navigation">
    <ul class="pagination">
        {# Previous page #}
        <li class="page-item {{ 'disabled' if not pagination_obj.has_prev }}">
            {% if pagination_obj.has_prev %}
                <a class="page-link" 
                   href="{{ url_for(endpoint, page=pagination_obj.prev_num, **kwargs) }}">
                    Previous
                </a>
            {% else %}
                <span class="page-link">Previous</span>
            {% endif %}
        </li>
        
        {# Page numbers #}
        {% for page_num in pagination_obj.iter_pages() %}
            {% if page_num %}
                {% if page_num != pagination_obj.page %}
                    <li class="page-item">
                        <a class="page-link" 
                           href="{{ url_for(endpoint, page=page_num, **kwargs) }}">
                            {{ page_num }}
                        </a>
                    </li>
                {% else %}
                    <li class="page-item active">
                        <span class="page-link">{{ page_num }}</span>
                    </li>
                {% endif %}
            {% else %}
                <li class="page-item disabled">
                    <span class="page-link">...</span>
                </li>
            {% endif %}
        {% endfor %}
        
        {# Next page #}
        <li class="page-item {{ 'disabled' if not pagination_obj.has_next }}">
            {% if pagination_obj.has_next %}
                <a class="page-link" 
                   href="{{ url_for(endpoint, page=pagination_obj.next_num, **kwargs) }}">
                    Next
                </a>
            {% else %}
                <span class="page-link">Next</span>
            {% endif %}
        </li>
    </ul>
</nav>
{% endif %}
{% endmacro %}
```

### 6.3 Uso de Macros
```jinja2
{# ✅ user_form.html #}
{% from 'macros/forms.html' import input, button, alert %}

<form method="post" action="{{ url_for('user.update_profile') }}">
    {{ csrf_token() }}
    
    {% if messages %}
        {% for message in messages %}
            {{ alert(message.text, message.type) }}
        {% endfor %}
    {% endif %}
    
    {{ input('first_name', 'First Name', value=user.first_name, required=true) }}
    {{ input('last_name', 'Last Name', value=user.last_name, required=true) }}
    {{ input('email', 'Email', type='email', value=user.email, required=true) }}
    {{ input('phone', 'Phone Number', type='tel', value=user.phone) }}
    
    <div class="form-actions">
        {{ button('Save Changes', type='submit') }}
        {{ button('Cancel', type='button', class='btn-secondary') }}
    </div>
</form>
```

## 7. **Seguridad**

### 7.1 Escape de HTML
```jinja2
{# ✅ Escape automático (por defecto en la mayoría de configuraciones) #}
{{ user.bio }}  {# Se escapa automáticamente #}

{# ✅ HTML seguro explícito #}
{{ user.bio | escape }}

{# ✅ HTML confiable (solo cuando es seguro) #}
{{ trusted_html_content | safe }}

{# ✅ Filtro striptags para contenido de usuario #}
{{ user.comment | striptags }}

{# ❌ Evitar raw HTML sin validación #}
{{ user_input | safe }}  {# PELIGROSO si user_input no es confiable #}
```

### 7.2 Protección CSRF
```jinja2
{# ✅ Token CSRF en formularios #}
<form method="post" action="{{ url_for('user.update') }}">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    {# o usando macro si está disponible #}
    {{ csrf_token() }}
    
    {# resto del formulario #}
</form>

{# ✅ CSRF en AJAX requests #}
<script>
    const csrfToken = "{{ csrf_token() }}";
    
    fetch('/api/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data)
    });
</script>
```

### 7.3 Validación de URLs
```jinja2
{# ✅ URLs seguras #}
<a href="{{ url_for('user.profile', user_id=user.id) }}">Profile</a>

{# ✅ URLs externas con validación #}
{% if external_url and external_url.startswith(('http://', 'https://')) %}
    <a href="{{ external_url }}" rel="noopener noreferrer" target="_blank">
        External Link
    </a>
{% endif %}

{# ❌ Evitar URLs sin validar #}
<a href="{{ user.website }}">Website</a>  {# Potencialmente peligroso #}
```

## 8. **Internacionalización (i18n)**

### 8.1 Mensajes Traducibles
```jinja2
{# ✅ Textos simples #}
<h1>{{ _('Welcome to our website') }}</h1>
<p>{{ _('Please log in to continue') }}</p>

{# ✅ Textos con variables #}
<p>{{ _('Hello, %(name)s!', name=user.name) }}</p>
<p>{{ _('You have %(count)d new messages', count=message_count) }}</p>

{# ✅ Pluralización #}
<p>
    {{ ngettext(
        'You have %(num)d item in your cart',
        'You have %(num)d items in your cart',
        cart_items|length,
        num=cart_items|length
    ) }}
</p>

{# ✅ Contexto para desambiguación #}
<button>{{ _('Close', context='button') }}</button>
<p>{{ _('Close', context='adjective') }} relationship</p>
```

### 8.2 Fechas y Números Localizados
```jinja2
{# ✅ Fechas localizadas #}
{{ moment(created_at).format('LLLL') }}
{{ created_at | strftime(_('%B %d, %Y')) }}

{# ✅ Números y monedas #}
{{ price | currency }}
{{ percentage | percent }}
{{ large_number | number }}

{# ✅ Direccionalidad de texto #}
<html lang="{{ get_locale() }}" dir="{{ 'rtl' if is_rtl_language() else 'ltr' }}">
```

## 9. **Performance y Optimización**

### 9.1 Caching de Templates
```python
# ✅ Configuración de cache en Python
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml']),
    cache_size=1000,  # Cache de templates compilados
    auto_reload=False,  # False en producción
)
```

### 9.2 Optimización de Bucles
```jinja2
{# ✅ Verificar antes de iterar #}
{% if users %}
    <ul class="user-list">
    {% for user in users %}
        <li>{{ user.name }}</li>
    {% endfor %}
    </ul>
{% else %}
    <p>No users found</p>
{% endif %}

{# ✅ Limitar iteraciones grandes #}
{% for item in large_list[:100] %}
    {{ item }}
{% endfor %}

{# ✅ Usar batch para procesar en grupos #}
<div class="row">
{% for batch in items | batch(3) %}
    {% for item in batch %}
        <div class="col-md-4">{{ item.name }}</div>
    {% endfor %}
{% endfor %}
</div>
```

### 9.3 Lazy Loading y Includes Condicionales
```jinja2
{# ✅ Includes condicionales #}
{% if user.is_premium %}
    {% include 'premium/features.html' %}
{% endif %}

{# ✅ Lazy loading de componentes pesados #}
<div class="charts-container" data-lazy-load="/api/charts">
    <div class="loading">Loading charts...</div>
</div>

{# ✅ Fragmentos opcionales #}
{% if show_analytics | default(false) %}
    {% include 'analytics/tracking.html' %}
{% endif %}
```

## 10. **Testing y Debugging**

### 10.1 Templates de Debug
```jinja2
{# ✅ Debug template #}
{% if config.DEBUG %}
<div class="debug-panel">
    <h3>Debug Information</h3>
    <ul>
        <li><strong>Template:</strong> {{ self._module.__name__ }}</li>
        <li><strong>User:</strong> {{ current_user.id if current_user.is_authenticated else 'Anonymous' }}</li>
        <li><strong>Request:</strong> {{ request.method }} {{ request.path }}</li>
    </ul>
    
    <h4>Context Variables:</h4>
    <pre>{{ context | pprint }}</pre>
</div>
{% endif %}

{# ✅ Debug de variables específicas #}
{% if config.DEBUG %}
    <!-- Debug: user = {{ user | pprint }} -->
    <!-- Debug: permissions = {{ permissions | pprint }} -->
{% endif %}
```

### 10.2 Manejo de Errores
```jinja2
{# ✅ Manejo de errores en templates #}
{% try %}
    {{ user.profile.advanced_settings.custom_field }}
{% except %}
    {{ 'N/A' }}
{% endtry %}

{# ✅ Verificaciones defensivas #}
{% if user and user.profile and hasattr(user.profile, 'bio') %}
    {{ user.profile.bio }}
{% else %}
    <em>No bio available</em>
{% endif %}

{# ✅ Fallbacks para datos faltantes #}
{% set profile_image = user.profile.image if user.profile else '/static/img/default-profile.png' %}
<img src="{{ profile_image }}" alt="Profile">
```

## 11. **Organización de Archivos**

### 11.1 Estructura de Directorios
```
templates/
├── base.html
├── errors/
│   ├── 404.html
│   ├── 500.html
│   └── base_error.html
├── auth/
│   ├── login.html
│   ├── register.html
│   └── reset_password.html
├── user/
│   ├── profile.html
│   ├── settings.html
│   └── dashboard.html
├── partials/
│   ├── navigation.html
│   ├── footer.html
│   ├── sidebar.html
│   └── user_card.html
├── macros/
│   ├── forms.html
│   ├── pagination.html
│   └── utils.html
├── emails/
│   ├── base_email.html
│   ├── welcome.html
│   └── password_reset.html
└── admin/
    ├── base_admin.html
    ├── dashboard.html
    └── users.html
```

### 11.2 Convenciones de Nombres
```jinja2
{# ✅ Nombres descriptivos de archivos #}
user_profile_edit.html
product_listing_grid.html
checkout_payment_form.html

{# ✅ Prefijos para tipos específicos #}
email_welcome.html
partial_user_card.html
macro_form_helpers.html

{# ✅ Sufijos para variaciones #}
user_profile_mobile.html
product_card_compact.html
```

## 12. **Configuración del Entorno**

### 12.1 Configuración de Jinja2
```python
# ✅ Configuración completa de Jinja2
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

def create_jinja_env():
    """Crear y configurar el entorno Jinja2."""
    
    # Configurar loader
    template_dirs = [
        'templates',
        'themes/current/templates'  # Soporte para temas
    ]
    
    env = Environment(
        loader=FileSystemLoader(template_dirs),
        autoescape=select_autoescape(['html', 'xml', 'j2']),
        trim_blocks=True,
        lstrip_blocks=True,
        cache_size=1000 if not os.getenv('DEBUG') else 0,
        auto_reload=bool(os.getenv('DEBUG')),
        optimized=not bool(os.getenv('DEBUG')),
    )
    
    # Registrar filtros personalizados
    env.filters.update({
        'currency': format_currency,
        'slugify': slugify,
        'markdown': render_markdown,
        'time_ago': time_ago,
    })
    
    # Registrar tests personalizados
    env.tests.update({
        'admin': lambda user: user.role == 'admin',
        'mobile': lambda request: 'mobile' in request.user_agent.string.lower(),
    })
    
    # Variables globales
    env.globals.update({
        'current_year': lambda: datetime.now().year,
        'app_version': os.getenv('APP_VERSION', '1.0.0'),
        'config': get_config(),
    })
    
    return env
```

### 12.2 Filtros Personalizados Útiles
```python
# ✅ Filtros personalizados comunes
def time_ago(dt):
    """Filtro para mostrar tiempo relativo."""
    from datetime import datetime, timezone
    
    if not dt:
        return 'Never'
    
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    diff = now - dt
    
    if diff.days > 365:
        return f"{diff.days // 365} year{'s' if diff.days // 365 > 1 else ''} ago"
    elif diff.days > 30:
        return f"{diff.days // 30} month{'s' if diff.days // 30 > 1 else ''} ago"
    elif diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"

def format_filesize(bytes_value):
    """Formatear tamaño de archivo."""
    if bytes_value < 1024:
        return f"{bytes_value} B"
    elif bytes_value < 1024 * 1024:
        return f"{bytes_value / 1024:.1f} KB"
    elif bytes_value < 1024 * 1024 * 1024:
        return f"{bytes_value / (1024 * 1024):.1f} MB"
    else:
        return f"{bytes_value / (1024 * 1024 * 1024):.1f} GB"

def highlight_search(text, search_term):
    """Resaltar términos de búsqueda."""
    if not search_term:
        return text
    
    import re
    pattern = re.compile(re.escape(search_term), re.IGNORECASE)
    return pattern.sub(f'<mark>{search_term}</mark>', text)
```

```jinja2
{# ✅ Uso de filtros personalizados #}
{{ user.last_login | time_ago }}
{{ file.size | filesize }}
{{ article.content | highlight_search(search_query) | safe }}
```

## 13. **Mejores Prácticas Específicas**

### 13.1 Formularios Complejos
```jinja2
{# ✅ Formulario con validación y estados #}
{% from 'macros/forms.html' import field_with_errors %}

<form method="post" class="user-form" novalidate>
    {{ csrf_token() }}
    
    {% for field in form %}
        {% if field.widget.input_type != 'hidden' %}
            <div class="form-group {{ 'has-error' if field.errors }}">
                {{ field.label(class='form-label') }}
                {{ field(class='form-control' + (' is-invalid' if field.errors else '')) }}
                
                {% if field.errors %}
                    <div class="invalid-feedback">
                        {% for error in field.errors %}
                            <div>{{ error }}</div>
                        {% endfor %}
                    </div>
                {% endif %}
                
                {% if field.description %}
                    <small class="form-text text-muted">{{ field.description }}</small>
                {% endif %}
            </div>
        {% endif %}
    {% endfor %}
    
    <div class="form-actions">
        <button type="submit" class="btn btn-primary">
            {% if form.id.data %}Update{% else %}Create{% endif %} User
        </button>
        <a href="{{ url_for('user.list') }}" class="btn btn-secondary">Cancel</a>
    </div>
</form>
```

### 13.2 Tablas de Datos
```jinja2
{# ✅ Tabla responsive con paginación #}
<div class="table-responsive">
    <table class="table table-striped">
        <thead>
            <tr>
                {% for column in table_columns %}
                    <th scope="col">
                        {% if column.sortable %}
                            <a href="{{ url_for(request.endpoint, 
                                     sort=column.key, 
                                     order='desc' if request.args.get('sort') == column.key and request.args.get('order') == 'asc' else 'asc',
                                     **request.args) }}">
                                {{ column.label }}
                                {% if request.args.get('sort') == column.key %}
                                    <i class="fas fa-sort-{{ 'up' if request.args.get('order') == 'asc' else 'down' }}"></i>
                                {% endif %}
                            </a>
                        {% else %}
                            {{ column.label }}
                        {% endif %}
                    </th>
                {% endfor %}
                <th scope="col">Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for item in items %}
                <tr>
                    <td>{{ item.id }}</td>
                    <td>{{ item.name }}</td>
                    <td>{{ item.email }}</td>
                    <td>
                        <span class="badge badge-{{ 'success' if item.is_active else 'secondary' }}">
                            {{ 'Active' if item.is_active else 'Inactive' }}
                        </span>
                    </td>
                    <td>{{ item.created_at | strftime('%Y-%m-%d') }}</td>
                    <td>
                        <div class="btn-group" role="group">
                            <a href="{{ url_for('user.view', id=item.id) }}" 
                               class="btn btn-sm btn-outline-primary">View</a>
                            <a href="{{ url_for('user.edit', id=item.id) }}" 
                               class="btn btn-sm btn-outline-secondary">Edit</a>
                            <button type="button" 
                                    class="btn btn-sm btn-outline-danger"
                                    data-bs-toggle="modal" 
                                    data-bs-target="#deleteModal"
                                    data-item-id="{{ item.id }}"
                                    data-item-name="{{ item.name }}">
                                Delete
                            </button>
                        </div>
                    </td>
                </tr>
            {% else %}
                <tr>
                    <td colspan="{{ table_columns | length + 1 }}" class="text-center">
                        No data available
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

{# Paginación #}
{% if pagination.pages > 1 %}
    {{ pagination(pagination, 'user.list') }}
{% endif %}
```

## 14. **Errores Comunes y Soluciones**

### 14.1 Errores de Sintaxis
```jinja2
{# ❌ Errores comunes #}
{% if user.is_active %}
    Welcome!
{# endif %}  {# Comentario en lugar de tag #}

{% for item in items %}
    {{ item.name }}
{% end %}  {# Incorrecto - debería ser endfor #}

{{ user.name | filter1 | filter2() }}  {# Paréntesis innecesarios #}

{# ✅ Versiones corregidas #}
{% if user.is_active %}
    Welcome!
{% endif %}

{% for item in items %}
    {{ item.name }}
{% endfor %}

{{ user.name | filter1 | filter2 }}
```

### 14.2 Problemas de Contexto
```jinja2
{# ❌ Variables no definidas #}
{{ undefined_variable }}  {# Error si no existe #}

{# ✅ Verificaciones seguras #}
{{ undefined_variable | default('N/A') }}
{% if undefined_variable is defined %}{{ undefined_variable }}{% endif %}

{# ❌ Acceso a atributos sin verificar #}
{{ user.profile.settings.theme }}  {# Error si profile es None #}

{# ✅ Acceso seguro #}
{% if user and user.profile and user.profile.settings %}
    {{ user.profile.settings.theme }}
{% endif %}
```

---

## Checklist de Mejores Prácticas Jinja2

### ✅ Sintaxis y Formato
- [ ] Usar espacios consistentes en expresiones
- [ ] Comentarios descriptivos para templates complejos
- [ ] Control de whitespace apropiado
- [ ] Nomenclatura consistente para variables

### ✅ Seguridad
- [ ] Auto-escape habilitado para contenido HTML
- [ ] Usar filtros striptags para input de usuarios
- [ ] Validar URLs externas
- [ ] Incluir tokens CSRF en formularios

### ✅ Estructura
- [ ] Herencia de templates bien organizada
- [ ] Macros para componentes reutilizables
- [ ] Includes para fragmentos comunes
- [ ] Organización lógica de directorios

### ✅ Performance
- [ ] Cache de templates habilitado en producción
- [ ] Verificaciones antes de iteraciones grandes
- [ ] Includes condicionales para componentes pesados
- [ ] Lazy loading cuando sea apropiado

### ✅ Mantenibilidad
- [ ] Filtros personalizados para lógica compleja
- [ ] Tests personalizados para verificaciones comunes
- [ ] Documentación de templates complejos
- [ ] Nombres descriptivos para archivos y variables

### ✅ Internacionalización
- [ ] Uso de funciones de traducción para textos
- [ ] Soporte para pluralización
- [ ] Formato localizado de fechas y números
- [ ] Consideración de direccionalidad de texto

## Recursos Adicionales

- [Documentación Oficial de Jinja2](https://jinja.palletsprojects.com/)
- [Flask-Jinja2 Documentation](https://flask.palletsprojects.com/en/2.3.x/templating/)
- [Django Templates vs Jinja2](https://docs.djangoproject.com/en/4.2/topics/templates/)
- [Jinja2 Best Practices](https://jinja.palletsprojects.com/en/3.1.x/tricks/)
- [Template Security Guidelines](https://jinja.palletsprojects.com/en/3.1.x/api/#sandboxed-execution)

---

*Última actualización: Junio 2025*
