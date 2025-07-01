# Entorno de Desarrollo Python 3.13

Este proyecto está configurado con un devcontainer optimizado para desarrollo en Python 3.13.

## 🚀 Características

- **Python 3.13**: Última versión de Python con mejoras de rendimiento
- **uv**: Gestor de paquetes ultrarrápido para Python
- **Herramientas de desarrollo**: Black, Flake8, Pylint, Pytest preinstalados
- **Extensiones VS Code**: Configuración automática de extensiones Python
- **Dependabot**: Actualizaciones automáticas de dependencias
- **GitHub Actions**: CI/CD automático con Dependabot
- **Optimizaciones**: Cache de pip y uv persistente para máximo rendimiento
- **Formateo automático**: Black configurado para formatear al guardar
- **Linting**: Pylint y Flake8 habilitados por defecto

## 📦 Estructura del Proyecto

```
.
├── .devcontainer/
│   └── devcontainer.json    # Configuración del contenedor
├── .github/
│   ├── ISSUE_TEMPLATE/      # Plantillas para issues
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   ├── documentation.md
│   │   ├── help.md
│   │   └── config.yml
│   ├── workflows/
│   │   └── dependabot.yml   # Workflow de auto-merge
│   ├── dependabot.yml       # Configuración de Dependabot
│   ├── dependabot-security.yml  # Configuración de seguridad
│   └── PULL_REQUEST_TEMPLATE.md # Plantilla para PRs
├── .gitignore               # Archivos ignorados por Git
├── CODEOWNERS              # Propietarios de código
├── CODE_OF_CONDUCT.md      # Código de conducta
├── CONTRIBUTING.md         # Guía de contribución
├── LICENSE                 # Licencia MIT
├── SECURITY.md            # Política de seguridad
├── requirements.txt       # Dependencias Python
├── main.py               # Archivo de ejemplo
├── dependabot_manager.py # Script de gestión de Dependabot
└── README.md            # Este archivo
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

# Instalar dependencias adicionales (usando uv para mayor velocidad)
uv pip install numpy pandas

# O usando pip tradicional
pip install numpy pandas
```

## 📋 Dependencias Incluidas

### Gestión de paquetes
- `uv`: Gestor de paquetes ultrarrápido (10-100x más rápido que pip)
- `pip`: Gestor de paquetes tradicional (como respaldo)

### Herramientas de desarrollo (instaladas por defecto)
- `black`: Formateador de código
- `flake8`: Linter para verificar estilo
- `pylint`: Análisis estático de código
- `pytest`: Framework de testing
- `pytest-cov`: Cobertura de tests
- `python-dotenv`: Manejo de variables de entorno
- `pyyaml`: Para validar configuración de Dependabot

### Dependencias opcionales (comentadas en requirements.txt)
- Científicas: numpy, pandas, matplotlib, jupyter
- Web: fastapi, uvicorn, requests

## ⚙️ Configuraciones Incluidas

- **Formateo automático**: Se ejecuta Black al guardar archivos
- **Organización de imports**: Automática al guardar
- **Puertos expuestos**: 3000, 5000, 8000 para desarrollo web
- **Variables de entorno**: Configuradas para mejor rendimiento Python
- **Cache de pip y uv**: Persistente entre reconstrucciones para máxima velocidad

## 🤖 Dependabot

Este proyecto incluye configuración de Dependabot para mantener las dependencias actualizadas automáticamente:

### Características del Dependabot configurado:
- **Programación**: Revisa dependencias cada lunes a las 9:00 AM (zona horaria Madrid)
- **Límite de PRs**: Máximo 5 pull requests abiertos simultáneamente
- **Agrupación inteligente**: Las dependencias relacionadas se agrupan en un solo PR
- **Auto-merge**: Actualizaciones menores de herramientas de desarrollo se fusionan automáticamente
- **Etiquetas**: PRs marcados con `dependencies` y `python`

### Grupos de dependencias:
- **Desarrollo**: black, flake8, pylint, pytest
- **Científicas**: numpy, pandas, matplotlib, jupyter
- **Web**: fastapi, uvicorn, requests

### Configuración manual:
Para modificar el comportamiento de Dependabot, edita `.github/dependabot.yml`

## ⚡ uv - Gestor de Paquetes Ultrarrápido

Este proyecto incluye `uv`, un gestor de paquetes de Python de última generación que es significativamente más rápido que pip tradicional.

### 🚀 Beneficios de uv:
- **10-100x más rápido** que pip para instalación de paquetes
- **Resolución de dependencias más inteligente** y rápida
- **Compatible con pip** - misma sintaxis, mejores resultados
- **Cache más eficiente** que reduce descargas duplicadas
- **Mejor manejo de conflictos** de dependencias

### 🛠️ Comandos principales:
```bash
# Instalación básica
uv pip install requests fastapi

# Instalación desde requirements.txt
uv pip install -r requirements.txt

# Sincronización exacta (remueve paquetes no listados)
uv pip sync requirements.txt

# Listar paquetes instalados
uv pip list

# Mostrar información de un paquete
uv pip show requests

# Verificar paquetes desactualizados
uv pip list --outdated
```

### 🔄 Migración desde pip:
Si ya tienes un entorno con pip, puedes migrar fácilmente:
```bash
# uv es compatible con pip, simplemente reemplaza el comando
pip install paquete    →    uv pip install paquete
pip freeze            →    uv pip freeze
pip list              →    uv pip list
```

## 📄 Documentación del Proyecto

Este repositorio incluye documentación completa para facilitar la contribución:

### 📋 Archivos de Documentación
- **`LICENSE`**: Licencia MIT del proyecto
- **`CONTRIBUTING.md`**: Guía detallada para contribuir al proyecto
- **`CODE_OF_CONDUCT.md`**: Código de conducta para la comunidad
- **`SECURITY.md`**: Política de seguridad y cómo reportar vulnerabilidades
- **`CODEOWNERS`**: Define los propietarios responsables de diferentes partes del código

### 🎫 Plantillas de GitHub
- **Issues**: Plantillas para reportar bugs, solicitar características, mejorar documentación o pedir ayuda
- **Pull Requests**: Plantilla completa para PRs con checklist de revisión
- **Configuración**: Auto-enlace a discussions y reportes de seguridad

### 🛡️ Características de Seguridad
- **Dependabot Security**: Monitoreo automático de vulnerabilidades
- **Política de Seguridad**: Proceso claro para reportar problemas de seguridad
- **CODEOWNERS**: Control de acceso y revisión obligatoria

## 🔧 Personalización

Para personalizar el entorno:

1. **Agregar dependencias**: Edita `requirements.txt`
2. **Agregar extensiones**: Modifica `.devcontainer/devcontainer.json`
3. **Cambiar configuraciones**: Ajusta las settings en devcontainer.json

## 📝 Comandos Útiles

```bash
# Gestión de paquetes con uv (recomendado - mucho más rápido)
uv pip install nombre-paquete      # Instalar nueva dependencia
uv pip freeze > requirements.txt   # Actualizar requirements.txt
uv pip sync requirements.txt       # Sincronizar entorno exacto

# Gestión de paquetes con pip tradicional (respaldo)
pip install nombre-paquete         # Instalar nueva dependencia
pip freeze > requirements.txt      # Actualizar requirements.txt

# Testing y calidad de código
pytest                             # Ejecutar tests
black .                           # Formatear todo el código
flake8 .                          # Verificar estilo
pylint *.py                       # Análisis con pylint

# Gestión de proyecto
python dependabot_manager.py       # Gestionar dependencias con Dependabot
```

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor lee nuestra [Guía de Contribución](CONTRIBUTING.md) para conocer el proceso.

### Pasos rápidos para contribuir:
1. **Fork** el repositorio
2. **Crea** una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. **Commit** tus cambios (`git commit -m 'feat: agregar nueva característica'`)
4. **Push** a la rama (`git push origin feature/nueva-caracteristica`)
5. **Abre** un Pull Request usando nuestra plantilla

### Tipos de contribución:
- 🐛 **Reportar bugs** usando la [plantilla de bug report](.github/ISSUE_TEMPLATE/bug_report.md)
- 💡 **Solicitar características** usando la [plantilla de feature request](.github/ISSUE_TEMPLATE/feature_request.md)
- 📖 **Mejorar documentación** usando la [plantilla de documentación](.github/ISSUE_TEMPLATE/documentation.md)
- 🆘 **Pedir ayuda** usando la [plantilla de ayuda](.github/ISSUE_TEMPLATE/help.md)

## 🛡️ Seguridad

Para reportar vulnerabilidades de seguridad, por favor sigue nuestras [políticas de seguridad](SECURITY.md). **NO** uses issues públicos para reportar problemas de seguridad.

## 📜 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ve el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Soporte y Comunidad

- 💬 **GitHub Discussions**: Para preguntas generales y discusiones
- 🐛 **Issues**: Para bugs y solicitudes de características
- 🔒 **Seguridad**: Para reportes privados de seguridad
- 📖 **Documentación**: Consulta los archivos MD en el repositorio

---

**¡Tu entorno Python 3.13 está listo para el desarrollo! 🎉**
