from flask import Flask, render_template, request, redirect, url_for
import os
import random
from telegram import Bot

app = Flask(__name__)

# Credenciais
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "1234"

# Token e canal do Telegram via variáveis de ambiente
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "SEU_TOKEN_AQUI")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@SEU_CANAL_AQUI")

def enviar_sinal_telegram(sinal):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
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
    except Exception as e:
        print(f"[ERRO] Falha ao enviar para Telegram: {e}")

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

    base = round(random.uniform(1.0900, 1.1000), 4)
    variacao = round(random.uniform(0.0005, 0.0015), 4)

    preco_entrada = round(base, 4)
    preco_saida = round(base + variacao, 4)

    sinal = {
        'moeda': 'EUR/USD',
        'tipo': 'PUT',
        'expiracao': 1,
        'preco_entrada': preco_entrada,
        'preco_saida': preco_saida,
        'assertividade': assertividade
    }

    enviar_sinal_telegram(sinal)

    return render_template('dashboard.html',
                           total_sinais=total_sinais,
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