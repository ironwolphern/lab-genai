---
applyTo: "**/*.yml,**/*.yaml"
---
# Buenas Prácticas de YAML

## 1. **Sintaxis y Estructura Básica**

### 1.1 Indentación
- **SIEMPRE** usa espacios, nunca tabs
- Usa 2 espacios para indentación (estándar más común)
- Mantén consistencia en toda la indentación del archivo
- Cada nivel de anidamiento debe tener exactamente 2 espacios más

```yaml
# ✅ Correcto - 2 espacios por nivel
parent:
  child:
    grandchild: value
    another_grandchild:
      - item1
      - item2

# ❌ Incorrecto - Inconsistente
parent:
    child:  # 4 espacios
      grandchild: value  # 2 espacios más
```

### 1.2 Separadores de Documentos
- Usa `---` para separar múltiples documentos en un archivo
- Usa `...` para indicar el final de un documento (opcional)

```yaml
# ✅ Múltiples documentos YAML
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  key: value

---
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
data:
  password: cGFzc3dvcmQ=
...
```

### 1.3 Espaciado y Formato
- Deja un espacio después de los dos puntos
- No dejes espacios al final de las líneas
- Usa líneas en blanco para separar secciones lógicas

```yaml
# ✅ Correcto
key: value
another_key: another_value

section:
  nested_key: nested_value
  
another_section:
  key: value

# ❌ Incorrecto
key:value
another_key :another_value
section:
  nested_key:nested_value
```

## 2. **Tipos de Datos y Valores**

### 2.1 Strings (Cadenas de Texto)
```yaml
# ✅ String simple (sin comillas necesarias)
simple_string: Hello World

# ✅ String con comillas simples (literal)
quoted_string: 'Hello World'

# ✅ String con comillas dobles (permite escape)
escaped_string: "Hello\nWorld"

# ✅ String multilínea literal (preserva saltos de línea)
literal_multiline: |
  This is a multiline string
  that preserves line breaks
  exactly as written

# ✅ String multilínea plegado (convierte saltos en espacios)
folded_multiline: >
  This is a multiline string
  that will be folded into
  a single line with spaces

# ✅ String con caracteres especiales
special_chars: 'String with: colons, [brackets], and {braces}'

# ✅ String vacío
empty_string: ""
# o
null_string: null
```

### 2.2 Números
```yaml
# ✅ Enteros
integer: 42
negative_integer: -17
octal: 0o644
hexadecimal: 0xFF

# ✅ Flotantes
float: 3.14159
scientific: 1.23e+4
infinity: .inf
not_a_number: .nan

# ❌ Evitar ambigüedad - usar comillas si es necesario
version: "1.20"  # String, no número
port: 8080       # Número
```

### 2.3 Booleanos
```yaml
# ✅ Valores booleanos explícitos
enabled: true
disabled: false

# ✅ También válidos pero menos recomendados
legacy_true: yes
legacy_false: no

# ❌ Evitar para claridad
confusing_bool: "true"  # Esto es un string, no booleano
```

### 2.4 Null y Valores Vacíos
```yaml
# ✅ Valores null explícitos
empty_value: null
tilde_null: ~

# ✅ Valor vacío vs null
empty_string: ""
null_value: null

# ✅ Key sin valor (implícitamente null)
implicit_null:
```

## 3. **Estructuras de Datos**

### 3.1 Listas (Arrays)
```yaml
# ✅ Lista con guiones
fruits:
  - apple
  - banana
  - orange

# ✅ Lista inline (para listas cortas)
colors: [red, green, blue]

# ✅ Lista de objetos
users:
  - name: John
    age: 30
    active: true
  - name: Jane
    age: 25
    active: false

# ✅ Lista anidada
nested_list:
  - item1
  - - subitem1
    - subitem2
  - item3

# ❌ Evitar mezclar estilos
mixed_style:
  - item1
  - item2: [sub1, sub2]  # No recomendado
```

### 3.2 Mapas (Objetos/Diccionarios)
```yaml
# ✅ Mapa básico
person:
  name: John Doe
  age: 30
  city: New York

# ✅ Mapa inline (para mapas pequeños)
coordinates: {x: 10, y: 20}

# ✅ Mapa anidado
database:
  connection:
    host: localhost
    port: 5432
    credentials:
      username: admin
      password: secret

# ✅ Mapa con listas
permissions:
  admin:
    - read
    - write
    - delete
  user:
    - read
```

### 3.3 Tipos Complejos
```yaml
# ✅ Combinando diferentes tipos
application:
  name: MyApp
  version: "1.2.0"
  enabled: true
  ports:
    - 8080
    - 8443
  database:
    type: postgresql
    config:
      host: db.example.com
      port: 5432
      ssl: true
  features:
    feature_a: true
    feature_b: false
    feature_c: null
```

## 4. **Comentarios y Documentación**

### 4.1 Comentarios Efectivos
```yaml
# ✅ Comentario de header del archivo
# Application Configuration
# Version: 1.0
# Last Updated: 2025-06-19

# ✅ Comentarios de sección
# Database Configuration
database:
  host: localhost  # ✅ Comentario inline explicativo
  port: 5432
  # ✅ Comentario multi-línea para configuraciones complejas
  # Connection pool settings:
  # - min_connections: minimum connections to maintain
  # - max_connections: maximum connections allowed
  pool:
    min_connections: 5
    max_connections: 20

# ✅ Comentarios para valores importantes
security:
  # IMPORTANT: Change this in production!
  secret_key: "dev-key-only"
  
  # Enable this for production deployment
  # ssl_required: true

# ❌ Evitar comentarios obvios
name: John  # This is a name
```

### 4.2 Documentación en YAML
```yaml
# ✅ Metadata descriptiva
metadata:
  name: my-application
  description: |
    This is a comprehensive configuration file for MyApp.
    It includes database settings, security configuration,
    and feature flags.
  version: "1.2.0"
  maintainer: "platform-team@company.com"
  created: "2025-06-19"
  
# ✅ Secciones bien documentadas
# =============================================================================
# APPLICATION SETTINGS
# =============================================================================
app:
  name: MyApp
  debug: false  # Set to true for development

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
database:
  # Primary database connection
  primary:
    host: db-primary.example.com
    port: 5432
  
  # Read replica for scaling reads
  replica:
    host: db-replica.example.com
    port: 5432
```

## 5. **Organización y Estructura**

### 5.1 Agrupación Lógica
```yaml
# ✅ Agrupar configuraciones relacionadas
# Application Core Settings
application:
  name: MyApp
  version: "1.2.0"
  environment: production

# Infrastructure Settings
infrastructure:
  database:
    host: db.example.com
    port: 5432
  redis:
    host: redis.example.com
    port: 6379
  messaging:
    broker: rabbitmq.example.com
    port: 5672

# Security Settings
security:
  authentication:
    method: oauth2
    provider: auth.example.com
  authorization:
    rbac_enabled: true
    default_role: user

# Feature Flags
features:
  new_ui: true
  beta_api: false
  advanced_analytics: true
```

### 5.2 Jerarquía Clara
```yaml
# ✅ Estructura jerárquica clara
company:
  name: "Tech Corp"
  departments:
    engineering:
      teams:
        backend:
          lead: "John Smith"
          members:
            - "Alice Johnson"
            - "Bob Wilson"
        frontend:
          lead: "Sarah Davis"
          members:
            - "Mike Brown"
            - "Lisa Garcia"
    marketing:
      budget: 100000
      campaigns:
        - name: "Summer Sale"
          budget: 25000
        - name: "Product Launch"
          budget: 50000
```

## 6. **Nombrado y Convenciones**

### 6.1 Convenciones de Nomenclatura
```yaml
# ✅ snake_case para keys (recomendado)
database_host: localhost
max_connections: 100
api_key: secret

# ✅ Alternativa: kebab-case (consistente en el archivo)
database-host: localhost
max-connections: 100
api-key: secret

# ✅ camelCase (menos común pero válido si es consistente)
databaseHost: localhost
maxConnections: 100
apiKey: secret

# ❌ Evitar mezclar estilos
database_host: localhost
max-connections: 100  # Inconsistente
apiKey: secret        # Inconsistente
```

### 6.2 Nombres Descriptivos
```yaml
# ✅ Nombres descriptivos y claros
web_server:
  listen_port: 8080
  worker_processes: 4
  request_timeout_seconds: 30
  max_request_size_mb: 10

# ✅ Evitar abreviaciones confusas
database_configuration:
  connection_string: "postgresql://..."
  maximum_connections: 20
  connection_timeout_milliseconds: 5000

# ❌ Nombres poco descriptivos
srv:
  p: 8080
  w: 4
  t: 30

# ❌ Abreviaciones confusas
db_cfg:
  conn_str: "postgresql://..."
  max_conn: 20
```

## 7. **Seguridad y Datos Sensibles**

### 7.1 Manejo de Secretos
```yaml
# ✅ Referencias a secretos externos
database:
  host: db.example.com
  port: 5432
  username: ${DB_USERNAME}  # Variable de entorno
  password: ${DB_PASSWORD}  # Variable de entorno

# ✅ Placeholder para valores sensibles
api:
  keys:
    stripe: "REPLACE_WITH_STRIPE_KEY"
    sendgrid: "REPLACE_WITH_SENDGRID_KEY"

# ✅ Configuración por entornos
environments:
  development:
    database_url: "postgresql://dev-db:5432/myapp"
    debug: true
  production:
    database_url: "${DATABASE_URL}"  # Desde variables de entorno
    debug: false

# ❌ NUNCA hardcodear secretos
api_key: "sk_live_abc123def456"  # ¡PELIGROSO!
database_password: "supersecret"  # ¡PELIGROSO!
```

### 7.2 Separación por Entornos
```yaml
# ✅ config/base.yml
defaults: &defaults
  app_name: MyApp
  port: 8080
  log_level: info

# ✅ config/development.yml
development:
  <<: *defaults
  database_url: "postgresql://localhost:5432/myapp_dev"
  debug: true
  log_level: debug

# ✅ config/production.yml
production:
  <<: *defaults
  database_url: "${DATABASE_URL}"
  debug: false
  log_level: warn
```

## 8. **Anclas y Referencias**

### 8.1 Uso de Anclas (&) y Referencias (*)
```yaml
# ✅ Definir anclas para reutilización
defaults: &default_settings
  timeout: 30
  retries: 3
  log_level: info

# ✅ Usar referencias para evitar duplicación
web_server:
  <<: *default_settings  # Merge
  port: 8080
  workers: 4

api_server:
  <<: *default_settings  # Merge
  port: 3000
  workers: 2

# ✅ Anclas para valores comunes
database_config: &db_config
  host: db.example.com
  port: 5432
  ssl: true

primary_db:
  <<: *db_config
  database: primary

replica_db:
  <<: *db_config
  database: replica
  readonly: true
```

### 8.2 Anclas Complejas
```yaml
# ✅ Anclas para configuraciones complejas
resource_limits: &resource_limits
  cpu: "500m"
  memory: "512Mi"

security_context: &security_context
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true

# ✅ Aplicar en múltiples servicios
services:
  web:
    name: web-service
    resources:
      limits: *resource_limits
    security: *security_context
  
  api:
    name: api-service
    resources:
      limits: *resource_limits
    security: *security_context

# ✅ Merge con override
api_extended:
  <<: *security_context
  capabilities:
    drop: ["ALL"]
```

## 9. **Validación y Esquemas**

### 9.1 Estructura Predecible
```yaml
# ✅ Estructura consistente para objetos similares
users:
  - id: 1
    name: "John Doe"
    email: "john@example.com"
    active: true
    roles: ["user"]
  
  - id: 2
    name: "Jane Smith"
    email: "jane@example.com"
    active: true
    roles: ["admin", "user"]

# ✅ Campos obligatorios siempre presentes
servers:
  - name: "web-01"
    ip: "10.0.1.10"
    role: "web"
    active: true
    tags: []  # Array vacío en lugar de omitir
  
  - name: "db-01"
    ip: "10.0.1.20"
    role: "database"
    active: true
    tags: ["primary"]
```

### 9.2 Tipos Consistentes
```yaml
# ✅ Tipos de datos consistentes
configuration:
  # Strings siempre como strings
  version: "1.2.0"
  environment: "production"
  
  # Números siempre como números
  port: 8080
  timeout: 30
  
  # Booleanos siempre como booleanos
  debug: false
  ssl_enabled: true
  
  # Arrays siempre como arrays (incluso si están vacíos)
  allowed_ips: []
  features: ["feature_a", "feature_b"]

# ❌ Evitar tipos inconsistentes
inconsistent:
  version: 1.2        # Número en lugar de string
  port: "8080"        # String en lugar de número
  debug: "false"      # String en lugar de booleano
  features: null      # null en lugar de array vacío
```

## 10. **Performance y Legibilidad**

### 10.1 Longitud de Líneas
```yaml
# ✅ Líneas cortas y legibles
database:
  connection_string: >
    postgresql://user:password@hostname:5432/database?
    sslmode=require&application_name=myapp

# ✅ Listas largas bien formateadas
allowed_origins:
  - "https://app.example.com"
  - "https://admin.example.com"
  - "https://api.example.com"
  - "https://staging.example.com"

# ✅ Configuración compleja bien estructurada
monitoring:
  prometheus:
    enabled: true
    scrape_interval: "30s"
    evaluation_interval: "30s"
    rules:
      - alert: "HighCPUUsage"
        expr: "cpu_usage > 80"
        for: "5m"
        labels:
          severity: "warning"
        annotations:
          summary: "High CPU usage detected"
```

### 10.2 Agrupación Visual
```yaml
# ✅ Usar separación visual para claridad
# =============================================================================
# CORE APPLICATION SETTINGS
# =============================================================================
app:
  name: MyApplication
  version: "2.1.0"
  debug: false

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
database:
  primary:
    host: db-primary.example.com
    port: 5432
    pool_size: 20
  
  replica:
    host: db-replica.example.com
    port: 5432
    pool_size: 10

# =============================================================================
# CACHING CONFIGURATION
# =============================================================================
cache:
  redis:
    host: redis.example.com
    port: 6379
    db: 0
    ttl: 3600
```

## 11. **Casos de Uso Específicos**

### 11.1 Configuración de Aplicaciones
```yaml
# ✅ application.yml
application:
  name: "MyWebApp"
  version: "1.0.0"
  
server:
  port: 8080
  servlet:
    context-path: "/api"
  
spring:
  datasource:
    url: "${DATABASE_URL:jdbc:postgresql://localhost:5432/myapp}"
    username: "${DB_USERNAME:myapp}"
    password: "${DB_PASSWORD:secret}"
    driver-class-name: "org.postgresql.Driver"
  
  jpa:
    hibernate:
      ddl-auto: "validate"
    show-sql: false
    properties:
      hibernate:
        dialect: "org.hibernate.dialect.PostgreSQLDialect"
        format_sql: true

logging:
  level:
    com.mycompany.myapp: DEBUG
    org.springframework.security: DEBUG
  pattern:
    console: "%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n"
```

### 11.2 Docker Compose
```yaml
# ✅ docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - NODE_ENV=production
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - db
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=myapp
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local

networks:
  default:
    name: myapp-network
```

### 11.3 Kubernetes Manifests
```yaml
# ✅ deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
  labels:
    app: web-app
    version: v1.0.0
    environment: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
        version: v1.0.0
    spec:
      containers:
      - name: web-app
        image: myorg/web-app:v1.0.0
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: log-level
        resources:
          requests:
            cpu: "100m"
            memory: "256Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 11.4 CI/CD Pipelines
```yaml
# ✅ .github/workflows/deploy.yml
name: Deploy Application

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  DOCKER_REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm test
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

## 12. **Herramientas y Validación**

### 12.1 Linters y Validadores
```yaml
# ✅ .yamllint.yml - Configuración de yamllint
extends: default

rules:
  line-length:
    max: 120
    level: warning
  
  indentation:
    spaces: 2
    indent-sequences: true
    check-multi-line-strings: false
  
  trailing-spaces: enable
  empty-lines:
    max: 2
    max-start: 0
    max-end: 1
  
  comments:
    min-spaces-from-content: 1
    
  truthy:
    allowed-values: ['true', 'false']
    check-keys: true
```

### 12.2 Schema Validation
```yaml
# ✅ JSON Schema para validación
# config-schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "application": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
        "port": {"type": "integer", "minimum": 1, "maximum": 65535}
      },
      "required": ["name", "version", "port"]
    },
    "database": {
      "type": "object",
      "properties": {
        "host": {"type": "string"},
        "port": {"type": "integer"},
        "ssl": {"type": "boolean"}
      },
      "required": ["host", "port"]
    }
  },
  "required": ["application"]
}
```

## 13. **Errores Comunes y Cómo Evitarlos**

### 13.1 Errores de Sintaxis
```yaml
# ❌ Errores comunes
incorrect:
  - item1
   - item2  # Indentación incorrecta
  
  key:value  # Falta espacio después de ':'
  
  "unclosed string
  
  - item with: colon but no quotes  # Debería estar entre comillas

# ✅ Versiones corregidas
correct:
  - item1
  - item2  # Indentación consistente
  
  key: value  # Espacio después de ':'
  
  "closed string"
  
  - "item with: colon and quotes"
```

### 13.2 Problemas de Tipos de Datos
```yaml
# ❌ Problemas comunes
problematic:
  version: 1.20        # Se interpreta como float, no string
  enabled: yes         # Ambiguo, mejor usar true/false
  port: "8080"         # String cuando debería ser número
  items: null          # null cuando se espera array

# ✅ Versiones corregidas
correct:
  version: "1.20"      # String explícito
  enabled: true        # Booleano explícito
  port: 8080           # Número explícito
  items: []            # Array vacío en lugar de null
```

### 13.3 Problemas de Estructura
```yaml
# ❌ Estructura problemática
bad_structure:
  - name: item1
    value: 100
  - item2: 200  # Estructura inconsistente
  - name: item3
    value: 300

# ✅ Estructura consistente
good_structure:
  - name: item1
    value: 100
  - name: item2
    value: 200
  - name: item3
    value: 300
```

## 14. **Herramientas Recomendadas**

### 14.1 Editores y Extensiones
```yaml
# Configuración para VS Code (.vscode/settings.json)
{
  "yaml.schemas": {
    "./config-schema.json": ["config/*.yml", "config/*.yaml"]
  },
  "yaml.format.enable": true,
  "yaml.validate": true,
  "yaml.completion": true,
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.detectIndentation": false
}
```

### 14.2 Comandos Útiles
```bash
# ✅ Validación con yamllint
yamllint config.yml

# ✅ Formateo con yq
yq eval '.' config.yml

# ✅ Validación de sintaxis
python -c "import yaml; yaml.safe_load(open('config.yml'))"

# ✅ Conversión JSON a YAML
cat config.json | yq eval -P '.'

# ✅ Extraer valores específicos
yq eval '.database.host' config.yml
```

---

## Checklist de Mejores Prácticas YAML

### ✅ Sintaxis
- [ ] Usar 2 espacios para indentación
- [ ] No usar tabs
- [ ] Espacio después de los dos puntos
- [ ] Sin espacios al final de líneas
- [ ] Separar documentos múltiples con `---`

### ✅ Tipos de Datos
- [ ] Usar tipos explícitos y consistentes
- [ ] Comillas para strings con caracteres especiales
- [ ] Booleanos explícitos (`true`/`false`)
- [ ] Strings de versión entre comillas

### ✅ Estructura
- [ ] Agrupación lógica de configuraciones
- [ ] Jerarquía clara y consistente
- [ ] Nombres descriptivos para keys
- [ ] Estructura predecible para objetos similares

### ✅ Seguridad
- [ ] No hardcodear secretos
- [ ] Usar variables de entorno para datos sensibles
- [ ] Separar configuración por entornos

### ✅ Documentación
- [ ] Comentarios útiles y descriptivos
- [ ] Metadata de archivo cuando sea apropiado
- [ ] Documentar configuraciones complejas

### ✅ Mantenibilidad
- [ ] Usar anclas para evitar duplicación
- [ ] Validar con herramientas de linting
- [ ] Mantener consistencia en todo el archivo

## Recursos Adicionales

- [YAML Specification](https://yaml.org/spec/)
- [yamllint - YAML Linter](https://yamllint.readthedocs.io/)
- [yq - YAML Processor](https://mikefarah.gitbook.io/yq/)
- [YAML Multiline Strings](https://yaml-multiline.info/)
- [Online YAML Validator](https://codebeautify.org/yaml-validator)

---

*Última actualización: Junio 2025*
