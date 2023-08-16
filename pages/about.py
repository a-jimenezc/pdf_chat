import gradio as gr

intro_html = """
<html>
<body>
    <p>
        Esta app permite hacer preguntas a documentos en formato PDF. \
        Funciona con documentos de diez páginas, así como con libros de más \
        de mil páginas. Esto es posible gracias al uso de tecnologías tales \
        como los Grandes Modelos de Lenguaje (LLM por sus siglas en inglés), \
        Bases de Datos Vectoriales, entre otras. Adicionalmente, se genera un índice \
        basado en el contenido del documento, esto con el fin de resumir el contenido \
        del mismo.
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
        Hola, soy Antonio Jimenez y soy un entusiasta de usar la ciencia \
        de datos para resolver problemas. En mi Github encontrarás otros \
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

