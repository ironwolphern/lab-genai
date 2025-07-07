# Manual de Uso del Framework CrewAI

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Conceptos Fundamentales](#conceptos-fundamentales)
4. [Configuración Inicial](#configuración-inicial)
5. [Creación de Agentes](#creación-de-agentes)
6. [Definición de Tareas](#definición-de-tareas)
7. [Configuración de Crews](#configuración-de-crews)
8. [Herramientas y Capacidades](#herramientas-y-capacidades)
9. [Ejemplos Prácticos](#ejemplos-prácticos)
10. [Mejores Prácticas](#mejores-prácticas)
11. [Solución de Problemas](#solución-de-problemas)

## 1. Introducción

CrewAI es un framework de Python diseñado para orquestar agentes de IA autónomos que trabajan colaborativamente en tareas complejas. Permite crear sistemas multi-agente donde cada agente tiene un rol específico, similar a un equipo de trabajo humano.

### Características Principales:
- **Colaboración Multi-Agente**: Los agentes trabajan juntos para completar tareas complejas
- **Roles Especializados**: Cada agente puede tener habilidades y responsabilidades específicas
- **Delegación Inteligente**: Los agentes pueden delegar tareas entre sí
- **Integración con LLMs**: Compatible con OpenAI, Anthropic, Ollama y otros proveedores
- **Herramientas Extensibles**: Soporte para herramientas personalizadas y predefinidas

## 2. Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- API key de OpenAI o configuración de Ollama (para modelos locales)

### Instalación Básica

```bash
# Instalación estándar
pip install crewai

# Instalación con herramientas adicionales
pip install 'crewai[tools]'

# Para usar con Ollama (modelos locales)
pip install crewai ollama
```

### Configuración de Variables de Entorno

```bash
# Para OpenAI
export OPENAI_API_KEY="tu-api-key-aqui"

# Para otros proveedores (opcional)
export ANTHROPIC_API_KEY="tu-api-key-anthropic"
```

## 3. Conceptos Fundamentales

### Agentes (Agents)
Los agentes son las entidades autónomas que ejecutan tareas. Cada agente tiene:
- **Role**: Define el papel del agente
- **Goal**: Objetivo principal del agente
- **Backstory**: Contexto que guía el comportamiento
- **Tools**: Herramientas disponibles para el agente
- **LLM**: Modelo de lenguaje a utilizar

### Tareas (Tasks)
Las tareas son unidades de trabajo específicas que deben completarse:
- **Description**: Qué debe hacerse
- **Agent**: Quién lo hará
- **Expected Output**: Resultado esperado
- **Tools**: Herramientas necesarias

### Crews
Un crew es un equipo de agentes que trabajan juntos:
- **Agents**: Lista de agentes en el equipo
- **Tasks**: Tareas a completar
- **Process**: Flujo de trabajo (secuencial o jerárquico)

## 4. Configuración Inicial

### Estructura de Proyecto Recomendada

```
mi_proyecto_crewai/
├── agents/
│   ├── __init__.py
│   └── my_agents.py
├── tasks/
│   ├── __init__.py
│   └── my_tasks.py
├── tools/
│   ├── __init__.py
│   └── custom_tools.py
├── config/
│   └── agents.yaml
├── main.py
└── requirements.txt
```

### Archivo de Configuración YAML (Opcional)

```yaml
# config/agents.yaml
researcher:
  role: "Senior Research Analyst"
  goal: "Uncover cutting-edge developments in {topic}"
  backstory: |
    You work at a leading tech think tank.
    Your expertise lies in identifying emerging trends.

writer:
  role: "Tech Content Strategist"
  goal: "Craft compelling content on {topic}"
  backstory: |
    You are a renowned Content Strategist.
```

## 5. Creación de Agentes

### Ejemplo Básico de Agente

```python
from crewai import Agent
from langchain.llms import OpenAI

# Crear un agente investigador
researcher = Agent(
    role='Senior Researcher',
    goal='Encontrar información precisa y actualizada sobre {topic}',
    backstory="""Eres un investigador experimentado con años de experiencia
    en análisis de datos y búsqueda de información relevante.""",
    verbose=True,
    allow_delegation=False,
    llm=OpenAI(temperature=0.7)
)

# Crear un agente escritor
writer = Agent(
    role='Content Writer',
    goal='Crear contenido claro y engaging basado en la investigación',
    backstory="""Eres un escritor profesional especializado en transformar
    información técnica en contenido accesible.""",
    verbose=True,
    allow_delegation=True,
    llm=OpenAI(temperature=0.7)
)
```

### Configuración Avanzada de Agentes

```python
from crewai import Agent
from crewai_tools import SerperDevTool, FileReadTool

# Agente con herramientas específicas
analyst = Agent(
    role='Data Analyst',
    goal='Analizar datos y generar insights significativos',
    backstory='Especialista en análisis de datos con experiencia en BI',
    tools=[
        SerperDevTool(),  # Para búsquedas en internet
        FileReadTool()     # Para leer archivos
    ],
    max_iter=3,  # Máximo de iteraciones
    max_execution_time=300,  # Tiempo máximo en segundos
    system_template="""Eres un analista experto. 
    Siempre verifica tus fuentes y proporciona datos precisos."""
)
```

## 6. Definición de Tareas

### Creación de Tareas Básicas

```python
from crewai import Task

# Tarea de investigación
research_task = Task(
    description="""Investiga las últimas tendencias en {topic}.
    Identifica los desarrollos clave, empresas líderes y casos de uso.
    Tu informe final debe incluir:
    - Resumen ejecutivo
    - Principales hallazgos
    - Fuentes consultadas""",
    agent=researcher,
    expected_output="Un informe detallado de investigación en formato markdown"
)

# Tarea de escritura
writing_task = Task(
    description="""Usando la investigación proporcionada, escribe un artículo
    de blog engaging sobre {topic}. El artículo debe ser:
    - Informativo pero accesible
    - Entre 500-800 palabras
    - Con una introducción atractiva y conclusión clara""",
    agent=writer,
    expected_output="Artículo de blog completo en formato markdown"
)
```

### Tareas con Dependencias

```python
# Tarea que depende de otra
analysis_task = Task(
    description="Analiza los datos recopilados y genera visualizaciones",
    agent=analyst,
    context=[research_task],  # Esta tarea usa el output de research_task
    expected_output="Informe con gráficos y análisis estadístico"
)
```

## 7. Configuración de Crews

### Crew Básico

```python
from crewai import Crew, Process

# Crear el crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,  # Las tareas se ejecutan en orden
    verbose=True
)

# Ejecutar el crew
result = crew.kickoff(inputs={'topic': 'Inteligencia Artificial en 2025'})
print(result)
```

### Crew con Proceso Jerárquico

```python
# Crew con manager
manager_crew = Crew(
    agents=[researcher, writer, analyst],
    tasks=[research_task, writing_task, analysis_task],
    process=Process.hierarchical,
    manager_llm=OpenAI(model="gpt-4"),  # El manager coordina
    verbose=True
)
```

### Crew con Configuración Avanzada

```python
from crewai import Crew
from crewai.project import CrewBase, agent, task, crew

@CrewBase
class MyResearchCrew:
    """Crew para investigación avanzada"""
    
    @agent
    def researcher(self) -> Agent:
        return Agent(
            role='Lead Researcher',
            goal='Conduct thorough research',
            backstory='Expert researcher with 10 years experience',
            tools=[SerperDevTool()]
        )
    
    @task
    def research_task(self) -> Task:
        return Task(
            description='Research {topic} comprehensively',
            agent=self.researcher(),
            expected_output='Detailed research report'
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.researcher()],
            tasks=[self.research_task()],
            process=Process.sequential
        )
```

## 8. Herramientas y Capacidades

### Herramientas Predefinidas

```python
from crewai_tools import (
    SerperDevTool,      # Búsqueda en internet
    WebsiteSearchTool,  # Búsqueda en sitios web
    FileReadTool,       # Lectura de archivos
    CSVSearchTool,      # Análisis de CSV
    MDXSearchTool,      # Búsqueda en MDX
    PDFSearchTool,      # Búsqueda en PDF
    DirectoryReadTool   # Lectura de directorios
)

# Configurar herramientas
search_tool = SerperDevTool()
web_tool = WebsiteSearchTool(website='https://example.com')
file_tool = FileReadTool(file_path='./data/')
```

### Creación de Herramientas Personalizadas

```python
from crewai_tools import BaseTool

class MyCustomTool(BaseTool):
    name: str = "Custom Calculator"
    description: str = "Performs custom calculations"
    
    def _run(self, operation: str) -> str:
        """Ejecuta la herramienta"""
        try:
            result = eval(operation)
            return f"El resultado es: {result}"
        except:
            return "Error en la operación"

# Usar la herramienta personalizada
calculator = MyCustomTool()
math_agent = Agent(
    role='Mathematician',
    goal='Solve mathematical problems',
    tools=[calculator]
)
```

## 9. Ejemplos Prácticos

### Ejemplo 1: Crew de Análisis de Noticias

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, WebsiteSearchTool

# Agentes
news_researcher = Agent(
    role='News Researcher',
    goal='Find latest news about {topic}',
    backstory='Expert in finding breaking news and trends',
    tools=[SerperDevTool()],
    verbose=True
)

news_analyst = Agent(
    role='News Analyst',
    goal='Analyze news for insights and patterns',
    backstory='Senior analyst with expertise in media analysis',
    verbose=True
)

news_writer = Agent(
    role='News Writer',
    goal='Write compelling news summaries',
    backstory='Journalist with 10 years of experience',
    verbose=True
)

# Tareas
research_news = Task(
    description="""Find the latest news about {topic}.
    Focus on:
    1. Breaking news from last 24 hours
    2. Major developments
    3. Expert opinions
    Include at least 5 sources.""",
    agent=news_researcher,
    expected_output="List of relevant news with summaries"
)

analyze_news = Task(
    description="""Analyze the news found and identify:
    1. Key trends
    2. Common themes
    3. Potential impacts
    4. Contrasting viewpoints""",
    agent=news_analyst,
    context=[research_news],
    expected_output="Analytical report with insights"
)

write_summary = Task(
    description="""Write a comprehensive news summary that:
    1. Highlights key findings
    2. Explains the significance
    3. Provides balanced perspective
    4. Is engaging and easy to read""",
    agent=news_writer,
    context=[research_news, analyze_news],
    expected_output="Professional news summary article"
)

# Crew
news_crew = Crew(
    agents=[news_researcher, news_analyst, news_writer],
    tasks=[research_news, analyze_news, write_summary],
    process=Process.sequential,
    verbose=True
)

# Ejecutar
result = news_crew.kickoff(inputs={'topic': 'AI developments in 2025'})
```

### Ejemplo 2: Crew de Desarrollo de Producto

```python
# Crew para desarrollo de producto
product_researcher = Agent(
    role='Product Researcher',
    goal='Research market needs and opportunities',
    backstory='Expert in market research and user needs analysis',
    tools=[SerperDevTool(), WebsiteSearchTool()]
)

product_designer = Agent(
    role='Product Designer',
    goal='Design innovative product solutions',
    backstory='Creative designer with UX/UI expertise'
)

product_strategist = Agent(
    role='Product Strategist',
    goal='Develop go-to-market strategy',
    backstory='Strategic thinker with business acumen'
)

# Tareas del producto
market_research = Task(
    description="""Research the market for {product_idea}:
    - Target audience
    - Competitor analysis
    - Market size and trends
    - User pain points""",
    agent=product_researcher
)

product_design = Task(
    description="""Design the product concept:
    - Key features
    - User experience flow
    - Unique value proposition
    - MVP definition""",
    agent=product_designer,
    context=[market_research]
)

strategy_development = Task(
    description="""Develop launch strategy:
    - Pricing strategy
    - Marketing channels
    - Launch timeline
    - Success metrics""",
    agent=product_strategist,
    context=[market_research, product_design]
)

product_crew = Crew(
    agents=[product_researcher, product_designer, product_strategist],
    tasks=[market_research, product_design, strategy_development],
    process=Process.sequential
)
```

## 10. Mejores Prácticas

### 1. Diseño de Agentes
- **Roles Claros**: Define roles específicos y no superpuestos
- **Goals Medibles**: Establece objetivos claros y alcanzables
- **Backstories Relevantes**: Proporciona contexto que guíe el comportamiento

### 2. Optimización de Rendimiento
```python
# Usar caché para respuestas
from crewai.cache import SimpleCache

crew = Crew(
    agents=[...],
    tasks=[...],
    cache=SimpleCache(),  # Cachea resultados
    max_rpm=10  # Límite de requests por minuto
)
```

### 3. Manejo de Errores
```python
try:
    result = crew.kickoff(inputs={'topic': 'AI'})
except Exception as e:
    print(f"Error en la ejecución: {e}")
    # Implementar lógica de recuperación
```

### 4. Logging y Monitoreo
```python
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('crewai')

# Los agentes con verbose=True mostrarán logs detallados
```

### 5. Testing
```python
# Test unitario de un agente
def test_researcher_agent():
    agent = Agent(
        role='Tester',
        goal='Test functionality',
        backstory='QA specialist'
    )
    
    task = Task(
        description='Simple test task',
        agent=agent,
        expected_output='Test result'
    )
    
    # Verificar configuración
    assert agent.role == 'Tester'
    assert task.agent == agent
```

## 11. Solución de Problemas

### Problemas Comunes y Soluciones

#### 1. Error de API Key
**Problema**: "OpenAI API key not found"
**Solución**:
```bash
export OPENAI_API_KEY="tu-api-key"
# O en el código:
import os
os.environ["OPENAI_API_KEY"] = "tu-api-key"
```

#### 2. Timeout en Tareas
**Problema**: Las tareas tardan demasiado
**Solución**:
```python
agent = Agent(
    # ...
    max_execution_time=600,  # 10 minutos
    max_iter=5  # Máximo 5 intentos
)
```

#### 3. Memoria Insuficiente
**Problema**: Out of memory con crews grandes
**Solución**:
```python
# Procesar en lotes
crew = Crew(
    agents=[...],
    tasks=[...],
    memory=False  # Desactivar memoria si no es necesaria
)
```

#### 4. Agentes No Colaboran
**Problema**: Los agentes no comparten información
**Solución**:
```python
# Asegurar que allow_delegation=True
agent = Agent(
    role='Collaborative Agent',
    allow_delegation=True,  # Permite delegar
    # ...
)

# Usar context en las tareas
task = Task(
    description='...',
    context=[previous_task],  # Acceso a tareas anteriores
    # ...
)
```

### Comandos de Depuración

```python
# Activar modo debug
crew = Crew(
    agents=[...],
    tasks=[...],
    verbose=2,  # Máximo nivel de verbosidad
    debug=True  # Modo debug
)

# Ver el estado del crew
print(crew.agents)
print(crew.tasks)
print(crew.process)
```

## Recursos Adicionales

### Enlaces Útiles
- [Documentación Oficial](https://docs.crewai.com)
- [GitHub Repository](https://github.com/joaomdmoura/crewai)
- [Ejemplos de la Comunidad](https://github.com/joaomdmoura/crewai-examples)
- [Discord de CrewAI](https://discord.com/invite/X4JWnZnxPb)

### Próximos Pasos
1. Experimenta con los ejemplos básicos
2. Crea tu propio crew personalizado
3. Integra herramientas específicas para tu caso de uso
4. Únete a la comunidad para compartir experiencias

---

**Nota**: Este manual está actualizado a julio de 2025. CrewAI está en desarrollo activo, por lo que algunas características pueden cambiar. Consulta la documentación oficial para las últimas actualizaciones.