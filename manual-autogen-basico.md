# Manual Básico de AutoGen - Microsoft

## 📚 Tabla de Contenidos
1. [¿Qué es AutoGen?](#qué-es-autogen)
2. [Instalación](#instalación)
3. [Conceptos Básicos](#conceptos-básicos)
4. [Primer Ejemplo](#primer-ejemplo)
5. [Tipos de Agentes](#tipos-de-agentes)
6. [Conversaciones entre Agentes](#conversaciones-entre-agentes)
7. [Casos de Uso Comunes](#casos-de-uso-comunes)
8. [Mejores Prácticas](#mejores-prácticas)
9. [Recursos Adicionales](#recursos-adicionales)

## ¿Qué es AutoGen?

AutoGen es un framework de código abierto desarrollado por Microsoft que permite crear aplicaciones con múltiples agentes de IA que pueden conversar entre sí para resolver tareas complejas. Facilita el desarrollo de:

- 🤖 Sistemas multi-agente
- 💬 Conversaciones automatizadas
- 🔧 Flujos de trabajo con IA
- 🧩 Resolución colaborativa de problemas

## Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación Básica
```bash
# Instalación básica
pip install pyautogen

# Instalación con soporte para modelos locales
pip install "pyautogen[local]"

# Instalación completa con todas las características
pip install "pyautogen[all]"
```

## Conceptos Básicos

### 1. **Agentes**
Los agentes son las unidades fundamentales en AutoGen. Cada agente puede:
- Enviar y recibir mensajes
- Ejecutar código
- Interactuar con APIs
- Tomar decisiones

### 2. **Conversaciones**
Las conversaciones son intercambios de mensajes entre agentes para completar tareas.

### 3. **Roles**
Cada agente puede tener un rol específico:
- Assistant (Asistente)
- User Proxy (Proxy de Usuario)
- Group Chat Manager (Gestor de Chat Grupal)

## Primer Ejemplo

### Ejemplo 1: Conversación Simple
```python
import autogen

# Configuración
config_list = [{
    "model": "gpt-4",
    "api_key": "tu-api-key-aqui"
}]

# Crear un agente asistente
assistant = autogen.AssistantAgent(
    name="asistente",
    llm_config={
        "config_list": config_list,
        "temperature": 0.7,
    }
)

# Crear un agente proxy de usuario
user_proxy = autogen.UserProxyAgent(
    name="usuario",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding"}
)

# Iniciar conversación
user_proxy.initiate_chat(
    assistant,
    message="Escribe un programa en Python que calcule el factorial de un número"
)
```

## Tipos de Agentes

### 1. **AssistantAgent**
Agente basado en LLM que puede generar respuestas y código.

```python
assistant = autogen.AssistantAgent(
    name="asistente_python",
    system_message="Eres un experto programador de Python",
    llm_config={"config_list": config_list}
)
```

### 2. **UserProxyAgent**
Representa al usuario y puede ejecutar código.

```python
user_proxy = autogen.UserProxyAgent(
    name="usuario",
    human_input_mode="TERMINATE",  # NEVER, ALWAYS, TERMINATE
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": False
    }
)
```

### 3. **GroupChatManager**
Gestiona conversaciones entre múltiples agentes.

```python
groupchat = autogen.GroupChat(
    agents=[user_proxy, coder, reviewer],
    messages=[],
    max_round=12
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)
```

## Conversaciones entre Agentes

### Ejemplo: Sistema de Desarrollo de Software
```python
# Agente Programador
coder = autogen.AssistantAgent(
    name="programador",
    system_message="""Eres un programador senior. 
    Escribes código Python limpio y eficiente.""",
    llm_config=llm_config
)

# Agente Revisor
reviewer = autogen.AssistantAgent(
    name="revisor",
    system_message="""Eres un revisor de código experto. 
    Analizas el código en busca de errores y sugieres mejoras.""",
    llm_config=llm_config
)

# Agente Tester
tester = autogen.AssistantAgent(
    name="tester",
    system_message="""Eres un QA engineer. 
    Escribes y ejecutas pruebas para el código.""",
    llm_config=llm_config
)

# Chat grupal
groupchat = autogen.GroupChat(
    agents=[user_proxy, coder, reviewer, tester],
    messages=[],
    max_round=20
)

manager = autogen.GroupChatManager(
    groupchat=groupchat, 
    llm_config=llm_config
)

# Iniciar proyecto
user_proxy.initiate_chat(
    manager,
    message="Necesito una aplicación que gestione una lista de tareas"
)
```

## Casos de Uso Comunes

### 1. **Análisis de Datos Automatizado**
```python
data_analyst = autogen.AssistantAgent(
    name="analista_datos",
    system_message="Eres un experto en análisis de datos con pandas y matplotlib",
    llm_config=llm_config
)

user_proxy.initiate_chat(
    data_analyst,
    message="Analiza el archivo sales.csv y crea visualizaciones de las tendencias"
)
```

### 2. **Generación de Documentación**
```python
doc_writer = autogen.AssistantAgent(
    name="escritor_docs",
    system_message="Eres un experto en escribir documentación técnica clara",
    llm_config=llm_config
)
```

### 3. **Depuración de Código**
```python
debugger = autogen.AssistantAgent(
    name="depurador",
    system_message="Eres un experto en encontrar y corregir bugs en código",
    llm_config=llm_config
)
```

## Mejores Prácticas

### 1. **Configuración de LLM**
```python
# Configuración robusta con múltiples modelos
config_list = [
    {
        "model": "gpt-4",
        "api_key": os.environ.get("OPENAI_API_KEY"),
    },
    {
        "model": "gpt-3.5-turbo",
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
]

# Configuración con límites
llm_config = {
    "config_list": config_list,
    "temperature": 0.7,
    "max_tokens": 1000,
    "timeout": 120,
}
```

### 2. **Manejo de Errores**
```python
try:
    user_proxy.initiate_chat(
        assistant,
        message="Tu mensaje aquí"
    )
except Exception as e:
    print(f"Error en la conversación: {e}")
```

### 3. **Guardar Conversaciones**
```python
# Guardar historial
import json

conversation_history = groupchat.messages
with open("conversacion.json", "w") as f:
    json.dump(conversation_history, f, indent=2)
```

### 4. **Límites de Conversación**
```python
user_proxy = autogen.UserProxyAgent(
    name="usuario",
    max_consecutive_auto_reply=5,  # Limitar respuestas automáticas
    human_input_mode="TERMINATE",   # Permitir intervención humana
    is_termination_msg=lambda x: "TERMINADO" in x.get("content", "")
)
```

## Ejemplo Completo: Asistente de Investigación

```python
import autogen
import os

# Configuración
config_list = [{
    "model": "gpt-4",
    "api_key": os.environ.get("OPENAI_API_KEY")
}]

llm_config = {
    "config_list": config_list,
    "temperature": 0.5
}

# Agente Investigador
researcher = autogen.AssistantAgent(
    name="investigador",
    system_message="""Eres un investigador experto. 
    Tu trabajo es buscar información y proporcionar resúmenes detallados.""",
    llm_config=llm_config
)

# Agente Escritor
writer = autogen.AssistantAgent(
    name="escritor",
    system_message="""Eres un escritor técnico. 
    Tomas la investigación y creas documentos bien estructurados.""",
    llm_config=llm_config
)

# Agente Crítico
critic = autogen.AssistantAgent(
    name="critico",
    system_message="""Eres un revisor crítico. 
    Analizas el contenido en busca de precisión y calidad.""",
    llm_config=llm_config
)

# Usuario
user_proxy = autogen.UserProxyAgent(
    name="usuario",
    human_input_mode="TERMINATE",
    code_execution_config=False
)

# Chat grupal
groupchat = autogen.GroupChat(
    agents=[user_proxy, researcher, writer, critic],
    messages=[],
    max_round=15
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

# Iniciar investigación
user_proxy.initiate_chat(
    manager,
    message="Necesito un artículo sobre las tendencias en IA para 2024"
)
```

## Recursos Adicionales

### 📖 Documentación Oficial
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [GitHub Repository](https://github.com/microsoft/autogen)

### 🎓 Tutoriales
- [AutoGen Notebooks](https://github.com/microsoft/autogen/tree/main/notebook)
- [Ejemplos de Código](https://github.com/microsoft/autogen/tree/main/samples)

### 🛠️ Herramientas Útiles
- [AutoGen Studio](https://github.com/microsoft/autogen/tree/main/studio) - Interfaz visual para AutoGen
- [AutoGen Playground](https://microsoft.github.io/autogen/docs/Examples) - Ejemplos interactivos

### 💡 Tips Finales

1. **Comienza Simple**: Empieza con conversaciones de dos agentes antes de crear sistemas complejos.

2. **Experimenta con Prompts**: Los system_message son cruciales para el comportamiento de los agentes.

3. **Monitorea Costos**: Usa modelos más económicos durante el desarrollo.

4. **Versiona tu Código**: Guarda configuraciones exitosas para reutilizarlas.

5. **Únete a la Comunidad**: Participa en los foros y Discord de AutoGen para aprender de otros.

---

¡Felicitaciones! Ahora tienes los conocimientos básicos para empezar a crear aplicaciones con AutoGen. Recuerda que la práctica es clave para dominar el framework. 🚀