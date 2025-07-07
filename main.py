#!/usr/bin/env python3
"""
Archivo de ejemplo para probar el entorno de desarrollo Python 3.13
"""

import sys
from typing import List


def saludar(nombre: str) -> str:
    """
    Función de ejemplo que saluda a una persona.

    Args:
        nombre: El nombre de la persona a saludar

    Returns:
        Un mensaje de saludo personalizado
    """
    return f"¡Hola, {nombre}! Bienvenido a Python 3.13"


def obtener_info_python() -> dict:
    """
    Obtiene información sobre la versión de Python actual.

    Returns:
        Diccionario con información del sistema Python
    """
    return {
        "version": sys.version,
        "version_info": sys.version_info,
        "executable": sys.executable,
    }


def main() -> None:
    """Función principal del programa."""
    print("🐍 Entorno de desarrollo Python 3.13")
    print("=" * 40)

    # Probar la función de saludo
    nombres: List[str] = ["Desarrollador", "IA Assistant"]
    for nombre in nombres:
        print(saludar(nombre))

    print("\n📊 Información del sistema Python:")
    info = obtener_info_python()
    for clave, valor in info.items():
        print(f"  {clave}: {valor}")


if __name__ == "__main__":
    main()
