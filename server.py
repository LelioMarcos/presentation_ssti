from flask import Flask, render_template, render_template_string, request, redirect, url_for
import json

app = Flask(__name__)

@app.route("/")
def root(user=None):
    return "It's working"

# Exemplo de código MUITO inseguro.
@app.route("/produtos")
def search():
    param = request.args.get('search')
    if not param:
        param = ""
        
    template = """
        <html>
            <head>
                <title>Produtos</title>
            </head>
            <body>
                <form method="get">
                    <label for="search">Produto:</label>
                    <input type="text" id="search" name="search"><br>
                    <input type="submit" value="Submit">
                </form>
                <h1>Resultados para """ + param + """</h1>
                <p> Nenhum resultado :(</p>
            </body>
        </html>
    """
    return render_template_string(template)

if __name__ == "__main__":
    app.run(host="0.0.0.0")