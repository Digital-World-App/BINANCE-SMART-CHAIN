import os
import json
from web3 import Web3
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def connect_to_node(node_urls):
    """
    Função para conectar-se a cada nó RPC da lista e obter informações sobre o último bloco.
    """
    successful_connections = []
    for url in node_urls:
        try:
            web3 = Web3(Web3.HTTPProvider(url))
            latest_block = web3.eth.block_number
            print(f"Connected to {url}. Latest Block Number: {latest_block}")
            successful_connections.append({"url": url, "web3": web3, "latest_block": latest_block})
        except Exception as e:
            print(f"Failed to connect to {url}: {e}")
    return successful_connections

def query_contract_info(contract_address, web3, contract_abi):
    """
    Consulta informações sobre um contrato BEP-20.
    Retorna um dicionário com os detalhes do contrato ou None em caso de erro.
    """
    try:
        # Estabelecendo a conexão com o contrato
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)
        
        # Consultando informações do contrato
        symbol = contract.functions.symbol().call()
        token0 = contract.functions.token0().call()
        token1 = contract.functions.token1().call()
        total_supply = contract.functions.totalSupply().call()
        balance = contract.functions.balanceOf(default_account).call() if default_account else None
        decimals = contract.functions.decimals().call()
        reserves = contract.functions.getReserves().call()

        # Retornando informações do contrato como um dicionário
        return {
            "address": contract_address,
            "symbol": symbol,
            "token0": token0,
            "token1": token1,
            "totalSupply": total_supply,
            "balance": balance,
            "decimals": decimals,
            "reserves": reserves,
        }
    except Exception as e:
        print(f"Error querying contract {contract_address}: {e}")
        return None

def somar_reservas_token0(contratos):
    """
    Soma o valor total das reservas do Token0 em todos os contratos.
    """
    total_reservas_token0 = 0
    for contrato in contratos:
        if contrato and 'reserves' in contrato:
            for reserve in contrato['reserves']:
                if isinstance(reserve, (list, tuple)):
                    total_reservas_token0 += reserve[0]  # O primeiro elemento em cada reserva é o valor do Token0
                else:
                    total_reservas_token0 += reserve  # Se reserve não for uma lista ou tupla, adiciona-se diretamente
    return total_reservas_token0

# Lendo a ABI do arquivo uma vez para o escopo global
with open('liquidity_pool_bsc.abi', 'r') as abi_file:
    contract_abi = json.load(abi_file)


# Definir constantes e variáveis globais
# Lista de URLs dos nós RPC
node_urls = [
    os.getenv("BINANCE_SMART_CHAIN_MAINNET_NODE_URL_1"),
    os.getenv("BINANCE_SMART_CHAIN_MAINNET_NODE_URL_2"),
    os.getenv("BINANCE_SMART_CHAIN_MAINNET_NODE_URL_3"),
    os.getenv("BINANCE_SMART_CHAIN_MAINNET_NODE_URL_4"),
    os.getenv("BINANCE_SMART_CHAIN_MAINNET_NODE_URL_5"),
    os.getenv("BINANCE_SMART_CHAIN_MAINNET_NODE_URL_6"),
    os.getenv("BINANCE_SMART_CHAIN_MAINNET_NODE_URL_7"),
    os.getenv("BINANCE_SMART_CHAIN_MAINNET_NODE_URL_8"),
    os.getenv("BINANCE_SMART_CHAIN_MAINNET_NODE_URL_9"),
    os.getenv("BINANCE_SMART_CHAIN_MAINNET_NODE_URL_10"),
    os.getenv("BINANCE_SMART_CHAIN_MAINNET_NODE_URL_11"),
    os.getenv("BINANCE_SMART_CHAIN_MAINNET_NODE_URL_12")
]

default_account = os.getenv("MAINNET_DEFAULT_ACCOUNT")
contract_address = os.getenv("MAINNET_CONTRACT_ADDRESS")

# Lista de destinatários
contract_addresses = [    
    os.getenv("LIQUIDITY_POOL_CONTRACT_1"), 
    os.getenv("LIQUIDITY_POOL_CONTRACT_2"), 
    os.getenv("LIQUIDITY_POOL_CONTRACT_3"), 
    os.getenv("LIQUIDITY_POOL_CONTRACT_4"), 
    os.getenv("LIQUIDITY_POOL_CONTRACT_5"), 
    os.getenv("LIQUIDITY_POOL_CONTRACT_6")    
]

connections = connect_to_node(node_urls)

if connections:
    print("-" * 50)
    print("Connection Successful")
    print("Connected to the following nodes:")
    for connection in connections:
        print("URL:", connection["url"])
        print("Latest Block Number:", connection["latest_block"])
        print("-" * 50)
else:
    print("No successful connections established.")

for connection_info in connections:
    if connection_info:
        print("-" * 50)
        print("Connection Successful")
        print("Connected to:", connection_info["url"])
        print("Latest Block Number:", connection_info["latest_block"])
        print("-" * 50)
        web3 = connection_info["web3"]
        break
else:
    print("No successful connections established.")

# Iteração sobre uma lista de endereços de contrato
contratos = []
for address in contract_addresses:
    contract_info = query_contract_info(address, web3, contract_abi)
    if contract_info:
        contratos.append(contract_info)
        print("-" * 50)
        print(f"Endereço do Contrato: {contract_info['address']}")
        print(f"Símbolo: {contract_info['symbol']}")
        print(f"Token0: {contract_info['token0']}")
        print(f"Token1: {contract_info['token1']}")
        print(f"Fornecimento Total: {contract_info['totalSupply']:,}")
        print(f"Saldo da Conta Padrão: {contract_info['balance']}")
        print(f"Casas Decimais: {contract_info['decimals']}")
        print("Reservas:")
        for reserve in contract_info['reserves']:
            print(f"{reserve:,}")
        print("-" * 50)
    else:
        print(f"Failed to query contract {address}")

# Somar as reservas do Token0 em todos os contratos
total_reservas_token0 = somar_reservas_token0(contratos)

# Formatar o número para torná-lo mais legível
total_reservas_token0_formatado = "{:,.2f}".format(total_reservas_token0)
print("Total de Reservas de Token0 em Todos os Contratos:", total_reservas_token0_formatado)
