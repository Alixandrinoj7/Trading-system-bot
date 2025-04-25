from flask import Flask, render_template, request, redirect, url_for
import os
import random
import telegram

app = Flask(__name__)

# Usuário e senha simulados
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "1234"

# Configuração do Telegram
TELEGRAM_TOKEN = '7932994002:AAEi9wAKS2gl6dHwezOEbN5pIJUgVwN8LbA'
CHANNEL_ID = '5404730148'

def enviar_sinal_telegram(sinal):
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        mensagem = (
            f"🔔 Novo Sinal de Entrada\n"
            f"🪙 Par: {sinal['moeda']}\n"
            f"📈 Tipo: {sinal['tipo']}\n"
            f"⏱ Expiração: {sinal['expiracao']}min\n"
            f"🎯 Entrada: {sinal['preco_entrada']}\n"
            f"💰 Saída: {sinal['preco_saida']}\n"
            f"📊 Assertividade: {sinal['assertividade']}%"
        )
        bot.send_message(chat_id=CHANNEL_ID, text=mensagem)
    except Exception as e:
        print(f"Erro ao enviar sinal: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
            return redirect(url_for('home'))
        else:
            return render_template('login.html', erro="Usuário ou senha incorretos.")
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    total_sinais = 150
    sinais_positivos = random.randint(80, 120)
    sinais_negativos = total_sinais - sinais_positivos
    assertividade = round((sinais_positivos / total_sinais) * 100, 2)

    # Gerar sinal
    sinal = {
        'moeda': 'EUR/USD',
        'tipo': 'Call',
        'expiracao': 1,
        'preco_entrada': '1.0910',
        'preco_saida': '1.0925',
        'assertividade': assertividade
    }

    enviar_sinal_telegram(sinal)

    return render_template(
        'dashboard.html',
        total_sinais=total_sinais,
        sinais_positivos=sinais_positivos,
        sinais_negativos=sinais_negativos,
        assertividade=assertividade
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))