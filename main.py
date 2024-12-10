
from flask import Flask, render_template, request  # Corrigir a importação
from dotenv import load_dotenv
import google.generativeai as genai
import os
import json

load_dotenv()

# Configurar a API uma única vez
genai.configure(api_key=os.getenv('API'))
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)


vinhos = [
    {
    "nome": "MIOLO RESERVA PINOT GRIGIO",
    "id": 1,
    "tipo": "Branco",
    "regiao": "Alentejo",
    "safra": 2020,
    "preco": 75.30,
    "imagem": "static/img/branco.png"
    },
    {
    "nome": "Mesa Suave Vinhedos do Vale",
    "id": 2,
    "tipo": "Rosé",
    "regiao": "Provence",
    "safra": 2018,
    "preco": 90.00,
    "imagem": "static/img/rose.png"
    },
    {
    "nome": "Fino Rosé Moscatel",
    "id": 3,
    "tipo": "Espumante",
    "regiao": "Champagne",
    "safra": 2012,
    "preco": 250.00,
    "imagem": "static/img/espumante.png"
    },
    {
    "nome": "Poças Porto Tawny",
    "id": 4,
    "tipo": "Fortificado",
    "regiao": "Porto",
    "safra": 2010,
    "preco": 180.00,
    "imagem": "static/img/fortificado.png"
    },
    {
    "nome": "Tokaji Aszu",
    "id": 5,
    "tipo": "Sobremesa",
    "regiao": "Tokaji",
    "safra": 2016,
    "preco": 130.00,
    "imagem": "static/img/doce.png"
    },
    {
    "nome": "Santa Julia La Oveja Torrontés",
    "id": 6,
    "tipo": "Natural",
    "regiao": "Catalunha",
    "safra": 2019,
    "preco": 110.00,
    "imagem": "static/img/natural.png"
    },
    {
    "nome": "Bordo Seco De Cezaro",
    "id": 7,
    "tipo": "Orgânico",
    "regiao": "Toscana",
    "safra": 2021,
    "preco": 95.00,
    "imagem": "static/img/organico.png"
    },
    {
    "nome": "Casa Navaronne Meio Seco",
    "id": 8,
    "tipo": "Sem álcool",
    "regiao": "Califórnia",
    "safra": 2023,
    "preco": 50.00,
    "imagem": "static/img/sem alcool.png"
    },
]

@app.route('/search')
def search():
    context = ('Você é um bot de vinhos diversos a serviço da empresa Divinno, seu nome é Divinnobot, sua'
               'únia e exclusiva função é fazer com que os clientes descubram qual o melhor tipo de vinho'
               'para as mais demasiadas ocasiões. Apenas responda questões relacionadas à Divinno e sobre'
               'os tipos de vinhos oferecidos.')

    prompt = request.args.get('prompt')
    if not prompt:
        return {'message': 'Desculpe, não consegui entender sua pergunta. Pode tentar novamente?'}

    input_ia = f'{context}: {prompt}'
    try:
        output = model.generate_content(input_ia)
        return {'message': output.text}  # Retorna a resposta do modelo
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        return {'message': 'Desculpe, houve um erro ao processar sua solicitação.'}
@app.route("/")
def inicial():
    return render_template("index.html")

@app.route("/cardapio")
def cardapio():
    return render_template("cardapio.html", vinhos=vinhos)

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/vinho/<int:vinho_id>")
def vinho_detalhado(vinho_id):
    if vinho_id < len(vinhos):
        vinho = vinhos[vinho_id]
        return render_template("produto.html", vinho=vinho)
    else:
        return "Vinho não encontrado", 404

@app.route("/chat")
def chat():
    return render_template("chat.html")

if __name__ == '__main__':
    app.run(debug=True)
