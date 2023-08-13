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

    # Build prompts
    template = """Utiliza los siguientes fragmentos de contexto para responder la pregunta al final. Si no conoces la respuesta, simplemente di que no lo sabes, no trates de inventar una respuesta.
    Responde en el mismo idioma que el idioma de la pregunta.
        {context}
        Pregunta: {question}
        Respuesta útil:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    follow_up_template = """Dada la siguiente conversación y una pregunta de seguimiento, reformula la pregunta de seguimiento para que sea una pregunta independiente, en su idioma original.

    conversación:
    {chat_history}
    pregunta de seguimiento: {question}
    pregunta independiente:"""

    condense_question_prompt = PromptTemplate(
        input_variables=['chat_history', 'question'],
        output_parser=None,
        partial_variables={},
        template=follow_up_template,
        template_format='f-string',
        validate_template=True
        )
    
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
        condense_question_prompt=condense_question_prompt,
        verbose = False,
        combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    return qa_chain