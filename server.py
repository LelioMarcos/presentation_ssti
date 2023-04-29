from flask import Flask, render_template, render_template_string, request, redirect, url_for
import json

app = Flask(__name__)

notes = {
    "lelio": ["fui ao mercado hoje", "mercado:\nsuco\nrefri\nmiojo"],
    "angus": ["senha do banco: GANESH\{tempalte_injection\}"]
}

session = {}

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

@app.route("/messages", methods=['GET', 'POST'])
def messages():
    if session and session['username']:
        print(notes[session['username']])

        templates = []
        
        for message in notes[session['username']]:
            templates.append(render_template_string(message))

        templates.reverse()

        return render_template('passwords.html', user=session['username'], messages=templates)
    
    return redirect('/login')

# Criar rota de adicionar
@app.route("/messages/add", methods=["POST"])
def add_message():
    if session['username']:
        if request.form['message']:
            notes[session['username']].append(request.form['message'])

            return redirect(url_for('messages'))

        return "Faltam parâmetros"

    return redirect('/login')



@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        f = open("usuarios.json")
        data = json.load(f)
        f.close()
        for i in range(len(data)):
            if data[i]["username"] == request.form['username']:
                if data[i]["password"] == request.form['password']:
                    session['username'] = data[i]["username"]
                    return redirect('/messages')
                else: 
                    return "Erro ao logar"
                break
    else:
        return render_template('login.html')
        

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

if __name__ == "__main__":
    app.run(host="0.0.0.0")