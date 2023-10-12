sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'
print(sdw2023_api_url)

import pandas as pd

df = pd.read_csv('usuarios.csv')

user_ids = df['UserID'].tolist()

print(user_ids)

# Requisitando banco de dados externos
import requests
import json

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]

# Transformando os dados com CHATGPT
# Instalando o api da openai
#!pip install openai

import yfinance as yf

def generate_ai_news(user):
  # Obter dados históricos do produto de investimento
  product = user['product']
  def get_historical_data(ticker, start_date, end_date):
    return yf.download(ticker, start_date, end_date)
  df = get_historical_data(product, '2022-01-01', '2023-07-20')

  # Gerar recomendação de investimento
  return f"Olá {user['name']}, aqui está uma dica de investimento para você: invista em {product}. O retorno anual do produto foi de {df['Close'].pct_change(12).mean() * 100}% nos últimos 12 meses."


for user in users:
  news = generate_ai_news(user)
  print(news)

# Adicionar a notícia ao usuário
# Corrigindo o erro de sintaxe
user['news'].append({
    "icon": "https://github.com/digitalinnovationone/santander-dev-week-2023-api/blob/665804c8231b32923b03b30ab832ccee33cf2cc3/docs/icons/credit.svg",
    "description": news
})

### LOAD dos dados
def update_user(user):
  response = requests.put(f'{sdw2023_api_url}/users/{user["id"]}', json=user)
  return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}")
