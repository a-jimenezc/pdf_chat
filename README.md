# Ask the PDF

This repository contains the source code for the web application: Ask the PDF. The application enables users to upload a PDF document and, regardless of its size, begin asking questions about it. Additionally, it provides a concise summary in a table-of-contents format as a guide. It was designed for Spanish speakers, but the application also supports responses in English. It utilizes LLaMA 2 or gpt-3.5 Turbo as its language model; further details are provided below.

## Requirements

* **Python version:** 3.10
* **Libraries:** langchain, pypdf, nltk, faiss, gensim, gradio, sentence-transformers, hugchat.
* **Installation:** requirements.txt

## Usage

### Web App
The simplest way to try the app is to follow the link: 

[https://pdf-chat-q3sojgpqiq-uc.a.run.app/](https://pdf-chat-q3sojgpqiq-uc.a.run.app/)

It was deployed with Docker and using the serverless service from Google, *Cloud Run*.

### Local installation
To run the web app on your local machine, install python 3.10 and git. Then, run on the terminal:

```bash
git clone https://github.com/a-jimenezc/pdf_chat
cd pdf_chat
pip install -r requirements.txt
python download_sentence_transformer.py
python app.py
```

## Project Description

The main goal of this project is to enable chatting with a PDF document, regardless of its size and without incurring any additional cost. This was achieved with the help of open source libaries and resources:

### Summarization with LDA
Providing a concise summary of the document helps the user gain an understanding of its content, making it easier to start chatting. LLMs could easily summarize documents, but the computational cost for large documents makes using them for this task prohibitively expensive. So, some preprossessing was needed. **LDA** (Latent Dirichlet Allocatioin) is a great algorithm for document processing. It produces a list of words per topic, allowing the selection of the number of topics and words per topic. Then, the output word lists could be feeded into an LLM and ask, prompting it to articulate a description using natural language. This approach aids in extracting the core ideas from the document. In this case, the summary is given in a table-of-content format.

### "Local" Embeddings
Creating a vector database for a one thousand page book would require a lot of calls to an embedding generator. Luckily, those models are relarively small and can be run in consumer hardware. The library **[SentenceTransformers](https://www.sbert.net)** is a "Python framework for state-of-the-art sentence, text and image embeddings". For this scenario, [Multi-Lingual Models](https://www.sbert.net/docs/pretrained_models.html#multi-lingual-models) were necessary, due to the multilingual purpose of the application. *distiluse-base-multilingual-cased-v1* worked fine after some testing, so this was used.

### LLM (Large Language Model) Support

#### HugChat, Unofficial Hugging Chat API
The library [hugchat](https://github.com/Soulter/hugging-chat-api) by Soulter offered an unofficial API for [Hugging Chat](https://huggingface.co/chat/). Currently, the model powering Hugging Chat is [LLaMA 2](https://huggingface.co/meta-llama/Llama-2-70b-chat-hf), from Meta. So, **the terms of use, limitations, caveats, and licencing** stipulated by both LLaMA 2 and Hugging Chat apply when using this web application. Please, follow the previous links for more information.

#### OpenAi API
The application also offers support for the OpenAI gpt-3.5 Turbo model. However, users are required to input their own API key due to associated costs. Please note that this information is kept temporarily in a per sesion basis. Once the sesion is closed, the API key is deleted.

### Gradio
The application was built with gradio. It offers back-end and front-end support for machine learning applications. Also, they have an exelent support for language models, including a very handy chat object. 

### LangChain, the orchestration library
LangChain made this project possible. It offers a rich set of tools for working wiht LLMs, including template for prompts, vector databases, and more.

## To do
* Add multilanguage support
* Add more LLMs to choose from.

## Licence
GNU General Public License v2.0

## Disclaimer
This application relies on third-party libraries and resources. Consequently, its utilization is subject to specific terms of use, conditions, and licenses that pertain to these external libraries and resources.

## Author
[Antonio Jimenez Caballero](https://www.linkedin.com/in/antonio-jimnzc/)



