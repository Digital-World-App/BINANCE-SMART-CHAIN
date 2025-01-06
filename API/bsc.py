import requests
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Função para obter a chave da API de uma variável de ambiente
def get_api_key():
    api_key = os.getenv('BSC_API_KEY')  # Alterado para corresponder ao nome da variável no .env
    if not api_key:
        raise Exception("BSC_API_KEY não encontrada. Defina a variável de ambiente BSC_API_KEY no arquivo .env.")
    print(f"BSC_API_KEY carregada: {api_key}")  # Depuração para verificar o valor carregado
    return api_key

# Função para verificar a resposta da API
def check_response(response):
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar API: {response.status_code}")
    data = response.json()
    if 'result' not in data:
        raise Exception("Resultado não encontrado na resposta da API.")
    return data

def get_gas_price(api_key):
    url = f"https://api.bscscan.com/api?module=proxy&action=eth_gasPrice&apikey={api_key}"
    response = requests.get(url)
    data = check_response(response)
    return int(data['result'], 16)

def estimate_gas(api_key, data, to, value, gas_price, gas):
    url = f"https://api.bscscan.com/api?module=proxy&action=eth_estimateGas&data={data}&to={to}&value={value}&gasPrice={gas_price}&gas={gas}&apikey={api_key}"
    response = requests.get(url)
    data = check_response(response)
    return int(data['result'], 16)


def get_gas_price_usd(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    response = requests.get(url)
    
    # Verificar se a resposta da API é válida
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar a API do CoinGecko: {response.status_code}")
    
    data = response.json()
    
    # Verificar se a chave 'usd' está presente na resposta
    if crypto_id not in data or 'usd' not in data[crypto_id]:
        raise Exception(f"Preço do {crypto_id} em USD não encontrado na resposta da API.")
    
    return data[crypto_id]['usd']


def get_eth_block_number(api_key):
    url = f"https://api.bscscan.com/api?module=proxy&action=eth_blockNumber&apikey={api_key}"
    response = requests.get(url)
    data = check_response(response)
    return int(data['result'], 16)

def get_gas_oracle(api_key):
    url = f"https://api.bscscan.com/api?module=gastracker&action=gasoracle&apikey={api_key}"
    response = requests.get(url)
    data = check_response(response)
    return data['result']

def get_bnb_supply(api_key):
    url = f"https://api.bscscan.com/api?module=stats&action=bnbsupply&apikey={api_key}"
    response = requests.get(url)
    data = check_response(response)
    return data['result']

def get_bnb_price(api_key):
    url = f"https://api.bscscan.com/api?module=stats&action=bnbprice&apikey={api_key}"
    response = requests.get(url)
    data = check_response(response)
    return data['result']

# Função para formatar números com zeros à esquerda
def format_with_zeros(number, decimals=10):
    return f"{number:.{decimals}f}"

# Carregar a chave da API de uma variável de ambiente
bsc_api_key = get_api_key()

# Obter o preço atual do BNB em BTC e USD
bnb_price_info = get_bnb_price(bsc_api_key)
print("Preço Atual do BNB (em BTC):", format_with_zeros(float(bnb_price_info['ethbtc'])))
print("Preço Atual do BNB (em USD):", format_with_zeros(float(bnb_price_info['ethusd'])))

# Obter o fornecimento total de BNB
bnb_supply_info = get_bnb_supply(bsc_api_key)
print("Fornecimento Total de BNB:", bnb_supply_info)

# Obter o último bloco processado pelo Oráculo de Gás
gas_oracle_info = get_gas_oracle(bsc_api_key)
print("Último Bloco Processado pelo Oráculo de Gás:", gas_oracle_info['LastBlock'])

# Obter o número do bloco Ethereum
eth_block_number = get_eth_block_number(bsc_api_key)
print("Número do Bloco:", eth_block_number)

# Obter o preço do gás em wei e convertê-lo para USD e BNB
gas_price_wei = get_gas_price(bsc_api_key)
gas_price_usd = gas_price_wei * (get_gas_price_usd("ethereum") / 10**18)
gas_price_bnb = gas_price_wei * (get_gas_price_usd("binancecoin") / 10**18)

print("Preço do Gás (em Wei):", gas_price_wei)
print("Preço do Gás (em USD):", format_with_zeros(gas_price_usd))
print("Preço do Gás (em BNB):", format_with_zeros(gas_price_bnb))

# Exemplo de dados para estimativa de gás
data = "0x4e71d92d"
to = "0xEeee7341f206302f2216e39D715B96D8C6901A1C"
value = "0xff22"
gas_price = "0x51da038cc"
gas = "0x5f5e0ff"

# Obter o gas estimado e convertê-lo para USD e BNB
estimated_gas_wei = estimate_gas(bsc_api_key, data, to, value, gas_price, gas)

print("Gas Estimado (em Wei):", estimated_gas_wei)
