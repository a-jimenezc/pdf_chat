import gensim
import nltk
from gensim import corpora
from gensim.models import LdaModel
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from pypdf import PdfReader
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate


def get_topic_lists_from_pdf(file, num_topics, words_per_topic):
    """
    Uses LDA algoritm for topic discovery
    Returns: list of num_topics lists with relevant words for each topic (nested list).
    """
    loader = PdfReader(file)

    documents= []
    for page in loader.pages:
        documents.append(page.extract_text())

    # Preprocess the documents
    nltk.download('stopwords')
    stop_words = set(stopwords.words(['english','spanish']))

    def preprocess(text):
        result = []
        for token in simple_preprocess(text, deacc=True):
            if token not in stop_words and len(token) > 3:
                result.append(token)
        return result

    processed_documents = [preprocess(doc) for doc in documents]

    # Create a dictionary and a corpus
    dictionary = corpora.Dictionary(processed_documents)
    corpus = [dictionary.doc2bow(doc) for doc in processed_documents]

    # Build the LDA model
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

    # Print the topics and their corresponding words
    topics = lda_model.print_topics(num_words=words_per_topic)
    topics_ls = []
    for topic in topics:
        words = topic[1].split("+")
        topic_words = [word.split("*")[1].replace('"', '').strip() for word in words]
        topics_ls.append(topic_words)
        
    return topics_ls

def topics_from_pdf(llm, file, num_topics, words_per_topic):
    """
    Takes a the output of get_topic_lists_from_pdf and returns a string
    """

    # Extract topics and convert to string
    list_of_topicwords = get_topic_lists_from_pdf(file, num_topics, words_per_topic)
    string_lda = ""
    for list in list_of_topicwords:
        string_lda += str(list) + "\n"

    # LLM call
    template_string = '''Describe el tema de cada una de las listas delimitadas por comillas en una oración sencilla y escribe además tres posibles subtemas diferentes. Las listas son el resultado del algoritmo "Latent Dirichlet Allocation" para descubrir temas.
    No des una introducción ni una conclusión, solo describe los temas.
    Utiliza el siguiente Template para la respuesta. 

    Tema  1: <<<(oración que describe el tema)>>>
    - <<<Frase que describe primer subtema)>>>
    - <<<(Frase que describe segundo subtema)>>>
    - <<<Frase que describe tercer subtema)>>>

    Tema  2: <<<(oración que describe el tema)>>>
    - <<<Frase que describe primer subtema)>>>
    - <<<(Frase que describe segundo subtema)>>>
    - <<<Frase que describe tercer subtema)>>>
    
    ...

    Tema  n: <<<(oración que describe el tema)>>>
    - <<<Frase que describe primer subtema)>>>
    - <<<(Frase que describe segundo subtema)>>>
    - <<<Frase que describe tercer subtema)>>>
    
    Listas: """{string_lda}""" '''

    prompt_template = ChatPromptTemplate.from_template(template_string)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain.run(string_lda)

    return response