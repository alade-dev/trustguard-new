import requests
import os
import re
import json
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain.schema.runnable import RunnablePassthrough
from web3 import Web3

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
# DUNE_API_KEY = os.getenv("DUNE_API_KEY")

GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
if not GOOGLE_GEMINI_API_KEY:
    raise ValueError("Google Gemini API key is missing. Set GOOGLE_GEMINI_API_KEY as an environment variable.")
if not ETHERSCAN_API_KEY:
    raise ValueError("Etherscan API key is missing. Set ETHERSCAN_API_KEY as an environment variable.")

gemini_llm = GoogleGenerativeAI(api_key=GOOGLE_GEMINI_API_KEY, model="gemini-1.5-flash")

def getETherBalance(WALLET_ADDRESS, ETHERSCAN_API_KEY):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={WALLET_ADDRESS}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    balance = int(data['result']) / 1e18
    return balance

def fetchTx(WALLET_ADDRESS, ETHERSCAN_API_KEY):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={WALLET_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    transactions = []
    if data["status"] == "1":
        transactions = data["result"]
    return transactions

def contractTx(WALLET_ADDRESS, ETHERSCAN_API_KEY):
    url_internal = f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={WALLET_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    response_internal = requests.get(url_internal)
    data_internal = response_internal.json()
    internal_txs = []
    if data_internal["status"] == "1":
        internal_txs = data_internal["result"]
    return internal_txs

def tokenTx(WALLET_ADDRESS, ETHERSCAN_API_KEY):
    url_token = f"https://api.etherscan.io/api?module=account&action=tokentx&address={WALLET_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    response_token = requests.get(url_token)
    data_token = response_token.json()
    token_txs = []
    if data_token["status"] == "1":
        token_txs = data_token["result"]
    return token_txs

def nft_token_tx(WALLET_ADDRESS, ETHERSCAN_API_KEY):
    url_token = f"https://api.etherscan.io/api?module=account&action=tokennfttx&address={WALLET_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    response_token = requests.get(url_token)
    data_token = response_token.json()
    nft_txs = []
    if data_token["status"] == "1":
        nft_txs = data_token["result"]
    return nft_txs

def getEthereumData(WALLET_ADDRESS, ETHERSCAN_API_KEY):
    data = {
        "balance": getETherBalance(WALLET_ADDRESS, ETHERSCAN_API_KEY),
        "normal_tx": fetchTx(WALLET_ADDRESS, ETHERSCAN_API_KEY),
        "internal_tx": contractTx(WALLET_ADDRESS, ETHERSCAN_API_KEY),
        "token_tx": tokenTx(WALLET_ADDRESS, ETHERSCAN_API_KEY),
        "nft_tx": nft_token_tx(WALLET_ADDRESS, ETHERSCAN_API_KEY)
    }
    return data

# Example usage


# ### AI to format and structure data

# # Prompt template for vulnerability analysis
# template = """You are a professional data analyst. You are provided with data about a wallet address to determine the reputation score.
# Identify the most critical vulnerability in the contract from the following categories:
# Overflow, Reentrancy, Frontrunning, Unauthorized Access, Gas Efficiency, Self-Destruct.
# For the identified vulnerability, provide a list of recommended fixes.
# Return a JSON object that follows this format:
# {format_instructions}

# # Vulnerability patterns and fixes
# VULNERABILITY_PATTERNS = {vulnerability_patterns}

# <smart contract>
# {smart_contract}
# </smart contract>
# """
template = PromptTemplate(
    input_variables=["wallet_address"],
    template="""
    You are a professional data analyst. You are provided with data about a wallet address to determine the reputation score.
    Analyze the blockchain wallet address: {wallet_address}.
    Provide insights on transaction history, security risks, and token distribution.
    - Number of transactions.
    - Assess token distribution and key holdings.
    - Provide an overall risk assessment and investment insights.
    Ensure your response is concise, professional, and actionable.
    """
)

wallet_analysis = template | gemini_llm | RunnablePassthrough()

def analyze_wallet():
    try:
        data = requests.json()
        wallet_address = data.get("wallet_address")
        if not wallet_address or not is_valid_eth_address(wallet_address):
            return json({"error": "wallet_address is required"}), 400
        
        transactions = fetchTx(wallet_address)
        transaction_count = len(transactions)

        if isinstance(transactions, dict) and "error" in transactions:
            return json(transactions), 500
        
        response = wallet_analysis.run(wallet_address=wallet_address, transaction_count=transaction_count)
        
        return json({"wallet_address": wallet_address, "analysis": response, "transaction_count": transaction_count})
    except Exception as e:
        return json({"error": str(e)}), 500


#Returns
# If the address is a contract or externally owned account
def is_valid_eth_address(address):
    return Web3.is_address(address)

#The age of the wallet
def fetch_transactions(WALLET_ADDRESS):
    """Fetch normal ETH transactions."""
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={WALLET_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("result", []) if data.get("status") == "1" else []

def calculate_wallet_age(WALLET_ADDRESS):
    """Determine wallet age from the first transaction."""
    transactions = fetch_transactions(WALLET_ADDRESS)
    if not transactions:
        return 0 
    first_tx_timestamp = int(transactions[0]["timeStamp"])
    first_tx_date = datetime.utcfromtimestamp(first_tx_timestamp)
    wallet_age_days = (datetime.utcnow() - first_tx_date).days
    return wallet_age_days

#The balance of the wallet
def fetch_token_holdings(WALLET_ADDRESS):
    """Fetch ERC-20 token balances."""
    url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={WALLET_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    tokens = {}
    if data.get("status") == "1":
        for tx in data["result"]:
            token_symbol = tx["tokenSymbol"]
            token_value = int(tx["value"]) / (10 ** int(tx["tokenDecimal"]))
            tokens[token_symbol] = tokens.get(token_symbol, 0) + token_value
    return tokens

def fetch_nft_holdings(WALLET_ADDRESS):
    """Fetch ERC-721 and ERC-1155 NFT holdings."""
    url = f"https://api.etherscan.io/api?module=account&action=tokennfttx&address={WALLET_ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()
    nfts = {}
    if data.get("status") == "1":
        for tx in data["result"]:
            nft_name = tx["tokenName"]
            nfts[nft_name] = nfts.get(nft_name, 0) + 1
    return nfts

#The number of transactions
def transaction_counts(WALLET_ADDRESS):
    """Analyze transaction success/failure rates and gas usage."""
    transactions = fetch_transactions(WALLET_ADDRESS)
    success_count = 0
    failed_count = 0
    high_gas_txs = 0
    gas_threshold = 0.01

    for tx in transactions:
        if tx["isError"] == "0":
            success_count += 1
        else:
            failed_count += 1
        gas_used = int(tx["gasUsed"]) * int(tx["gasPrice"]) / 1e18
        if gas_used > gas_threshold:
            high_gas_txs += 1

    return {"success_count": success_count, "failed_count": failed_count, "high_gas_txs": high_gas_txs}

# async def fetch_dune_analytics(wallet_address):
#   url = f"https://api.dune.com/api/v1/query/your-query-id/results?wallet={wallet_address}"
#  headers = {"Authorization": f"Bearer {DUNE_API_KEY}"}

#    async with aiohttp.ClientSession() as session:
#       async with session.get(url, headers=headers) as response:
#            if response.status != 200:
#                raise ValueError(f"Error: API responded with status {response.status}")

#            try:
#                data = await response.json()
#                if not data:
#                    raise ValueError("Dune API returned an empty response")
#                return data
#            except Exception:
#                raise ValueError("Failed to decode JSON from Dune API")


# The reputation of the address is 70/100
async def calculate_reputation_score(WALLET_ADDRESS):
    """Compute a reputation score based on multiple criteria."""
    wallet_age = calculate_wallet_age(WALLET_ADDRESS)
    tx_analysis = transaction_counts(WALLET_ADDRESS)
    token_holdings = fetch_token_holdings(WALLET_ADDRESS)
    nft_holdings = fetch_nft_holdings(WALLET_ADDRESS)

    score = 100

    if wallet_age < 30:
        score -= 10
    elif wallet_age < 90:
        score -= 5

    # Transaction Failure Rate Penalty
    failure_rate = tx_analysis["failed_count"] / max(1, tx_analysis["success_count"] + tx_analysis["failed_count"])
    if failure_rate > 0.3:
        score -= 20
    elif failure_rate > 0.1:
        score -= 10

    # High Gas Usage
    if tx_analysis["high_gas_txs"] > 10:
        score -= 5

    if len(token_holdings) > 5:
        score += 5
    if len(nft_holdings) > 3:
        score += 5

    score = max(0, min(100, score))
    return {
        "wallet_address": WALLET_ADDRESS,
        "wallet_age_days": wallet_age,
        "transaction_analysis": tx_analysis,
        "token_holdings": token_holdings,
        "nft_holdings": nft_holdings,
        "reputation_score": score
    }


if __name__ == "__main__":
    async def main():
        # ethereum_data = getEthereumData(WALLET_ADDRESS, ETHERSCAN_API_KEY)
        reputation_data = await calculate_reputation_score(WALLET_ADDRESS)
        ethereum_data = fetch_transactions(WALLET_ADDRESS)

        print(json.dumps(reputation_data, indent=4))
        print(json.dumps(ethereum_data, indent=4))

    asyncio.run(main()) 