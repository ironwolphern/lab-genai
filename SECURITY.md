# Política de Seguridad

## Versiones Compatibles

Actualmente brindamos soporte de seguridad para las siguientes versiones:

| Versión | Soporte de Seguridad     |
| ------- | ------------------------ |
| 1.0.x   | ✅ Completamente soportada |
| 0.9.x   | ⚠️ Soporte limitado       |
| < 0.9   | ❌ No soportada           |

## Reportar una Vulnerabilidad

La seguridad de nuestro proyecto es una prioridad. Si descubres una vulnerabilidad de seguridad, 
agradecemos tu ayuda para divulgarla de manera responsable.

### 🔒 Reporte Privado

**NO** reportes vulnerabilidades de seguridad a través de issues públicos de GitHub.

En su lugar, usa una de estas opciones:

#### Opción 1: GitHub Security Advisories (Recomendado)
1. Ve a la pestaña "Security" del repositorio
2. Haz clic en "Report a vulnerability"
3. Completa el formulario con los detalles de la vulnerabilidad

#### Opción 2: Email Privado
Envía un email a: **security@lab-genai.org** (o el email del mantenedor)

### 📋 Información a Incluir

Por favor incluye la siguiente información en tu reporte:

- **Tipo de vulnerabilidad** (ej. buffer overflow, SQL injection, cross-site scripting, etc.)
- **Ubicación completa** del código fuente afectado (tag/branch/commit o URL directo)
- **Configuración especial** requerida para reproducir el issue
- **Pasos detallados** para reproducir la vulnerabilidad
- **Prueba de concepto** o código de explotación (si es posible)
- **Impacto potencial** de la vulnerabilidad, incluyendo cómo un atacante podría explotarla

### ⏱️ Proceso de Respuesta

| Tiempo | Acción |
|--------|--------|
| < 24 horas | Confirmación de recepción del reporte |
| < 72 horas | Evaluación inicial y clasificación de severidad |
| < 7 días | Plan de corrección y cronograma de lanzamiento |
| < 30 días | Lanzamiento de parche de seguridad |

#### Severidad de Vulnerabilidades

Clasificamos las vulnerabilidades usando el sistema CVSS v3.1:

- **🔴 Crítica (9.0-10.0)**: Corrección inmediata, hotfix en < 24 horas
- **🟠 Alta (7.0-8.9)**: Corrección en < 7 días
- **🟡 Media (4.0-6.9)**: Corrección en < 30 días
- **🟢 Baja (0.1-3.9)**: Corrección en próximo release menor

### 🎯 Vulnerabilidades en el Alcance

Estas vulnerabilidades están dentro del alcance de nuestro programa:

- **Ejecución remota de código**
- **Inyección SQL**
- **Cross-Site Scripting (XSS)**
- **Cross-Site Request Forgery (CSRF)**
- **Escalación de privilegios**
- **Exposición de información sensible**
- **Bypass de autenticación/autorización**
- **Vulnerabilidades en dependencias críticas**

### ❌ Fuera del Alcance

Estas NO se consideran vulnerabilidades de seguridad:

- Vulnerabilidades en versiones no soportadas
- Issues que requieren acceso físico al dispositivo
- Ataques de fuerza bruta sin mitigaciones adicionales
- Vulnerabilidades en software de terceros (repórtalas al upstream)
- Issues de usabilidad o UX
- Spam o abuso de funcionalidades

### 🏆 Reconocimiento

Agradecemos a los investigadores de seguridad responsables. Los reportes válidos recibirán:

- **Reconocimiento público** en nuestro archivo SECURITY.md (si lo deseas)
- **Crédito** en las notas de lanzamiento de la corrección
- **Badge de reconocimiento** en tu perfil de GitHub (cuando esté disponible)

#### Hall of Fame de Seguridad

Agradecemos a estos investigadores por ayudar a mejorar la seguridad de lab-genai:

- *Tu nombre podría estar aquí* 🎉

### 🛡️ Medidas de Seguridad Implementadas

Este proyecto implementa las siguientes medidas de seguridad:

#### Desarrollo Seguro
- ✅ **Análisis estático de código** con Pylint y Flake8
- ✅ **Revisión de código** obligatoria antes de merge
- ✅ **Tests automatizados** incluyendo casos de seguridad
- ✅ **Dependabot** para actualizaciones automáticas de seguridad

#### Dependencias
- ✅ **Escaneo automático** de vulnerabilidades en dependencias
- ✅ **Actualizaciones automáticas** de parches de seguridad
- ✅ **Pinning de versiones** en requirements.txt
- ✅ **Revisión manual** de dependencias críticas

#### Infraestructura
- ✅ **Contenedores inmutables** con Dev Containers
- ✅ **Principio de menor privilegio** en configuraciones
- ✅ **Variables de entorno** para configuración sensible
- ✅ **Logs de auditoría** en acciones críticas

### 📖 Recursos Adicionales

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/archive/2023/2023_top25_list.html)
- [Python Security Best Practices](https://python.org/dev/security/)
- [GitHub Security Lab](https://securitylab.github.com/)

### 📞 Contacto

Para cualquier pregunta sobre esta política de seguridad:

- 📧 **Email**: security@lab-genai.org
- 🔐 **PGP Key**: [ID de clave PGP si aplica]
- 💬 **Discusiones**: Para preguntas generales (NO vulnerabilidades)

---

**Gracias por ayudar a mantener lab-genai seguro!** 🛡️

*Última actualización: Julio 2025*
