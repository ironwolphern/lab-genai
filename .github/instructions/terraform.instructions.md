---
applyTo: "**/*.tf,**/*.tfvars,**/*.tfstate"
---
# Buenas Prácticas de Terraform

## 1. **Organización y Estructura de Código**

### 1.1 Estructura de Directorios
- Organiza el código en módulos reutilizables y mantenibles
- Separa entornos (dev, staging, production) en directorios independientes
- Estructura recomendada:
  ```
  proyecto-terraform/
  ├── environments/
  │   ├── dev/
  │   ├── staging/
  │   └── production/
  ├── modules/
  │   ├── vpc/
  │   ├── ec2/
  │   └── rds/
  ├── global/
  └── shared/
  ```

### 1.2 Nomenclatura de Recursos
- Usa nombres descriptivos y consistentes para recursos
- Incluye el entorno en el nombre: `app-prod-web-server`
- Usa guiones bajos para variables y guiones para nombres de recursos
- Mantén consistencia en tags y etiquetas

### 1.3 Archivos de Configuración
- Separa la configuración en archivos lógicos:
  - `main.tf` - Recursos principales
  - `variables.tf` - Definiciones de variables
  - `outputs.tf` - Outputs del módulo
  - `versions.tf` - Versiones de providers
  - `terraform.tf` - Configuración de Terraform

## 2. **Gestión de Estado (State)**

### 2.1 Backend Remoto
- **NUNCA** uses el backend local para proyectos en equipo
- Configura un backend remoto (S3, Terraform Cloud, Azure Storage)
- Habilita el versionado del estado
- Configura el bloqueo de estado para evitar conflictos

### 2.2 Aislamiento del Estado
- Mantén estados separados por entorno
- Usa workspaces para separación lógica cuando sea apropiado
- Evita compartir estado entre proyectos no relacionados

### 2.3 Seguridad del Estado
- Cifra el estado en reposo y en tránsito
- Controla el acceso al estado usando IAM/RBAC
- No almacenes secretos en el estado cuando sea posible

## 3. **Versionado y Dependencias**

### 3.1 Versiones de Providers
- **SIEMPRE** especifica versiones de providers con constraints
- Usa versionado semántico: `~> 4.0` para actualizaciones menores
- Documenta cambios breaking en actualizaciones
- Ejemplo:
  ```hcl
  terraform {
    required_providers {
      aws = {
        source  = "hashicorp/aws"
        version = "~> 4.0"
      }
    }
    required_version = ">= 1.0"
  }
  ```

### 3.2 Versiones de Módulos
- Versionado de módulos con tags Git
- Usa versionado semántico para módulos
- Especifica versiones exactas en producción

## 4. **Desarrollo de Módulos**

### 4.1 Principio de Responsabilidad Única
- Cada módulo debe tener una función específica y bien definida
- Mantén módulos pequeños y enfocados
- Haz módulos reutilizables entre proyectos

### 4.2 Interfaz de Módulos
- Define inputs y outputs claramente
- Usa variables tipadas con validación
- Proporciona valores por defecto sensatos
- Ejemplo:
  ```hcl
  variable "instance_type" {
    description = "EC2 instance type"
    type        = string
    default     = "t3.micro"
    validation {
      condition     = contains(["t3.micro", "t3.small", "t3.medium"], var.instance_type)
      error_message = "Instance type must be t3.micro, t3.small, or t3.medium."
    }
  }
  ```

### 4.3 Documentación de Módulos
- Incluye un `README.md` completo en cada módulo
- Documenta todos los inputs, outputs y ejemplos de uso
- Usa terraform-docs para generar documentación automática

## 5. **Variables y Configuración**

### 5.1 Jerarquía de Variables
- Usa archivos `.tfvars` para configuraciones específicas de entorno
- Mantén variables sensibles en archivos separados
- Usa variables de entorno para secretos: `TF_VAR_`

### 5.2 Tipos de Variables
- Especifica tipos de variables explícitamente
- Usa objetos complejos cuando sea apropiado
- Implementa validación de variables
- Ejemplo:
  ```hcl
  variable "vpc_config" {
    description = "VPC configuration"
    type = object({
      cidr_block           = string
      enable_dns_hostnames = bool
      enable_dns_support   = bool
    })
  }
  ```

### 5.3 Gestión de Secretos
- **NUNCA** hardcodees secretos en el código
- Usa sistemas de gestión de secretos (AWS Secrets Manager, HashiCorp Vault)
- Considera usar `sensitive = true` para outputs sensibles

## 6. **Seguridad**

### 6.1 Principio de Menor Privilegio
- Usa roles y políticas IAM específicas para Terraform
- Evita usar credenciales de administrador
- Implementa assume roles para acceso cross-account

### 6.2 Validación de Recursos
- Usa data sources para validar recursos existentes
- Implementa precondiciones con `lifecycle` rules
- Valida configuraciones antes de aplicar

### 6.3 Compliance y Políticas
- Implementa políticas de compliance (Sentinel, OPA)
- Usa herramientas de escaneo de seguridad (Checkov, tfsec)
- Mantén estándares de seguridad consistentes

## 7. **Testing y Validación**

### 7.1 Validación de Sintaxis
- Usa `terraform fmt` para formateo consistente
- Ejecuta `terraform validate` antes de commits
- Implementa `terraform plan` en CI/CD

### 7.2 Testing Automatizado
- Implementa tests unitarios con Terratest
- Usa `terraform-compliance` para tests de compliance
- Ejecuta tests de integración en entornos de prueba

### 7.3 Análisis Estático
- Usa herramientas como tflint, tfsec, checkov
- Implementa análisis de seguridad automático
- Integra herramientas en pipelines CI/CD

## 8. **CI/CD y Automatización**

### 8.1 Pipeline de Deployment
- Implementa un pipeline con etapas claras:
  1. Validación y formato
  2. Planning
  3. Revisión manual
  4. Apply
- Usa `terraform plan` para validación antes de merge

### 8.2 Automatización Segura
- Nunca ejecutes `terraform apply` sin revisión en producción
- Implementa aprobaciones manuales para cambios críticos
- Usa drift detection para detectar cambios externos

### 8.3 Rollback y Recuperación
- Mantén un plan de rollback para cambios críticos
- Usa import para recuperar recursos huérfanos
- Implementa backups de estado antes de cambios importantes

## 9. **Performance y Optimización**

### 9.1 Paralelización
- Configura paralelismo apropiado: `terraform apply -parallelism=10`
- Evita dependencias innecesarias entre recursos
- Usa `depends_on` solo cuando sea necesario

### 9.2 Estado Eficiente
- Minimiza el tamaño del estado
- Usa `terraform refresh` cuando sea necesario
- Considera state splitting para proyectos grandes

### 9.3 Providers y Recursos
- Usa aliases de providers para multi-region
- Evita recursos que no agregan valor
- Implementa resource targeting cuando sea apropiado

## 10. **Monitoreo y Logging**

### 10.1 Logging
- Habilita logging detallado para debugging: `TF_LOG=DEBUG`
- Mantén logs de ejecuciones de CI/CD
- Usa structured logging cuando sea posible

### 10.2 Drift Detection
- Implementa drift detection regular
- Monitorea cambios no planificados en infraestructura
- Configura alertas para cambios críticos

### 10.3 Métricas
- Rastrea tiempo de ejecución de plans y applies
- Monitorea tasa de éxito de deployments
- Implementa métricas de cobertura de infraestructura

## 11. **Gestión de Datos**

### 11.1 Data Sources
- Usa data sources para referenciar recursos existentes
- Evita hardcodear ARNs o IDs de recursos
- Implementa validación en data sources

### 11.2 Locals
- Usa locals para cálculos complejos y reutilización
- Mantén locals simples y legibles
- Documenta locals complejos

### 11.3 Outputs
- Expone outputs útiles para otros módulos
- Usa outputs para debugging y validación
- Implementa outputs sensibles apropiadamente

## 12. **Colaboración en Equipo**

### 12.1 Estándares de Código
- Establece y documenta estándares de codificación
- Usa pre-commit hooks para validaciones
- Implementa code reviews obligatorios

### 12.2 Documentación
- Mantén documentación de arquitectura actualizada
- Documenta decisiones de diseño importantes
- Incluye runbooks para operaciones comunes

### 12.3 Formación y Conocimiento
- Proporciona formación en Terraform al equipo
- Mantén guías de mejores prácticas internas
- Facilita sesiones de knowledge sharing

## 13. **Migración y Evolución**

### 13.1 Migraciones de Estado
- Planifica migraciones de estado cuidadosamente
- Usa `terraform state mv` para reorganizar estado
- Mantén backups antes de migraciones

### 13.2 Refactoring
- Refactoriza código regularmente para mantener calidad
- Usa `terraform import` para recursos existentes
- Implementa cambios incrementales

### 13.3 Upgrades
- Mantén Terraform y providers actualizados
- Prueba upgrades en entornos no productivos
- Documenta procesos de upgrade

## 14. **Herramientas y Ecosistema**

### 14.1 Herramientas Recomendadas
- **Formateo**: terraform fmt, prettier-plugin-terraform
- **Linting**: tflint, terraform validate
- **Seguridad**: tfsec, checkov, terrascan
- **Testing**: terratest, terraform-compliance
- **Documentación**: terraform-docs

### 14.2 Integración IDE
- Usa extensiones de Terraform para tu IDE
- Configura syntax highlighting y autocompletion
- Implementa snippets para patrones comunes

---

## Comandos Útiles

```bash
# Formateo y validación
terraform fmt -recursive
terraform validate
terraform plan -out=tfplan

# Análisis de seguridad
tfsec .
checkov -d .

# Documentación
terraform-docs markdown table . > README.md

# Debugging
TF_LOG=DEBUG terraform apply
```

## Recursos Adicionales

- [Documentación Oficial de Terraform](https://www.terraform.io/docs/)
- [Terraform Registry](https://registry.terraform.io/)
- [Terraform Best Practices by Gruntwork](https://www.gruntwork.io/guides/terraform/)
- [HashiCorp Learn Terraform](https://learn.hashicorp.com/terraform)

---

*Última actualización: Junio 2025*
