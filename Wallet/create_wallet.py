import json
import random
import time
from datetime import datetime, timezone
from eth_account import Account
import mnemonic
import os
from dotenv import load_dotenv
from web3 import Web3
import uuid
import re

# Carregar as variáveis do arquivo .env
load_dotenv()

# Montar a lista de nós RPC a partir das variáveis do .env
node_urls = [
    os.getenv(f"BINANCE_SMART_CHAIN_MAINNET_NODE_URL_{i}")
    for i in range(1, 13)  # Alterar o intervalo conforme o número total de URLs
]

# Remover quaisquer valores `None` (caso alguma variável não esteja definida)
node_urls = [url for url in node_urls if url is not None]

def validate_node_url(node_url):
    """
    Função para validar a URL do nó RPC (verifica se é uma URL HTTP válida).
    """
    regex = re.compile(
        r'^(http|https)://[a-zA-Z0-9.-]+(?::\d+)?(/.*)?$'
    )
    return re.match(regex, node_url) is not None

def connect_to_node(node_url):
    """
    Função para conectar-se a um nó RPC e obter informações sobre o último bloco.
    """
    try:
        if not validate_node_url(node_url):
            raise ValueError(f"URL inválida para o nó RPC: {node_url}")
        
        web3 = Web3(Web3.HTTPProvider(node_url))
        
        # Testar a conexão obtendo o número do bloco
        latest_block = web3.eth.block_number
        if latest_block is None:
            raise ConnectionError(f"Falha ao conectar ao nó RPC: {node_url}")
        
        return {"url": node_url, "web3": web3, "latest_block": latest_block}
    
    except (ValueError, ConnectionError) as e:
        print(f"Erro de conexão ou URL inválida com {node_url}: {e}")
        return None
    except Exception as e:
        print(f"Erro desconhecido ao conectar-se a {node_url}: {e}")
        return None

def generate_seed(strength):
    """
    Função para gerar uma seed com base no tamanho da chave de recuperação.
    """
    word_list = mnemonic.Mnemonic("english").generate(strength=strength)
    return word_list.split()

def create_new_address(seed_strength):
    """
    Função para criar um novo endereço e gerar uma chave privada e uma seed.
    """
    Account.enable_unaudited_hdwallet_features()  # Habilitar recursos de mnemônico
    seed_phrase = generate_seed(seed_strength)
    new_account = Account.from_mnemonic(" ".join(seed_phrase))
    private_key = new_account._private_key.hex()
    public_address = new_account.address
    return private_key, public_address, seed_phrase

def save_wallet_to_file(wallet_data):
    """
    Função para salvar as carteiras geradas no arquivo JSON.
    """
    try:
        # Tenta abrir o arquivo e ler os dados existentes
        if os.path.exists("wallets.json"):
            with open("wallets.json", "r") as file:
                wallets = json.load(file)
        else:
            wallets = []  # Caso o arquivo não exista, inicializa uma lista vazia

        # Adiciona a nova carteira à lista de carteiras
        wallets.append(wallet_data)

        # Grava as carteiras de volta no arquivo JSON
        with open("wallets.json", "w") as file:
            json.dump(wallets, file, indent=4)

        print("Carteira salva com sucesso!")

    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON. O arquivo pode estar corrompido.")
        # Se o arquivo JSON estiver corrompido, criar um novo arquivo
        with open("wallets.json", "w") as file:
            json.dump([wallet_data], file, indent=4)
        print("Arquivo JSON corrompido. Um novo arquivo foi criado.")
    except PermissionError:
        print("Erro de permissão ao tentar acessar o arquivo wallets.json.")
    except Exception as e:
        print(f"Erro ao salvar as informações no arquivo: {e}")

def generate_wallets():
    """
    Função principal para gerar múltiplas carteiras.
    Pergunta ao usuário quantas carteiras deseja gerar e processa a criação.
    """
    num_wallets = int(input("Quantas carteiras você gostaria de gerar? "))
    
    # Definir as opções de tamanhos de palavras e forças
    word_sizes = {
        12: 128,
        15: 160,
        18: 192,
        21: 224,
        24: 256
    }
    
    for i in range(num_wallets):
        # Solicita ao usuário o tamanho da chave de recuperação
        print("Escolha o tamanho da chave de recuperação:")
        for words, strength in word_sizes.items():
            print(f"{words} palavras: Força {strength} bits")
        
        word_count = int(input("Digite o número de palavras para a chave de recuperação (12, 15, 18, 21, 24): "))
        if word_count not in word_sizes:
            print("Tamanho inválido. Usando 12 palavras por padrão.")
            word_count = 12  # Default to 12 words if invalid input

        # Escolher um nó aleatório da lista de nós disponíveis
        node_url = random.choice(node_urls)

        # Conectar-se ao nó
        connection_info = None
        attempts = 0
        while connection_info is None and attempts < 3:
            connection_info = connect_to_node(node_url)
            if connection_info is None:
                print(f"Tentando novamente com outro nó...")
                attempts += 1
                time.sleep(2)

        if connection_info:
            print("-" * 50)
            print(f"Conexão bem-sucedida com o nó: {connection_info['url']}")
            print(f"Número do último bloco: {connection_info['latest_block']}")
            print("-" * 50)

            # Criar um novo endereço
            new_private_key, new_public_address, seed_phrase = create_new_address(word_sizes[word_count])

            # Obter o timestamp atual em UTC
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

            # Gerar um ID único para a carteira
            wallet_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{new_public_address}-{timestamp}-{connection_info['latest_block']}"))

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
            print(f"Carteira {i + 1}/{num_wallets} gerada com sucesso.")
            time.sleep(0.1)  # Adicionar um pequeno delay entre as gerações
        else:
            print(f"Falha ao conectar a todos os nós. Tente mais tarde.")

# Executar a função para gerar carteiras
generate_wallets()
