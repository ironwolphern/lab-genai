# Guía de Contribución

¡Gracias por tu interés en contribuir a lab-genai! 🎉

Esta guía te ayudará a entender cómo puedes contribuir de manera efectiva a este proyecto.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo puedo contribuir?](#cómo-puedo-contribuir)
- [Configuración del entorno de desarrollo](#configuración-del-entorno-de-desarrollo)
- [Proceso de contribución](#proceso-de-contribución)
- [Estándares de código](#estándares-de-código)
- [Reporte de bugs](#reporte-de-bugs)
- [Solicitud de características](#solicitud-de-características)

## 📜 Código de Conducta

Este proyecto y todos los participantes están regidos por nuestro [Código de Conducta](CODE_OF_CONDUCT.md). Al participar, se espera que mantengas este código.

## 🤝 ¿Cómo puedo contribuir?

Hay muchas formas de contribuir:

- 🐛 **Reportar bugs**: Encuentra y reporta errores
- 💡 **Sugerir mejoras**: Propón nuevas características
- 📖 **Mejorar documentación**: Ayuda a que la documentación sea más clara
- 🔧 **Contribuir código**: Implementa nuevas características o corrige bugs
- 🧪 **Escribir tests**: Mejora la cobertura de pruebas
- 🎨 **Mejorar UX/UI**: Mejora la experiencia de usuario

## 🛠️ Configuración del entorno de desarrollo

### Prerrequisitos

- Docker instalado
- Visual Studio Code con extensión "Dev Containers"
- Git configurado

### Configuración rápida

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/[tu-usuario]/lab-genai.git
   cd lab-genai
   ```

2. **Abrir en VS Code**:
   ```bash
   code .
   ```

3. **Reabrir en contenedor**: Cuando VS Code lo sugiera, selecciona "Reopen in Container"

4. **Verificar instalación**:
   ```bash
   python --version  # Debe mostrar Python 3.13.x
   python main.py    # Debe ejecutarse sin errores
   ```

## 🔄 Proceso de contribución

### 1. Fork y Clone

```bash
# Fork el repositorio en GitHub, luego:
git clone https://github.com/[tu-usuario]/lab-genai.git
cd lab-genai
git remote add upstream https://github.com/[repo-original]/lab-genai.git
```

### 2. Crear una rama

```bash
git checkout -b feature/nombre-descriptivo
# o
git checkout -b fix/descripcion-del-bug
```

### 3. Realizar cambios

- Mantén los commits pequeños y enfocados
- Escribe mensajes de commit descriptivos
- Sigue los estándares de código

### 4. Probar cambios

```bash
# Ejecutar linting
black .
flake8 .
pylint *.py

# Ejecutar tests
pytest

# Probar funcionalidad
python main.py
```

### 5. Commit y Push

```bash
git add .
git commit -m "feat: descripción clara del cambio"
git push origin feature/nombre-descriptivo
```

### 6. Crear Pull Request

- Ve a GitHub y crea un Pull Request
- Usa la plantilla proporcionada
- Describe claramente los cambios
- Enlaza issues relacionados

## 🎯 Estándares de código

### Python

- **Formateo**: Usar Black con líneas de 88 caracteres
- **Linting**: Código debe pasar Flake8 y Pylint
- **Type hints**: Usar anotaciones de tipo cuando sea posible
- **Docstrings**: Documentar funciones y clases públicas

```python
def ejemplo_funcion(nombre: str, edad: int) -> str:
    """
    Función de ejemplo que demuestra el estilo de código.
    
    Args:
        nombre: El nombre de la persona
        edad: La edad de la persona
        
    Returns:
        Un mensaje formateado
    """
    return f"{nombre} tiene {edad} años"
```

### Commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` para nuevas características
- `fix:` para corrección de bugs
- `docs:` para cambios en documentación
- `style:` para cambios de formato (sin cambios de lógica)
- `refactor:` para refactorización de código
- `test:` para añadir o corregir tests
- `chore:` para tareas de mantenimiento

## 🐛 Reporte de bugs

Para reportar un bug, [crea un issue](../../issues/new?template=bug_report.md) con:

- **Título claro** y descriptivo
- **Descripción detallada** del problema
- **Pasos para reproducir** el bug
- **Comportamiento esperado** vs **comportamiento actual**
- **Entorno**: OS, versión de Python, etc.
- **Screenshots** si es aplicable

## 💡 Solicitud de características

Para solicitar una nueva característica, [crea un issue](../../issues/new?template=feature_request.md) con:

- **Título claro** y descriptivo
- **Descripción del problema** que resuelve
- **Solución propuesta** (opcional)
- **Alternativas consideradas** (opcional)
- **Contexto adicional** que pueda ser útil

## 🧪 Tests

- Escribe tests para nuevo código
- Asegúrate de que todos los tests pasen
- Mantén buena cobertura de código

```bash
# Ejecutar tests
pytest

# Ejecutar tests con cobertura
pytest --cov=. --cov-report=html
```

## 📝 Documentación

- Actualiza README.md si es necesario
- Documenta nuevas funciones y clases
- Incluye ejemplos de uso cuando sea apropiado

## 🏷️ Versionado

Este proyecto sigue [Semantic Versioning](https://semver.org/):

- **MAJOR**: Cambios incompatibles en la API
- **MINOR**: Nueva funcionalidad compatible con versiones anteriores
- **PATCH**: Correcciones de bugs compatibles

## 📞 ¿Necesitas ayuda?

- 📧 **Email**: [tu-email@ejemplo.com]
- 💬 **Discussions**: Usa las [GitHub Discussions](../../discussions)
- 🐛 **Issues**: Para bugs o características específicas

## 🙏 Reconocimientos

¡Agradecemos a todos los contribuidores que han ayudado a hacer este proyecto mejor!

---

**¡Gracias por contribuir a lab-genai! 🚀**
