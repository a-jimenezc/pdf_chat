# Ask the PDF

This repository contains the source code for the web application: Ask the pdf. The application allows the user to upload a document in pdf format and then start asking questions to it. As a guide, it also returns a brief summary in table-of-contents format. Initially, the application was implemented for Spanish speakers, but later it was extended for its use in English. It uses LLaMA 2 or gpt 3.5 as its language model, more details are given bellow.

## Requirements

* **Python version:** 3.10
* **Libraries:** langchain, pypdf, nltk, faiss, gensim, gradio, sentence-transformers, hugchat.
* **Installation:** requirements.txt

## Usage

### Web App
The simplest way to try the app is to follow the link: 

[https://pdf-chat-q3sojgpqiq-uc.a.run.app/](https://pdf-chat-q3sojgpqiq-uc.a.run.app/)

It was   deployed using the serverless service from Google, *Cloud Run*.
