# Ask the PDF

This repository contains the source code for the web application: Ask the pdf. The application allows the user to upload a document in pdf format and, regardless of the size, start asking questions to it. As a guide, it also returns a brief summary in table-of-contents format. Initially, the application was implemented for Spanish speakers, but later it was extended for its use in English. It uses LLaMA 2 or gpt 3.5 as its language model, more details are given bellow.

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
For a local installation run:

```bash
git clone https://github.com/a-jimenezc/pdf_chat
cd pdf_chat
pip install -r requirements.txt
python download_sentence_transformer.py
python app.py
```

## Project Description

The main goal of this project is to enable chatting with a PDF document, regardless of its size and without incurring any additional cost. This was achieved with the help of open source libaries and resources. The following were the main ideas

### Summarization with LDA
Returning a brief summary of the document helps the user to have an idea of the content, making it easier to start chatting. LLMs could easily summarize documents, but the computational cost for large documents would make using them for the whole document prohibitively expensive. So, some preprossessing was needed. **LDA** (Latent Dirichlet Allocatioin) is a great algorithm for document processing. It yields a list of words per topic, with the possiblility to control the number of topics and words per topic. Then, the output word lists could be feeded to an LLM and ask it to describe them in natural language, thus extracting the main ideas from the document. In this case, the summary is given in a table-of-content format.

### Local Embeddings
Creating a vector database for a one thousand page book would require a lot of calls to an embedding generator. Luckily, those models are relarively small and can be run in consumer hardware. The library **[SentenceTransformers](https://www.sbert.net)** is a "Python framework for state-of-the-art sentence, text and image embeddings". In this case, [Multi-Lingual Models](https://www.sbert.net/docs/pretrained_models.html#multi-lingual-models) were necessary, due to the multilingual purpose of the application. *distiluse-base-multilingual-cased-v1* worked fine after some testing, so this was used.

### HugChat, Unoficial Hugging Chat API
There were several options for free LLM support. One promising option was [Petal](https://github.com/bigscience-workshop/petals), but the size and the speed of generation were important limitations. Luckily, again, the library [hugchat](https://github.com/Soulter/hugging-chat-api) by Soulter offered an unofficial API for [Hugging Chat](https://huggingface.co/chat/). Currently, the model powering Hugging Chat is [LLaMA 2](https://huggingface.co/meta-llama/Llama-2-70b-chat-hf), from Meta. So, **the terms of use, limitations, caveats, and licencing** from both, LLaMA 2 and Hugging Chat, apply when using this web application. Please, follow the previous links for more information.


### Gradio Suport for Chat Applications

### Lang Chain as an orchestration library



