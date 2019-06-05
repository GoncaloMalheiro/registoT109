from flask import Flask, render_template, request

app = Flask(__name__)

def gravar(v1, v2, v3):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usr (nome text,email text,pass text)")
    db.execute("INSERT INTO usr VALUES (?, ?, ?)", (v1, v2, v3))
    ficheiro.commit()
    ficheiro.close()

def existe(v1):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE nome =?", (v1,))
    valor = db.fetchone()
    ficheiro.close()
    return valor

def alterar(v1):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("SELECT * INTO usr SET pass = ? WHERE nome =?", (v1))
    valor = 0
    ficheiro.commit()
    ficheiro.close()
    return valor


@app.route('/', methods=['GET', 'POST'])
def route():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['email']
        v3 = request.form['passe']
        v4 = request.form['cpasse']
        if existe(v1):
            erro = 'O Utilizador ja existe.'
        elif v3 != v4:
             erro = 'A palavra passe não coincide.'
        else:
           gravar(v1, v2, v3)
    return render_template('registo.html', erro=erro)

@app.route('/newpass', methods=['GET', 'POST'])
def newpass():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        v3 = request.form['cpasse']
        if v2 != v3:
             erro = 'A palavra passe não coincide.'
        else:
           alterar(v1, v2)
    return render_template('newpass.html', erro=erro)

if __name__=='__main__':
    app.run(debug=True)
