import gradio as gr

openai_key_html = """
<html>
<body>
    <p>
        La "API key" se almacena de forma temporal mientras dure la sesión y se
        limita a brindar la funcionalidad a la página. Una vez cerrada o actualizada la ventana
        del navegador, esta información se elimina. Además, su uso se limita a la sesión del usuario
        que la ingresó.
        <br>
        <br>
        Adicionalmente, se implementaron optimizaciones para limitar
        su uso, dado el costo que representa. Por ejemplo, para resumir el documento, 
        primero este se preprocesa en nuestros servidores con algoritmos de texto. 
        Una vez se extrae la información clave, solo hace falta una única llamada a gpt 3.5 
        mediante el uso de la "API key" para estructurar la información en lenguaje natural y 
        presentar el resumen en forma de índice. Otra forma de limitar las llamadas a la "API" de 
        OpenAi es mediante el uso de un modelo generador de "Embeddings" instalado en nuestros
        servidores. Estos "Embeddings" son vectores que representan a los párrafos de texto y son 
        esenciales para el chat. De esta forma se hace innecesario el uso de los "Embeddings" de
        OpenAi, haciendo factible trabajar con documentos muy extensos sin incurrir en costos adicionales. 
        <br>
        <br>
        Para obtener solicitar una "api key" ingresar a 
        <a href="https://platform.openai.com/account/billing/overview">"OpenAi, start payment plan"</a>.
        Una vez establecida la cuenta de pago, se puede solicitar la "api key" en 
        <a href="https://platform.openai.com/account/api-keys">"OpenAi, API keys."</a>.
        Finalmente, se recomienda establecer un limite fijo para no incurrir en costos inadvertidos. Para
        ello se puede ingresar a 
        <a href="https://platform.openai.com/account/billing/limits">"OpenAi, Usage limits."</a>.
        <br>
        <br>
        OpenAi recomienda no compartir esta información debido al costo que en que puede incurrir.
        Sin embargo, y repitiendo la nota inicial, esta aplicación usa este valor de forma temporal,
        mientras dure su sesión. Cada ventana en que se abre la aplicación, es una sesión diferente, incluso
        usando el mismo navegador.
    </p>
</body>
</html>
"""

intro_html = """
<html>
<body>
    <p>
        Esta app permite hacer preguntas a documentos en formato PDF y
        funciona con documentos de diez páginas, así como con libros de más
        de mil páginas. Esto es posible gracias al uso de
        los Grandes Modelos de Lenguaje (LLM por sus siglas en inglés),
        Bases de Datos Vectoriales y algoritmos de procesamiento de texto.
        Así mismo, la app genera un índice
        basado en el contenido del documento, el cual ofrece una guía al momento de
        hacer preguntas. Adicionalmente, la app entrega los extractos del documento en los cuales
        basó su respuesta. Esto es muy útil en caso de necesitar validar la respuesta dada por el modelo.
    </p>
</body>
</html>
"""

author_html = """
<html>
<head>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
  </style>
</head>

<body>
    <h2 style="text-align: center;">
        Sobre el Autor:
    </h2>
    <p>
        Hola, soy Antonio Jimenez y soy un entusiasta de usar la ciencia
        de datos para resolver problemas. En mi Github encontrarás otros
        proyectos en los que estuve trabajando.
    </p>

    <h4 style="text-align: center;">
        <a href="https://github.com/a-jimenezc">
            <i class="fab fa-github"></i> 
            GitHub
        </a>
        &nbsp &nbsp &nbsp &nbsp
        <a href="https://www.linkedin.com/in/antonio-jimnzc">
            <i class="fab fa-linkedin linkedin-icon"></i> 
            Linkedin
        </a>
    </h4>

</body>
</html>
"""

