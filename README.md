# Banorte CV Agent - Reto IA

**Por:** Víctor Molina Sánchez  
**Perfil:** DevSecOps / Cloud Architect  

Este repositorio contiene el código de mi agente conversacional para el Reto IA de Banorte. El objetivo de este diseño no fue solo conectar una API, sino mostrar cómo estructurar, asegurar y desplegar un servicio de IA siguiendo buenas prácticas de ingeniería.

## 1. Arquitectura (Monorepo)

Decidí estructurar el proyecto como un monorepo para separar claramente las responsabilidades. 

* **`01_foundation/` y `04_deployment/`**: Contienen *stubs* (plantillas) de Terraform. Por el límite de tiempo del hackathon, el despliegue final lo hice mediante la CLI de Google Cloud, pero dejé estos archivos como muestra de cómo automatizaría la infraestructura en un entorno productivo real.
* **`02_security/`**: Esqueletos para reglas de OPA (Open Policy Agent) y escaneos de vulnerabilidades (*Shift-Left Security*).
* **`03_microservice/`**: Aquí vive el código funcional del agente (FastAPI).

## 2. El Agente y el Modelo

El servicio expone un endpoint principal compatible con **Open Responses** (`/v1/responses`) y mantiene compatibilidad adicional con **Chat Completions** (`/v1/chat/completions`). Por detrás, la generación se realiza con la API de **Gemini 3.6 Flash**.

Para inyectar el contexto de mi perfil, implementé un flujo RAG simplificado que indexa documentos Markdown dentro de `03_microservice/knowledge/` (perfil, experiencia, educación, habilidades y proyectos). Usé un *System Prompt* estricto para mantener respuestas técnicas, verificables y alineadas al CV.

## 3. Seguridad y Buenas Prácticas

Al apuntar a un sector bancario, traté de cubrir lo básico de DevSecOps:
* **Protección de Inputs:** Un sanitizador basado en RegEx para mitigar intentos básicos de *Prompt Injection* antes de que lleguen al LLM.
* **Docker seguro:** El `Dockerfile` aplica el Principio de Menor Privilegio (PoLP). Creé un `appuser` para asegurar que el contenedor no se ejecute como `root`.
* **Gestión de Secretos:** Configuré reglas estrictas en `.gitignore` y resolví advertencias de *Secret Scanning* en GitHub para asegurar que mis API Keys nunca se filtren. Las llaves se inyectan como variables de entorno directamente en el servicio Cloud Run.

## 4. Despliegue en la Nube

El agente está dockerizado usando una imagen ligera (`python:3.11-slim`) y fue desplegado en **Google Cloud Run** (Serverless) para asegurar disponibilidad y escalabilidad automática.

* **Endpoint público (Open Responses):** `https://banorte-cv-agent-252099743248.us-central1.run.app/v1/responses`
* **Compatibilidad adicional (Chat Completions):** `https://banorte-cv-agent-252099743248.us-central1.run.app/v1/chat/completions`

