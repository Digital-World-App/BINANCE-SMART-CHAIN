# BSC Wallet Generator

Este projeto é um **gerador de carteiras** para a **Binance Smart Chain (BSC)**. Ele permite a criação de múltiplas carteiras, fornecendo as seguintes informações para cada uma:

- **ID da carteira** (`wallet_id`)
- **Chave privada** (`private_key`)
- **Endereço público** (`public_address`)
- **Frase-semente** (`seed_phrase`)
- **Timestamp** da criação
- **Número do bloco mais recente** da rede BSC
- **URL do nó RPC** utilizado para conectar à BSC

---

## **Funcionalidades**

1. **Geração de Carteiras:** Criação de carteiras com chaves privadas, endereços públicos e frases-semente únicas.
2. **Conexão à Binance Smart Chain:** Conexão a nós RPC da Binance Smart Chain para obter o número do bloco mais recente.
3. **Armazenamento seguro das informações:** Todas as informações geradas são armazenadas de maneira estruturada em um arquivo JSON.
4. **Resiliência em conexões RPC:** A ferramenta tenta se conectar a múltiplos nós RPC configurados no arquivo `.env` para garantir maior estabilidade e confiabilidade.
5. **Personalização da criação de carteiras:** Permite ao usuário escolher o número de palavras para a frase-semente (12, 15, 18, 21 ou 24 palavras).

---

## **Pré-requisitos**

Antes de começar, certifique-se de ter os seguintes itens instalados:

- **Python 3.12** ou superior
- Um ambiente virtual Python configurado (opcional, mas recomendado)

Além disso, você precisará instalar as seguintes dependências:

- `python-dotenv`: Para carregar variáveis de ambiente do arquivo `.env`
- `web3`: Para interagir com a Binance Smart Chain
- `mnemonic`: Para gerar a frase-semente
- `eth-account`: Para criação e gerenciamento de contas Ethereum

---

## **Instalação**

Siga os passos abaixo para configurar e executar o projeto:

1. **Clone o repositório ou baixe os arquivos:**

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd BSC-Wallet
   
  ```

2. **Crie e ative um ambiente virtual (opcional):**

   ```bash
   python3.12 -m venv env
   source env/bin/activate  # Linux/macOS
   env\Scripts\activate   # Windows
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o arquivo `.env`:**
   Crie um arquivo chamado `.env` na raiz do projeto e adicione os seguintes links RPC da Binance Smart Chain:

   ```env
   # Configurações da Binance Smart Chain
   ## Rede Principal
   BINANCE_SMART_CHAIN_MAINNET_NODE_URL_1=https://bsc-dataseed1.binance.org/
   BINANCE_SMART_CHAIN_MAINNET_NODE_URL_2=https://bsc-dataseed2.binance.org/
   BINANCE_SMART_CHAIN_MAINNET_NODE_URL_3=https://bsc-dataseed3.binance.org/
   BINANCE_SMART_CHAIN_MAINNET_NODE_URL_4=https://bsc-dataseed4.binance.org/
   BINANCE_SMART_CHAIN_MAINNET_NODE_URL_5=https://bsc-dataseed1.defibit.io/
   BINANCE_SMART_CHAIN_MAINNET_NODE_URL_6=https://bsc-dataseed2.defibit.io/
   BINANCE_SMART_CHAIN_MAINNET_NODE_URL_7=https://bsc-dataseed3.defibit.io/
   BINANCE_SMART_CHAIN_MAINNET_NODE_URL_8=https://bsc-dataseed4.defibit.io/
   BINANCE_SMART_CHAIN_MAINNET_NODE_URL_9=https://bsc-dataseed1.ninicoin.io/
   BINANCE_SMART_CHAIN_MAINNET_NODE_URL_10=https://bsc-dataseed2.ninicoin.io/
   BINANCE_SMART_CHAIN_MAINNET_NODE_URL_11=https://bsc-dataseed3.ninicoin.io/
   BINANCE_SMART_CHAIN_MAINNET_NODE_URL_12=https://bsc-dataseed4.ninicoin.io/
   ```

5. **Execute o script:**
   Para gerar as carteiras, execute:

   ```bash
   python3.12 create_wallet.py
   ```

---

## **Uso**

1. Após rodar o comando acima, o script perguntará quantas carteiras você deseja gerar.
2. O script conectará à Binance Smart Chain usando os nós RPC definidos no `.env` e verificará o número do bloco mais recente.
3. Para cada carteira gerada, o script exibirá as informações no terminal e salvará todas em um arquivo JSON para consulta posterior.

---

## **Estrutura do Projeto**

```plaintext
BSC-Wallet/
├── create_wallet.py   # Script principal para geração de carteiras
├── .env               # Arquivo de variáveis de ambiente (não incluído no repositório por padrão)
├── requirements.txt   # Lista de dependências Python
└── wallet_data.json   # Arquivo gerado contendo as informações das carteiras
```

---

## **Saída do Script**

A saída gerada pelo script será semelhante ao exemplo abaixo:

```json
[
    {
        "wallet_id": "0000000000000000000000000000",
        "private_key": "0000000000000000000000000000000000000000000000",
        "public_address": "0000000000000000000000000000000000000000000",
        "seed_phrase": "brasileiro manguaceiro pinga brasielira cerveja beba com moderação caboco mineiro comedor queijo",
        "timestamp": "2025-01-05 14:53:51",
        "block_number": 45502553,
        "node_url": "https://bsc-dataseed2.binance.org/"
    }
]

```

- **`wallet_id`**: Um identificador único para a carteira gerada.
- **`private_key`**: A chave privada usada para assinar transações.
- **`public_address`**: O endereço público da carteira na BSC.
- **`seed_phrase`**: Uma frase-semente que pode ser usada para recuperar a carteira.
- **`timestamp`**: Data e hora da criação da carteira (formato UTC).
- **`block_number`**: O número do bloco mais recente da BSC.
- **`node_url`**: URL do nó RPC usado para conectar à blockchain.

---

## **Notas Importantes**

1. **Segurança:**
   - Nunca compartilhe sua chave privada ou frase-semente.
   - Armazene o arquivo `wallet_data.json` em um local seguro.

2. **Rede:**
   - Certifique-se de que você está conectado a um nó RPC confiável.
   - O script usa nós públicos, mas considere usar um nó privado para maior segurança e velocidade.

---

## **Contribuições**

Contribuições são bem-vindas! Para colaborar:

1. Faça um fork do repositório
2. Crie um branch para suas mudanças: `git checkout -b minha-mudanca`
3. Faça um commit das suas mudanças: `git commit -m 'Minha mudança'`
4. Envie suas mudanças para o branch principal: `git push origin minha-mudanca`
5. Abra um Pull Request

---

## **Licença**

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.
