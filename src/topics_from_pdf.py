import gensim
import nltk
from gensim import corpora
from gensim.models import LdaModel
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from pypdf import PdfReader
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

def preprocess(text, stop_words):
    """
    Tokenizes and preprocesses the input text, removing stopwords and short tokens.

    
    Parameters:
        text (str): The input text to preprocess.

    Returns:
        list: A list of preprocessed tokens.
    """
    result = []
    for token in simple_preprocess(text, deacc=True):
        if token not in stop_words and len(token) > 3:
            result.append(token)
    return result


def get_topic_lists_from_pdf(file, num_topics, words_per_topic):
    """
    Extracts topics and their associated words from a PDF document using the Latent Dirichlet 
    Allocation (LDA) algorithm.

    Parameters:
        file (str): The path to the PDF file for topic extraction.
        num_topics (int): The number of topics to discover.
        words_per_topic (int): The number of words to include per topic.

    Returns:
        list: A list of num_topics sublists, each containing relevant words for a topic.
    """
    loader = PdfReader(file)

    documents= []
    for page in loader.pages:
        documents.append(page.extract_text())

    # Preprocess the documents
    nltk.download('stopwords')
    stop_words = set(stopwords.words(['english','spanish']))

    processed_documents = [preprocess(doc, stop_words) for doc in documents]

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

def topics_from_pdf(llm, file, num_topics, words_per_topic, lang):
    """
    Generates descriptive prompts for LLM based on topic words extracted from a PDF document.

    This function takes the output of `get_topic_lists_from_pdf` function, which consists of a list
    of topic-related words for each topic, and generates an output string in table of content format.

    Parameters:
        llm (LLM): An instance of the Large Language Model (LLM) for generating responses.
        file (str): The path to the PDF file for extracting topic-related words.
        num_topics (int): The number of topics to consider.
        words_per_topic (int): The number of words per topic to include.
        lang (str): The prompt language

    Returns:
        str: A response generated by the language model based on the provided topic words.
    """

    # Extract topics and convert to string
    list_of_topicwords = get_topic_lists_from_pdf(file, num_topics, words_per_topic)
    string_lda = ""
    for list in list_of_topicwords:
        string_lda += str(list) + "\n"

    # LLM call
    if lang == "English":
        template_string = '''Describe the theme of each of the double-quote delimited lists in a simple sentence and also write down three possible different subthemes. The lists are the result of an algorithm for topic discovery.
        Do not provide an introduction or a conclusion, only describe the themes.
        Use the following template for the response.

        Theme 1: <<<(sentence describing the theme)>>>
        - <<<(Phrase describing the first subtheme)>>>
        - <<<(Phrase describing the second subtheme)>>>
        - <<<(Phrase describing the third subtheme)>>>

        Theme 2: <<<(sentence describing the theme)>>>
        - <<<(Phrase describing the first subtheme)>>>
        - <<<(Phrase describing the second subtheme)>>>
        - <<<(Phrase describing the third subtheme)>>>

        ...

        Theme n: <<<(sentence describing the theme)>>>
        - <<<(Phrase describing the first subtheme)>>>
        - <<<(Phrase describing the second subtheme)>>>
        - <<<(Phrase describing the third subtheme)>>>

        Lists: """{string_lda}""" '''
    else:
        template_string = '''Describe el tema de cada una de las listas delimitadas por comillas en una oración sencilla y escribe además tres posibles subtemas diferentes. Las listas son el resultado de un algoritmo para descubrir temas.
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