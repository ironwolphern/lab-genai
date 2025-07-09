---
applyTo: "**/*.json"
---
# Buenas Prácticas de JSON

## 1. **Sintaxis y Estructura Básica**

### 1.1 Formato y Espaciado
- **SIEMPRE** usa UTF-8 encoding
- Usa indentación consistente (2 o 4 espacios)
- Incluye espacios después de comas y dos puntos para legibilidad
- Mantén una estructura consistente en todo el archivo

```json
// ✅ Correcto - Bien formateado
{
  "name": "John Doe",
  "age": 30,
  "email": "john.doe@example.com",
  "address": {
    "street": "123 Main St",
    "city": "New York",
    "zipCode": "10001"
  },
  "hobbies": ["reading", "swimming", "coding"]
}

// ❌ Incorrecto - Mal formateado
{"name":"John Doe","age":30,"email":"john.doe@example.com","address":{"street":"123 Main St","city":"New York","zipCode":"10001"},"hobbies":["reading","swimming","coding"]}
```

### 1.2 Comillas y Caracteres
- **SIEMPRE** usa comillas dobles para strings y nombres de propiedades
- Escapa caracteres especiales correctamente
- No uses trailing commas (no soportadas en JSON estándar)

```json
// ✅ Correcto
{
  "message": "Hello \"World\"",
  "path": "C:\\Users\\John\\Documents",
  "newline": "Line 1\nLine 2",
  "unicode": "Emoji: \u1F60A"
}

// ❌ Incorrecto
{
  'message': 'Hello World',  // Comillas simples no válidas
  "trailing": "comma",       // Trailing comma no válida
}
```

### 1.3 Estructura de Archivos
```json
{
  "metadata": {
    "version": "1.0.0",
    "created": "2025-06-19T10:30:00Z",
    "description": "User configuration file"
  },
  "configuration": {
    "theme": "dark",
    "language": "en",
    "notifications": true
  },
  "data": {
    "users": [],
    "settings": {}
  }
}
```

## 2. **Tipos de Datos**

### 2.1 Strings
```json
{
  "simpleString": "Hello World",
  "emptyString": "",
  "stringWithQuotes": "She said \"Hello\"",
  "stringWithBackslash": "Path: C:\\Program Files",
  "multilineString": "Line 1\nLine 2\nLine 3",
  "unicodeString": "Café ☕ 你好",
  "urlString": "https://api.example.com/v1/users",
  "dateString": "2025-06-19T10:30:00Z",
  "versionString": "1.2.3"
}
```

### 2.2 Números
```json
{
  "integer": 42,
  "negativeInteger": -17,
  "float": 3.14159,
  "scientificNotation": 1.23e10,
  "negativeFloat": -0.5,
  "zero": 0,
  "price": 29.99,
  "percentage": 0.85
}

// ❌ Evitar - No son números válidos en JSON
{
  "invalid": Infinity,    // No válido
  "invalid2": NaN,        // No válido
  "invalid3": 0xFF,       // No válido (hexadecimal)
  "invalid4": 077         // No válido (octal)
}
```

### 2.3 Booleanos y Null
```json
{
  "isActive": true,
  "isDeleted": false,
  "nullValue": null,
  "settings": {
    "enableNotifications": true,
    "debugMode": false,
    "temporaryData": null
  }
}

// ❌ Evitar - Estos no son booleanos válidos
{
  "invalid": "true",      // String, no booleano
  "invalid2": 1,          // Número, no booleano
  "invalid3": undefined   // No válido en JSON
}
```

### 2.4 Arrays
```json
{
  "emptyArray": [],
  "numbers": [1, 2, 3, 4, 5],
  "strings": ["apple", "banana", "cherry"],
  "mixed": [1, "two", true, null],
  "nestedArrays": [[1, 2], [3, 4], [5, 6]],
  "objects": [
    {"id": 1, "name": "John"},
    {"id": 2, "name": "Jane"}
  ]
}
```

### 2.5 Objetos
```json
{
  "emptyObject": {},
  "user": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "nestedObject": {
    "level1": {
      "level2": {
        "level3": {
          "value": "deep nested value"
        }
      }
    }
  }
}
```

## 3. **Nomenclatura y Convenciones**

### 3.1 Convenciones de Naming
```json
{
  // ✅ camelCase (recomendado para JavaScript/APIs)
  "firstName": "John",
  "lastName": "Doe",
  "dateOfBirth": "1990-01-01",
  "isActive": true,
  
  // ✅ snake_case (común en APIs REST)
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-01",
  "is_active": true,
  
  // ✅ kebab-case (menos común pero válido)
  "first-name": "John",
  "last-name": "Doe"
}

// ❌ Evitar nombres inconsistentes
{
  "firstName": "John",
  "last_name": "Doe",      // Mezcla de convenciones
  "Date-Of-Birth": "1990-01-01"  // PascalCase con guiones
}
```

### 3.2 Nombres Descriptivos
```json
{
  // ✅ Nombres descriptivos y claros
  "userProfile": {
    "personalInformation": {
      "fullName": "John Doe",
      "emailAddress": "john@example.com",
      "phoneNumber": "+1-555-0123"
    },
    "accountSettings": {
      "isEmailNotificationEnabled": true,
      "preferredLanguage": "en-US",
      "accountCreationDate": "2025-01-15T08:30:00Z"
    }
  },
  
  // ❌ Nombres poco descriptivos
  "u": {
    "pi": {
      "n": "John Doe",
      "e": "john@example.com",
      "p": "+1-555-0123"
    }
  }
}
```

## 4. **Estructura y Organización**

### 4.1 Agrupación Lógica
```json
{
  "application": {
    "name": "MyApp",
    "version": "1.2.0",
    "environment": "production"
  },
  "database": {
    "host": "db.example.com",
    "port": 5432,
    "name": "myapp_db",
    "ssl": true
  },
  "cache": {
    "provider": "redis",
    "host": "cache.example.com",
    "port": 6379,
    "ttl": 3600
  },
  "security": {
    "authentication": {
      "provider": "oauth2",
      "issuer": "https://auth.example.com"
    },
    "encryption": {
      "algorithm": "AES-256",
      "keyRotationInterval": "30d"
    }
  }
}
```

### 4.2 Jerarquía Consistente
```json
{
  "users": [
    {
      "id": 1,
      "personalInfo": {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1-555-0123"
      },
      "preferences": {
        "language": "en",
        "timezone": "America/New_York",
        "notifications": {
          "email": true,
          "sms": false,
          "push": true
        }
      },
      "metadata": {
        "createdAt": "2025-01-15T08:30:00Z",
        "lastLogin": "2025-06-19T09:15:00Z",
        "isActive": true
      }
    }
  ]
}
```

## 5. **APIs y Responses**

### 5.1 Estructura de Response Estándar
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
      }
    ]
  },
  "meta": {
    "total": 1,
    "page": 1,
    "perPage": 10,
    "totalPages": 1
  },
  "links": {
    "self": "/api/v1/users?page=1",
    "first": "/api/v1/users?page=1",
    "last": "/api/v1/users?page=1",
    "next": null,
    "prev": null
  }
}
```

### 5.2 Manejo de Errores
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid data",
    "details": [
      {
        "field": "email",
        "message": "Email format is invalid",
        "code": "INVALID_FORMAT"
      },
      {
        "field": "age",
        "message": "Age must be between 18 and 100",
        "code": "OUT_OF_RANGE"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-06-19T10:30:00Z",
    "requestId": "req_123456789"
  }
}
```

### 5.3 Paginación
```json
{
  "data": [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
  ],
  "pagination": {
    "currentPage": 2,
    "itemsPerPage": 20,
    "totalItems": 150,
    "totalPages": 8,
    "hasNext": true,
    "hasPrev": true,
    "links": {
      "first": "/api/items?page=1&limit=20",
      "prev": "/api/items?page=1&limit=20",
      "self": "/api/items?page=2&limit=20",
      "next": "/api/items?page=3&limit=20",
      "last": "/api/items?page=8&limit=20"
    }
  }
}
```

## 6. **Configuración de Aplicaciones**

### 6.1 Configuración por Entornos
```json
// config/development.json
{
  "environment": "development",
  "server": {
    "host": "localhost",
    "port": 3000,
    "cors": {
      "origin": "*",
      "credentials": true
    }
  },
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "myapp_dev",
    "username": "dev_user",
    "ssl": false,
    "logging": true
  },
  "logging": {
    "level": "debug",
    "format": "detailed",
    "outputs": ["console", "file"]
  },
  "features": {
    "enableDebugEndpoints": true,
    "mockExternalServices": true
  }
}

// config/production.json
{
  "environment": "production",
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "cors": {
      "origin": ["https://myapp.com", "https://admin.myapp.com"],
      "credentials": true
    }
  },
  "database": {
    "host": "${DATABASE_HOST}",
    "port": 5432,
    "name": "${DATABASE_NAME}",
    "username": "${DATABASE_USER}",
    "ssl": true,
    "logging": false
  },
  "logging": {
    "level": "info",
    "format": "json",
    "outputs": ["file"]
  },
  "features": {
    "enableDebugEndpoints": false,
    "mockExternalServices": false
  }
}
```

### 6.2 Package.json Best Practices
```json
{
  "name": "my-awesome-app",
  "version": "1.2.0",
  "description": "A comprehensive web application for managing tasks",
  "main": "dist/index.js",
  "scripts": {
    "start": "node dist/index.js",
    "dev": "nodemon src/index.ts",
    "build": "tsc",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src/**/*.ts",
    "lint:fix": "eslint src/**/*.ts --fix",
    "format": "prettier --write src/**/*.ts"
  },
  "keywords": [
    "task-management",
    "productivity",
    "web-app",
    "typescript"
  ],
  "author": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "url": "https://johndoe.dev"
  },
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/johndoe/my-awesome-app.git"
  },
  "bugs": {
    "url": "https://github.com/johndoe/my-awesome-app/issues"
  },
  "homepage": "https://github.com/johndoe/my-awesome-app#readme",
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=8.0.0"
  },
  "dependencies": {
    "express": "^4.18.2",
    "dotenv": "^16.0.3",
    "joi": "^17.9.2"
  },
  "devDependencies": {
    "@types/node": "^20.3.1",
    "typescript": "^5.1.3",
    "nodemon": "^2.0.22",
    "jest": "^29.5.0",
    "eslint": "^8.42.0",
    "prettier": "^2.8.8"
  },
  "peerDependencies": {
    "react": ">=17.0.0"
  }
}
```

## 7. **Validación y Esquemas**

### 7.1 JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://example.com/user.schema.json",
  "title": "User",
  "description": "A user in the system",
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "minimum": 1,
      "description": "Unique identifier for the user"
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100,
      "description": "Full name of the user"
    },
    "email": {
      "type": "string",
      "format": "email",
      "description": "Email address of the user"
    },
    "age": {
      "type": "integer",
      "minimum": 18,
      "maximum": 120,
      "description": "Age of the user"
    },
    "preferences": {
      "type": "object",
      "properties": {
        "language": {
          "type": "string",
          "enum": ["en", "es", "fr", "de"],
          "default": "en"
        },
        "notifications": {
          "type": "boolean",
          "default": true
        }
      },
      "additionalProperties": false
    },
    "roles": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["admin", "user", "moderator"]
      },
      "uniqueItems": true,
      "minItems": 1
    }
  },
  "required": ["id", "name", "email"],
  "additionalProperties": false
}
```

### 7.2 Ejemplo de Datos Válidos
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 30,
  "preferences": {
    "language": "en",
    "notifications": true
  },
  "roles": ["user", "moderator"]
}
```

## 8. **Seguridad y Datos Sensibles**

### 8.1 Configuración Segura
```json
{
  "application": {
    "name": "MySecureApp",
    "version": "1.0.0"
  },
  "database": {
    "host": "${DB_HOST}",
    "port": "${DB_PORT}",
    "username": "${DB_USER}",
    "password": "${DB_PASSWORD}",
    "ssl": true,
    "sslMode": "require"
  },
  "secrets": {
    "jwtSecret": "${JWT_SECRET}",
    "encryptionKey": "${ENCRYPTION_KEY}",
    "apiKeys": {
      "stripe": "${STRIPE_API_KEY}",
      "sendgrid": "${SENDGRID_API_KEY}"
    }
  },
  "security": {
    "passwordPolicy": {
      "minLength": 12,
      "requireUppercase": true,
      "requireLowercase": true,
      "requireNumbers": true,
      "requireSpecialChars": true
    },
    "sessionTimeout": 3600,
    "maxLoginAttempts": 5
  }
}

// ❌ NUNCA hacer esto
{
  "database": {
    "password": "super_secret_password"  // ¡PELIGROSO!
  },
  "apiKeys": {
    "stripe": "sk_live_abc123def456"     // ¡PELIGROSO!
  }
}
```

### 8.2 Sanitización de Datos
```json
{
  "sanitizedResponse": {
    "user": {
      "id": 123,
      "name": "John Doe",
      "email": "j***@example.com",
      "createdAt": "2025-01-15T08:30:00Z"
      // password, internalId, y otros campos sensibles omitidos
    },
    "publicProfile": true,
    "lastLogin": "2025-06-19T09:15:00Z"
  }
}
```

## 9. **Performance y Optimización**

### 9.1 Estructura Optimizada
```json
{
  // ✅ Campos más importantes primero
  "id": 123,
  "name": "John Doe",
  "status": "active",
  
  // ✅ Datos anidados al final
  "details": {
    "description": "Long description...",
    "metadata": {
      "tags": ["tag1", "tag2", "tag3"]
    }
  }
}
```

### 9.2 Paginación Eficiente
```json
{
  "items": [
    {
      "id": 1,
      "name": "Item 1",
      "summary": "Brief summary"
      // Detalles completos disponibles en endpoint específico
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "hasMore": true
  },
  "links": {
    "next": "/api/items?page=2&limit=20",
    "self": "/api/items?page=1&limit=20"
  }
}
```

### 9.3 Compresión y Minimización
```json
// Desarrollo - Formateado para legibilidad
{
  "user": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  }
}

// Producción - Minimizado para performance
{"user":{"id":123,"name":"John Doe","email":"john@example.com"}}
```

## 10. **Fechas y Timestamps**

### 10.1 Formato de Fechas
```json
{
  "events": [
    {
      "id": 1,
      "name": "Conference 2025",
      // ✅ ISO 8601 formato recomendado
      "startDate": "2025-09-15T09:00:00Z",
      "endDate": "2025-09-17T18:00:00Z",
      "createdAt": "2025-06-19T10:30:00.123Z",
      "updatedAt": "2025-06-19T15:45:30.456Z",
      
      // ✅ Fechas locales con timezone
      "localStartTime": "2025-09-15T09:00:00-05:00",
      
      // ✅ Unix timestamp cuando sea apropiado
      "timestamp": 1718793000,
      
      // ✅ Fecha sin hora para casos específicos
      "birthDate": "1990-01-15"
    }
  ]
}

// ❌ Formatos de fecha problemáticos
{
  "badDates": {
    "american": "06/19/2025",     // Ambiguo
    "european": "19/06/2025",     // Ambiguo
    "informal": "June 19, 2025",  // No estándar
    "incomplete": "2025-06-19"    // Sin hora cuando se necesita
  }
}
```

## 11. **Internacionalización (i18n)**

### 11.1 Estructura de Traducciones
```json
{
  "en": {
    "common": {
      "save": "Save",
      "cancel": "Cancel",
      "delete": "Delete",
      "confirm": "Confirm"
    },
    "navigation": {
      "home": "Home",
      "profile": "Profile",
      "settings": "Settings"
    },
    "messages": {
      "welcome": "Welcome, {{name}}!",
      "itemsCount": {
        "zero": "No items",
        "one": "{{count}} item",
        "other": "{{count}} items"
      }
    },
    "errors": {
      "required": "This field is required",
      "invalid_email": "Please enter a valid email address"
    }
  },
  "es": {
    "common": {
      "save": "Guardar",
      "cancel": "Cancelar",
      "delete": "Eliminar",
      "confirm": "Confirmar"
    },
    "navigation": {
      "home": "Inicio",
      "profile": "Perfil",
      "settings": "Configuración"
    },
    "messages": {
      "welcome": "¡Bienvenido, {{name}}!",
      "itemsCount": {
        "zero": "Sin elementos",
        "one": "{{count}} elemento",
        "other": "{{count}} elementos"
      }
    },
    "errors": {
      "required": "Este campo es obligatorio",
      "invalid_email": "Por favor ingrese un email válido"
    }
  }
}
```

## 12. **Testing y Mocking**

### 12.1 Datos de Prueba
```json
{
  "testUsers": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@test.example.com",
      "role": "admin",
      "createdAt": "2025-01-01T00:00:00Z",
      "isActive": true
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane.smith@test.example.com",
      "role": "user",
      "createdAt": "2025-01-02T00:00:00Z",
      "isActive": true
    }
  ],
  "testScenarios": {
    "validUser": {
      "name": "Test User",
      "email": "test@example.com",
      "password": "ValidPass123!"
    },
    "invalidUser": {
      "name": "",
      "email": "invalid-email",
      "password": "123"
    }
  }
}
```

### 12.2 Mock Responses
```json
{
  "mockApiResponses": {
    "getUserSuccess": {
      "status": 200,
      "data": {
        "id": 123,
        "name": "John Doe",
        "email": "john@example.com"
      }
    },
    "getUserNotFound": {
      "status": 404,
      "error": {
        "code": "USER_NOT_FOUND",
        "message": "User with ID 123 not found"
      }
    },
    "validationError": {
      "status": 400,
      "error": {
        "code": "VALIDATION_ERROR",
        "message": "Request validation failed",
        "details": [
          {
            "field": "email",
            "message": "Email is required"
          }
        ]
      }
    }
  }
}
```

## 13. **Herramientas y Validación**

### 13.1 Configuración de Herramientas
```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": 2022,
    "sourceType": "module"
  },
  "rules": {
    "quotes": ["error", "single"],
    "semi": ["error", "always"],
    "no-unused-vars": "error",
    "no-console": "warn"
  },
  "env": {
    "node": true,
    "es2022": true,
    "jest": true
  }
}

// .prettierrc.json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "bracketSpacing": true,
  "arrowParens": "avoid"
}
```

### 13.2 Configuración de VS Code
```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "json.validate.enable": true,
  "json.format.enable": true,
  "files.associations": {
    "*.json": "json"
  },
  "json.schemas": [
    {
      "fileMatch": ["package.json"],
      "url": "https://json.schemastore.org/package.json"
    },
    {
      "fileMatch": ["tsconfig.json"],
      "url": "https://json.schemastore.org/tsconfig.json"
    }
  ]
}
```

## 14. **Errores Comunes y Cómo Evitarlos**

### 14.1 Errores de Sintaxis
```json
// ❌ Errores comunes
{
  "name": "John",
  "age": 30,     // Trailing comma no válida
}

{
  'name': 'John'  // Comillas simples no válidas
}

{
  name: "John"    // Keys sin comillas no válidas
}

{
  "comment": "// This is not a valid comment"  // Comentarios no válidos en JSON
}

// ✅ Versiones corregidas
{
  "name": "John",
  "age": 30
}

{
  "name": "John"
}

{
  "name": "John"
}

{
  "description": "This is a valid description field"
}
```

### 14.2 Problemas de Tipos
```json
// ❌ Problemas comunes
{
  "isActive": "true",     // String en lugar de boolean
  "count": "42",          // String en lugar de number
  "value": undefined,     // undefined no es válido en JSON
  "data": NaN,            // NaN no es válido en JSON
  "infinity": Infinity    // Infinity no es válido en JSON
}

// ✅ Versiones corregidas
{
  "isActive": true,       // Boolean correcto
  "count": 42,            // Number correcto
  "value": null,          // null en lugar de undefined
  "data": null,           // null en lugar de NaN
  "infinity": null        // null en lugar de Infinity
}
```

### 14.3 Problemas de Estructura
```json
// ❌ Estructura inconsistente
{
  "users": [
    {"id": 1, "name": "John", "active": true},
    {"id": 2, "name": "Jane"},  // Campo 'active' faltante
    {"id": 3, "fullName": "Bob", "active": false}  // Campo 'name' vs 'fullName'
  ]
}

// ✅ Estructura consistente
{
  "users": [
    {"id": 1, "name": "John", "active": true},
    {"id": 2, "name": "Jane", "active": false},
    {"id": 3, "name": "Bob", "active": false}
  ]
}
```

## 15. **Comandos y Herramientas Útiles**

### 15.1 Validación y Formateo
```bash
# Validar JSON
cat file.json | jq '.'

# Formatear JSON
cat file.json | jq '.' > formatted.json

# Extraer valores específicos
cat file.json | jq '.users[0].name'

# Filtrar arrays
cat file.json | jq '.users[] | select(.active == true)'

# Validar con Node.js
node -e "JSON.parse(require('fs').readFileSync('file.json', 'utf8'))"

# Validar con Python
python -m json.tool file.json

# Formatear con prettier
npx prettier --write "**/*.json"
```

### 15.2 Schema Validation
```javascript
// Usando Ajv para validación de schema
const Ajv = require('ajv');
const ajv = new Ajv();

const schema = {
  type: "object",
  properties: {
    name: { type: "string" },
    age: { type: "number", minimum: 0 }
  },
  required: ["name"]
};

const validate = ajv.compile(schema);
const valid = validate(data);

if (!valid) {
  console.log(validate.errors);
}
```

---

## Checklist de Mejores Prácticas JSON

### ✅ Sintaxis
- [ ] Usar UTF-8 encoding
- [ ] Comillas dobles para strings y keys
- [ ] No trailing commas
- [ ] Escapar caracteres especiales correctamente
- [ ] Indentación consistente

### ✅ Tipos de Datos
- [ ] Usar tipos apropiados (string, number, boolean, null)
- [ ] Evitar undefined, NaN, Infinity
- [ ] Consistencia en tipos para campos similares
- [ ] Formato ISO 8601 para fechas

### ✅ Estructura
- [ ] Agrupación lógica de datos
- [ ] Nomenclatura consistente (camelCase o snake_case)
- [ ] Jerarquía clara y predecible
- [ ] Estructura consistente para objetos similares

### ✅ APIs
- [ ] Formato de response estándar
- [ ] Manejo de errores consistente
- [ ] Paginación apropiada
- [ ] Versionado de API

### ✅ Seguridad
- [ ] No hardcodear secretos
- [ ] Usar variables de entorno
- [ ] Sanitizar datos sensibles en responses
- [ ] Validar inputs con schemas

### ✅ Performance
- [ ] Minimizar para producción
- [ ] Paginación para listas grandes
- [ ] Campos esenciales primero
- [ ] Evitar anidamiento excesivo

## Recursos Adicionales

- [JSON.org - Especificación Oficial](https://www.json.org/)
- [JSON Schema](https://json-schema.org/)
- [JSONLint - Validador Online](https://jsonlint.com/)
- [jq - Procesador JSON para línea de comandos](https://jqlang.github.io/jq/)
- [Ajv - JSON Schema Validator](https://ajv.js.org/)
- [Prettier - Code Formatter](https://prettier.io/)

---

*Última actualización: Junio 2025*
