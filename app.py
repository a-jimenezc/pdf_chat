import time
import os
import gradio as gr
from langchain.memory import ConversationBufferMemory
from src import LLM_hugging_chat
from src import topics_from_pdf
from src import qa_convertational_chain_function
from langchain.llms import OpenAI
from pages.about import intro_html, author_html, openai_key_html

# Variables
email_1 = os.environ.get("HF_EMAIL_1")
psw_1 = os.environ.get("HF_PW_1")

email_2 = os.environ.get("HF_EMAIL_2")
psw_2 = os.environ.get("HF_PW_2")

model_llama2_1 = "LLaMA 2-HugChat-s1 (experimental)"
model_llama2_2 = "LLaMA 2-HugChat-s2 (experimental)"
model_gpt_1 = "GPT-3.5 Turbo (recomendado)"


css = """
footer {visibility: hidden}
.feedback textarea {font-size: 40px !important} 
"""

# Functions
def input_model(model):
    """
    Run when selecting the dropdown menu. This sets which model to use.
    """
    if model == model_gpt_1:
        #print(model_gpt_1)
        return {
            input_key : gr.update(visible=True),
            upload_uploaded_file : gr.update(visible=False),
            llm_str_var : model_gpt_1
                }
    elif model == model_llama2_2:
        #print(model_llama2_2)
        return {
            input_key : gr.update(visible=False),
            upload_uploaded_file : gr.update(visible=True),
            llm_str_var : model_llama2_2
                }
    else:
        #print(model_llama2_1)
        return {
            input_key : gr.update(visible=False),
            upload_uploaded_file : gr.update(visible=True),
            llm_str_var : model_llama2_1 # default is choosen in summary
            }

def input_openai_key(key):
    """
    The user is force to introduce the key if openAI model selected.
    """
    return {
        input_key : gr.update(visible=False),
        upload_uploaded_file : gr.update(visible=True),
        openai_key_var : key
        }

def input_lang(language):
    """
    The user is force to introduce the key if openAI model selected.
    """
    return {
        lang_var : language
        }

def show_model_caveat():
    return {model_availability_note : gr.update(visible=True)}

def summary(file, llm_model_str, openai_key, lang):
    # To use as default
    if llm_model_str == model_gpt_1:
        llm = OpenAI(openai_api_key=openai_key, max_tokens=-1)
    elif llm_model_str == model_llama2_2:
        llm = LLM_hugging_chat(
            n=2000, 
            hugging_face_account=email_2,
            hugging_face_psw=psw_2
            )
    else:
        llm = LLM_hugging_chat(
            n=2000, 
            hugging_face_account=email_1,
            hugging_face_psw=psw_1
            )

    num_topics = 5
    words_per_topic = 30 # optimizar
    file = file.name
    topics = topics_from_pdf(llm, file, num_topics, words_per_topic, lang)
    return {
        output_summary : topics,
        file_doc_var : file,
        processing_note: gr.update(visible=True),
        llm_var : llm,
        model_availability_note : gr.update(visible=False),
    }

def conversation_vars(file, llm_model, lang):
    """
    Initializes the chat sesion variables and stores them temporarily.
    """
    chain_type = "stuff"
    retreiver_search_type = "mmr"
    retreiver_k = 5
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa_chain = qa_convertational_chain_function(
        file, 
        llm_model, 
        chain_type, 
        retreiver_search_type, 
        retreiver_k,
        lang
        )
    return {
        memory_var : memory, 
        qa_chain_var : qa_chain,
        output_col : gr.update(visible=True),
        processing_note: gr.update(visible=False)
        }

def respond(query, chat_history, memory, qa_chain):
    """
    Response to user query
    """
    result = qa_chain({
        "question": query,
        "chat_history" : memory.load_memory_variables({})["chat_history"]
        })
    response = result["answer"]
    source_docs = result["source_documents"]
    memory.save_context({"input": query}, {"output": response})

    bot_message = response
    chat_history.append([query, bot_message])
    references = "\n".join(["\nPágina no. " + str(doc.metadata["page"]) + "\n" + doc.page_content + "..." for doc in source_docs])
    #time.sleep(2)
    return {
        input_msg : "",
        response_var : bot_message,
        chatbot : chat_history, 
        memory_var : memory,
        output_references : references
    }

def bot(history, response):
    """
    Streaming functionallity
    """
    bot_message = response
    history[-1][1] = ""
    for character in bot_message:
        history[-1][1] += character
        time.sleep(0.0005)
        yield history

def clear_memory(memory):
    memory.clear()
    return {
        memory_var : memory,
        output_references : ""
    }


with gr.Blocks(css=css, title="Pregunta al PDF") as demo:

    # Sesion variables
    file_doc_var = gr.State()
    qa_chain_var = gr.State()
    memory_var = gr.State()
    response_var = gr.State() # to allow streaming
    llm_str_var = gr.State()
    openai_key_var = gr.State()
    llm_var = gr.State()
    lang_var = gr.State()

    # Title
    gr.Markdown("\n")
    gr.Markdown('\n # <p style="text-align: center;">Pregunta al PDF</p>')
    gr.Markdown("\n")

    # Main Tab
    with gr.Tab("Inicio"):

        # Input
        with gr.Row(equal_height=True):
            with gr.Column(scale=0.25, min_width=0):
                model_dropdown = gr.Dropdown(
                    choices=[
                        model_llama2_1,
                        model_llama2_2,
                        model_gpt_1
                        ],
                    value=model_llama2_1,
                    label="Seleccionar modelo"
                    )
                lang_dropdown = gr.Dropdown(
                    choices=[
                        "Español",
                        "English",
                        ],
                    value="Español",
                    label="Seleccionar lenguaje de respuesta"
                    )
            with gr.Column(scale=0.75, visible=True, min_width=0) as upload_uploaded_file:
                uploaded_file = gr.UploadButton("Subir pdf 📁", file_types=["document"])
            with gr.Column(scale=0.75, visible=False, min_width=0) as input_key:
                model_api_textbox = gr.Textbox(
                    label="""Introducir la "API key" de OpenAi y precionar Enter""",
                    placeholder="sk-V8V..."
                    )
                
                with gr.Accordion("""Click para mayor información sobre la "API key" de OpenAi:""", open=False):
                    gr.HTML(openai_key_html)
                
        # Summary and processing notes
        with gr.Column(visible=False) as model_availability_note:
            gr.Markdown('\n ## <p style="text-align: center;">Cargando el modelo y resumiendo el documento...</p>')
            gr.Markdown('<p style="text-align: center;">Esto no debería demorar más de un minuto para \
                        documentos de menos de 30 páginas. \
                        Si no hay respuesta, puede que el modelo se encuentre temporalmente fuera de servicio. \
                        En este caso, refrescar la página y seleccionar otro modelo en el menú ubicado en la parte superior izquierda. \
                        Pronto se darán mas opciones.</p>')
            gr.Markdown('<p style="text-align: center;"> Para documentos extensos, esto puede demorar \
                        varios minutos.</p>')
        output_summary = gr.Textbox(label="Breve resumen del documento")
        with gr.Column(visible=False) as processing_note:
            gr.Markdown('\n ## <p style="text-align: center;">Procesando PDF...</p>')
            gr.Markdown('<p style="text-align: center;">Esto podría demorar unos minutos.</p>')
        
        # Chat and references
        with gr.Column(visible=False) as output_col:
            input_msg = gr.Textbox(label="Preguntar", placeholder="Introducir pregunta y presionar Enter")
            chatbot = gr.Chatbot()
            output_references = gr.components.Textbox(label="Referencias")
            clear_chat_memory = gr.Button(value="Borrar chat")
        
        gr.Markdown("Versión 0.1")

        # Interactivity
        model_dropdown.input(
            input_model,
            [model_dropdown],
            [input_key, upload_uploaded_file, llm_str_var]
            )
        lang_dropdown.input(
            input_lang,
            [lang_dropdown],
            [lang_var]
            )
        model_api_textbox.submit(
            input_openai_key,
            [model_api_textbox],
            [input_key, upload_uploaded_file, openai_key_var]
             )                 
        uploaded_file.upload(
            show_model_caveat,
            None,
            [model_availability_note],
            ).success(summary,
                [uploaded_file, llm_str_var, openai_key_var, lang_var],
                [output_summary, file_doc_var, processing_note, llm_var, model_availability_note],
                queue=False
                ).success(
                    conversation_vars,
                    [file_doc_var, llm_var, lang_var],
                    [memory_var, qa_chain_var, output_col, processing_note]
                    ).success( # delete displayed chat
                        lambda: None,
                        None,
                        chatbot,
                        queue=False
                        )
        input_msg.submit(
            respond,
            [input_msg, chatbot, memory_var, qa_chain_var],
            [input_msg, response_var, chatbot, memory_var, output_references],
            queue=False
            ).success(
                bot,
                [chatbot, response_var],
                chatbot
                )
        clear_chat_memory.click(
            clear_memory, # memory for model
            [memory_var],
            [memory_var, output_references]
            ).success( # displayed chat
                lambda: None,
                None,
                chatbot,
                queue=False
                )

    # # Model Explanation Tab
    # with gr.Tab("Modelos"):
    #     gr.Markdown("## LLaMA 2")

    # About Tab
    with gr.Tab("Acerca de"):
        gr.Markdown(intro_html)
        gr.HTML(author_html)

demo.queue(concurrency_count=5,  max_size=10, api_open=False)
#demo.launch()
demo.launch(server_name="0.0.0.0", server_port=8080)