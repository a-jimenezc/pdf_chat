import gensim
import nltk
from gensim import corpora
from gensim.models import LdaModel
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from pypdf import PdfReader

def get_topics_from_pdf(file, num_topics, words_per_topic):
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