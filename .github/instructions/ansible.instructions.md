---
applyTo: "**/*.yml,**/*.yaml"
---
# Buenas Prácticas de Ansible

## 1. **Organización y Estructura de Proyectos**

### 1.1 Estructura de Directorios
- Utiliza una estructura de directorios consistente y bien organizada
- Separa playbooks, roles, variables e inventarios en directorios específicos
- Ejemplo de estructura recomendada:
  ```
  proyecto-ansible/
  ├── ansible.cfg
  ├── site.yml
  ├── inventories/
  │   ├── production/
  │   └── staging/
  ├── group_vars/
  ├── host_vars/
  ├── roles/
  └── playbooks/
  ```

### 1.2 Nomenclatura
- Usa nombres descriptivos y consistentes para playbooks, roles y variables
- Utiliza guiones bajos (`_`) para variables y guiones (`-`) para nombres de archivos
- Evita abreviaciones confusas
- Usa sintaxis de modulos fqcn (fully qualified collection name) para evitar conflictos de nombres

## 2. **Gestión de Variables**

### 2.1 Jerarquía de Variables
- Comprende y utiliza correctamente la jerarquía de precedencia de variables
- Usa `group_vars/` y `host_vars/` para organizar variables por grupos y hosts
- Define variables por defecto en roles usando `defaults/main.yml`

### 2.2 Cifrado de Datos Sensibles
- **SIEMPRE** usa Ansible Vault para datos sensibles (contraseñas, claves API, certificados)
- No commitees datos sensibles sin cifrar en control de versiones
- Usa archivos vault separados para diferentes entornos

### 2.3 Variables Booleanas
- Usa valores booleanos explícitos (`true`/`false`) en lugar de `yes`/`no`
- Sé consistente en el uso de booleanos en todo el proyecto

## 3. **Desarrollo de Playbooks**

### 3.1 Idempotencia
- **FUNDAMENTAL**: Asegúrate de que todos los playbooks sean idempotentes
- Los playbooks deben poder ejecutarse múltiples veces sin efectos adversos
- Usa módulos que soporten idempotencia naturalmente

### 3.2 Estructura de Tareas
- Mantén las tareas simples y enfocadas en una sola responsabilidad
- Usa nombres descriptivos para todas las tareas
- Agrupa tareas relacionadas lógicamente

### 3.3 Manejo de Errores
- Implementa manejo de errores apropiado con `ignore_errors`, `failed_when`, `rescue`
- Usa `block`/`rescue`/`always` para control de flujo complejo
- Valida precondiciones antes de ejecutar tareas críticas

## 4. **Desarrollo de Roles**

### 4.1 Principio de Responsabilidad Única
- Cada rol debe tener una responsabilidad específica y bien definida
- Evita roles monolíticos que hagan demasiadas cosas
- Haz los roles reutilizables y parametrizables

### 4.2 Estructura de Roles
- Usa la estructura estándar de Ansible Galaxy:
  ```
  roles/
  └── nombre-rol/
      ├── tasks/main.yml
      ├── handlers/main.yml
      ├── defaults/main.yml
      ├── vars/main.yml
      ├── files/
      ├── templates/
      ├── meta/main.yml
      └── README.md
  ```

### 4.3 Documentación de Roles
- Incluye siempre un `README.md` detallado en cada rol
- Documenta todas las variables, dependencias y ejemplos de uso
- Mantén actualizada la metadata en `meta/main.yml`

## 5. **Inventarios y Configuración**

### 5.1 Inventarios Dinámicos
- Usa inventarios dinámicos cuando sea posible (cloud providers, CMDB)
- Mantén inventarios estáticos simples y organizados por entornos
- Usa grupos lógicos para organizar hosts

### 5.2 Configuración de Ansible
- Utiliza `ansible.cfg` para configuraciones específicas del proyecto
- Configura timeout, paralelismo y otras opciones según necesidades
- Documenta configuraciones no estándar

## 6. **Seguridad**

### 6.1 Control de Acceso
- Usa el principio de menor privilegio
- Evita ejecutar tareas como root cuando no sea necesario
- Implementa `become` de manera granular, no global

### 6.2 Conexiones Seguras
- Usa SSH con autenticación por clave
- Configura SSH correctamente (deshabilita autenticación por contraseña)
- Considera usar jump hosts para acceso a redes privadas

### 6.3 Validación de Entrada
- Valida variables de entrada usando `assert`
- Sanitiza datos antes de usarlos en comandos shell
- Usa módulos específicos en lugar de `shell`/`command` cuando sea posible

## 7. **Testing y Validación**

### 7.1 Sintaxis y Lint
- Usa `ansible-lint` para verificar mejores prácticas
- Valida sintaxis con `ansible-playbook --syntax-check`
- Implementa hooks de pre-commit para validaciones automáticas

### 7.2 Testing de Roles
- Implementa tests usando Molecule
- Prueba roles en múltiples distribuciones y versiones
- Incluye tests de idempotencia

### 7.3 Dry Run
- Siempre ejecuta `--check` antes de aplicar cambios en producción
- Usa `--diff` para ver qué cambios se aplicarán
- Implementa un proceso de validación en staging

## 8. **Control de Versiones**

### 8.1 Git Best Practices
- Usa commits descriptivos y atómicos
- Implementa un flujo de trabajo con branches (GitFlow, GitHub Flow)
- Tagea releases de manera consistente

### 8.2 Gestión de Dependencias
- Especifica versiones de roles externos en `requirements.yml`
- Usa roles de Ansible Galaxy de fuentes confiables
- Mantén un lockfile de dependencias

## 9. **Performance y Optimización**

### 9.1 Paralelización
- Configura `forks` apropiadamente según tu infraestructura
- Usa `serial` para deployments controlados
- Implementa `async` para tareas de larga duración

### 9.2 Cacheo
- Habilita fact caching para evitar gathering repetitivo
- Usa `gather_facts: false` cuando no necesites facts
- Implementa cacheo de roles y playbooks cuando sea apropiado

### 9.3 Módulos Eficientes
- Prefiere módulos nativos sobre `shell`/`command`
- Usa `lineinfile` en lugar de `sed` en scripts
- Evita loops innecesarios, usa módulos que soporten listas

## 10. **Monitoreo y Logging**

### 10.1 Logging
- Configura logging apropiado en `ansible.cfg`
- Usa callbacks para logging estructurado
- Mantén logs de ejecuciones importantes

### 10.2 Métricas
- Monitorea tiempo de ejecución de playbooks
- Rastrea éxito/fallo de ejecuciones
- Implementa alertas para fallos críticos

## 11. **Documentación y Mantenimiento**

### 11.1 Documentación
- Mantén documentación actualizada del proyecto
- Documenta procedimientos de deployment
- Incluye diagramas de arquitectura cuando sea necesario

### 11.2 Mantenimiento
- Revisa y actualiza roles regularmente
- Mantén Ansible y módulos actualizados
- Implementa un proceso de deprecación para código obsoleto

## 12. **Colaboración en Equipo**

### 12.1 Estándares de Codificación
- Establece y documenta estándares de codificación del equipo
- Usa herramientas de formateo consistentes
- Implementa revisiones de código (code reviews)

### 12.2 Conocimiento Compartido
- Facilita sesiones de knowledge sharing
- Documenta decisiones arquitecturales importantes
- Mantén un runbook para operaciones comunes

---

## Recursos Adicionales

- [Documentación Oficial de Ansible](https://docs.ansible.com/)
- [Ansible Lint](https://ansible-lint.readthedocs.io/)
- [Molecule Testing Framework](https://molecule.readthedocs.io/)
- [Ansible Galaxy](https://galaxy.ansible.com/)

---

*Última actualización: Junio 2025*
