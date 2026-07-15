<!-- Logo y badges -->
<p align="center">
    <img alt="ÁnimAgent" src="assets/logo.png">
</p>

<h3 align="center">Un chatbot IA de conocimiento institucional</h3>

<div align="center">
    <img src="https://img.shields.io/badge/STATUS-EN%20DESAROLLO-blue">
    <img src="https://img.shields.io/badge/Oracle%20ONE%202026-8A2BE2?logo=livechat&logoColor=white&link=https%3A%2F%2Fwww.oracle.com%2Flatam%2Feducation%2Foracle-next-education">
    <img src="https://img.shields.io/badge/LangChain-blue?logo=langchain">
</div>

<!-- Visión general -->
## 📖︲Descripción

ÁnimAgent es un agente de inteligencia artificial diseñado para responder preguntas sobre la documentación institucional de un instituto. A partir de documentos reales como reglamentos, horarios, políticas de becas y preguntas frecuentes, el agente recupera información relevante y genera respuestas claras y confiables, sin alucinar datos que no estén en la fuente.

Desarrollado como proyecto de la segunda etapa Oracle ONE 2026, ÁnimAgent combina técnicas modernas de RAG (Generación Aumentada por Recuperación) con un agente inteligente basado en LangGraph, capaz de enrutar cada consulta al conjunto de documentos más adecuado antes de responder.

<!-- Características principales -->
## 💫︲Características principales

- **RAG (Generación Aumentada por Recuperación):** las respuestas se generan a partir de fragmentos reales de la documentación institucional, no de conocimiento genérico del modelo.
- **Agente con routing inteligente:** basado en LangGraph, el agente analiza cada pregunta y decide qué colección de documentos consultar antes de responder.
- **Fragmentación semántica de documentos:** los documentos se dividen en chunks con superposición para preservar el contexto entre fragmentos.
- **Embeddings con HuggingFace:** generación de representaciones vectoriales de los textos usando modelos de embeddings de HuggingFace.
- **Base de datos vectorial FAISS:** almacenamiento y búsqueda eficiente de embeddings para recuperación de fragmentos relevantes.
- **Integración con múltiples LLMs:** soporte para Google Gemini (con API key propia del usuario) y Groq como alternativa gratuita.
- **Citación de fuentes:** el agente indica de qué documento proviene la información utilizada para generar la respuesta.
- **Interfaz de chat moderna:** frontend construido con Astro y Vue, accesible desde el navegador.
- **Desplegado en Oracle Cloud Infrastructure:** la aplicación corre en OCI Compute y es accesible públicamente.
- **Arquitectura preparada para Docker:** contenedorización del backend para facilitar el despliegue y la portabilidad.
- **API key configurable por el usuario:** el usuario puede ingresar su propia API key de Google Gemini desde la interfaz; de lo contrario, el sistema utiliza Groq automáticamente.

<!-- Arquitectura del sistema -->
## ⚙️︲Arquitectura y flujo

> 🚧 En proceso. La documentación de la arquitectura y el diagrama de flujo del agente estarán disponibles próximamente.

<!-- Estructura del Proyecto -->
## 📂︲Estructura del proyecto

```text
animagent/
│
├── assets/                     # Imágenes, logo y archivos estáticos del proyecto
│
├── documents/                  # Documentación de la institución
│
├── backend/
│   ├── agent/
│   │   ├── graph.py            # StateGraph de LangGraph (nodos y conexiones)
│   │   ├── nodes.py            # Lógica de cada nodo del agente
│   │   ├── router.py           # Lógica de routing entre colecciones
│   │   └── state.py            # Definición del estado que viaja por el grafo
│   │
│   ├── rag/
│   │   ├── loader.py           # Carga y parseo de PDFs y CSVs
│   │   ├── embeddings.py       # Generación de embeddings e índice FAISS
│   │   └── retriever.py        # Búsqueda de fragmentos relevantes
│   │
│   ├── models/
│   │   └── factory.py          # Instancia Gemini o Groq según disponibilidad
│   │
│   ├── api/
│   │   └── routes.py           # Endpoints FastAPI
│   │
│   ├── config.py               # Variables de entorno y configuración global
│   ├── main.py                 # Punto de entrada del servidor
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.vue  # Ventana de mensajes
│   │   │   ├── ChatInput.vue   # Input del usuario
│   │   │   └── ApiKeyModal.vue # Modal para ingresar API key propia
│   │   ├── pages/
│   │   │   └── index.astro     # Página principal
│   │   └── services/
│   │       └── api.ts          # Llamadas al backend
│   ├── astro.config.mjs
│   └── package.json
│
├── .env.example                # Template de variables de entorno
├── .gitignore
└── README.md
```

<!-- Tecnologías usadas -->
## ☕︲Tech Stack

### Lenguajes

- Python 3.11+
- TypeScript

### IA / LLM

- [LangChain](https://www.langchain.com/) — orquestación de cadenas y herramientas
- [LangGraph](https://langchain-ai.github.io/langgraph/) — agente con flujo basado en grafos de estado
- [Google Gemini](https://deepmind.google/technologies/gemini/) — modelo de lenguaje principal (con API key del usuario)
- [Groq](https://groq.com/) — modelo de lenguaje alternativo gratuito

### Recuperación de datos

- [FAISS](https://faiss.ai/) — base de datos vectorial para búsqueda semántica
- [HuggingFace Embeddings](https://huggingface.co/) — generación de representaciones vectoriales

### Procesamiento de documentos

- [PyPDF](https://pypdf.readthedocs.io/) — lectura y extracción de texto de PDFs
- [Pandas](https://pandas.pydata.org/) — procesamiento de archivos CSV

### Interfaz de usuario

- [Astro](https://astro.build/) — framework web para el frontend
- [Vue 3](https://vuejs.org/) — componentes interactivos del chat
- [FastAPI](https://fastapi.tiangolo.com/) — API REST del backend

### Cloud

- [Oracle Cloud Infrastructure (OCI)](https://www.oracle.com/cloud/) — hosting del agente en OCI Compute

### DevOps

- [Docker](https://www.docker.com/) — contenedorización del backend
- [Git](https://git-scm.com/) / [GitHub](https://github.com/) — control de versiones

<!-- Roadmap -->
## 🛤️︲Roadmap

### ⌛｜Versión 1.0

- Agente RAG funcional con LangGraph y routing por tipo de documento
- Indexación de todos los documentos institucionales (PDFs y CSVs)
- Backend con FastAPI
- Frontend de chat con Astro y Vue
- Soporte para Google Gemini y Groq
- API key configurable desde la interfaz por el usuario
- Citación de la fuente utilizada en cada respuesta
- Deploy en OCI Compute
- Arquitectura contenedorizada con Docker
- README con descripción, arquitectura y ejemplos de uso

### 🚧｜Versión 1.1

- Historial de conversación por sesión (memoria de contexto)
- Indicador visual de qué documento consultó el agente en cada respuesta
- Mejoras de UI: animaciones, estados de carga, manejo de errores visible
- Soporte para modelos adicionales (OpenAI, Cohere)

### 🚧｜Versión 1.2

- Carga de documentos nuevos sin necesidad de reiniciar el servidor (hot reload del índice)
- Sistema de feedback por respuesta (pulgar arriba / abajo)
- Logging de consultas para análisis de uso
- Tests automatizados del agente y del backend

### 🚧｜Versión 2.0

- Soporte multiidioma (español e inglés)
- Panel de administración para cargar y gestionar documentos desde la interfaz
- Autenticación de usuarios (estudiantes vs. administrativos)
- Respuestas diferenciadas según el perfil del usuario autenticado
