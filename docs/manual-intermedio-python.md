# Manual Intermedio de Python 🚀

## 📋 Índice
1. [Programación Orientada a Objetos](#programación-orientada-a-objetos)
2. [Decoradores](#decoradores)
3. [Generators y Yield](#generators-y-yield)
4. [Context Managers](#context-managers)
5. [Type Hints y Anotaciones](#type-hints-y-anotaciones)
6. [Dataclasses](#dataclasses)
7. [Pattern Matching](#pattern-matching)
8. [Programación Asíncrona](#programación-asíncrona)
9. [Expresiones Regulares](#expresiones-regulares)
10. [Testing](#testing)

## Programación Orientada a Objetos

### Clases y Objetos
```python
class Persona:
    # Variable de clase (compartida por todas las instancias)
    especie = "Homo sapiens"
    
    # Constructor
    def __init__(self, nombre, edad):
        # Atributos de instancia
        self.nombre = nombre
        self.edad = edad
        self._email = None  # Atributo "privado" (convención)
        self.__id = id(self)  # Atributo "muy privado" (name mangling)
    
    # Método de instancia
    def presentarse(self):
        return f"Hola, soy {self.nombre} y tengo {self.edad} años"
    
    # Método de clase
    @classmethod
    def crear_bebe(cls, nombre):
        return cls(nombre, 0)
    
    # Método estático
    @staticmethod
    def es_mayor_edad(edad):
        return edad >= 18
    
    # Propiedades (getters y setters)
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, valor):
        if "@" in valor:
            self._email = valor
        else:
            raise ValueError("Email inválido")
    
    # Métodos especiales (magic methods)
    def __str__(self):
        return f"Persona({self.nombre}, {self.edad})"
    
    def __repr__(self):
        return f"Persona(nombre='{self.nombre}', edad={self.edad})"
    
    def __eq__(self, otra):
        return self.nombre == otra.nombre and self.edad == otra.edad
    
    def __lt__(self, otra):
        return self.edad < otra.edad

# Uso
juan = Persona("Juan", 25)
print(juan.presentarse())
juan.email = "juan@email.com"
bebe = Persona.crear_bebe("María")
```

### Herencia
```python
class Empleado(Persona):
    def __init__(self, nombre, edad, salario, puesto):
        super().__init__(nombre, edad)  # Llamar al constructor padre
        self.salario = salario
        self.puesto = puesto
    
    # Sobrescribir método
    def presentarse(self):
        base = super().presentarse()
        return f"{base}. Trabajo como {self.puesto}"
    
    # Nuevo método
    def calcular_salario_anual(self):
        return self.salario * 12

# Herencia múltiple
class Habilidades:
    def __init__(self):
        self.habilidades = []
    
    def agregar_habilidad(self, habilidad):
        self.habilidades.append(habilidad)

class Desarrollador(Empleado, Habilidades):
    def __init__(self, nombre, edad, salario, lenguajes):
        Empleado.__init__(self, nombre, edad, salario, "Desarrollador")
        Habilidades.__init__(self)
        self.lenguajes = lenguajes

# MRO (Method Resolution Order)
print(Desarrollador.__mro__)
```

### Polimorfismo y Abstracción
```python
from abc import ABC, abstractmethod

# Clase abstracta
class Vehiculo(ABC):
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
    
    @abstractmethod
    def arrancar(self):
        pass
    
    @abstractmethod
    def detener(self):
        pass

class Coche(Vehiculo):
    def arrancar(self):
        return "El coche está arrancando... 🚗"
    
    def detener(self):
        return "El coche se ha detenido"

class Moto(Vehiculo):
    def arrancar(self):
        return "La moto está arrancando... 🏍️"
    
    def detener(self):
        return "La moto se ha detenido"

# Polimorfismo en acción
vehiculos = [Coche("Toyota", "Corolla"), Moto("Honda", "CBR")]
for v in vehiculos:
    print(v.arrancar())  # Mismo método, diferente comportamiento
```

### Composición vs Herencia
```python
# Composición: "tiene un" en lugar de "es un"
class Motor:
    def __init__(self, cilindros, potencia):
        self.cilindros = cilindros
        self.potencia = potencia
    
    def encender(self):
        return f"Motor de {self.cilindros} cilindros encendido"

class Coche:
    def __init__(self, marca, motor):
        self.marca = marca
        self.motor = motor  # Composición
    
    def arrancar(self):
        return f"{self.marca}: {self.motor.encender()}"

# Uso
motor_v8 = Motor(8, 400)
mustang = Coche("Ford Mustang", motor_v8)
```

## Decoradores

### Decoradores básicos
```python
# Decorador simple
def cronometrar(func):
    import time
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"{func.__name__} tardó {fin - inicio:.4f} segundos")
        return resultado
    return wrapper

@cronometrar
def operacion_lenta():
    import time
    time.sleep(1)
    return "Completado"

# Decorador con parámetros
def repetir(veces):
    def decorador(func):
        def wrapper(*args, **kwargs):
            for i in range(veces):
                resultado = func(*args, **kwargs)
            return resultado
        return wrapper
    return decorador

@repetir(3)
def saludar():
    print("¡Hola!")

# Múltiples decoradores
@cronometrar
@repetir(2)
def proceso():
    print("Procesando...")
```

### Decoradores avanzados
```python
from functools import wraps

# Preservar metadatos de la función
def mi_decorador(func):
    @wraps(func)  # Preserva __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        """Esta es la función wrapper"""
        return func(*args, **kwargs)
    return wrapper

# Decorador de clase
def singleton(cls):
    instancias = {}
    def get_instancia(*args, **kwargs):
        if cls not in instancias:
            instancias[cls] = cls(*args, **kwargs)
        return instancias[cls]
    return get_instancia

@singleton
class BaseDatos:
    def __init__(self):
        print("Creando conexión a BD")

# Decorador con estado
class ContadorLlamadas:
    def __init__(self, func):
        self.func = func
        self.contador = 0
    
    def __call__(self, *args, **kwargs):
        self.contador += 1
        print(f"Llamada #{self.contador} a {self.func.__name__}")
        return self.func(*args, **kwargs)

@ContadorLlamadas
def funcion():
    print("Ejecutando función")
```

## Generators y Yield

### Generators básicos
```python
# Generator function
def numeros_pares(n):
    for i in range(n):
        if i % 2 == 0:
            yield i  # Produce un valor y pausa

# Uso
gen = numeros_pares(10)
print(next(gen))  # 0
print(next(gen))  # 2

# Iterar sobre generator
for num in numeros_pares(10):
    print(num)

# Generator expression
cuadrados_gen = (x**2 for x in range(10))

# Generator infinito
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Usar con itertools
from itertools import islice
primeros_10_fib = list(islice(fibonacci(), 10))
```

### Generators avanzados
```python
# send() method
def acumulador():
    total = 0
    while True:
        valor = yield total
        if valor is not None:
            total += valor

acc = acumulador()
next(acc)  # Inicializar
print(acc.send(10))  # 10
print(acc.send(20))  # 30

# yield from
def generador_combinado():
    yield from range(3)
    yield from "ABC"
    yield from [10, 20, 30]

# Generator con manejo de recursos
def leer_archivo_grande(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        for linea in f:
            yield linea.strip()

# Pipeline de generators
def leer_numeros(archivo):
    with open(archivo) as f:
        for linea in f:
            yield int(linea.strip())

def filtrar_pares(numeros):
    for num in numeros:
        if num % 2 == 0:
            yield num

def elevar_al_cuadrado(numeros):
    for num in numeros:
        yield num ** 2

# Uso del pipeline
# numeros = leer_numeros("numeros.txt")
# pares = filtrar_pares(numeros)
# cuadrados = elevar_al_cuadrado(pares)
# for resultado in cuadrados:
#     print(resultado)
```

## Context Managers

### Usando with statement
```python
# Context manager básico
class MiArchivo:
    def __init__(self, nombre, modo):
        self.nombre = nombre
        self.modo = modo
        self.archivo = None
    
    def __enter__(self):
        print(f"Abriendo {self.nombre}")
        self.archivo = open(self.nombre, self.modo)
        return self.archivo
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Cerrando {self.nombre}")
        if self.archivo:
            self.archivo.close()
        # Retornar False propaga la excepción
        return False

# Uso
with MiArchivo("test.txt", "w") as f:
    f.write("Hola mundo")

# contextlib
from contextlib import contextmanager

@contextmanager
def tiempo_ejecucion(nombre):
    import time
    print(f"Iniciando {nombre}")
    inicio = time.time()
    try:
        yield
    finally:
        fin = time.time()
        print(f"{nombre} tardó {fin - inicio:.4f} segundos")

with tiempo_ejecucion("proceso"):
    import time
    time.sleep(1)
```

### Context managers avanzados
```python
from contextlib import contextmanager, ExitStack, suppress

# Múltiples context managers
with ExitStack() as stack:
    archivos = [
        stack.enter_context(open(f"archivo{i}.txt", "w"))
        for i in range(3)
    ]
    for i, f in enumerate(archivos):
        f.write(f"Archivo {i}")

# Suprimir excepciones
with suppress(FileNotFoundError):
    with open("no_existe.txt") as f:
        contenido = f.read()

# Context manager reutilizable
class ConexionBD:
    def __init__(self, host, puerto):
        self.host = host
        self.puerto = puerto
        self.conexion = None
    
    def __enter__(self):
        print(f"Conectando a {self.host}:{self.puerto}")
        # Simular conexión
        self.conexion = f"Conexión a {self.host}"
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Cerrando conexión")
        self.conexion = None
    
    def ejecutar(self, query):
        return f"Ejecutando: {query}"

# Uso
with ConexionBD("localhost", 5432) as db:
    resultado = db.ejecutar("SELECT * FROM usuarios")
```

## Type Hints y Anotaciones

### Type hints básicos
```python
from typing import List, Dict, Tuple, Optional, Union, Any

# Funciones con type hints
def saludar(nombre: str) -> str:
    return f"Hola, {nombre}"

def dividir(a: float, b: float) -> float:
    return a / b

# Colecciones tipadas
def procesar_numeros(numeros: List[int]) -> Dict[str, float]:
    return {
        "suma": sum(numeros),
        "promedio": sum(numeros) / len(numeros),
        "maximo": max(numeros)
    }

# Optional y Union
def buscar_usuario(id: int) -> Optional[Dict[str, Any]]:
    # Retorna dict o None
    if id > 0:
        return {"id": id, "nombre": "Usuario"}
    return None

def procesar_dato(dato: Union[str, int]) -> str:
    if isinstance(dato, int):
        return f"Número: {dato}"
    return f"Texto: {dato}"

# Tuplas tipadas
def obtener_coordenadas() -> Tuple[float, float]:
    return (10.5, 20.3)

# Callable
from typing import Callable

def aplicar_operacion(
    numeros: List[int],
    operacion: Callable[[int], int]
) -> List[int]:
    return [operacion(n) for n in numeros]
```

### Type hints avanzados
```python
from typing import TypeVar, Generic, Protocol, Literal, Final, TypedDict

# Type variables
T = TypeVar('T')

def primer_elemento(lista: List[T]) -> Optional[T]:
    return lista[0] if lista else None

# Clases genéricas
class Pila(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> Optional[T]:
        return self._items.pop() if self._items else None

# Protocols (interfaces)
class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...

def ordenar_elementos(items: List[Comparable]) -> List[Comparable]:
    return sorted(items)

# TypedDict
class PersonaDict(TypedDict):
    nombre: str
    edad: int
    email: Optional[str]

def crear_persona(datos: PersonaDict) -> str:
    return f"{datos['nombre']} ({datos['edad']} años)"

# Literal types
from typing import Literal

def mover(direccion: Literal["arriba", "abajo", "izquierda", "derecha"]) -> str:
    return f"Moviendo {direccion}"

# Final
PI: Final[float] = 3.14159
```

## Dataclasses

### Dataclasses básicas
```python
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Producto:
    nombre: str
    precio: float
    stock: int = 0
    categorias: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo")
    
    def valor_inventario(self) -> float:
        return self.precio * self.stock

# Dataclass inmutable
@dataclass(frozen=True)
class Punto:
    x: float
    y: float
    
    def distancia_al_origen(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

# Dataclass con orden
@dataclass(order=True)
class Persona:
    sort_index: int = field(init=False, repr=False)
    nombre: str
    edad: int
    email: Optional[str] = None
    
    def __post_init__(self):
        self.sort_index = self.edad

# Herencia con dataclasses
@dataclass
class Empleado(Persona):
    salario: float
    fecha_contrato: datetime = field(default_factory=datetime.now)
```

### Dataclasses avanzadas
```python
from dataclasses import dataclass, field, asdict, astuple, replace
import json

@dataclass
class Configuracion:
    host: str = "localhost"
    puerto: int = 8000
    debug: bool = False
    opciones: dict = field(default_factory=dict)
    
    def to_json(self) -> str:
        return json.dumps(asdict(self))
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Configuracion':
        return cls(**json.loads(json_str))
    
    def actualizar(self, **kwargs) -> 'Configuracion':
        return replace(self, **kwargs)

# Uso
config = Configuracion(debug=True)
config_json = config.to_json()
nueva_config = config.actualizar(puerto=9000)

# Dataclass con validación compleja
@dataclass
class Usuario:
    username: str
    email: str
    edad: int
    _password_hash: str = field(init=False, repr=False)
    
    def __post_init__(self):
        self._validar_email()
        self._validar_edad()
    
    def _validar_email(self):
        if "@" not in self.email:
            raise ValueError("Email inválido")
    
    def _validar_edad(self):
        if not 0 < self.edad < 150:
            raise ValueError("Edad inválida")
    
    def set_password(self, password: str):
        import hashlib
        self._password_hash = hashlib.sha256(password.encode()).hexdigest()
```

## Pattern Matching

### Match básico (Python 3.10+)
```python
def procesar_comando(comando):
    match comando.split():
        case ["salir" | "exit" | "quit"]:
            return "Adiós!"
        case ["ayuda" | "help"]:
            return "Comandos disponibles: salir, ayuda, ir <lugar>"
        case ["ir", lugar]:
            return f"Yendo a {lugar}"
        case ["ir", direccion, "rápido"]:
            return f"Yendo {direccion} rápidamente"
        case _:
            return "Comando no reconocido"

# Pattern matching con tipos
def procesar_dato(dato):
    match dato:
        case int(n) if n > 0:
            return f"Entero positivo: {n}"
        case int(n) if n < 0:
            return f"Entero negativo: {n}"
        case float(f):
            return f"Decimal: {f}"
        case str(s):
            return f"Texto: {s}"
        case [x, y]:
            return f"Lista de 2 elementos: {x}, {y}"
        case [x, *resto]:
            return f"Lista con {len(resto) + 1} elementos"
        case {"nombre": nombre, "edad": edad}:
            return f"Persona: {nombre}, {edad} años"
        case _:
            return "Tipo no reconocido"
```

### Pattern matching avanzado
```python
from dataclasses import dataclass

@dataclass
class Punto:
    x: float
    y: float

@dataclass
class Circulo:
    centro: Punto
    radio: float

@dataclass
class Rectangulo:
    esquina: Punto
    ancho: float
    alto: float

def calcular_area(figura):
    match figura:
        case Circulo(centro=_, radio=r):
            return 3.14159 * r ** 2
        case Rectangulo(esquina=_, ancho=w, alto=h):
            return w * h
        case Punto():
            return 0
        case _:
            raise ValueError("Figura no reconocida")

# Pattern matching con guardas
def clasificar_triangulo(a, b, c):
    match (a, b, c):
        case (x, y, z) if x == y == z:
            return "Equilátero"
        case (x, y, z) if x == y or y == z or x == z:
            return "Isósceles"
        case (x, y, z) if x + y > z and x + z > y and y + z > x:
            return "Escaleno"
        case _:
            return "No es un triángulo válido"

# Pattern matching anidado
def procesar_respuesta(respuesta):
    match respuesta:
        case {"status": 200, "data": {"usuarios": usuarios}}:
            return f"Éxito: {len(usuarios)} usuarios"
        case {"status": 404}:
            return "No encontrado"
        case {"status": code, "error": mensaje}:
            return f"Error {code}: {mensaje}"
        case _:
            return "Respuesta inválida"
```

## Programación Asíncrona

### Async/Await básico
```python
import asyncio
import aiohttp
from typing import List

# Función asíncrona básica
async def saludar_asincrono(nombre: str, delay: int):
    print(f"Saludando a {nombre}...")
    await asyncio.sleep(delay)
    print(f"¡Hola, {nombre}!")
    return f"Saludo a {nombre} completado"

# Ejecutar múltiples tareas
async def main():
    # Ejecutar concurrentemente
    resultados = await asyncio.gather(
        saludar_asincrono("Juan", 2),
        saludar_asincrono("María", 1),
        saludar_asincrono("Pedro", 3)
    )
    print(resultados)

# Ejecutar
# asyncio.run(main())

# Manejo de excepciones asíncronas
async def tarea_riesgosa():
    await asyncio.sleep(1)
    raise ValueError("Algo salió mal")

async def ejecutar_con_manejo():
    try:
        await tarea_riesgosa()
    except ValueError as e:
        print(f"Error capturado: {e}")
```

### Async avanzado
```python
# Async context manager
class ConexionAsincrona:
    async def __aenter__(self):
        print("Abriendo conexión asíncrona")
        await asyncio.sleep(1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Cerrando conexión asíncrona")
        await asyncio.sleep(0.5)
    
    async def consultar(self, query: str):
        await asyncio.sleep(0.1)
        return f"Resultado de: {query}"

# Async iterator
class ContadorAsincrono:
    def __init__(self, limite):
        self.limite = limite
        self.contador = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.contador < self.limite:
            await asyncio.sleep(0.1)
            self.contador += 1
            return self.contador
        raise StopAsyncIteration

# Async generator
async def generar_numeros(n):
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i

# Uso
async def usar_async_features():
    # Context manager
    async with ConexionAsincrona() as conn:
        resultado = await conn.consultar("SELECT * FROM usuarios")
    
    # Iterator
    async for num in ContadorAsincrono(5):
        print(f"Contador: {num}")
    
    # Generator
    async for num in generar_numeros(3):
        print(f"Generado: {num}")

# Tareas con timeout
async def tarea_lenta():
    await asyncio.sleep(10)
    return "Completado"

async def con_timeout():
    try:
        resultado = await asyncio.wait_for(tarea_lenta(), timeout=3.0)
    except asyncio.TimeoutError:
        print("La tarea tardó demasiado")

# Producer-Consumer pattern
async def productor(queue: asyncio.Queue, n: int):
    for i in range(n):
        await asyncio.sleep(0.5)
        await queue.put(f"item_{i}")
        print(f"Producido: item_{i}")

async def consumidor(queue: asyncio.Queue, nombre: str):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"{nombre} consumió: {item}")
        await asyncio.sleep(1)
        queue.task_done()

async def main_producer_consumer():
    queue = asyncio.Queue(maxsize=3)
    
    # Crear tareas
    prod = asyncio.create_task(productor(queue, 5))
    cons1 = asyncio.create_task(consumidor(queue, "Consumidor-1"))
    cons2 = asyncio.create_task(consumidor(queue, "Consumidor-2"))
    
    # Esperar al productor
    await prod
    
    # Señalar fin
    await queue.put(None)
    await queue.put(None)
    
    # Esperar a consumidores
    await asyncio.gather(cons1, cons2)
```

## Expresiones Regulares

### Regex básico
```python
import re

# Búsqueda simple
texto = "Mi email es usuario@ejemplo.com y mi teléfono es 123-456-7890"

# findall - encuentra todas las coincidencias
emails = re.findall(r'\b[\w.-]+@[\w.-]+\.\w+\b', texto)
print(emails)  # ['usuario@ejemplo.com']

# search - encuentra la primera coincidencia
match = re.search(r'\d{3}-\d{3}-\d{4}', texto)
if match:
    print(f"Teléfono encontrado: {match.group()}")

# match - coincidencia al inicio
if re.match(r'Mi', texto):
    print("El texto empieza con 'Mi'")

# Grupos de captura
patron_fecha = r'(\d{2})/(\d{2})/(\d{4})'
fecha = "Hoy es 25/12/2025"
match = re.search(patron_fecha, fecha)
if match:
    dia, mes, año = match.groups()
    print(f"Día: {dia}, Mes: {mes}, Año: {año}")

# Substitución
texto_limpio = re.sub(r'\d{3}-\d{3}-\d{4}', 'XXX-XXX-XXXX', texto)
print(texto_limpio)
```

### Regex avanzado
```python
# Compilar patrones para reutilizar
patron_email = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    re.IGNORECASE
)

def validar_email(email):
    return bool(patron_email.match(email))

# Named groups
patron_log = re.compile(
    r'(?P<fecha>\d{4}-\d{2}-\d{2}) '
    r'(?P<hora>\d{2}:\d{2}:\d{2}) '
    r'\[(?P<nivel>\w+)\] '
    r'(?P<mensaje>.*)'
)

log = "2025-01-15 10:30:45 [ERROR] Fallo en la conexión"
match = patron_log.match(log)
if match:
    info = match.groupdict()
    print(f"Nivel: {info['nivel']}, Mensaje: {info['mensaje']}")

# Lookahead y lookbehind
# Positive lookahead (?=...)
patron_password = re.compile(
    r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
)

# Negative lookbehind (?<!...)
# Encontrar números no precedidos por $
numeros = re.findall(r'(?<!\$)\d+', "Precio: $50, Cantidad: 30")

# Non-capturing groups (?:...)
patron_telefono = re.compile(r'(?:\+34)?(\d{9})')

# Flags útiles
texto_multilinea = """
Primera línea
Segunda línea
Tercera línea
"""

# re.MULTILINE - ^ y $ funcionan por línea
lineas = re.findall(r'^.*línea$', texto_multilinea, re.MULTILINE)

# re.DOTALL - . incluye saltos de línea
todo = re.search(r'Primera.*línea', texto_multilinea, re.DOTALL)

# Split avanzado
partes = re.split(r'[,;]', "python,java;javascript,go")
print(partes)  # ['python', 'java', 'javascript', 'go']

# Función de reemplazo
def capitalizar_palabras(match):
    return match.group(0).upper()

texto = "python es genial"
resultado = re.sub(r'\b\w+\b', capitalizar_palabras, texto)
print(resultado)  # PYTHON ES GENIAL
```

## Testing

### Unit Testing con pytest
```python
# archivo: calculadora.py
class Calculadora:
    def sumar(self, a: float, b: float) -> float:
        return a + b
    
    def dividir(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("División por cero")
        return a / b
    
    def calcular_promedio(self, numeros: list) -> float:
        if not numeros:
            raise ValueError("Lista vacía")
        return sum(numeros) / len(numeros)

# archivo: test_calculadora.py
import pytest
from calculadora import Calculadora

class TestCalculadora:
    @pytest.fixture
    def calc(self):
        """Fixture que proporciona una instancia de Calculadora"""
        return Calculadora()
    
    def test_sumar(self, calc):
        assert calc.sumar(2, 3) == 5
        assert calc.sumar(-1, 1) == 0
        assert calc.sumar(0.1, 0.2) == pytest.approx(0.3)
    
    def test_dividir(self, calc):
        assert calc.dividir(10, 2) == 5
        assert calc.dividir(-10, 2) == -5
    
    def test_dividir_por_cero(self, calc):
        with pytest.raises(ValueError, match="División por cero"):
            calc.dividir(10, 0)
    
    @pytest.mark.parametrize("numeros,esperado", [
        ([1, 2, 3, 4, 5], 3),
        ([10], 10),
        ([-1, 0, 1], 0),
        ([2.5, 2.5], 2.5)
    ])
    def test_calcular_promedio(self, calc, numeros, esperado):
        assert calc.calcular_promedio(numeros) == esperado
    
    def test_promedio_lista_vacia(self, calc):
        with pytest.raises(ValueError, match="Lista vacía"):
            calc.calcular_promedio([])
```

### Testing avanzado
```python
# Mocking
from unittest.mock import Mock, patch, MagicMock
import requests

class ServicioAPI:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def obtener_usuario(self, user_id):
        response = requests.get(f"{self.base_url}/users/{user_id}")
        response.raise_for_status()
        return response.json()
    
    def crear_usuario(self, datos):
        response = requests.post(f"{self.base_url}/users", json=datos)
        response.raise_for_status()
        return response.json()

# Tests con mocking
class TestServicioAPI:
    @patch('requests.get')
    def test_obtener_usuario(self, mock_get):
        # Configurar mock
        mock_response = Mock()
        mock_response.json.return_value = {"id": 1, "nombre": "Juan"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Probar
        servicio = ServicioAPI("https://api.ejemplo.com")
        usuario = servicio.obtener_usuario(1)
        
        # Verificar
        assert usuario["nombre"] == "Juan"
        mock_get.assert_called_once_with("https://api.ejemplo.com/users/1")
    
    @patch('requests.post')
    def test_crear_usuario(self, mock_post):
        # Configurar mock
        datos_entrada = {"nombre": "María", "email": "maria@ejemplo.com"}
        mock_response = Mock()
        mock_response.json.return_value = {"id": 2, **datos_entrada}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # Probar
        servicio = ServicioAPI("https://api.ejemplo.com")
        usuario = servicio.crear_usuario(datos_entrada)
        
        # Verificar
        assert usuario["id"] == 2
        mock_post.assert_called_once_with(
            "https://api.ejemplo.com/users",
            json=datos_entrada
        )

# Fixtures avanzadas
@pytest.fixture(scope="module")
def conexion_db():
    """Fixture de alcance de módulo para conexión a BD"""
    print("Estableciendo conexión a BD")
    conn = {"conexion": "activa"}
    yield conn
    print("Cerrando conexión a BD")

@pytest.fixture
def usuario_prueba(conexion_db):
    """Fixture que depende de otra fixture"""
    usuario = {"id": 1, "nombre": "Test User", "db": conexion_db}
    return usuario

# Marcadores personalizados
@pytest.mark.slow
def test_operacion_lenta():
    import time
    time.sleep(2)
    assert True

@pytest.mark.skip(reason="No implementado aún")
def test_funcionalidad_futura():
    pass

@pytest.mark.skipif(
    sys.version_info < (3, 10),
    reason="Requiere Python 3.10+"
)
def test_pattern_matching():
    match [1, 2, 3]:
        case [x, y, z]:
            assert x == 1

# Property-based testing con hypothesis
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_promedio_propiedades(numeros):
    if numeros:
        calc = Calculadora()
        promedio = calc.calcular_promedio(numeros)
        assert min(numeros) <= promedio <= max(numeros)
        assert promedio == sum(numeros) / len(numeros)

# Test de integración asíncrono
@pytest.mark.asyncio
async def test_servicio_asincrono():
    async with ConexionAsincrona() as conn:
        resultado = await conn.consultar("SELECT 1")
        assert resultado is not None
```

## 🚀 Mejores Prácticas y Consejos

### Principios SOLID en Python
```python
# Single Responsibility Principle
class UsuarioServicio:
    def crear_usuario(self, datos): pass

class UsuarioValidador:
    def validar(self, datos): pass

# Open/Closed Principle
from abc import ABC, abstractmethod

class Procesador(ABC):
    @abstractmethod
    def procesar(self, datos): pass

class ProcesadorJSON(Procesador):
    def procesar(self, datos):
        return json.dumps(datos)

# Liskov Substitution Principle
class Ave:
    def mover(self): pass

class Pinguino(Ave):
    def mover(self):
        return "Nadar"

# Interface Segregation Principle
class Leible(Protocol):
    def leer(self): ...

class Escribible(Protocol):
    def escribir(self, datos): ...

# Dependency Inversion Principle
class Servicio:
    def __init__(self, repositorio: Repository):
        self.repositorio = repositorio
```

### Performance Tips
```python
# Usar generadores para grandes datasets
def procesar_archivo_grande(archivo):
    with open(archivo) as f:
        for linea in f:  # No carga todo en memoria
            yield procesar_linea(linea)

# List comprehension es más rápido
# Lento
resultado = []
for i in range(1000):
    if i % 2 == 0:
        resultado.append(i ** 2)

# Rápido
resultado = [i ** 2 for i in range(1000) if i % 2 == 0]

# Usar sets para búsquedas rápidas
elementos = set(range(10000))
if 5000 in elementos:  # O(1) en lugar de O(n)
    print("Encontrado")

# Cachear resultados costosos
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

## 📚 Recursos para Profundizar

### Libros recomendados:
- 📖 "Fluent Python" - Luciano Ramalho
- 📖 "Effective Python" - Brett Slatkin
- 📖 "Python Tricks" - Dan Bader

### Frameworks y librerías importantes:
- 🌐 **Web**: FastAPI, Django, Flask
- 📊 **Data Science**: pandas, numpy, scikit-learn
- 🤖 **Machine Learning**: TensorFlow, PyTorch
- 🧪 **Testing**: pytest, hypothesis, tox
- 📦 **Async**: asyncio, aiohttp, httpx

### Herramientas de desarrollo:
- 🔧 **Linting**: pylint, flake8, black
- 📝 **Type Checking**: mypy, pyright
- 📈 **Profiling**: cProfile, memory_profiler
- 🐛 **Debugging**: pdb, ipdb

¡Felicidades! Ahora tienes una base sólida en conceptos intermedios de Python 🎯