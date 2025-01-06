import requests
from typing import List, Dict, Optional
import logging

# Configuração do log
logging.basicConfig(level=logging.INFO)

def get_market_data(ids: List[str]) -> Optional[List[Dict]]:
    """
    Obtém dados de mercado das criptomoedas especificadas da API da CoinGecko.

    Args:
        ids (list): Lista de ids das criptomoedas que se deseja obter os dados.

    Returns:
        list: Lista contendo os dados de mercado das criptomoedas especificadas.
              Se ocorrer um erro na solicitação ou se a resposta não for válida, retorna None.
    """
    # Limite de criptomoedas por requisição
    per_page = min(len(ids), 100)
    
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ",".join(ids),
        "order": "market_cap_desc",
        "per_page": str(per_page),
        "page": "1",
        "sparkline": "false",
        "price_change_percentage": "1h,24h,7d"
    }
    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Verifica se houve erro na requisição

        # Se a resposta for bem-sucedida, retorna os dados em formato de lista
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na requisição: {e}")
        return None
    except ValueError as e:
        logging.error(f"Erro ao processar os dados JSON: {e}")
        return None

def format_market_data(data: Dict) -> str:
    """
    Formata os dados de mercado em uma string legível.

    Args:
        data (dict): Dados de mercado obtidos da API da CoinGecko.

    Returns:
        str: Dados de mercado formatados como uma string legível.
    """
    # Verificação de campos presentes nos dados antes de formatar
    ath_date = data.get('ath_date', 'N/A')
    atl_date = data.get('atl_date', 'N/A')

    formatted_data = f"""
ID: {data['id']}
Nome: {data['name']}
Símbolo: {data['symbol']}
Preço Atual: ${data['current_price']:.2f}
Market Cap: ${data['market_cap']:,}
Rank de Market Cap: {data['market_cap_rank']}
Volume Total (24h): ${data['total_volume']:,}
Variação de Preço (24h): {data['price_change_percentage_24h']:.2f}%
ATH (All-Time High): ${data['ath']:.2f} ({ath_date})
ATL (All-Time Low): ${data['atl']:.2f} ({atl_date})
Última Atualização: {data['last_updated']}
"""
    return formatted_data

# Lista de ids das criptomoedas desejadas
crypto_ids = ["bitcoin", "binancecoin", "ethereum", "Shentu", "filecoin", "trust-wallet-token"]

# Exemplo de uso:
market_data = get_market_data(crypto_ids)
if market_data:
    logging.info("Dados das criptomoedas:")
    for data in market_data:
        print(format_market_data(data))
else:
    logging.error("Falha ao obter dados das criptomoedas.")
