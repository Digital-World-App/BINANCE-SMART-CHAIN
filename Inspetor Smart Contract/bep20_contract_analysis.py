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

def query_contract_info(contract_address, web3, default_account, contract_abi):
    """
    Consulta informações sobre um contrato BEP-20.
    Retorna um dicionário com os detalhes do contrato ou None em caso de erro.
    """
    try:
        # Estabelecendo a conexão com o contrato
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)
        
        # Consultando informações do contrato
        symbol = contract.functions.symbol().call()
        name = contract.functions.name().call()
        decimals = contract.functions.decimals().call()
        total_supply = contract.functions.totalSupply().call()
        token_type = "Fungível"  # Assumindo que todos os tokens são fungíveis

        # Formatando as informações de oferta total
        total_supply_formatted = f"{total_supply:,} {symbol}"

        # Retornando informações do contrato como um dicionário
        return {
            "symbol": symbol,
            "name": name,
            "contract_address": contract_address,
            "decimals": decimals,
            "total_supply": total_supply_formatted,
            "token_type": token_type
        }
    except Exception as e:
        print(f"Error querying contract {contract_address}: {e}")
        return None

# Lendo a ABI do arquivo uma vez para o escopo global
with open('bep20_contract.abi', 'r') as abi_file:
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
private_key = os.getenv("MAINNET_PRIVATE_KEY")
contract_address = os.getenv("MAINNET_CONTRACT_ADDRESS")

# Lista de destinatários
contract_addresses = [    
    os.getenv("BEP20_CONTRACT_ANALYSIS_1"), 
    os.getenv("BEP20_CONTRACT_ANALYSIS_2"), 
    os.getenv("BEP20_CONTRACT_ANALYSIS_3"), 
    os.getenv("BEP20_CONTRACT_ANALYSIS_4"), 
    os.getenv("BEP20_CONTRACT_ANALYSIS_5"), 
    os.getenv("BEP20_CONTRACT_ANALYSIS_6")    
]


gwei_to_usd = 0.000000001

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
for address in contract_addresses:
    contract_info = query_contract_info(address, web3, default_account, contract_abi)
    if contract_info:
        print("-" * 50)
        print(f"Contract Address: {contract_info['contract_address']}")
        print(f"Name: {contract_info['name']}")
        print(f"Symbol: {contract_info['symbol']}")
        print(f"Decimals: {contract_info['decimals']}")
        print(f"Total Supply: {contract_info['total_supply']}")
        print(f"Token Type: {contract_info['token_type']}")
        print("-" * 50)
    else:
        print(f"Failed to query contract {address}")
