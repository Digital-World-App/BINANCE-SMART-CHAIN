import requests
import time
import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()


# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Obter API Key de variáveis de ambiente
API_KEY = os.getenv("ZEROX_API_KEY")
if not API_KEY:
    raise ValueError("A chave da API não foi encontrada. Defina a variável de ambiente 'ZEROX_API_KEY'.")

def get_token_price(sell_token: str, buy_token: str, sell_amount: int) -> Optional[float]:
    """
    Obtém o preço de um token em relação a outro usando a API 0x.

    Args:
        sell_token (str): Endereço do token a ser vendido.
        buy_token (str): Endereço do token a ser comprado.
        sell_amount (int): Quantidade do token a ser vendido (em unidades menores, como wei).

    Returns:
        Optional[float]: O preço do token em relação ao token de compra ou None em caso de erro.
    """
    if not (sell_token and buy_token and sell_amount > 0):
        logging.error("Parâmetros inválidos. Certifique-se de que os tokens e o valor de venda são válidos.")
        return None

    url = "https://bsc.api.0x.org/swap/v1/price"
    params = {
        "sellToken": sell_token,
        "buyToken": buy_token,
        "sellAmount": sell_amount
    }
    headers = {
        "0x-api-key": API_KEY
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Lança exceção para erros HTTP
        data = response.json()
        price = data.get("price")
        if price is None:
            logging.error("Resposta da API não contém o campo 'price'.")
        return float(price) if price else None
    except requests.exceptions.Timeout:
        logging.error("A solicitação à API expirou.")
    except requests.exceptions.ConnectionError:
        logging.error("Erro de conexão com a API.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na solicitação à API: {e}")
    return None

def main():
    sell_token = "0x0697AB2B003FD2Cbaea2dF1ef9b404E45bE59d4C"  # Endereço do ASPPBR
    buy_token = "0x55d398326f99059fF775485246999027B3197955"  # Endereço do USDT
    sell_amount = 10_000_000  # 10 USDC (USDC tem uma unidade base de 6)

    try:
        while True:
            token_price = get_token_price(sell_token, buy_token, sell_amount)
            if token_price:
                logging.info(f"Preço do token em dólares americanos: {token_price:.6f}")
            else:
                logging.warning("Não foi possível obter o preço do token.")
            time.sleep(5)  # Espera 5 segundos antes da próxima consulta
    except KeyboardInterrupt:
        logging.info("Execução interrompida pelo usuário.")

if __name__ == "__main__":
    main()














