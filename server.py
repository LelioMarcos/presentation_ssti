from flask import Flask, render_template, render_template_string, request

app = Flask(__name__)
seguro = "nao"

@app.route("/")
def root(user=None):
    return "It's working"

@app.route("/<user>")
def hello_world(user=None):
    return render_template('index.html', user=user)

# SSTI sem concatenação
@app.route("/insecure/<user>")
def hello_world_insecure(user=None):
    return render_template('index.html', user=render_template_string(user))

# Exemplo de código MUITO inseguro.
@app.route("/produtos")
def search():
    param = request.args.get('search') or None
    template = """
        <html>
            <head>
                <title>Produtos</title>
            </head>
            <body>
                <h1>Resultados para """ + param + """</h1>
                <p> Nenhum resultado :(</p>
            </body>
        </html>
    """
    return render_template_string(template)
