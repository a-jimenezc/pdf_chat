from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings # see also sentence-transformers
from langchain.document_loaders import PyPDFLoader # install pypdf
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain

def qa_convertational_chain_function(
        file,
        llm,
        chain_type,
        retreiver_search_type,
        retreiver_k,
        ):
    
    """
    Parameters
    chain_type: The chain type to use to create the combine_docs_chain, will be sent to load_qa_chain.
    Returns 
    ConversationalRetrievalChain object.
    """

    # Build prompt
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. 
    Answer in the same language as the Question language.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
    
    # Creating vector db
    loader = PyPDFLoader(file)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index = False,
        )
    pages = loader.load_and_split()
    chunks = text_splitter.split_documents(pages)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/distiluse-base-multilingual-cased-v1",
        cache_folder="./sentence_transformers"
        )
    vectordb = FAISS.from_documents(chunks, embedding=embeddings)

    retreiver = vectordb.as_retriever(
        search_type=retreiver_search_type, 
        search_kwargs={"k": retreiver_k}
        )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type=chain_type, 
        retriever=retreiver,
        return_source_documents=True,
        return_generated_question=True,
        verbose = False,
        combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    return qa_chain