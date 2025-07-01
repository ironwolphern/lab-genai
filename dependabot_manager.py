#!/usr/bin/env python3
"""
Script de utilidad para gestionar actualizaciones de Dependabot
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import List, Dict


def run_command(command: str) -> tuple[int, str]:
    """Ejecuta un comando del sistema y devuelve el código de salida y la salida."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, str(e)


def check_dependabot_config() -> bool:
    """Verifica que la configuración de Dependabot sea válida."""
    dependabot_file = Path(".github/dependabot.yml")
    
    if not dependabot_file.exists():
        print("❌ No se encontró el archivo .github/dependabot.yml")
        return False
    
    print("✅ Archivo de configuración de Dependabot encontrado")
    
    # Verificar sintaxis YAML
    try:
        import yaml
        with open(dependabot_file, 'r') as f:
            yaml.safe_load(f.read())
        print("✅ Sintaxis YAML válida")
        return True
    except ImportError:
        print("⚠️  No se puede verificar sintaxis YAML (instalar pyyaml)")
        return True
    except Exception as e:
        print(f"❌ Error en sintaxis YAML: {e}")
        return False


def list_dependencies() -> List[str]:
    """Lista las dependencias actuales del proyecto."""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ No se encontró requirements.txt")
        return []
    
    dependencies = []
    with open(requirements_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Extraer nombre del paquete
                pkg_name = line.split('==')[0].split('>=')[0].split('<=')[0]
                dependencies.append(pkg_name)
    
    return dependencies


def check_outdated_packages() -> Dict[str, str]:
    """Verifica qué paquetes están desactualizados."""
    print("🔍 Verificando paquetes desactualizados...")
    
    code, output = run_command("pip list --outdated --format=json")
    
    if code != 0:
        print(f"❌ Error al verificar paquetes: {output}")
        return {}
    
    try:
        outdated_packages = json.loads(output)
        result = {}
        for pkg in outdated_packages:
            result[pkg['name']] = f"{pkg['version']} -> {pkg['latest_version']}"
        return result
    except json.JSONDecodeError:
        print("❌ Error al parsear la salida de pip list")
        return {}


def main():
    """Función principal del script."""
    print("🤖 Gestor de Dependabot para lab-genai")
    print("=" * 40)
    
    # Verificar configuración
    if not check_dependabot_config():
        sys.exit(1)
    
    # Listar dependencias
    dependencies = list_dependencies()
    print(f"\n📦 Dependencias encontradas: {len(dependencies)}")
    for dep in dependencies:
        print(f"  - {dep}")
    
    # Verificar paquetes desactualizados
    outdated = check_outdated_packages()
    if outdated:
        print(f"\n⬆️  Paquetes desactualizados: {len(outdated)}")
        for pkg, versions in outdated.items():
            print(f"  - {pkg}: {versions}")
    else:
        print("\n✅ Todos los paquetes están actualizados")
    
    # Información sobre Dependabot
    print("\n🔧 Comandos útiles de GitHub CLI:")
    print("  - Ver PRs de Dependabot: gh pr list --author 'dependabot[bot]'")
    print("  - Fusionar PR específico: gh pr merge <número> --squash")
    print("  - Ver estado del repositorio: gh repo view --web")
    
    print("\n✨ ¡Dependabot está configurado y listo!")


if __name__ == "__main__":
    main()
