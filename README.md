# Entorno de Desarrollo Python 3.13

Este proyecto está configurado con un devcontainer optimizado para desarrollo en Python 3.13.

## 🚀 Características

- **Python 3.13**: Última versión de Python con mejoras de rendimiento
- **Herramientas de desarrollo**: Black, Flake8, Pylint, Pytest preinstalados
- **Extensiones VS Code**: Configuración automática de extensiones Python
- **Optimizaciones**: Cache de pip persistente y configuraciones de rendimiento
- **Formateo automático**: Black configurado para formatear al guardar
- **Linting**: Pylint y Flake8 habilitados por defecto

## 📦 Estructura del Proyecto

```
.
├── .devcontainer/
│   └── devcontainer.json    # Configuración del contenedor
├── .gitignore              # Archivos ignorados por Git
├── requirements.txt        # Dependencias Python
├── main.py                # Archivo de ejemplo
└── README.md              # Este archivo
```

## 🛠️ Uso del Devcontainer

### Prerrequisitos

- Docker instalado
- Visual Studio Code con la extensión "Dev Containers"

### Pasos para usar

1. **Abrir en VS Code**: Abre este proyecto en VS Code
2. **Reabrir en contenedor**: Cuando VS Code detecte el devcontainer, selecciona "Reopen in Container"
3. **Esperar**: El contenedor se construirá automáticamente (puede tomar unos minutos la primera vez)
4. **¡Listo!**: Tu entorno Python 3.13 está configurado y listo para usar

### Probar el entorno

```bash
# Ejecutar el archivo de ejemplo
python main.py

# Verificar la versión de Python
python --version

# Instalar dependencias adicionales
pip install numpy pandas
```

## 📋 Dependencias Incluidas

### Herramientas de desarrollo (instaladas por defecto)
- `black`: Formateador de código
- `flake8`: Linter para verificar estilo
- `pylint`: Análisis estático de código
- `pytest`: Framework de testing
- `pytest-cov`: Cobertura de tests
- `python-dotenv`: Manejo de variables de entorno

### Dependencias opcionales (comentadas en requirements.txt)
- Científicas: numpy, pandas, matplotlib, jupyter
- Web: fastapi, uvicorn, requests

## ⚙️ Configuraciones Incluidas

- **Formateo automático**: Se ejecuta Black al guardar archivos
- **Organización de imports**: Automática al guardar
- **Puertos expuestos**: 3000, 5000, 8000 para desarrollo web
- **Variables de entorno**: Configuradas para mejor rendimiento Python
- **Cache de pip**: Persistente entre reconstrucciones del contenedor

## 🔧 Personalización

Para personalizar el entorno:

1. **Agregar dependencias**: Edita `requirements.txt`
2. **Agregar extensiones**: Modifica `.devcontainer/devcontainer.json`
3. **Cambiar configuraciones**: Ajusta las settings en devcontainer.json

## 📝 Comandos Útiles

```bash
# Instalar nueva dependencia
pip install nombre-paquete

# Actualizar requirements.txt
pip freeze > requirements.txt

# Ejecutar tests
pytest

# Formatear todo el código
black .

# Verificar estilo
flake8 .

# Análisis con pylint
pylint *.py
```

---

**¡Tu entorno Python 3.13 está listo para el desarrollo! 🎉**
