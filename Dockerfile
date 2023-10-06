FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python download_sentence_transformer.py
EXPOSE 8080
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
