import requests

def get_pair_details(exchange_slug, chain_slug, pair_slug):
    url = "https://tradingstrategy.ai/api/pair-details"
    params = {
        "exchange_slug": exchange_slug,
        "chain_slug": chain_slug,
        "pair_slug": pair_slug
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lança uma exceção para erros HTTP

        pair_details = response.json()
        return pair_details

    except requests.exceptions.HTTPError as err:
        print(f"Erro HTTP ao obter informações do par de negociação: {err}")
        return None

    except Exception as err:
        print(f"Ocorreu um erro ao processar a solicitação: {err}")
        return None

def print_pair_details(pair_details):
    if pair_details:
        summary = pair_details['summary']
        print("Detalhes do par de negociação:")
        print(f"Nome: {summary['pair_name']}")
        print(f"Símbolo: {summary['pair_symbol']}")
        print(f"Preço USD: {summary['usd_price_latest']}")
        print(f"Volume USD 24h: {summary['usd_volume_24h']}")
        print(f"Liquidez USD: {summary['usd_liquidity_latest']}")
        print(f"Taxa de swap: {summary['pair_swap_fee']}")
        print(f"Taxa de pool: {summary['pool_swap_fee']}")
        print(f"TVL: {summary['pair_tvl']}")
        print(f"Última atualização: {summary['pair_tvl_last_updated']}")
    else:
        print("Não foi possível obter informações para este par.")

# Lista de pares que deseja consultar
pairs = [
    {"exchange_slug": "pancakeswap-v2", "chain_slug": "binance", "pair_slug": "asppbr-usdt"} 
]

# Itera sobre cada par e obtém os detalhes
for pair in pairs:
    exchange_slug = pair["exchange_slug"]
    chain_slug = pair["chain_slug"]
    pair_slug = pair["pair_slug"]

    print(f"\nObtendo detalhes para o par: {pair_slug.upper()}")
    pair_details = get_pair_details(exchange_slug, chain_slug, pair_slug)
    print_pair_details(pair_details)
