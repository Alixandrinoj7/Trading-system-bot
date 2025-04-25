from flask import Flask, render_template, request, redirect, url_for
import os
import random
import telegram

app = Flask(__name__)

# Usuário e senha simulados
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "1234"

# Telegram Bot
TELEGRAM_TOKEN = 'SEU_TOKEN_AQUI'
CHANNEL_ID = '@SEU_CANAL_AQUI'

def enviar_sinal_telegram(sinal):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    mensagem = (
        f"📈 Novo Sinal Gerado!\n"
        f"Par: {sinal['moeda']}\n"
        f"Tipo: {sinal['tipo']}\n"
        f"Expiração: {sinal['expiracao']} min\n"
        f"Preço Entrada: {sinal['preco_entrada']}\n"
        f"Preço Saída: {sinal['preco_saida']}\n"
        f"📊 Assertividade: {sinal['assertividade']}%"
    )
    bot.send_message(chat_id=CHANNEL_ID, text=mensagem)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', erro="Usuário ou senha incorretos.")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    total_sinais = 150
    sinais_positivos = random.randint(80, 120)
    sinais_negativos = total_sinais - sinais_positivos
    assertividade = round((sinais_positivos / total_sinais) * 100, 2)

    sinal = {
        'moeda': 'EUR/USD',
        'tipo': 'PUT',
        'expiracao': 1,
        'preco_entrada': f"{round(random.uniform(1.0900, 1.1000), 4)}",
        'preco_saida': f"{round(random.uniform(1.0900, 1.1000), 4)}",
        'assertividade': assertividade
    }
    enviar_sinal_telegram(sinal)

    return render_template('dashboard.html', total_sinais=total_sinais,
                           sinais_positivos=sinais_positivos,
                           sinais_negativos=sinais_negativos,
                           assertividade=assertividade)

@app.route('/gerar')
def gerar():
    return render_template('gerar.html')

@app.route('/ultimas')
def ultimas():
    return render_template('ultimas.html')

@app.route('/config')
def config():
    return render_template('config.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
