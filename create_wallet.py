from web3 import Web3
from eth_account import Account
import mnemonic  # Importando o módulo mnemonic
import json
import random
import time
from datetime import datetime, timezone

# Lista de nós RPC da Binance Smart Chain (BSC)
node_urls = [
    "https://bsc-dataseed1.binance.org/",
    "https://bsc-dataseed2.binance.org/",
    "https://bsc-dataseed3.binance.org/",
    "https://bsc-dataseed4.binance.org/",
    "https://bsc-dataseed1.defibit.io/",
    "https://bsc-dataseed2.defibit.io/",
    "https://bsc-dataseed3.defibit.io/",
    "https://bsc-dataseed4.defibit.io/",
    "https://bsc-dataseed1.ninicoin.io/",
    "https://bsc-dataseed2.ninicoin.io/",
    "https://bsc-dataseed3.ninicoin.io/",
    "https://bsc-dataseed4.ninicoin.io/"
]

def connect_to_node(node_url):
    """
    Função para conectar-se a um nó RPC e obter informações sobre o último bloco.

    Parâmetros:
    - node_url: URL do nó RPC.

    Retorna:
    Um dicionário contendo informações sobre a conexão, incluindo a URL do nó, uma instância Web3 e o número do último bloco.
    """
    try:
        web3 = Web3(Web3.HTTPProvider(node_url))
        latest_block = web3.eth.block_number
        return {"url": node_url, "web3": web3, "latest_block": latest_block}
    except Exception as e:
        print(f"Error connecting to {node_url}: {e}")
        return None

def generate_seed():
    """
    Função para gerar uma seed de 12 palavras.

    Retorna:
    A seed de 12 palavras.
    """
    word_list = mnemonic.Mnemonic("english").generate(strength=128)
    return word_list.split()

def create_new_address():
    """
    Função para criar um novo endereço na blockchain.

    Retorna:
    A chave privada, o endereço público e a seed de 12 palavras do novo endereço criado.
    """
    Account.enable_unaudited_hdwallet_features()  # Habilitar recursos de mnemônico
    seed_phrase = generate_seed()
    new_account = Account.from_mnemonic(" ".join(seed_phrase))
    private_key = new_account._private_key.hex()
    public_address = new_account.address
    return private_key, public_address, seed_phrase

def save_wallet_to_file(wallet_data):
    """
    Função para salvar as carteiras geradas no arquivo JSON.

    Parâmetros:
    - wallet_data: Dado da carteira a ser salvo.
    """
    try:
        with open("wallets.json", "r") as file:
            wallets = json.load(file)
    except FileNotFoundError:
        wallets = []

    wallets.append(wallet_data)

    with open("wallets.json", "w") as file:
        json.dump(wallets, file, indent=4)

def generate_wallets():
    """
    Função principal para gerar múltiplas carteiras.

    Pergunta ao usuário quantas carteiras deseja gerar e processa a criação.
    """
    num_wallets = int(input("Quantas carteiras você gostaria de gerar? "))

    for i in range(num_wallets):
        # Escolher um nó aleatório da lista de nós disponíveis
        node_url = random.choice(node_urls)

        # Conectar-se ao nó
        connection_info = connect_to_node(node_url)
        if connection_info:
            print("-" * 50)
            print("Connection Successful")
            print("Connected to:", connection_info["url"])
            print("Latest Block Number:", connection_info["latest_block"])
            print("-" * 50)
            web3 = connection_info["web3"]

            # Criar um novo endereço
            new_private_key, new_public_address, seed_phrase = create_new_address()

            # Obter o timestamp atual em UTC
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

            # Gerar um ID único para a carteira
            unique_data = f"{new_public_address}-{timestamp}-{connection_info['latest_block']}"
            wallet_id = hash(unique_data)

            # Salvar os dados da carteira em um dicionário
            wallet_data = {
                "wallet_id": wallet_id,
                "private_key": new_private_key,
                "public_address": new_public_address,
                "seed_phrase": " ".join(seed_phrase),
                "timestamp": timestamp,
                "block_number": connection_info["latest_block"],
                "node_url": connection_info["url"]
            }

            # Salvar no arquivo JSON
            save_wallet_to_file(wallet_data)
            print(f"Generated wallet {i + 1}/{num_wallets}")
            time.sleep(0.1)  # Adicionar um pequeno delay entre as gerações
        else:
            print(f"Failed to connect to {node_url}. Trying another node...")

# Executar a função para gerar carteiras
generate_wallets()
