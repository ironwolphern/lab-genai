---
applyTo: "**/*.hcl"
---
# Buenas Prácticas para HCL (HashiCorp Configuration Language)

## 1. Estructura y Organización del Código

### 1.1 Organización de Archivos
- **Usa nombres descriptivos para archivos**: `main.tf`, `variables.tf`, `outputs.tf`
- **Separa configuraciones por responsabilidad**: Un archivo por tipo de recurso o módulo
- **Mantén archivos de tamaño manejable**: Máximo 200-300 líneas por archivo
- **Usa estructura de directorios lógica**:
  ```
  project/
  ├── main.tf
  ├── variables.tf
  ├── outputs.tf
  ├── modules/
  │   └── networking/
  └── environments/
      ├── dev/
      └── prod/
  ```

### 1.2 Estructura de Bloques
- **Ordena los bloques de forma consistente**:
  1. `terraform` blocks
  2. `provider` blocks  
  3. `locals` blocks
  4. `data` sources
  5. `resource` blocks
  6. `module` calls

## 2. Convenciones de Nomenclatura

### 2.1 Nombres de Recursos
- **Usa snake_case** para todos los identificadores: `web_server`, `database_subnet`
- **Nombres descriptivos y específicos**: `web_server_sg` en lugar de `sg1`
- **Prefijos consistentes por tipo**: `sg_` para security groups, `subnet_` para subnets
- **Evita abreviaciones confusas**: `security_group` mejor que `sg`

### 2.2 Variables y Outputs
- **Variables en snake_case**: `instance_type`, `vpc_cidr_block`
- **Outputs descriptivos**: `vpc_id`, `database_endpoint`
- **Usa prefijos para agrupar**: `db_username`, `db_password`, `db_endpoint`

## 3. Documentación y Comentarios

### 3.1 Comentarios en el Código
```hcl
# Comentarios de línea para explicaciones breves
/* 
   Comentarios de bloque para 
   explicaciones más extensas
*/

# Crear VPC principal para el entorno de producción
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name        = "${var.project_name}-vpc"
    Environment = var.environment
  }
}
```

### 3.2 Documentación de Variables
```hcl
variable "instance_type" {
  description = "Tipo de instancia EC2 para el servidor web"
  type        = string
  default     = "t3.micro"
  
  validation {
    condition = contains([
      "t3.micro", "t3.small", "t3.medium"
    ], var.instance_type)
    error_message = "El tipo de instancia debe ser t3.micro, t3.small, o t3.medium."
  }
}
```

## 4. Variables y Tipos de Datos

### 4.1 Definición de Variables
- **Especifica siempre el tipo**:
```hcl
variable "vpc_cidr" {
  description = "CIDR block para la VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Lista de zonas de disponibilidad"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b"]
}
```

- **Usa valores por defecto apropiados**
- **Incluye validaciones cuando sea necesario**
- **Agrupa variables relacionadas en objetos**:
```hcl
variable "database_config" {
  description = "Configuración de la base de datos"
  type = object({
    engine         = string
    engine_version = string
    instance_class = string
    allocated_storage = number
  })
}
```

### 4.2 Uso de Locals
- **Define valores calculados en locals**:
```hcl
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    CreatedDate = formatdate("YYYY-MM-DD", timestamp())
  }
  
  vpc_name = "${var.project_name}-${var.environment}-vpc"
}
```

## 5. Recursos y Configuración

### 5.1 Configuración de Recursos
- **Usa tags consistentes**:
```hcl
resource "aws_instance" "web_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  
  tags = merge(local.common_tags, {
    Name = "${local.vpc_name}-web-server"
    Role = "WebServer"
  })
}
```

- **Evita hardcoding de valores**
- **Usa data sources para referencias externas**
- **Implementa count o for_each para recursos similares**

### 5.2 Dependencias
- **Usa referencias implícitas cuando sea posible**:
```hcl
resource "aws_security_group" "web" {
  name_prefix = "${var.project_name}-web-"
  vpc_id      = aws_vpc.main.id  # Dependencia implícita
}
```

- **Usa depends_on solo cuando sea necesario**
- **Evita dependencias circulares**

## 6. Modularización

### 6.1 Creación de Módulos
- **Un módulo por funcionalidad lógica**
- **Interfaz clara con variables y outputs**
- **Documentación completa del módulo**:
```hcl
# modules/networking/main.tf
variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
}

variable "environment" {
  description = "Entorno (dev, staging, prod)"
  type        = string
}

output "vpc_id" {
  description = "ID de la VPC creada"
  value       = aws_vpc.main.id
}
```

### 6.2 Uso de Módulos
- **Versionado de módulos**:
```hcl
module "networking" {
  source = "git::https://github.com/company/terraform-modules.git//networking?ref=v1.2.0"
  
  project_name = var.project_name
  environment  = var.environment
}
```

## 7. Estado y Backend

### 7.1 Configuración de Backend
```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "project/environment/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### 7.2 Gestión del Estado
- **Usa backend remoto para equipos**
- **Implementa bloqueo de estado**
- **Backups regulares del estado**
- **Nunca edites el estado manualmente**

## 8. Seguridad

### 8.1 Manejo de Secretos
- **No hardcodees credenciales**
- **Usa variables de entorno o gestores de secretos**
- **Marca variables sensibles**:
```hcl
variable "database_password" {
  description = "Password para la base de datos"
  type        = string
  sensitive   = true
}
```

### 8.2 Principio de Menor Privilegio
- **Permisos mínimos necesarios**
- **Roles específicos por servicio**
- **Revisión regular de permisos**

## 9. Testing y Validación

### 9.1 Validaciones
```hcl
variable "environment" {
  description = "Entorno de despliegue"
  type        = string
  
  validation {
    condition = contains([
      "dev", "staging", "prod"
    ], var.environment)
    error_message = "Environment debe ser dev, staging, o prod."
  }
}
```

### 9.2 Testing
- **Usa `terraform plan` antes de aplicar**
- **Implementa tests automáticos con Terratest**
- **Validación de sintaxis con `terraform validate`**
- **Formato consistente con `terraform fmt`**

## 10. Performance y Optimización

### 10.1 Paralelización
- **Estructura para aprovechar paralelización automática**
- **Evita dependencias innecesarias**
- **Usa `-parallelism` para ajustar concurrencia**

### 10.2 Gestión de Recursos
- **Usa `lifecycle` rules apropiadamente**:
```hcl
resource "aws_instance" "web" {
  # ... configuración ...
  
  lifecycle {
    create_before_destroy = true
    prevent_destroy       = true
  }
}
```

## 11. Versionado y CI/CD

### 11.1 Control de Versiones
- **Commits atómicos y descriptivos**
- **Tags para releases**
- **Branches por entorno o feature**
- **Pull requests obligatorios**

### 11.2 Integración Continua
```hcl
# .github/workflows/terraform.yml
name: 'Terraform'
on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: hashicorp/setup-terraform@v2
    - run: terraform fmt -check
    - run: terraform init
    - run: terraform validate
    - run: terraform plan
```

## 12. Mantenimiento y Monitoring

### 12.1 Actualizaciones
- **Actualiza providers regularmente**
- **Revisa deprecaciones**
- **Mantén documentación actualizada**
- **Auditoría regular de recursos**

### 12.2 Monitoring
- **Logs de cambios en infraestructura**
- **Alertas para cambios no planificados**
- **Métricas de costos**
- **Health checks de recursos críticos**

## Checklist de Revisión

Antes de hacer commit, verifica:

- [ ] `terraform fmt` ejecutado
- [ ] `terraform validate` pasa
- [ ] `terraform plan` revisado
- [ ] Variables documentadas
- [ ] Outputs definidos
- [ ] Tags aplicados consistentemente
- [ ] No hay valores hardcodeados
- [ ] Secretos manejados apropiadamente
- [ ] Documentación actualizada
- [ ] Tests pasando (si aplica)

## Herramientas Recomendadas

- **Formateo**: `terraform fmt`
- **Validación**: `terraform validate`
- **Linting**: `tflint`
- **Seguridad**: `checkov`, `terrascan`
- **Testing**: `terratest`
- **Documentación**: `terraform-docs`
- **IDE**: VS Code con extensión HashiCorp Terraform

---

*Estas prácticas ayudan a mantener código HCL limpio, mantenible y seguro. Adapta estas recomendaciones según las necesidades específicas de tu proyecto y organización.*
