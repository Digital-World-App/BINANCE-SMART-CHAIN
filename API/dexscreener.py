import json
import requests

url = 'https://api.dexscreener.io/latest/dex/tokens/0x0697AB2B003FD2Cbaea2dF1ef9b404E45bE59d4C'

response = requests.get(url)

if response.status_code == 200:
    data = json.loads(response.text)

    # Itera sobre os pares de tokens e imprime informações
    for pair in data['pairs']:
        print("Chain:", pair['chainId'])
        print("Exchange:", pair['dexId'])
        print("Pair URL:", pair['url'])
        print("Pair Address:", pair['pairAddress'])
        print("Base Token:", pair['baseToken']['symbol'], "-", pair['baseToken']['name'])
        print("Quote Token:", pair['quoteToken']['symbol'], "-", pair['quoteToken']['name'])
        print("Price (Native):", pair['priceNative'])
        print("Price (USD):", pair['priceUsd'])
        print("Price Change (last 5m):", pair['priceChange']['m5'])
        print("Price Change (last 1h):", pair['priceChange']['h1'])
        print("Price Change (last 6h):", pair['priceChange']['h6'])
        print("Price Change (last 24h):", pair['priceChange']['h24'])
        print("Transactions (last 24h):", pair['txns']['h24']['buys'], "buys,", pair['txns']['h24']['sells'], "sells")
        print("Volume (last 24h):", pair['volume']['h24'])
        print("Liquidity (USD):", pair['liquidity']['usd'])
        print("Liquidity (Base):", pair['liquidity']['base'])
        print("Liquidity (Quote):", pair['liquidity']['quote'])
        print("FDV:", pair['fdv'])
        print("Pair Created At:", pair['pairCreatedAt'])
        print("\n")
else:
    print('Error:', response.status_code)
