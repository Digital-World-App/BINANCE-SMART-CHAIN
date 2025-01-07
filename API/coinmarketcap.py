import os
from requests import Session
from requests.exceptions import RequestException
from dotenv import load_dotenv
import time

class CoinMarketCapAPI:
    def __init__(self):
        load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
        self.api_key = os.getenv('COINMARKETCAP_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Please set COINMARKETCAP_API_KEY in .env file.")

    def establish_connection(self, endpoint, params=None):
        url = f'https://pro-api.coinmarketcap.com{endpoint}'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=params)
            response.raise_for_status()  # Raises exception for HTTP errors
            print(f"Conexão bem-sucedida com {endpoint}! Status:", response.status_code)
            time.sleep(5)  # Espera por 5 segundos
            return response.json()
        except RequestException as e:
            print("Erro ao conectar-se à API:", e)
            return None

    def get_latest_market_pairs(self, start=1, limit=5, convert='USD'):
        params = {
            'start': start,
            'limit': limit,
        }
        if convert:
            params['convert'] = convert
        return self.establish_connection('/v1/cryptocurrency/listings/latest', params=params)

    def get_crypto_map(self, start=1, limit=5, convert=None):
        params = {
            'start': start,
            'limit': limit,
        }
        return self.establish_connection('/v1/cryptocurrency/map', params=params)

    def get_crypto_categories(self, start=1, limit=5, convert=None):
        params = {
            'start': start,
            'limit': limit,
        }
        return self.establish_connection('/v1/cryptocurrency/categories', params=params)


    def format_crypto_data(self, data):
        formatted_data = {}
        for currency in data['data']:
            name = currency['name']
            symbol = currency['symbol']
            price = currency['quote']['EUR']['price']
            volume_24h = currency['quote']['EUR']['volume_24h']
            percent_change_1h = currency['quote']['EUR']['percent_change_1h']
            percent_change_24h = currency['quote']['EUR']['percent_change_24h']
            percent_change_7d = currency['quote']['EUR']['percent_change_7d']
            market_cap = currency['quote']['EUR']['market_cap']
            formatted_data[name] = {
                'Preço em EUR': price,
                'Volume em 24h': volume_24h,
                'Variação em 1h': percent_change_1h,
                'Variação em 24h': percent_change_24h,
                'Variação em 7d': percent_change_7d,
                'Capitalização de Mercado': market_cap
            }
        return formatted_data


    
if __name__ == "__main__":
    coinmarketcap_api = CoinMarketCapAPI()
    
    # Consulta aos endpoints
    latest_market_pairs = coinmarketcap_api.get_latest_market_pairs(convert='EUR')
    crypto_map = coinmarketcap_api.get_crypto_map()
    crypto_categories = coinmarketcap_api.get_crypto_categories()
    
    # Formatando e imprimindo os resultados
    if latest_market_pairs:
        formatted_data = coinmarketcap_api.format_crypto_data(latest_market_pairs)
        print("Resultados da consulta - Últimos Pares de Mercado:")
        for currency, info in formatted_data.items():
            print(f"{currency}:")
            for key, value in info.items():
                print(f"- {key}: {value}")
            print()
    else:
        print("Falha ao obter dados mais recentes do mercado.")
        
    if crypto_map:
        print("Resultados da consulta - Mapa de Criptomoedas:")
        for currency in crypto_map['data']:
            name = currency['name']
            rank = currency['rank']
            is_active = "Sim" if currency['is_active'] else "Não"
            first_historical_data = currency['first_historical_data']
            last_historical_data = currency['last_historical_data']
            print(f"- {name} ({currency['symbol']}):")
            print(f"  - Rank: {rank}")
            print(f"  - Ativo: {is_active}")
            print(f"  - Primeiros dados históricos: {first_historical_data}")
            print(f"  - Últimos dados históricos: {last_historical_data}")
            print()
    else:
        print("Falha ao obter o mapa de criptomoedas.")
        

    if crypto_categories:
        print("Resultados da consulta - Categorias de Criptomoedas:")
        for category in crypto_categories['data']:
            print(f"- {category['name']} ({category['title']}):")
            print(f"  - Descrição: {category['description']}")
            print(f"  - Número de tokens: {category['num_tokens']}")
            print(f"  - Variação média de preço: {category['avg_price_change']:.2f}%")
            print(f"  - Capitalização de mercado: ${category['market_cap']:.2f}")
            print(f"  - Variação na capitalização de mercado: {category['market_cap_change']:.2f}%")
            print(f"  - Volume em 24h: ${category['volume']:.2f}")
            print(f"  - Variação no volume em 24h: {category['volume_change']:.2f}%")
            print(f"  - Última atualização: {category['last_updated']}")
            print()
    else:
        print("Falha ao obter as categorias de criptomoedas.")

