# Pregutna al PDF

English | [Español](README_es.md)

Este repositorio contiene el código fuente para la aplicación web: Pregunta al PDF. La aplicación permite a los usuarios cargar un documento PDF y, independientemente de su tamaño, comenzar a hacer preguntas sobre él. Además, proporciona un resumen conciso en formato de tabla de contenido como guía. La aplicación esta en español, pero la aplicación también admite respuestas en inglés. Utiliza LLaMA 2 o gpt-3.5 Turbo como su modelo de lenguaje; se proporcionan más detalles a continuación.

## Requisitos

* **Versión de Python:** 3.10
* **Bibliotecas:** langchain, pypdf, nltk, faiss, gensim, gradio, sentence-transformers, hugchat.
* **Instalación:** requirements.txt

## Uso

### Aplicación Web
La forma más sencilla de probar la aplicación es seguir el enlace:

[https://pdf.dsapp.me/](https://pdf.dsapp.me/)

Fue implementada con Docker y utilizando el servicio *serverless* de Google, *Cloud Run*.

### Instalación Local
Para ejecutar la aplicación web localmente, instalar Python 3.10 y Git. Luego, ejecutar en la terminal:

```bash
git clone https://github.com/a-jimenezc/pdf_chat
cd pdf_chat
pip install -r requirements.txt
python download_sentence_transformer.py
python app.py
```

## Descripción del Proyecto

El objetivo principal de este proyecto es permitir conversar con un documento PDF, independientemente de su tamaño y sin incurrir en costos adicionales. Esto se logró con la ayuda de bibliotecas y recursos de código abierto:

### Resumen con LDA
Proporcionar un resumen conciso del documento ayuda al usuario a comprender su contenido, facilitando el inicio de la conversación. Los Grandes Modelos de Lenguaje (LLMs) pueden resumir documentos documentos, pero el costo computacional para documentos extensos hace que usarlos directamente para esta tarea sea prohibitivamente caro. Por lo tanto, se efectuó preprocesamiento. **LDA** (Latent Dirichlet Allocation) es un gran algoritmo para el procesamiento de documentos. Produce una lista de palabras por tema, y permite seleccionar el número de temas y palabras por tema. Luego, las listas de palabras resultantes podrían ingresarse a un LLM, pidiéndole que articule una descripción utilizando lenguaje natural. Este enfoque ayuda a extraer las ideas principales del documento. En este caso, el resumen se presenta en un formato de tabla de contenido.

### "Local" Embeddings
Crear una base de datos de vectores para un libro de mil páginas requeriría muchas llamadas a un generador de *embeddings*. Afortunadamente, los modelos generadores de *embeddings* son relativamente pequeños y pueden ejecutarse en hardware convencional. La biblioteca **[SentenceTransformers](https://www.sbert.net)** es un "marco de trabajo de Python para *embeddings* de oraciones, texto e imágenes de última generación". Para este escenario, se utilizó los [Modelos Multi-Lingües](https://www.sbert.net/docs/pretrained_models.html#multi-lingual-models), debido al propósito multilingüe de la aplicación. *distiluse-base-multilingual-cased-v1* funcionó bien después de algunas pruebas, por lo que se utilizó este modelo.

### Soporte para LLM (Modelo de Lenguaje Grande)

#### HugChat, API de Chat de Hugging no oficial
La biblioteca [hugchat](https://github.com/Soulter/hugging-chat-api) de Soulter ofrece una API no oficial para [Hugging Chat](https://huggingface.co/chat/). Actualmente, el modelo que impulsa Hugging Chat es [LLaMA 2](https://huggingface.co/meta-llama/Llama-2-70b-chat-hf), de Meta. Por lo tanto, **los términos de uso, limitaciones, advertencias y licencias** estipulados tanto por LLaMA 2 como por Hugging Chat se aplican al usar esta aplicación web. Por favor, sigue los enlaces anteriores para obtener más información.

#### API de OpenAI
La aplicación también ofrece soporte para el modelo gpt-3.5 Turbo de OpenAI. Sin embargo, se requiere que los usuarios ingresen su propia clave API debido a los costos asociados. Tener en cuenta que esta información se guarda temporalmente en una base de datos por sesión. Una vez que se cierra la sesión, la clave API se elimina.

### Gradio
La aplicación fue construida con Gradio. Ofrece soporte tanto para el backend como para el frontend de aplicaciones de aprendizaje automático. Además, tienen un excelente soporte para modelos de lenguaje, incluido un objeto de chat muy útil.

### LangChain, la biblioteca de orquestación
LangChain hizo posible este proyecto. Ofrece un conjunto completo de herramientas para trabajar con LLMs, incluidas plantillas para *prompts*, bases de datos de vectores y más.

## Por Hacer
* Agregar soporte multilingüe
* Agregar más LLMs de donde elegir.

## Licencia
GNU General Public License v2.0

## Descargo de Responsabilidad
Esta aplicación se basa en bibliotecas y recursos de terceros. En consecuencia, su utilización está sujeta a términos de uso, condiciones y licencias específicas que se aplican a estas bibliotecas y recursos externos.

## Autor
[Antonio Jimenez Caballero](https://www.linkedin.com/in/antonio-jimnzc/)
