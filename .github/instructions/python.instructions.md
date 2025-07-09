---
applyTo: "**/*.py,**/*.pyi,**/*.pyx,**/*.pxd,**/*.pxi"
---
# Buenas Prácticas de Python

## 1. **Estilo de Código y Formateo**

### 1.1 PEP 8 - Guía de Estilo
- **SIEMPRE** sigue las convenciones de PEP 8
- Usa 4 espacios para indentación (no tabs)
- Limita las líneas a 79 caracteres para código, 72 para comentarios
- Usa líneas en blanco para separar funciones y clases
- Usa espacios alrededor de operadores y después de comas

### 1.2 Nomenclatura
- **Variables y funciones**: `snake_case`
- **Clases**: `PascalCase`
- **Constantes**: `UPPER_SNAKE_CASE`
- **Módulos**: `lowercase` o `snake_case`
- **Privado**: prefijo con un guión bajo `_private_method`

### 1.3 Herramientas de Formateo
- Usa **Black** para formateo automático
- Usa **isort** para ordenar imports
- Usa **flake8** o **pylint** para linting
- Configura pre-commit hooks para automatizar

```python
# Ejemplo de código bien formateado
class UserManager:
    """Manages user operations and authentication."""
    
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self._connection = None
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user with username and password."""
        # Implementation here
        return True
```

## 2. **Estructura de Proyecto**

### 2.1 Organización de Directorios
```
mi-proyecto/
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── .env.example
├── src/
│   └── mi_proyecto/
│       ├── __init__.py
│       ├── main.py
│       ├── models/
│       ├── services/
│       └── utils/
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_models.py
├── docs/
└── scripts/
```

### 2.2 Archivos de Configuración
- `requirements.txt` - Dependencias de producción
- `requirements-dev.txt` - Dependencias de desarrollo
- `setup.py` o `pyproject.toml` - Configuración del paquete
- `.env` - Variables de entorno (no commitear)
- `Makefile` - Comandos comunes automatizados

### 2.3 Gestión de Dependencias
- Usa entornos virtuales (`venv`, `conda`, `poetry`)
- Fija versiones de dependencias críticas
- Separa dependencias de desarrollo y producción
- Usa `pip-tools` o `poetry` para gestión avanzada

## 3. **Tipado y Documentación**

### 3.1 Type Hints
- Usa type hints para mejorar legibilidad y detectar errores
- Importa tipos desde `typing` module
- Usa `mypy` para verificación estática de tipos

```python
from typing import List, Dict, Optional, Union
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
    is_active: bool = True

def get_users(limit: int = 10) -> List[User]:
    """Returns a list of users with optional limit."""
    return []

def process_data(data: Dict[str, Union[str, int]]) -> Optional[str]:
    """Process data and return result or None."""
    return None
```

### 3.2 Docstrings
- Usa docstrings para todas las funciones, clases y módulos públicos
- Sigue el formato Google, NumPy o Sphinx
- Incluye parámetros, tipos de retorno y ejemplos

```python
def calculate_total(items: List[float], tax_rate: float = 0.1) -> float:
    """
    Calculate total price including tax.
    
    Args:
        items: List of item prices
        tax_rate: Tax rate as decimal (default: 0.1 for 10%)
    
    Returns:
        Total price including tax
    
    Raises:
        ValueError: If tax_rate is negative
    
    Example:
        >>> calculate_total([10.0, 20.0], 0.15)
        34.5
    """
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
    
    subtotal = sum(items)
    return subtotal * (1 + tax_rate)
```

## 4. **Manejo de Errores**

### 4.1 Excepciones Específicas
- Captura excepciones específicas, no genéricas
- Usa `finally` para cleanup
- Crea excepciones personalizadas cuando sea necesario

```python
class DatabaseError(Exception):
    """Custom exception for database operations."""
    pass

def connect_to_database(url: str) -> None:
    """Connect to database with proper error handling."""
    try:
        # Connection logic
        connection = create_connection(url)
    except ConnectionError as e:
        raise DatabaseError(f"Failed to connect to database: {e}")
    except ValueError as e:
        raise DatabaseError(f"Invalid database URL: {e}")
    finally:
        # Cleanup resources
        cleanup_resources()
```

### 4.2 Logging
- Usa el módulo `logging` en lugar de `print`
- Configura niveles de logging apropiados
- Incluye información contextual en logs

```python
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def process_user_data(user_id: int) -> None:
    """Process user data with proper logging."""
    logger.info(f"Starting to process user {user_id}")
    
    try:
        # Processing logic
        result = perform_processing(user_id)
        logger.info(f"Successfully processed user {user_id}")
    except Exception as e:
        logger.error(f"Failed to process user {user_id}: {e}")
        raise
```

## 5. **Programación Orientada a Objetos**

### 5.1 Principios SOLID
- **Single Responsibility**: Una clase, una responsabilidad
- **Open/Closed**: Abierto para extensión, cerrado para modificación
- **Liskov Substitution**: Subclases deben ser sustituibles
- **Interface Segregation**: Interfaces específicas, no genéricas
- **Dependency Inversion**: Depende de abstracciones, no concreciones

### 5.2 Uso de Dataclasses y Properties
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    name: str
    price: float
    _discount: float = 0.0
    
    @property
    def discount(self) -> float:
        return self._discount
    
    @discount.setter
    def discount(self, value: float) -> None:
        if not 0 <= value <= 1:
            raise ValueError("Discount must be between 0 and 1")
        self._discount = value
    
    @property
    def final_price(self) -> float:
        return self.price * (1 - self._discount)
```

### 5.3 Context Managers
- Usa context managers para gestión de recursos
- Implementa `__enter__` y `__exit__` o usa `contextlib`

```python
from contextlib import contextmanager

@contextmanager
def database_transaction():
    """Context manager for database transactions."""
    conn = get_connection()
    trans = conn.begin()
    try:
        yield conn
        trans.commit()
    except Exception:
        trans.rollback()
        raise
    finally:
        conn.close()

# Uso
with database_transaction() as conn:
    conn.execute("INSERT INTO users ...")
```

## 6. **Programación Funcional**

### 6.1 Funciones Puras
- Prefiere funciones puras cuando sea posible
- Evita efectos secundarios
- Usa funciones de orden superior

```python
from functools import reduce
from typing import Callable

def apply_discount(price: float, discount: float) -> float:
    """Pure function to apply discount."""
    return price * (1 - discount)

def process_prices(prices: List[float], 
                   processor: Callable[[float], float]) -> List[float]:
    """Higher-order function to process prices."""
    return [processor(price) for price in prices]

# Uso
discounted_prices = process_prices(
    [100, 200, 300], 
    lambda p: apply_discount(p, 0.1)
)
```

### 6.2 Comprehensions y Generadores
- Usa list/dict/set comprehensions para código conciso
- Usa generadores para eficiencia de memoria

```python
# List comprehension
squared_evens = [x**2 for x in range(10) if x % 2 == 0]

# Dictionary comprehension
word_lengths = {word: len(word) for word in ['hello', 'world', 'python']}

# Generator expression
def fibonacci_generator():
    """Generator for Fibonacci sequence."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Uso eficiente de memoria
first_10_fibs = list(itertools.islice(fibonacci_generator(), 10))
```

## 7. **Testing**

### 7.1 Tipos de Tests
- **Unit tests**: Pruebas de funciones/métodos individuales
- **Integration tests**: Pruebas de interacción entre componentes
- **End-to-end tests**: Pruebas del flujo completo

### 7.2 Frameworks de Testing
- Usa `pytest` como framework principal
- Usa `unittest.mock` para mocking
- Implementa fixtures para datos de prueba

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def sample_user():
    """Fixture that provides a sample user."""
    return User(id=1, name="John Doe", email="john@example.com")

def test_user_creation(sample_user):
    """Test user creation with fixture."""
    assert sample_user.name == "John Doe"
    assert sample_user.email == "john@example.com"

@patch('my_module.external_api_call')
def test_api_integration(mock_api_call):
    """Test with mocked external API."""
    mock_api_call.return_value = {"status": "success"}
    
    result = my_function_that_calls_api()
    
    assert result == "success"
    mock_api_call.assert_called_once()
```

### 7.3 Cobertura de Tests
- Mantén cobertura de tests > 80%
- Usa `coverage.py` para medir cobertura
- Incluye tests en CI/CD pipeline

## 8. **Rendimiento y Optimización**

### 8.1 Profiling
- Usa `cProfile` para identificar cuellos de botella
- Usa `memory_profiler` para análisis de memoria
- Mide antes de optimizar

```python
import cProfile
import pstats

def profile_function():
    """Profile a function's performance."""
    pr = cProfile.Profile()
    pr.enable()
    
    # Código a profiler
    expensive_function()
    
    pr.disable()
    stats = pstats.Stats(pr)
    stats.sort_stats('cumulative')
    stats.print_stats()
```

### 8.2 Optimizaciones Comunes
- Usa `collections.defaultdict` y `collections.Counter`
- Usa `set` para lookups rápidos
- Considera `numpy` para operaciones numéricas
- Usa `asyncio` para operaciones I/O

```python
from collections import defaultdict, Counter
import asyncio

# Uso eficiente de estructuras de datos
word_count = Counter(words)
grouped_data = defaultdict(list)

# Programación asíncrona
async def fetch_data(url: str) -> str:
    """Fetch data asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def fetch_multiple_urls(urls: List[str]) -> List[str]:
    """Fetch multiple URLs concurrently."""
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)
```

## 9. **Seguridad**

### 9.1 Validación de Entrada
- Valida y sanitiza todas las entradas
- Usa bibliotecas como `pydantic` para validación
- Evita `eval()` y `exec()`

```python
from pydantic import BaseModel, EmailStr, validator

class UserInput(BaseModel):
    name: str
    email: EmailStr
    age: int
    
    @validator('name')
    def name_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @validator('age')
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v
```

### 9.2 Gestión de Secretos
- Usa variables de entorno para secretos
- Usa `python-dotenv` para desarrollo
- Nunca hardcodees credenciales

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")
```

### 9.3 Prevención de Vulnerabilidades
- Usa `bandit` para análisis de seguridad
- Sanitiza inputs para prevenir inyecciones
- Usa HTTPS para comunicaciones

## 10. **Gestión de Dependencias**

### 10.1 Entornos Virtuales
- **SIEMPRE** usa entornos virtuales
- Usa `venv`, `conda`, o `poetry`
- Documenta cómo recrear el entorno

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 10.2 Poetry (Recomendado)
```toml
[tool.poetry]
name = "mi-proyecto"
version = "0.1.0"
description = "Descripción del proyecto"

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.28.0"
pydantic = "^1.10.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "^22.0.0"
mypy = "^0.991"
```

## 11. **Documentación**

### 11.1 README.md
- Incluye descripción del proyecto
- Instrucciones de instalación y uso
- Ejemplos de código
- Información de contribución

### 11.2 Documentación API
- Usa `sphinx` para documentación completa
- Genera documentación desde docstrings
- Incluye ejemplos de uso

### 11.3 Comentarios en Código
- Comenta el "por qué", no el "qué"
- Mantén comentarios actualizados
- Usa TODO para tareas pendientes

```python
def complex_algorithm(data: List[int]) -> int:
    """
    Complex algorithm that processes data.
    
    This algorithm uses a specific approach because the standard
    library implementation has performance issues with large datasets.
    """
    # TODO: Optimize this section for better performance
    result = 0
    
    # We iterate backwards to avoid index shifting issues
    for i in range(len(data) - 1, -1, -1):
        result += process_item(data[i])
    
    return result
```

## 12. **Herramientas de Desarrollo**

### 12.1 Linting y Formateo
```bash
# Formateo automático
black .
isort .

# Linting
flake8 .
pylint src/

# Type checking
mypy src/
```

### 12.2 Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
```

### 12.3 CI/CD
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest coverage
    - name: Run tests
      run: |
        coverage run -m pytest
        coverage report -m
```

## 13. **Mejores Prácticas Específicas**

### 13.1 Imports
```python
# Orden de imports
import os
import sys
from pathlib import Path

import requests
import numpy as np

from myproject.models import User
from myproject.utils import helper_function
```

### 13.2 Constants y Configuration
```python
# constants.py
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
SUPPORTED_FORMATS = ['json', 'xml', 'yaml']

# config.py
from dataclasses import dataclass
from os import getenv

@dataclass
class Config:
    database_url: str = getenv('DATABASE_URL', 'sqlite:///default.db')
    debug: bool = getenv('DEBUG', 'False').lower() == 'true'
    api_key: str = getenv('API_KEY', '')
```

### 13.3 Error Handling Patterns
```python
from typing import Optional, Union, Tuple

def safe_divide(a: float, b: float) -> Optional[float]:
    """Safe division that returns None on error."""
    try:
        return a / b
    except ZeroDivisionError:
        return None

def divide_with_result(a: float, b: float) -> Tuple[bool, Union[float, str]]:
    """Division that returns success flag and result or error message."""
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, "Division by zero"
```

## 14. **Recursos y Herramientas**

### 14.1 Herramientas Esenciales
- **Formateo**: Black, autopep8
- **Linting**: flake8, pylint, ruff
- **Type checking**: mypy, pyright
- **Testing**: pytest, hypothesis
- **Dependency management**: poetry, pip-tools
- **Security**: bandit, safety

### 14.2 Librerías Útiles
- **CLI**: click, typer, argparse
- **HTTP**: requests, httpx, aiohttp
- **Data**: pandas, numpy, pydantic
- **Database**: SQLAlchemy, databases
- **Config**: python-dotenv, pydantic-settings

---

## Comandos Útiles

```bash
# Setup del proyecto
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Desarrollo
black .
isort .
flake8 .
mypy .
pytest --cov=src

# Publicación
python -m build
python -m twine upload dist/*
```

## Recursos Adicionales

- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Real Python](https://realpython.com/)
- [Python Documentation](https://docs.python.org/3/)
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/)
- [Python Packaging Authority](https://www.pypa.io/)

---

*Última actualización: Junio 2025*
