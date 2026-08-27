# Guion de Demostracion - Reto IA Banorte

## 1. Objetivo de la demostracion
Demostrar que la solucion no es solo un prototipo funcional, sino un diseno de agente con criterio de ingenieria bancaria: seguridad por capas, arquitectura modular, trazabilidad operativa y capacidad de evolucionar a entorno empresarial.

## 2. Mensaje central para abrir el video (30-45 segundos)
Hola, soy Victor Molina. En esta demostracion presento un agente conversacional de CV desplegado en Google Cloud Run, compatible con Open Responses y disenado con buenas practicas de seguridad y operacion.

El objetivo del reto no era cargar millones de documentos, sino demostrar criterio tecnico para convertir una idea en un producto funcional y confiable. Por eso implemento una base de conocimiento acotada, pero con una arquitectura preparada para escalar a un escenario bancario real.

## 3. Historia tecnica recomendada (6-8 minutos)

### 3.1 Arquitectura del repositorio
Explicar el monorepo por dominios de responsabilidad:
- 01_foundation: base de infraestructura como codigo para red y KMS.
- 02_security: politicas y reglas de seguridad para control preventivo.
- 03_microservice: servicio funcional del agente con API, guardrails y recuperacion de contexto.
- 04_deployment: estructura de despliegue para Cloud Run y componentes operativos.

Mensaje clave:
Algunas carpetas estan como plantilla porque en un proyecto laboral completo se despliegan con pipelines, aprobaciones y controles de entorno. En este reto, priorice una entrega funcional en tiempo con trazabilidad de decisiones y camino de evolucion claro.

### 3.2 Flujo del agente
1. El cliente llama al endpoint publico.
2. Se valida API key antes de cualquier inferencia.
3. Se sanitiza la entrada para bloquear prompt injection.
4. Se recupera contexto del CV desde la base de conocimiento.
5. Se construye el system prompt con ese contexto.
6. Se consulta el modelo Gemini.
7. Se filtra la salida para reducir riesgo de fuga de datos.
8. Se responde en formato Open Responses terminal.

### 3.3 Por que escalar reducido fue una decision consciente
Narrativa sugerida:
- No era necesario simular un lago documental de millones de lineas para demostrar arquitectura de IA generativa.
- Para un agente de CV, la mejor practica es conocimiento curado, versionado y auditable.
- En banca, primero se valida control y gobernanza; luego se expande volumen.

Frase util:
Preferi demostrar calidad de arquitectura, seguridad y operacion sobre volumen artificial de datos.

### 3.4 Seguridad aplicada
- Autenticacion por token Bearer.
- Guardrail de entrada contra instrucciones maliciosas.
- Filtro de salida para enmascarar patrones sensibles.
- Contenedor sin usuario root.
- Separacion de configuracion via variables de entorno.

### 3.5 Operacion y observabilidad
- Logs estructurados en API, capa de agente y recuperador RAG.
- Trazas de parseo, consulta, recuperacion y estado final de respuesta.
- Contrato de salida validado para evitar errores de integracion con frontend.

## 4. Que mostrar en pantalla durante la demo

### 4.1 Estructura del repositorio
Mostrar carpetas y explicar:
- Lo implementado en produccion del reto esta en 03_microservice.
- 01_foundation, 02_security y 04_deployment muestran preparacion para un ciclo enterprise.

### 4.2 Endpoint y contrato
Probar el endpoint Open Responses y remarcar:
- object: response
- status: completed
- output con message y output_text

### 4.3 Pruebas automatizadas
Mostrar ejecucion de pruebas para evidenciar calidad tecnica:
- health
- contrato Open Responses
- seguridad por API key
- bloqueo de prompt injection
- compatibilidad con chat completions

## 5. Justificacion de carpetas plantilla o vacias
Texto sugerido para explicarlo en video:
En un entorno bancario real, estas carpetas se completan por fases y por equipos: red, seguridad, despliegue y monitoreo. Aqui las deje como estructura objetivo para evidenciar que conozco el proceso enterprise, aunque para el reto priorice una implementacion funcional, auditable y desplegada de extremo a extremo.

## 6. Riesgos identificados y siguiente evolucion (muy importante para perfil senior)
- Migrar de indice TF-IDF local a vector store administrado.
- Incorporar evaluacion automatica de respuestas con metricas de relevancia y factualidad.
- Endurecer politicas OPA en pipeline CI/CD.
- Agregar monitoreo de costo, latencia y tasa de rechazo por guardrails.
- Implementar versionado formal de prompts y knowledge base.

## 7. Cierre de demostracion (20-30 segundos)
Esta solucion cumple con el objetivo del reto: agente funcional, integrado y desplegado, con decisiones tecnicas alineadas a seguridad y operacion bancaria. Mi enfoque fue construir una base pequena pero correcta, lista para escalar con practicas reales de MLOps y DevSecOps.

## 8. Preguntas probables del jurado y respuesta corta

Pregunta: Por que no usaste millones de documentos?
Respuesta: Porque para este caso de uso, una base curada de CV es mas confiable y auditable. El valor evaluado esta en arquitectura y gobernanza, no en volumen artificial.

Pregunta: Que faltaria para produccion bancaria completa?
Respuesta: Politicas y pipelines totalmente automatizados, monitoreo profundo, evaluacion continua del agente y gestion empresarial de identidades, llaves y cumplimiento.

Pregunta: Como evitas respuestas fuera de contexto?
Respuesta: Guardrails de entrada, contexto recuperado por consulta, system prompt estricto y control de salida antes de responder.

## 9. Checklist de grabacion
- Confirmar endpoint publico activo.
- Confirmar API key de prueba configurada.
- Ejecutar pruebas automatizadas.
- Ensayar opening y cierre.
- Limitar demo a 8-10 minutos.
