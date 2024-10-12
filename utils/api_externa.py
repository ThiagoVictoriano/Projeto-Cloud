import os
import requests
from fastapi import HTTPException

def consulta_api():
    params = {
        'vs_currency': 'brl',  # Para obter preços em reais
        'order': 'market_cap_desc',  # Ordena por capitalização de mercado
        'per_page': 100,  # Número de resultados por página
        'page': 1,  # Página que deseja consultar
        'sparkline': 'false'  # Não incluir dados de sparkline
    }

    response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params=params)
    
    if response.status_code == 200:
        # Retorna os dados recebidos da API CoinGecko
        return response.json()
    else:
        return {"error": "Não foi possível obter os preços das criptomoedas."}