# Manual de Uso de LangGraph

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Conceptos Fundamentales](#conceptos-fundamentales)
4. [Primeros Pasos](#primeros-pasos)
5. [Creación de Grafos](#creación-de-grafos)
6. [Gestión de Estados](#gestión-de-estados)
7. [Nodos y Edges](#nodos-y-edges)
8. [Agentes y Herramientas](#agentes-y-herramientas)
9. [Flujos de Control](#flujos-de-control)
10. [Persistencia y Checkpoints](#persistencia-y-checkpoints)
11. [Debugging y Monitoreo](#debugging-y-monitoreo)
12. [Casos de Uso Avanzados](#casos-de-uso-avanzados)
13. [Mejores Prácticas](#mejores-prácticas)
14. [Recursos Adicionales](#recursos-adicionales)

## 1. Introducción

### ¿Qué es LangGraph?

LangGraph es un framework desarrollado por LangChain para construir aplicaciones con LLMs (Large Language Models) utilizando grafos de estados. Permite crear flujos de trabajo complejos, agentes autónomos y aplicaciones de IA conversacional con mayor control y flexibilidad que las cadenas tradicionales.

### Características Principales

- **Grafos de Estados**: Modelado de aplicaciones como máquinas de estado
- **Ciclos y Condicionales**: Soporte nativo para lógica compleja
- **Persistencia**: Capacidad de guardar y restaurar estados
- **Streaming**: Soporte para respuestas en tiempo real
- **Human-in-the-loop**: Integración de intervención humana
- **Paralelismo**: Ejecución concurrente de nodos

### ¿Cuándo usar LangGraph?

- Construcción de agentes complejos con múltiples herramientas
- Flujos de trabajo que requieren decisiones condicionales
- Aplicaciones que necesitan mantener estado entre interacciones
- Sistemas que requieren validación humana en puntos específicos
- Orquestación de múltiples LLMs o modelos

## 2. Instalación

### Requisitos Previos

```bash
# Python 3.9 o superior
python --version

# pip actualizado
pip install --upgrade pip
```

### Instalación Básica

```bash
# Instalar LangGraph
pip install langgraph

# Instalar con dependencias adicionales
pip install langgraph[all]

# Para desarrollo
pip install langgraph[dev]
```

### Dependencias Recomendadas

```bash
# LangChain y herramientas
pip install langchain langchain-openai langchain-community

# Para visualización
pip install matplotlib networkx

# Para persistencia
pip install redis sqlite3
```

### Configuración del Entorno

```python
# .env file
OPENAI_API_KEY=tu_clave_api
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=tu_clave_langchain
LANGCHAIN_PROJECT=mi_proyecto_langgraph
```

## 3. Conceptos Fundamentales

### Estado (State)

El estado es la información que se mantiene y modifica a lo largo de la ejecución del grafo.

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    current_step: str
    context: dict
```

### Nodos (Nodes)

Los nodos son funciones que procesan el estado y lo modifican.

```python
def process_input(state: AgentState) -> AgentState:
    # Lógica del nodo
    state["current_step"] = "processing"
    return state
```

### Edges (Aristas)

Las aristas definen las transiciones entre nodos.

```python
# Edge simple
graph.add_edge("inicio", "proceso")

# Edge condicional
graph.add_conditional_edges(
    "proceso",
    lambda state: "éxito" if state["valid"] else "error",
    {
        "éxito": "finalizar",
        "error": "reintentar"
    }
)
```

## 4. Primeros Pasos

### Ejemplo Básico: Hola Mundo

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

# Definir el estado
class State(TypedDict):
    mensaje: str
    contador: int

# Definir nodos
def saludar(state: State) -> State:
    state["mensaje"] = "¡Hola, LangGraph!"
    state["contador"] = state.get("contador", 0) + 1
    return state

def despedir(state: State) -> State:
    state["mensaje"] += " ¡Hasta luego!"
    return state

# Construir el grafo
workflow = StateGraph(State)

# Añadir nodos
workflow.add_node("saludo", saludar)
workflow.add_node("despedida", despedir)

# Definir el flujo
workflow.set_entry_point("saludo")
workflow.add_edge("saludo", "despedida")
workflow.add_edge("despedida", END)

# Compilar
app = workflow.compile()

# Ejecutar
result = app.invoke({"mensaje": "", "contador": 0})
print(result)
```

### Ejemplo con LLM

```python
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class ChatState(TypedDict):
    messages: List[str]
    response: str

def call_llm(state: ChatState) -> ChatState:
    llm = ChatOpenAI(model="gpt-4")
    response = llm.invoke(state["messages"][-1])
    state["response"] = response.content
    state["messages"].append(response.content)
    return state

# Crear grafo
workflow = StateGraph(ChatState)
workflow.add_node("llm", call_llm)
workflow.set_entry_point("llm")
workflow.add_edge("llm", END)

app = workflow.compile()

# Usar
result = app.invoke({
    "messages": ["¿Qué es LangGraph?"],
    "response": ""
})
```

## 5. Creación de Grafos

### StateGraph Detallado

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator

class GraphState(TypedDict):
    # Lista que se acumula con operator.add
    messages: Annotated[List[str], operator.add]
    # Valor que se sobrescribe
    current_task: str
    # Diccionario que se actualiza
    metadata: dict

# Crear grafo con estado tipado
workflow = StateGraph(GraphState)

# Configuración de visualización
workflow.set_debug(True)
```

### Grafos Multi-Agente

```python
class MultiAgentState(TypedDict):
    messages: List[str]
    next_agent: str
    agent_outputs: dict

def agent_coordinator(state: MultiAgentState) -> MultiAgentState:
    # Lógica para decidir qué agente ejecutar
    if "research" in state["messages"][-1]:
        state["next_agent"] = "researcher"
    elif "code" in state["messages"][-1]:
        state["next_agent"] = "coder"
    else:
        state["next_agent"] = "general"
    return state

def researcher_agent(state: MultiAgentState) -> MultiAgentState:
    # Lógica del agente investigador
    state["agent_outputs"]["research"] = "Resultados de investigación..."
    return state

def coder_agent(state: MultiAgentState) -> MultiAgentState:
    # Lógica del agente programador
    state["agent_outputs"]["code"] = "```python\n# Código generado\n```"
    return state

# Construir grafo multi-agente
workflow = StateGraph(MultiAgentState)

# Añadir nodos
workflow.add_node("coordinator", agent_coordinator)
workflow.add_node("researcher", researcher_agent)
workflow.add_node("coder", coder_agent)

# Configurar flujo
workflow.set_entry_point("coordinator")
workflow.add_conditional_edges(
    "coordinator",
    lambda x: x["next_agent"],
    {
        "researcher": "researcher",
        "coder": "coder",
        "general": END
    }
)

workflow.add_edge("researcher", END)
workflow.add_edge("coder", END)
```

## 6. Gestión de Estados

### Estados Complejos

```python
from typing import TypedDict, Optional, List, Dict, Any
from datetime import datetime

class AdvancedState(TypedDict):
    # Estado de conversación
    messages: List[Dict[str, str]]
    
    # Estado de contexto
    user_id: str
    session_id: str
    timestamp: datetime
    
    # Estado de proceso
    current_step: str
    steps_completed: List[str]
    errors: List[str]
    
    # Estado de datos
    extracted_data: Dict[str, Any]
    validation_results: Dict[str, bool]
    
    # Estado de configuración
    temperature: float
    max_retries: int
    current_retry: int

# Funciones auxiliares para gestión de estado
def initialize_state(user_id: str) -> AdvancedState:
    return {
        "messages": [],
        "user_id": user_id,
        "session_id": str(uuid.uuid4()),
        "timestamp": datetime.now(),
        "current_step": "inicio",
        "steps_completed": [],
        "errors": [],
        "extracted_data": {},
        "validation_results": {},
        "temperature": 0.7,
        "max_retries": 3,
        "current_retry": 0
    }

def update_step(state: AdvancedState, step: str) -> AdvancedState:
    state["steps_completed"].append(state["current_step"])
    state["current_step"] = step
    state["timestamp"] = datetime.now()
    return state
```

### Reducers Personalizados

```python
from langgraph.graph import add_messages

# Reducer personalizado para mensajes
def custom_message_reducer(existing: List, new: List) -> List:
    # Mantener solo los últimos 10 mensajes
    combined = existing + new
    return combined[-10:]

class StateWithReducer(TypedDict):
    messages: Annotated[List, custom_message_reducer]
    summary: str  # Se sobrescribe por defecto
    metrics: Annotated[Dict, lambda x, y: {**x, **y}]  # Merge de diccionarios
```

## 7. Nodos y Edges

### Tipos de Nodos

```python
# Nodo simple
def simple_node(state: State) -> State:
    # Procesar estado
    return state

# Nodo asíncrono
async def async_node(state: State) -> State:
    # Operaciones asíncronas
    await asyncio.sleep(1)
    return state

# Nodo con herramientas
def tool_node(state: State) -> State:
    from langchain.tools import DuckDuckGoSearchRun
    
    search = DuckDuckGoSearchRun()
    results = search.run(state["query"])
    state["search_results"] = results
    return state

# Nodo con validación
def validation_node(state: State) -> State:
    if not state.get("input"):
        state["errors"] = ["Input requerido"]
        state["valid"] = False
    else:
        state["valid"] = True
    return state
```

### Edges Condicionales Avanzados

```python
def routing_function(state: State) -> str:
    """Función de enrutamiento compleja"""
    if state.get("errors"):
        return "handle_error"
    
    if state["confidence"] > 0.8:
        return "high_confidence_path"
    elif state["confidence"] > 0.5:
        return "medium_confidence_path"
    else:
        return "low_confidence_path"

# Añadir edges condicionales con mapeo completo
workflow.add_conditional_edges(
    "process",
    routing_function,
    {
        "handle_error": "error_handler",
        "high_confidence_path": "execute",
        "medium_confidence_path": "review",
        "low_confidence_path": "human_review"
    }
)

# Edge con condición inline
workflow.add_conditional_edges(
    "validate",
    lambda x: "success" if x["valid"] else "retry",
    {
        "success": "process",
        "retry": "fix_errors"
    }
)
```

## 8. Agentes y Herramientas

### Agente con Herramientas

```python
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolExecutor, ToolInvocation

# Definir herramientas
def calculate(expression: str) -> str:
    """Calcula expresiones matemáticas"""
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error en el cálculo"

def search_web(query: str) -> str:
    """Busca información en la web"""
    # Implementación de búsqueda
    return f"Resultados para: {query}"

tools = [
    Tool(
        name="calculator",
        func=calculate,
        description="Útil para cálculos matemáticos"
    ),
    Tool(
        name="search",
        func=search_web,
        description="Busca información en internet"
    )
]

# Estado del agente
class AgentState(TypedDict):
    messages: List[str]
    current_tool: Optional[str]
    tool_output: Optional[str]
    final_answer: Optional[str]

# Nodo del agente
def agent_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4")
    
    # Bind tools al LLM
    llm_with_tools = llm.bind_tools(tools)
    
    response = llm_with_tools.invoke(state["messages"])
    
    # Verificar si se debe usar una herramienta
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        state["current_tool"] = tool_call["name"]
        state["tool_input"] = tool_call["args"]
    else:
        state["final_answer"] = response.content
    
    return state

# Nodo ejecutor de herramientas
def tool_executor_node(state: AgentState) -> AgentState:
    tool_name = state["current_tool"]
    tool_input = state["tool_input"]
    
    # Ejecutar herramienta
    for tool in tools:
        if tool.name == tool_name:
            result = tool.func(**tool_input)
            state["tool_output"] = result
            break
    
    return state
```

### Agente ReAct

```python
from langgraph.prebuilt import create_react_agent

# Crear agente ReAct
app = create_react_agent(
    model=ChatOpenAI(model="gpt-4"),
    tools=tools,
    state_schema=AgentState,
    debug=True
)

# Usar el agente
result = app.invoke({
    "messages": ["¿Cuánto es 25 * 4 + 10?"]
})
```

## 9. Flujos de Control

### Bucles y Ciclos

```python
class LoopState(TypedDict):
    counter: int
    max_iterations: int
    results: List[str]
    should_continue: bool

def process_iteration(state: LoopState) -> LoopState:
    # Procesar iteración
    state["counter"] += 1
    state["results"].append(f"Iteración {state['counter']}")
    
    # Verificar condición de salida
    if state["counter"] >= state["max_iterations"]:
        state["should_continue"] = False
    
    return state

def check_condition(state: LoopState) -> str:
    return "continue" if state["should_continue"] else "exit"

# Configurar bucle
workflow = StateGraph(LoopState)
workflow.add_node("process", process_iteration)
workflow.add_node("finalize", lambda x: x)

workflow.set_entry_point("process")
workflow.add_conditional_edges(
    "process",
    check_condition,
    {
        "continue": "process",  # Bucle
        "exit": "finalize"
    }
)
workflow.add_edge("finalize", END)
```

### Flujo Paralelo

```python
from langgraph.graph import StateGraph, END
from concurrent.futures import ThreadPoolExecutor

class ParallelState(TypedDict):
    input_data: List[str]
    results: Dict[str, Any]
    
def parallel_processor(state: ParallelState) -> ParallelState:
    def process_item(item: str) -> tuple:
        # Procesar cada item
        result = f"Procesado: {item}"
        return item, result
    
    # Ejecutar en paralelo
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_item, item) 
                  for item in state["input_data"]]
        
        for future in futures:
            key, value = future.result()
            state["results"][key] = value
    
    return state

# Configurar grafo con procesamiento paralelo
workflow = StateGraph(ParallelState)
workflow.add_node("parallel_process", parallel_processor)
workflow.set_entry_point("parallel_process")
workflow.add_edge("parallel_process", END)
```

### Subgrafos

```python
def create_subgraph() -> StateGraph:
    """Crear un subgrafo reutilizable"""
    subgraph = StateGraph(dict)
    
    def sub_process(state: dict) -> dict:
        state["processed"] = True
        return state
    
    subgraph.add_node("subprocess", sub_process)
    subgraph.set_entry_point("subprocess")
    subgraph.add_edge("subprocess", END)
    
    return subgraph

# Grafo principal
main_workflow = StateGraph(dict)

# Compilar subgrafo
subgraph_app = create_subgraph().compile()

def call_subgraph(state: dict) -> dict:
    # Llamar al subgrafo
    result = subgraph_app.invoke(state)
    return result

main_workflow.add_node("main_process", lambda x: x)
main_workflow.add_node("subgraph", call_subgraph)

main_workflow.set_entry_point("main_process")
main_workflow.add_edge("main_process", "subgraph")
main_workflow.add_edge("subgraph", END)
```

## 10. Persistencia y Checkpoints

### Checkpointer en Memoria

```python
from langgraph.checkpoint import MemorySaver

# Crear checkpointer
checkpointer = MemorySaver()

# Compilar con checkpointer
app = workflow.compile(checkpointer=checkpointer)

# Ejecutar con thread_id para mantener estado
config = {"configurable": {"thread_id": "thread-123"}}

# Primera ejecución
result1 = app.invoke({"message": "Hola"}, config)

# Segunda ejecución - mantiene el estado
result2 = app.invoke({"message": "¿Cómo estás?"}, config)
```

### Checkpointer con SQLite

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Configurar SQLite checkpointer
with SqliteSaver.from_conn_string(":memory:") as checkpointer:
    app = workflow.compile(checkpointer=checkpointer)
    
    # Usar la aplicación con persistencia
    thread_id = "persistent-thread-1"
    config = {"configurable": {"thread_id": thread_id}}
    
    # Ejecutar
    result = app.invoke(initial_state, config)
    
    # Obtener historial
    history = list(app.get_state_history(config))
    
    # Restaurar desde checkpoint
    state = app.get_state(config)
```

### Checkpointer Personalizado

```python
from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint
import json

class CustomCheckpointer(BaseCheckpointSaver):
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        
    def put(self, config: dict, checkpoint: Checkpoint) -> None:
        """Guardar checkpoint"""
        thread_id = config["configurable"]["thread_id"]
        file_path = f"{self.storage_path}/{thread_id}.json"
        
        with open(file_path, 'w') as f:
            json.dump(checkpoint, f)
    
    def get(self, config: dict) -> Optional[Checkpoint]:
        """Recuperar checkpoint"""
        thread_id = config["configurable"]["thread_id"]
        file_path = f"{self.storage_path}/{thread_id}.json"
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def list(self, config: dict) -> List[Checkpoint]:
        """Listar checkpoints"""
        # Implementar listado
        pass
```

## 11. Debugging y Monitoreo

### Debug Mode

```python
# Activar modo debug
app = workflow.compile(debug=True)

# O configurar por entorno
import os
os.environ["LANGGRAPH_DEBUG"] = "true"

# Debug con callbacks
from langchain.callbacks import StdOutCallbackHandler

app.invoke(
    initial_state,
    config={"callbacks": [StdOutCallbackHandler()]}
)
```

### Visualización de Grafos

```python
from IPython.display import Image, display

# Generar visualización
try:
    display(Image(app.get_graph().draw_mermaid_png()))
except Exception:
    # Fallback a representación de texto
    print(app.get_graph().draw_ascii())

# Exportar a archivo
with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())
```

### Logging Estructurado

```python
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("langgraph")

def logged_node(state: State) -> State:
    """Nodo con logging"""
    logger.info(f"Entrando al nodo: {state.get('current_step')}")
    
    try:
        # Procesar
        state["processed"] = True
        logger.info("Procesamiento exitoso")
    except Exception as e:
        logger.error(f"Error en procesamiento: {e}")
        state["error"] = str(e)
    
    return state

# Métricas personalizadas
class MetricsCollector:
    def __init__(self):
        self.metrics = {
            "node_executions": {},
            "execution_times": {},
            "errors": []
        }
    
    def record_execution(self, node_name: str, duration: float):
        if node_name not in self.metrics["node_executions"]:
            self.metrics["node_executions"][node_name] = 0
        self.metrics["node_executions"][node_name] += 1
        
        if node_name not in self.metrics["execution_times"]:
            self.metrics["execution_times"][node_name] = []
        self.metrics["execution_times"][node_name].append(duration)
    
    def record_error(self, node_name: str, error: Exception):
        self.metrics["errors"].append({
            "node": node_name,
            "error": str(error),
            "timestamp": datetime.now().isoformat()
        })
```

### Tracing con LangSmith

```python
# Configurar LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "tu-api-key"
os.environ["LANGCHAIN_PROJECT"] = "langgraph-manual"

# El tracing se activa automáticamente
result = app.invoke(initial_state)

# Agregar metadata personalizada
result = app.invoke(
    initial_state,
    config={
        "metadata": {
            "user_id": "user-123",
            "session_id": "session-456",
            "experiment": "v2"
        }
    }
)
```

## 12. Casos de Uso Avanzados

### Chat con Memoria y Herramientas

```python
from typing import TypedDict, Annotated, List
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langgraph.graph import StateGraph, END
import operator

class ChatState(TypedDict):
    messages: Annotated[List[dict], operator.add]
    summary: str
    current_tool: Optional[str]
    tool_result: Optional[str]

class AdvancedChatbot:
    def __init__(self, model="gpt-4"):
        self.llm = ChatOpenAI(model=model)
        self.memory = ConversationSummaryMemory(llm=self.llm)
        self.tools = self._setup_tools()
        self.workflow = self._build_workflow()
        
    def _setup_tools(self):
        return [
            Tool(name="weather", func=self.get_weather, 
                 description="Get weather information"),
            Tool(name="calendar", func=self.check_calendar,
                 description="Check calendar events")
        ]
    
    def _build_workflow(self):
        workflow = StateGraph(ChatState)
        
        # Nodos
        workflow.add_node("process_message", self.process_message)
        workflow.add_node("use_tool", self.use_tool)
        workflow.add_node("generate_response", self.generate_response)
        workflow.add_node("update_memory", self.update_memory)
        
        # Flujo
        workflow.set_entry_point("process_message")
        workflow.add_conditional_edges(
            "process_message",
            self.should_use_tool,
            {
                "tool": "use_tool",
                "respond": "generate_response"
            }
        )
        workflow.add_edge("use_tool", "generate_response")
        workflow.add_edge("generate_response", "update_memory")
        workflow.add_edge("update_memory", END)
        
        return workflow.compile()
    
    def process_message(self, state: ChatState) -> ChatState:
        # Analizar mensaje y determinar intención
        last_message = state["messages"][-1]
        
        # Agregar contexto de memoria
        if state.get("summary"):
            context = f"Resumen previo: {state['summary']}\n"
            state["messages"][-1]["content"] = context + last_message["content"]
        
        return state
    
    def should_use_tool(self, state: ChatState) -> str:
        # Lógica para determinar si usar herramienta
        message_content = state["messages"][-1]["content"].lower()
        
        if "weather" in message_content or "clima" in message_content:
            state["current_tool"] = "weather"
            return "tool"
        elif "calendar" in message_content or "calendario" in message_content:
            state["current_tool"] = "calendar"
            return "tool"
        
        return "respond"
    
    def use_tool(self, state: ChatState) -> ChatState:
        tool_name = state["current_tool"]
        
        # Ejecutar herramienta correspondiente
        for tool in self.tools:
            if tool.name == tool_name:
                result = tool.func()
                state["tool_result"] = result
                break
        
        return state
    
    def generate_response(self, state: ChatState) -> ChatState:
        # Generar respuesta con o sin resultado de herramienta
        if state.get("tool_result"):
            prompt = f"Basándote en este resultado: {state['tool_result']}, responde al usuario."
        else:
            prompt = "Responde al usuario de manera útil y amigable."
        
        messages = state["messages"] + [{"role": "system", "content": prompt}]
        response = self.llm.invoke(messages)
        
        state["messages"].append({
            "role": "assistant",
            "content": response.content
        })
        
        return state
    
    def update_memory(self, state: ChatState) -> ChatState:
        # Actualizar memoria con la conversación
        conversation = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in state["messages"][-4:]  # Últimos 4 mensajes
        ])
        
        state["summary"] = self.memory.predict_new_summary(
            state.get("summary", ""),
            conversation
        )
        
        return state
    
    def get_weather(self) -> str:
        # Simulación de API del clima
        return "El clima está soleado, 25°C"
    
    def check_calendar(self) -> str:
        # Simulación de calendario
        return "Tienes una reunión a las 3 PM"
    
    def chat(self, message: str, thread_id: str):
        config = {"configurable": {"thread_id": thread_id}}
        
        result = self.workflow.invoke({
            "messages": [{"role": "user", "content": message}]
        }, config)
        
        return result["messages"][-1]["content"]

# Usar el chatbot
chatbot = AdvancedChatbot()
response = chatbot.chat("¿Cómo está el clima?", "user-123")
```

### Sistema de RAG (Retrieval-Augmented Generation)

```python
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RAGSystem:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.workflow = self._build_workflow()
    
    def _build_workflow(self):
        workflow = StateGraph(dict)
        
        workflow.add_node("retrieve", self.retrieve_documents)
        workflow.add_node("rerank", self.rerank_documents)
        workflow.add_node("generate", self.generate_answer)
        workflow.add_node("validate", self.validate_answer)
        
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "rerank")
        workflow.add_edge("rerank", "generate")
        workflow.add_conditional_edges(
            "generate",
            lambda x: "valid" if x["confidence"] > 0.7 else "invalid",
            {
                "valid": END,
                "invalid": "retrieve"  # Reintentar con query diferente
            }
        )
        
        return workflow.compile()
    
    def index_documents(self, documents: List[str]):
        """Indexar documentos en el vectorstore"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        chunks = []
        for doc in documents:
            chunks.extend(text_splitter.split_text(doc))
        
        self.vectorstore = FAISS.from_texts(chunks, self.embeddings)
    
    def retrieve_documents(self, state: dict) -> dict:
        query = state["query"]
        
        # Recuperar documentos relevantes
        docs = self.vectorstore.similarity_search(
            query, 
            k=state.get("k", 5)
        )
        
        state["retrieved_docs"] = [doc.page_content for doc in docs]
        return state
    
    def rerank_documents(self, state: dict) -> dict:
        # Implementar reranking (ej: con cross-encoder)
        # Por ahora, mantener el orden original
        state["reranked_docs"] = state["retrieved_docs"][:3]
        return state
    
    def generate_answer(self, state: dict) -> dict:
        llm = ChatOpenAI(model="gpt-4")
        
        context = "\n\n".join(state["reranked_docs"])
        prompt = f"""Basándote en el siguiente contexto, responde la pregunta.
        
Contexto:
{context}

Pregunta: {state["query"]}

Respuesta:"""
        
        response = llm.invoke(prompt)
        state["answer"] = response.content
        
        # Calcular confianza (simplificado)
        state["confidence"] = 0.8 if len(state["reranked_docs"]) > 2 else 0.5
        
        return state
    
    def validate_answer(self, state: dict) -> dict:
        # Validación adicional de la respuesta
        if "no sé" in state["answer"].lower():
            state["confidence"] *= 0.5
        
        return state

# Usar el sistema RAG
rag = RAGSystem()
rag.index_documents([
    "LangGraph es un framework para construir aplicaciones con LLMs usando grafos.",
    "Los grafos en LangGraph permiten crear flujos de trabajo complejos.",
    "LangGraph soporta persistencia de estado mediante checkpointers."
])

result = rag.workflow.invoke({
    "query": "¿Qué es LangGraph?",
    "k": 3
})
```

### Pipeline de Procesamiento de Datos

```python
class DataPipeline:
    def __init__(self):
        self.workflow = self._build_pipeline()
    
    def _build_pipeline(self):
        workflow = StateGraph(dict)
        
        # Nodos de procesamiento
        workflow.add_node("validate_input", self.validate_input)
        workflow.add_node("clean_data", self.clean_data)
        workflow.add_node("extract_entities", self.extract_entities)
        workflow.add_node("enrich_data", self.enrich_data)
        workflow.add_node("store_results", self.store_results)
        workflow.add_node("handle_error", self.handle_error)
        
        # Flujo principal
        workflow.set_entry_point("validate_input")
        
        workflow.add_conditional_edges(
            "validate_input",
            lambda x: "valid" if x["is_valid"] else "invalid",
            {
                "valid": "clean_data",
                "invalid": "handle_error"
            }
        )
        
        workflow.add_edge("clean_data", "extract_entities")
        workflow.add_edge("extract_entities", "enrich_data")
        workflow.add_edge("enrich_data", "store_results")
        workflow.add_edge("store_results", END)
        workflow.add_edge("handle_error", END)
        
        return workflow.compile(debug=True)
    
    def validate_input(self, state: dict) -> dict:
        data = state.get("input_data")
        
        # Validaciones
        if not data:
            state["is_valid"] = False
            state["error"] = "No input data provided"
        elif not isinstance(data, (dict, list)):
            state["is_valid"] = False
            state["error"] = "Invalid data format"
        else:
            state["is_valid"] = True
        
        return state
    
    def clean_data(self, state: dict) -> dict:
        # Limpieza de datos
        data = state["input_data"]
        
        if isinstance(data, dict):
            # Eliminar campos vacíos
            cleaned = {k: v for k, v in data.items() if v}
        else:
            cleaned = data
        
        state["cleaned_data"] = cleaned
        return state
    
    def extract_entities(self, state: dict) -> dict:
        # Extracción de entidades con NER
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-4")
        
        prompt = f"""Extract all named entities from this data:
        {state['cleaned_data']}
        
        Return as JSON with categories: persons, organizations, locations"""
        
        response = llm.invoke(prompt)
        state["entities"] = response.content
        
        return state
    
    def enrich_data(self, state: dict) -> dict:
        # Enriquecer datos con información adicional
        enriched = {
            "original": state["cleaned_data"],
            "entities": state["entities"],
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "pipeline_version": "1.0"
            }
        }
        
        state["enriched_data"] = enriched
        return state
    
    def store_results(self, state: dict) -> dict:
        # Simular almacenamiento
        print(f"Storing results: {state['enriched_data']}")
        state["stored"] = True
        return state
    
    def handle_error(self, state: dict) -> dict:
        print(f"Error: {state.get('error', 'Unknown error')}")
        state["handled"] = True
        return state

# Usar el pipeline
pipeline = DataPipeline()

result = pipeline.workflow.invoke({
    "input_data": {
        "text": "Apple Inc. fue fundada por Steve Jobs en Cupertino.",
        "date": "2024-01-01"
    }
})
```

## 13. Mejores Prácticas

### 1. Diseño de Estados

```python
# ❌ Evitar estados monolíticos
class BadState(TypedDict):
    everything: dict  # Demasiado genérico

# ✅ Estados bien estructurados
class GoodState(TypedDict):
    # Agrupación lógica
    conversation: ConversationState
    user_context: UserContext
    processing: ProcessingState
    
class ConversationState(TypedDict):
    messages: List[Message]
    turn_count: int
    language: str

class UserContext(TypedDict):
    user_id: str
    preferences: dict
    history: List[str]

class ProcessingState(TypedDict):
    current_step: str
    errors: List[str]
    metadata: dict
```

### 2. Manejo de Errores

```python
from typing import Optional, Union

def safe_node(state: State) -> State:
    """Nodo con manejo robusto de errores"""
    try:
        # Operación principal
        result = process_data(state["data"])
        state["result"] = result
        state["status"] = "success"
    
    except ValidationError as e:
        # Error esperado
        state["status"] = "validation_error"
        state["error"] = str(e)
        state["should_retry"] = True
    
    except Exception as e:
        # Error inesperado
        state["status"] = "error"
        state["error"] = f"Unexpected error: {str(e)}"
        state["should_retry"] = False
        
        # Log para debugging
        import traceback
        state["error_trace"] = traceback.format_exc()
    
    finally:
        # Limpieza
        state["processed_at"] = datetime.now().isoformat()
    
    return state

# Nodo de recuperación
def error_recovery_node(state: State) -> State:
    if state.get("should_retry") and state.get("retry_count", 0) < 3:
        state["retry_count"] = state.get("retry_count", 0) + 1
        # Reset para reintentar
        state["status"] = "retrying"
        del state["error"]
    else:
        state["status"] = "failed"
    
    return state
```

### 3. Testing

```python
import pytest
from unittest.mock import Mock, patch

class TestWorkflow:
    def test_simple_workflow(self):
        """Test básico del workflow"""
        # Crear workflow de prueba
        workflow = create_test_workflow()
        app = workflow.compile()
        
        # Estado inicial
        initial_state = {
            "input": "test",
            "processed": False
        }
        
        # Ejecutar
        result = app.invoke(initial_state)
        
        # Verificar
        assert result["processed"] == True
        assert "output" in result
    
    def test_conditional_routing(self):
        """Test de enrutamiento condicional"""
        workflow = create_workflow_with_conditions()
        app = workflow.compile()
        
        # Test ruta exitosa
        result = app.invoke({"value": 10})
        assert result["path"] == "success"
        
        # Test ruta de error
        result = app.invoke({"value": -1})
        assert result["path"] == "error"
    
    @patch('langchain_openai.ChatOpenAI')
    def test_llm_node(self, mock_llm):
        """Test de nodo con LLM"""
        # Configurar mock
        mock_llm.return_value.invoke.return_value.content = "Respuesta de prueba"
        
        # Ejecutar nodo
        state = llm_node({"query": "test"})
        
        # Verificar
        assert state["response"] == "Respuesta de prueba"
        mock_llm.return_value.invoke.assert_called_once()

# Fixtures para testing
@pytest.fixture
def sample_state():
    return {
        "messages": [],
        "user_id": "test-user",
        "timestamp": datetime.now()
    }

@pytest.fixture
def compiled_app():
    workflow = create_main_workflow()
    return workflow.compile()
```

### 4. Optimización de Rendimiento

```python
# Uso eficiente de memoria
class OptimizedState(TypedDict):
    # Usar generadores para datos grandes
    data_iterator: Iterator[str]
    # Limitar tamaño de historial
    recent_messages: Annotated[List[str], lambda x, y: (x + y)[-10:]]
    # Comprimir datos grandes
    compressed_data: bytes

# Procesamiento asíncrono
async def async_optimized_node(state: State) -> State:
    # Operaciones I/O concurrentes
    tasks = [
        fetch_data(url) for url in state["urls"]
    ]
    
    results = await asyncio.gather(*tasks)
    state["results"] = results
    
    return state

# Caching de resultados
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_operation(input_data: str) -> str:
    # Operación costosa
    return process(input_data)

def cached_node(state: State) -> State:
    # Usar cache para operaciones repetidas
    state["result"] = expensive_operation(state["input"])
    return state
```

### 5. Configuración y Despliegue

```python
# Configuración por entorno
from pydantic import BaseSettings

class Settings(BaseSettings):
    # API Keys
    openai_api_key: str
    langchain_api_key: Optional[str]
    
    # Configuración de LangGraph
    langgraph_debug: bool = False
    checkpoint_backend: str = "memory"  # memory, sqlite, redis
    
    # Configuración de aplicación
    max_retries: int = 3
    timeout_seconds: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()

# Factory para crear aplicaciones
def create_app(config: Settings) -> CompiledGraph:
    # Configurar checkpointer según backend
    if config.checkpoint_backend == "sqlite":
        checkpointer = SqliteSaver.from_conn_string("app.db")
    elif config.checkpoint_backend == "redis":
        checkpointer = RedisSaver(redis_client)
    else:
        checkpointer = MemorySaver()
    
    # Crear workflow
    workflow = create_main_workflow()
    
    # Compilar con configuración
    return workflow.compile(
        checkpointer=checkpointer,
        debug=config.langgraph_debug
    )

# Despliegue con FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
langgraph_app = create_app(settings)

class ChatRequest(BaseModel):
    message: str
    thread_id: str

class ChatResponse(BaseModel):
    response: str
    thread_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        
        result = await langgraph_app.ainvoke(
            {"messages": [{"role": "user", "content": request.message}]},
            config
        )
        
        return ChatResponse(
            response=result["messages"][-1]["content"],
            thread_id=request.thread_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "langgraph-app"}
```

## 14. Recursos Adicionales

### Documentación Oficial
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [API Reference](https://api.python.langchain.com/en/latest/langgraph_api_reference.html)

### Tutoriales y Guías
- [LangGraph Tutorials](https://github.com/langchain-ai/langgraph/tree/main/examples)
- [Building Agents with LangGraph](https://python.langchain.com/docs/langgraph/tutorials)
- [LangGraph Academy](https://academy.langchain.com/courses/intro-to-langgraph)

### Comunidad
- [LangChain Discord](https://discord.gg/langchain)
- [GitHub Discussions](https://github.com/langchain-ai/langgraph/discussions)
- [LangChain Blog](https://blog.langchain.dev/)

### Ejemplos de Código
- [Oficial Examples Repository](https://github.com/langchain-ai/langgraph/tree/main/examples)
- [Community Templates](https://github.com/langchain-ai/langchain/tree/master/templates)

### Videos y Cursos
- [LangGraph YouTube Tutorials](https://www.youtube.com/@LangChain)
- [Build Production-Ready AI Applications](https://www.deeplearning.ai/short-courses/building-agentic-ai-with-langgraph/)

### Herramientas Complementarias
- [LangSmith](https://smith.langchain.com/) - Para debugging y monitoreo
- [LangServe](https://github.com/langchain-ai/langserve) - Para despliegue de APIs
- [LangChain Hub](https://smith.langchain.com/hub) - Prompts y componentes compartidos

---

Este manual cubre los aspectos fundamentales y avanzados de LangGraph. Para mantenerlo actualizado, consulta regularmente la documentación oficial y participa en la comunidad para conocer las últimas actualizaciones y mejores prácticas.