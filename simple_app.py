import gradio as gr
import random
import time
from src import LLM_gradioAPI
from src import topics_from_pdf
from src import qa_convertational_chain_function
from langchain.memory import ConversationBufferMemory

# Define the LLM endpoint
llm = LLM_gradioAPI(n=2000) # hugging face repo
llm.client_api = "https://ysharma-explore-llamav2-with-tgi.hf.space/"
llm.api_name = "/chat_1"

css = """
footer {visibility: hidden}
.feedback textarea {font-size: 40px !important} 
"""

with gr.Blocks(css=css) as demo:

    # Variables
    file_doc = gr.State()
    qa_chain_var = gr.State()
    memory_var = gr.State()

    # Functions
    def summary(file):
        num_topics = 3
        words_per_topic = 30 # optimizar
        file = file.name

        topics = topics_from_pdf(llm, file, num_topics, words_per_topic)
        return {
            output_summary : topics,
            file_doc : file,
            processing_note: gr.update(visible=True)
        }
    
    def conversation_vars(file):
        chain_type = "stuff"
        retreiver_search_type = "mmr"
        retreiver_k = 5
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        qa_chain = qa_convertational_chain_function(file, llm, chain_type, retreiver_search_type, retreiver_k)
        return {
            memory_var : memory, 
            qa_chain_var : qa_chain,
            output_col : gr.update(visible=True),
            processing_note: gr.update(visible=False)
            }
    
    def respond(query, chat_history, memory, qa_chain):
        result = qa_chain({
            "question": query,
            "chat_history" : memory.load_memory_variables({})["chat_history"]
            })
        response = result["answer"]
        source_docs = result["source_documents"]
        memory.save_context({"input": query}, {"output": response})

        bot_message = response
        chat_history.append((query, bot_message))
        references = "\n".join(["\nPágina no. " + str(doc.metadata["page"]) + "\n" + doc.page_content[:150] + "..." for doc in source_docs])

        time.sleep(2)
        return {
            msg : "", 
            chatbot : chat_history, 
            memory_var : memory,
            output_references : references
        }
    
    def clear_memory(memory):
        #print(memory)
        memory.clear()
        #print(memory)
        return {
            memory_var : memory,
            output_references : ""
        }

    # Layout
    gr.Markdown("\n")
    gr.Markdown('\n # <p style="text-align: center;">Pregunta al PDF</p>')
    gr.Markdown("\n")

    with gr.Tab("Inicio"):
        btn = gr.UploadButton("Subir pdf 📁", file_types=["document"])
        output_summary = gr.components.Textbox(label="Breve resumen del documento").style(height=100)

        with gr.Column(visible=True) as processing_note:
            gr.Markdown('\n ## <p style="text-align: center;">Procesando PDF...</p>')
            gr.Markdown('<p style="text-align: center;">Esto podría demorar unos minutos.</p>')

        with gr.Column(visible=True) as output_col:
            msg = gr.Textbox(label="Preguntar", placeholder="Introducir pregunta")
            chatbot = gr.Chatbot()
            output_references = gr.components.Textbox(label="Referencias")

            clear_chat_memory = gr.Button(value="Borrar chat")

        btn.upload(summary, [btn], [output_summary, file_doc, processing_note], 
                        queue=False).success(conversation_vars, inputs=[file_doc], 
                                        outputs=[memory_var, qa_chain_var, output_col, processing_note])
        msg.submit(respond, [msg, chatbot, memory_var, qa_chain_var], 
                   [msg, chatbot, memory_var, output_references])
        clear_chat_memory.click(clear_memory, inputs=[memory_var], outputs=[memory_var, output_references]).success(
            lambda: None, None, chatbot, queue=False)

    with gr.Tab("Acerca de"):
        gr.Markdown("Some description")

demo.launch()
