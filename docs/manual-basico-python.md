# Manual Básico de Python 🐍

## 📋 Índice
1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Sintaxis Básica](#sintaxis-básica)
4. [Variables y Tipos de Datos](#variables-y-tipos-de-datos)
5. [Operadores](#operadores)
6. [Estructuras de Control](#estructuras-de-control)
7. [Funciones](#funciones)
8. [Listas y Colecciones](#listas-y-colecciones)
9. [Manejo de Errores](#manejo-de-errores)
10. [Módulos y Paquetes](#módulos-y-paquetes)

## Introducción

Python es un lenguaje de programación interpretado, de alto nivel y con una sintaxis muy limpia y legible. Es ideal para principiantes y profesionales por igual.

### ¿Por qué Python?
- ✅ Sintaxis simple y clara
- ✅ Gran comunidad y soporte
- ✅ Multiplataforma
- ✅ Amplia biblioteca estándar
- ✅ Versátil (web, IA, datos, automatización)

## Instalación

### Windows
1. Descarga Python desde [python.org](https://www.python.org/downloads/)
2. Ejecuta el instalador
3. **IMPORTANTE**: Marca "Add Python to PATH"

### macOS/Linux
```bash
# macOS con Homebrew
brew install python3

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3
```

### Verificar instalación
```bash
python --version
# o
python3 --version
```

## Sintaxis Básica

### Tu primer programa
```python
# Esto es un comentario
print("¡Hola, mundo!")  # Imprime texto en pantalla
```

### Reglas importantes
- Python usa **indentación** (espacios/tabs) para definir bloques de código
- No necesitas punto y coma (;) al final de las líneas
- Los comentarios empiezan con #

## Variables y Tipos de Datos

### Variables
```python
# No necesitas declarar el tipo
nombre = "Juan"  # String (texto)
edad = 25        # Integer (entero)
altura = 1.75    # Float (decimal)
es_estudiante = True  # Boolean (verdadero/falso)

# Python es dinámicamente tipado
x = 5       # x es int
x = "hola"  # ahora x es string
```

### Tipos de datos básicos
```python
# String (cadenas de texto)
texto = "Hola Python"
texto2 = 'También con comillas simples'
texto_largo = """Texto
en múltiples
líneas"""

# Números
entero = 42
decimal = 3.14
complejo = 2 + 3j

# Boolean
verdadero = True
falso = False

# None (valor nulo)
vacio = None
```

### Conversión de tipos
```python
# str() -> convierte a string
numero = 123
texto = str(numero)  # "123"

# int() -> convierte a entero
texto = "456"
numero = int(texto)  # 456

# float() -> convierte a decimal
numero = float("3.14")  # 3.14

# bool() -> convierte a booleano
print(bool(0))    # False
print(bool(1))    # True
print(bool(""))   # False
print(bool("a"))  # True
```

## Operadores

### Operadores aritméticos
```python
# Básicos
suma = 5 + 3        # 8
resta = 10 - 4      # 6
multiplicacion = 3 * 4  # 12
division = 10 / 3   # 3.333...
division_entera = 10 // 3  # 3
modulo = 10 % 3     # 1 (resto)
potencia = 2 ** 3   # 8
```

### Operadores de comparación
```python
igual = 5 == 5      # True
diferente = 5 != 3  # True
mayor = 5 > 3       # True
menor = 3 < 5       # True
mayor_igual = 5 >= 5  # True
menor_igual = 3 <= 5  # True
```

### Operadores lógicos
```python
# and, or, not
resultado1 = True and False  # False
resultado2 = True or False   # True
resultado3 = not True        # False
```

## Estructuras de Control

### Condicionales (if/elif/else)
```python
edad = 18

if edad >= 18:
    print("Eres mayor de edad")
elif edad >= 13:
    print("Eres adolescente")
else:
    print("Eres menor de edad")

# If en una línea (operador ternario)
mensaje = "Mayor" if edad >= 18 else "Menor"
```

### Bucles

#### Bucle while
```python
contador = 0
while contador < 5:
    print(f"Contador: {contador}")
    contador += 1  # contador = contador + 1
```

#### Bucle for
```python
# Iterar sobre una secuencia
for i in range(5):  # 0, 1, 2, 3, 4
    print(i)

# Iterar sobre una lista
frutas = ["manzana", "banana", "naranja"]
for fruta in frutas:
    print(fruta)

# Enumerate para obtener índice y valor
for indice, fruta in enumerate(frutas):
    print(f"{indice}: {fruta}")
```

### Control de flujo
```python
# break - salir del bucle
for i in range(10):
    if i == 5:
        break
    print(i)  # 0, 1, 2, 3, 4

# continue - saltar a la siguiente iteración
for i in range(5):
    if i == 2:
        continue
    print(i)  # 0, 1, 3, 4

# pass - no hacer nada (placeholder)
if True:
    pass  # TODO: implementar más tarde
```

## Funciones

### Definir funciones
```python
# Función simple
def saludar():
    print("¡Hola!")

# Función con parámetros
def saludar_persona(nombre):
    print(f"¡Hola, {nombre}!")

# Función con valor de retorno
def sumar(a, b):
    return a + b

# Función con parámetros por defecto
def presentarse(nombre, edad=18):
    print(f"Soy {nombre} y tengo {edad} años")

# Llamar funciones
saludar()
saludar_persona("María")
resultado = sumar(5, 3)
presentarse("Juan")  # edad = 18 por defecto
presentarse("Ana", 25)
```

### Funciones avanzadas
```python
# Argumentos variables (*args)
def sumar_todos(*numeros):
    return sum(numeros)

print(sumar_todos(1, 2, 3, 4))  # 10

# Argumentos con nombre (**kwargs)
def crear_perfil(**datos):
    for clave, valor in datos.items():
        print(f"{clave}: {valor}")

crear_perfil(nombre="Juan", edad=25, ciudad="Madrid")

# Funciones lambda (anónimas)
cuadrado = lambda x: x ** 2
print(cuadrado(5))  # 25
```

## Listas y Colecciones

### Listas
```python
# Crear listas
numeros = [1, 2, 3, 4, 5]
mixta = [1, "dos", 3.0, True]
vacia = []

# Acceder a elementos (índice desde 0)
primero = numeros[0]   # 1
ultimo = numeros[-1]   # 5

# Modificar elementos
numeros[0] = 10

# Métodos de lista
numeros.append(6)      # Agregar al final
numeros.insert(0, 0)   # Insertar en posición
numeros.remove(3)      # Eliminar valor
numeros.pop()          # Eliminar y retornar último
numeros.sort()         # Ordenar
numeros.reverse()      # Invertir

# Slicing (rebanadas)
sublista = numeros[1:4]  # elementos del índice 1 al 3
copia = numeros[:]       # copia completa
```

### Tuplas (inmutables)
```python
coordenadas = (10, 20)
x, y = coordenadas  # Desempaquetado
```

### Diccionarios
```python
# Crear diccionarios
persona = {
    "nombre": "Juan",
    "edad": 25,
    "ciudad": "Madrid"
}

# Acceder a valores
nombre = persona["nombre"]
edad = persona.get("edad", 0)  # Con valor por defecto

# Modificar/agregar
persona["edad"] = 26
persona["profesion"] = "Programador"

# Métodos útiles
claves = persona.keys()
valores = persona.values()
items = persona.items()
```

### Sets (conjuntos)
```python
# Crear sets
numeros = {1, 2, 3, 4, 5}
letras = set(['a', 'b', 'c'])

# Operaciones de conjuntos
a = {1, 2, 3}
b = {3, 4, 5}
union = a | b        # {1, 2, 3, 4, 5}
interseccion = a & b # {3}
diferencia = a - b   # {1, 2}
```

### List Comprehensions
```python
# Crear listas de forma concisa
cuadrados = [x**2 for x in range(10)]
pares = [x for x in range(20) if x % 2 == 0]

# Dict comprehension
cuadrados_dict = {x: x**2 for x in range(5)}
```

## Manejo de Errores

### Try/Except
```python
try:
    numero = int(input("Ingresa un número: "))
    resultado = 10 / numero
    print(f"Resultado: {resultado}")
except ValueError:
    print("Error: Debes ingresar un número válido")
except ZeroDivisionError:
    print("Error: No se puede dividir por cero")
except Exception as e:
    print(f"Error inesperado: {e}")
else:
    print("Todo salió bien")
finally:
    print("Esto siempre se ejecuta")
```

### Lanzar excepciones
```python
def validar_edad(edad):
    if edad < 0:
        raise ValueError("La edad no puede ser negativa")
    return edad
```

## Módulos y Paquetes

### Importar módulos
```python
# Importar módulo completo
import math
print(math.pi)
print(math.sqrt(16))

# Importar funciones específicas
from datetime import datetime
ahora = datetime.now()

# Importar con alias
import numpy as np  # (requiere instalación: pip install numpy)

# Importar todo (no recomendado)
from math import *
```

### Crear tu propio módulo
```python
# archivo: mis_funciones.py
def saludar(nombre):
    return f"Hola, {nombre}!"

def despedir(nombre):
    return f"Adiós, {nombre}!"

# archivo: main.py
import mis_funciones
print(mis_funciones.saludar("Juan"))
```

## 🚀 Próximos pasos

### Conceptos intermedios para aprender:
1. **Programación Orientada a Objetos (POO)**
   - Clases y objetos
   - Herencia y polimorfismo
   - Encapsulación

2. **Manejo de archivos**
   ```python
   # Leer archivo
   with open('archivo.txt', 'r') as f:
       contenido = f.read()
   
   # Escribir archivo
   with open('archivo.txt', 'w') as f:
       f.write("Hola mundo")
   ```

3. **Bibliotecas populares**
   - `requests` - Para hacer peticiones HTTP
   - `pandas` - Para análisis de datos
   - `flask/django` - Para desarrollo web
   - `pygame` - Para crear juegos
   - `tkinter` - Para interfaces gráficas

### Recursos recomendados:
- 📚 [Documentación oficial de Python](https://docs.python.org/es/)
- 🎮 [Python Tutor](http://pythontutor.com/) - Visualiza tu código
- 💻 [Repl.it](https://replit.com/) - Practica en línea
- 🎯 [LeetCode](https://leetcode.com/) - Ejercicios de programación
- 📖 [Real Python](https://realpython.com/) - Tutoriales avanzados

### Ejercicio final
```python
# TODO: Crea un programa que:
# 1. Pida el nombre del usuario
# 2. Pida su edad
# 3. Calcule en qué año nació
# 4. Muestre un mensaje personalizado

# Pista:
from datetime import datetime

nombre = input("¿Cómo te llamas? ")
edad = int(input("¿Cuántos años tienes? "))
año_actual = datetime.now().year
año_nacimiento = año_actual - edad

print(f"Hola {nombre}, naciste en el año {año_nacimiento}")
```

## 💡 Consejos finales
1. **Practica todos los días** - La consistencia es clave
2. **Lee código de otros** - Aprende diferentes estilos
3. **Construye proyectos** - Aplica lo que aprendes
4. **No tengas miedo a los errores** - Son parte del aprendizaje
5. **Únete a la comunidad** - Participa en foros y grupos

¡Felicidades! Ya tienes las bases para empezar a programar en Python 🎉