
![ID ASPPIBRA-DAO](https://github.com/user-attachments/assets/a6540bf2-9dec-4042-a528-cdb6686b91cf)
![Card VIP ASPPIBRA-DAO1](https://github.com/user-attachments/assets/e5afb5f4-9b1a-4014-afcd-f6598af6ab5e)

# 📦 Blockchain Toolkit

Este repositório contém um conjunto de ferramentas e utilitários desenvolvidos em Python para interagir com contratos inteligentes, consultar APIs de preços e analisar liquidez de tokens na Binance Smart Chain (BSC). O projeto está organizado em módulos específicos para facilitar a manutenção e a expansão.

---

## 📁 Estrutura do Projeto

. ├── API/ ├── Inspetor Smart Contract/ ├── Pool/ ├── Smart Contract/ ├── Wallet/ ├── requirements.txt └── README.md

---

## 🔍 Descrição dos Diretórios e Arquivos

### 🧠 API/

Scripts para integração com diversas APIs de dados relacionados a blockchain e criptomoedas.

- `0x.py`: Integração com a API da 0x (protocolos de troca descentralizada).
- `bsc.py`: Conexão e utilitários para a Binance Smart Chain.
- `coingecko.py`: Consulta de preços e dados de mercado via CoinGecko.
- `coinmarketcap.py`: Consulta de dados de mercado via CoinMarketCap.
- `dexscreener.py`: Acesso a informações de liquidez e pares via DEX Screener.
- `pancakeswap.py`: Consulta de pools e swaps via PancakeSwap.
- `tradingstrategy.py`: Estratégias automatizadas de trading baseadas em dados externos.

---

### 🔎 Inspetor Smart Contract/

Scripts e arquivos para análise e decodificação de contratos BEP-20.

- `bep20_contract.abi`: Interface ABI de um contrato padrão BEP-20.
- `bep20_contract_analysis.py`: Script para inspeção e análise de contratos inteligentes BEP-20.

---

### 💧 Pool/

Gerenciamento de pools de liquidez.

- `liquidity_pool_bsc.abi`: ABI de contrato de pool de liquidez.
- `pool.py`: Script para consultar e interagir com pools de liquidez na BSC.

---

### 📜 Smart Contract/

Execução e manipulação de transações em contratos inteligentes.

- `transection.py`: Envio e monitoramento de transações na BSC.

---

### 👛 Wallet/

Criação e gerenciamento de carteiras.

- `create_wallet.py`: Geração de novas carteiras (chaves públicas e privadas).
- `wallets.json`: Armazenamento local de carteiras geradas.
- `README.md`: Documentação específica do módulo Wallet.

---

## 📦 Requisitos

Instale as dependências do projeto com:

```bash
pip install -r requirements.txt
