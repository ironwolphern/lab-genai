# Manual Completo de AutoGen con autogen-core y autogen-agentchat
## Versión más reciente - Julio 2025

## Introducción a la Nueva Arquitectura

Microsoft AutoGen ha evolucionado hacia una arquitectura modular más flexible y escalable. La versión actual (0.4+) se divide en varios paquetes especializados:

- **autogen-core**: Framework base para sistemas multi-agente asíncronos
- **autogen-agentchat**: Agentes de alto nivel para aplicaciones de chat
- **autogen-ext**: Extensiones y integraciones con servicios externos
- **autogen-studio**: Interfaz visual para diseñar flujos de agentes

Esta nueva arquitectura permite mayor flexibilidad, mejor rendimiento y desarrollo más modular.

## Instalación de la Nueva Arquitectura

```bash
# Instalación del core (requerido)
pip install autogen-core

# Instalación de agentchat (para agentes conversacionales)
pip install autogen-agentchat

# Instalación de extensiones
pip install autogen-ext

# Instalación completa con todas las características
pip install "autogen-agentchat[all]"

# Para desarrollo
pip install "autogen-core[dev]" "autogen-agentchat[dev]"

# Verificar versiones instaladas
python -c "import autogen_core; print(f'Core: {autogen_core.__version__}')"
python -c "import autogen_agentchat; print(f'AgentChat: {autogen_agentchat.__version__}')"
```

## Conceptos Fundamentales de autogen-core

### 1. Runtime Asíncrono

El nuevo autogen-core está construido sobre un runtime completamente asíncrono:

```python
import asyncio
from autogen_core import (
    SingleThreadedAgentRuntime,
    DefaultTopicId,
    MessageContext,
    AgentId,
    AgentType
)
from autogen_core.components import DefaultSubscription
from dataclasses import dataclass

# Definir tipos de mensajes
@dataclass
class TextMessage:
    content: str
    sender: str

@dataclass
class CodeMessage:
    code: str
    language: str

# Runtime principal
async def setup_runtime():
    runtime = SingleThreadedAgentRuntime()
    
    # Registrar agentes
    await runtime.register(
        "assistant",
        lambda: AssistantAgent(),
        subscriptions=lambda: [
            DefaultSubscription(topic_type="conversation", agent_type="assistant")
        ]
    )
    
    await runtime.register(
        "coder",
        lambda: CoderAgent(),
        subscriptions=lambda: [
            DefaultSubscription(topic_type="coding", agent_type="coder")
        ]
    )
    
    # Iniciar runtime
    runtime.start()
    return runtime
```

### 2. Agentes Base con autogen-core

```python
from autogen_core import Agent, MessageContext
from typing import Any

class BaseAgent(Agent):
    """Agente base usando autogen-core"""
    
    def __init__(self, name: str):
        self.name = name
        self._message_queue = []
    
    async def on_message(self, message: Any, ctx: MessageContext) -> Any:
        """Maneja mensajes entrantes"""
        print(f"{self.name} recibió: {message}")
        
        if isinstance(message, TextMessage):
            return await self.handle_text_message(message, ctx)
        elif isinstance(message, CodeMessage):
            return await self.handle_code_message(message, ctx)
    
    async def handle_text_message(self, message: TextMessage, ctx: MessageContext) -> Any:
        """Maneja mensajes de texto"""
        # Implementar lógica específica
        pass
    
    async def handle_code_message(self, message: CodeMessage, ctx: MessageContext) -> Any:
        """Maneja mensajes de código"""
        # Implementar lógica específica
        pass
```

### 3. Sistema de Publicación/Suscripción

```python
from autogen_core import TopicId, AgentId
from autogen_core.components import TypeSubscription

class EventDrivenSystem:
    """Sistema basado en eventos con pub/sub"""
    
    def __init__(self):
        self.runtime = SingleThreadedAgentRuntime()
    
    async def setup_subscriptions(self):
        # Agente que se suscribe a múltiples topics
        await self.runtime.register(
            "analyzer",
            lambda: DataAnalyzer(),
            subscriptions=lambda: [
                TypeSubscription(topic_type="data_received", agent_type="analyzer"),
                TypeSubscription(topic_type="analysis_requested", agent_type="analyzer"),
            ]
        )
        
        # Agente que publica eventos
        await self.runtime.register(
            "collector",
            lambda: DataCollector(),
            subscriptions=lambda: [
                TypeSubscription(topic_type="collection_trigger", agent_type="collector")
            ]
        )
    
    async def publish_event(self, topic: str, message: Any):
        """Publica un evento a todos los suscriptores"""
        topic_id = TopicId(type=topic, source="system")
        await self.runtime.publish_message(message, topic_id)
```

## autogen-agentchat: Agentes Conversacionales de Alto Nivel

### 1. Configuración Básica con autogen-agentchat

```python
from autogen_agentchat import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models import OpenAIChatCompletionClient

# Configurar cliente LLM
model_client = OpenAIChatCompletionClient(
    model="gpt-4-turbo-preview",
    api_key="tu-api-key",
    # Nuevas opciones de configuración
    base_url="https://api.openai.com/v1",
    temperature=0.7,
    max_tokens=2000,
    top_p=0.95,
    presence_penalty=0.0,
    frequency_penalty=0.0,
    seed=42  # Para reproducibilidad
)

# Crear agente asistente con la nueva API
assistant = AssistantAgent(
    name="primary_assistant",
    model_client=model_client,
    system_message="""Eres un asistente útil y experto en programación.
    Proporciona código limpio, bien documentado y siguiendo mejores prácticas.""",
    description="Asistente principal para tareas de programación",
    handoffs=["specialist_agent", "reviewer_agent"]  # Nueva característica
)

# Agente usuario con capacidades mejoradas
user_proxy = UserProxyAgent(
    name="user_proxy",
    description="Representa al usuario y ejecuta código",
    code_execution_config={
        "work_dir": "./coding",
        "use_docker": True,
        "timeout": 120,
        "last_n_messages": "all",  # Nueva opción
        "stop_on_error": False,    # Nueva opción
    }
)
```

### 2. Teams y Colaboración Mejorada

```python
from autogen_agentchat.teams import (
    RoundRobinGroupChat,
    SelectorGroupChat,
    Swarm,
    MagenticOneGroupChat
)
from autogen_agentchat.base import TaskResult
import asyncio

async def create_development_team():
    """Crea un equipo de desarrollo con la nueva arquitectura"""
    
    # Configurar modelo
    model_client = OpenAIChatCompletionClient(
        model="gpt-4-turbo-preview",
        api_key="tu-api-key"
    )
    
    # Arquitecto de Software
    architect = AssistantAgent(
        name="software_architect",
        model_client=model_client,
        system_message="""Eres un arquitecto de software senior.
        Diseña sistemas escalables, define patrones y mejores prácticas.""",
        description="Diseña la arquitectura del sistema"
    )
    
    # Desarrollador Backend
    backend_dev = AssistantAgent(
        name="backend_developer",
        model_client=model_client,
        system_message="""Eres un desarrollador backend experto en Python y FastAPI.
        Implementa APIs RESTful, maneja bases de datos y asegura rendimiento.""",
        description="Implementa la lógica del servidor y APIs"
    )
    
    # Desarrollador Frontend
    frontend_dev = AssistantAgent(
        name="frontend_developer",
        model_client=model_client,
        system_message="""Eres un desarrollador frontend experto en React y TypeScript.
        Crea interfaces intuitivas, responsivas y accesibles.""",
        description="Desarrolla la interfaz de usuario"
    )
    
    # Ingeniero de Calidad
    qa_engineer = AssistantAgent(
        name="qa_engineer",
        model_client=model_client,
        system_message="""Eres un QA engineer experto en testing automatizado.
        Escribes tests unitarios, de integración y E2E. Aseguras calidad.""",
        description="Diseña y ejecuta estrategias de testing"
    )
    
    # Ejecutor de código
    code_executor = UserProxyAgent(
        name="code_executor",
        description="Ejecuta y valida código",
        code_execution_config={
            "work_dir": "./project",
            "use_docker": True,
        }
    )
    
    # Crear equipo con selector inteligente
    team = SelectorGroupChat(
        participants=[architect, backend_dev, frontend_dev, qa_engineer, code_executor],
        model_client=model_client,
        selector_prompt="""Selecciona el siguiente agente basándote en:
        1. La tarea actual que necesita ser completada
        2. Las habilidades específicas requeridas
        3. El estado actual del proyecto
        
        Arquitecto: Para decisiones de diseño y arquitectura
        Backend Dev: Para implementar APIs y lógica del servidor
        Frontend Dev: Para interfaces de usuario
        QA Engineer: Para testing y calidad
        Code Executor: Para ejecutar y validar código""",
        allow_repeated_speaker=False,
        termination_condition=MaxMessageTermination(max_messages=50)
    )
    
    return team

# Usar el equipo
async def develop_project(project_description: str):
    team = await create_development_team()
    
    # Ejecutar tarea
    result = await team.run(
        task=f"""Desarrolla una aplicación completa: {project_description}
        
        Requisitos:
        1. Arquitectura bien definida
        2. Backend con API RESTful
        3. Frontend moderno y responsivo
        4. Suite completa de tests
        5. Documentación clara
        
        Genera todo el código necesario y asegúrate de que funcione correctamente."""
    )
    
    return result
```

### 3. Nuevo Sistema Swarm

```python
from autogen_agentchat.teams import Swarm
from autogen_agentchat.base import HandoffMessage

class SwarmSystem:
    """Sistema Swarm para manejo dinámico de tareas"""
    
    def __init__(self, model_client):
        self.model_client = model_client
        self.agents = self._create_agents()
    
    def _create_agents(self):
        # Agente de triaje
        triage_agent = AssistantAgent(
            name="triage_agent",
            model_client=self.model_client,
            system_message="""Analiza las solicitudes y determina qué especialista
            debe manejar cada tarea. Eres eficiente en la delegación.""",
            handoffs=["data_analyst", "ml_engineer", "report_writer"]
        )
        
        # Analista de datos
        data_analyst = AssistantAgent(
            name="data_analyst",
            model_client=self.model_client,
            system_message="""Experto en análisis de datos con pandas, numpy.
            Realizas EDA, estadísticas y preparación de datos.""",
            handoffs=["ml_engineer", "report_writer"]
        )
        
        # Ingeniero ML
        ml_engineer = AssistantAgent(
            name="ml_engineer",
            model_client=self.model_client,
            system_message="""Experto en machine learning con scikit-learn, tensorflow.
            Construyes y optimizas modelos predictivos.""",
            handoffs=["report_writer"]
        )
        
        # Escritor de reportes
        report_writer = AssistantAgent(
            name="report_writer",
            model_client=self.model_client,
            system_message="""Experto en comunicación técnica. Creas reportes
            claros con visualizaciones y recomendaciones accionables.""",
            handoffs=[]  # Agente final
        )
        
        return {
            "triage": triage_agent,
            "data_analyst": data_analyst,
            "ml_engineer": ml_engineer,
            "report_writer": report_writer
        }
    
    async def process_task(self, task: str):
        """Procesa una tarea usando el sistema swarm"""
        
        # Crear swarm con handoffs dinámicos
        swarm = Swarm(
            participants=list(self.agents.values()),
            termination_condition=TextMentionTermination("TASK_COMPLETE")
        )
        
        # Ejecutar tarea empezando por triaje
        result = await swarm.run(
            task=task,
            initial_agent="triage_agent"
        )
        
        return result
```

### 4. MagenticOne: Sistema de Agentes Orquestado

```python
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.agents import (
    MultimodalWebSurfer,
    FileSurfer,
    Coder,
    ComputerTerminal,
    Orchestrator
)

async def create_magentic_one_system():
    """Crea un sistema MagenticOne completo"""
    
    model_client = OpenAIChatCompletionClient(
        model="gpt-4-turbo-preview",
        api_key="tu-api-key"
    )
    
    # Orquestador principal
    orchestrator = Orchestrator(
        name="orchestrator",
        model_client=model_client,
        max_rounds=30,
        max_time=1800  # 30 minutos
    )
    
    # Navegador web multimodal
    web_surfer = MultimodalWebSurfer(
        name="web_surfer",
        model_client=model_client,
        headless=False,
        viewport_size=(1920, 1080),
        downloads_folder="./downloads"
    )
    
    # Explorador de archivos
    file_surfer = FileSurfer(
        name="file_surfer",
        model_client=model_client,
        root_path="./workspace"
    )
    
    # Programador
    coder = Coder(
        name="coder",
        model_client=model_client,
        execute_code=True,
        language_preferences=["python", "javascript", "typescript"]
    )
    
    # Terminal de computadora
    terminal = ComputerTerminal(
        name="terminal",
        model_client=model_client,
        allowed_commands=["python", "pip", "npm", "git", "docker"]
    )
    
    # Crear equipo MagenticOne
    team = MagenticOneGroupChat(
        orchestrator=orchestrator,
        agents=[web_surfer, file_surfer, coder, terminal],
        max_rounds=50,
        log_level="INFO"
    )
    
    return team

# Usar MagenticOne para tareas complejas
async def execute_complex_task(task_description: str):
    team = await create_magentic_one_system()
    
    result = await team.run(
        task=task_description,
        context={
            "working_directory": "./magentic_workspace",
            "available_tools": ["web_browser", "file_system", "code_execution", "terminal"],
            "constraints": ["No acceder a sitios peligrosos", "No ejecutar comandos destructivos"]
        }
    )
    
    return result
```

## Extensiones con autogen-ext

### 1. Integración con Modelos de Diferentes Proveedores

```python
from autogen_ext.models import (
    OpenAIChatCompletionClient,
    AnthropicChatCompletionClient,
    AzureOpenAIChatCompletionClient,
    GeminiChatCompletionClient,
    MistralAIChatCompletionClient,
    CohereAIChatCompletionClient,
    OllamaChatCompletionClient
)

# Configurar múltiples modelos
models = {
    "openai": OpenAIChatCompletionClient(
        model="gpt-4-turbo-preview",
        api_key="openai-key"
    ),
    "anthropic": AnthropicChatCompletionClient(
        model="claude-3-opus-20240229",
        api_key="anthropic-key"
    ),
    "azure": AzureOpenAIChatCompletionClient(
        azure_endpoint="https://tu-recurso.openai.azure.com",
        api_key="azure-key",
        api_version="2024-02-01",
        azure_deployment="gpt-4-deployment"
    ),
    "gemini": GeminiChatCompletionClient(
        model="gemini-1.5-pro",
        api_key="google-key"
    ),
    "local": OllamaChatCompletionClient(
        model="llama3:70b",
        base_url="http://localhost:11434"
    )
}

# Crear agentes con diferentes modelos
async def create_multi_model_agents():
    agents = {}
    
    for name, model_client in models.items():
        agent = AssistantAgent(
            name=f"{name}_assistant",
            model_client=model_client,
            system_message=f"Eres un asistente potenciado por {name}."
        )
        agents[name] = agent
    
    return agents
```

### 2. Herramientas y Capacidades Extendidas

```python
from autogen_ext.tools import (
    PythonCodeExecutor,
    DockerCommandLineCodeExecutor,
    LocalCommandLineCodeExecutor
)
from autogen_ext.tools.web_surfer import WebSurferTool
from autogen_ext.tools.file_surfer import FileSurferTool
from autogen_agentchat.agents import AssistantAgent

# Configurar herramientas de ejecución de código
code_executors = {
    "python": PythonCodeExecutor(
        work_dir="./python_workspace",
        virtual_env=True,
        install_packages=True
    ),
    "docker": DockerCommandLineCodeExecutor(
        image="python:3.11",
        volumes={"/workspace": "./docker_workspace"},
        timeout=300
    ),
    "local": LocalCommandLineCodeExecutor(
        work_dir="./local_workspace",
        allowed_commands=["python", "pip", "git"]
    )
}

# Crear agente con herramientas
async def create_tool_agent():
    model_client = OpenAIChatCompletionClient(
        model="gpt-4-turbo-preview",
        api_key="tu-key"
    )
    
    # Herramientas web y archivos
    web_tool = WebSurferTool(
        headless=True,
        viewport_size=(1920, 1080)
    )
    
    file_tool = FileSurferTool(
        root_path="./workspace"
    )
    
    # Agente con múltiples herramientas
    agent = AssistantAgent(
        name="tool_master",
        model_client=model_client,
        tools=[web_tool, file_tool, code_executors["python"]],
        system_message="""Eres un agente con acceso a navegador web,
        sistema de archivos y ejecución de código Python.
        Usa estas herramientas sabiamente para completar tareas."""
    )
    
    return agent
```

### 3. RAG (Retrieval Augmented Generation) Mejorado

```python
from autogen_ext.storage import ChromaVectorDB, QdrantVectorDB
from autogen_ext.models.embeddings import OpenAIEmbeddingFunction
from autogen_agentchat.contrib.retriever import RetrieverAgent
import asyncio

class AdvancedRAGSystem:
    """Sistema RAG avanzado con múltiples fuentes"""
    
    def __init__(self):
        # Configurar embeddings
        self.embedding_function = OpenAIEmbeddingFunction(
            model="text-embedding-3-large",
            api_key="tu-key"
        )
        
        # Configurar vector stores
        self.vector_stores = {
            "technical_docs": ChromaVectorDB(
                collection_name="technical_documentation",
                embedding_function=self.embedding_function,
                persist_directory="./chroma_db"
            ),
            "code_snippets": QdrantVectorDB(
                collection_name="code_examples",
                embedding_function=self.embedding_function,
                url="http://localhost:6333"
            )
        }
        
        # Configurar modelo
        self.model_client = OpenAIChatCompletionClient(
            model="gpt-4-turbo-preview",
            api_key="tu-key"
        )
    
    async def create_rag_agent(self, knowledge_base: str):
        """Crea un agente RAG para una base de conocimiento específica"""
        
        retriever = RetrieverAgent(
            name=f"{knowledge_base}_retriever",
            vector_db=self.vector_stores[knowledge_base],
            model_client=self.model_client,
            retrieve_config={
                "top_k": 5,
                "score_threshold": 0.7,
                "max_tokens": 2000
            },
            system_message=f"""Eres un asistente experto que responde basándose
            en la documentación de {knowledge_base}. Siempre cita tus fuentes."""
        )
        
        return retriever
    
    async def add_documents(self, knowledge_base: str, documents: list):
        """Agrega documentos a una base de conocimiento"""
        
        vector_store = self.vector_stores[knowledge_base]
        
        # Procesar documentos en lotes
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            await vector_store.add_documents(batch)
        
        print(f"Agregados {len(documents)} documentos a {knowledge_base}")
    
    async def query(self, knowledge_base: str, question: str):
        """Consulta una base de conocimiento específica"""
        
        agent = await self.create_rag_agent(knowledge_base)
        
        result = await agent.run(
            task=question,
            context={
                "include_sources": True,
                "max_sources": 3
            }
        )
        
        return result
```

## Patrones Avanzados y Mejores Prácticas

### 1. Sistema de Monitoreo y Observabilidad

```python
from autogen_core.components import (
    ClosureAgent,
    DefaultTopicId,
    MessageContext,
    default_subscription
)
from autogen_ext.telemetry import (
    AzureMonitorTracer,
    PrometheusMetrics,
    OpenTelemetryTracer
)
import logging
from datetime import datetime

class MonitoredAgentSystem:
    """Sistema de agentes con monitoreo completo"""
    
    def __init__(self):
        # Configurar telemetría
        self.tracer = OpenTelemetryTracer(
            service_name="autogen_system",
            endpoint="http://localhost:4317"
        )
        
        self.metrics = PrometheusMetrics(
            port=8000,
            namespace="autogen"
        )
        
        # Logger estructurado
        self.logger = self._setup_logger()
        
        # Runtime con telemetría
        self.runtime = SingleThreadedAgentRuntime(
            tracer=self.tracer,
            metrics_collector=self.metrics
        )
    
    def _setup_logger(self):
        """Configura logging estructurado"""
        logger = logging.getLogger("autogen_system")
        logger.setLevel(logging.INFO)
        
        # Handler con formato JSON
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
                '"agent": "%(name)s", "message": "%(message)s"}'
            )
        )
        logger.addHandler(handler)
        
        return logger
    
    async def create_monitored_agent(self, name: str, role: str):
        """Crea un agente con capacidades de monitoreo"""
        
        @default_subscription
        class MonitoredAgent(ClosureAgent):
            def __init__(self):
                super().__init__(
                    description=f"Monitored agent: {name}",
                    closure=self._monitored_closure
                )
                self.name = name
                self.role = role
                self.message_count = 0
                self.error_count = 0
            
            async def _monitored_closure(self, message: Any, ctx: MessageContext) -> Any:
                """Procesa mensajes con monitoreo"""
                start_time = datetime.now()
                
                try:
                    # Log entrada
                    self.logger.info(f"Processing message", extra={
                        "agent": self.name,
                        "message_type": type(message).__name__,
                        "message_id": ctx.message_id
                    })
                    
                    # Incrementar contador
                    self.message_count += 1
                    self.metrics.increment("messages_processed", labels={
                        "agent": self.name,
                        "role": self.role
                    })
                    
                    # Procesar mensaje (lógica específica del agente)
                    result = await self._process_message(message, ctx)
                    
                    # Medir latencia
                    latency = (datetime.now() - start_time).total_seconds()
                    self.metrics.histogram("message_latency", latency, labels={
                        "agent": self.name
                    })
                    
                    return result
                    
                except Exception as e:
                    # Log error
                    self.error_count += 1
                    self.logger.error(f"Error processing message", extra={
                        "agent": self.name,
                        "error": str(e),
                        "message_id": ctx.message_id
                    })
                    
                    self.metrics.increment("errors", labels={
                        "agent": self.name,
                        "error_type": type(e).__name__
                    })
                    
                    raise
            
            async def _process_message(self, message: Any, ctx: MessageContext) -> Any:
                """Implementación específica del agente"""
                # Lógica del agente aquí
                pass
        
        return MonitoredAgent()
```

### 2. Sistema de Caché Distribuido

```python
from autogen_ext.cache import RedisCache, MemoryCache
from autogen_agentchat import AssistantAgent
import hashlib
import json

class CachedAgentSystem:
    """Sistema con caché distribuido para optimización"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        # Caché distribuido
        self.redis_cache = RedisCache(
            url=redis_url,
            ttl=3600,  # 1 hora
            namespace="autogen"
        )
        
        # Caché en memoria para acceso rápido
        self.memory_cache = MemoryCache(
            max_size=1000,
            ttl=300  # 5 minutos
        )
    
    def _generate_cache_key(self, agent_name: str, message: str, context: dict) -> str:
        """Genera clave única para caché"""
        cache_data = {
            "agent": agent_name,
            "message": message,
            "context": context
        }
        
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.sha256(cache_string.encode()).hexdigest()
    
    async def get_cached_response(self, agent_name: str, message: str, context: dict):
        """Intenta obtener respuesta del caché"""
        cache_key = self._generate_cache_key(agent_name, message, context)
        
        # Intentar memoria primero
        response = await self.memory_cache.get(cache_key)
        if response:
            return response, "memory"
        
        # Intentar Redis
        response = await self.redis_cache.get(cache_key)
        if response:
            # Guardar en memoria para acceso rápido
            await self.memory_cache.set(cache_key, response)
            return response, "redis"
        
        return None, None
    
    async def cache_response(self, agent_name: str, message: str, 
                           context: dict, response: str):
        """Guarda respuesta en caché"""
        cache_key = self._generate_cache_key(agent_name, message, context)
        
        # Guardar en ambos cachés
        await self.memory_cache.set(cache_key, response)
        await self.redis_cache.set(cache_key, response)
    
    def create_cached_agent(self, name: str, model_client, system_message: str):
        """Crea un agente con capacidades de caché"""
        
        class CachedAssistant(AssistantAgent):
            def __init__(self, cache_system):
                super().__init__(
                    name=name,
                    model_client=model_client,
                    system_message=system_message
                )
                self.cache_system = cache_system
                self.cache_hits = 0
                self.cache_misses = 0
            
            async def generate_response(self, messages, sender, **kwargs):
                """Genera respuesta con caché"""
                # Intentar obtener del caché
                last_message = messages[-1]["content"] if messages else ""
                context = {"sender": sender.name, "system": self.system_message[:100]}
                
                cached_response, cache_type = await self.cache_system.get_cached_response(
                    self.name, last_message, context
                )
                
                if cached_response:
                    self.cache_hits += 1
                    print(f"Cache hit ({cache_type}) for {self.name}")
                    return cached_response
                
                # Generar nueva respuesta
                self.cache_misses += 1
                response = await super().generate_response(messages, sender, **kwargs)
                
                # Guardar en caché
                await self.cache_system.cache_response(
                    self.name, last_message, context, response
                )
                
                return response
            
            def get_cache_stats(self):
                """Obtiene estadísticas de caché"""
                total = self.cache_hits + self.cache_misses
                hit_rate = self.cache_hits / total if total > 0 else 0
                
                return {
                    "hits": self.cache_hits,
                    "misses": self.cache_misses,
                    "hit_rate": hit_rate
                }
        
        return CachedAssistant(self)
```

### 3. Sistema de Gestión de Estado Complejo

```python
from enum import Enum
from typing import Dict, Any, Optional
import asyncio
from dataclasses import dataclass, field
from datetime import datetime

class AgentState(Enum):
    """Estados posibles de un agente"""
    IDLE = "idle"
    PROCESSING = "processing"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"

@dataclass
class StateSnapshot:
    """Snapshot del estado del sistema"""
    timestamp: datetime
    agent_states: Dict[str, AgentState]
    pending_tasks: list
    completed_tasks: list
    context: Dict[str, Any] = field(default_factory=dict)

class StatefulAgentSystem:
    """Sistema con gestión avanzada de estado"""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.global_state: Dict[str, Any] = {}
        self.state_history: list[StateSnapshot] = []
        self.state_lock = asyncio.Lock()
    
    async def update_agent_state(self, agent_name: str, new_state: AgentState, 
                                context: Optional[Dict] = None):
        """Actualiza el estado de un agente"""
        async with self.state_lock:
            if agent_name not in self.agents:
                self.agents[agent_name] = {
                    "state": new_state,
                    "context": context or {},
                    "state_history": []
                }
            else:
                # Guardar estado anterior
                old_state = self.agents[agent_name]["state"]
                self.agents[agent_name]["state_history"].append({
                    "from": old_state,
                    "to": new_state,
                    "timestamp": datetime.now(),
                    "context": context
                })
                
                # Actualizar estado
                self.agents[agent_name]["state"] = new_state
                if context:
                    self.agents[agent_name]["context"].update(context)
            
            # Tomar snapshot
            await self._take_snapshot()
    
    async def _take_snapshot(self):
        """Toma un snapshot del estado actual"""
        snapshot = StateSnapshot(
            timestamp=datetime.now(),
            agent_states={name: data["state"] for name, data in self.agents.items()},
            pending_tasks=self.global_state.get("pending_tasks", []),
            completed_tasks=self.global_state.get("completed_tasks", []),
            context=self.global_state.copy()
        )
        
        self.state_history.append(snapshot)
        
        # Limitar historial
        if len(self.state_history) > 1000:
            self.state_history = self.state_history[-500:]
    
    async def get_agent_state(self, agent_name: str) -> Optional[AgentState]:
        """Obtiene el estado actual de un agente"""
        async with self.state_lock:
            return self.agents.get(agent_name, {}).get("state")
    
    async def rollback_to_snapshot(self, snapshot_index: int):
        """Revierte el sistema a un snapshot anterior"""
        async with self.state_lock:
            if 0 <= snapshot_index < len(self.state_history):
                snapshot = self.state_history[snapshot_index]
                
                # Restaurar estados
                for agent_name, state in snapshot.agent_states.items():
                    if agent_name in self.agents:
                        self.agents[agent_name]["state"] = state
                
                # Restaurar estado global
                self.global_state = snapshot.context.copy()
                
                return True
            return False
    
    def create_stateful_agent(self, name: str, model_client, system_message: str):
        """Crea un agente con gestión de estado"""
        
        class StatefulAgent(AssistantAgent):
            def __init__(self, state_system):
                super().__init__(
                    name=name,
                    model_client=model_client,
                    system_message=system_message
                )
                self.state_system = state_system
            
            async def on_message_received(self, message, sender, **kwargs):
                """Maneja recepción de mensajes con estado"""
                # Actualizar estado a procesando
                await self.state_system.update_agent_state(
                    self.name, 
                    AgentState.PROCESSING,
                    {"current_message": str(message)[:100]}
                )
                
                try:
                    # Procesar mensaje
                    response = await super().on_message_received(message, sender, **kwargs)
                    
                    # Actualizar estado a completado
                    await self.state_system.update_agent_state(
                        self.name,
                        AgentState.COMPLETED,
                        {"last_response": str(response)[:100]}
                    )
                    
                    return response
                    
                except Exception as e:
                    # Actualizar estado a error
                    await self.state_system.update_agent_state(
                        self.name,
                        AgentState.ERROR,
                        {"error": str(e)}
                    )
                    raise
        
        return StatefulAgent(self)
```

## Ejemplos de Implementación Completos

### 1. Sistema de Análisis de Documentos Empresariales

```python
import asyncio
from autogen_agentchat import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_ext.models import OpenAIChatCompletionClient
from autogen_ext.tools import PythonCodeExecutor

async def create_document_analysis_system():
    """Sistema completo para análisis de documentos empresariales"""
    
    # Configurar modelo
    model_client = OpenAIChatCompletionClient(
        model="gpt-4-turbo-preview",
        api_key="tu-key"
    )
    
    # Extractor de información
    extractor = AssistantAgent(
        name="info_extractor",
        model_client=model_client,
        system_message="""Experto en extracción de información de documentos.
        Extraes datos clave, entidades, fechas, montos y relaciones.
        Estructuras la información en formato JSON."""
    )
    
    # Analizador de sentimiento y tono
    sentiment_analyzer = AssistantAgent(
        name="sentiment_analyzer",
        model_client=model_client,
        system_message="""Experto en análisis de sentimiento y tono.
        Identificas emociones, intenciones y el tono general del documento.
        Proporcionas métricas de confianza."""
    )
    
    # Verificador de cumplimiento
    compliance_checker = AssistantAgent(
        name="compliance_checker",
        model_client=model_client,
        system_message="""Experto en cumplimiento y regulaciones.
        Verificas que los documentos cumplan con normativas aplicables.
        Identificas riesgos potenciales y áreas de mejora."""
    )
    
    # Generador de resúmenes
    summarizer = AssistantAgent(
        name="summarizer",
        model_client=model_client,
        system_message="""Experto en crear resúmenes ejecutivos.
        Produces resúmenes concisos, claros y accionables.
        Destacas puntos clave y recomendaciones."""
    )
    
    # Visualizador de datos
    visualizer = AssistantAgent(
        name="data_visualizer",
        model_client=model_client,
        system_message="""Experto en visualización de datos.
        Creas gráficos claros usando matplotlib y seaborn.
        Diseñas dashboards informativos.""",
        tools=[PythonCodeExecutor(work_dir="./visualizations")]
    )
    
    # Coordinador ejecutor
    executor = UserProxyAgent(
        name="analysis_coordinator",
        code_execution_config={
            "work_dir": "./analysis_output",
            "use_docker": True
        }
    )
    
    # Crear equipo selector
    team = SelectorGroupChat(
        participants=[extractor, sentiment_analyzer, compliance_checker, 
                     summarizer, visualizer, executor],
        model_client=model_client,
        selector_prompt="""Selecciona el agente apropiado:
        - Info Extractor: Para extraer datos del documento
        - Sentiment Analyzer: Para análisis de tono y sentimiento
        - Compliance Checker: Para verificar cumplimiento
        - Summarizer: Para crear resúmenes
        - Data Visualizer: Para crear gráficos
        - Analysis Coordinator: Para ejecutar código y coordinar""",
        termination_condition=TextMentionTermination("ANALYSIS_COMPLETE")
    )
    
    return team

# Usar el sistema
async def analyze_document(document_path: str):
    team = await create_document_analysis_system()
    
    result = await team.run(
        task=f"""Analiza el documento en {document_path}:
        
        1. Extrae toda la información relevante
        2. Analiza el sentimiento y tono
        3. Verifica cumplimiento normativo
        4. Crea un resumen ejecutivo
        5. Genera visualizaciones de datos clave
        
        Proporciona un informe completo con todos los hallazgos."""
    )
    
    return result
```

### 2. Sistema de Trading Algorítmico

```python
from autogen_core import SingleThreadedAgentRuntime, Agent, MessageContext
from autogen_agentchat import AssistantAgent
from autogen_ext.models import OpenAIChatCompletionClient
import numpy as np
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class MarketData:
    symbol: str
    price: float
    volume: int
    timestamp: datetime

@dataclass
class TradingSignal:
    symbol: str
    action: str  # BUY, SELL, HOLD
    confidence: float
    reason: str

class TradingSystem:
    """Sistema de trading algorítmico con múltiples estrategias"""
    
    def __init__(self):
        self.runtime = SingleThreadedAgentRuntime()
        self.model_client = OpenAIChatCompletionClient(
            model="gpt-4-turbo-preview",
            api_key="tu-key"
        )
        self.positions: Dict[str, float] = {}
        self.cash = 100000.0  # Capital inicial
    
    async def setup_agents(self):
        """Configura los agentes del sistema de trading"""
        
        # Analizador técnico
        technical_analyst = AssistantAgent(
            name="technical_analyst",
            model_client=self.model_client,
            system_message="""Experto en análisis técnico de mercados.
            Analizas patrones, indicadores técnicos y tendencias.
            Proporcionas señales de trading basadas en análisis técnico."""
        )
        
        # Analizador fundamental
        fundamental_analyst = AssistantAgent(
            name="fundamental_analyst",
            model_client=self.model_client,
            system_message="""Experto en análisis fundamental.
            Evalúas noticias, eventos económicos y fundamentos de empresas.
            Proporcionas perspectivas de largo plazo."""
        )
        
        # Gestor de riesgo
        risk_manager = AssistantAgent(
            name="risk_manager",
            model_client=self.model_client,
            system_message="""Experto en gestión de riesgo financiero.
            Calculas exposición, VaR, y límites de posición.
            Aseguras que las operaciones cumplan con políticas de riesgo."""
        )
        
        # Ejecutor de órdenes
        order_executor = Agent()
        
        class OrderExecutorAgent(Agent):
            async def on_message(self, message: TradingSignal, ctx: MessageContext):
                """Ejecuta órdenes de trading"""
                if message.confidence > 0.7:
                    if message.action == "BUY":
                        await self.execute_buy(message.symbol, message.confidence)
                    elif message.action == "SELL":
                        await self.execute_sell(message.symbol, message.confidence)
                
                return f"Orden ejecutada: {message.action} {message.symbol}"
            
            async def execute_buy(self, symbol: str, confidence: float):
                """Ejecuta orden de compra"""
                # Lógica de ejecución
                pass
            
            async def execute_sell(self, symbol: str, confidence: float):
                """Ejecuta orden de venta"""
                # Lógica de ejecución
                pass
        
        # Registrar agentes
        await self.runtime.register(
            "technical", 
            lambda: technical_analyst,
            subscriptions=lambda: [TypeSubscription("market_data", "technical")]
        )
        
        await self.runtime.register(
            "fundamental",
            lambda: fundamental_analyst,
            subscriptions=lambda: [TypeSubscription("news_data", "fundamental")]
        )
        
        await self.runtime.register(
            "risk",
            lambda: risk_manager,
            subscriptions=lambda: [TypeSubscription("trading_signal", "risk")]
        )
        
        await self.runtime.register(
            "executor",
            lambda: OrderExecutorAgent(),
            subscriptions=lambda: [TypeSubscription("approved_signal", "executor")]
        )
    
    async def process_market_data(self, data: MarketData):
        """Procesa datos de mercado"""
        # Publicar a analizadores
        await self.runtime.publish_message(
            data,
            TopicId(type="market_data", source="market_feed")
        )
    
    async def get_portfolio_status(self) -> Dict:
        """Obtiene el estado actual del portfolio"""
        total_value = self.cash
        
        for symbol, shares in self.positions.items():
            # Obtener precio actual
            current_price = await self.get_current_price(symbol)
            total_value += shares * current_price
        
        return {
            "cash": self.cash,
            "positions": self.positions,
            "total_value": total_value,
            "returns": (total_value - 100000) / 100000 * 100
        }
```

### 3. Sistema de Soporte al Cliente Inteligente

```python
from autogen_agentchat import AssistantAgent
from autogen_agentchat.teams import Swarm
from autogen_ext.models import OpenAIChatCompletionClient
from autogen_ext.storage import ChromaVectorDB
from typing import Dict, List

class CustomerSupportSystem:
    """Sistema de soporte al cliente con múltiples niveles"""
    
    def __init__(self):
        self.model_client = OpenAIChatCompletionClient(
            model="gpt-4-turbo-preview",
            api_key="tu-key"
        )
        
        # Base de conocimientos
        self.knowledge_base = ChromaVectorDB(
            collection_name="support_docs",
            embedding_function=OpenAIEmbeddingFunction()
        )
        
        self.conversation_history: Dict[str, List] = {}
    
    def create_support_agents(self):
        """Crea agentes especializados de soporte"""
        
        # Agente de primer nivel (triaje)
        triage_agent = AssistantAgent(
            name="triage_agent",
            model_client=self.model_client,
            system_message="""Eres el primer punto de contacto para clientes.
            Eres amable, empático y eficiente. Clasificas las consultas y
            las derivas al especialista apropiado.""",
            handoffs=["technical_support", "billing_support", "sales_support", "escalation"]
        )
        
        # Soporte técnico
        technical_support = AssistantAgent(
            name="technical_support",
            model_client=self.model_client,
            system_message="""Experto en soporte técnico. Resuelves problemas
            técnicos, guías en configuraciones y troubleshooting.
            Eres paciente y claro en tus explicaciones.""",
            handoffs=["escalation"]
        )
        
        # Soporte de facturación
        billing_support = AssistantAgent(
            name="billing_support",
            model_client=self.model_client,
            system_message="""Experto en facturación y pagos. Manejas consultas
            sobre facturas, planes, pagos y reembolsos. Eres preciso con
            números y fechas.""",
            handoffs=["escalation"]
        )
        
        # Soporte de ventas
        sales_support = AssistantAgent(
            name="sales_support",
            model_client=self.model_client,
            system_message="""Experto en ventas y productos. Ayudas a clientes
            a elegir el producto adecuado, explicas características y beneficios.
            Eres persuasivo pero no agresivo.""",
            handoffs=["escalation"]
        )
        
        # Escalación a humano
        escalation = AssistantAgent(
            name="escalation",
            model_client=self.model_client,
            system_message="""Manejas casos que requieren atención humana.
            Recopilas toda la información relevante y preparas el caso
            para transferencia a un agente humano.""",
            handoffs=[]
        )
        
        return {
            "triage": triage_agent,
            "technical": technical_support,
            "billing": billing_support,
            "sales": sales_support,
            "escalation": escalation
        }
    
    async def handle_customer_query(self, customer_id: str, query: str):
        """Maneja una consulta de cliente"""
        
        # Obtener historial
        history = self.conversation_history.get(customer_id, [])
        
        # Buscar en base de conocimientos
        relevant_docs = await self.knowledge_base.search(query, top_k=3)
        
        # Crear contexto
        context = {
            "customer_id": customer_id,
            "history": history[-5:],  # Últimas 5 interacciones
            "knowledge_base": relevant_docs
        }
        
        # Crear swarm de soporte
        agents = self.create_support_agents()
        swarm = Swarm(
            participants=list(agents.values()),
            termination_condition=TextMentionTermination("RESOLVED")
        )
        
        # Procesar consulta
        result = await swarm.run(
            task=f"""Cliente {customer_id} consulta: {query}
            
            Contexto disponible:
            - Historial de conversación
            - Base de conocimientos relevante
            
            Resuelve la consulta del cliente de manera eficiente y amable.""",
            initial_agent="triage_agent",
            context=context
        )
        
        # Guardar en historial
        self.conversation_history[customer_id].append({
            "query": query,
            "response": result.messages,
            "timestamp": datetime.now()
        })
        
        return result
    
    async def analyze_support_metrics(self):
        """Analiza métricas de soporte"""
        
        analyst = AssistantAgent(
            name="support_analyst",
            model_client=self.model_client,
            system_message="""Analizas métricas de soporte al cliente.
            Identificas patrones, áreas de mejora y generas reportes."""
        )
        
        # Recopilar datos
        total_conversations = len(self.conversation_history)
        resolution_times = []
        escalation_rate = 0
        
        # Análisis
        result = await analyst.run(
            task=f"""Analiza las métricas de soporte:
            - Total de conversaciones: {total_conversations}
            - Tasa de escalación: {escalation_rate}%
            
            Proporciona insights y recomendaciones."""
        )
        
        return result
```

## Guía de Migración y Mejores Prácticas

### Migración desde versiones anteriores

```python
# Antiguo (pyautogen <= 0.2)
from autogen import AssistantAgent, UserProxyAgent

# Nuevo (autogen-agentchat >= 0.4)
from autogen_agentchat import AssistantAgent, UserProxyAgent
from autogen_ext.models import OpenAIChatCompletionClient

# Cambios principales:
# 1. Modelos ahora son clientes separados
# 2. Importaciones desde paquetes específicos
# 3. Configuración más modular

# Ejemplo de migración:
# Antiguo
assistant = AssistantAgent(
    "assistant",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": "key"}]}
)

# Nuevo
model_client = OpenAIChatCompletionClient(model="gpt-4", api_key="key")
assistant = AssistantAgent("assistant", model_client=model_client)
```

### Mejores Prácticas para Producción

```python
# 1. Gestión de errores robusta
from autogen_core.exceptions import AgentError
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

class ProductionAgent(AssistantAgent):
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate_response_with_retry(self, messages, **kwargs):
        try:
            return await self.generate_response(messages, **kwargs)
        except AgentError as e:
            # Log error
            logger.error(f"Agent error: {e}")
            # Fallback response
            return "Lo siento, hay un problema técnico. Por favor intenta más tarde."

# 2. Configuración por entorno
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    model_name: str = "gpt-4-turbo-preview"
    max_agents: int = 10
    cache_ttl: int = 3600
    use_docker: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()

# 3. Logging estructurado
import structlog

logger = structlog.get_logger()

class LoggedAgent(AssistantAgent):
    async def on_message(self, message, ctx):
        logger.info(
            "message_received",
            agent=self.name,
            message_type=type(message).__name__,
            context_id=ctx.message_id
        )
        
        result = await super().on_message(message, ctx)
        
        logger.info(
            "message_processed",
            agent=self.name,
            success=True,
            response_length=len(str(result))
        )
        
        return result
```

## Recursos y Referencias

- **Documentación Oficial**: 
  - autogen-core: [https://microsoft.github.io/autogen/docs/core](https://microsoft.github.io/autogen/docs/core)
  - autogen-agentchat: [https://microsoft.github.io/autogen/docs/agentchat](https://microsoft.github.io/autogen/docs/agentchat)
  - autogen-ext: [https://microsoft.github.io/autogen/docs/extensions](https://microsoft.github.io/autogen/docs/extensions)

- **Repositorios GitHub**:
  - Principal: [https://github.com/microsoft/autogen](https://github.com/microsoft/autogen)
  - Ejemplos: [https://github.com/microsoft/autogen/tree/main/python/packages](https://github.com/microsoft/autogen/tree/main/python/packages)

- **Comunidad**:
  - Discord: [https://discord.gg/pAbnFJrkgZ](https://discord.gg/pAbnFJrkgZ)
  - Discussions: [https://github.com/microsoft/autogen/discussions](https://github.com/microsoft/autogen/discussions)

- **Tutoriales y Guías**:
  - Getting Started: [https://microsoft.github.io/autogen/docs/getting-started](https://microsoft.github.io/autogen/docs/getting-started)
  - Cookbook: [https://microsoft.github.io/autogen/docs/cookbook](https://microsoft.github.io/autogen/docs/cookbook)

## Conclusión

La nueva arquitectura modular de AutoGen con `autogen-core` y `autogen-agentchat` representa una evolución significativa del framework, ofreciendo:

1. **Mayor Flexibilidad**: Arquitectura modular que permite usar solo los componentes necesarios
2. **Mejor Rendimiento**: Runtime asíncrono nativo para operaciones concurrentes
3. **Escalabilidad**: Diseñado para sistemas de producción con múltiples agentes
4. **Extensibilidad**: Sistema de plugins y fácil integración con servicios externos
5. **Robustez**: Mejor manejo de errores y capacidades de monitoreo

Para mantenerte actualizado:
- Sigue las releases en GitHub
- Únete a la comunidad en Discord
- Experimenta con los ejemplos oficiales
- Contribuye al proyecto open source

AutoGen continúa siendo una de las plataformas más avanzadas para crear sistemas multi-agente inteligentes, con un futuro prometedor en la automatización y colaboración de IA.