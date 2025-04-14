import os
import time
import json
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware
from eth_account import Account
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

def calculate_token_value(amount, token_price_usd):
    """
    Função para calcular o valor do montante de token transferido em dólar.
    """
    token_value_usd = amount * token_price_usd
    return token_value_usd

def confirm_transaction(recipient, amount):
    """
    Função para solicitar confirmação do usuário antes de enviar a transação.
    """
    print("-" * 40)
    print(f"Você está prestes a transferir {amount} tokens para {recipient}.")
    confirmation = input("Deseja confirmar a transferência? (s/n): ")
    if confirmation.lower() != 's':
        print("Transferência cancelada.")
        return False
    return True

def transfer_tokens(contract_address, recipient, amount, account, private_key, web3, node_connections):
    """
    Função para transferir tokens para outro endereço, alternando entre os nós conectados.
    """
    # Lendo a ABI do arquivo
    with open('bep20_contract.abi', 'r') as abi_file:
        contract_abi = json.load(abi_file)

    for i, connection in enumerate(node_connections):
        try:
            # Confirmar a transação antes de prosseguir
            if not confirm_transaction(recipient, amount):
                return None
            
            print(f"Attempting to send transaction to node {i + 1}...")
            web3 = connection["web3"]
            contract = web3.eth.contract(address=contract_address, abi=contract_abi)
            recipient = web3.to_checksum_address(recipient)
            gas_price = web3.eth.gas_price
            gas_price_gwei = gas_price / 10**9
            gas_price_usd = gas_price_gwei * gwei_to_usd

            tx = contract.functions.transfer(recipient, amount).build_transaction({
                "chainId": web3.eth.chain_id,
                "gas": 2000000,
                "gasPrice": gas_price,
                "nonce": web3.eth.get_transaction_count(account),
                "from": account
            })
            
            signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            gas_used_wei = tx_receipt.gasUsed * gas_price  # Custo da transação em Wei
            gas_used_usd = tx_receipt.gasUsed * gas_price_gwei * gwei_to_usd  # Custo da transação em USD

            token_price_usd = 1.5  # Preço do token em dólar (ajustar conforme necessário)
            token_value_usd = calculate_token_value(amount, token_price_usd)

            print("Transaction Details:")
            print("-" * 40)
            print(f"Recipient Address: {recipient}")
            print(f"Amount Transferred: {amount} Tokens")
            print(f"Token Value (USD): ${token_value_usd:.2f}")
            print(f"Transaction Hash: {tx_hash.hex()}")
            print(f"Block Number: {tx_receipt.blockNumber}")
            print(f"Gas Used: {tx_receipt.gasUsed}")
            print(f"Gas Used (Wei): {gas_used_wei} Wei")
            print(f"Gas Used (USD): ${gas_used_usd:.2f}")
            print(f"Gas Price (Gwei): {gas_price_gwei} Gwei ({gas_price} wei)")
            print(f"Gas Price (USD): ${gas_price_usd:.10f}")
            print(f"Node: {connection['url']}")
            print("-" * 40)

            time.sleep(5)
            return tx_hash
        except Exception as e:
            print(f"Failed to send transaction to node {i + 1}: {e}")
            continue
    
    print("Failed to send transaction to any node.")
    return None

# Definir constantes e variáveis globais
# Lista de URLs dos nós RPC
node_urls = [
    os.getenv("NODE_URL_1"),
    os.getenv("NODE_URL_2"),
    os.getenv("NODE_URL_3"),
    os.getenv("NODE_URL_4")
]

default_account = os.getenv("DEFAULT_ACCOUNT")
private_key = os.getenv("PRIVATE_KEY")
contract_address = os.getenv("CONTRACT_ADDRESS")
# Lista de destinatários
recipient_addresses = [
    os.getenv("RECIPIENT_ADDRESS_1"),
    os.getenv("RECIPIENT_ADDRESS_2"),
    os.getenv("RECIPIENT_ADDRESS_3"),
    os.getenv("RECIPIENT_ADDRESS_4"),
    os.getenv("RECIPIENT_ADDRESS_5"),
    os.getenv("RECIPIENT_ADDRESS_6"),
    os.getenv("RECIPIENT_ADDRESS_7"),
    os.getenv("RECIPIENT_ADDRESS_8"),
    os.getenv("RECIPIENT_ADDRESS_9")
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

for recipient_address in recipient_addresses:
    transfer_amount = 1000
    tx_hash = transfer_tokens(contract_address, recipient_address, transfer_amount, default_account, private_key, web3, connections)
    if tx_hash:
        print(f"Tokens transferred to {recipient_address}. Amount: {transfer_amount}. Transaction Hash: {tx_hash.hex()}")
