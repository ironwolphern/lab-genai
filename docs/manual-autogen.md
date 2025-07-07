# Manual Completo de AutoGen - Versión más reciente (Julio 2025)

## ¿Qué es AutoGen?

AutoGen es un framework de código abierto desarrollado por Microsoft que permite crear aplicaciones con múltiples agentes conversacionales basados en Large Language Models (LLMs). El framework ha evolucionado significativamente, ofreciendo capacidades avanzadas para la orquestación de agentes de IA.

## Estado Actual del Framework (Julio 2025)

Según la información más reciente disponible, AutoGen continúa siendo activamente desarrollado con actualizaciones regulares. El proyecto mantiene su enfoque en:

- **Multi-agente colaborativo**: Agentes que trabajan juntos para resolver problemas complejos
- **Flexibilidad de modelos**: Soporte para múltiples proveedores de LLM
- **Ejecución de código segura**: Entornos sandboxed para ejecutar código generado
- **Arquitectura extensible**: Sistema de plugins y componentes personalizables

## Instalación de la Última Versión

```bash
# Instalación básica (última versión estable)
pip install pyautogen --upgrade

# Instalación con todas las características
pip install "pyautogen[all]" --upgrade

# Verificar versión instalada
python -c "import autogen; print(autogen.__version__)"

# Instalación para desarrollo
pip install "pyautogen[dev]" --upgrade

# Instalación con soporte para bases de datos
pip install "pyautogen[retrievechat]" --upgrade
```

## Arquitectura y Conceptos Fundamentales

### Tipos de Agentes Principales

1. **ConversableAgent**: Clase base para todos los agentes
2. **AssistantAgent**: Agente potenciado por LLM para tareas generales
3. **UserProxyAgent**: Representa al usuario y puede ejecutar código
4. **GroupChatManager**: Coordina conversaciones entre múltiples agentes
5. **RetrieveUserProxyAgent**: Agente con capacidades de recuperación de información

### Configuración Moderna

```python
import autogen
from typing import Dict, List, Optional

# Configuración flexible para múltiples modelos
config_list = [
    {
        "model": "gpt-4-turbo",
        "api_key": "tu-api-key",
        "api_type": "openai",
        "temperature": 0.7,
        "max_tokens": 2000,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0
    },
    {
        "model": "claude-3-opus",
        "api_key": "tu-anthropic-key",
        "api_type": "anthropic",
        "temperature": 0.5
    }
]

# Configuración con caché y límites
llm_config = {
    "config_list": config_list,
    "cache_seed": 42,  # Para resultados reproducibles
    "temperature": 0.7,
    "timeout": 600,
    "max_retries": 3,
    "retry_wait_time": 5
}
```

## Ejemplo Básico Actualizado

```python
import autogen
import os
from datetime import datetime

# Configuración usando variables de entorno
config_list = [
    {
        "model": "gpt-4-turbo",
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
]

# Crear agente asistente
assistant = autogen.AssistantAgent(
    name="coding_assistant",
    llm_config={
        "config_list": config_list,
        "temperature": 0,
        "seed": 42,
    },
    system_message="""Eres un programador experto en Python. 
    Sigue estas reglas:
    1. Escribe código limpio y bien documentado
    2. Incluye manejo de errores
    3. Usa type hints cuando sea apropiado
    4. Sigue PEP 8"""
)

# Crear agente usuario/ejecutor
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",  # Opciones: NEVER, TERMINATE, ALWAYS
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": f"workspace_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "use_docker": False,  # True para mayor seguridad
        "timeout": 120,
        "last_n_messages": 3
    }
)

# Iniciar conversación
response = user_proxy.initiate_chat(
    assistant,
    message="""Crea una clase Python para gestionar una lista de tareas (TODO list) 
    con las siguientes funcionalidades:
    1. Agregar tareas
    2. Marcar tareas como completadas
    3. Listar tareas pendientes y completadas
    4. Guardar y cargar desde archivo JSON
    """,
    summary_method="reflection_with_llm",
    summary_args={
        "summary_prompt": "Resume los puntos clave y el código generado"
    }
)
```

## Patrones Avanzados de Diseño

### 1. Patrón de Agentes Especializados

```python
import autogen
from typing import Dict, Any

class SpecializedAgentSystem:
    """Sistema con agentes especializados para diferentes tareas"""
    
    def __init__(self, config_list: List[Dict[str, Any]]):
        self.config_list = config_list
        self.llm_config = {
            "config_list": config_list,
            "temperature": 0.7,
            "cache_seed": 42
        }
        self._setup_agents()
    
    def _setup_agents(self):
        # Agente de investigación
        self.researcher = autogen.AssistantAgent(
            name="researcher",
            llm_config=self.llm_config,
            system_message="""Eres un investigador experto. Tu trabajo es:
            1. Buscar información relevante
            2. Verificar fuentes
            3. Sintetizar hallazgos
            4. Proporcionar referencias"""
        )
        
        # Agente de análisis
        self.analyst = autogen.AssistantAgent(
            name="analyst",
            llm_config=self.llm_config,
            system_message="""Eres un analista de datos. Tu trabajo es:
            1. Analizar información cuantitativa
            2. Identificar patrones
            3. Crear visualizaciones
            4. Generar insights accionables"""
        )
        
        # Agente escritor
        self.writer = autogen.AssistantAgent(
            name="writer",
            llm_config=self.llm_config,
            system_message="""Eres un escritor técnico experto. Tu trabajo es:
            1. Crear documentación clara
            2. Estructurar información lógicamente
            3. Usar lenguaje apropiado para la audiencia
            4. Incluir ejemplos relevantes"""
        )
        
        # Agente revisor
        self.reviewer = autogen.AssistantAgent(
            name="reviewer",
            llm_config=self.llm_config,
            system_message="""Eres un revisor crítico. Tu trabajo es:
            1. Verificar precisión técnica
            2. Evaluar claridad y coherencia
            3. Sugerir mejoras
            4. Asegurar calidad"""
        )
        
        # Coordinador
        self.coordinator = autogen.UserProxyAgent(
            name="coordinator",
            human_input_mode="NEVER",
            code_execution_config=False,
            max_consecutive_auto_reply=1
        )
    
    def process_request(self, request: str) -> str:
        """Procesa una solicitud usando el sistema de agentes"""
        
        # Fase 1: Investigación
        research_result = self.coordinator.initiate_chat(
            self.researcher,
            message=f"Investiga sobre: {request}",
            max_turns=2
        )
        
        # Fase 2: Análisis
        analysis_result = self.coordinator.initiate_chat(
            self.analyst,
            message=f"Analiza estos hallazgos: {research_result.summary}",
            max_turns=2
        )
        
        # Fase 3: Redacción
        draft = self.coordinator.initiate_chat(
            self.writer,
            message=f"Escribe un informe basado en: {analysis_result.summary}",
            max_turns=2
        )
        
        # Fase 4: Revisión
        final_result = self.coordinator.initiate_chat(
            self.reviewer,
            message=f"Revisa y mejora este informe: {draft.summary}",
            max_turns=2
        )
        
        return final_result.summary
```

### 2. Patrón de Chat Grupal Avanzado

```python
import autogen
from autogen import GroupChat, GroupChatManager

def create_advanced_group_chat(config_list):
    """Crea un sistema de chat grupal con roles específicos"""
    
    # Configuración base
    llm_config = {"config_list": config_list, "cache_seed": 42}
    
    # Agente Product Manager
    pm = autogen.AssistantAgent(
        name="product_manager",
        llm_config=llm_config,
        system_message="""Eres un Product Manager. Tu rol es:
        - Definir requisitos y especificaciones
        - Priorizar características
        - Asegurar que el producto cumpla las necesidades del usuario
        - Coordinar entre equipos técnicos y de negocio"""
    )
    
    # Agente Arquitecto
    architect = autogen.AssistantAgent(
        name="architect",
        llm_config=llm_config,
        system_message="""Eres un Arquitecto de Software. Tu rol es:
        - Diseñar la arquitectura del sistema
        - Definir patrones y mejores prácticas
        - Asegurar escalabilidad y mantenibilidad
        - Revisar decisiones técnicas importantes"""
    )
    
    # Agente Desarrollador Senior
    senior_dev = autogen.AssistantAgent(
        name="senior_developer",
        llm_config=llm_config,
        system_message="""Eres un Desarrollador Senior. Tu rol es:
        - Implementar funcionalidades complejas
        - Mentorear a otros desarrolladores
        - Revisar código
        - Optimizar rendimiento"""
    )
    
    # Agente QA Engineer
    qa_engineer = autogen.AssistantAgent(
        name="qa_engineer",
        llm_config=llm_config,
        system_message="""Eres un QA Engineer. Tu rol es:
        - Diseñar casos de prueba
        - Encontrar bugs y problemas
        - Asegurar calidad del código
        - Automatizar pruebas cuando sea posible"""
    )
    
    # Agente DevOps
    devops = autogen.AssistantAgent(
        name="devops_engineer",
        llm_config=llm_config,
        system_message="""Eres un DevOps Engineer. Tu rol es:
        - Configurar CI/CD pipelines
        - Gestionar infraestructura
        - Monitorear sistemas
        - Automatizar despliegues"""
    )
    
    # Ejecutor de código
    executor = autogen.UserProxyAgent(
        name="executor",
        system_message="Ejecutor de código. Ejecuta código cuando se requiera.",
        human_input_mode="NEVER",
        code_execution_config={
            "work_dir": "project_workspace",
            "use_docker": True,
        }
    )
    
    # Configurar chat grupal
    groupchat = GroupChat(
        agents=[pm, architect, senior_dev, qa_engineer, devops, executor],
        messages=[],
        max_round=50,
        speaker_selection_method="auto",
        allow_repeat_speaker=False
    )
    
    # Manager del chat
    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config
    )
    
    return executor, manager

# Uso del chat grupal
def develop_project(project_description: str, config_list):
    """Desarrolla un proyecto usando el equipo de agentes"""
    
    executor, manager = create_advanced_group_chat(config_list)
    
    # Iniciar el proyecto
    result = executor.initiate_chat(
        manager,
        message=f"""Necesitamos desarrollar: {project_description}
        
        Por favor, sigan este proceso:
        1. Product Manager: Define los requisitos
        2. Arquitecto: Diseña la arquitectura
        3. Senior Developer: Implementa el código core
        4. QA Engineer: Define y ejecuta pruebas
        5. DevOps: Prepara el despliegue
        
        Trabajen colaborativamente y asegúrense de que cada paso esté completo 
        antes de continuar al siguiente."""
    )
    
    return result
```

### 3. Patrón de Agente con Memoria y Contexto

```python
import autogen
import json
from typing import Dict, List, Any
from datetime import datetime

class MemoryAgent(autogen.AssistantAgent):
    """Agente con memoria persistente y gestión de contexto"""
    
    def __init__(self, name: str, llm_config: Dict, memory_file: str = None):
        super().__init__(name=name, llm_config=llm_config)
        self.memory_file = memory_file or f"{name}_memory.json"
        self.memory = self._load_memory()
        self.context_window = []
        self.max_context_size = 10
    
    def _load_memory(self) -> Dict[str, Any]:
        """Carga memoria desde archivo"""
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "conversations": [],
                "learned_facts": {},
                "user_preferences": {},
                "task_history": []
            }
    
    def _save_memory(self):
        """Guarda memoria en archivo"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2, default=str)
    
    def remember(self, key: str, value: Any):
        """Almacena información en memoria"""
        self.memory["learned_facts"][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.9
        }
        self._save_memory()
    
    def recall(self, key: str) -> Any:
        """Recupera información de memoria"""
        return self.memory["learned_facts"].get(key, {}).get("value")
    
    def add_to_context(self, message: str, response: str):
        """Agrega intercambio al contexto"""
        self.context_window.append({
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "response": response
        })
        
        # Mantener ventana de contexto limitada
        if len(self.context_window) > self.max_context_size:
            self.context_window.pop(0)
    
    def get_relevant_context(self, query: str) -> str:
        """Obtiene contexto relevante para la consulta"""
        # Aquí podrías implementar búsqueda semántica
        relevant_facts = []
        for key, fact in self.memory["learned_facts"].items():
            if query.lower() in key.lower():
                relevant_facts.append(f"{key}: {fact['value']}")
        
        context = "Contexto relevante:\n"
        if relevant_facts:
            context += "\n".join(relevant_facts[:5])
        
        # Agregar conversaciones recientes
        if self.context_window:
            context += "\n\nConversaciones recientes:\n"
            for item in self.context_window[-3:]:
                context += f"- {item['message'][:100]}...\n"
        
        return context
    
    def generate_reply(self, messages, sender, config=None):
        """Genera respuesta con contexto aumentado"""
        # Obtener el último mensaje
        last_message = messages[-1]["content"] if messages else ""
        
        # Obtener contexto relevante
        context = self.get_relevant_context(last_message)
        
        # Aumentar el mensaje con contexto
        augmented_message = f"{context}\n\nMensaje actual: {last_message}"
        
        # Generar respuesta
        response = super().generate_reply(
            [{"content": augmented_message, "role": "user"}],
            sender,
            config
        )
        
        # Guardar en contexto
        self.add_to_context(last_message, response)
        
        # Extraer y guardar hechos nuevos (simplificado)
        if "aprend" in response.lower() or "entiendo" in response.lower():
            # Aquí podrías usar NLP para extraer hechos
            self.remember(f"fact_{len(self.memory['learned_facts'])}", response)
        
        return response

# Uso del agente con memoria
def create_memory_agent_system():
    config_list = [{"model": "gpt-4", "api_key": "tu-key"}]
    
    # Agente con memoria
    memory_agent = MemoryAgent(
        name="assistant_with_memory",
        llm_config={"config_list": config_list},
        memory_file="assistant_memory.json"
    )
    
    # Usuario
    user = autogen.UserProxyAgent(
        name="user",
        human_input_mode="ALWAYS",
        max_consecutive_auto_reply=0
    )
    
    # Conversación
    user.initiate_chat(
        memory_agent,
        message="Hola, mi nombre es Juan y me gusta la programación en Python"
    )
    
    # El agente recordará esta información para futuras conversaciones
```

### 4. Sistema de Agentes con RAG (Retrieval Augmented Generation)

```python
import autogen
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
import chromadb

class RAGSystem:
    """Sistema de agentes con capacidades RAG"""
    
    def __init__(self, config_list, docs_path="docs/"):
        self.config_list = config_list
        self.docs_path = docs_path
        self._setup_agents()
    
    def _setup_agents(self):
        # Configuración para RAG
        self.retrieve_config = {
            "task": "qa",
            "docs_path": self.docs_path,
            "chunk_token_size": 1000,
            "model": self.config_list[0]["model"],
            "client": chromadb.PersistentClient(path="./chromadb"),
            "collection_name": "knowledge_base",
            "embedding_model": "all-MiniLM-L6-v2",
            "get_or_create": True,
        }
        
        # Agente RAG
        self.rag_agent = RetrieveUserProxyAgent(
            name="rag_assistant",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
            retrieve_config=self.retrieve_config,
            code_execution_config=False,
        )
        
        # Asistente que usa la información recuperada
        self.assistant = RetrieveAssistantAgent(
            name="assistant",
            system_message="""Eres un asistente experto que responde preguntas 
            basándote en la documentación proporcionada. 
            Siempre cita las fuentes de tu información.""",
            llm_config={"config_list": self.config_list},
        )
    
    def add_documents(self, documents: List[str]):
        """Agrega documentos a la base de conocimiento"""
        # Aquí implementarías la lógica para agregar documentos
        pass
    
    def query(self, question: str) -> str:
        """Realiza una consulta al sistema RAG"""
        self.rag_agent.reset()
        
        result = self.rag_agent.initiate_chat(
            self.assistant,
            problem=question,
            n_results=3,
        )
        
        return result.summary

# Uso del sistema RAG
def setup_rag_system():
    config_list = [{"model": "gpt-4", "api_key": "tu-key"}]
    
    rag_system = RAGSystem(
        config_list=config_list,
        docs_path="./knowledge_base/"
    )
    
    # Agregar documentos
    rag_system.add_documents([
        "manual_python.pdf",
        "best_practices.md",
        "api_documentation.txt"
    ])
    
    # Hacer consultas
    answer = rag_system.query("¿Cómo implementar async/await en Python?")
    print(answer)
```

## Integración con Herramientas Externas

### 1. Integración con APIs Web

```python
import autogen
import requests
from typing import Dict, Any

class WebAPIAgent(autogen.AssistantAgent):
    """Agente con capacidad de llamar APIs web"""
    
    def __init__(self, name: str, llm_config: Dict, api_configs: Dict[str, Dict]):
        super().__init__(name=name, llm_config=llm_config)
        self.api_configs = api_configs
        self.register_function(
            function_map={
                "call_api": self.call_api,
                "search_web": self.search_web,
                "get_weather": self.get_weather,
            }
        )
    
    def call_api(self, endpoint: str, method: str = "GET", 
                 params: Dict = None, data: Dict = None) -> Dict[str, Any]:
        """Llama a una API genérica"""
        try:
            response = requests.request(
                method=method,
                url=endpoint,
                params=params,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_web(self, query: str) -> str:
        """Busca en la web usando una API de búsqueda"""
        # Implementar búsqueda web
        pass
    
    def get_weather(self, location: str) -> Dict[str, Any]:
        """Obtiene información del clima"""
        # Implementar API del clima
        pass
```

### 2. Integración con Bases de Datos

```python
import autogen
import sqlite3
import pandas as pd
from typing import List, Dict, Any

class DatabaseAgent(autogen.AssistantAgent):
    """Agente con acceso a base de datos"""
    
    def __init__(self, name: str, llm_config: Dict, db_path: str):
        super().__init__(
            name=name,
            llm_config=llm_config,
            system_message="""Eres un experto en SQL y análisis de datos.
            Puedes ejecutar consultas SQL y analizar resultados."""
        )
        self.db_path = db_path
        self.register_function(
            function_map={
                "execute_sql": self.execute_sql,
                "analyze_data": self.analyze_data,
                "get_schema": self.get_schema,
            }
        )
    
    def execute_sql(self, query: str) -> pd.DataFrame:
        """Ejecuta una consulta SQL"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query(query, conn)
                return df.to_dict('records')
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_data(self, table_name: str) -> Dict[str, Any]:
        """Realiza análisis básico de una tabla"""
        query = f"SELECT * FROM {table_name} LIMIT 1000"
        df = pd.DataFrame(self.execute_sql(query))
        
        analysis = {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "null_counts": df.isnull().sum().to_dict(),
            "basic_stats": df.describe().to_dict() if not df.empty else {}
        }
        
        return analysis
    
    def get_schema(self) -> List[str]:
        """Obtiene el esquema de la base de datos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            schema = []
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table[0]})")
                columns = cursor.fetchall()
                schema.append({
                    "table": table[0],
                    "columns": [{"name": col[1], "type": col[2]} for col in columns]
                })
            
            return schema
```

## Mejores Prácticas y Optimización

### 1. Gestión de Costos

```python
class CostOptimizedAgent(autogen.AssistantAgent):
    """Agente optimizado para reducir costos"""
    
    def __init__(self, name: str, llm_config: Dict):
        # Configuración optimizada
        optimized_config = llm_config.copy()
        optimized_config.update({
            "cache_seed": 42,  # Habilitar caché
            "temperature": 0,  # Respuestas determinísticas
            "max_tokens": 500,  # Limitar longitud
        })
        
        super().__init__(
            name=name,
            llm_config=optimized_config,
            system_message="""Sé conciso y directo. 
            Evita repeticiones innecesarias."""
        )
        
        self.token_count = 0
        self.cost_estimate = 0.0
    
    def track_usage(self, response):
        """Rastrea uso de tokens y costos"""
        # Implementar tracking de tokens
        pass
```

### 2. Manejo Robusto de Errores

```python
import autogen
from typing import Optional
import logging

class RobustAgent(autogen.AssistantAgent):
    """Agente con manejo robusto de errores"""
    
    def __init__(self, name: str, llm_config: Dict):
        super().__init__(name=name, llm_config=llm_config)
        self.logger = logging.getLogger(name)
        self.error_count = 0
        self.max_errors = 3
    
    def safe_generate_reply(self, messages, sender, config=None) -> Optional[str]:
        """Genera respuesta con manejo de errores"""
        try:
            response = self.generate_reply(messages, sender, config)
            self.error_count = 0  # Reset en éxito
            return response
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"Error en generación: {e}")
            
            if self.error_count >= self.max_errors:
                return "Lo siento, estoy experimentando dificultades técnicas."
            
            # Reintentar con configuración más simple
            fallback_config = config or {}
            fallback_config["temperature"] = 0
            fallback_config["max_tokens"] = 100
            
            try:
                return self.generate_reply(messages, sender, fallback_config)
            except:
                return "Error al procesar la solicitud."
```

### 3. Monitoreo y Métricas

```python
import autogen
import time
from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class AgentMetrics:
    """Métricas de rendimiento del agente"""
    response_times: List[float]
    token_usage: List[int]
    error_count: int
    success_count: int
    
    def get_stats(self) -> Dict:
        return {
            "avg_response_time": sum(self.response_times) / len(self.response_times) if self.response_times else 0,
            "total_tokens": sum(self.token_usage),
            "error_rate": self.error_count / (self.error_count + self.success_count) if (self.error_count + self.success_count) > 0 else 0,
            "total_requests": self.error_count + self.success_count
        }

class MonitoredAgent(autogen.AssistantAgent):
    """Agente con capacidades de monitoreo"""
    
    def __init__(self, name: str, llm_config: Dict):
        super().__init__(name=name, llm_config=llm_config)
        self.metrics = AgentMetrics([], [], 0, 0)
    
    def generate_reply(self, messages, sender, config=None):
        """Genera respuesta con monitoreo"""
        start_time = time.time()
        
        try:
            response = super().generate_reply(messages, sender, config)
            
            # Registrar métricas
            self.metrics.response_times.append(time.time() - start_time)
            self.metrics.success_count += 1
            
            # Estimar tokens (simplificado)
            token_estimate = len(str(response).split()) * 1.3
            self.metrics.token_usage.append(int(token_estimate))
            
            return response
            
        except Exception as e:
            self.metrics.error_count += 1
            raise e
    
    def export_metrics(self, filepath: str):
        """Exporta métricas a archivo"""
        with open(filepath, 'w') as f:
            json.dump(self.metrics.get_stats(), f, indent=2)
```

## Casos de Uso Avanzados

### 1. Sistema de Desarrollo de Software Completo

```python
def create_software_development_system(config_list):
    """Sistema completo para desarrollo de software"""
    
    # Configuración base
    llm_config = {"config_list": config_list, "cache_seed": 42}
    
    # Product Owner
    product_owner = autogen.AssistantAgent(
        name="product_owner",
        llm_config=llm_config,
        system_message="""Eres el Product Owner. Define historias de usuario claras,
        criterios de aceptación y prioridades del producto."""
    )
    
    # Tech Lead
    tech_lead = autogen.AssistantAgent(
        name="tech_lead",
        llm_config=llm_config,
        system_message="""Eres el Tech Lead. Tomas decisiones de arquitectura,
        defines estándares técnicos y revisas el diseño general."""
    )
    
    # Backend Developer
    backend_dev = autogen.AssistantAgent(
        name="backend_developer",
        llm_config=llm_config,
        system_message="""Eres un Backend Developer experto en Python, FastAPI,
        bases de datos y microservicios. Escribes código limpio y escalable."""
    )
    
    # Frontend Developer
    frontend_dev = autogen.AssistantAgent(
        name="frontend_developer",
        llm_config=llm_config,
        system_message="""Eres un Frontend Developer experto en React, TypeScript,
        y diseño responsivo. Creas interfaces intuitivas y accesibles."""
    )
    
    # QA Automation Engineer
    qa_automation = autogen.AssistantAgent(
        name="qa_automation",
        llm_config=llm_config,
        system_message="""Eres un QA Automation Engineer. Escribes tests automatizados,
        defines estrategias de testing y aseguras la calidad del código."""
    )
    
    # DevOps Engineer
    devops = autogen.AssistantAgent(
        name="devops",
        llm_config=llm_config,
        system_message="""Eres un DevOps Engineer. Configuras CI/CD, gestionas
        infraestructura como código y optimizas el deployment."""
    )
    
    # Security Engineer
    security = autogen.AssistantAgent(
        name="security_engineer",
        llm_config=llm_config,
        system_message="""Eres un Security Engineer. Identificas vulnerabilidades,
        implementas mejores prácticas de seguridad y realizas auditorías."""
    )
    
    # Code Executor
    executor = autogen.UserProxyAgent(
        name="executor",
        human_input_mode="NEVER",
        code_execution_config={
            "work_dir": "software_project",
            "use_docker": True,
        }
    )
    
    # Configurar chat grupal con orden específico
    groupchat = GroupChat(
        agents=[product_owner, tech_lead, backend_dev, frontend_dev, 
                qa_automation, devops, security, executor],
        messages=[],
        max_round=100,
        speaker_selection_method="round_robin",
        allow_repeat_speaker=True
    )
    
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    
    return executor, manager

# Usar el sistema
def develop_application(project_description: str, config_list):
    executor, manager = create_software_development_system(config_list)
    
    result = executor.initiate_chat(
        manager,
        message=f"""Desarrollar una aplicación completa: {project_description}
        
        Proceso:
        1. Product Owner: Define requisitos y user stories
        2. Tech Lead: Diseña la arquitectura
        3. Backend Dev: Implementa API y lógica de negocio
        4. Frontend Dev: Crea la interfaz de usuario
        5. QA Automation: Escribe tests
        6. Security: Revisa seguridad
        7. DevOps: Prepara deployment
        
        Generen código funcional, documentación y tests."""
    )
    
    return result
```

### 2. Sistema de Análisis de Datos Inteligente

```python
class DataAnalysisSystem:
    """Sistema completo de análisis de datos con múltiples agentes"""
    
    def __init__(self, config_list):
        self.config_list = config_list
        self.llm_config = {"config_list": config_list}
        self._setup_agents()
    
    def _setup_agents(self):
        # Data Engineer
        self.data_engineer = autogen.AssistantAgent(
            name="data_engineer",
            llm_config=self.llm_config,
            system_message="""Eres un Data Engineer experto. Tu trabajo incluye:
            - Limpiar y preparar datos
            - Crear pipelines de datos
            - Optimizar consultas y almacenamiento
            - Implementar validaciones de calidad de datos"""
        )
        
        # Data Scientist
        self.data_scientist = autogen.AssistantAgent(
            name="data_scientist",
            llm_config=self.llm_config,
            system_message="""Eres un Data Scientist experto. Tu trabajo incluye:
            - Análisis exploratorio de datos
            - Creación de modelos predictivos
            - Feature engineering
            - Validación de modelos"""
        )
        
        # Business Analyst
        self.business_analyst = autogen.AssistantAgent(
            name="business_analyst",
            llm_config=self.llm_config,
            system_message="""Eres un Business Analyst. Tu trabajo incluye:
            - Traducir insights técnicos a lenguaje de negocio
            - Identificar oportunidades de mejora
            - Crear dashboards y reportes ejecutivos
            - Definir KPIs relevantes"""
        )
        
        # Visualization Expert
        self.viz_expert = autogen.AssistantAgent(
            name="visualization_expert",
            llm_config=self.llm_config,
            system_message="""Eres un experto en visualización de datos. Tu trabajo incluye:
            - Crear gráficos claros y efectivos
            - Diseñar dashboards interactivos
            - Usar matplotlib, seaborn, plotly
            - Seguir mejores prácticas de visualización"""
        )
        
        # Code Executor
        self.executor = autogen.UserProxyAgent(
            name="data_executor",
            human_input_mode="NEVER",
            code_execution_config={
                "work_dir": "data_analysis",
                "use_docker": False,
            }
        )
    
    def analyze_dataset(self, dataset_path: str, business_question: str):
        """Analiza un dataset completo respondiendo a una pregunta de negocio"""
        
        # Fase 1: Preparación de datos
        data_prep = self.executor.initiate_chat(
            self.data_engineer,
            message=f"""Prepara el dataset en {dataset_path} para análisis.
            Incluye: limpieza, validación, y creación de features relevantes."""
        )
        
        # Fase 2: Análisis científico
        analysis = self.executor.initiate_chat(
            self.data_scientist,
            message=f"""Realiza un análisis completo del dataset preparado.
            Pregunta de negocio: {business_question}
            Incluye estadísticas descriptivas, correlaciones y modelos si aplica."""
        )
        
        # Fase 3: Visualizaciones
        visualizations = self.executor.initiate_chat(
            self.viz_expert,
            message="""Crea visualizaciones impactantes de los hallazgos principales.
            Incluye gráficos para presentación ejecutiva."""
        )
        
        # Fase 4: Reporte de negocio
        business_report = self.executor.initiate_chat(
            self.business_analyst,
            message="""Crea un reporte ejecutivo con los hallazgos principales,
            recomendaciones accionables y próximos pasos."""
        )
        
        return {
            "data_preparation": data_prep.summary,
            "analysis": analysis.summary,
            "visualizations": visualizations.summary,
            "business_report": business_report.summary
        }
```

## Guía de Solución de Problemas

### Problemas Comunes y Soluciones

```python
# 1. Problema: Rate Limiting
def handle_rate_limit():
    config_list = [{
        "model": "gpt-4",
        "api_key": "key",
        "api_type": "openai",
        "max_retries": 5,
        "retry_wait_time": 10,
        "timeout": 120
    }]
    
    # Usar múltiples API keys
    config_list_multiple = [
        {"model": "gpt-4", "api_key": "key1"},
        {"model": "gpt-4", "api_key": "key2"},
        {"model": "gpt-3.5-turbo", "api_key": "key3"},  # Fallback
    ]

# 2. Problema: Memoria/Contexto largo
def handle_long_context():
    # Dividir tareas largas
    chunk_size = 1000
    text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    # Procesar por partes
    results = []
    for chunk in text_chunks:
        result = agent.generate_reply([{"content": chunk, "role": "user"}])
        results.append(result)

# 3. Problema: Ejecución de código insegura
def safe_code_execution():
    execution_config = {
        "work_dir": "sandbox",
        "use_docker": True,  # Siempre True en producción
        "timeout": 60,
        "last_n_messages": 3
    }

# 4. Problema: Costos altos
def optimize_costs():
    # Usar modelos más económicos para tareas simples
    simple_task_config = {
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "max_tokens": 150
    }
    
    # Caché agresivo
    llm_config = {
        "config_list": config_list,
        "cache_seed": 42,
        "cache": autogen.Cache.disk()  # Cache en disco
    }
```

## Recursos y Referencias Actualizadas

- **Repositorio GitHub**: [https://github.com/microsoft/autogen](https://github.com/microsoft/autogen)
- **Documentación Oficial**: [https://microsoft.github.io/autogen/](https://microsoft.github.io/autogen/)
- **Tutoriales y Notebooks**: [https://github.com/microsoft/autogen/tree/main/notebook](https://github.com/microsoft/autogen/tree/main/notebook)
- **Blog de Microsoft Research**: [https://www.microsoft.com/en-us/research/blog/autogen/](https://www.microsoft.com/en-us/research/blog/autogen/)
- **Comunidad y Soporte**:
  - Discord: [AutoGen Discord Server](https://discord.gg/autogen)
  - GitHub Discussions: [https://github.com/microsoft/autogen/discussions](https://github.com/microsoft/autogen/discussions)
  - Stack Overflow: Tag `autogen-microsoft`

## Conclusión

AutoGen continúa evolucionando como una plataforma robusta para crear sistemas multi-agente sofisticados. Las características clave incluyen:

1. **Flexibilidad**: Soporte para múltiples proveedores de LLM y modelos locales
2. **Escalabilidad**: Capacidad de manejar sistemas complejos con muchos agentes
3. **Seguridad**: Ejecución de código en entornos aislados
4. **Extensibilidad**: Fácil integración con herramientas externas
5. **Optimización**: Herramientas para gestionar costos y rendimiento

Para mantenerte actualizado:
- Sigue el repositorio de GitHub para notificaciones de nuevas versiones
- Únete a la comunidad en Discord
- Revisa regularmente la documentación oficial
- Experimenta con los notebooks de ejemplo

El framework AutoGen de Microsoft representa una herramienta poderosa para el desarrollo de aplicaciones de IA conversacional y sistemas multi-agente, con un futuro prometedor en la automatización inteligente de tareas complejas.