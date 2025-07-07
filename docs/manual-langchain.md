# Manual de Uso de LangChain

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Conceptos Fundamentales](#conceptos-fundamentales)
4. [Componentes Principales](#componentes-principales)
5. [Modelos de Lenguaje](#modelos-de-lenguaje)
6. [Prompts](#prompts)
7. [Chains (Cadenas)](#chains-cadenas)
8. [Agents (Agentes)](#agents-agentes)
9. [Memory (Memoria)](#memory-memoria)
10. [Document Loaders](#document-loaders)
11. [Vector Stores](#vector-stores)
12. [Ejemplos Prácticos](#ejemplos-prácticos)
13. [Mejores Prácticas](#mejores-prácticas)
14. [Recursos Adicionales](#recursos-adicionales)

## Introducción

LangChain es un framework de código abierto diseñado para facilitar el desarrollo de aplicaciones potenciadas por modelos de lenguaje grandes (LLMs). Proporciona una arquitectura modular que permite a los desarrolladores construir aplicaciones complejas de IA de manera eficiente.

### ¿Qué es LangChain?

LangChain es una biblioteca que simplifica la creación de aplicaciones con LLMs mediante:
- Composición de cadenas de procesamiento
- Gestión de prompts
- Integración con múltiples modelos de IA
- Manejo de memoria y contexto
- Creación de agentes autónomos

### Ventajas principales

1. **Modularidad**: Componentes reutilizables y combinables
2. **Flexibilidad**: Compatible con múltiples proveedores de LLM
3. **Abstracciones potentes**: Simplifica tareas complejas
4. **Comunidad activa**: Amplio ecosistema y soporte

## Instalación

### Python

```bash
# Instalación básica
pip install langchain

# Con todas las dependencias
pip install langchain[all]

# Instalación específica para OpenAI
pip install langchain openai

# Para usar embeddings y vectores
pip install langchain chromadb tiktoken

# Instalación de LangChain Community
pip install langchain-community
```

### JavaScript/TypeScript

```bash
# Instalación con npm
npm install langchain

# Instalación con yarn
yarn add langchain

# Para TypeScript
npm install @types/node
```

### Configuración del entorno

```python
# Configurar variables de entorno
import os
from dotenv import load_dotenv

load_dotenv()

# Configurar API keys
os.environ["OPENAI_API_KEY"] = "tu-api-key"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "tu-langchain-api-key"
```

## Conceptos Fundamentales

### 1. LLMs (Large Language Models)
Modelos de lenguaje que procesan y generan texto.

### 2. Chains
Secuencias de llamadas a LLMs u otras utilidades.

### 3. Agents
Sistemas que usan LLMs para decidir qué acciones tomar.

### 4. Memory
Capacidad de mantener información entre interacciones.

### 5. Indexes
Formas de estructurar documentos para interactuar con LLMs.

## Componentes Principales

### Arquitectura de LangChain

```
┌─────────────────────────────────────────┐
│            Aplicación LangChain         │
├─────────────────────────────────────────┤
│  Agents  │  Chains  │  Memory  │ Tools │
├─────────────────────────────────────────┤
│    Prompts    │    Models    │  Data   │
├─────────────────────────────────────────┤
│          LangChain Core API             │
└─────────────────────────────────────────┘
```

## Modelos de Lenguaje

### Configuración de OpenAI

```python
from langchain_openai import ChatOpenAI

# Inicializar modelo
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    max_tokens=1000
)

# Uso básico
response = llm.invoke("¿Qué es LangChain?")
print(response.content)
```

### Configuración de otros modelos

```python
# Anthropic Claude
from langchain_anthropic import ChatAnthropic
claude = ChatAnthropic(model="claude-3-sonnet-20240229")

# Google Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
gemini = ChatGoogleGenerativeAI(model="gemini-pro")

# Modelos locales con Ollama
from langchain_community.llms import Ollama
ollama = Ollama(model="llama2")
```

## Prompts

### Templates de Prompts

```python
from langchain.prompts import PromptTemplate

# Template simple
template = """
Eres un asistente útil. Responde la siguiente pregunta:
{question}
"""

prompt = PromptTemplate(
    input_variables=["question"],
    template=template
)

# Uso del prompt
formatted_prompt = prompt.format(question="¿Cómo funciona LangChain?")
```

### Chat Prompt Templates

```python
from langchain.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente especializado en {topic}"),
    ("human", "{user_input}")
])

messages = chat_template.format_messages(
    topic="programación",
    user_input="Explica qué es una función recursiva"
)
```

### Few-shot Prompts

```python
from langchain.prompts import FewShotPromptTemplate

examples = [
    {"input": "feliz", "output": "triste"},
    {"input": "alto", "output": "bajo"},
]

example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Da el antónimo de cada input:",
    suffix="Input: {input}\nOutput:",
    input_variables=["input"]
)
```

## Chains (Cadenas)

### Chain Simple

```python
from langchain.chains import LLMChain

# Crear una chain básica
chain = LLMChain(llm=llm, prompt=prompt)

# Ejecutar la chain
result = chain.run(question="¿Qué es Python?")
```

### Sequential Chain

```python
from langchain.chains import SimpleSequentialChain

# Primera chain
first_prompt = PromptTemplate(
    input_variables=["product"],
    template="¿Cuál es el mejor nombre para una empresa que hace {product}?"
)
chain_one = LLMChain(llm=llm, prompt=first_prompt)

# Segunda chain
second_prompt = PromptTemplate(
    input_variables=["company_name"],
    template="Escribe un eslogan para la empresa: {company_name}"
)
chain_two = LLMChain(llm=llm, prompt=second_prompt)

# Chain secuencial
overall_chain = SimpleSequentialChain(
    chains=[chain_one, chain_two],
    verbose=True
)

result = overall_chain.run("zapatos ecológicos")
```

### Router Chain

```python
from langchain.chains.router import MultiPromptChain

physics_template = """Eres un profesor de física.
Pregunta: {input}"""

math_template = """Eres un profesor de matemáticas.
Pregunta: {input}"""

prompt_infos = [
    {
        "name": "physics",
        "description": "Para preguntas de física",
        "prompt_template": physics_template
    },
    {
        "name": "math",
        "description": "Para preguntas de matemáticas",
        "prompt_template": math_template
    }
]

destination_chains = {}
for p_info in prompt_infos:
    name = p_info["name"]
    prompt_template = p_info["prompt_template"]
    prompt = PromptTemplate(template=prompt_template, input_variables=["input"])
    chain = LLMChain(llm=llm, prompt=prompt)
    destination_chains[name] = chain

router_chain = MultiPromptChain(
    destination_chains=destination_chains,
    default_chain=destination_chains["physics"]
)
```

## Agents (Agentes)

### Agente con Herramientas

```python
from langchain.agents import create_react_agent, Tool
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import AgentExecutor

# Definir herramientas
search = DuckDuckGoSearchRun()

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Útil para buscar información actual en internet"
    )
]

# Crear agente
from langchain import hub
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# Ejecutar agente
result = agent_executor.invoke({
    "input": "¿Cuál es el clima actual en Madrid?"
})
```

### Agente con Funciones Personalizadas

```python
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool

@tool
def calculate(expression: str) -> str:
    """Calcula expresiones matemáticas."""
    try:
        result = eval(expression)
        return f"El resultado es: {result}"
    except:
        return "Error en el cálculo"

@tool
def get_word_length(word: str) -> str:
    """Obtiene la longitud de una palabra."""
    return f"La palabra '{word}' tiene {len(word)} caracteres"

tools = [calculate, get_word_length]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

result = agent.run("¿Cuánto es 25 * 4 y cuántas letras tiene la palabra 'LangChain'?")
```

## Memory (Memoria)

### Memoria de Conversación

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Memoria simple
memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Mantiene el contexto entre llamadas
conversation.predict(input="Hola, mi nombre es Carlos")
conversation.predict(input="¿Cuál es mi nombre?")
```

### Memoria con Resumen

```python
from langchain.memory import ConversationSummaryMemory

memory = ConversationSummaryMemory(llm=llm)

conversation_with_summary = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)
```

### Memoria con Ventana

```python
from langchain.memory import ConversationBufferWindowMemory

# Solo recuerda las últimas k interacciones
memory = ConversationBufferWindowMemory(k=2)

conversation = ConversationChain(
    llm=llm,
    memory=memory
)
```

### Memoria Vectorial

```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(embedding_function=embeddings)

retriever = vectorstore.as_retriever(search_kwargs=dict(k=1))
memory = VectorStoreRetrieverMemory(retriever=retriever)
```

## Document Loaders

### Carga de Documentos

```python
# PDF
from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("documento.pdf")
pages = loader.load()

# Texto
from langchain.document_loaders import TextLoader
loader = TextLoader("archivo.txt")
docs = loader.load()

# CSV
from langchain.document_loaders import CSVLoader
loader = CSVLoader("datos.csv")
data = loader.load()

# Web
from langchain.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://example.com")
data = loader.load()
```

### División de Texto

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

documents = text_splitter.split_documents(pages)
```

## Vector Stores

### Configuración de ChromaDB

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Crear embeddings
embeddings = OpenAIEmbeddings()

# Crear vector store
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# Búsqueda
query = "¿Qué dice sobre inteligencia artificial?"
docs = vectorstore.similarity_search(query, k=3)
```

### Retrieval QA

```python
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

result = qa_chain.run("¿Cuál es el tema principal del documento?")
```

## Ejemplos Prácticos

### 1. Chatbot Simple

```python
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(temperature=0.9)

def chatbot():
    print("Chatbot iniciado. Escribe 'salir' para terminar.")
    
    messages = [
        SystemMessage(content="Eres un asistente amigable y útil.")
    ]
    
    while True:
        user_input = input("\nUsuario: ")
        if user_input.lower() == 'salir':
            break
            
        messages.append(HumanMessage(content=user_input))
        response = chat(messages)
        messages.append(response)
        
        print(f"Bot: {response.content}")

chatbot()
```

### 2. Analizador de Documentos

```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

def analyze_pdf(pdf_path):
    # Cargar PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    # Dividir texto
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0
    )
    texts = text_splitter.split_documents(documents)
    
    # Crear embeddings y vectorstore
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_documents(texts, embeddings)
    
    # Crear chain de QA
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(),
        chain_type="stuff",
        retriever=docsearch.as_retriever()
    )
    
    return qa

# Uso
qa_system = analyze_pdf("documento.pdf")
answer = qa_system.run("¿De qué trata este documento?")
print(answer)
```

### 3. Agente de Investigación

```python
from langchain.agents import initialize_agent, Tool
from langchain.tools import DuckDuckGoSearchRun
from langchain.utilities import WikipediaAPIWrapper

search = DuckDuckGoSearchRun()
wikipedia = WikipediaAPIWrapper()

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Buscar información actual en internet"
    ),
    Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="Buscar información en Wikipedia"
    )
]

research_agent = initialize_agent(
    tools,
    ChatOpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

result = research_agent.run(
    "Investiga sobre los últimos avances en computación cuántica"
)
```

### 4. Sistema RAG (Retrieval-Augmented Generation)

```python
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA

# Cargar documentos de un directorio
loader = DirectoryLoader('./docs', glob="**/*.txt")

# Crear índice
index = VectorstoreIndexCreator().from_loaders([loader])

# Sistema de preguntas y respuestas
def rag_system(query):
    return index.query(query, llm=ChatOpenAI())

# Uso
answer = rag_system("¿Qué información hay sobre machine learning?")
print(answer)
```

### 5. Pipeline de Procesamiento de Datos

```python
from langchain.chains import TransformChain, SequentialChain

def transform_func(inputs: dict) -> dict:
    text = inputs["text"]
    # Procesar texto
    return {"processed_text": text.upper()}

transform_chain = TransformChain(
    input_variables=["text"],
    output_variables=["processed_text"],
    transform=transform_func
)

# Chain de análisis
analysis_prompt = PromptTemplate(
    input_variables=["processed_text"],
    template="Analiza el siguiente texto: {processed_text}"
)

analysis_chain = LLMChain(
    llm=llm,
    prompt=analysis_prompt,
    output_key="analysis"
)

# Pipeline completo
pipeline = SequentialChain(
    chains=[transform_chain, analysis_chain],
    input_variables=["text"],
    output_variables=["processed_text", "analysis"]
)

result = pipeline({"text": "LangChain es un framework poderoso"})
```

## Mejores Prácticas

### 1. Gestión de Costos

```python
# Usar callbacks para monitorear tokens
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = llm.invoke("Test")
    print(f"Tokens usados: {cb.total_tokens}")
    print(f"Costo: ${cb.total_cost}")
```

### 2. Manejo de Errores

```python
from langchain.callbacks import StdOutCallbackHandler
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def robust_llm_call(prompt):
    try:
        return llm.invoke(prompt)
    except Exception as e:
        print(f"Error: {e}")
        raise
```

### 3. Logging y Debugging

```python
import logging
from langchain.globals import set_debug

# Activar modo debug
set_debug(True)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Usar callbacks personalizados
class CustomHandler(StdOutCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        logger.info(f"LLM iniciado con prompt: {prompts}")
    
    def on_llm_end(self, response, **kwargs):
        logger.info(f"LLM finalizado: {response}")

llm = ChatOpenAI(callbacks=[CustomHandler()])
```

### 4. Optimización de Prompts

```python
# Usar OutputParser para estructurar respuestas
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class ResponseModel(BaseModel):
    summary: str = Field(description="resumen del texto")
    sentiment: str = Field(description="sentimiento: positivo, negativo o neutro")
    keywords: list[str] = Field(description="palabras clave")

parser = PydanticOutputParser(pydantic_object=ResponseModel)

prompt = PromptTemplate(
    template="Analiza el siguiente texto:\n{text}\n{format_instructions}",
    input_variables=["text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain = LLMChain(llm=llm, prompt=prompt)
output = chain.run(text="LangChain es increíble para construir aplicaciones de IA")
parsed_output = parser.parse(output)
```

### 5. Caché y Persistencia

```python
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

# Configurar caché en memoria
set_llm_cache(InMemoryCache())

# O usar caché SQLite
from langchain.cache import SQLiteCache
set_llm_cache(SQLiteCache(database_path=".langchain.db"))

# Las llamadas repetidas usarán caché
response1 = llm.invoke("¿Qué es LangChain?")  # Primera llamada
response2 = llm.invoke("¿Qué es LangChain?")  # Usa caché
```

## Recursos Adicionales

### Documentación Oficial
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [LangChain API Reference](https://api.python.langchain.com/)
- [LangChain JS/TS](https://js.langchain.com/docs/get_started/introduction)

### Comunidad
- [GitHub Repository](https://github.com/langchain-ai/langchain)
- [Discord Community](https://discord.gg/langchain)
- [Twitter/X](https://twitter.com/LangChainAI)

### Tutoriales y Cursos
- [LangChain University](https://learn.langchain.com/)
- [Cookbook con ejemplos](https://github.com/langchain-ai/langchain/tree/master/cookbook)
- [Videos tutoriales oficiales](https://www.youtube.com/@LangChain)

### Herramientas Complementarias
- [LangSmith](https://smith.langchain.com/) - Para debugging y monitoreo
- [LangServe](https://github.com/langchain-ai/langserve) - Para desplegar aplicaciones
- [LangChain Hub](https://smith.langchain.com/hub) - Compartir y descubrir prompts

### Integraciones Populares
- OpenAI, Anthropic, Google, Cohere
- Pinecone, Weaviate, ChromaDB, FAISS
- MongoDB, PostgreSQL, Redis
- Hugging Face, Replicate

## Conclusión

LangChain es un framework poderoso que simplifica el desarrollo de aplicaciones con LLMs. Su arquitectura modular, amplia gama de integraciones y abstracciones bien diseñadas lo convierten en una herramienta esencial para desarrolladores que trabajan con IA.

### Puntos Clave:
- **Modularidad**: Construye aplicaciones complejas con componentes simples
- **Flexibilidad**: Adapta y personaliza según tus necesidades
- **Comunidad**: Aprovecha el ecosistema en constante crecimiento
- **Mejores Prácticas**: Implementa patrones probados y optimizaciones

Con este manual, tienes las bases para comenzar a construir aplicaciones sofisticadas con LangChain. Recuerda experimentar, consultar la documentación oficial y participar en la comunidad para mantenerte actualizado con las últimas características y mejores prácticas.

---

*Última actualización: Julio 2025*