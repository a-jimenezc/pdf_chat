import time
import gradio as gr
from langchain.memory import ConversationBufferMemory
from src import LLM_gradioAPI
from src import topics_from_pdf
from src import qa_convertational_chain_function
from langchain.llms import OpenAI

# Define the LLM endpoint

css = """
footer {visibility: hidden}
.feedback textarea {font-size: 40px !important} 
"""

with gr.Blocks(css=css) as demo:

    # Sesion variables
    file_doc = gr.State()
    qa_chain_var = gr.State()
    memory_var = gr.State()
    response_var = gr.State() # to allow streaming
    llm_var = gr.State()

    # Layout
    gr.Markdown("\n")
    gr.Markdown('\n # <p style="text-align: center;">Pregunta al PDF</p>')
    gr.Markdown("\n")

    # Functions
    def input_openai_key(model):
        # Due to the flow of the app, it is ok to have this here
        llm = LLM_gradioAPI(n=2000)
        llm.client_api = "https://ysharma-explore-llamav2-with-tgi.hf.space/"
        llm.api_name = "/chat_1"
        if model == "GPT-3.5 Turbo":
            return {
                input_key : gr.update(visible=True),
                upload_btn : gr.update(visible=False),
                llm_var : llm
                    }
        else:
            return {
                input_key : gr.update(visible=False),
                upload_btn : gr.update(visible=True),
                llm_var : llm
                    }
    
    def input_model(key):
        #print(key)
        llm = OpenAI(openai_api_key=key, max_tokens=-1)
        return {
            input_key : gr.update(visible=False),
            upload_btn : gr.update(visible=True),
            llm_var : llm
                }

    def summary(file, llm_model):
        #print(llm_model)
        if llm_model is None:
            llm_model = LLM_gradioAPI(n=2000) # hugging face repo
            llm_model.client_api = "https://ysharma-explore-llamav2-with-tgi.hf.space/"
            llm_model.api_name = "/chat_1"
            print(llm_model)
        num_topics = 5
        words_per_topic = 30 # optimizar
        file = file.name
        topics = topics_from_pdf(llm_model, file, num_topics, words_per_topic)
        return {
            output_summary : topics,
            file_doc : file,
            processing_note: gr.update(visible=True),
            llm_var : llm_model
        }
        
    def conversation_vars(file, llm_model):
        """
        Initializes the chat sesion variables and stores them temporarily.
        """
        chain_type = "stuff"
        retreiver_search_type = "mmr"
        retreiver_k = 5
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        qa_chain = qa_convertational_chain_function(file, llm_model, chain_type, retreiver_search_type, retreiver_k)
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
        references = "\n".join(["\nPágina no. " + str(doc.metadata["page"]) + "\n" + doc.page_content[:150] + "..." for doc in source_docs])
        time.sleep(2)
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

    with gr.Tab("Inicio"):

        with gr.Row(equal_height=True):#.style(equal_height=True):
            with gr.Column(scale=0.75, visible=True) as upload_btn:
                btn = gr.UploadButton("Subir pdf 📁", file_types=["document"])
            with gr.Column(scale=0.75, visible=False) as input_key:
                model_api_textbox = gr.Textbox(label="Introducir OpenAI api key",
                                             placeholder="sk-V8V...")
            with gr.Column(scale=0.25, min_width=0):
                model_dropdown = gr.Dropdown(choices=["LLaMA 2", "GPT-3.5 Turbo"],
                                       #value="LLaMA 2", # A bug in gradio
                                       label="Seleccionar modelo"
                                       )


        output_summary = gr.Textbox(label="Breve resumen del documento")#.style(height=100)
        with gr.Column(visible=False) as processing_note:
            gr.Markdown('\n ## <p style="text-align: center;">Procesando PDF...</p>')
            gr.Markdown('<p style="text-align: center;">Esto podría demorar unos minutos.</p>')

        with gr.Column(visible=False) as output_col:
            input_msg = gr.Textbox(label="Preguntar", placeholder="Introducir pregunta y presionar Enter")
            chatbot = gr.Chatbot()
            output_references = gr.components.Textbox(label="Referencias")
            clear_chat_memory = gr.Button(value="Borrar chat")

        # Interactivity
        model_dropdown.input(input_openai_key, [model_dropdown], [input_key, upload_btn, llm_var])
        model_api_textbox.submit(input_model, [model_api_textbox], [input_key, upload_btn, llm_var])                 
        btn.upload(summary, [btn, llm_var], 
                   [output_summary, file_doc, processing_note, llm_var], queue=False).success(
            conversation_vars, [file_doc, llm_var], [memory_var, qa_chain_var, output_col, processing_note]
            )
        input_msg.submit(respond, 
                         [input_msg, chatbot, memory_var, qa_chain_var],
                         [input_msg, response_var, chatbot, memory_var, output_references],
                         queue=False).success(
                             bot, [chatbot, response_var], chatbot
                             )
        clear_chat_memory.click(clear_memory, [memory_var], [memory_var, output_references]).success(
            lambda: None, None, chatbot, queue=False
            )

    with gr.Tab("Acerca de"):
        gr.Markdown("## Autor:\n")
        gr.Markdown("Antonio Jimenez Caballero")

demo.queue(concurrency_count=5,  max_size=10, api_open=False)
demo.launch(server_name="0.0.0.0", server_port=8080)
