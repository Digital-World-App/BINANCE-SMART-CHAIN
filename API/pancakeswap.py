import requests
import json
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave API do arquivo .env
pancakeswap_api_key = os.getenv("PANCAKESWAP_API_KEY")

# Verifica se a chave foi carregada corretamente
if not pancakeswap_api_key:
    raise ValueError("Chave da API não encontrada no arquivo .env")

# URL da API GraphQL
url = f"https://open-platform.nodereal.io/{pancakeswap_api_key}/pancakeswap-free/graphql"

# Função para fazer uma consulta GraphQL com tratamento de exceções
def make_graphql_query(query):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + pancakeswap_api_key
    }
    
    try:
        response = requests.post(url, json={"query": query}, headers=headers)
        response.raise_for_status()  # Verifica se houve erro na requisição HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

# Função para consultar dados de pares de tokens com verificação robusta
def get_pair_data(pair_address):
    query = '''
    {{
      pairDayDatas(
        first: 1
        skip: 0
        where: {{
          date_gt: 1659312000
          pairAddress: "{}"
        }}
      ) {{
        pairAddress {{
          id
          name
        }}
        date
        dailyVolumeUSD
        dailyTxns
        dailyVolumeToken0
        dailyVolumeToken1
        reserve0
        reserve1
        reserveUSD
        totalSupply
      }}
    }}
    '''.format(pair_address)
    
    result = make_graphql_query(query)
    if result and 'data' in result and 'pairDayDatas' in result['data'] and result['data']['pairDayDatas']:
        return result['data']['pairDayDatas'][0]
    else:
        print(f"Erro na consulta para o par de tokens: {pair_address}")
        return None

# Função para calcular o TVL
def calculate_tvl(reserve_usd):
    return float(reserve_usd) if reserve_usd else 0.0

# Função para calcular o valor unitário de cada token
def calcular_valor_unitario(tvl_total, total_tokens):
    return tvl_total / total_tokens if total_tokens else 0.0

# Função para calcular o valor de mercado total dos tokens ASPPBR
def calcular_valor_mercado(valor_unitario, total_tokens):
    return valor_unitario * total_tokens if total_tokens else 0.0

# Função para calcular o valor total da reserva do token ASPPBR
def calculate_total_asppbr_reserve(pair_addresses):
    total_reserve = 0
    for pair_address, _ in pair_addresses:
        pair_data = get_pair_data(pair_address)
        if pair_data is not None:
            total_reserve += float(pair_data['reserve0'])  # Supondo que reserve0 é o ASPPBR
    return total_reserve

# Função para calcular o valor unitário e o valor de mercado do token ASPPBR
def calcular_valor_unitario_e_mercado(pair_addresses):
    total_tvl = 0
    total_tokens_asppbr = 0
    total_supply_asppbr = 21_000_000  # Total de tokens fixos

    for pair_address, token_name in pair_addresses:
        pair_data = get_pair_data(pair_address)
        if pair_data is None:
            continue
        
        # Calcula e acumula o TVL total
        total_tvl += float(pair_data['reserveUSD'])
        
        # Acumula o total de tokens ASPPBR
        total_tokens_asppbr += float(pair_data['reserve0'])  # Assumindo que reserve0 é a reserva do token ASPPBR

        # Imprime informações sobre o par de tokens
        print(f"### Par de Tokens: ASPPBR-{token_name}")
        print(f"- Endereço do Par: {pair_address}")
        print(f"- Data: {pair_data['date']}")
        print(f"- Volume Diário em USD: ${float(pair_data['dailyVolumeUSD']):,.2f}")
        print(f"- Transações Diárias: {pair_data['dailyTxns']}")
        print(f"- Volume Diário do Token ASPPBR: {float(pair_data['dailyVolumeToken0']):,.2f}")
        print(f"- Volume Diário do Token {token_name}: {float(pair_data['dailyVolumeToken1']):,.2f}")
        print(f"- Reserva do Token ASPPBR: {float(pair_data['reserve0']):,.2f}")
        print(f"- Reserva do Token {token_name}: {float(pair_data['reserve1']):,.2f}")
        print(f"- Reserva Total em USD: ${float(pair_data['reserveUSD']):,.2f}")
        print(f"- Total de Suprimento: {float(pair_data['totalSupply']):,.2f}")
        
        # Calcula e imprime o TVL
        tvl = calculate_tvl(pair_data['reserveUSD'])
        print(f"- TVL: ${tvl:,.2f}")
        print()

    # Calcula o valor unitário
    valor_unitario = calcular_valor_unitario(total_tvl, total_tokens_asppbr)
    
    # Calcula o valor de mercado total dos tokens ASPPBR
    valor_mercado_total = calcular_valor_mercado(valor_unitario, total_supply_asppbr)
    
    # Calcula o total da reserva de token ASPPBR
    total_asppbr_reserve = calculate_total_asppbr_reserve(pair_addresses)
    
    return valor_unitario, valor_mercado_total, total_tvl, total_tokens_asppbr, total_asppbr_reserve

# Lista de endereços de pares de tokens para consultar
pair_addresses = [
    ("0xB9a2b08Be15dC15e531b0d25B3942268DA27B100", "WBNB"),   # WBNB
    ("0x3DAc89C0C868eb9F835D97E1FDb702b6fD6Ae38E", "CTK"),   # CTK
    ("0x60825783086bbEbbF0C83129e88c69914ad17073", "TWT"),   # TWT
    ("0x2E931d4b735F476E5edba95D0FEba9eb848cECD0", "WBTC"),   # WBTC
    ("0x4F287Dd8B2b02aA8885AB9C6DdCE876D1031268B", "USDT"),   # USDT
    ("0x25aF0AC22fdC2A408Ef07FcB795c516B3a0F3858", "Filecoin")    # Filecoin
]

# Chama a função para calcular o valor unitário, o valor de mercado e o total das reservas
valor_unitario, valor_mercado_total, total_tvl, total_tokens_asppbr, total_asppbr_reserve = calcular_valor_unitario_e_mercado(pair_addresses)

# Imprime os resultados formatados
print(f"O valor unitário de cada token ASPPBR é: ${valor_unitario:,.2f}")
print(f"O valor de mercado total dos tokens ASPPBR é: ${valor_mercado_total:,.2f}")
print(f"Total das Reservas de TVL: ${total_tvl:,.2f}")
print(f"Total das Reservas de Token ASPPBR: ${total_asppbr_reserve:,.2f}")
