---
applyTo: "**/*.md"
---
# Buenas Prácticas de Markdown

## 1. **Estructura y Formato**

### 1.1 Títulos y Jerarquía
- Usa un solo H1 por documento
- Mantén la jerarquía secuencial (H1 → H2 → H3)
- Deja líneas en blanco antes y después de los títulos

```markdown
# ✅ Título Principal (H1)

## ✅ Sección Principal (H2)

### ✅ Subsección (H3)

#### ✅ Sub-subsección (H4)

# ❌ Evita múltiples H1
```

### 1.2 Espaciado y Líneas en Blanco
```markdown
# ✅ Espaciado correcto

## Sección con espaciado apropiado

Este párrafo tiene líneas en blanco antes y después.

Otro párrafo separado correctamente.

- Lista con espaciado
- Segundo elemento

## Siguiente Sección

Contenido de la siguiente sección.


# ❌ Evita espaciado excesivo



## ❌ Evita falta de espaciado
Texto pegado al título.
```

### 1.3 Longitud de Línea
```markdown
# ✅ Líneas de longitud razonable (70-80 caracteres)
Este párrafo mantiene una longitud de línea razonable que es fácil de 
leer tanto en el editor como en el resultado renderizado.

# ❌ Líneas muy largas
Este párrafo tiene una línea extremadamente larga que es difícil de leer en el editor y puede causar problemas de renderizado en diferentes dispositivos y aplicaciones.
```

## 2. **Texto y Formato**

### 2.1 Énfasis y Formato
```markdown
# ✅ Uso correcto de énfasis
Texto con **negrita** para énfasis fuerte.
Texto con *cursiva* para énfasis suave.
Texto con ***negrita y cursiva*** para énfasis muy fuerte.

# ✅ Código inline
Usa `código inline` para comandos, variables y fragmentos cortos.

# ❌ Evita uso excesivo
**Todo** *el* ***texto*** `no` **debe** *estar* ***formateado***.
```

### 2.2 Listas
```markdown
# ✅ Listas ordenadas
1. Primer elemento
2. Segundo elemento
3. Tercer elemento
   - Sub-elemento
   - Otro sub-elemento

# ✅ Listas no ordenadas
- Elemento principal
- Otro elemento principal
  - Sub-elemento indentado
  - Otro sub-elemento
    - Sub-sub-elemento

# ✅ Listas de tareas
- [x] Tarea completada
- [ ] Tarea pendiente
- [ ] Otra tarea pendiente

# ❌ Evita inconsistencias
- Elemento con guión
* Elemento con asterisco
+ Elemento con plus
```

### 2.3 Enlaces y Referencias
```markdown
# ✅ Enlaces inline
Visita [GitHub](https://github.com) para más información.

# ✅ Enlaces de referencia
Consulta la [documentación oficial][docs] y el [repositorio][repo].

[docs]: https://docs.example.com
[repo]: https://github.com/example/repo

# ✅ Enlaces automáticos
<https://example.com>
<email@example.com>

# ✅ Enlaces internos
Ver [sección anterior](#estructura-y-formato) para más detalles.

# ❌ Evita URLs desnudas en texto
Visita https://example.com para más información.
```

## 3. **Código y Sintaxis**

### 3.1 Bloques de Código
```markdown
# ✅ Bloques de código con sintaxis específica
```python
def hello_world():
    print("Hello, World!")
    return True
```

```javascript
function helloWorld() {
    console.log("Hello, World!");
    return true;
}
```

```bash
# Comandos de shell
ls -la
cd /path/to/directory
```

# ✅ Código sin sintaxis específica
```
Texto plano o código genérico
sin resaltado de sintaxis específico
```

# ❌ Evita bloques sin especificar lenguaje cuando sea posible
```
def hello():
    print("Hello")
```
```

### 3.2 Código Inline
```markdown
# ✅ Código inline apropiado
Usa el comando `git status` para verificar el estado.
La variable `username` debe ser una cadena.
Ejecuta `npm install` para instalar dependencias.

# ✅ Código inline con caracteres especiales
Para mostrar backticks, usa ``código con `backticks` dentro``.

# ❌ Evita código inline innecesario
El `archivo` se encuentra en la `carpeta` del `proyecto`.
```

## 4. **Imágenes y Multimedia**

### 4.1 Imágenes
```markdown
# ✅ Imágenes con texto alternativo descriptivo
![Diagrama de arquitectura del sistema](images/architecture-diagram.png)

# ✅ Imágenes con enlaces
[![Logo del proyecto](images/logo.png)](https://project-website.com)

# ✅ Imágenes de referencia
![Logo][logo]

[logo]: images/logo.png "Logo de la aplicación"

# ✅ Imágenes con dimensiones (si el renderizador lo soporta)
<img src="images/screenshot.png" alt="Captura de pantalla" width="500">

# ❌ Evita texto alternativo genérico
![imagen](screenshot.png)
![](logo.png)
```

### 4.2 Multimedia
```markdown
# ✅ Enlaces a videos
[▶️ Ver video tutorial](https://youtube.com/watch?v=example)

# ✅ Embed de videos (donde sea soportado)
[![Video Tutorial](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://youtube.com/watch?v=VIDEO_ID)

# ✅ Audio y otros medios
[🎵 Archivo de audio](audio/example.mp3)
```

## 5. **Tablas**

### 5.1 Estructura de Tablas
```markdown
# ✅ Tablas bien formateadas
| Nombre     | Edad | Ciudad      |
|------------|------|-------------|
| Ana        | 25   | Madrid      |
| Carlos     | 30   | Barcelona   |
| María      | 28   | Valencia    |

# ✅ Tablas con alineación
| Producto      | Precio | Disponible |
|:------------- |-------:| :---------:|
| Laptop        | €1,200 |     ✅     |
| Mouse         |   €25  |     ❌     |
| Teclado       |   €80  |     ✅     |

# ✅ Tablas complejas
| Característica | Básico | Premium | Enterprise |
|----------------|--------|---------|------------|
| Usuarios       | 5      | 50      | Ilimitado  |
| Almacenamiento | 1GB    | 100GB   | 1TB        |
| Soporte        | Email  | Chat    | 24/7       |
```

### 5.2 Alternativas para Tablas Complejas
```markdown
# ✅ Cuando las tablas son muy complejas, considera HTML
<table>
  <thead>
    <tr>
      <th rowspan="2">Producto</th>
      <th colspan="2">Precio</th>
    </tr>
    <tr>
      <th>Normal</th>
      <th>Descuento</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Laptop</td>
      <td>€1,200</td>
      <td>€1,000</td>
    </tr>
  </tbody>
</table>
```

## 6. **Citas y Referencias**

### 6.1 Citas en Bloque
```markdown
# ✅ Citas simples
> Esta es una cita importante que queremos destacar.

# ✅ Citas múltiples
> Primera línea de la cita.
> Segunda línea de la cita.
> Tercera línea de la cita.

# ✅ Citas anidadas
> Cita principal
> > Cita dentro de la cita
> > > Cita anidada más profunda

# ✅ Citas con formato
> **Nota importante:** Esta información es crítica para el proyecto.
> 
> Asegúrate de seguir todos los pasos mencionados.

# ✅ Citas con autor
> "La simplicidad es la máxima sofisticación."
> 
> — Leonardo da Vinci
```

### 6.2 Notas al Pie
```markdown
# ✅ Notas al pie (donde sea soportado)
Este concepto es fundamental[^1] para entender el framework.

[^1]: Ver documentación oficial para más detalles.

# ✅ Notas múltiples
Markdown[^md] es un lenguaje de marcado[^markup] muy popular.

[^md]: Creado por John Gruber en 2004
[^markup]: Lenguaje que usa etiquetas para estructurar texto
```

## 7. **Organización y Estructura**

### 7.1 Índice de Contenidos
```markdown
# ✅ Índice manual
## Índice
1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
   - [Configuración básica](#configuración-básica)
   - [Configuración avanzada](#configuración-avanzada)
4. [Uso](#uso)
5. [Troubleshooting](#troubleshooting)

# ✅ Índice automático (donde sea soportado)
<!-- TOC -->
```

### 7.2 Secciones y Separadores
```markdown
# ✅ Separadores horizontales
## Sección 1
Contenido de la primera sección.

---

## Sección 2  
Contenido de la segunda sección.

***

## Sección 3
Contenido de la tercera sección.

# ✅ Saltos de página (donde sea soportado)
<div style="page-break-after: always;"></div>
```

## 8. **Extensiones y Características Especiales**

### 8.1 Elementos Expandibles
```markdown
# ✅ Detalles expandibles (HTML)
<details>
<summary>Haz clic para expandir</summary>

Contenido que se muestra cuando se expande.

```python
def ejemplo():
    return "código oculto"
```

</details>
```

### 8.2 Alertas y Admoniciones
```markdown
# ✅ Usando blockquotes con emojis
> ⚠️ **Advertencia:** Esta operación no se puede deshacer.

> ℹ️ **Información:** Consulta la documentación para más detalles.

> ✅ **Éxito:** La operación se completó correctamente.

> ❌ **Error:** Se produjo un problema durante la ejecución.

# ✅ Usando HTML para styling especial
<div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px;">
⚠️ <strong>Advertencia:</strong> Esta función está en desarrollo.
</div>
```

### 8.3 Comentarios
```markdown
# ✅ Comentarios HTML (no se renderizan)
<!-- Este es un comentario que no aparece en el resultado -->

# ✅ Comentarios para colaboradores
<!-- TODO: Añadir más ejemplos aquí -->
<!-- FIXME: Revisar la información de la sección 3 -->
<!-- NOTE: Esta sección necesita actualización -->
```

## 9. **Compatibilidad y Portabilidad**

### 9.1 Características Estándar
```markdown
# ✅ Usa características universalmente soportadas
- Títulos con #
- Listas con - o *
- Enlaces con [texto](url)
- Código con ```
- Énfasis con * o **

# ⚠️ Verifica compatibilidad antes de usar
- Tablas avanzadas
- Notas al pie
- Elementos HTML
- Extensiones específicas
```

### 9.2 Fallbacks
```markdown
# ✅ Proporciona alternativas
## Opción 1: Tabla Markdown
| Col1 | Col2 |
|------|------|
| A    | B    |

## Opción 2: Lista cuando las tablas no funcionan
- **Col1:** A, **Col2:** B
- **Col1:** C, **Col2:** D
```

## 10. **Mantenimiento y Documentación**

### 10.1 Metadatos
```markdown
# ✅ Información del documento
---
title: "Guía de Buenas Prácticas"
author: "Tu Nombre"
date: "2025-06-19"
version: "1.0"
tags: ["markdown", "documentación", "guía"]
---

# ✅ Encabezados de archivo
<!--
Archivo: buenas-practicas-markdown.md
Propósito: Documentar las mejores prácticas para Markdown
Autor: Tu Nombre
Última actualización: 19 de junio de 2025
-->
```

### 10.2 Versionado
```markdown
# ✅ Control de versiones
## Historial de Cambios

### v1.2.0 (2025-06-19)
- Añadida sección de tablas complejas
- Mejorados ejemplos de código
- Corregidos enlaces rotos

### v1.1.0 (2025-06-15)
- Nueva sección de multimedia
- Ejemplos de elementos expandibles

### v1.0.0 (2025-06-01)
- Versión inicial del documento
```

## 11. **Herramientas y Validación**

### 11.1 Linters y Validadores
```markdown
# ✅ Herramientas recomendadas
- markdownlint: Validador de sintaxis
- Prettier: Formateador automático
- Vale: Verificador de estilo de escritura
- textlint: Linter de texto natural

# ✅ Configuración de markdownlint
{
  "MD013": false,
  "MD033": false,
  "MD041": false
}
```

### 11.2 Editores Recomendados
```markdown
# ✅ Editores con buen soporte para Markdown
- VS Code con extensiones Markdown
- Typora (WYSIWYG)
- Mark Text
- Zettlr
- Obsidian

# ✅ Extensiones útiles para VS Code
- Markdown All in One
- Markdown Preview Enhanced
- markdownlint
- Markdown Table Formatter
```

## 12. **Casos de Uso Específicos**

### 12.1 README.md
```markdown
# ✅ Estructura típica de README
# Nombre del Proyecto

Descripción breve del proyecto.

## Características

- Característica 1
- Característica 2
- Característica 3

## Instalación

```bash
npm install proyecto
```

## Uso

```javascript
const proyecto = require('proyecto');
proyecto.ejecutar();
```

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles.
```

### 12.2 Documentación Técnica
```markdown
# ✅ API Documentation
## Clase Usuario

### Constructor
```javascript
new Usuario(nombre, email, opciones)
```

**Parámetros:**
- `nombre` (string): Nombre completo del usuario
- `email` (string): Dirección de email válida
- `opciones` (object, opcional): Configuración adicional

**Retorna:** Instancia de Usuario

**Ejemplo:**
```javascript
const usuario = new Usuario('Juan Pérez', 'juan@email.com', {
  activo: true,
  rol: 'admin'
});
```

### Métodos

#### `obtenerPerfil()`
Obtiene el perfil completo del usuario.

**Retorna:** `Promise<Object>` - Datos del perfil

**Ejemplo:**
```javascript
const perfil = await usuario.obtenerPerfil();
console.log(perfil.nombre); // "Juan Pérez"
```
```

### 12.3 Guías y Tutoriales
```markdown
# ✅ Tutorial paso a paso
## Configurando tu Primer Proyecto

### Paso 1: Instalación
Primero, instala las dependencias necesarias:

```bash
npm init -y
npm install express
```

### Paso 2: Configuración
Crea el archivo `app.js`:

```javascript
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('¡Hola Mundo!');
});

app.listen(3000, () => {
  console.log('Servidor corriendo en puerto 3000');
});
```

### Paso 3: Ejecución
Ejecuta tu aplicación:

```bash
node app.js
```

### Verificación
Abre tu navegador y ve a `http://localhost:3000`. Deberías ver "¡Hola Mundo!".

### Próximos Pasos
- [Añadir rutas adicionales](tutorial-rutas.md)
- [Configurar middleware](tutorial-middleware.md)
- [Integrar base de datos](tutorial-database.md)
```

## Checklist de Buenas Prácticas

### ✅ Estructura
- [ ] Un solo H1 por documento
- [ ] Jerarquía de títulos secuencial
- [ ] Líneas en blanco apropiadas
- [ ] Longitud de línea razonable (70-80 caracteres)

### ✅ Contenido
- [ ] Texto alternativo descriptivo en imágenes
- [ ] Enlaces funcionales y descriptivos
- [ ] Código con sintaxis especificada
- [ ] Tablas bien formateadas

### ✅ Formato
- [ ] Énfasis usado apropiadamente
- [ ] Listas consistentes
- [ ] Citas correctamente formateadas
- [ ] Separadores utilizados apropiadamente

### ✅ Organización
- [ ] Índice de contenidos (si es necesario)
- [ ] Secciones lógicamente organizadas
- [ ] Metadatos incluidos
- [ ] Información de versionado

### ✅ Compatibilidad
- [ ] Características estándar utilizadas
- [ ] Compatibilidad verificada
- [ ] Fallbacks proporcionados
- [ ] Probado en múltiples renderizadores

### ✅ Mantenimiento
- [ ] Documentación actualizada
- [ ] Enlaces verificados
- [ ] Ortografía y gramática revisadas
- [ ] Validación con herramientas automáticas

## Recursos Adicionales

- [Markdown Guide](https://www.markdownguide.org/)
- [CommonMark Specification](https://commonmark.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)
- [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
- [markdownlint Rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [Markdown Style Guide](https://google.github.io/styleguide/docguide/style.html)

---

*Última actualización: Junio 2025*
